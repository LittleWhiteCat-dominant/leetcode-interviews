# System Design Mock Interview: Real-Time Vehicle Telemetry Ingestion Pipeline

**Company theme:** Rivian-style (vehicle/EV), also broadly applicable to Tesla, Ford, Waymo, or any connected-fleet company.
**Round:** System Design (45-60 min onsite loop)
**Interviewer expectation:** Structured problem-solving, not a specific tech stack. Clarify → requirements → estimate → high-level → deep dive → trade-offs → wrap-up.

This document is written as a self-contained interview walkthrough: it includes the clarifying questions you should ask, a model answer for each section, and the follow-up probes an interviewer is likely to throw at you.

---

## 0. Opening: Clarify the Problem (first 3-5 minutes)

Don't start designing immediately. Restate the prompt and ask clarifying questions to narrow scope. Sample dialogue:

> **You:** "Before I dive in — when you say 'telemetry,' are we talking about a handful of high-level signals (GPS, speed, battery %), or the full breadth of what a vehicle can emit, including raw CAN-bus sensor data and diagnostic trouble codes (DTCs)?"
>
> **Interviewer:** "Assume a broad set: location, speed, battery state, a rotating set of sensor readings (tire pressure, ambient temp, IMU data, etc.), and DTCs. Not raw CAN frames — assume there's an in-vehicle gateway that already curates a telemetry payload."
>
> **You:** "Got it. A few more questions:
> 1. What fleet size and what does 'active' mean — connected and reporting, or actually driving?
> 2. Do we need hard real-time guarantees for anything, or is this primarily for analytics/ML?
> 3. Is per-vehicle event ordering important, or is a rough global ordering acceptable?
> 4. Do we need exactly-once processing, or is at-least-once with idempotent consumers acceptable?
> 5. How long does raw data need to be retained, and who consumes it downstream?"

Assume the interviewer answers:
- Fleet size: ~500,000 vehicles today, design target 1,000,000 within 2 years. "Active" means connected and capable of reporting; only a fraction are actually driving at any moment.
- Most telemetry feeds analytics/ML and fleet dashboards (soft real-time, seconds-to-minutes latency is fine), but a small subset — critical DTCs (e.g., brake system fault, thermal event) — needs sub-second to few-second alerting to on-call safety/ops teams.
- Per-vehicle ordering matters (e.g., "was the DTC raised before or after the speed spike?"), but cross-vehicle global ordering does not.
- At-least-once delivery with idempotent downstream processing is acceptable; true exactly-once end-to-end is not worth the complexity here.
- Raw telemetry should be replayable/reprocessable for at least 7 days (for pipeline bugs/backfills) and land in a long-term data lake (months to years) for ML training and fleet analytics.

---

## 1. Functional Requirements

**Core function** — the 1-3 things this system must fundamentally do; everything else below is elaboration on how:

1. Continuously ingest a heterogeneous stream of telemetry from up to a million vehicles despite each vehicle's connectivity being intermittent.
2. Get a small set of safety-critical signals to an alerting system within seconds, independent of the health of the much larger bulk-analytics path.
3. Make ingested telemetry durable and replayable so downstream consumers can be added or fixed without re-instrumenting the fleet.

State the fuller requirement list explicitly on the whiteboard before designing anything.

1. **Ingest telemetry from up to 1M vehicles** — a heterogeneous mix of signal types (GPS/location, speed, battery %, DTCs, and a rotating catalog of sensor readings) at varying frequencies.
2. **Edge buffering and store-and-forward** — the vehicle must locally buffer telemetry during connectivity loss and flush it once reconnected, without unbounded local storage growth.
3. **Schema validation and versioning** — every message is validated against a registered schema; the pipeline must support producers (vehicle firmware) and consumers (downstream jobs) evolving independently over time (different firmware versions in the field simultaneously).
4. **Hot path: real-time alerting** — critical signals (e.g., specific DTC codes, safety-relevant thresholds) must reach an alerting/dispatch system within a few seconds of being generated, independent of the health of the bulk analytics pipeline.
5. **Cold path: durable storage for analytics/ML** — all validated telemetry lands in a queryable, cost-efficient data lake for offline analytics, dashboarding, and ML model training.
6. **Replayability** — the raw ingested stream must be re-consumable (e.g., to backfill a new downstream consumer, or reprocess after fixing a bug in a stream job) for a bounded retention window.
7. **Per-vehicle ordering guarantee** — events from the same vehicle must be processed in the order they were generated, even as the pipeline scales horizontally across many consumers.
8. **Data-quality enforcement** — malformed, out-of-range, or unparseable messages must be quarantined (dead-lettered) rather than silently corrupting downstream aggregates.
9. **Horizontal scalability** — the ingestion tier must scale by adding capacity (partitions/brokers/consumers), not by redesigning the system, as fleet size grows from hundreds of thousands to millions.
10. **Backpressure handling** — a downstream slowdown (e.g., a stream processor falling behind) must not cause data loss or take down the ingestion tier; it should degrade gracefully (increased lag, not dropped data, within the retention window).

