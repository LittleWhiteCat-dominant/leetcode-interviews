# System Design Mock Interview: EV Battery Health Monitoring System

**Company theme:** Rivian-style (vehicle/EV), also broadly applicable to Tesla, Ford, or any BEV manufacturer with a fleet of vehicles carrying high-voltage battery packs.
**Round:** System Design (45-60 min onsite loop)
**Interviewer expectation:** Structured problem-solving, not a specific tech stack. Clarify → requirements → estimate → high-level → deep dive → trade-offs → wrap-up.

This document is written as a self-contained interview walkthrough: it includes the clarifying questions you should ask, a model answer for each section, and the follow-up probes an interviewer is likely to throw at you.

> **Note on scope:** This system builds on top of the general-purpose [Vehicle Telemetry Ingestion Pipeline](./vehicle-telemetry-ingestion-pipeline.md) (Document A) — it reuses the same edge-to-cloud transport, streaming ingestion tier, and schema registry rather than reinventing them. This document does **not** re-derive that shared infrastructure; it focuses on what's genuinely distinctive about battery health: cell/module-level time series, state-of-health (SOH) and state-of-charge (SOC) estimation, degradation trend modeling, a safety-critical thermal-runaway early-warning path, and fleet-wide aggregation for warranty/recall analysis. Where relevant, this document calls out exactly which parts are shared vs. battery-specific.

---

## 0. Opening: Clarify the Problem (first 3-5 minutes)

Don't start designing immediately. Restate the prompt and ask clarifying questions to narrow scope. Sample dialogue:

> **You:** "Battery health monitoring touches a lot of things — cell-level diagnostics, degradation over years of use, thermal safety, and fleet-wide warranty analysis. Should I assume the general telemetry ingestion pipeline (ingestion gateway, streaming tier, schema registry) already exists and I'm designing what sits on top of it, or should I design the whole thing from scratch?"
>
> **Interviewer:** "Assume the general ingestion pipeline exists — you don't need to redesign Kafka-style ingestion. Focus on what's specific to battery health: how you monitor it, detect problems, and use the data at fleet scale."
>
> **You:** "Got it. A few more questions:
> 1. How many cells are we actually talking about per vehicle, and do we need per-cell telemetry in the cloud, or is pack/module-level aggregation acceptable?
> 2. Is thermal-runaway detection purely an on-vehicle safety system (BMS-local), or does the cloud pipeline need to participate in that latency-critical path at all?
> 3. What's the primary business use case driving this — customer-facing range/health estimates, engineering R&D, warranty/recall analysis, or all three?
> 4. Do we need to support real-time SOH/SOC computation in the cloud, or can the vehicle's BMS compute those locally and just report the result?"

Assume the interviewer answers:
- A typical pack has on the order of 1,000-7,000 individual cells grouped into ~100-200 logical "cell groups" or modules that the BMS treats as monitoring units — individually addressing thousands of raw cells over cellular is out of the question; design for module/group-level summaries as the primary cloud-visible granularity, with raw cell-level data available on-vehicle and pullable on-demand (e.g., during a service visit) but not routinely streamed.
- The vehicle's BMS already has a hard real-time (millisecond-to-second scale), safety-certified local control loop for the most extreme thermal-runaway precursors — that's out of scope; we own the *early-warning* layer that catches trends the local hard-real-time loop hasn't yet tripped on, escalates within seconds via the cloud, and can trigger conservative vehicle-side mitigations (e.g., limit charge rate) as a second line of defense.
- All three use cases matter, but prioritize: (1) safety/thermal early-warning, (2) fleet-wide warranty/recall analysis, (3) customer-facing health estimates, in that order of engineering rigor required.
- The BMS computes an initial SOC/SOH estimate locally (it must, for on-vehicle systems like the range estimate), but the cloud recomputes/refines SOH using a more sophisticated model with access to full fleet history and cross-vehicle context — the two don't need to agree to the decimal point, but should be reconciled and monitored for divergence.

---

## 1. Functional Requirements

State these explicitly on the whiteboard before designing anything.

1. **Ingest battery telemetry** — pack- and module-level voltage, current, and temperature summaries at regular intervals while driving/charging, reusing the shared ingestion pipeline (Document A).
2. **Edge-side feature extraction** — the vehicle computes and uplinks summary statistics (min/max/mean/stddev voltage and temperature per module, cell-group imbalance metrics) rather than raw per-cell readings, to control cellular bandwidth.
3. **State-of-Charge (SOC) tracking** — maintain a continuously updated estimate of how "full" the battery is, reconciling the vehicle-reported SOC with cloud-side correction where warranted.
4. **State-of-Health (SOH) estimation** — estimate the battery's remaining usable capacity relative to when new (capacity fade), updated incrementally as new charge/discharge cycle data arrives.
5. **Degradation trend modeling** — track SOH over the vehicle's lifetime, detect abnormal degradation rates (a specific vehicle or cohort degrading meaningfully faster than the fleet baseline), and support projecting future degradation.
6. **Thermal-runaway early-warning (hot path)** — detect precursor patterns (rapid temperature rise, abnormal cell-group voltage divergence, unusual internal resistance signatures) and escalate to safety response within a strict, low latency budget, independent of routine analytics processing.
7. **Fleet-wide aggregation for warranty/recall analysis** — support queries like "all vehicles with battery lot X showing SOH degradation above Y% by month Z of ownership" for engineering and warranty teams.
8. **Customer-facing health surfacing** — expose a simplified, stable health metric (e.g., "88% of original capacity") to in-app/dashboard surfaces without exposing noisy raw internals.
9. **Anomaly/fault flagging** — detect and flag individual cell-group faults (e.g., one module consistently reading anomalous voltage/temperature relative to its peers) for service scheduling, distinct from fleet-wide safety escalation.
10. **On-demand deep diagnostics pull** — support requesting full-resolution, per-cell raw data from a specific vehicle (e.g., during a service visit or a warranty investigation), as an exception path distinct from routine streaming.

