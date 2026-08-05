# System Design Mock Interview: Fail-Secure OTA Rollback Architecture (Safety Deep-Dive Variant)

**Company theme:** Rivian-style (vehicle/EV), also broadly applicable to Tesla, Ford, Waymo, or any connected-fleet company shipping embedded firmware to safety-relevant ECUs.
**Round:** System Design (45-60 min onsite loop) — Safety/functional-safety-leaning variant.
**Interviewer expectation:** Precise, mechanism-level reasoning about atomicity, boot-time verification, and failure recovery — not a broad system tour. The interviewer wants to hear you reason like someone who has actually thought about what happens at the exact millisecond power is lost.

> **This is a deep-dive variant, not a standalone system.** The general OTA distribution/rollout system (campaigns, delta packages, staged rollouts, the offline-first vehicle agent) is covered in [`./ota-update-system-for-connected-vehicle-fleet.md`](./ota-update-system-for-connected-vehicle-fleet.md) ("Document #1"). That document covers the A/B dual-partition rollback mechanism in about one paragraph (section 6.2) — enough to show you know the pattern exists, but not enough to survive a follow-up round where the interviewer asks "walk me through exactly what the watchdog checks and how many seconds it has to check it." **This document owns that follow-up.** We assume the distribution/campaign/delta machinery from Document #1 already exists and has successfully delivered bytes to the inactive partition; our scope starts the instant the bootloader is asked to boot into a newly-flashed image and ends when that version is either durably committed or durably reverted.

This document is written as a self-contained interview walkthrough: clarifying questions, a model answer per section, and likely follow-up probes.

---

## 0. Opening: Clarify the Problem (first 3-5 minutes)

> **You:** "This sounds like a narrower, deeper version of a rollback mechanism I've designed before at the fleet-distribution level — dual partitions, canary rings, a backend halting a bad rollout. Should I assume all of that exists and focus purely on the *guarantee mechanism* — what makes a single vehicle's rollback provably safe, independent of anything the backend does — or do you want the full distribution story again?"
>
> **Interviewer:** "Correct, assume delta packages have already been downloaded, verified, and fully written to the inactive partition. I want to know exactly how you guarantee that if the update is interrupted at any point — power loss mid-flash, a crash during first boot, a subtle firmware bug that only shows up after boot — the vehicle recovers to a safe, functioning state without any human intervention. And I specifically want you to address how this differs for an infotainment head unit versus a steer-by-wire or braking ECU."
>
> **You:** "A few more questions:
> 1. Are we designing one universal mechanism for all ECUs, or should the design explicitly branch by criticality?
> 2. Can we assume a hardware bootloader with basic verification capability (e.g., checking a boot flag, running a hash check), or is this a software-only mechanism running under a generic OS?
> 3. Should I address ISO 26262 / ASIL concepts explicitly, or keep this generic functional-safety reasoning?
> 4. Is 'interrupted' limited to power loss during the flash, or does it also include 'the update applied cleanly but the new firmware has a latent bug that only manifests after some driving'?
> 5. Do we need to handle the worst case — both partitions unusable — or is that out of scope?"

Assume the interviewer answers:
- Design one core mechanism, then explicitly branch where safety criticality demands more.
- Assume a minimal, trusted hardware/first-stage bootloader exists (this is realistic and standard for automotive ECUs — a small immutable first-stage loader is nearly universal).
- Yes, explicitly reason about ASIL and ISO 26262 concepts for the safety-critical branch.
- "Interrupted" covers both: a hard interruption (power loss, crash during boot) and a soft interruption (boots fine, but a latent defect surfaces after the vehicle has been driving for a while) — both need a rollback path, on different timescales.
- Yes, the both-partitions-corrupt worst case is explicitly in scope and should be treated seriously, not hand-waved.

---

## 1. Functional Requirements

