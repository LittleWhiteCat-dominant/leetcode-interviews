# System Design Mock Interview: Reservation & Inventory Management for Direct-to-Consumer Vehicle Sales

**Company theme:** Rivian-style direct-to-consumer (DTC) automaker — no dealership/franchise network, all sales happen through Rivian's own configurator, reservation, and delivery pipeline.
**Round:** System Design (45-60 min onsite loop)
**Interviewer expectation:** This is the one question in Rivian's system design rotation that is *intentionally not* vehicle-hardware/connectivity-themed. It doesn't test offline-first agents or OTA rollout mechanics — it tests general distributed-systems and e-commerce design fluency (consistency vs. availability, concurrency control, workflow/state-machine design), applied to a genuinely different constraint: the "inventory" isn't a warehouse SKU with 10,000 fungible units, it's a finite, physical, serialized good (a VIN) tied to a scarce factory production schedule.

This document is written as a self-contained interview walkthrough: it includes the clarifying questions you should ask, a model answer for each section, and the follow-up probes an interviewer is likely to throw at you.

---

## 0. Opening: Clarify the Problem (first 3-5 minutes)

Don't start designing immediately. Restate the prompt and ask clarifying questions to narrow scope. Sample dialogue:

> **You:** "Before I dive in, I want to flag something: this feels like a general e-commerce/inventory design question rather than a vehicle-connectivity one — is that a fair reading, or is there a hardware/telemetry angle you want me to fold in?"
>
> **Interviewer:** "Correct, no hardware angle. Treat this like designing checkout and fulfillment for a company that sells a physical, highly configurable, expensive product directly to consumers, with no dealer network."
>
> **You:** "Got it. A few more questions:
> 1. Is a vehicle 'unit' always something built to order, or can customers also buy an already-built vehicle sitting in finished-goods inventory?
> 2. When a customer configures a trim/color/options combination, are we responsible for telling them whether and when it can be built, given factory capacity?
> 3. Should I design the full order lifecycle through delivery, or just the reservation/checkout front-door?
> 4. Is payment processing something I need to design (PCI compliance, card networks), or can I treat it as an external system?
> 5. Is this single-region (US) or do I need to think about multi-region/international allocation from the start?"

Assume the interviewer answers:
- Both paths matter: most orders are build-to-order against future production slots, but a meaningful fraction buy an already-built VIN sitting at a delivery hub (cancellations, overproduction buffer, test/loaner fleet rotation).
- Yes — checking buildability against current factory allocation and giving an honest estimated delivery window is a core function, not a nice-to-have.
- Design the full lifecycle: reservation → order → production → delivery, since state transitions and cancellation/change rules at each stage are the interesting part of this problem.
- Treat payment/deposit capture as an external, PCI-compliant processor we integrate with via tokenized references — don't design the payment gateway itself, but do call out where it sits as a system boundary.
- Start single-region (US, one primary assembly plant), but mention how regional allocation would generalize as a follow-up.

---

## 1. Functional Requirements

State these explicitly on the whiteboard before designing anything.

1. **Configuration & buildability check** — given a trim/color/options selection, tell the customer whether that exact configuration is currently orderable and provide an estimated delivery window based on current factory allocation.
2. **Reservation with deposit hold** — let a customer place a refundable deposit to hold either (a) a future production slot for a build-to-order configuration, or (b) a specific already-built VIN from existing finished-goods inventory.
3. **Overselling prevention** — under concurrent demand for a limited allocation (a popular configuration, a limited "Launch Edition," or a specific VIN), never let two customers successfully hold/pay for the same slot or the same physical vehicle.
4. **Order lifecycle management** — track an order through reservation → configuration lock → production → build → quality inspection → delivery logistics → handoff, exposing the current state to both the customer and internal operations.
5. **Configuration change & cancellation rules gated by stage** — allow changes (e.g., exterior color) up until a hard cutoff tied to the physical build process (e.g., before paint has started), and enforce different cancellation/refund policies at each stage.
6. **Allocation & rationing under scarcity** — when demand for a configuration/region exceeds factory capacity for a given production period, manage a fair, ordered waitlist rather than an uncontrolled race.
7. **Reservation → VIN binding** — once a physical vehicle finishes production and passes quality inspection, bind it to the correct order (or, for the buy-from-inventory path, bind an already-existing VIN at hold time).
8. **Payment/deposit orchestration** — authorize a deposit hold at reservation time, capture it at order confirmation, and handle refunds on cancellation, all via an external payment processor.
9. **Customer-facing status visibility** — real-time order status, estimated delivery window, and clear communication about what can/can't still be changed.
10. **Operational visibility** — dashboards for factory allocation vs. demand, waitlist depth per configuration/region, and conversion funnel from reservation to delivered order.
11. **Audit trail** — every state transition, configuration change, and allocation decision is logged immutably, since this system moves real money and makes binding promises to consumers (relevant for financial reconciliation and consumer-protection disputes).