**Out of scope (state this explicitly):** the general telemetry transport/ingestion infrastructure (covered by [Document A](./vehicle-telemetry-ingestion-pipeline.md)), the vehicle's hard-real-time, safety-certified local BMS control loop that physically disconnects/isolates a cell string on an imminent thermal event (that's a functional-safety-certified embedded system, not a cloud design problem), and the physical battery/cell chemistry itself.

---

## 2. Non-Functional Requirements

| Requirement | Target / Reasoning |
|---|---|
| **Safety-path latency** | Thermal-runaway early-warning: precursor pattern detected in telemetry to safety-team/vehicle-mitigation triggered in under ~10 seconds end-to-end. This is the single most important NFR in this system — treat it as a hard constraint. |
| **Routine analytics latency** | SOH/degradation updates, warranty aggregations: minutes to hours of staleness is acceptable; these are not time-critical. |
| **Bandwidth efficiency** | Edge feature extraction must reduce per-vehicle uplinked battery data by roughly two orders of magnitude versus raw cell-level streaming (see §3) — this is a hard requirement, not an optimization; raw streaming at fleet scale is not viable. |
| **Accuracy (SOH estimation)** | Cloud-side SOH estimate should track true capacity fade within a few percentage points, validated periodically against ground-truth data (e.g., full charge/discharge reference cycles, service-visit diagnostics). |
| **False-negative tolerance (safety path)** | Effectively zero tolerance for missed genuine thermal-runaway precursors — bias detection thresholds toward sensitivity, accepting a higher false-positive rate as the safer trade-off. |
| **False-positive cost awareness** | While safety bias is correct, an excessive false-positive rate erodes trust and triggers unnecessary conservative vehicle-side actions (e.g., charge-rate limiting) that degrade customer experience — tune and monitor this trade-off explicitly rather than ignoring the cost of false alarms. |
| **Scalability** | Support the same 500K-1M vehicle fleet as Document A; battery telemetry volume is a small fraction of total fleet telemetry (see §3) but processing (SOH modeling, degradation trend analysis) is more compute-intensive per message. |
| **Data retention** | Full-resolution battery summaries retained for the vehicle's warranty period (e.g., 8-10 years) at reduced granularity after an initial high-resolution window, to support long-horizon degradation and recall analysis. |
| **Auditability** | Every safety-relevant alert and every SOH estimate used in a warranty/recall decision must be traceable (what data, what model version, what threshold) — this is as much a legal/compliance requirement as an engineering one. |

Call out explicitly to the interviewer: *"This system has two genuinely different latency/criticality regimes living side by side — a small, safety-critical, low-latency thermal path, and a much larger, compute-intensive but latency-tolerant analytics path. That split should show up explicitly in the architecture, not just as a documentation note."*

---

## 3. Back-of-the-Envelope Capacity Estimation

Doing this out loud shows quantitative rigor.

