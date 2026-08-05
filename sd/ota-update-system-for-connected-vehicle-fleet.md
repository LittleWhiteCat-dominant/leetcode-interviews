# System Design Mock Interview: OTA Update System for a Fleet of Connected Vehicles

**Company theme:** Rivian-style (vehicle/EV), also broadly applicable to Tesla, Ford, Waymo, or any connected-fleet company.
**Round:** System Design (45-60 min onsite loop)
**Interviewer expectation:** Structured problem-solving, not a specific tech stack. Clarify → requirements → estimate → high-level → deep dive → trade-offs → wrap-up.

This document is written as a self-contained interview walkthrough: it includes the clarifying questions you should ask, a model answer for each section, and the follow-up probes an interviewer is likely to throw at you.

---

## 0. Opening: Clarify the Problem (first 3-5 minutes)

Don't start designing immediately. Restate the prompt and ask clarifying questions to narrow scope. Sample dialogue:

> **You:** "Before I dive in, let me make sure I understand the scope. When you say 'OTA update system,' are we covering the full lifecycle — build/sign, distribution, rollout orchestration, and the in-vehicle agent that applies the update — or should I focus on one layer?"
>
> **Interviewer:** "Assume the firmware/software artifacts already exist and are signed. Focus on distributing and safely applying them to the fleet."
>
> **You:** "Got it. A few more questions:
> 1. What's being updated — infotainment apps only, or safety-critical ECUs (e.g., steer-by-wire, ADAS)?
> 2. What's the fleet size we should design for?
> 3. Should updates be mandatory (recall-style, security patch) or optional (user-initiated, like a phone update)?
> 4. What connectivity can we assume — cellular (LTE/5G), Wi-Fi at home, or both?
> 5. Is rollback a hard requirement, or can we assume updates rarely fail?"

Assume the interviewer answers:
- Both infotainment and safety-critical ECUs, but safety-critical ones need extra rigor (fail-secure, functional-safety alignment with ISO 26262).
- Fleet size: ~2 million vehicles today, growing to 5 million in 3 years.
- Mix of mandatory (security/safety patches) and optional (feature updates) rollouts.
- Cellular is the primary always-on channel; Wi-Fi is opportunistic and preferred for large payloads.
- Rollback is a hard requirement — a bricked vehicle is unacceptable.

---

## 1. Functional Requirements

State these explicitly on the whiteboard before designing anything.

1. **Package management** — build, sign, and register new firmware/software packages, versioned per ECU/component.
2. **Delta generation** — produce differential (delta) packages between any two supported versions to minimize payload size.
3. **Campaign/rollout management** — target a rollout to a cohort of vehicles (by region, model year, hardware revision, or percentage-based ring) and control rollout velocity.
4. **Vehicle-side agent** — download, verify, stage, and apply updates; support pause/resume across connectivity loss; report status back.
5. **Atomic apply with rollback** — an interrupted or failed update must never leave the vehicle in a non-functional ("bricked") state; automatic rollback to the last-known-good version.
6. **Status & fleet visibility** — real-time dashboard of rollout progress (per version, per region, success/failure/in-progress counts) for release engineers.
7. **Pause / halt / rollback a campaign** — if a rollout shows anomalies (elevated failure rate, crash telemetry spike), operators can halt or reverse it fleet-wide.
8. **User consent & scheduling** (for non-critical/optional updates) — the driver can defer a non-urgent update or schedule it (e.g., "install tonight while parked").
9. **Audit trail** — every update attempt, version transition, and operator action is logged immutably for compliance and incident investigation.

**Out of scope (state this explicitly):** the CI/CD pipeline that builds and code-signs binaries, the in-vehicle infotainment UI, and billing/entitlement — assume these are handled elsewhere and we consume their output (a signed artifact + manifest).

---

## 2. Non-Functional Requirements