**Out of scope (state this explicitly):** the manufacturing execution system (MES) that sequences robots and line stations on the factory floor, the PCI-compliant payment gateway itself, and route/logistics optimization for physical vehicle transport — assume these are external systems we integrate with via well-defined APIs.

---

## 2. Non-Functional Requirements

| Requirement | Target / Reasoning |
|---|---|
| **Consistency (checkout path)** | Strong consistency is mandatory at the moment of deposit capture / order confirmation: the same production slot or the same physical VIN must never be allocated to two customers. This is a hard correctness constraint, not a tunable trade-off. |
| **Availability (browse/configure path)** | The configurator and delivery-estimate pages should stay available and fast even during a flash-demand event, tolerating a small amount of staleness in the displayed "estimated delivery window." |
| **Scalability (bursty, event-driven)** | Baseline traffic is modest, but a model reveal or new-trim announcement can drive 10-50x normal reservation volume within minutes — design for spiky, event-driven load, not smooth diurnal growth. |
| **Latency (checkout path)** | A reservation hold decision should return in well under a second; customers abandon carts quickly, and a slow "is this available?" check during a launch event is a lost sale. |
| **Durability** | Reservations, orders, and payment references are financial records — zero data loss, point-in-time recoverable, retained for years for tax/audit purposes. |
| **Fairness / auditability of rationing** | When demand exceeds supply, the allocation/waitlist ordering logic must be deterministic and explainable after the fact — "why did customer A get a slot before customer B" must have a defensible answer. |
| **Security** | No raw payment card data touches our systems (PCI scope stays with the external processor); strict ownership checks so customers can only view/modify their own orders. |
| **Observability** | Allocation utilization, hold-to-conversion rate, and waitlist velocity must be visible near-real-time to catch both technical issues (counter drift) and business issues (a region undershooting/overshooting its allocation). |

Call out explicitly to the interviewer: *"This is fundamentally a CAP-style trade-off problem: the read-heavy browsing/estimation path should be optimized for availability and can tolerate staleness, while the narrow checkout/payment/VIN-binding path must be optimized for strong consistency, even at some cost to availability or latency. Splitting the system along that line is the central design decision here."*

---

## 3. Back-of-the-Envelope Capacity Estimation

Doing this out loud shows quantitative rigor.

- **Factory production rate:** assume a combined run-rate of ~150,000 vehicles/year across current models, scaling toward ~300,000/year as a second plant ramps — that's roughly `150,000 / 52 ≈ 2,900 vehicles/week` today, designing headroom for ~6,000/week at scale.
- **Order-to-delivery cycle time:** assume an average of ~4 months from reservation to delivery (production scheduling lead time + build + transit). With 300,000 orders/year at steady state and a 4-month pipeline, the number of orders "in flight" at any given time is roughly `300,000 × (4/12) ≈ 100,000 concurrent open orders` across all lifecycle stages — this is the working-set size the order-management system must serve efficiently, not the full historical order count.
- **Steady-state reservation rate:** `300,000 orders/year / 365 ≈ 820 new reservations/day` on average — a small, unremarkable number for a database.
- **Flash-demand event:** a real-world analog is useful here — a major new-model reveal can generate on the order of tens of thousands of reservations within 24 hours (comparable to reported EV preorder events in this range). Assume **50,000 reservation attempts in the first 24 hours**, averaging `50,000 / 86,400s ≈ 0.6 req/s`, but the true danger is the burst in the first few minutes right after a livestream/announcement ends: a 10-30x instantaneous multiplier over the average is realistic, i.e. **peak bursts of a few hundred to ~1,000 reservation attempts/second for a short window**, heavily concentrated on a handful of "hero" configurations (the exact trim/color shown on stage).
- **Contention hotspot size:** a "Launch Edition" allocation might be capped at, say, 7,500 units globally. That means the *specific row(s)* representing that allocation's remaining-capacity counter could see thousands of concurrent read-modify-write attempts within seconds — a tiny amount of data, but an extreme concurrency hotspot.
- **Entity volumes:** `VehicleConfiguration` rows are small in number (thousands, bounded by valid trim × color × option combinations after a compatibility engine prunes invalid combos); `FactoryAllocation` rows are one per (plant, production-period, region, config-bucket) — low tens of thousands even over years; `Reservation`/`Order` rows accumulate to the low millions over the company's lifetime; `VehicleUnit` (VIN) rows grow by exactly the production rate — a few hundred thousand per year, trivial for a modern OLTP store.