**Out of scope (state this explicitly):** the in-vehicle sensor fusion / ECU logic that produces the curated telemetry payload, the ML models themselves (we design the pipeline that feeds them), and the OTA update mechanism (a separate system — see the companion document on [OTA updates](./ota-update-system-for-connected-vehicle-fleet.md)).

---

## 2. Non-Functional Requirements

| Requirement | Target / Reasoning |
|---|---|
| **Scalability** | Support 500K vehicles today, 1M in 2 years, scaling horizontally (add partitions/brokers/consumers) rather than by redesign. |
| **Throughput** | Sustain bursty peaks of 100K+ messages/sec fleet-wide (e.g., morning commute) without falling behind. |
| **Hot-path latency** | Critical DTC/safety alerts: end-to-end (vehicle emits → alert delivered) under ~5 seconds at p99. |
| **Cold-path latency** | Analytics/ML data lake freshness: minutes, not seconds — a few minutes of staleness is acceptable and expected. |
| **Durability** | Zero silent data loss for validated messages once acknowledged by the ingestion tier; store-and-forward on the vehicle prevents loss during connectivity gaps. |
| **Ordering** | Per-vehicle (not global) ordering guaranteed for events on the same signal stream. |
| **Delivery semantics** | At-least-once, with idempotent/deduplicating consumers — true exactly-once is not required and would add unjustified complexity. |
| **Replayability** | Raw stream retained and re-consumable for at least 7 days; cold-path data lake retained for months to years. |
| **Bandwidth efficiency** | Cellular data is costly; edge pre-aggregation/sampling must materially reduce uplinked bytes versus raw sensor rates. |
| **Availability** | Ingestion tier: 99.9%+. Vehicle-side buffering means brief backend outages should be invisible to data completeness, only to freshness. |
| **Backpressure resilience** | A slow or failed downstream consumer must not cause ingestion-tier data loss or cascading failure — degrade via increased consumer lag, absorbed by log retention. |

Call out explicitly to the interviewer: *"This is fundamentally a streaming/data-infrastructure problem, not a request/response API problem. The core tension is between a small, latency-critical hot path and a large, throughput-oriented cold path — and the architecture needs to let one slow down without affecting the other."*

---

## 3. Back-of-the-Envelope Capacity Estimation

Doing this out loud shows quantitative rigor.

- **Fleet size:** 1,000,000 vehicles (design target), ~500,000 today.
- **Signal mix and frequency (post edge-aggregation, not raw sensor rate):**
  - GPS + speed + core vehicle state: 1 reading/sec while driving, 1 reading/60 sec ("heartbeat") while parked.
  - Battery %, odometer, and slower-changing signals: bundled into the same 1 Hz driving frame.
  - Rotating sensor readings (tire pressure, ambient temp, IMU summary, etc.): 1 reading/10 sec while driving.
  - DTCs: event-driven, not periodic — fired only on state change, effectively negligible in volume but critical in priority.
- **Peak concurrency:** assume at peak commute hours ~15% of the fleet is actively driving simultaneously → `1,000,000 × 15% = 150,000` concurrently active vehicles.
- **Peak message rate:** each active vehicle emits ~1 combined telemetry frame/sec (bundling GPS/speed/battery + any due sensor readings into one payload to amortize per-message overhead) → `150,000 vehicles × 1 msg/sec = 150,000 msgs/sec` at peak. Add a generous 30% headroom for uneven regional peaks and traffic-pattern skew → design for **~200,000 msgs/sec peak ingestion**.
- **Message size:** a compact binary encoding (e.g., Protobuf) with ~15-20 fields ≈ 300-500 bytes/message. Use 400 bytes as a working number.
- **Peak ingress bandwidth:** `200,000 msgs/sec × 400 bytes ≈ 80 MB/s ≈ 640 Mbps` sustained at peak fleet-wide — very manageable for a horizontally-scaled streaming cluster, but not something a single node or a naive REST API fronted by one database could absorb.
- **Daily volume (rough):** assume the average vehicle is actively driving ~1 hour/day (3,600 driving-seconds) and parked-but-connected the remaining 23 hours (heartbeat every 60s = 1,380 heartbeats/day).
  - Driving messages/day: `1,000,000 × 3,600 = 3.6B messages/day`.
  - Heartbeat messages/day: `1,000,000 × 1,380 ≈ 1.38B messages/day`.
  - **Total ≈ 5B messages/day fleet-wide**, at ~400 bytes average → `5,000,000,000 × 400 bytes ≈ 2 TB/day` of raw ingested telemetry.