| Requirement | Target / Reasoning |
|---|---|
| **Availability** | Backend control plane: 99.95%+. The vehicle-side agent must function correctly even when the backend is fully unreachable (offline-first). |
| **Reliability / Safety** | Zero-bricking guarantee. An interrupted flash, power loss mid-update, or corrupted payload must always be recoverable via rollback. This is the single most important NFR — treat it as a hard constraint, not a nice-to-have. |
| **Scalability** | Support 2M vehicles today, 5M in 3 years, without redesigning the distribution tier. A single campaign may need to reach millions of vehicles over days to weeks. |
| **Bandwidth efficiency** | Cellular data is expensive and often metered; delta updates should reduce payload size by 70-90%+ versus full images. |
| **Intermittent connectivity** | Vehicles routinely lose connectivity (tunnels, parking garages, rural dead zones, cellular handoff). Downloads and status reporting must be resumable and eventually-consistent, not synchronous/blocking. |
| **Security** | End-to-end integrity and authenticity: signed manifests, signed packages, secure boot chain of trust, protection against downgrade/replay attacks. |
| **Rollout controllability** | Ability to throttle a rollout to X% of the fleet per hour/day, and to halt within minutes of detecting anomalies. |
| **Latency (not the primary concern)** | Unlike a typical web service, update delivery is not latency-sensitive — a rollout completing over hours to days is acceptable. Design for throughput and reliability, not p99 latency. |
| **Observability** | Every vehicle's update state must be queryable in near-real-time (target: staleness under a few minutes once connectivity is available). |

Call out explicitly to the interviewer: *"This system is optimized for reliability and controllability over latency — very different from a typical consumer web service, and that shapes almost every design decision below."*

---

## 3. Back-of-the-Envelope Capacity Estimation

Doing this out loud shows quantitative rigor.

- **Fleet size:** 2,000,000 vehicles (design target: 5,000,000).
- **Update frequency:** assume ~2 campaigns/month on average across all ECUs combined (mix of security patches and feature releases).
- **Full firmware image size:** ~2 GB for a major infotainment/ADAS bundle; delta updates average ~150-300 MB (85-90% reduction is realistic for binary diffing on similar builds).
- **Total monthly egress (delta-only, steady state):** `2,000,000 vehicles × 2 campaigns × 250 MB ≈ 1 PB/month` — this justifies putting a CDN in front of the origin store rather than serving directly from application servers.
- **Status reporting:** each vehicle reports state transitions (download started/progress/complete, verify, apply, reboot, success/fail) — call it ~10 events per update × 2M vehicles × 2 campaigns/month ≈ 40M events/month, i.e. a modest, bursty stream (bursty because a campaign ramps over days, not spread evenly).
- **Peak concurrent downloads:** if a canary ring is 1% of fleet, that's 20,000 vehicles; a full-fleet ring at say 20%/day is 400,000 vehicles initiating downloads over a day — spread using a rollout scheduler, not a thundering herd at t=0.
- **Database sizing:** the fleet state table has one row (or small document) per vehicle per component ≈ 2M × (number of updatable components, say 10) = 20M rows — trivial for a modern OLTP store with proper indexing/partitioning, but the *event/audit log* grows unbounded and should live in a separate append-only/time-series store.

Conclusion to state out loud: *"The bottleneck isn't compute or a single database — it's egress bandwidth and avoiding synchronized load spikes across a huge fleet. That drives us toward a CDN-backed distribution tier and an explicit rollout-pacing/rate-limiting mechanism."*

---

## 4. Data Model / Database Design

### Core entities

**`Package`** (a signed, immutable build artifact for one component/ECU)
```
package_id (PK)
component_id        -- e.g. "adas-ecu", "infotainment", "battery-bms"
version              -- semver, e.g. 4.2.1
artifact_url         -- pointer to blob storage (full image)
checksum_sha256
signature            -- signature over the manifest, verified against a trusted root
size_bytes
release_notes
created_at
```

**`DeltaPackage`** (a precomputed diff between two `Package` versions for a component)
```
delta_id (PK)
component_id
from_version
to_version
delta_artifact_url
checksum_sha256
signature
size_bytes
```
Delta packages are generated proactively for common upgrade paths (e.g., "last 3 shipped versions → latest") rather than on-demand, to keep the vehicle-side download path simple and cacheable.