1. **Atomic apply** — from the perspective of the next boot, an update is either fully applied or not applied at all; there is no partially-applied, ambiguous state that the system can boot into.
2. **Automatic, unattended fallback** — a failed update must trigger a fallback to the last-known-good version without requiring connectivity, a backend round-trip, or human action (dealer visit, service tool). The vehicle must be able to save itself while parked in a garage with zero signal.
3. **Bounded fallback latency** — the decision to fall back must happen within a defined, small time budget after a failed boot attempt, not "eventually."
4. **Boot-loop detection** — repeated failed boot attempts on the new version must be detected and treated as a permanent failure, not retried indefinitely (which would itself be a hazard — e.g., cycling actuators or power states repeatedly).
5. **Deferred commit ("soak period")** — a new version is only permanently accepted (and the old version's storage reclaimed) after it has demonstrated sustained nominal operation, not merely "it booted."
6. **Differentiated guarantees by criticality** — an infotainment ECU and a steer-by-wire ECU cannot share the exact same risk tolerance; the mechanism must have a per-component criticality tier with correspondingly stricter gates for higher tiers.
7. **True last-resort recovery** — even if both application-facing partitions are unusable (corrupted, unbootable, or both fail health checks), the vehicle must have a path back to a functioning, safe state that does not depend on network connectivity.
8. **Degraded-but-safe operating modes** — for safety-critical actuation ECUs, a failed or reverted update should be able to leave the vehicle in a restricted-but-safe operating mode (e.g., speed-limited, reduced steering assist with mechanical backup engaged) rather than a binary "works / totally dead" outcome.
9. **Tamper/verification at every boot, not just at flash time** — the bootloader re-verifies the signature/integrity of whichever partition it's about to boot, every boot, not only immediately after flashing — this catches corruption introduced after a successful flash (e.g., bit rot, a later unrelated fault).

**Out of scope (state this explicitly):** how the update bytes get to the vehicle (delta generation, CDN, campaign pacing, canary rings — all Document #1), and how the artifact was built and signed upstream (Document #9, [`./secure-automated-ota-deployment-pipeline.md`](./secure-automated-ota-deployment-pipeline.md)). We assume a correctly signed, correctly downloaded image sitting in the inactive partition, and focus entirely on what happens from that point through commit or rollback.

---

## 2. Non-Functional Requirements

| Requirement | Target / Reasoning |
|---|---|
| **Safety (primary NFR)** | Zero scenarios where an interrupted or failed update leaves a safety-critical ECU in an undefined or hazardous state. This dominates every other requirement in this document. |
| **Fallback latency** | Detect a failed boot and complete fallback within a single boot cycle — target under 30-60 seconds from power-on to either "healthy and running" or "reverted and running the old version," so a driver who unlocks the vehicle doesn't sit at a dead dashboard. |
| **Boot-loop threshold** | No more than 2-3 failed boot attempts on a new version before automatic, permanent fallback — bounded precisely so the mechanism itself never becomes a hazard (e.g., repeatedly cycling high-voltage contactors or actuator init sequences). |
| **Independence from connectivity** | The entire detect-and-fallback path must work with zero network connectivity — this is a stricter version of Document #1's "offline-first" requirement, since here even a backend round-trip of a few seconds is disqualifying. |
| **Independence from correct software** | The mechanism that *decides* to roll back must not depend on the correctness of the software it might be rolling back away from — i.e., the watchdog/fallback logic must live at a lower trust layer (bootloader/hardware) than the application software it supervises. |
| **Soak period duration** | Long enough to catch defects that only manifest under real operating conditions (thermal cycling, a full drive cycle, sustained load), short enough that storage isn't tied up indefinitely — target on the order of one full ignition-on/drive/ignition-off cycle, or a bounded time window, whichever comes first (detailed in section 6.4). |
| **Criticality-tiered rigor** | Higher-ASIL components must have strictly stricter gates (more redundant checks, longer soak, more conservative auto-revert triggers) than lower-ASIL ones — the mechanism should not be "one size fits all." |
| **Auditability** | Every state transition (attempt, health-check pass/fail, commit, rollback, boot-loop-triggered fallback) is logged locally (surviving power loss) and eventually reported to the backend for fleet-wide visibility and regulatory audit. |
| **Storage overhead** | Dual-partition (2x storage for updatable regions) is an accepted, budgeted cost — call this out as a known, non-negotiable trade-off rather than something to optimize away. |

Call out explicitly to the interviewer: *"Every mechanism I describe from here has to satisfy one property above all: it must fail toward safety even if every layer of software above it is broken. That's why the core decision logic keeps moving down the stack — from application, to OS, to bootloader, to hardware-latched state — as the consequences of getting it wrong get more severe."*

---

## 3. Back-of-the-Envelope Timing & Threshold Budget

This section replaces the fleet-capacity estimation from Document #1 — the relevant "capacity" here is a timing and threshold budget, not throughput.

- **Boot-time health check budget:** a typical automotive ECU boot-to-application-ready time is roughly 2-8 seconds depending on component (infotainment head units, with a full OS, trend toward the higher end; a smaller RTOS-based ECU like steer-by-wire trends toward the lower end). Budget the health check itself to complete within **an additional 3-5 seconds** after the application reports "up" — long enough to run a meaningful self-test suite, short enough that a driver isn't staring at a non-responsive dashboard or a car that won't shift out of park. Total: target **under ~10-15 seconds from power-on to a pass/fail health verdict** for most ECUs, tighter (closer to 2-3 seconds) for the safety-critical actuation path specifically, since a vehicle that's already moving (waking from a low-power state) cannot tolerate a 15-second ambiguity window on steering availability.
- **Boot-loop counter threshold:** set at **3 consecutive failed attempts**. Reasoning: 1 attempt doesn't distinguish a transient fault (e.g., a sensor not yet warmed up, a one-off timing glitch) from a real defect — you'd cause unnecessary rollbacks. 2 attempts is defensible but still has a meaningful false-positive rate for genuinely transient conditions. By 3 consecutive failures, the odds that this is a transient environmental fluke rather than a real defect in the new image drop enough to justify committing to fallback — and 3 attempts still only costs roughly 3 × 15 seconds ≈ 45 seconds of total delay in the worst case before the vehicle is usable again on the old version, which is an acceptable one-time cost.
- **Soak period duration:** target **one full drive cycle, capped at 24-48 hours of elapsed time, whichever comes first**. Reasoning: many defects (thermal-related sensor drift, a memory leak, a race condition under sustained CAN bus load) only manifest after the ECU has been running under real load for tens of minutes to hours — a health check performed only at boot cannot catch these. A full drive cycle (ignition on, driving, ignition off) is a reasonable proxy for "the vehicle was actually used under real conditions." Capping at 24-48 hours prevents an edge case where a vehicle sits in a garage for a week without being driven from indefinitely delaying commit and tying up the fallback partition's storage.
- **Recovery-partition update frequency:** by design, near-zero — target **fewer than 1-2 updates per year**, each requiring a substantially higher review bar than a routine application update (detailed in section 6.6). This is a deliberate near-zero number, not a throughput target to optimize.
- **Persistent counter write overhead:** the boot-attempt counter itself must be written to non-volatile storage before every boot attempt — this is a tiny write (a few bytes) but must use a storage technology and write pattern that's itself power-loss-safe (e.g., a dedicated small region of EEPROM/eFuse-backed storage or a redundant, checksummed pair of flash blocks) — budget this as effectively free from a capacity standpoint, but non-negotiable from a correctness standpoint, since a counter that can be corrupted or fail to persist defeats the entire boot-loop-detection mechanism.

Conclusion to state out loud: *"Unlike Document #1, where the interesting numbers were bandwidth and fleet size, the interesting numbers here are all timing windows and attempt thresholds — and every one of them is a genuine safety-vs-availability trade-off: too aggressive a threshold causes unnecessary rollbacks on transient faults, too lenient a threshold leaves a vehicle stuck on bad firmware for too long or repeatedly attempting a dangerous boot sequence."*

---

## 4. Data Model / State-Machine & Transaction-Log Design

Rather than application-level entities (campaigns, packages), the data model here is the **on-vehicle persistent state** that makes rollback possible even when nothing else in the system can be trusted.

### `BootAttemptRecord` (persisted in power-loss-safe non-volatile storage, NOT in the partition being booted)

```
active_slot            -- which partition (A/B) is currently marked bootable
candidate_slot         -- the partition the bootloader is about to try (nullable if none pending)
attempt_count           -- consecutive failed attempts on candidate_slot since it was staged
last_attempt_result     -- NONE / PENDING / PASS / FAIL
committed_version_hash  -- hash of the last version that completed a full soak period
```

This record must be written **before** each boot attempt (attempt_count incremented) and updated only **after** a health-check verdict is known — never the other way around. This ordering is the crux of boot-loop detection: if the counter were only incremented *after* a successful boot, a hard crash mid-boot (before the counter update) would never register as an attempt, and the vehicle could loop forever. Incrementing before the attempt guarantees every real boot attempt is counted even if the boot itself never completes.

### `SoakState` (tracks progress toward permanent commit)

```
candidate_version
soak_started_at
drive_cycles_completed
elapsed_time_in_soak
critical_dtc_count_during_soak   -- Diagnostic Trouble Codes logged while on the candidate version
soak_status                        -- IN_PROGRESS / PASSED / FAILED
```

A candidate only transitions to `PASSED` when `drive_cycles_completed >= 1 AND critical_dtc_count_during_soak == 0`, bounded by the 24-48 hour cap from section 3. On `PASSED`, the previous partition is unlocked for reuse as the new inactive slot. On `FAILED` (a critical DTC logged during soak, even after a successful boot), the system triggers the same rollback path as a boot-time failure — this is the "soft interruption" case from the opening dialogue: the update looked fine at boot but revealed a defect once driven.

### `HealthCheckLog` (append-only, local-first — the transaction log of every boot attempt)

```
log_id (PK, monotonic)
slot_attempted
attempt_count_at_time
timestamp
checks_run (JSON)          -- which checks executed and their individual pass/fail
verdict                     -- PASS / FAIL / TIMEOUT
action_taken                 -- COMMIT / RETRY / FALLBACK / RECOVERY_MODE
```

This is a local analogue of Document #1's `UpdateEvent` audit log, but with one critical difference: **it must be readable and useful even if the vehicle never reconnects to the backend again.** A technician plugged into the vehicle locally (dealer diagnostic tool) must be able to read this log directly off the ECU to understand exactly what happened, since the whole point of this mechanism is to function correctly with zero connectivity.

### Why keep the boot-attempt counter physically separate from the partitions it's counting?

This is worth narrating explicitly: *"If the boot-attempt counter lived inside partition A or B, a corrupted partition could corrupt its own counter, or a rollback that wipes/reflashes a partition could accidentally reset the very counter meant to detect repeated failures on it. The counter has to live in storage that survives independently of both partitions and is only ever touched by the bootloader — the lowest, most-trusted layer in the system — never by application software."*

---

## 5. High-Level Design

This is an **infrastructure/topology view** — what pieces of infrastructure exist on the vehicle, what type each one is (immutable root-of-trust code, power-loss-safe persistent store, continuously-running monitor, structurally-isolated last-resort partition...), and how they're wired together — not a step-by-step trace of one boot attempt. Sequencing and per-hop logic belong in the Deep Dives (§6); this section should stand on its own as "here's what we'd provision on every ECU."

### Infrastructure tiers

**Root-of-trust tier (immutable, the lowest layer — trusted independent of any software above it)**
- **First-stage (immutable) bootloader** — a small, rarely-changed piece of code (ideally masked ROM or write-protected after manufacturing) that reads the boot-attempt counter, decides which partition to boot, increments the counter, and hands off control. This is the root of trust for the entire mechanism.
- **Boot-attempt counter store (`BootAttemptRecord`)** — a small, power-loss-safe region of non-volatile storage, physically separate from both A/B partitions and touched only by the bootloader; this separation is deliberate infrastructure, not an implementation detail — a corrupted partition can never corrupt the counter meant to detect its own repeated failures.

**Boot control tier**
- **Second-stage bootloader / boot manager** — re-verifies the signature/hash of the target partition at every boot (not just at flash time) and enforces the boot-loop threshold.
- **Boot-time health-check / watchdog service** — runs immediately after the application layer signals "up," executes the self-test suite, and reports pass/fail within the timing budget from section 3.

**Runtime supervision tier**
- **Runtime soak monitor** — runs continuously, not just at boot, after a candidate version has passed its initial health check; watches for critical DTCs and tracks drive-cycle completion toward permanent commit.

**Storage / partition tier**
- **Partition manager** — owns the actual A/B slots; exposes "stage an update to the inactive slot," "mark a slot bootable," and "reclaim a slot for reuse"; the only component allowed to write to flash outside of active application updates.
- **Recovery/bootstrap partition** — a minimal, essentially-never-touched third image, structurally isolated from the routine A/B write path, that can restore a known-safe baseline if both A and B are ever simultaneously unusable.

**Safety-response tier (safety-critical ECUs only)**
- **Degraded-mode controller** — on persistent fallback failure, decides whether the vehicle can safely operate in a restricted mode (e.g., mechanical backup engaged, speed-limited) versus requiring the vehicle to remain immobilized until serviced.

**Supporting / cross-cutting infrastructure (off-vehicle, beside this per-vehicle mechanism, not a dependency of it)**
- Document #1's fleet-side campaign-halt / canary anomaly-detection reacts to the aggregate of many vehicles' rollback events reported by this mechanism (section 10), forming a population-level safety net on top of it — but this per-vehicle mechanism must function correctly with zero connectivity to that backend, ever.

### Topology diagram (infrastructure view, described in ASCII)

```
                          ROOT-OF-TRUST TIER
              ┌─────────────────────────┐        ┌──────────────────────────┐
              │ First-Stage Bootloader   │◄──────►│ Boot-Attempt Counter      │
              │ (immutable, masked ROM)   │        │ Store (separate NV mem,   │
              └────────────┬─────────────┘        │  power-loss-safe)         │
                            │ hand off, counter incremented first  └──────────────────────────┘
                            ▼
                   BOOT CONTROL TIER
              ┌─────────────────────────┐
              │ Second-Stage Boot Mgr     │  verify sig/hash, enforce boot-loop threshold
              └────────────┬─────────────┘
             under threshold│                  over threshold
                            ▼                          \
              ┌─────────────────────────┐                \
              │ Boot-Time Health-Check    │──FAIL/TIMEOUT──► FALLBACK: flip active_slot,
              │ / Watchdog Service         │                  reboot into other partition
              └────────────┬─────────────┘                 /
                       PASS │                              /
                            ▼                             /
                 RUNTIME SUPERVISION TIER                /
              ┌─────────────────────────┐               /
              │ Runtime Soak Monitor       │──critical DTC──┘
              │ (drive cycle, DTC watch)   │
              └────────────┬─────────────┘
                  soak PASSED
                            ▼
                 STORAGE / PARTITION TIER
              ┌─────────────────────────┐
              │ Partition Manager          │  commit: reclaim old slot, reset counter
              │ (owns A/B slots)           │
              └─────────────────────────┘

    WORST CASE — both A and B unusable ─────────────────────────────────►
              ┌─────────────────────────┐        ┌────────────────────────────┐
              │ Recovery/Bootstrap         │───────►│ Degraded-Mode Controller     │
              │ Partition (last resort,     │        │ (safety-critical ECUs only)  │
              │  structurally isolated)     │        └────────────────────────────┘
              └─────────────────────────┘

 SUPPORTING (off-vehicle, beside this mechanism, never a dependency of it):
   • Document #1 campaign-halt / canary anomaly-detection — reacts to the fleet-wide
     aggregate of rollback events this mechanism reports; not something this mechanism reads from.
```

Narrate the key architectural decision: *"The whole mechanism is organized as a chain of increasingly-trusted layers, with the trust boundary drawn explicitly: the root-of-trust tier (bootloader + counter store) is the only infrastructure the design assumes cannot itself be broken by a bad update, because it sits below and physically separate from every partition it's judging. Everything above it — the boot manager, the watchdog, the soak monitor, the partition manager — is composed around that root rather than the other way around. The recovery partition is structurally isolated infrastructure, not just a policy that says 'don't touch it' — it's unreachable by the routine A/B write path by construction. And the fleet-side backend that reacts to rollback telemetry is drawn off to the side deliberately: it's a population-level side-car this per-vehicle mechanism reports to, never something it depends on to function."*

---

## 6. Detailed Design / Deep Dives

This is where the bulk of an interview on this topic should go. Ask the interviewer which to prioritize: *"Should I go deepest on atomicity semantics at the storage layer, the health-check/watchdog design, the boot-loop math, the soak period, or the safety-critical-vs-infotainment split?"*

### 6.1 What "atomic apply" actually means at the flash-write level

"Atomic" here does not mean a single instruction — it means **the next boot decision is always well-defined**, no matter when power is lost during the write. Concretely:

- The update is written entirely to the **inactive** partition while the active partition continues serving the running system untouched. This is the first and most important atomicity property: a partial or corrupted write to the inactive partition, by construction, cannot affect what's currently running, because the CPU is executing from a completely different physical region of flash.
- Write ordering matters enormously. The bootloader must never observe "partition B has new data" until *all* of partition B's data (including any embedded checksums) has been durably written. This requires a storage-layer **write barrier / fsync-equivalent**: data blocks are flushed and confirmed committed to physical flash *before* the single small "boot flag" or "slot valid" marker is written that tells the bootloader "B is now a legitimate boot candidate." If the marker could be written (or reordered by a write-back cache to appear written) before the data itself is durable, a power loss in that narrow window would leave the bootloader trusting a partition that's actually incomplete — this is precisely the class of bug that fsync/write-barrier semantics exist to prevent.
- Practically, this means: write all data blocks → issue a flush/barrier to guarantee those blocks are physically committed → compute and write a checksum/hash covering the whole partition → issue a second flush/barrier → only then flip the single "candidate slot" marker, which itself should be a single atomic sector write (many flash technologies guarantee atomicity for a single small aligned write, which is exactly why the "is this slot valid" state should be reduced to the smallest possible marker rather than inferred from partial partition contents).
- **The marker write itself is the true atomicity boundary.** Everything before it can be interrupted arbitrarily and safely retried (the inactive partition just gets re-flashed from scratch or resumed, per Document #1's resumable-download logic). Only the marker flip is the single moment that must be indivisible — and by using a small, aligned, single-sector write for that marker, we push the atomicity requirement down to something the underlying flash hardware can actually guarantee, rather than trying to make an entire multi-hundred-megabyte write atomic (which no realistic storage layer can do directly).
- Say this explicitly to the interviewer: *"The trick to atomicity at scale isn't making a huge write atomic — it's decomposing the problem so that the only thing that needs to be atomic is one tiny marker flip, and everything upstream of that marker is idempotent and safely retryable."*

### 6.2 Boot-time health-check / watchdog design

The watchdog is not a single check — it's a layered suite, each layer catching a different failure class, and it must complete inside the timing budget from section 3.

1. **Process/task liveness heartbeats (sub-second to ~1-2 seconds):** every critical process or RTOS task registers a heartbeat with the watchdog on startup and periodically thereafter. If any expected critical process fails to heartbeat within its expected window, that's an immediate fail — this catches crashes, hangs, and deadlocks in the new software, the cheapest and fastest class of check.
2. **CAN bus responsiveness from dependent/critical ECUs (~1-3 seconds):** the ECU that just booted issues a defined diagnostic or status request to the other ECUs it depends on or coordinates with (e.g., steer-by-wire checking in with the steering angle sensor module and the EPS motor controller) and confirms responses within an expected latency window. This catches integration failures — the new firmware might boot fine in isolation but have broken a message format or timing assumption that the rest of the vehicle's network depends on.
3. **Self-test suite covering critical subsystems (~2-5 seconds):** a defined battery of built-in tests — e.g., for steer-by-wire, confirming the redundant angle sensors agree within tolerance, confirming the motor controller responds to a small, safe test actuation command, confirming the mechanical/hydraulic fallback path (if present) is mechanically engaged/disengaged as expected. For infotainment, this might be far lighter — confirming the display driver initializes and a known test pattern renders, confirming audio subsystem init succeeds.
4. **Aggregate verdict with a hard timeout:** if all layers pass within budget, verdict is `PASS`. If any layer fails, or if the *entire suite* doesn't produce a verdict within the timeout budget (a hang during the health check itself must not be able to leave the system in limbo forever), the verdict is `FAIL` — a timeout is treated identically to an explicit failure, never as "assume it's fine and keep waiting."

State the reasoning explicitly: *"The layering matters because each layer is cheap-and-fast-but-shallow versus expensive-and-slow-but-deep. Running liveness checks first lets us fail fast and cheaply on the most common failure mode — an outright crash — without spending the full timeout budget. We only pay for the deeper self-test suite when the cheap checks already passed."*

### 6.3 Boot-loop counting and fallback-trigger threshold logic

The exact sequence, restated precisely (this is the part interviewers most often probe on):

1. Before attempting to boot `candidate_slot`, the bootloader reads `BootAttemptRecord.attempt_count`, increments it, and **durably persists the increment before jumping to the candidate partition's code.** This ordering is the whole trick: if the increment happened after boot (e.g., as part of the application's own startup sequence), a crash early enough in boot would never be counted, and a bad image that always crashes before reaching that point could loop forever without ever tripping the threshold.
2. The candidate boots and runs the health-check suite from 6.2.
3. **On PASS:** `attempt_count` is reset to 0, and (if this is the first pass for this version) `SoakState` is initialized to begin the soak period. The reset must also be durably persisted — otherwise a *later*, unrelated failure years down the line could inherit a stale nonzero count and trip the threshold prematurely.
4. **On FAIL or TIMEOUT:** the bootloader checks `attempt_count` against the threshold (3, per section 3). If under threshold, it reboots and retries the same candidate slot — this handles genuinely transient faults (a sensor that hadn't finished initializing, a one-off timing hiccup) without unnecessarily discarding a perfectly good update.
5. **On reaching the threshold:** the bootloader marks `candidate_slot` as permanently disqualified (not just "try again"), flips `active_slot` to the other partition, resets the counter for a fresh boot attempt on that partition, and reboots. This is the automatic fallback — no backend call, no human action.
6. Note the asymmetry deliberately: **the counter only ever needs to reach the threshold on the *new* candidate.** The previously-committed, already-soaked partition is assumed trustworthy (it passed its own soak period when it was new) and does not re-run the same threshold logic during a routine boot — it only becomes a "candidate" again if it's the fallback target after the new version fails, at which point it gets a much shorter, lighter-weight verification (it already proved itself; we're mainly re-confirming it hasn't been corrupted since).

### 6.4 The soak period, precisely

A health check that only runs at boot cannot catch defects that need real operating time to surface — thermal drift, memory leaks, race conditions under sustained bus load, a control-loop instability that only appears at highway speed. The soak period exists specifically to close this gap.

What it measures, concretely:
- **A bounded window of nominal operation** — no unexpected resets, no watchdog-triggered reboots, no unhandled exceptions logged, for the duration of the soak.
- **Absence of critical DTCs** — Diagnostic Trouble Codes are the standard automotive mechanism for "something in this ECU or its interactions detected an abnormal condition." Any DTC classified as safety-relevant or critical logged during the soak window immediately fails the soak, even if the vehicle otherwise appears to be running fine — the DTC subsystem is specifically designed to catch problems that a simple "is it still running" check would miss.
- **Successful completion of at least one full drive cycle** — ignition on, the vehicle actually driven (not just idling), ignition off — because many real-world failure modes (thermal cycling, vibration-induced connector issues, sustained-load behavior) simply don't occur while parked with the engine off.
- **A time cap** (24-48 hours, from section 3) so a vehicle that's rarely driven doesn't hold the old partition hostage indefinitely — after the cap, if no critical DTC has fired, the system commits even if a full "drive cycle" hasn't technically completed, since holding storage in a permanently uncommitted state is itself an operational cost.

Only on soak `PASSED` does the partition manager reclaim the old (previously-active) slot as reusable storage for the *next* future update's inactive-slot staging. This ordering matters: reclaiming the old slot early (right after a health-check pass, without waiting for soak) would mean a defect discovered mid-soak has nowhere to fall back to — you'd have already destroyed your only safety net.

### 6.5 Differentiating infotainment versus safety-critical ECUs

The mechanism described so far (A/B partitions, boot-time health check, boot-loop counting, soak period) is the **shared baseline** — every updatable ECU gets it. The difference is in what happens **beyond** that baseline, and how conservatively the thresholds are set.

**Infotainment / merely-inconvenient ECUs:**
- A failed update means: reboot into the old, still-fully-functional version. The driver might notice a slightly longer boot or a "your update didn't apply, will retry later" notification. No degraded operating mode is needed because the ECU isn't in the safety loop — worst case is annoyance, not hazard.
- Thresholds can be looser (e.g., the full 3-attempt boot-loop budget, a shorter or even skippable soak period) because the cost of a false-positive rollback (unnecessarily reverting a good update) and the cost of a false-negative (committing a subtly-broken update a bit too early) are both low and roughly symmetric.

**Safety-critical actuation ECUs (steer-by-wire, braking, etc.):**
- The same A/B/watchdog/soak mechanism applies, but layered with additional mechanisms, because "just boot the old version" isn't sufficient reassurance when the failure mode being guarded against is "the vehicle can't be steered":
  - **A hardware-enforced minimal safe-fallback firmware** — a small, extremely stable firmware image (conceptually similar to the recovery partition in 6.6, but potentially even more minimal) that provides only the bare minimum safe actuation behavior and is updated, if ever, on a timescale of years with the highest level of scrutiny — not part of the routine A/B rotation at all. Think of it as the functional equivalent of an aircraft's mechanical backup flight controls: rarely touched, deliberately simple, and trusted precisely because it almost never changes.
  - **Degraded-but-safe operating modes rather than binary success/failure** — if both the new and old software-defined partitions are unusable, the ECU should be able to fall back to a strictly limited-function mode (e.g., steering assist disabled but a mechanical/hydraulic backup linkage still provides basic control, or braking falls back to a simpler, independently-verified control law with reduced regenerative braking but full mechanical braking intact) rather than presenting the driver with a fully inert, unresponsive system.
  - **Independent, redundant verification of the health check itself** — for the highest-criticality ECUs, the health-check verdict shouldn't be trusted from a single source; a second, independent monitor (potentially on a separate physical microcontroller, a common pattern for safety-rated automotive control units) cross-checks the primary health check's verdict before the system commits to a new version.
  - **More conservative rollback triggers** — a lower DTC tolerance during soak (even a single non-critical-but-unusual DTC might extend the soak window rather than being ignored), and a shorter fallback-latency budget at boot (closer to 2-3 seconds than 10-15, since a steer-by-wire ECU waking from a low-power state while the vehicle may already be rolling cannot tolerate as long an ambiguity window).

**ASIL and ISO 26262, briefly:** ISO 26262 is the automotive functional-safety standard, and it classifies hazards using **ASIL (Automotive Safety Integrity Level)**, from **ASIL A** (lowest rigor) through **ASIL D** (highest rigor) — determined by a hazard's severity, exposure (how often the operating situation occurs), and controllability (how much the driver can do about it if it goes wrong). Steer-by-wire and braking control functions typically land at ASIL D, since a failure is high-severity, occurs in essentially all driving situations, and offers the driver little to no ability to compensate; an infotainment display defect is typically QM (below ASIL A — no special safety rigor required) or at most ASIL A. **Why this matters for update/rollback design specifically:** ISO 26262 requires that the *rigor of verification* scale with ASIL — for a D-rated component, that translates concretely into things like independent verification of safety-relevant decisions (hence the redundant health-check monitor above), additional hardware redundancy (dual sensors, independent power paths), and more conservative fault-handling behavior (prefer a safe degraded state over any state whose safety hasn't been proven) — which is exactly the reasoning behind stricter rollback triggers, mandatory degraded-mode fallbacks, and a near-frozen minimal safe-fallback firmware for the highest-ASIL ECUs, versus a much lighter-touch mechanism being acceptable for a QM-rated infotainment unit.

### 6.6 The true worst case: both partitions unusable

This deserves more than the one sentence Document #1 gives it, because it's the scenario every reviewer will push on.

- **How this can happen:** both A and B become unbootable — e.g., a defect in the update logic itself corrupts the currently-active partition during what should have been a routine write to the *inactive* one (a bug, not the intended design), a hardware fault affects a flash region spanning both partitions, or an attacker somehow manages to corrupt both (mitigated separately by signature verification, but worth naming as a threat).
- **The mitigation is a physically and logically separate recovery/bootstrap partition** — a third image, distinct from the A/B application partitions, that the first-stage (immutable) bootloader can always fall back to as an absolute last resort. It's deliberately minimal: enough to bring the ECU to a known-safe baseline (for an actuation ECU, this might mean the same minimal safe-fallback firmware described in 6.5; for infotainment, it might mean a bare factory-default image with basic connectivity to allow re-provisioning).
- **How it's protected from ever being overwritten by a routine OTA:** the recovery partition is not a target of the normal A/B write path at all — the partition manager's write API doesn't expose it as a valid destination for staged updates, and ideally it sits behind a hardware write-protect mechanism (e.g., a region that's only writable when a physical or cryptographic "recovery update mode" is explicitly entered, which routine OTA campaigns never do). This is the same principle as a phone's separate recovery-mode partition, or a server's out-of-band management firmware — it must be architecturally impossible for a bug in the routine update path to reach it, not just policy-prohibited.
- **Its own update policy is intentionally the opposite of the routine OTA pipeline:** updates to the recovery partition happen extremely infrequently (think low-single-digit times per *vehicle lifetime*, not per year), require the highest level of scrutiny in Document #9's pipeline (dedicated review, likely the on-prem-HSM-tier signing key referenced there, and probably staged through an even smaller, more conservative canary population than a normal release), and — for the highest-ASIL components — may reasonably require the vehicle to be at a service center rather than applied fully remotely, trading convenience for an extra layer of assurance on the one thing that must never itself become the single point of failure.
- Say this explicitly: *"The recovery partition's entire value proposition is that it almost never changes. The moment you start treating it like just another routine OTA target, you've recreated the exact problem it exists to solve — now you need a recovery path for your recovery path."*

---

## 7. Minimal API Surface (illustrative, on-vehicle local interfaces)

```
# Bootloader-internal (not network-exposed; conceptual interfaces between bootloader stages)
read_boot_attempt_record()          -> BootAttemptRecord
persist_boot_attempt_record(record) -> ack   (must complete before jumping to candidate code)
verify_partition(slot)               -> { valid: bool, hash_match: bool }
mark_slot_active(slot)
mark_slot_disqualified(slot)

# Health-check service (invoked by boot manager after application signals "up")
run_health_check(timeout_ms) -> { verdict: PASS|FAIL|TIMEOUT, checks: [...] }

# Soak monitor (runs continuously post-boot)
report_drive_cycle_complete()
report_dtc(code, severity)
get_soak_status() -> SoakState

# Local diagnostic interface (for dealer/service tooling, works with zero connectivity)
GET /local/health-check-log        -> HealthCheckLog entries
GET /local/boot-attempt-record     -> current BootAttemptRecord
GET /local/soak-status             -> current SoakState

# Eventually-consistent reporting to backend (reuses Document #1's status-reporting path)
POST /v1/vehicles/{vehicle_id}/rollback-event
     -> { component_id, from_version, to_version, trigger: BOOT_LOOP|SOAK_FAILURE|
          RECOVERY_MODE, health_check_log_excerpt, timestamp }
```

---

## 8. Trade-offs and Alternatives Considered

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| Where atomicity is enforced | Reduce atomicity requirement to a single small marker-flip write, guarded by write barriers before it | Attempt to make the entire multi-hundred-MB write transactionally atomic | No realistic embedded flash/storage layer can make a huge write atomic directly; decomposing to "everything upstream is idempotent/retryable, only the marker flip must be atomic" maps onto guarantees real flash hardware can actually provide. |
| Boot-loop threshold | 3 consecutive failures | 1 failure triggers immediate fallback | A single-failure threshold has an unacceptable false-positive rate against transient faults (sensor warm-up, timing glitches), causing unnecessary rollbacks; 3 balances a small additional delay (~45s worst case) against much better discrimination between transient and real defects. |
| Soak period | Full drive cycle, capped at 24-48h | Commit immediately after a passing boot-time health check | A boot-time check alone can't catch defects that only surface under sustained real-world operation (thermal, load, timing); but an uncapped soak could hold storage hostage indefinitely for a rarely-driven vehicle. |
| Safety-critical ECU fallback | Layered: A/B rollback + hardware-enforced minimal safe-fallback firmware + degraded-but-safe modes | Rely solely on the same A/B mechanism used for infotainment | For ASIL D components, "reboot to the old version" isn't sufficient reassurance on its own — a mechanism whose own failure mode could itself be hazardous needs independent, redundant, more conservative layers on top. |
| Worst-case recovery | Separate, rarely-touched recovery/bootstrap partition, architecturally unreachable by routine OTA | Rely on A/B redundancy alone (no third partition) | A/B redundancy assumes at least one of the two is always healthy; a third, structurally isolated fallback is the only mitigation for the scenario where that assumption breaks (both corrupt simultaneously). |
| Counter storage location | Physically separate from both A/B partitions | Store the attempt counter inside the partition being booted | A corrupted partition could corrupt its own counter, or a reflash could reset it; keeping it in independent, bootloader-owned storage makes boot-loop detection resilient to exactly the failures it's meant to catch. |

---

## 9. Failure Modes & Edge Cases to Call Out Proactively

- **Power loss exactly during the marker-flip write:** mitigated by choosing a marker size/alignment that the underlying flash technology can write atomically in a single operation — the bootloader will observe either the old marker value or the new one, never a corrupted hybrid.
- **A health check that itself hangs (not fails, just never returns):** treated identically to an explicit FAIL via a hard timeout — never allow "still waiting" to persist indefinitely, since that's operationally indistinguishable from a hang the driver experiences as a dead vehicle.
- **A defect that only manifests under conditions the health check and soak period don't cover** (e.g., a rare combination of temperature and load that occurs once a year): acknowledge this as a genuine residual risk — no finite test suite catches everything — and mitigate at the fleet level via Document #1's canary rings and anomaly-detection auto-halt, which is a complementary, population-level safety net on top of this per-vehicle mechanism.
- **The soak monitor itself has a bug that fails to detect a real critical DTC:** mitigate by keeping the soak monitor's logic intentionally simple and separately, rigorously tested/verified relative to the feature code it's monitoring — a complex soak monitor is itself a liability.
- **Boot-loop counter persisted successfully, but the fallback partition has since degraded (bit rot) since it was last actually booted:** this is exactly why every boot, including a fallback boot, re-verifies the target partition's signature/hash rather than assuming "it passed once, it's still fine" — feeding into the recovery-partition path if even the fallback fails.
- **Two ECUs on the network are mid-rollback simultaneously and briefly disagree about protocol version during the transition:** during any window where dependent ECUs might be running mismatched versions (one rolled back, one not yet), the CAN-bus responsiveness check in 6.2 should be tolerant of version skew for non-critical fields, but must hard-fail on any safety-relevant message-format mismatch — version compatibility windows should be an explicit, tested part of the release process, not an afterthought.
- **An attacker deliberately tries to induce a boot loop as a denial-of-service** (e.g., repeatedly triggering updates that fail): mitigated by the same signature-verification-at-every-boot mechanism preventing untrusted images from ever becoming boot candidates in the first place, plus rate-limiting how frequently a new candidate can even be staged (a backend-side concern, but worth naming as a threat model).

---

## 10. Monitoring, Observability, and Security (brief)

- **Dashboards:** fleet-wide rollback rate per component/version (feeds Document #1's canary anomaly detection — a spike in per-vehicle rollback events is itself a strong signal to auto-halt a campaign), soak-failure rate broken down by DTC code, recovery-partition invocation count (should be effectively zero at fleet scale — any nonzero count deserves individual investigation).
- **Alerting:** any recovery-partition invocation anywhere in the fleet should page an engineer immediately — this event is rare enough and severe enough that it should never be treated as routine telemetry noise.
- **Audit/compliance:** the local `HealthCheckLog` plus the eventually-reported `rollback-event` stream together form the evidence trail expected by ISO 26262 functional-safety audits and internal incident review — every automatic fallback decision must be reconstructable after the fact, including exactly which check failed and why.
- **Security:** signature/hash re-verification at every boot (not just once at flash time) closes the window where a partition could be tampered with after passing initial verification; the recovery partition's hardware write-protection is itself a security boundary, not just a reliability one — it also prevents a compromised application layer from ever overwriting the one thing guaranteed to bring the vehicle back to a trusted state.

---

## 11. Wrap-up / How to Close the Interview

Summarize in 30 seconds: *"To recap: atomicity is achieved not by making a giant write atomic, but by decomposing the update into a fully retryable data write followed by a single, hardware-guaranteed atomic marker flip. A layered boot-time watchdog — fast liveness checks, then CAN responsiveness, then a deeper self-test suite — produces a pass/fail verdict within a tight timing budget, backed by a persistent, independently-stored boot-attempt counter that guarantees boot-loop detection even across crashes that happen before the application layer runs. A soak period extends the safety net beyond boot time to catch defects that only surface under real driving conditions before we permanently commit and reclaim the old partition. Safety-critical ECUs get everything infotainment gets, plus a hardware-enforced, rarely-touched minimal safe-fallback firmware, degraded-but-safe operating modes, and stricter thresholds justified by ISO 26262 ASIL reasoning. And the true worst case — both application partitions unusable — is covered by a structurally isolated recovery partition that routine OTA can never reach, with its own extremely conservative, near-frozen update policy."*

Then proactively offer extension directions:
- How would you extend the redundant/independent health-check verification concept (mentioned briefly for ASIL D components) into a full dual-microcontroller safety architecture, and how would the two controllers reach agreement without introducing their own consensus/failure problems?
- How would you design the *cross-ECU* version-compatibility matrix so that a rollback on one ECU doesn't strand the vehicle with an incompatible combination of versions across the CAN network?
- How would this design need to change for an ECU with no dual-partition storage budget at all (a genuine hardware constraint on some low-cost components) — what's the minimum viable fail-secure mechanism without A/B redundancy?

---

## 12. Follow-up Questions Interviewers May Ask

- "Walk me through, instruction by instruction, what happens if power is lost at the exact moment the boot-loop counter is being persisted."
- "Why increment the attempt counter before the boot attempt instead of after a failure is detected — what specifically goes wrong with the other ordering?"
- "How would you decide the boot-loop threshold empirically rather than just picking a number — what data would you want from the fleet?"
- "What's the difference between what the health check verifies and what the soak period verifies, and why can't one subsume the other?"
- "How does ASIL classification concretely change which checks you run or how long you wait, versus just being a compliance label?"
- "If the recovery partition is almost never updated, how do you keep confidence that it will actually work correctly years after it was flashed, on hardware that has since evolved?"
- "How would you test this entire mechanism, including the both-partitions-corrupt worst case, without literally bricking test vehicles?"

---

## References

- Rivian system design round context and exact question wording: see [`../rivian/index.md`](../rivian/index.md), section "Common Questions" (#10).
- General OTA distribution/rollout system this deep-dive extends (delta updates, campaign orchestration, canary rollout, the brief A/B partition summary this document expands on): see [`./ota-update-system-for-connected-vehicle-fleet.md`](./ota-update-system-for-connected-vehicle-fleet.md).
- Sibling deep-dive on the build/sign/CI-CD pipeline that produces the signed artifact this document assumes already exists in the inactive partition: see [`./secure-automated-ota-deployment-pipeline.md`](./secure-automated-ota-deployment-pipeline.md).
- Conceptually related to Android's A/B (seamless) update verified-boot model, and to ISO 26262 functional-safety concepts (ASIL classification, redundant verification for high-integrity components) as applied to automotive software-update mechanisms.