- **Cold-path storage growth:** raw + enrichment overhead (vehicle metadata joins, schema/version tags) roughly doubles effective stored size before compression, but columnar formats (Parquet/ORC) with dictionary encoding on repeated fields typically compress 4-6x → net storage growth is comparable to or somewhat better than the raw 2 TB/day figure, i.e., **on the order of 1-2 TB/day (~30-60 TB/month, ~0.4-0.7 PB/year)** in the data lake. This is a job for cheap object storage with a columnar table format, not a traditional data warehouse charged per-row.
- **Kafka-style partitioning math:** to keep per-partition throughput manageable (a good rule of thumb is a few MB/s per partition for safety margin) at 80 MB/s peak, you'd want on the order of **50-100 partitions minimum** for the main telemetry topic purely for throughput — but the real driver ends up being consumer parallelism and hot-key avoidance (see §6.3), so in practice teams provision more, e.g., **512-1024 partitions**, to leave headroom for consumer group scale-out as the fleet grows toward 1M vehicles.

Conclusion to state out loud: *"The numbers say this is a moderate-scale streaming problem, not an extreme one — 200K msgs/sec and ~2 TB/day is well within what a properly partitioned Kafka-style cluster and a columnar data lake handle routinely. The real engineering challenge isn't raw throughput; it's edge bandwidth efficiency (cellular data costs money per vehicle), maintaining per-vehicle ordering while scaling horizontally, and isolating the tiny-but-critical hot path from the much larger cold path so a slow ML job never delays a safety alert."*

---

## 4. Data Model / Database Design

### Core entities

**`TelemetryFrame`** (the primary, high-volume streaming message — one per vehicle per reporting interval)
```
vehicle_id
schema_version        -- e.g. "telemetry.v3" — resolved against the schema registry
timestamp              -- vehicle-local monotonic clock + synced wall-clock offset
sequence_number         -- monotonically increasing per vehicle_id, used for dedup/gap detection
gps_lat, gps_lon, gps_accuracy_m
speed_kph
battery_pct
odometer_km
sensor_readings (map)   -- e.g. { "tire_pressure_fl": 32.1, "ambient_temp_c": 18.4, ... }
edge_buffered            -- bool: was this message delayed by store-and-forward (i.e., generated
                          --   while offline and flushed later)?
```
`sequence_number` (per `vehicle_id`) is what makes at-least-once delivery safe: a downstream consumer can detect and drop duplicates, and detect gaps (missing sequence numbers) that indicate buffer overflow or lost data on the vehicle side.

**`DTCEvent`** (diagnostic trouble code — low-volume, high-priority, event-driven, not periodic)
```
vehicle_id
dtc_code               -- e.g. "P0A80" (standardized OBD-II style code)
severity                -- INFO / WARNING / CRITICAL
timestamp
sequence_number
raised_or_cleared        -- this code was newly raised, or a previously active code cleared
context (JSON)           -- speed, gear, ambient conditions at time of event, for triage
```
`DTCEvent` is modeled and routed separately from `TelemetryFrame` even though both originate from the same vehicle, because its consumption pattern is entirely different: it needs a dedicated low-latency hot path (see §6.5), not batch analytics.

**`SchemaRegistryEntry`** (versioned contract between vehicle firmware and backend consumers)
```
schema_name (e.g. "telemetry_frame")
version (PK, composite with schema_name)
schema_definition (Protobuf/Avro IDL)
compatibility_mode       -- BACKWARD / FORWARD / FULL
status                    -- ACTIVE / DEPRECATED / RETIRED
min_supported_firmware_version
created_at
```
This is a small, low-write-volume, high-read-volume table (every producer and consumer checks it, effectively never writes to it except on release) — a good candidate for aggressive client-side caching with a short TTL, rather than a lookup on every single message.

**`VehicleMetadata`** (slow-changing dimension, joined during enrichment — not part of the hot streaming path)
```
vehicle_id (PK)
vin
model, hardware_revision
region
firmware_version
telemetry_schema_version  -- which schema this vehicle's firmware currently emits
```

**Cold-path storage layout** (data lake, e.g., Parquet/Iceberg on object storage)
```
telemetry_lake/
  dt=2026-08-04/
    hour=14/
      part-0000.parquet   -- partitioned by ingestion date+hour, and clustered/sorted by vehicle_id
                           --   within each file to make per-vehicle time-range queries efficient
```
Partition by date (for time-range queries and lifecycle/retention policies — e.g., "delete raw data older than 2 years") and secondarily sort/cluster by `vehicle_id` within each partition (for "give me vehicle X's history over the last month" queries, which are common for both ML feature generation and incident investigation).

### Why split the hot DTC path's storage from the bulk telemetry lake?