**`Campaign`** (a rollout of a specific package/version to a cohort)
```
campaign_id (PK)
component_id
target_version
cohort_filter        -- JSON: region, model_year, hw_revision, or explicit vehicle_id list
rollout_strategy      -- e.g. "canary_1pct_then_ring", "linear_20pct_per_day"
priority               -- mandatory (security/recall) vs optional
status                 -- draft / active / paused / halted / completed
created_by, created_at
```

**`VehicleUpdateState`** (current state per vehicle per component — this is the "device shadow" for OTA)
```
vehicle_id, component_id (composite PK)
current_version
target_campaign_id     -- nullable, the campaign currently assigned (if any)
target_version
state                   -- IDLE / DOWNLOAD_PENDING / DOWNLOADING / DOWNLOADED /
                        --   VERIFYING / STAGED / APPLYING / REBOOTING /
                        --   SUCCESS / FAILED / ROLLED_BACK
download_offset_bytes    -- checkpoint for resumable download
last_reported_at
retry_count
```
This is the single most frequently read/written table — read by the rollout orchestrator to decide who to notify next, and written by the vehicle agent (via the backend) on every state transition. Partition/shard by `vehicle_id` hash for horizontal scale.

**`UpdateEvent`** (append-only audit log, one row per state transition — never updated, only inserted)
```
event_id (PK)
vehicle_id
component_id
campaign_id
from_state, to_state
timestamp
metadata (JSON)          -- error codes, bytes transferred, signal strength, etc.
```
This belongs in a time-series or append-optimized store (e.g., a columnar/event store), not the same OLTP database as `VehicleUpdateState`, because it's write-heavy, append-only, and queried mostly by time-range for dashboards/incident investigation — very different access patterns from the hot, frequently-updated device-shadow table.

### Why split hot state from the audit log?

This is a good trade-off to narrate explicitly: *"`VehicleUpdateState` is small, frequently updated, and needs low-latency point lookups/updates — a good fit for a sharded relational or key-value store. `UpdateEvent` is append-only, grows unbounded, and is queried by time range and aggregation for dashboards — a good fit for a columnar/time-series store or a data warehouse fed by a stream. Mixing them into one table would force one storage engine to serve two very different access patterns poorly."*

---

## 5. High-Level Design

This is an **infrastructure/topology view** — what pieces of infrastructure exist, what type each one is (blob store, durable log, control-plane service, database...), and how they're wired together — not a step-by-step trace of one campaign's rollout. Sequencing and per-hop logic belong in the Deep Dives (§6); this section should stand on its own as "here's what we'd provision."

### Infrastructure tiers

**Edge tier (runs on the vehicle, outside our infrastructure footprint)**
- **Vehicle OTA Agent** — an on-vehicle state machine, not a backend service. Downloads, verifies, stages, applies, and reports status. Owns a small local durable queue (store-and-forward) so it keeps making correct decisions with zero connectivity for hours or days.
- **Dual A/B Partitions (flash + boot)** — the vehicle-local half of rollback/recovery: the update flashes to the inactive partition while the active one keeps running, giving fail-secure rollback at the bootloader level, independent of any backend availability.

**Ingestion/gateway tier (the boundary where the fleet meets our infrastructure)**
- **Vehicle Communication Gateway** — a horizontally-scaled, stateless fleet of connection terminators (MQTT/HTTPS), built to hold millions of long-lived, low-throughput, intermittent connections. Its jobs are auth, notification delivery, and manifest/status relay — no rollout logic lives here.

**Control-plane services (consulted for orchestration, not on the byte-delivery path)**
- **Campaign Orchestrator** — where release engineers create campaigns, define cohorts and rollout strategy, and monitor/pause/halt. A low-throughput, human-facing control surface.
- **Rollout Scheduler / Notifier** — walks `VehicleUpdateState` for vehicles matching an active campaign's cohort, and enqueues paced "update available" notifications through the gateway to avoid a thundering herd. Logically part of the control plane even though it emits into the gateway's data path.
- **Rollback/Recovery policy layer** — a backend service that watches aggregated failure rate per campaign and auto-halts it when a threshold is crossed; the backend-side counterpart to the vehicle-local A/B rollback mechanism above.