Conclusion to state out loud: *"The bottleneck here is never raw storage or read throughput — it's write contention on a tiny number of hot counters (allocation pools for popular configurations) during short, predictable bursts around launch events. That's fundamentally a concurrency-control and queueing problem, not a capacity problem, and it should shape the design of the checkout path specifically, while the rest of the system (browsing, order tracking, dashboards) can use conventional, simpler patterns."*

---

## 4. Data Model / Database Design

### Core entities

**`VehicleConfiguration`** (a specific, validated, buildable spec)
```
config_id (PK)
model                  -- e.g. R1T, R1S, R2
trim
exterior_color
options                -- JSON array of option codes (wheels, ADAS package, interior, drivetrain)
compatibility_hash      -- derived hash confirming this is a validated, buildable combination
msrp_cents
orderable                -- whether currently open for new reservations
created_at, updated_at
```

**`FactoryAllocation`** (finite build capacity for a config-bucket in a given period/region — the scarce resource at the heart of this system)
```
allocation_id (PK)
plant_id                -- e.g. "normal-il", "stanton-ga"
production_week          -- ISO week, the target build period
region                     -- allocation is split by market/region for logistics and fairness reasons
config_bucket              -- a coarser grouping than config_id (e.g. model + trim + drivetrain) matching real line build-mix constraints
capacity_units              -- total slots available in this bucket/week
reserved_units               -- units currently held or confirmed (see concurrency section, 6.1)
version                       -- optimistic-concurrency stamp, incremented on every update
```

**`Reservation`** (customer intent + a soft hold, before payment is finalized)
```
reservation_id (PK)
customer_id
config_id (FK)
allocation_id (FK, nullable)              -- set for the build-to-order path
existing_vehicle_unit_id (FK, nullable)   -- set for the buy-from-inventory path
status                -- PENDING_HOLD / HELD / EXPIRED / CONVERTED_TO_ORDER / CANCELLED
hold_expires_at        -- TTL before an unconfirmed hold auto-releases
deposit_amount_cents
deposit_payment_ref     -- opaque reference into the external payment processor
target_delivery_window
idempotency_key          -- client-supplied, prevents duplicate holds on retry
created_at, updated_at
```

**`Order`** (a confirmed, paid commitment — created when a `Reservation` is successfully converted)
```
order_id (PK)
reservation_id (FK)
customer_id
config_id                -- frozen copy at confirmation time, immutable audit reference
vehicle_unit_id (FK, nullable)    -- bound once production/QA completes (or immediately, for buy-from-inventory)
production_slot_id (FK, nullable)
state       -- CONFIRMED / CONFIG_LOCKED / IN_PRODUCTION / PAINT_STARTED / BUILT /
            --   QA_INSPECTION / IN_TRANSIT / READY_FOR_DELIVERY / DELIVERED / CANCELLED
config_lock_at            -- timestamp the change window closed
total_price_cents
payment_status
created_at, updated_at
```

**`VehicleUnit`** (a specific, serialized, physical vehicle — exists only once actually built)
```
vin (PK)
config_id
plant_id
production_slot_id
build_started_at
build_completed_at
qa_status                 -- PENDING / PASSED / FAILED / REWORK
current_location            -- plant / rail / delivery-hub / in-transit / with-customer
order_id (nullable)           -- null while sitting as unsold finished-goods inventory
status      -- IN_PRODUCTION / BUILT / QA_PASSED / QA_FAILED / IN_TRANSIT / AT_HUB / DELIVERED
```