This is a good trade-off to narrate explicitly: *"`TelemetryFrame` is high-volume and consumed in large batches for analytics/ML — a great fit for a columnar data lake read by big batch/stream-processing jobs. `DTCEvent` is low-volume but latency-critical — it needs a low-latency, indexed store (e.g., a small operational database or an in-memory/stream-native store) that an alerting service can query or subscribe to within milliseconds, not a data lake meant for petabyte-scale batch scans. Forcing both through the same storage tier would either make the hot path too slow or make the cold path prohibitively expensive to run at telemetry volume."*

---

## 5. High-Level Design

This is an **infrastructure/topology view** — what pieces of infrastructure exist, what type each one is (log, cache, blob store, stateless service...), and how they're wired together — not a step-by-step trace of one message's journey. Sequencing and per-hop logic belong in the Deep Dives (§6); this section should stand on its own as "here's what we'd provision."

### Infrastructure tiers

**Edge tier (runs on the vehicle, outside our infrastructure footprint but part of the design)**
- **Edge Telemetry Agent** — an on-vehicle process, not a backend service. Reads the internal sensor/ECU bus, pre-aggregates/adaptively samples to control bandwidth, and owns a small local durable queue (store-and-forward) so connectivity loss never blocks or drops data at the source.

**Ingestion tier (the internet-facing boundary — where the fleet meets our infrastructure)**
- **Ingestion Gateway** — a horizontally-scaled, stateless fleet of connection terminators (e.g., an MQTT broker cluster or an HTTPS ingestion service behind a load balancer), built to hold millions of concurrent long-lived, low-throughput, intermittent connections. Its only jobs are auth and lightweight structural checks — no business logic.
- **Schema Registry** — a small, low-write/high-read control-plane service (its own lightweight datastore), consulted by both the edge agent and every downstream consumer to resolve `schema_version`. It sits *beside* the data path, not on it.

**Messaging backbone (the one piece of shared infrastructure everything else is built around)**
- **Streaming Ingestion Tier** — a durable, partitioned, replayable log (Kafka-style), partitioned by `hash(vehicle_id)`. This is the system's central nervous system: every tier downstream is just an independent reader of this log, at its own pace. This single design choice is what makes hot/cold isolation (below) possible without any direct coupling between them.

**Processing tier (two independently-provisioned consumer groups reading the same backbone)**
- **Hot-path processing** — a small, deliberately over-provisioned stream-processing cluster (validation + dedup + rules/threshold engine) sized for the DTC/critical-signal volume only, not fleet-wide volume.
- **Cold-path processing** — a much larger, throughput-oriented stream-processing cluster (validation + dedup + enrichment) sized for bulk telemetry volume, and allowed to lag under load without violating any SLA.

**Storage / serving tier**
- **Alerting / Dispatch system** — the hot path's downstream sink; an existing on-call/paging system, treated as an external dependency we push into.
- **Data Lake** — columnar object storage (Parquet/Iceberg), partitioned by date and clustered by `vehicle_id`; the cold path's sink, read by ML training jobs and BI/dashboarding tools.

**Supporting infrastructure (cross-cutting, attached to multiple tiers rather than sitting in the data path)**
- **Vehicle Metadata Service** — a small, cacheable lookup service for slow-changing dimension data (VIN, region, firmware version), used by the processing tier for enrichment via broadcast/cached joins — never a per-message synchronous call on the hot path.
- **Monitoring / Consumer-Lag Tracking** — an observability layer spanning the gateway, the backbone, and both processing clusters; not a functional component of the data path, but load-bearing for detecting backpressure and data-quality regressions.

### Topology diagram (infrastructure view, described in ASCII)