**Distribution / data-plane tier (a separate, much higher-throughput pipe than the control plane)**
- **Package/Artifact Store** — durable blob storage (e.g., S3-style object store) holding signed full images and delta packages.
- **CDN** — fronts the artifact store for fleet-scale download egress; vehicles fetch bytes here via a short-lived signed URL, never from the control plane directly.

**Messaging backbone (the shared piece of infrastructure the status side fans out from)**
- **Status Ingestion Stream** — a durable, partitioned log (Kafka-style) that every vehicle's `UpdateEvent`s are written into; every downstream store below is just an independent reader of this one stream.

**Storage / serving tier (two different types for two very different access patterns)**
- **`VehicleUpdateState` store** — a low-latency, frequently-written/read key-value or document store (the "device shadow"), sharded by `vehicle_id`.
- **Audit/Event Store** — an append-only, time-series/columnar store for `UpdateEvent` history, optimized for time-range scans, not point lookups.

**Supporting infrastructure (cross-cutting, attached beside the data path)**
- **Dashboards + Alerts (anomaly detection)** — observes rollout funnels and failure-rate thresholds across campaigns; not a functional hop in the data path, but load-bearing for detecting a bad rollout early.

### Topology diagram (infrastructure view, described in ASCII)

```
   EDGE TIER                 INGESTION TIER              CONTROL PLANE (side-car)
 ┌──────────────────┐      ┌────────────────────┐      ┌───────────────────────────┐
 │ Vehicle OTA Agent  │      │ Vehicle Comm        │      │ Campaign Orchestrator      │
 │ (state machine) +  │◄────►│ Gateway             │◄────►│  + Rollout Scheduler       │
 │ local queue +      │      │ (stateless, MQTT/   │      │  + Rollback/Recovery       │
 │ A/B partitions      │      │  HTTPS boundary)    │      │  policy layer (auto-halt)  │
 └─────────┬──────────┘      └──────────┬──────────┘      └───────────────────────────┘
           │                            │ status events (buffered when offline)
           │ fetch bytes via                           ▼
           │ short-lived signed URL          MESSAGING BACKBONE
           │                       ┌───────────────────────────────┐
           │                       │ Status Ingestion Stream         │
           │                       │ (durable, partitioned log) —    │
           │                       │ every store below reads it      │
           │                       │ independently                   │
           │                       └───────────┬─────────┬───────────┘
           ▼                                   ▼         ▼
 DISTRIBUTION / DATA PLANE          STORAGE / SERVING TIER
 ┌───────────────────────┐     ┌───────────────────────┐   ┌───────────────────────┐
 │ CDN → Package/Artifact  │     │ VehicleUpdateState      │   │ Audit/Event Store       │
 │ Store (blob storage,    │     │ (hot device shadow, KV) │   │ (append-only, time-     │
 │ signed full + delta      │     └───────────────────────┘   │  series)                │
 │ images)                  │                                  └───────────────────────┘
 └───────────────────────┘

 SUPPORTING (cross-cutting, attached to the messaging backbone — not shown per-arrow above):
   • Dashboards + Alerts — observes campaign rollout funnels and failure-rate thresholds
```

Narrate the key architectural decision: *"The vehicle never talks to the control plane for the actual update bytes — it fetches them from the CDN using a short-lived signed URL, so the low-throughput orchestration path (campaigns, cohorts, pacing) is entirely decoupled from the high-throughput data-plane path (petabytes of egress). The other piece of shared infrastructure is the status stream: it's the one backbone that both the hot device-shadow store and the append-only audit log read independently, so a slow audit-log writer can never delay a device's current-state lookup. Everything else — the gateway, the orchestrator, the rollback policy layer — is either a stateless edge terminator or a small side-car control-plane service; the real capacity-planning conversation is about the CDN/artifact store and the status stream."*

---