- **Fleet size:** 1,000,000 vehicles (consistent with Document A's design target).
- **Pack composition:** ~1,000-7,000 individual cells per pack, organized by the BMS into roughly **100-200 logical cell groups/modules** for monitoring purposes. This grouping is itself a bandwidth/complexity decision made on-vehicle, before the cloud ever sees the data.
- **Internal (on-vehicle) sampling rate:** the BMS samples cell-group voltage and temperature internally at ~1 Hz — this never leaves the vehicle in raw form.
- **Edge-computed summary message:** instead of streaming 150 cell groups × 2 metrics (voltage, temp) × 1 Hz raw, the edge agent computes a rolled-up `BatteryHealthSummary` (pack-level SOC/SOH/voltage/current + per-module min/max/mean voltage and temperature + a handful of derived stats like voltage-delta and imbalance score) and uplinks it **every 30 seconds while driving or charging**, and roughly every 15 minutes while parked and not charging (a slow balancing/self-discharge check).
- **Raw-vs-summary bandwidth comparison (the headline number):** raw per-cell-group streaming at 1 Hz would be `150 modules × 2 metrics × 4 bytes × 1 Hz ≈ 1.2 KB/sec/vehicle` continuously. The edge-computed summary is roughly `1.5 KB every 30 sec ≈ 50 bytes/sec/vehicle` — **over a 20x bandwidth reduction**, and that's before accounting for the fact that raw streaming would need to run continuously (parked or not) while the summary backs off to a 15-minute cadence when parked. Real-world reduction is closer to two orders of magnitude once idle-time behavior is included, which is why edge feature extraction is a hard requirement, not a nice-to-have.
- **Peak concurrency:** reuse Document A's estimate that ~15% of the fleet (150,000 vehicles) is actively driving at peak, plus a smaller overlapping population actively charging (assume another 5%, ~50,000 vehicles, with some overlap negligible since a vehicle is rarely driving and charging simultaneously) → roughly **150,000-200,000 vehicles actively uplinking battery summaries at peak**.
- **Peak message rate:** `~180,000 vehicles / 30-sec interval ≈ 6,000 messages/sec` at peak — noticeably smaller than Document A's general telemetry peak (200,000 msgs/sec), because battery data is one subsystem among many and reports on a slower (30s vs. 1s) cadence.
- **Message size:** larger per-message than a generic telemetry frame due to the per-module stat arrays — roughly 1-1.5 KB (150 modules × ~4 summary floats × 4 bytes ≈ 2.4 KB before compression, more like 1-1.5 KB after compact encoding/compression of mostly-similar values across modules).
- **Peak ingress bandwidth:** `6,000 msgs/sec × 1.5 KB ≈ 9 MB/s` — small enough to ride on the same shared streaming tier as general telemetry without needing dedicated infrastructure, though it gets its own topic for independent scaling and retention policy.
- **Daily volume:** assume the average vehicle is actively driving/charging ~2.5 hours/day → `2.5 × 3600 / 30 = 300` summary messages/day/vehicle during active periods, plus ~4-6 parked-heartbeat messages/day → **~1,000,000 vehicles × ~305 messages/day ≈ 305M messages/day**, at ~1.2 KB average ≈ **~370 GB/day raw ingest** — roughly 5-6x smaller than Document A's general telemetry volume, which makes sense given the slower reporting cadence and narrower scope (one subsystem vs. the whole vehicle).
- **On-demand raw cell-level pulls:** these are the exception, not the norm — assume a few thousand per month fleet-wide (service visits, warranty investigations), each pulling a bounded historical window (e.g., last N hours of full-resolution data cached locally on the vehicle, or a live diagnostic dump over Wi-Fi/wired connection during service) rather than routine cellular streaming. This keeps the "we sometimes need per-cell resolution" requirement satisfiable without ever having to support it at fleet scale over cellular.

Conclusion to state out loud: *"Battery telemetry is a smaller, slower-cadence slice of the overall telemetry problem — the interesting engineering challenge here isn't raw ingestion throughput, it's (a) making sure edge-side aggregation doesn't throw away the signal needed to detect real problems, and (b) building a genuinely separate, low-latency escalation path for thermal safety that can't be allowed to queue behind routine SOH/degradation batch processing."*

---

## 4. Data Model / Database Design

### Core entities

**`BatteryHealthSummary`** (the primary streaming message — reuses Document A's transport/schema-registry infrastructure, but is its own schema/topic)
```
vehicle_id
pack_id
timestamp
schema_version
soc_pct                     -- state of charge, vehicle-reported
soh_pct                     -- state of health, vehicle-reported (cloud recomputes independently)
pack_voltage_v
pack_current_a
charge_cycle_count
max_module_temp_c, min_module_temp_c, avg_module_temp_c
max_module_voltage_v, min_module_voltage_v
voltage_delta_v              -- max - min across modules; key imbalance indicator
module_stats (array)         -- per-module: { module_id, voltage, temp, internal_resistance_est }
is_charging                   -- bool
fast_charge_session_id         -- nullable, links to a DC fast-charge session for degradation correlation
```
`module_stats` is bounded (100-200 entries, not thousands of raw cells) — this is the concrete artifact of edge-side feature extraction discussed in §3 and §6.1.

**`ThermalAlert`** (safety-critical, low-volume, hot-path event — modeled and routed independently, analogous to `DTCEvent` in Document A)
```
alert_id (PK)
vehicle_id
pack_id
detected_at
severity                    -- WATCH / WARNING / CRITICAL
trigger_reason               -- e.g. "rapid_temp_rise", "voltage_divergence", "internal_resistance_spike"
affected_module_ids (array)
model_version                 -- which detection model/ruleset version fired this alert, for auditability
recommended_mitigation         -- e.g. "limit_charge_rate", "notify_driver", "dispatch_roadside"
acknowledged_by, acknowledged_at
```
Like `DTCEvent` in Document A, this is deliberately a separate, small, indexed, low-latency-queryable store — never mixed into the same storage tier as bulk `BatteryHealthSummary` data.

**`DegradationSnapshot`** (periodic, e.g. weekly/monthly, per-vehicle rollup for trend analysis — not derived from every raw message)
```
vehicle_id, snapshot_period (composite PK)     -- e.g. week-granularity
soh_pct_estimate                                -- cloud-computed, model-refined SOH
soh_estimate_confidence
cumulative_charge_cycles
cumulative_fast_charge_sessions
avg_ambient_temp_exposure_c                      -- climate is a major degradation covariate
degradation_rate_pct_per_1000km                   -- trailing-window derived rate
model_version
```
This is the table that powers both customer-facing health trends and engineering degradation research — computed by a batch/stream job, not read directly off the raw summary stream, because degradation trends are inherently a longer-horizon, smoothed signal that would be noisy if computed per-message.

**`FleetBatteryCohort`** (materialized aggregation for warranty/recall analysis — the fleet-wide view)
```
cohort_key (PK)                -- e.g. "battery_lot=L2024-07, model=R1T, region=US-West"
vehicle_count
avg_soh_pct_at_month(n)          -- SOH distribution at each ownership-month milestone
pct_vehicles_below_threshold      -- e.g. % below 90% SOH at 3 years
thermal_alert_rate
last_computed_at
```
This is a derived/materialized table, recomputed periodically (e.g., nightly) by a batch job over `DegradationSnapshot` and `ThermalAlert` data — it is the concrete artifact that lets a warranty analyst ask "is battery lot X degrading faster than the fleet baseline?" without scanning raw telemetry.

### Why keep `ThermalAlert` and `BatteryHealthSummary` in entirely separate storage tiers?

This mirrors the hot/cold split in Document A, and is worth narrating explicitly: *"`ThermalAlert` is rare, safety-critical, and needs sub-second query/subscribe latency for an alerting service — a good fit for a small, indexed, low-latency operational store or a stream-native alerting system. `BatteryHealthSummary` is high-volume and consumed in large batches for SOH modeling and fleet aggregation — a good fit for a columnar time-series store or data lake. Mixing them would force the safety path to compete with, and be delayed by, bulk analytical scans — unacceptable given the latency budget in §2."*

---

## 5. High-Level Design

### Major components

1. **Edge Battery Feature Extractor (on-vehicle, part of the BMS/edge agent)** — computes the module-level summary statistics from raw cell-group readings, applies the adaptive driving/charging/parked cadence, and hands the resulting `BatteryHealthSummary` to the shared edge telemetry agent from Document A for uplink.
2. **Shared Ingestion Pipeline (reused from Document A)** — the ingestion gateway, schema registry, and partitioned streaming log. Battery data gets its own topic (`battery.health.raw`), partitioned by `vehicle_id` for the same per-vehicle-ordering reasons as general telemetry, but is otherwise the same physical infrastructure — no need to re-architect this.
3. **Thermal Early-Warning Engine (hot path)** — a dedicated, low-latency consumer group on the battery topic, running a combination of rule-based thresholds (fast, cheap, catches known failure signatures) and a lightweight anomaly-detection model (catches novel patterns), feeding directly into `ThermalAlert` creation and a safety-response/dispatch integration, and optionally a command channel back to the vehicle for conservative mitigation (e.g., "reduce max charge rate until inspected").
4. **SOC/SOH Estimation Service (cold path, near-real-time)** — a stream-processing job maintaining a per-vehicle "battery state" model, incrementally updating SOH using coulomb-counting-based capacity tracking cross-checked with a fleet-trained degradation model, reconciling against the vehicle-reported SOC/SOH and flagging significant divergence.
5. **Degradation Trend / Snapshot Job (batch, periodic)** — a scheduled job (e.g., weekly) that rolls up per-vehicle history into `DegradationSnapshot` records, computing smoothed degradation rates and confidence intervals.
6. **Fleet Aggregation / Warranty Analysis Service (batch, periodic)** — computes `FleetBatteryCohort` rollups, powering engineering and warranty-team dashboards/queries.
7. **Battery State Store** — a low-latency key-value/document store holding the current best estimate of SOC/SOH/health status per vehicle (the "digital twin" for battery health), read by customer-facing apps and service-technician tools.
8. **On-Demand Diagnostics Service** — handles the exception-path request for full-resolution, per-cell raw data pulls from a specific vehicle (service visit / warranty investigation), distinct from the routine streaming path.

### High-level data flow (whiteboard sketch, described in ASCII)

```
     ┌─────────────────────────────────────────────┐
     │  Vehicle (edge)                              │
     │  ┌─────────────────┐   ┌──────────────────┐ │
     │  │ BMS: raw cell-   │──►│ Edge Battery      │ │
     │  │ group voltage/   │   │ Feature Extractor │ │
     │  │ temp @ ~1 Hz     │   │ (module rollups)  │ │
     │  └─────────────────┘   └─────────┬──────────┘ │
     │                                   │ BatteryHealthSummary
     │                                   ▼            │
     │                    (hands off to shared edge   │
     │                     telemetry agent — Doc A)   │
     └───────────────────────────┬───────────────────┘
                                  ▼
     ┌───────────────────────────────────────────────────────┐
     │      Shared Ingestion Pipeline (Document A)            │
     │  Ingestion Gateway → Streaming Log (topic:              │
     │  battery.health.raw, partitioned by vehicle_id)          │
     └───────────────────┬───────────────────┬─────────────────┘
                          │                   │
             ┌────────────┘                   └────────────┐
             ▼                                              ▼
  ┌───────────────────────┐                     ┌─────────────────────────┐
  │ HOT PATH:               │                     │ COLD PATH:                │
  │ Thermal Early-Warning    │                     │ SOC/SOH Estimation Service │
  │ Engine (rules + anomaly  │                     │ (per-vehicle battery state) │
  │ model, <10s budget)      │                     └────────────┬─────────────┘
  └───────────┬─────────────┘                                   │
              │ ThermalAlert                                    ▼
              ▼                                       ┌─────────────────────────┐
  ┌───────────────────────┐                          │ Battery State Store       │
  │ Safety Response /       │                          │ (per-vehicle digital twin)│
  │ Dispatch + Vehicle       │                          └────────────┬─────────────┘
  │ Mitigation Command       │                                       │
  └───────────────────────┘                                         ▼
                                                        ┌─────────────────────────┐
                                                        │ Degradation Trend Job     │
                                                        │ (weekly DegradationSnapshot)│
                                                        └────────────┬─────────────┘
                                                                     ▼
                                                        ┌─────────────────────────┐
                                                        │ Fleet Aggregation /        │
                                                        │ Warranty Analysis           │
                                                        │ (FleetBatteryCohort)        │
                                                        └─────────────────────────┘
```

Narrate the key architectural decision: *"The thermal early-warning engine forks off the shared streaming log exactly like Document A's DTC hot path — same pattern, same reasoning: a safety-critical, low-latency consumer must never queue behind SOH modeling or nightly warranty aggregation jobs. The genuinely new piece here, versus the generic telemetry pipeline, is the layered cold-path pipeline itself — raw summaries feed a near-real-time SOH estimator, which feeds a periodic degradation-trend job, which feeds a fleet-wide warranty aggregation — each stage trading immediacy for a longer time horizon and a higher level of aggregation."*

---

## 6. Detailed Design / Deep Dives

Pick 2-3 of these based on interviewer interest — you won't have time for all of them in 45 minutes, so ask: *"Which of these would you like me to go deeper on: edge feature extraction, SOC/SOH estimation, the thermal early-warning path, or fleet-wide degradation aggregation?"*

### 6.1 Edge-side feature extraction (why summary stats, not raw cells)

- Streaming raw per-cell (or even per-module) time series continuously for a million vehicles is infeasible on cellular, as shown in §3 — but the deeper design question is *which* summary statistics preserve enough signal to still catch real problems.
- **Voltage delta / imbalance score is the single most valuable derived metric:** a healthy pack has all modules converging to similar voltage under similar load; a growing `voltage_delta_v` (max module voltage - min module voltage) over time is often the earliest observable signature of one module degrading faster than its peers — far more informative for early detection than any single module's absolute voltage.
- **Min/max/mean/stddev per module, not just pack-level aggregates:** a pack-level average can completely mask a single failing module (one bad module among 150 barely moves the fleet-wide mean) — module-level granularity is the minimum resolution that keeps localized faults visible, which is why the design reports ~150 module summaries rather than one number per pack.
- **Internal resistance estimation on-vehicle:** rather than streaming raw voltage-under-load curves, the BMS estimates internal resistance per module locally (from known current/voltage relationships during transients) and reports just the estimate — a good example of pushing a compute-cheap, bandwidth-expensive-to-transmit derivation onto the edge, where it's nearly free (the BMS already has the raw signal locally), rather than shipping raw data for the cloud to compute the same thing later.
- *Trade-off to mention:* summary statistics can hide the exact shape of an anomaly (e.g., a brief spike that's smoothed into a mean) — the mitigation is the on-demand raw-pull path (§1's requirement 10): when a summary-level flag is raised, a subsequent higher-resolution pull (opportunistic over Wi-Fi, or at next service visit) can retrieve the raw detail needed for root-cause investigation, rather than trying to stream that resolution continuously "just in case."

### 6.2 SOC vs. SOH estimation — what's actually being computed, and where

- **State of Charge (SOC)** answers "how full is the battery right now" (0-100%) — it's inherently short-horizon and must be available on-vehicle in real time (it drives the range estimate), so the vehicle's BMS computes it locally via coulomb counting (integrating current over time) with periodic recalibration at known reference points (e.g., a full charge). The cloud's role is secondary: cross-check the reported SOC trajectory for consistency and flag sensor drift, not recompute it independently in real time.
- **State of Health (SOH)** answers "how much usable capacity remains, relative to when new" — it's inherently long-horizon (meaningful degradation happens over months/years, not minutes) and benefits enormously from data the vehicle alone doesn't have: fleet-wide baselines for the same battery chemistry/lot, and a longer, more complete history than the vehicle may retain locally. This is why the cloud maintains its own, independently-computed SOH estimate rather than purely trusting the vehicle-reported figure.
- **Cloud SOH methodology (at a conceptual level, since exact algorithms are proprietary/domain-specific):** track full-capacity charge/discharge cycles when they occur naturally (e.g., a rare near-0-to-100% charge session), use coulomb-counting-derived capacity estimates from those cycles as high-confidence anchor points, and interpolate/model between anchors using incremental cycle data, ambient temperature exposure, and charge-rate history (fast-charging is a well-known accelerant of degradation) as covariates — essentially a time-series regression/state-space model (e.g., a Kalman-filter-style approach) refined as more data arrives, rather than a single point-in-time calculation.
- **Reconciliation, not blind override:** when the cloud-computed SOH diverges meaningfully from the vehicle-reported figure, that divergence itself is a signal worth surfacing (possible BMS calibration drift, possible cloud model blind spot for that vehicle's usage pattern) rather than the cloud simply "winning" and silently overriding the vehicle's number — both should be retained in `DegradationSnapshot` alongside a confidence score.

### 6.3 Thermal-runaway early-warning path (the safety-critical deep-dive)

- **This is explicitly a second, slower line of defense, not the primary safety mechanism** — the primary mechanism is the vehicle-local, hard-real-time, functional-safety-certified BMS control loop that can physically isolate a cell string in milliseconds-to-seconds on an imminent event; that system is out of scope here (embedded/functional-safety domain, not a cloud system design). The cloud's job is to catch *slower-building precursor trends* that the local loop hasn't yet crossed a trip threshold for, and to bring broader context (fleet baselines, this vehicle's own history, environmental correlation) to bear that a purely local, real-time-constrained system can't.
- **Signature-based detection (fast, explainable, first line):** simple, well-understood precursor patterns — rapid temperature rise rate exceeding a threshold, `voltage_delta_v` crossing an absolute or rate-of-change threshold, internal-resistance estimate jumping sharply for one module — are checked with cheap rule-based logic that runs in milliseconds per message, keeping the bulk of the latency budget for transport and escalation rather than computation.
- **Model-based detection (catches novel patterns, second line):** a lightweight anomaly-detection model (e.g., trained on historical `BatteryHealthSummary` sequences preceding known incidents/service events) runs alongside the rules to catch patterns that don't match a predefined signature — this needs its own model-versioning/auditability (recorded in `ThermalAlert.model_version`) since it will evolve over time and every alert must be attributable to the exact model that fired it.
- **Bias toward sensitivity, with an explicit downstream triage step:** given the near-zero tolerance for false negatives (§2), thresholds are tuned aggressively, which means a WATCH/WARNING-severity alert should not by itself trigger the most disruptive response (e.g., stranding a customer with a forced shutdown) — instead, escalate severity progressively (WATCH → notify + increase monitoring frequency; WARNING → conservative mitigation like charge-rate limiting; CRITICAL → immediate driver notification + safety dispatch), so the cost of a false positive scales with the confidence level rather than being all-or-nothing.
- **Latency budget breakdown (to make the <10s target concrete):** edge-to-gateway transport (~1-2s typical cellular), streaming log write + hot-path consumer read (sub-second, given the small dedicated consumer group), rule/model evaluation (milliseconds), alert creation + dispatch integration (~1-2s) — leaves comfortable margin within the 10-second budget even accounting for occasional cellular latency spikes, which is exactly why this path is architecturally isolated from the much larger, more variable-latency bulk analytics consumers.

### 6.4 Degradation trend modeling and fleet-wide aggregation for warranty/recall

- **Why a periodic snapshot, not a real-time recomputation:** meaningful degradation happens over weeks to months of usage, so recomputing a trend on every incoming message would be both wasteful (compute) and noisier (short-term fluctuation in a single cycle's estimate isn't a trend) — a weekly `DegradationSnapshot` job that smooths over many cycles gives a much more stable, decision-useful signal.
- **Key covariates that matter for interpretation, not just the SOH number itself:** ambient temperature exposure (batteries degrade faster in sustained heat), fast-charge frequency (DC fast charging is a known accelerant), and depth-of-discharge patterns (frequent full 0-100% cycles stress cells more than shallow cycling) — a fleet aggregation that only looked at raw SOH-vs-time without these covariates would conflate "this battery lot has a manufacturing defect" with "this cohort happens to be concentrated in a hot climate and fast-charges often," leading to wrong conclusions.
- **Cohort-based comparison is the actual warranty/recall workflow:** the real question engineering asks isn't "what's vehicle X's SOH" but "is battery lot L, or hardware revision H, or region R degrading faster than the fleet baseline after controlling for usage pattern?" — this is why `FleetBatteryCohort` is modeled as a distinct, purpose-built materialized aggregation rather than expecting analysts to write ad hoc queries over raw per-vehicle data every time.
- **Statistical rigor to call out:** flagging a cohort as "abnormally degrading" needs a real baseline comparison (e.g., compare against a similar cohort with different lot/hardware but matched usage patterns) rather than a naive fixed threshold — the same principle as canary-rollout anomaly detection in the OTA design, applied here to a much slower-moving signal (months, not hours).

---

## 7. Minimal API Surface (illustrative)

```
# Vehicle-facing (via the shared Ingestion Gateway from Document A)
POST /v1/vehicles/{vehicle_id}/battery-health
     → BatteryHealthSummary, routed to the battery.health.raw topic
     (reuses Document A's auth/schema-validation path)

POST /v1/vehicles/{vehicle_id}/battery-diagnostics/raw-pull-response
     → full-resolution per-cell data, in response to an on-demand diagnostics request

# Internal / operator-facing
GET  /v1/vehicles/{vehicle_id}/battery-state
     → current SOC, SOH, health status, most recent ThermalAlert (if any)

POST /v1/vehicles/{vehicle_id}/battery-diagnostics/request-raw-pull
     → triggers the on-demand deep-diagnostics path (service visit / investigation)

GET  /v1/fleet/battery-cohorts?battery_lot={lot}&region={region}
     → FleetBatteryCohort aggregation for warranty/recall analysis

GET  /v1/alerts/thermal?since={ts}&severity={level}
     → recent ThermalAlert records, for safety-ops dashboards
```

---

## 8. Trade-offs and Alternatives Considered

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| Cell-level telemetry granularity | Module/cell-group summary statistics, streamed routinely | Raw per-cell voltage/temp, streamed continuously | Raw streaming from thousands of cells across a million vehicles is bandwidth-infeasible (§3); module-level summaries preserve enough resolution to catch localized faults via imbalance metrics. |
| SOH computation location | Cloud-side model, reconciled against vehicle-reported estimate | Trust the vehicle-reported SOH exclusively | The cloud has fleet-wide baselines and longer retained history to refine estimates and catch on-vehicle calibration drift; pure on-vehicle trust would miss systematic sensor/model errors. |
| Thermal safety architecture | Cloud early-warning as a second, slower line of defense behind a local hard-real-time BMS loop | Rely solely on cloud-side detection for thermal safety | A cloud round-trip can never meet true hard-real-time safety latency requirements (network variability alone rules it out); the cloud's value is catching slower precursor trends with fleet-wide context, not replacing certified local safety systems. |
| Alert severity handling | Progressive escalation (WATCH → WARNING → CRITICAL) with response scaled to confidence | Binary alert/no-alert with a single aggressive response | Given the necessary bias toward sensitivity, a binary all-or-nothing response would make false positives disproportionately costly (e.g., unnecessary forced shutdowns); progressive escalation lets the response scale with confidence. |
| Degradation trend computation | Periodic (weekly) smoothed snapshot job | Real-time recomputation on every incoming message | Degradation is a slow, long-horizon signal; per-message recomputation would be computationally wasteful and noisier, not more accurate. |
| Fleet aggregation for warranty analysis | Purpose-built, covariate-aware `FleetBatteryCohort` materialized view | Ad hoc analyst queries over raw per-vehicle telemetry | Raw queries risk conflating confounding covariates (climate, charge patterns) with genuine defects; a purpose-built aggregation bakes in the correct comparison methodology. |
| High-resolution diagnostic data | On-demand pull, exception path (service visit / investigation) | Continuous full-resolution streaming "just in case" | The rare cases needing per-cell resolution don't justify the fleet-wide bandwidth cost of streaming that resolution continuously for all vehicles. |

---

## 9. Failure Modes & Edge Cases to Call Out Proactively

- **A single faulty voltage/temperature sensor on one module:** can look identical to a genuinely degrading module in the summary statistics; mitigate by cross-checking against neighboring modules' physically-expected correlation (modules in the same thermal/electrical vicinity should track each other) and by allowing service diagnostics to distinguish "sensor fault" from "cell fault" via the on-demand raw pull.
- **Thermal early-warning false positive causing unnecessary charge-rate limiting:** directly impacts customer experience (slower charging, reduced range availability); this is the concrete cost side of the sensitivity/false-positive trade-off in §6.3 — must be monitored as a first-class metric (false-positive rate, customer impact), not just detection recall.
- **SOH estimate drift from atypical usage patterns:** a vehicle that's rarely driven, or always charged to a partial state, may never produce the full-capacity reference cycles the cloud model relies on as anchor points (§6.2) — the estimation confidence should explicitly degrade (and be surfaced as lower `soh_estimate_confidence`) for such vehicles rather than silently reporting an overconfident number.
- **Module-level averaging masking a single bad cell within a module:** module-level summaries are themselves an aggregation over many raw cells; a single failing cell within an otherwise-healthy module could be diluted below detection threshold at the module-summary level — this is the residual risk accepted by choosing module-level (not cell-level) routine granularity, and is precisely why the on-demand full-resolution pull path exists as a backstop for suspicious cases.
- **Fast-charge session misattribution:** if `fast_charge_session_id` linkage breaks (e.g., a dropped message during the session), degradation analysis could under- or over-attribute wear to fast charging for that vehicle; reconcile using charge-session boundaries derived from `is_charging` transitions as a fallback rather than relying solely on the session ID.
- **Cohort aggregation confounded by regional climate or usage differences:** flagging "battery lot X is degrading faster" without controlling for the fact that lot X happens to be concentrated in a hot climate is a classic correlation-vs-causation trap — always compare against a climate/usage-matched control cohort, not the raw fleet average.
- **Vehicle offline during a critical charging session:** if connectivity drops while charging (common in some garages) and a thermal precursor develops during that window, the cloud-side early-warning has no visibility until reconnect — this is precisely why the vehicle-local hard-real-time BMS loop (out of scope here, but worth naming explicitly) must be the true primary safety mechanism, with the cloud path as a genuinely secondary layer, never the sole line of defense.

---

## 10. Monitoring, Observability, and Security (brief)

- **Dashboards:** fleet-wide SOH distribution by model/battery-lot/region, thermal-alert rate and severity breakdown, false-positive rate for thermal alerts (tracked via post-hoc service/investigation outcomes), SOC/SOH divergence rate between vehicle-reported and cloud-computed estimates.
- **Alerting:** immediate page on any CRITICAL `ThermalAlert`; daily digest for WATCH/WARNING trend shifts; automatic flag when a `FleetBatteryCohort`'s degradation rate crosses a statistically-significant threshold relative to its matched control cohort.
- **Model governance:** every `ThermalAlert` and `DegradationSnapshot` records the exact model/ruleset version that produced it (auditability requirement from §2); model updates go through the same staged-rollout discipline as the OTA design (canary on a small vehicle cohort before fleet-wide deployment of a new detection model).
- **Security:** the same transport-level authentication and payload validation as Document A applies; additionally, the on-demand raw-diagnostics-pull endpoint requires elevated, audited authorization (it's a sensitive, targeted data-access path, not routine telemetry) to prevent misuse for surveillance of a specific vehicle/owner.

---

## 11. Wrap-up / How to Close the Interview

Summarize in 30 seconds: *"To recap: this system layers battery-specific processing on top of the shared telemetry pipeline rather than duplicating it. Edge-side feature extraction turns thousands of raw cells into ~150 bounded module summaries per message, controlling bandwidth by roughly two orders of magnitude. From there, a fast thermal early-warning path — architecturally isolated the same way the OTA/telemetry hot paths are — acts as a second, slower line of defense behind the vehicle's local safety-certified BMS loop, with severity that escalates progressively rather than all-or-nothing. In parallel, a slower cold-path pipeline builds cloud-side SOH estimates, rolls them into periodic degradation snapshots, and aggregates those into covariate-aware fleet cohorts for warranty and recall analysis — each stage deliberately trading immediacy for a longer time horizon and higher level of aggregation."*

Then proactively offer a couple of extension directions, showing you know where the design could go next:
- How would you extend the degradation model to proactively recommend individual-vehicle service actions (e.g., "recommend a service visit") rather than only supporting after-the-fact fleet-wide warranty analysis?
- How would you validate that the cloud-side SOH model is actually accurate over years, given that ground truth (true remaining capacity) is expensive to measure directly at fleet scale?
- How would this design change for a fleet that includes third-party/aftermarket battery packs with less-trustworthy on-vehicle telemetry — how much do you shift toward cloud-side re-derivation versus trusting the reported data?

---

## 12. Follow-up Questions Interviewers May Ask

- "Why is module-level granularity the right choice instead of cell-level or pack-level — walk me through the failure mode each choice would miss."
- "How would you distinguish a genuinely failing module from a faulty sensor without pulling raw cell-level data every time?"
- "The thermal early-warning path is supposed to be a fast, sub-10-second escalation — what specifically would you monitor to know if that latency budget is being violated in production, and where would you look first to debug it?"
- "How do you validate a new anomaly-detection model for thermal precursors before trusting it in production, given that true positive incidents are (thankfully) rare and you can't easily generate labeled training data?"
- "If a specific battery-lot recall analysis shows elevated degradation, but you later realize that lot was disproportionately sold in a hot-climate region, how would you have caught that confound earlier?"
- "How would you extend this system if the fleet started including vehicles with battery swapping/leasing, where the physical pack changes vehicles over its lifetime?"
- "What would you do differently if cellular bandwidth costs were not a concern at all — would you still choose edge aggregation, or stream raw data?"

---

## References

- Rivian system design round context: see [`../rivian/index.md`](../rivian/index.md), section "System Design Interview Questions."
- Companion document: [Real-Time Vehicle Telemetry Ingestion Pipeline](./vehicle-telemetry-ingestion-pipeline.md) — this document builds directly on that pipeline's ingestion gateway, streaming tier, and schema registry, and mirrors its hot/cold path separation pattern for the battery-specific thermal-safety use case.
- Conceptually related to real-world EV battery management practices: coulomb-counting-based SOC estimation, capacity-fade-based SOH tracking, and BMS-level cell-group monitoring are standard practice across the EV industry (e.g., Tesla, GM, and most modern BEV manufacturers' battery management systems).