```
   EDGE TIER              INGESTION TIER                  MESSAGING BACKBONE
 ┌───────────────┐      ┌────────────────────┐          ┌──────────────────────────┐
 │ Edge Telemetry │      │ Ingestion Gateway   │          │  Streaming Ingestion      │
 │ Agent          │─────►│ (stateless, auth,   │─────────►│  Tier — durable,          │
 │ (store-and-    │      │ conn. termination)   │          │  partitioned, replayable  │
 │  forward)      │      └──────────┬──────────┘          │  log, keyed by vehicle_id │
 └───────────────┘                  │                      │                          │
                                     ▼                      │  (the shared source of   │
                          ┌────────────────────┐            │   truth — every tier      │
                          │ Schema Registry     │◄──────────►│   below reads it          │
                          │ (control plane;      │            │   independently)          │
                          │  side-car, not on     │            └────────────┬─────────────┘
                          │  the data path)       │                         │
                          └────────────────────┘                         │
                                                                          │
                        PROCESSING TIER          (two independently-provisioned consumer groups)
                        ┌─────────────────────────────────────┴──────────────────────────────────┐
                        ▼                                                                          ▼
             ┌───────────────────────┐                                                 ┌───────────────────────┐
             │ HOT-PATH CLUSTER       │                                                 │ COLD-PATH CLUSTER      │
             │ validate + dedup +     │                                                 │ validate + dedup +     │
             │ rules engine           │                                                 │ enrichment             │
             │ (small, over-          │                                                 │ (large, throughput-    │
             │  provisioned)          │                                                 │  oriented, lag-        │
             └───────────┬───────────┘                                                 │  tolerant)             │
                         │                                                              └───────────┬───────────┘
     STORAGE / SERVING   ▼                                                                           ▼
     TIER      ┌───────────────────────┐                                                 ┌───────────────────────┐
               │ Alerting / Dispatch    │                                                 │ Data Lake (Parquet/    │
               │ (external system)      │                                                 │ Iceberg) → ML / BI     │
               └───────────────────────┘                                                 └───────────────────────┘

 SUPPORTING (cross-cutting, attached to processing tier — not shown per-arrow above):
   • Vehicle Metadata Service   — cached enrichment lookup, consulted by both clusters
   • Monitoring / Consumer-Lag  — observes gateway health + lag on both consumer groups
```

Narrate the key architectural decision: *"The one piece of infrastructure everything else hangs off is the durable, replayable log. Hot and cold are not two steps in a pipeline — they're two independently-provisioned consumer groups that happen to read the same backbone at completely different rates. That's the whole trick: a slow ML batch job or a data lake outage can never delay a safety-critical DTC alert, because they're not sharing any compute, only a shared, replayable source of truth. Everything else on this diagram — the gateway, the schema registry, the metadata service — is either a stateless edge terminator or a small side-car control-plane service; the real capacity-planning conversation is entirely about the backbone and the two processing clusters."*

---

## 6. Detailed Design / Deep Dives

Pick 2-3 of these based on interviewer interest — you won't have time for all of them in 45 minutes, so ask: *"Which of these would you like me to go deeper on: edge bandwidth reduction, delivery semantics, partitioning/ordering, schema evolution, or backpressure handling?"*

### 6.1 Edge pre-aggregation and adaptive sampling