## 6. Detailed Design / Deep Dives

Pick 2-3 of these based on interviewer interest — you won't have time for all of them in 45 minutes, so ask: *"Which of these would you like me to go deeper on: delta updates, the rollback mechanism, rollout pacing, or the offline-first agent design?"*

### 6.1 Delta (differential) updates

- Precompute deltas for the most common upgrade paths (current version → N latest versions) at build/release time using a binary-diff algorithm (e.g., bsdiff-style courgette/binary patching), rather than computing on-demand per vehicle — this trades storage (a handful of extra delta artifacts per release) for massively reduced compute-per-request and predictable, cacheable CDN behavior.
- If a vehicle's current version has no precomputed delta path (e.g., it's many versions behind, or was never seen before), fall back to a full image download — slower, but correct. Track this fallback rate; a high fallback rate signals the fleet is fragmenting into too many long-tail versions and mandatory update policies may be needed.
- Delta application must be verified before it's trusted: after applying the diff, checksum the *resulting* image against the expected `Package.checksum_sha256` before flashing — never trust the diff algorithm blindly.

### 6.2 A/B (dual-partition) update and fail-secure rollback

- The vehicle's storage has two partitions, A and B (or "slot 0 / slot 1"). At any time, one is **active** (currently booted) and one is **inactive**.
- The update is downloaded and flashed entirely to the *inactive* partition while the vehicle continues running normally from the active one — this means a failed or interrupted download/flash never touches the running system.
- After flashing, the bootloader marks the inactive partition as the "next boot candidate" and reboots.
- On boot, a watchdog/health-check runs (e.g., can the OS reach a basic liveness milestone, do critical ECUs respond). If the health check fails within a bounded window (or the vehicle detects a boot-loop), the bootloader automatically falls back to the previous known-good partition — **fail-secure by construction, not by best-effort software logic**.
- Only after a successful boot and a "soak period" (e.g., N minutes of nominal operation) does the backend mark that vehicle's update as `SUCCESS`; the *previous* partition remains available as the fallback for at least one more cycle before being reclaimed for the next update.

*Trade-off to mention:* dual-partition doubles the flash storage requirement for updatable components — an explicit cost the hardware team must provision for, but it's the industry-standard (and effectively non-negotiable) approach for safety-critical automotive OTA (this is essentially how Android A/B seamless updates and most automotive OTA stacks work).

### 6.3 Staged / canary rollout

- **Ring 0 (internal fleet / dogfood):** a small set of company-owned test vehicles.
- **Ring 1 (canary, ~0.1-1%):** randomly sampled real customer vehicles across diverse hardware revisions and regions.
- **Ring 2..N (progressive rings):** e.g., 5% → 20% → 50% → 100%, each gated on the previous ring's success-rate and telemetry health staying within threshold for a soak period (e.g., 24-48 hours) before advancing.
- Cohort selection should stratify by hardware revision, region (climate/network conditions vary), and software history — a naive random sample can miss a bug that only manifests on one hardware revision.
- The orchestrator automatically halts advancement (and pages an on-call engineer) if the failure rate, crash-rate, or a defined "canary metric" (e.g., battery-management anomaly count) exceeds a threshold relative to the pre-update baseline — this should be automatic, not dependent on a human noticing a dashboard.

### 6.4 Offline-first vehicle agent (state machine)

The agent must make correct decisions with zero backend connectivity for arbitrarily long periods.

```
IDLE → DOWNLOAD_PENDING → DOWNLOADING ⇄ (paused by connectivity loss) → DOWNLOADED
     → VERIFYING → STAGED → (await user consent / scheduled window, if optional)
     → APPLYING → REBOOTING → (health check) → SUCCESS
                                            └─(fail)→ ROLLED_BACK
```