**`Waitlist`** (fair-ordering queue when demand exceeds a `FactoryAllocation` bucket's capacity)
```
waitlist_id (PK)
customer_id
config_bucket
region
priority_score        -- composite of tier weight (e.g., expiring-lease customer) + queue timestamp
queued_at
status                  -- WAITING / OFFERED / EXPIRED / CONVERTED
offer_expires_at
```

**`OrderStateEvent`** (append-only audit log, one row per transition — mirrors the audit-log pattern used for compliance-sensitive systems)
```
event_id (PK)
order_id
from_state, to_state
actor            -- customer / system / ops-agent, plus identifier
timestamp
metadata (JSON)   -- reason codes, related config diff, refund amount, etc.
```

### Key partitioning and storage-engine trade-offs

The interesting split here is not hot-state-vs-audit-log (though `OrderStateEvent` should still live in an append-optimized store for the same reasons as in a telemetry/audit system) — it's **narrow hot rows vs. everything else**. `FactoryAllocation.reserved_units` for a handful of popular buckets is read-modify-written by thousands of concurrent requests in a tight burst, while `VehicleConfiguration`, `Order`, and `VehicleUnit` see comparatively ordinary OLTP traffic. Narrate this explicitly: *"I want to treat the allocation-counter hot path as a special case — probably backed by an in-memory atomic-counter store with a short-lived reservation token, reconciled into the durable relational system of record — rather than force the same row-locking relational pattern to absorb a launch-day burst it wasn't sized for."* (Detailed in section 6.1.)

`Order` and `VehicleUnit` should be partitioned/sharded by a hash of `customer_id` and `vin` respectively for horizontal scale, though at the volumes estimated in section 3, a single well-indexed relational database is sufficient for years — don't over-engineer sharding here; call it out as a future lever, not a day-one requirement.

---

## 5. High-Level Design

### Major components

1. **Configurator Service** — read-heavy, serves buildable configurations and estimated delivery windows; backed by caches/read replicas since it can tolerate a few minutes of staleness on allocation data.
2. **Reservation/Checkout Service** — the strongly-consistent hot path; owns hold creation, allocation decrement, and orchestrates deposit authorization with the payment processor.
3. **Allocation Ledger Service** — the system of record for `FactoryAllocation` counters; fronted by a fast atomic-counter layer (e.g., Redis) for the launch-event hot path, reconciled asynchronously into the durable database (section 6.1).
4. **Payment Gateway** (external, PCI boundary) — tokenized deposit authorization/capture/refund; we only ever store opaque references, never card data.
5. **Order Management / Workflow Engine** — drives the order state machine from `CONFIRMED` through `DELIVERED`, enforcing the per-state mutable-field whitelist and emitting an event on every transition.
6. **Production Scheduling / MES Integration** — an external factory system; our system requests and receives slot commitments and build/QA status updates, but does not control the line itself.
7. **VIN Binding / Finished-Goods Inventory Service** — binds a completed, QA-passed `VehicleUnit` to the correct `Order`, and manages the pool of unsold built units available for the buy-from-inventory path.
8. **Waitlist / Rationing Service** — manages the fair-ordering queue and time-boxed offers when a bucket is oversubscribed.
9. **Notification Service** — pushes order-status and delivery-ETA updates to the customer app/email/SMS.
10. **Event Bus / Audit Pipeline** — every state transition and allocation decision flows through here, feeding the append-only audit log, dashboards, and notifications.
11. **Ops Console** — factory-allocation-vs-demand dashboards, waitlist depth, manual override tools for support agents handling disputes/exceptions.

### High-level data flow (whiteboard sketch, described in ASCII)

```
                ┌────────────────────┐
                │  Customer (web/app) │
                └──────────┬──────────┘
                            │ browse/configure           │ reserve / confirm / cancel
                            ▼                             ▼
                 ┌────────────────────┐        ┌────────────────────────┐
                 │ Configurator Svc    │        │ Reservation/Checkout    │
                 │ (AP, cache/replica) │        │ Svc (CP, hot path)      │
                 └──────────┬──────────┘        └───────────┬─────────────┘
                            │ read allocation                │ atomic hold + capture
                            ▼                                 ▼
                 ┌──────────────────────────────────────────────────┐
                 │            Allocation Ledger Service              │
                 │  ┌───────────────┐        ┌────────────────────┐  │
                 │  │ Fast counter   │──────► │ Durable allocation │  │
                 │  │ (Redis + TTL   │  async  │ system of record   │  │
                 │  │  tokens)       │  recon. │ (FactoryAllocation)│  │
                 │  └───────────────┘        └────────────────────┘  │
                 └───────────┬───────────────────────────┬────────────┘
                             │ oversubscribed?             │ confirmed
                             ▼                             ▼
                 ┌────────────────────┐        ┌────────────────────────┐
                 │ Waitlist/Rationing  │        │ Payment Gateway         │
                 │ Service (fair FIFO) │        │ (external, PCI-scoped)  │
                 └────────────────────┘        └───────────┬─────────────┘
                                                              │ captured
                                                              ▼
                 ┌────────────────────────────────────────────────────┐
                 │              Order Management / Workflow Engine     │
                 │   CONFIRMED → CONFIG_LOCKED → IN_PRODUCTION → ...    │
                 └───────────┬───────────────────────────────┬──────────┘
                              │ slot commitments/build events │ state events
                              ▼                                 ▼
                 ┌────────────────────┐        ┌────────────────────────┐
                 │ Production/MES      │        │ Event Bus / Audit Log   │
                 │ Integration (ext.)  │        │ + Notifications + Dash. │
                 └──────────┬──────────┘        └────────────────────────┘
                             │ build complete + QA pass
                             ▼
                 ┌────────────────────────────┐
                 │ VIN Binding / Finished-Goods │
                 │ Inventory Service            │
                 └────────────────────────────┘
```

Narrate the key architectural decision: *"The system is split down the middle by consistency requirement, not by business function: everything left of the Allocation Ledger (browsing, estimation, waitlist status) is optimized for availability and can read from caches or replicas; everything from the checkout hold through payment capture is a narrow, strongly-consistent path that intentionally trades some availability and raw throughput for correctness, because the cost of being wrong — double-selling a build slot or a physical VIN — is far higher than the cost of a customer occasionally seeing a 'please try again' during a launch-event spike."*

---

## 6. Detailed Design / Deep Dives

Pick 2-3 of these based on interviewer interest — ask: *"Which would you like me to go deeper on: the concurrency-control mechanism for the hot allocation counter, the consistency/availability split, the order-state-machine and change-window rules, allocation/rationing under scarcity, or VIN binding?"*

### 6.1 Concurrency control on the finite allocation counter

This is the crux of the "prevent overselling" requirement, and there are three viable approaches with real trade-offs:

- **Pessimistic locking** (`SELECT ... FOR UPDATE` on the `FactoryAllocation` row per attempt): simple and trivially correct, but a single row becomes a serialization bottleneck. During a launch-day burst on one popular bucket, thousands of requests queue behind one lock, and checkout latency degrades exactly when it matters most.
- **Optimistic concurrency with retry** (read `version` + `reserved_units`, then `UPDATE ... WHERE version = ? AND reserved_units < capacity_units`, retry on conflict): better throughput than naive locking under moderate contention, but at extreme contention (thousands of concurrent writers on one row) it degenerates into a retry storm — most attempts fail and retry, wasting work and producing unpredictable tail latency.
- **Reservation-token pattern with TTL (recommended for the true hot path):** front the durable counter with an in-memory atomic-decrement primitive (e.g., a Lua-scripted `DECR` in Redis that refuses to go below zero) that hands back a short-lived hold token (TTL ~10-15 minutes). This absorbs the burst on a data structure purpose-built for atomic counters, while a background process asynchronously reconciles the fast counter against the durable `FactoryAllocation` row.

The critical nuance: **the fast-path token is only a soft hold.** The one place a real transactional guarantee against the durable system of record is non-negotiable is at **deposit capture / order confirmation** — that step must re-verify against the durable row (via a lightweight compare-and-swap) before finalizing, even though the earlier "start a hold" step used the faster, eventually-reconciled counter. This two-phase approach — fast/optimistic hold, strict/transactional commit — gives good throughput during bursts without ever compromising the actual correctness guarantee. Unclaimed holds are released by TTL expiry via a background sweeper, not by requiring the customer to explicitly cancel.

### 6.2 Consistency vs. availability: where to draw the CAP line

Frame this explicitly for the interviewer rather than treating it as an afterthought:

- **Browse/configure/estimate-delivery path → favor availability.** Read replicas or a cache with a few minutes of staleness are perfectly acceptable; showing "estimated delivery: Q3 2027" that's 30 seconds out of date during a flash-demand event costs nothing.
- **Checkout/payment/VIN-binding path → favor consistency.** The moment real money changes hands or a specific VIN is bound to a customer, the system must be certain no concurrent transaction has consumed the same resource. Prefer to briefly reject or queue a request (sacrificing availability) over ever showing two customers the same confirmed VIN or double-charging for the same slot.
- The reason this matters more here than in a typical e-commerce system: a generic retailer with 10,000 fungible units of a SKU can absorb an oversell with a backorder and an apology email. Rivian cannot — a factory build slot or a specific serialized VIN is a scarce, six-figure physical asset; "overselling" here means literally promising two people the same car, which is a severe trust, financial-reconciliation, and potentially legal problem (double invoicing a nonexistent second unit). That asymmetry is *why* the checkout path deliberately trades availability/latency for strict consistency, even though the rest of the system leans the opposite way.

### 6.3 Order lifecycle state machine and configuration-lock windows

The order state machine needs to encode, per state, exactly which fields remain mutable — this must be a server-side hard gate, not a UI hint, since it's also a financial/consumer-protection control:

```
CONFIRMED → CONFIG_LOCKED → IN_PRODUCTION → PAINT_STARTED → BUILT
    → QA_INSPECTION → IN_TRANSIT → READY_FOR_DELIVERY → DELIVERED
(CANCELLED reachable from any pre-BUILT state, with stage-dependent refund policy)
```

- **`CONFIRMED` → `CONFIG_LOCKED`:** the customer can still freely change trim, color, or options; each change is validated like a fresh reservation attempt against the (possibly different) target `FactoryAllocation` bucket, since switching configurations can itself be capacity-constrained.
- **`CONFIG_LOCKED` → `IN_PRODUCTION`:** typically triggered on a fixed schedule (e.g., T-14 days before the scheduled production start) — no more configuration changes, but the order hasn't physically started building yet.
- **`IN_PRODUCTION` → `PAINT_STARTED`:** this is the concrete example the interviewer will likely probe on — exterior color can be changed right up until the body enters the paint shop, but once paint has started, a color change would require scrapping physically-applied paint, so the system must hard-block it from this state onward.
- **`BUILT` → `QA_INSPECTION` → `IN_TRANSIT` → `READY_FOR_DELIVERY` → `DELIVERED`:** no configuration changes remain possible; only logistics-level fields (delivery address, scheduling) may still be mutable, and even those may close before `IN_TRANSIT`.
- Implement this as a **mutable-field whitelist keyed by state** — a small lookup table, not scattered conditional logic — so it's auditable and easy to reason about when the interviewer asks "what if a customer requests X change while in state Y."
- Cancellation refund policy also varies per stage (fully refundable pre-production, partial/non-refundable post-paint per business policy) — architecturally, this just means the state machine must expose an ordered set of hard gates that the cancellation flow consults, rather than embedding refund logic as an incidental side effect.

### 6.4 Allocation and rationing under scarcity

When demand for a config-bucket/region/period exceeds `capacity_units`, the system needs a fairness mechanism, not just a race:

- **Regional allocation pools:** rather than one global first-come-first-served pool, factory capacity is split into named buckets per region (e.g., separate pools for different markets) to protect fulfillment/logistics commitments — at the cost of some inefficiency if one region undersells while another oversells relative to its pool (mitigated by a periodic, e.g. bi-weekly, inter-region rebalancing job rather than real-time global pooling).
- **Durable, ordered waitlist:** once a bucket's capacity is exhausted, further hold requests don't fail outright — they join a `Waitlist` row ordered by a `priority_score` (a deterministic composite of arrival timestamp plus any priority tier, e.g., an existing customer whose lease is expiring soon). This converts an uncontrolled concurrency problem into a manageable queueing problem.
- **Priority must be explainable:** boosting some customers (expiring leases, referral tiers) ahead of pure time-of-arrival is reasonable, but the scoring function must be deterministic and auditable — no ad hoc reshuffling — since customers will ask "why did they get a slot before me," and being able to answer precisely is both a trust and (in some jurisdictions) a compliance requirement.
- **Time-boxed offers:** when new capacity frees up (next period's slots open, or a cancellation returns a slot), the allocator pulls the next N waitlisted customers and extends an offer with its own TTL (e.g., 48-72 hours to accept and pay the deposit) before rolling to the next person — reusing the same hold/TTL/reconciliation machinery as the direct-reservation path in section 6.1, just triggered by queue advancement instead of a direct request.

### 6.5 Binding a Reservation to a specific VehicleUnit (VIN)

There are two distinct binding paths, and they should be treated as genuinely different flows rather than forced into one:

- **Build-to-order path:** the `Reservation`/`Order` binds to a `ProductionSlot` — a *promise* of a future VIN — and the physical `VehicleUnit` doesn't exist yet. Only after the unit finishes production and passes QA does an asynchronous event bind `vehicle_unit_id` onto the `Order`, guarded by a uniqueness constraint so a given VIN can only ever attach to one order. Deliberately deferring VIN assignment until after QA (rather than pre-assigning a VIN number at reservation time) means production variance — a unit failing QA, getting reworked, or scrapped — never requires unwinding a customer-visible commitment to a *specific* car; it's cleaner to substitute at the anonymous "unit" level than to explain to a customer why "their" VIN changed.
- **Buy-from-existing-inventory path:** the customer selects a specific, already-built, unsold `VehicleUnit` (a cancellation, an overproduction unit, a fleet-rotation return). This reuses the exact hold/TTL/strong-consistency pattern from 6.1, just scoped to a single row (`VehicleUnit.status = AVAILABLE` compare-and-swap to `HELD`) instead of a counter — arguably an easier correctness problem than the counter case, since it's inherently a quantity-of-one resource.
- **Edge case worth flagging proactively:** production sometimes yields a configuration slightly different from what was promised (e.g., a supply-constrained option gets substituted). This should trigger an explicit re-negotiation flow back to the customer — accept the substitute, wait for a rebuilt slot, or cancel with a full refund — rather than silently shipping a different car than the one that was configured and paid for.

---

## 7. Minimal API Surface (illustrative)

```
# Customer-facing
GET   /v1/configurator/models/{model}/options
      → valid trims/colors/options + current estimated delivery windows (cache-tolerant)

POST  /v1/reservations
      → { config_id, region, deposit_payment_token, idempotency_key }
      → attempts a hold; returns { reservation_id, hold_expires_at } or 409 (unavailable/queued)

POST  /v1/reservations/{id}/confirm
      → converts a HELD reservation into a paid Order (strongly consistent capture + decrement)

GET   /v1/orders/{id}
      → current state, configuration, delivery ETA, mutable-field list for current state

PATCH /v1/orders/{id}/configuration
      → requests a config change; validated against the current state's mutable-field whitelist

POST  /v1/orders/{id}/cancel
      → cancels the order and triggers the refund policy for the current state

POST  /v1/inventory/vehicle-units/{vin}/hold
      → holds a specific existing VIN (buy-from-inventory path)

# Operator-facing
POST  /v1/factory-allocations              → define capacity_units for plant/week/region/bucket
GET   /v1/waitlists/{bucket}                → queue depth + projected next-offer timing
POST  /v1/orders/{id}/admin-override        → support-agent exception handling (audited)
```

---

## 8. Trade-offs and Alternatives Considered

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| Hot allocation counter | Fast in-memory token/TTL hold, reconciled async into the durable ledger, with a strict compare-and-swap only at final capture | Pure database row locking (pessimistic or optimistic) for every hold attempt | Row locking is simpler but collapses under launch-event contention on a handful of hot rows; the two-phase approach absorbs the burst cheaply while keeping the one truly critical check (final capture) strictly consistent. |
| Consistency model | Split: AP for browsing/estimation, CP for checkout/payment/VIN-binding | Uniform strong consistency across the whole system | Uniform strong consistency would throttle read-heavy configurator traffic for no correctness benefit and hurt UX exactly when traffic is highest (launch events). |
| Rationing under scarcity | Durable, ordered waitlist with a deterministic priority score and time-boxed offers | Simple first-come-first-served free-for-all every time capacity is released | A recurring free-for-all (e.g., every Monday when next week's slots open) recreates the exact thundering-herd/overselling risk the design is meant to solve, repeatedly. |
| VIN binding timing | Bind the physical VIN only after production completes and QA passes | Pre-assign a specific VIN at reservation time | Pre-assignment looks appealing to the customer ("here's your VIN early") but forces an awkward customer-facing unwind whenever that specific unit fails QA, gets reworked, or is scrapped; late binding absorbs production variance transparently. |
| Configuration-change enforcement | Server-side mutable-field whitelist keyed by order state (hard gate) | Client/UI-only enforcement of what can be changed | UI-only enforcement is trivially bypassable via direct API calls and provides no audit trail for a financially/legally sensitive control. |
| Allocation pooling | Per-region allocation buckets with periodic inter-region rebalancing | One global allocation pool, allocated purely first-come-first-served | Regional pools protect delivery-logistics and market-fulfillment commitments; the cost is some inefficiency between regions, mitigated by a rebalancing job rather than accepted as permanent waste. |

---

## 9. Failure Modes & Edge Cases to Call Out Proactively

- **Duplicate reservation request (client retry after a timeout):** must be idempotent via a client-supplied `idempotency_key`, so a network retry never creates two holds.
- **Hold-expiry race with in-flight payment:** a customer's payment completes at the exact moment a TTL hold expires. Mitigate with a short grace/reconciliation window, and always let a successfully captured payment "win" over expiry if the confirmation arrives within that grace period, rather than accepting money for a slot that's already been released.
- **Ambiguous payment processor response (timeout, unclear success/failure):** never double-confirm or silently drop an order — capture requests are idempotent keyed by `reservation_id`, and ambiguous cases are resolved via the processor's webhook/reconciliation feed before finalizing state.
- **Factory replans capacity after slots are already sold** (e.g., a supply-chain shortage reduces a bucket's `capacity_units` below what's already been reserved): trigger an explicit demotion/renegotiation workflow — push affected orders to the waitlist or a later slot with proactive customer communication — rather than silently breaking a promised delivery window.
- **A bound VIN fails QA after production:** unwind the binding, and either substitute a matching unit from finished-goods inventory or roll the order into the next available slot; the `Order` must never be left referencing a VIN that's been scrapped or sent to rework.
- **Regional demand mismatch:** one region undersells its allocation while another oversells relative to its pool — addressed by the periodic inter-region rebalancing job (section 8), not by ad hoc manual transfers.
- **Cancellation after an irreversible production stage (e.g., post-paint):** the physical unit must be cleanly returned to the finished-goods inventory pool (available for the buy-from-inventory path) rather than left in an orphaned, unsellable limbo state.
- **Scalping/bot activity on limited allocations:** a popular "Launch Edition" bucket is an obvious target for automated mass-reservation abuse — needs rate limiting and bot detection on the reservation endpoint, not just capacity/concurrency correctness.

---

## 10. Monitoring, Observability, and Security (brief)

- **Dashboards:** allocation utilization per bucket/week/region (capacity vs. reserved vs. available), checkout funnel and drop-off rate, waitlist depth and velocity, hold-to-conversion rate, average time spent in each lifecycle stage.
- **Alerting:** paging on drift between the fast-path counter and the durable allocation ledger beyond a small threshold; anomalous reservation velocity on a single bucket (possible scalping/bot activity); rising rate of ambiguous/failed payment reconciliations.
- **Security:** payment tokenization and card data are entirely out of scope for our systems, handled by an external PCI-compliant processor — we only ever store opaque references; strict per-customer ownership checks on all order/reservation endpoints; rate limiting and bot detection on the reservation endpoint given the scalping incentive around limited allocations.
- **Audit/compliance:** the append-only `OrderStateEvent` log, plus a log of every admin-initiated allocation or override action, supports financial reconciliation and consumer-protection dispute resolution — this system moves real deposits and makes binding delivery promises, so auditability is a first-class requirement, not an afterthought.

---

## 11. Wrap-up / How to Close the Interview

Summarize in 30 seconds: *"To recap: I split the system along a consistency boundary rather than a purely functional one — browsing and delivery estimation favor availability and tolerate staleness, while the checkout/payment/VIN-binding path is strongly consistent, using a fast in-memory token/TTL hold to absorb launch-event bursts with a strict compare-and-swap guard only at final capture. A durable, deterministically-ordered waitlist handles rationing when demand exceeds factory capacity, and the order lifecycle is enforced as an explicit state machine with a server-side mutable-field whitelist per stage — so a color change is allowed before paint starts and hard-blocked after, as a real architectural gate rather than a UI convention. The core insight throughout is that a VIN or a production slot is a scarce, physical, non-fungible resource, which is what makes 'overselling' here a much more serious failure than in a typical e-commerce system."*

Then proactively offer a couple of extension directions, showing you know where the design could go next:
- How would this evolve to support a secondary marketplace — customers transferring or reselling their reservation/build slot to another buyer?
- How would the allocation model change if Rivian introduced dealer/franchise partners in some markets, mixing direct and indirect distribution over the same finite factory capacity?
- How would multi-currency deposits and region-specific consumer-protection rules (e.g., mandatory cooling-off/cancellation windows) change the cancellation and refund logic?

---

## 12. Follow-up Questions Interviewers May Ask

- "Walk me through exactly what happens if two customers click 'reserve' on the last unit of a limited allocation within the same millisecond."
- "How do you prevent a bot from mass-reserving a popular configuration to scalp it later?"
- "What happens if the payment processor confirms a charge 30 seconds after your hold already expired and the slot was given to someone else?"
- "How would your data model change if Rivian started reselling cancelled orders' physical units as discounted 'inventory' vehicles?"
- "How do you reconcile the fast in-memory allocation counter with the durable database if the fast-path store crashes and loses state mid-burst?"
- "How would you design regional rationing if the business wants to strategically prioritize certain markets over pure fairness?"
- "How would you support a customer wanting to transfer their reservation to a family member — what breaks in your data model?"
- "How is this fundamentally different from designing checkout for a company selling a normal, restockable SKU, and which of your design decisions specifically follow from that difference?"

---

## References

- Rivian system design round context: see [`../rivian/index.md`](../rivian/index.md), section "System Design Interview Questions" (question #8 — the one non-vehicle-themed prompt in the series, testing general distributed-systems/e-commerce fluency).
- Conceptually related to the concurrency and consistency trade-offs seen in any high-demand, limited-inventory checkout system (e.g., flash-sale ticketing or limited-drop retail), but distinguished here by the "unit" being a physical, serialized, build-scheduled good rather than a restockable SKU.