- Raw internal sensor/CAN-bus data can be sampled at tens to hundreds of Hz, but uplinking at that rate over cellular for a million vehicles is infeasible (and expensive per-vehicle). The edge agent's job is to compress the *information*, not just the bytes.
- **Adaptive frequency:** report at 1 Hz while driving (state is changing rapidly and matters for safety/UX), drop to a 60-second heartbeat while parked (state is nearly static — battery slowly self-discharging, nothing moving).
- **Delta/threshold-based reporting for slow-changing signals:** for a signal like ambient temperature, only emit a new reading if it changed by more than a threshold since the last report, rather than on a fixed clock — this can cut volume substantially for signals that are often flat.
- **Rotating/round-robin sensor coverage:** not every sensor needs to be in every frame; the tire-pressure and IMU-summary fields can rotate across frames (e.g., report tire pressure on frame N, IMU summary on frame N+1) if they change slowly relative to the 1 Hz frame rate — this amortizes payload size without losing meaningful resolution.
- **Batching + compression:** multiple 1-second frames are batched into a single uplink message every few seconds and compressed (e.g., gzip/Protobuf's natural compactness), amortizing per-message transport overhead (TLS handshake reuse, header overhead) which otherwise dominates at small payload sizes.
- *Trade-off to mention:* aggressive edge sampling risks losing a transient signal that only appears between sampling points; DTCs and safety-relevant thresholds are therefore always event-driven (fire immediately on state change) rather than subject to the periodic/adaptive sampling policy — the two policies coexist deliberately.

### 6.2 Store-and-forward buffering and delivery semantics (at-least-once vs. exactly-once)

- The edge agent writes telemetry to a small local durable queue (e.g., a bounded on-disk ring buffer) before attempting uplink. If connectivity is unavailable, messages accumulate locally rather than being dropped or blocking the vehicle's other systems.
- **Bounded buffer with priority-aware eviction:** the buffer has a finite size (vehicles don't have unlimited storage). When full, evict the oldest *low-priority* telemetry first (e.g., routine sensor readings), and never evict DTCs/safety events — if something has to be lost during an extended outage, it should be the least important data, not the most important.
- **Why at-least-once, not exactly-once end-to-end:** guaranteeing exactly-once across an unreliable network, a store-and-forward buffer, and a distributed streaming system requires either distributed transactions or complex two-phase idempotency protocols across every hop — high engineering cost for marginal benefit here, since duplicates are cheap to detect and drop downstream (via `sequence_number` per `vehicle_id`) and telemetry is not financial/transactional data where a duplicate would cause real harm.
- **Idempotent consumers via sequence numbers:** every message carries a monotonically increasing `sequence_number` scoped to `vehicle_id`. The validation layer maintains a small watermark per vehicle and drops/logs anything at or below the last-seen sequence number — this makes retries (from network blips, at-least-once redelivery, or reconnect-and-resend) safe by construction.
- **Gap detection as a feature, not just a defense:** a jump in `sequence_number` (e.g., from 1042 to 1201) tells the backend the vehicle's buffer overflowed and evicted messages — this is itself useful telemetry (which vehicles/regions are chronically under-connected) rather than just a data-loss annoyance to shrug off.

### 6.3 Partitioning strategy and per-vehicle ordering guarantees

- Telemetry topics are partitioned by `hash(vehicle_id) % num_partitions`. This guarantees that all messages for a given vehicle always land on the same partition, and since a partition is consumed in order by a single consumer at a time, **per-vehicle ordering is preserved automatically** without any additional coordination.
- **Why not partition by time or randomly?** Random/round-robin partitioning would maximize even load distribution but destroy per-vehicle ordering (messages from the same vehicle could be processed out of order by different consumers concurrently) — unacceptable given the requirement to reason about event sequence per vehicle (e.g., "DTC before or after the speed spike").
- **Hot-partition risk and mitigation:** vehicle IDs are effectively random (VINs/UUIDs), so a good hash function distributes load evenly across partitions in practice — there's no natural "celebrity vehicle" analogous to a celebrity user in a social app, so this is a comparatively low-risk hot-key scenario, but it's worth explicitly stating why (interviewers sometimes probe for hot-key awareness).
- **Partition count as a capacity/ordering trade-off:** more partitions = more consumer parallelism and higher aggregate throughput, but partition count is expensive to change later (repartitioning changes the `vehicle_id → partition` mapping, breaking the ordering guarantee for any in-flight or replayed data unless done very carefully with a migration window). Provision generously upfront (see §3's 512-1024 partition estimate) rather than under-provisioning and needing a disruptive repartition later.
- **Consumer group scaling:** because ordering is per-partition, the maximum useful consumer parallelism for a single logical consumer (e.g., the validation layer) equals the partition count — this is the concrete mechanism tying "how many partitions" to "how much we can horizontally scale."

### 6.4 Schema registry and data-quality validation

- Vehicle firmware is deployed incrementally across a fleet (recall the OTA design) — at any moment, vehicles in the field may be running dozens of different firmware versions, each potentially emitting a slightly different telemetry schema. The backend must handle this heterogeneity gracefully, not assume a single current schema.
- **Backward-compatible evolution by default:** new fields are added as optional with sensible defaults; existing fields are never repurposed or removed without a deprecation window. This lets old firmware keep working against new consumers, and new firmware's extra fields be safely ignored by consumers that don't yet understand them.
- **Schema version tagged per message:** every `TelemetryFrame` carries `schema_version`, so the validation layer knows exactly which schema to validate against, rather than guessing or assuming fleet-wide uniformity.
- **Data-quality checks beyond structural validation:** range checks (e.g., `battery_pct` between 0-100, `speed_kph` non-negative and below a physically plausible maximum), null/missing-field checks for required fields, and cross-field sanity checks (e.g., speed > 0 but GPS shows no movement over several frames could indicate a sensor fault worth flagging, not necessarily rejecting).
- **Dead-letter queue, not silent drop or silent pass-through:** records failing validation are routed to a dead-letter topic with the failure reason attached, rather than either crashing the pipeline or silently letting bad data corrupt downstream aggregates/ML training data. A regular review of dead-letter volume by signal type is itself a useful data-quality/fleet-health signal (e.g., a spike after a specific firmware rollout points straight at the regression).

### 6.5 Backpressure handling and hot/cold path isolation

- The durable, replayable log (§5) is the key mechanism: producers (the ingestion gateway) write at their own pace, and each consumer group reads independently at its own pace, bounded only by the topic's retention window. A slow consumer doesn't block ingestion — it just accumulates lag, which is visible and alertable, not silently lossy.
- **Hot path is provisioned for its (small) load, not the fleet's total load:** the real-time alerting consumer only subscribes to the low-volume DTC/critical-signal stream, so it can be over-provisioned relative to its actual load cheaply, guaranteeing headroom — decoupling it from bulk telemetry volume is precisely what makes this affordable.
- **Cold-path backpressure is expected and tolerable:** if the stream-to-lake sink falls behind during a traffic spike or a maintenance window, that's an acceptable, monitored condition (consumer lag rises, catches up later) as long as it stays within the log's retention window (§1's 7-day replayability requirement exists partly to give this subsystem room to catch up after an incident).
- **Ingestion Gateway sheds load at the edge, not the log:** if the gateway itself is overwhelmed (e.g., a regional connectivity restoration causes a burst of reconnecting vehicles all flushing buffers at once — a "thundering herd" after an outage), it should apply admission control/rate-limiting per-vehicle or per-region with client-side backoff/jitter, rather than let an unbounded burst overwhelm the streaming tier's write path.

---

## 7. Minimal API Surface (illustrative)

```
# Vehicle-facing (via the Ingestion Gateway)
POST /v1/vehicles/{vehicle_id}/telemetry
     → batched TelemetryFrame(s), schema_version-tagged, sequence_number-ordered
     (at-least-once; safe to retry after reconnect due to sequence_number dedup)

POST /v1/vehicles/{vehicle_id}/dtc-events
     → DTCEvent(s), routed directly into the hot path
     (higher priority than the bulk telemetry endpoint; smaller payloads, lower latency budget)

GET  /v1/schemas/{schema_name}/latest
     → current active schema version + compatibility mode, checked by edge agent on boot/update

# Internal / operator-facing
GET  /v1/pipeline/consumer-lag?topic=telemetry.raw
     → per-partition lag, used for backpressure/health dashboards

GET  /v1/pipeline/dead-letter?since=<ts>&signal=<name>
     → recent validation failures, grouped by reason and firmware version
```

---

## 8. Trade-offs and Alternatives Considered

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| Delivery semantics | At-least-once + idempotent, sequence-number-based dedup | Exactly-once end-to-end | Exactly-once across an unreliable edge network and a distributed log requires distributed transactions/complex protocols for marginal benefit; telemetry duplicates are cheap to detect and drop. |
| Partitioning key | `vehicle_id` hash | Random/round-robin, or partition by time | Preserves per-vehicle ordering, which is a stated functional requirement; random partitioning maximizes even load but destroys ordering guarantees. |
| Hot vs. cold path | Two independent consumer groups off the same durable log | A single unified pipeline for all telemetry | Isolates the tiny, latency-critical DTC/alerting path from the much larger bulk-analytics path so neither can starve or delay the other. |
| Edge data reduction | Adaptive sampling + delta reporting + rotating sensor coverage | Uplink all raw sensor data continuously | Cellular bandwidth is a real per-vehicle cost; raw high-frequency streaming from a million vehicles is both infeasible and unnecessary for most analytics use cases. |
| Schema evolution | Centralized versioned registry, backward-compatible by default | Ad hoc/implicit schema agreement between firmware and backend | Fleets run many firmware versions concurrently (staged OTA rollouts); a registry with enforced compatibility avoids silent breakage when producers and consumers evolve independently. |
| Storage for bulk telemetry | Columnar data lake (Parquet/Iceberg) on object storage | Traditional row-oriented data warehouse | Multi-terabyte/day analytical workloads with wide scans (ML feature generation, fleet-wide aggregation) are far cheaper and faster on columnar formats than row stores; object storage decouples storage cost from compute. |
| Backpressure strategy | Durable replayable log absorbs lag; consumers pull at their own pace | Push-based fan-out to consumers with synchronous acknowledgment | Pull-based consumption lets slow consumers fall behind without blocking producers or other consumers — critical for isolating hot and cold paths from each other. |

---

## 9. Failure Modes & Edge Cases to Call Out Proactively

- **Vehicle offline for an extended period (days):** the local buffer eventually fills; priority-aware eviction (§6.2) drops low-priority telemetry first and preserves DTCs, but this should be visible as a fleet-health metric (vehicles with high eviction rates likely have chronic connectivity issues worth investigating).
- **Thundering herd after a regional outage:** many vehicles reconnect and flush buffers simultaneously (e.g., after a cellular tower or backend outage is resolved); mitigate with client-side jittered backoff and gateway-side admission control/rate-limiting rather than letting the burst hit the streaming tier unshaped.
- **Firmware bug producing malformed or out-of-range telemetry at scale:** the dead-letter mechanism (§6.4) contains the damage to a quarantine queue instead of corrupting downstream aggregates/ML training sets; a spike in dead-letter volume correlated with a specific firmware version is a strong, fast diagnostic signal.
- **Clock skew on the vehicle:** vehicle-local clocks can drift or be wrong (especially before GPS lock); timestamps should be reconciled with the ingestion-time and, where possible, GPS-derived time, and downstream consumers should tolerate minor out-of-order arrival even within a single vehicle's ordered partition.
- **Sequence number gap without an actual outage (e.g., a bug that skips sequence numbers):** distinguish this from real buffer-overflow eviction by cross-checking against the `edge_buffered` flag and reported buffer-eviction counters — don't assume every gap means a real outage occurred.
- **Consumer lag growing unbounded on the cold path:** if a stream-to-lake job falls behind faster than it can catch up (e.g., a bug causing per-record processing to slow down), it will eventually hit the log's retention window and start losing the ability to replay from the true beginning — alert well before retention is exhausted, not after.
- **A "storm" of DTCs from a single vehicle (e.g., a genuinely failing vehicle spamming fault codes):** the hot path should rate-limit/deduplicate repeated identical DTCs per vehicle within a short window so one malfunctioning vehicle doesn't flood the alerting system and drown out other vehicles' genuine alerts.
- **New, previously-unseen schema version arriving from firmware that shipped ahead of a backend deploy:** the validation layer should reject/dead-letter gracefully with a clear "unknown schema version" reason rather than crash — this is a coordination/release-ordering problem (backend schema support should roll out before or alongside firmware, never after) worth calling out explicitly.

---

## 10. Monitoring, Observability, and Security (brief)

- **Dashboards:** per-region and fleet-wide ingestion rate, per-partition consumer lag (both hot and cold path consumer groups), dead-letter rate by signal/firmware version, and end-to-end hot-path latency (p50/p99, vehicle-emit-to-alert-delivered).
- **Alerting:** page on-call when hot-path latency exceeds the ~5-second SLA, when consumer lag on the hot path grows (even briefly), or when dead-letter volume spikes above baseline (likely a firmware regression).
- **Data-completeness monitoring:** track "expected vs. actually reporting" vehicles per region/time window — a silent drop in reporting vehicles (without a corresponding connectivity outage signal) can indicate an edge-agent bug rather than genuine offline vehicles.
- **Security:** mutual TLS or signed-token authentication for vehicle-to-gateway connections (prevent spoofed telemetry from an unauthorized source); payload size/rate limits per vehicle at the gateway (prevent a single compromised or malfunctioning vehicle from degrading service for others); schema validation doubles as a lightweight defense against malformed/malicious payloads reaching downstream storage.

---

## 11. Wrap-up / How to Close the Interview

Summarize in 30 seconds: *"To recap: telemetry flows from an edge agent that pre-aggregates and adaptively samples to control bandwidth, through a store-and-forward buffer that survives connectivity gaps, into a partitioned, replayable streaming log keyed by vehicle_id for per-vehicle ordering. From there, two independent consumer groups fork off the same log — a small, over-provisioned hot path for sub-5-second safety alerting, and a much larger cold path feeding a columnar data lake for analytics and ML — so the two never contend for the same capacity or block each other. At-least-once delivery with sequence-number-based dedup, plus a versioned schema registry, lets the system tolerate an unreliable network and a fleet running many firmware versions simultaneously."*

Then proactively offer a couple of extension directions, showing you know where the design could go next:
- How would you extend the hot path to support streaming anomaly detection (ML-based) rather than just static threshold rules — and how would you keep that within the same latency budget?
- How would this design change if a downstream consumer needed genuinely stronger consistency (e.g., billing based on telemetry) rather than analytics-grade at-least-once semantics?
- How would you evolve the partitioning scheme if a future requirement needed cross-vehicle correlation (e.g., "all vehicles in this geofence in the last 5 minutes") that a pure per-vehicle-ordered partition scheme doesn't naturally support?

---

## 12. Follow-up Questions Interviewers May Ask

- "Walk me through what happens end-to-end, in order, from a DTC being raised on the vehicle to an on-call engineer being paged — where could latency creep in, and how would you find it?"
- "How would you detect that a specific firmware version is silently sending corrupted telemetry that passes schema validation but is semantically wrong (e.g., GPS coordinates that are valid numbers but off by a fixed offset)?"
- "If you had to cut peak bandwidth usage by 50% without dropping any DTCs, what would you change first?"
- "How do you reprocess 3 days of historical telemetry through a newly fixed validation job without disrupting live ingestion?"
- "What happens to per-vehicle ordering guarantees if you need to increase the number of partitions on the main topic after the system is already live with a million vehicles?"
- "How would you extend this pipeline to support a new signal type that needs a much higher frequency (e.g., 10 Hz) than everything else, without blowing up bandwidth or overloading the shared partitions?"
- "This design assumes cellular connectivity end-to-end — how would it change to also support Wi-Fi-based bulk uploads for less time-sensitive, higher-volume data (e.g., periodic full sensor dumps for ML training) opportunistically?"

---

## References

- Rivian system design round context: see [`../rivian/index.md`](../rivian/index.md), section "System Design Interview Questions."
- Companion document: [OTA Update System for a Fleet of Connected Vehicles](./ota-update-system-for-connected-vehicle-fleet.md) — shares the same store-and-forward, offline-first constraints on the vehicle side.
- Conceptually similar to real-world IoT/connected-device telemetry architectures (e.g., Kafka-based ingestion with a schema registry, hot/cold path separation, and lakehouse-style analytical storage) used across the automotive and broader IoT industry.