- **Resumable, chunked download with checkpointing:** the agent persists `download_offset_bytes` locally; on reconnect (even to a different network — cellular this time instead of Wi-Fi), it resumes from the last checkpoint using HTTP range requests, rather than restarting from zero.
- **Store-and-forward for status:** state transitions are appended to a local durable queue and flushed to the backend opportunistically whenever connectivity is available; the backend treats status reports as eventually-consistent, not real-time-guaranteed.
- **Local policy for "when to actually apply":** even after a download completes, safety-critical components should only apply/reboot when the vehicle is confirmed parked, in park gear, and (for larger updates) plugged in/charging, to avoid interrupting a drive — this logic must live on the vehicle since connectivity to consult the backend can't be assumed at the exact right moment.
- **Idempotency:** because the backend may re-send a "you have an update available" notification after a connectivity gap (not knowing whether the vehicle already received it), the agent must treat notifications idempotently, keyed by `campaign_id` + `target_version`.

### 6.5 Rollout pacing / avoiding thundering herd

- The orchestrator doesn't broadcast "update available" to an entire ring simultaneously; it drips notifications at a controlled rate (e.g., N vehicles/minute), using jittered scheduling so vehicles don't all hit the CDN in the same second.
- Vehicles that are asleep/offline when notified will pick up the pending campaign the next time they check in (poll or reconnect), naturally smoothing bursts further.
- CDN + object storage absorb the actual byte-serving load; the control plane only needs to handle lightweight manifest requests and status pings, which is orders of magnitude lower throughput than the raw egress.

---

## 7. Minimal API Surface (illustrative)

```
# Vehicle-facing (via the Comm Gateway)
GET  /v1/vehicles/{vehicle_id}/pending-updates
     → returns any assigned campaign + manifest (component, target_version,
       delta_or_full_url signed for short-lived CDN access, checksum, signature)

POST /v1/vehicles/{vehicle_id}/update-status
     → { component_id, campaign_id, state, offset_bytes, error_code?, timestamp }
     (idempotent; safe to retry/replay after reconnect)

# Operator-facing (Campaign Orchestrator console)
POST /v1/campaigns                  → create a campaign (cohort, strategy, priority)
POST /v1/campaigns/{id}/pause
POST /v1/campaigns/{id}/halt
GET  /v1/campaigns/{id}/status      → aggregated counts per state, per ring
```

---

## 8. Trade-offs and Alternatives Considered

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| Update transport | Delta/differential packages | Always ship full images | Full images are simpler but 5-10x more egress cost and cellular data usage at fleet scale; worth the added build-pipeline complexity. |
| Partition scheme | Dual A/B partitions | Single partition + backup/restore script | A/B gives fail-secure rollback essentially "for free" at boot time; a software-only backup/restore is more fragile against power loss mid-write. |
| Rollout control | Progressive rings with automatic halt on anomaly | Push to 100% immediately | Slower time-to-full-deployment, but catches hardware-revision-specific or region-specific bugs before they hit the whole fleet — non-negotiable for safety-critical software. |
| Vehicle connectivity model | Offline-first, store-and-forward, eventually consistent | Require an active connection to perform any update step | A synchronous model would strand vehicles in dead zones indefinitely; offline-first is mandatory given the stated core constraint. |
| Hot state vs. audit log | Two separate stores (device-shadow vs. append-only event log) | One unified table for both | Keeps the frequently-updated hot path fast and small while letting the audit log scale independently and use storage optimized for time-range analytics. |
| Delta computation | Precomputed at release time for common upgrade paths | Computed on-demand per request | Predictable CDN cache behavior and no compute spike during a big rollout, at the cost of some storage for less-common upgrade paths (mitigated by full-image fallback). |

---

## 9. Failure Modes & Edge Cases to Call Out Proactively

- **Power loss mid-flash:** mitigated entirely by A/B partitioning — the active partition is untouched until the new one boots successfully.
- **Corrupted download (bit flips over cellular):** checksum verification before flashing catches this; the agent re-requests only the corrupted chunk range if the transport supports range validation, or the whole delta if not.
- **Vehicle stuck offline indefinitely:** campaigns don't "expire" the vehicle's eligibility; it simply resumes the next time it reconnects. For mandatory security patches with a hard deadline (e.g., a recall), define an escalation path (e.g., dealer service visit) for vehicles that fail to check in within a defined window.
- **Two campaigns targeting the same component overlap:** the orchestrator should reject/queue overlapping campaigns per component — a vehicle should never be told to install two different target versions of the same component concurrently.
- **Rollback itself fails (both partitions unhealthy):** this is the true worst case — mitigate via a minimal, extremely stable, rarely-updated "recovery/bootstrap" partition that's separate from the A/B application partitions and can always restore a known-safe baseline; this is analogous to a phone's recovery mode.
- **Malicious or spoofed update:** signature verification against a hardware-backed root of trust prevents installing unsigned or tampered packages; also guard against downgrade attacks (replaying an old, vulnerable signed version) via a monotonic version/counter check.
- **Metric-based auto-halt false positives:** an anomaly detector that's too sensitive could halt a legitimate rollout on noise; mitigate with a statistically-sound baseline comparison (e.g., compare against a control group not yet updated) rather than a naive fixed threshold.

---

## 10. Monitoring, Observability, and Security (brief)

- **Dashboards:** rollout funnel per campaign (assigned → downloading → applied → succeeded/failed), broken down by ring, region, and hardware revision.
- **Alerting:** automatic page when a ring's failure rate or a canary health metric deviates from the pre-rollout baseline beyond a statistical threshold.
- **Audit/compliance:** the append-only `UpdateEvent` log plus operator action log (who created/paused/halted a campaign) supports post-incident investigation and regulatory audit (relevant for safety-critical automotive software).
- **Security:** signed manifests and packages verified against a hardware root of trust; short-lived signed CDN URLs (prevent hot-linking/leaking artifacts); TLS/mutual-TLS for the vehicle-gateway channel; anti-downgrade/anti-replay version checks.

---

## 11. Wrap-up / How to Close the Interview

Summarize in 30 seconds: *"To recap: we separated the control plane (campaign orchestration, lightweight manifests, status) from the data plane (CDN-backed byte delivery), used dual-partition A/B updates for fail-secure rollback, delta packages to control bandwidth cost, progressive ring-based rollouts with automatic anomaly-based halting for safety, and an offline-first vehicle agent with resumable downloads and store-and-forward status reporting to handle intermittent connectivity — which was the core constraint throughout."*

Then proactively offer a couple of extension directions, showing you know where the design could go next:
- How would this change for a *safety-critical, real-time* ECU (e.g., steer-by-wire) versus infotainment — stricter functional-safety gating (ISO 26262), possibly requiring dealer/service-center confirmation rather than fully remote OTA?
- How would you extend this to support *partial/modular* updates (updating only a subset of an ECU's software components) versus whole-image updates?
- How would you evolve rollout targeting from static cohort rules to a more adaptive system (e.g., ML-based anomaly detection instead of fixed thresholds)?

---

## 12. Follow-up Questions Interviewers May Ask

- "How do you compute a delta between two arbitrary firmware versions efficiently, and what happens if no precomputed delta path exists for a very old vehicle?"
- "Walk me through exactly what happens if the vehicle loses power at the millisecond it's writing the last block of the inactive partition."
- "How would you detect that a rollout is causing a subtle issue that doesn't show up as a hard failure — e.g., increased battery drain — rather than an outright crash?"
- "How do you prevent a compromised backend from being used to push a malicious update to the fleet (defense in depth beyond just code signing)?"
- "How would the design change if a large fraction of the fleet has no cellular modem and relies purely on opportunistic Wi-Fi (e.g., at home)?"
- "How do you handle a scenario where a vehicle is sold/transferred and its identity/ownership context changes mid-campaign?"
- "What's your strategy for very large fleets (tens of millions of vehicles) where a single rollout could take weeks — how do you avoid maintaining too many supported versions simultaneously (version fragmentation)?"

---

## References

- Rivian system design round context: see [`../rivian/index.md`](../rivian/index.md), section "System Design Interview Questions."
- Conceptually similar to Android's A/B (seamless) system updates and Tesla/most automotive OTA architectures — dual-partition, delta-based, staged rollout is the de facto industry pattern for safety-critical fleet software updates.
