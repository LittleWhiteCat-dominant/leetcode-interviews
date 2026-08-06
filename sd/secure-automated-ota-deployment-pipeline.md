# System Design Mock Interview: Secure, Automated OTA Deployment Pipeline (DevOps/Infra Variant)

**Company theme:** Rivian-style (vehicle/EV), also broadly applicable to Tesla, Ford, Waymo, or any connected-fleet company shipping embedded firmware.
**Round:** System Design (45-60 min onsite loop) — DevOps/Infrastructure-leaning variant.
**Interviewer expectation:** Structured problem-solving with a CI/CD and release-engineering lens: build/sign/release pipeline mechanics, credential and secrets management, and audit/provenance — not a specific tech stack.

> **This is a deep-dive variant, not a standalone system.** The general OTA distribution/rollout system (campaigns, delta packages, A/B partitions, the vehicle agent, rollout pacing) is covered in [`./ota-update-system-for-connected-vehicle-fleet.md`](./ota-update-system-for-connected-vehicle-fleet.md) ("Document #1"). That document explicitly scopes *out* the build/sign/release pipeline, assuming "artifacts already exist and are signed." **This document owns exactly that scoped-out piece.** Where content overlaps (e.g., canary rollout mechanics, rollback triggers), we keep it brief and point back to Document #1, and spend the bulk of our time on what's genuinely new: source-to-artifact CI/CD, code-signing key management, hybrid cloud/factory secrets, and provenance/traceability.

This document is written as a self-contained interview walkthrough: clarifying questions, a model answer per section, and likely follow-up probes.

---

## 0. Opening: Clarify the Problem (first 3-5 minutes)

> **You:** "This sounds related to a general OTA rollout design I've thought through before — distribution, canary rings, A/B rollback on the vehicle. Should I assume that layer exists and focus on the pipeline that *produces* the signed artifact it consumes — the CI/CD, build, and signing process — or do you want the full stack again?"
>
> **Interviewer:** "Correct, assume the fleet-side rollout mechanism already exists. I want you to go deep on how a firmware change gets from a developer's commit to a signed, trusted artifact sitting in the distribution store — securely, automatically, and with full traceability. Rollback here means 'the pipeline itself detects a bad release and auto-reverts it,' not just the on-vehicle A/B mechanism."
>
> **You:** "A few more questions:
> 1. Are we building for a single component (say, one ECU's firmware) or a fleet of heterogeneous ECUs, each with its own toolchain?
> 2. Do we need hardware-in-the-loop (HIL) testing before an artifact is trusted, or is software-only CI sufficient?
> 3. What does 'hybrid cloud and factory environments' mean concretely — are factories air-gapped, or do they have some connectivity?
> 4. Who are the actors we need to model: developers, release engineers, security/compliance, and the automated pipeline itself — do any of them have different trust levels?
> 5. Is regulatory audit (e.g., automotive functional-safety or cybersecurity standards like ISO/SAE 21434) an explicit requirement, or just 'good practice'?"

Assume the interviewer answers:
- Dozens of heterogeneous ECU targets (ADAS, infotainment, BMS, body control), each with its own cross-compilation toolchain and test harness.
- Hardware-in-the-loop testing is required before any artifact can be promoted past CI — software-only unit tests are not sufficient for firmware destined for a real ECU.
- Factories provision device-unique keys/certificates at manufacturing time and have **limited, often intermittent connectivity** back to the cloud (some are effectively air-gapped for security reasons) — this must be designed around, not assumed away.
- Developers should never have direct access to signing keys; release engineers approve *promotions*, not individual builds; the pipeline itself is the only automated actor with (scoped, short-lived) signing access.
- Full audit trail from a fielded vehicle's running version back to source commit is a hard requirement — this is both a security and regulatory (ISO/SAE 21434, UNECE R156) expectation.

---

## 1. Functional Requirements

**Core function** — the 1-3 things this system must fundamentally do; everything else below is elaboration on how:

1. Automatically take a firmware commit from source through build, test, and signing to a trusted, distributable artifact.
2. Guarantee that only artifacts signed by the authorized pipeline itself — never a human or an unscoped credential — can ever reach a vehicle.
3. Detect a bad release from canary telemetry and automatically halt or revert its promotion without waiting on a human.

The fuller requirement list:

1. **Source-to-artifact CI/CD** — every commit to a component's firmware repo triggers cross-compilation, static analysis/security scanning, and unit tests; only artifacts that pass all gates become candidates for further promotion.
2. **Hardware-in-the-loop (HIL) validation** — candidate artifacts are automatically flashed to a rig of real (or high-fidelity emulated) ECUs and run through a regression/safety test suite before promotion to staging.
3. **Code-signing service** — a centralized, HSM-backed service signs approved artifacts; no human or CI job ever has direct access to a private signing key.
4. **Environment promotion pipeline** — automated, gated promotion: `dev → staging → canary → production`, each gate backed by automated checks (test results, HIL results, telemetry from a prior stage) rather than manual sign-off, except for a final human-approved release gate for mandatory/safety-impacting releases.
5. **Secrets management across hybrid environments** — distinct secret stores and access models for cloud CI/CD (build credentials, artifact-store credentials) versus factory-floor systems (device-provisioning keys), with short-lived, scoped credentials throughout.
6. **Factory-time device provisioning** — at manufacturing time, each vehicle/ECU receives a unique identity (device certificate/key pair), issued from a factory-local provisioning service that can operate with intermittent or no cloud connectivity.
7. **Build provenance & SBOM generation** — every artifact carries an immutable, cryptographically-verifiable record of its source commit, build environment, dependency versions (SBOM), and every signing event it underwent.
8. **Full traceability query** — given a `component_id` + `version` running on a fielded vehicle, an engineer or auditor can retrieve the exact commit, build job, test results, HIL results, and signing event that produced it.
9. **Automated rollback/release-gate-failure handling** — if telemetry from a canary stage (fed by Document #1's rollout mechanism) crosses a failure threshold, the pipeline automatically marks that release as "reverted," halts further promotion, and reinstates the previous release as the promotion target — framed as a CI/CD concept ("failed release gate → auto-revert"), distinct from the vehicle-local A/B partition rollback.

**Out of scope (state this explicitly):** the vehicle-side agent, A/B partition/boot mechanics, and delta-package generation are covered in Document #1 and assumed to exist as consumers of this pipeline's output. We also don't re-derive fleet-scale rollout pacing — we reuse it as the production gate's data source.

---

## 2. Non-Functional Requirements

| Requirement | Target / Reasoning |
|---|---|
| **Key security** | Private signing keys must never exist outside an HSM in plaintext, ever — not on a CI runner's disk, not in an environment variable, not in a log. This is the single hardest constraint in this design. |
| **Least privilege** | No individual (developer, release engineer, or even most automated jobs) should be able to sign an artifact directly. Only a narrowly-scoped signing service, itself invoked by an authenticated pipeline stage, can request a signature. |
| **Auditability / non-repudiation** | Every signing event, every promotion decision, and every credential issuance must be logged immutably and attributable to a specific principal (human or service identity) — required for both incident response and regulatory audit. |
| **Availability of the pipeline** | CI/CD control plane: 99.9%+ during business hours is reasonable (a pipeline outage delays releases but doesn't brick vehicles); the *factory provisioning* path has a stricter local-availability requirement since a line-down event at a factory is extremely costly. |
| **Resilience to intermittent factory connectivity** | Factory provisioning must function correctly for hours-to-days of cloud disconnection, similar in spirit to Document #1's offline-first vehicle agent, but for a very different actor (a provisioning station on a factory floor, not a fielded vehicle). |
| **Secrets rotation** | Short-lived credentials (minutes-to-hours) for CI/CD service accounts; longer-lived but still rotatable signing keys (weeks-to-months) with a defined rotation and revocation procedure that doesn't require re-signing already-fielded artifacts. |
| **Build reproducibility** | Given the same commit and pinned toolchain/dependency versions, a rebuild should produce a bit-identical (or at least behaviorally-identical and independently verifiable) artifact — this underlies both the SBOM's usefulness and the ability to detect a tampered build environment. |
| **Traceability latency** | A provenance query (version → commit/build/signing chain) should resolve in seconds, not minutes — this is frequently needed *during* an active incident, not just for after-the-fact audits. |
| **Throughput** | The pipeline must keep up with dozens of ECU targets, each with multiple daily commits, without becoming the bottleneck to shipping a security patch quickly. |

Call out explicitly to the interviewer: *"The central tension in this design is between developer velocity — dozens of engineers want fast CI feedback — and the fact that the blast radius of a compromised signing key is 'attacker can push arbitrary code to millions of vehicles.' Every design choice below is really about how we get both without one compromising the other."*

---

## 3. Back-of-the-Envelope Capacity Estimation

- **Number of components/ECU targets:** ~30-50 distinct firmware images across the fleet (ADAS, infotainment, BMS, body control, gateway, etc.), each with its own repo and toolchain.
- **Commit/build volume:** assume ~200 engineers across these components, each triggering a handful of CI builds/day (on push, on PR) → roughly **500-1,500 CI builds/day** across all components combined. Most of these never leave the `dev` stage.
- **HIL rig throughput:** a HIL test suite for one ECU might take 15-45 minutes per candidate (flash + boot + run regression suite). With a shared rig pool (say 20-30 rigs across all ECU types) and only a fraction of dev builds promoted to HIL candidacy (say 5-10% pass initial CI and are worth HIL time), that's roughly **50-150 HIL runs/day**, comfortably fitting a rig pool of that size with some queuing at peak.
- **Signing throughput:** only artifacts that clear staging need signing — call it **10-30 signing events/day** in steady state, spiking during a coordinated multi-component release. An HSM-backed signing service handling low hundreds of requests/day has enormous headroom versus typical HSM throughput (thousands of ops/sec) — the bottleneck here is process/approval latency, not cryptographic throughput.
- **Promotion pipeline latency (dev → staging → canary → production):** dev CI ~10-20 min, HIL validation ~30-60 min, staging soak ~hours to 1 day, canary soak (reusing Document #1's 24-48h ring soak) ~1-2 days, production rollout itself spans days-to-weeks per Document #1's pacing. **End-to-end, a security patch expedited through every gate can realistically reach the first canary ring within a day, but a full-fleet release is still a multi-day-to-multi-week affair** — the pipeline doesn't shortcut the fleet-side rollout, it just makes getting a *trustworthy* artifact to the front of that rollout fast and safe.
- **Factory provisioning volume:** at a manufacturing rate of, say, 1,000-3,000 vehicles/day across factories, and ~10 provisionable components per vehicle needing a unique key/certificate, that's **10,000-30,000 device-identity provisioning events/day** — this needs to work even if a factory's cloud uplink is degraded, since a stalled provisioning line is a direct production-line cost.
- **Audit/provenance log volume:** each build, HIL run, signing event, and promotion decision generates one immutable record; at ~1,500 builds/day plus proportionally fewer HIL/signing/promotion events, this is on the order of a few thousand records/day — trivial in volume, but each record must be tamper-evident (e.g., hash-chained or written to a write-once store), which shapes storage choice more than volume does.

Conclusion to state out loud: *"Unlike Document #1, where the bottleneck was egress bandwidth, here the bottleneck is almost entirely process latency and trust boundaries — HIL rig availability and human approval gates, not raw throughput. The design should optimize for fast, safe promotion decisions and airtight key custody, not for scaling a firehose of data."*

---

## 4. Data Model / Database Design

### Core entities

**`Commit`** (a source-controlled change to a component)
```
commit_sha (PK)
component_id
author
timestamp
branch
```

**`Build`** (one CI run producing a candidate artifact from a commit)
```
build_id (PK)
commit_sha
component_id
toolchain_version       -- pinned compiler/SDK version, part of reproducibility
status                  -- PENDING / PASSED_CI / FAILED_CI
static_analysis_report_url
sbom_url                 -- software bill of materials for this build's dependencies
artifact_checksum_sha256
created_at
```

**`HilRun`** (a hardware-in-the-loop validation of a `Build`)
```
hil_run_id (PK)
build_id
rig_id
test_suite_version
status                   -- PASSED / FAILED / INCONCLUSIVE
results_url
started_at, completed_at
```

**`SigningEvent`** (an immutable record of the HSM signing a specific artifact)
```
signing_event_id (PK)
build_id
signing_key_id            -- which HSM-resident key (rotatable) signed this
requested_by              -- service identity of the pipeline stage, never a human
approved_by                -- release engineer who approved the *promotion* that triggered signing (nullable for fully-automated non-production stages)
signature
signed_artifact_checksum_sha256
timestamp
```

**`Release`** (a signed artifact promoted into the environment-promotion pipeline)
```
release_id (PK)
signing_event_id
component_id
version
current_stage             -- DEV / STAGING / CANARY / PRODUCTION / REVERTED
promoted_at (per stage, or a separate PromotionEvent log)
```

**`PromotionEvent`** (append-only audit log, one row per stage transition — mirrors Document #1's `UpdateEvent` pattern, applied to the pipeline instead of the fleet)
```
event_id (PK)
release_id
from_stage, to_stage
gate_result (JSON)         -- which automated checks passed/failed, telemetry snapshot if applicable
triggered_by                -- "automated_gate" or a specific human principal
timestamp
```

**`DeviceIdentity`** (factory-issued, per-ECU-instance cryptographic identity — distinct from a `Release`, which is per-version, not per-device)
```
device_identity_id (PK)
vehicle_vin
component_id
public_key_fingerprint
issued_at
issuing_factory_id
provisioning_station_id
```

### Why this shape?

Notice the chain `Commit → Build → HilRun → SigningEvent → Release → PromotionEvent` is a linear, append-only lineage — this is deliberate. *"A provenance query for 'what produced the code running on vehicle X's ADAS ECU' is a single walk backward through this chain: `VehicleUpdateState.current_version` (from Document #1) → `Release` → `SigningEvent` → `Build` → `Commit`. Because every link is immutable and hash-linked (each record includes the checksum/hash of the previous stage's artifact), the chain is independently verifiable — you don't have to trust the database, you can recompute checksums and confirm they match."* This is the concrete implementation of "SBOM and full traceability from a fielded version back to commit."

`DeviceIdentity` is deliberately a separate lineage from `Release`: a `Release` describes *what software* exists, while `DeviceIdentity` describes *which physical device* can trust and be trusted by that software (via mutual authentication during OTA delivery) — conflating "artifact provenance" with "device identity" into one table would make both harder to reason about and audit independently.

---

## 5. High-Level Design

This is an **infrastructure/topology view** — what pieces of infrastructure exist, what type each one is (stateless CI runner, HSM-backed side-car, hash-linked audit log, external fleet system...), and how they're wired together — not a step-by-step trace of one commit's journey. Sequencing and per-hop logic belong in the Deep Dives (§6); this section should stand on its own as "here's what we'd provision."

### Infrastructure tiers

**Client / dev tier**
- **Developer** — external; a commit or PR is the only thing this tier contributes. Not part of our infra footprint.

**CI/build tier**
- **Source Control + CI Orchestrator** — triggers builds on commit/PR, runs cross-compilation per ECU toolchain, static analysis, and unit tests; produces an unsigned candidate artifact plus its SBOM.
- **HIL Test Farm** — a pool of rigs (real ECUs or high-fidelity emulators) that flash and exercise a candidate against a regression/safety test suite; reports pass/fail to the orchestration tier.

**Control-plane / side-car services (consulted by pipeline stages, never on the main promotion path)**
- **Signing Service (HSM-backed)** — the *only* component with any path to a private key; a narrow request/response API in front of an HSM, never invoked directly by CI.
- **Secrets & Credential Broker** — issues short-lived, scoped credentials to CI jobs and to factory provisioning stations, fronting two distinct underlying stores:
  - **Cloud Secrets Store** — CI/CD credentials (source-repo tokens, artifact-bucket access).
  - **Factory-Local Secrets Store** — device-provisioning keys, built to tolerate intermittent or air-gapped factory connectivity.

**Orchestration tier**
- **Environment Promotion Controller** — the state machine walking a `Release` through `DEV → STAGING → CANARY → PRODUCTION`, consulting the CI/HIL/Signing side-cars and — at the canary gate — Document #1's rollout telemetry.
- **Auto-Revert Controller** — subscribes to the same rollout-health telemetry as Document #1's anomaly detector; on a release-gate failure, flips a `Release` to `REVERTED` and re-targets the previous known-good `Release`.

**Factory-floor tier**
- **Factory Provisioning Service** — runs on factory-local infrastructure; issues `DeviceIdentity` records at manufacturing time, designed to tolerate the factory's cloud uplink being degraded or temporarily unavailable.

**Storage / serving tier**
- **Provenance/Audit Store** — the immutable, hash-linked `Commit → Build → HilRun → SigningEvent → Release → PromotionEvent` chain; queryable for both real-time incident response and long-horizon compliance audits.

**External dependency**
- **Rollout/Telemetry Pipeline (Document #1)** — the fleet-side rollout mechanism the Promotion Controller's canary gate reads telemetry from, and that the Auto-Revert Controller's re-targeted release feeds back into.

### Topology diagram (infrastructure view, described in ASCII)

```
  CLIENT/DEV TIER      CI/BUILD TIER                                        ORCHESTRATION TIER
 ┌────────────┐  push  ┌────────────────────┐  candidate  ┌────────────────┐  gates  ┌────────────────────────────────────┐
 │  Developer  │───────►│  CI Orchestrator    │──artifact──►│  HIL Test Farm │─pass/──►│ Environment Promotion Controller    │
 └────────────┘        │ (build+SAST+tests)  │             │  (rig pool)    │  fail   │  DEV ─► STAGING ─► CANARY ─► PROD    │
                        └────────────────────┘             └────────────────┘         └──────┬──────────────────┬────────────┘
                                                                                                │ sign request      │ canary telemetry
                                                                                                ▼                   ▼
                     CONTROL-PLANE / SIDE-CAR          ┌────────────────────┐        ┌───────────────────────────┐
                     (consulted, not on main path) ───►│  Signing Service    │        │ Rollout/Telemetry Pipeline │ (external, Doc #1)
                                                        │  (HSM-backed)       │        └─────────────┬───────────┘
                                                        └─────────┬───────────┘                       │ anomaly signal
                                                                  │ SigningEvent                        ▼
                                                                  ▼                            ┌────────────────────┐
                                                        ┌────────────────────────┐              │ Auto-Revert         │
                                                        │ Provenance/Audit Store   │◄─────────────┤ Controller          │
                                                        │ (hash-linked, append-only)│              └────────────────────┘
                                                        └────────────────────────┘

  CONTROL-PLANE / SIDE-CAR (secrets, a separate concern from signing)              FACTORY-FLOOR TIER
 ┌───────────────────┐        ┌───────────────────────┐        ┌───────────────────────┐        ┌───────────────────────┐
 │ Cloud Secrets Store │◄─────►│ Secrets & Credential   │◄─────►│ Factory-Local Secrets  │───────►│ Factory Provisioning    │
 │ (CI/CD credentials) │       │ Broker (short-lived)    │       │ Store (device keys,     │ shift- │ Service (per factory,   │
 └───────────────────┘        └───────────────────────┘        │ intermittent-tolerant)  │ scoped │  issues DeviceIdentity) │
                                                                  └───────────────────────┘  cred.  └───────────────────────┘
```

Narrate the key architectural decision: *"The one component every path to a trusted artifact must pass through is the Signing Service — it sits off to the side as a control-plane side-car, not inline in the CI/HIL build tier, and it's the only thing that ever touches key material. That placement is the whole security property: a compromised CI runner or a buggy HIL rig can produce a bad candidate, but it has no network path to a signature, so it can't produce a trusted one. The Secrets Broker is a second, independent side-car solving a different problem — short-lived credential issuance across a cloud/factory trust boundary — and the Provenance Store and Auto-Revert Controller are downstream consumers of the orchestration tier's decisions, not additional pipeline stages. Nothing here is a linear pipeline; it's a small orchestration tier surrounded by narrowly-scoped side-cars it calls out to."*

---

## 6. Detailed Design / Deep Dives

Ask the interviewer which of these to go deepest on: *"Should I focus on the signing/key-custody model, the factory/hybrid-cloud secrets problem, or the automated promotion-gate and auto-revert logic?"*

### 6.1 Code-signing key management (HSM-backed, build vs. signing separation)

- **Key hierarchy:** a root-of-trust key (offline, used only to issue/rotate intermediate signing keys — think minutes of use per year) signs one or more per-component (or per-ECU-family) intermediate signing keys, which are the keys actually used day-to-day. This mirrors standard PKI practice: compromise of a frequently-used intermediate key is containable (rotate it, re-sign only affected releases going forward) without ever touching the root.
- **Strict separation of build-time and signing-time access.** A CI job that compiles code has read access to source and write access to an artifact staging bucket — nothing more. It has *zero* network path to the HSM. Signing is requested by the Promotion Controller (a distinct service identity) only after an artifact has cleared HIL and — for production — received release-engineer approval. This means even a fully compromised CI pipeline (malicious dependency, compromised runner) cannot self-sign a malicious artifact; it can, at worst, produce a bad *candidate* that still has to pass through a gate it doesn't control.
- **Key rotation without re-signing history.** Rotate intermediate signing keys on a fixed schedule (e.g., every 6-12 months) or immediately on suspected compromise. Because each `SigningEvent` records *which* `signing_key_id` was used, already-fielded artifacts remain verifiable against the old (now-revoked-for-new-signing-but-still-valid-for-verification) key — you revoke a key's ability to *produce new* signatures without invalidating history, similar to how a CA can stop issuing new certs from an old intermediate without invalidating already-issued ones.
- **HSM choice:** cloud KMS-backed HSM (e.g., a FIPS 140-2/3 validated cloud HSM) is sufficient for most component signing keys; the very top of the hierarchy (root key, and possibly keys for the highest-ASIL components — see Document B, [`./fail-secure-ota-rollback-architecture.md`](./fail-secure-ota-rollback-architecture.md), for the ASIL discussion) may warrant an on-prem HSM under dual physical control, trading operational convenience for an even smaller attack surface.

### 6.2 Secrets management across hybrid cloud and factory environments

- **Two distinct trust domains, two distinct secret stores.** Cloud CI/CD secrets (source-repo tokens, artifact-bucket credentials, signing-request tokens) live in a cloud secrets manager, issued as short-lived (minutes-to-hours) tokens scoped to a single pipeline run — a leaked CI secret has a small blast radius and a short shelf life.
- **Factory-floor secrets are a genuinely different problem.** Factories provision device-unique keys/certificates at manufacturing time, often on production lines with **limited or deliberately air-gapped connectivity** (security teams often *want* the factory floor isolated from the general corporate network to reduce attack surface). This means the Factory Provisioning Service can't simply call out to the cloud secrets manager synchronously for every device.
- **Mitigation: pre-provisioned, locally-cached signing capability with periodic reconciliation.** Each factory-local provisioning station holds a *batch-issued, short-lived* device-issuance credential (e.g., valid for one shift or one day, enough device-identity "budget" for expected line throughput) fetched during a connectivity window, and can issue individual `DeviceIdentity` records offline against that budget. When connectivity is restored, the station reconciles: reports what it issued, and the cloud-side PKI root revokes/refreshes the batch credential. This is structurally similar to Document #1's offline-first vehicle agent (store-and-forward, reconcile-on-reconnect) but applied to a factory station instead of a fielded vehicle.
- **Least privilege between humans and automation.** Release engineers can *approve a promotion* (a scoped, audited action) but cannot directly retrieve a signing key or a factory device-issuance credential. Automated pipeline identities can request signatures/issuances but only within their narrow scope and only as a consequence of a passed gate — no standing broad credentials for either humans or machines.
- **Credential-leak blast-radius design goal to state explicitly:** *"If any single credential leaks — a CI token, a factory station's batch credential, even a release engineer's approval-console session — the worst case should be 'attacker can at most trigger or approve one already-gated promotion within a narrow scope and short time window,' never 'attacker can sign an arbitrary artifact' or 'attacker can mint unlimited device identities.'"*

### 6.3 Automated promotion gates (dev → staging → canary → production)

- Each stage transition is a *fully automated* decision, not a human clicking "approve" on a dashboard, with one deliberate exception noted below.
- **Dev → Staging:** gated on CI passing (build success, static analysis clean of high-severity findings, unit tests green) and HIL suite passing on at least N rig runs (to average out rig flakiness) with zero safety-relevant regressions.
- **Staging → Canary:** gated on a soak period in a staging environment that mirrors production telemetry ingestion (synthetic or dogfood-fleet traffic) showing no crash/error-rate regression versus the current production baseline.
- **Canary → Production:** gated on Document #1's canary-ring telemetry (crash rate, anomaly metrics) staying within threshold for the defined soak window — this is the one gate where this pipeline is a *consumer* of Document #1's mechanism rather than something new.
- **The one manual gate:** a release engineer must explicitly approve promotion to production for releases flagged as safety-impacting or for mandatory/security releases with unusually broad scope — not because automation isn't trusted, but because this is the point where a human accepts accountability for a fleet-wide action, which is both a good security practice and often a regulatory expectation. This approval is itself a signed, logged action tied to a specific `PromotionEvent`.
- **Idempotency and replay safety:** promotion-gate evaluation must be idempotent (re-evaluating the same gate with the same inputs always yields the same decision) so that a retried or replayed pipeline run can't accidentally double-promote or skip a gate due to a transient orchestrator hiccup.

### 6.4 Build provenance, SBOM, and end-to-end traceability

- Every `Build` generates an SBOM (list of every dependency, library, and toolchain version compiled in) at build time — not reconstructed after the fact, since a post-hoc SBOM is much easier to get subtly wrong or manipulate.
- **Reproducible builds as a verification mechanism:** for critical components, periodically rebuild from the recorded commit + pinned toolchain in a clean environment and confirm the artifact checksum matches — this detects a compromised build environment (e.g., a tampered CI runner injecting code at build time that wouldn't show up in a source diff).
- **The traceability query in practice:** *"Given `component_id=adas-ecu, version=4.2.1` running on a fielded vehicle (from Document #1's `VehicleUpdateState`), walk backward: `Release` row → `SigningEvent` (who/what requested and approved the signature, which key) → `Build` (commit SHA, SBOM, static-analysis report, toolchain version) → `HilRun` results → `Commit` (author, timestamp, diff). Every hop is a single indexed lookup, and every hop's integrity is checkable via the recorded checksums."* This is the concrete answer to "how do you know exactly what's running on a fielded vehicle and prove it."

### 6.5 Automated rollback as a CI/CD release-gate concept

- Document #1 covers the *vehicle-local* rollback mechanism (A/B partition, boot-time health check) — that's about a single vehicle recovering from a bad flash. This is a different, complementary concept: **the pipeline itself detects that an entire release is bad and stops recommending it to anyone else.**
- The Auto-Revert Controller subscribes to the same anomaly-detection signal Document #1's Campaign Orchestrator uses to auto-halt a rollout (elevated crash rate, canary metric deviation from baseline). The difference in framing: Document #1's halt stops *new* vehicles from receiving the bad version; this controller additionally flips the `Release`'s pipeline stage to `REVERTED` and re-targets the previous good `Release` as the active promotion candidate, so that any *subsequent* automated action (e.g., a new canary ring, a retry) defaults to the known-good version rather than the bad one.
- **Framed as a release gate, not an emergency procedure:** treat "release gate failed → auto-revert" as a routine, expected, well-tested code path in the promotion controller, not a rare break-glass procedure — this is the same philosophy as Document #1's fail-secure-by-construction rollback, applied one layer up in the pipeline.

---

## 7. Minimal API Surface (illustrative)

```
# CI/CD-facing (invoked by pipeline stages, all requests carry a short-lived, scoped token)
POST /v1/builds                         → register a new Build (commit_sha, component_id, artifact checksum, SBOM)
POST /v1/builds/{id}/hil-runs           → record a HilRun result
POST /v1/signing-requests               → { build_id, promotion_approval_token } → SigningEvent (HSM-backed; never returns key material)
POST /v1/releases/{id}/promote          → { target_stage, gate_evidence } → advance a Release through the promotion state machine
POST /v1/releases/{id}/revert           → invoked by the Auto-Revert Controller; flips stage to REVERTED, re-targets previous good Release

# Factory-facing (may operate against a locally-cached credential during connectivity gaps)
POST /v1/factory/device-identities      → { vehicle_vin, component_id, public_key } → issue a DeviceIdentity
POST /v1/factory/reconcile              → batch-report offline-issued identities once connectivity resumes

# Audit/traceability (read-only, for engineers and auditors)
GET  /v1/provenance/{component_id}/{version}   → full Commit→Build→HilRun→SigningEvent→Release chain
GET  /v1/releases/{id}/promotion-history        → ordered list of PromotionEvents with gate evidence
```

---

## 8. Trade-offs and Alternatives Considered

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| Signing access model | Centralized HSM-backed signing service, no direct key access for humans or CI | Give release engineers a local signing key/smart card | Centralizing removes key material from many endpoints to one narrowly-scoped, heavily-audited service; slightly slower/more complex than "just sign it locally," but the blast radius of a leak drops from "one person's laptop" to "a hardened service behind an HSM." |
| Build vs. signing separation | CI has zero network path to the HSM; signing is a separate service invoked post-gate | Let the CI pipeline call the signing API directly at the end of a successful build | A compromised CI runner with direct signing access could self-sign a malicious artifact; separating the concerns means compromising CI alone is insufficient to produce a trusted release. |
| Factory secrets | Locally-cached, short-lived batch credentials with reconcile-on-reconnect | Require synchronous cloud connectivity for every device-identity issuance | Factories often have limited/air-gapped connectivity by design (security posture); a synchronous requirement would halt the production line during any network blip — unacceptable given the cost of line-down time. |
| Promotion gates | Fully automated gates, with one explicit manual approval step for safety-impacting/mandatory releases | Fully manual sign-off at every stage | Manual sign-off doesn't scale to dozens of components with frequent commits and creates a human bottleneck exactly where consistency matters most; a single explicit human accountability point at the highest-stakes gate balances speed with governance. |
| Rollback framing | Pipeline-level auto-revert (stop recommending a bad release) layered on top of Document #1's vehicle-local A/B rollback | Rely solely on the vehicle-local A/B rollback and treat pipeline-level revert as manual | Vehicle-local rollback recovers one vehicle from one bad flash; without a pipeline-level auto-revert, the bad version could keep being pushed to new vehicles indefinitely until a human notices. |
| Provenance verification | Hash-linked, independently-recomputable chain (Commit→Build→...→Release) | Trust the database's records as-is | An attacker who could edit database rows directly could otherwise fabricate a clean-looking provenance trail; hash-linking means tampering is detectable even if the audit database itself is compromised. |

---

## 9. Failure Modes & Edge Cases to Call Out Proactively

- **HIL rig gives a false pass (rig itself is misconfigured or drifted from real hardware):** mitigate with periodic rig calibration/certification against a known-golden reference build, and require agreement across at least two independent rigs before a HIL result is trusted for production-bound artifacts.
- **Signing service compromised despite HSM (e.g., an attacker gains a valid, narrowly-scoped signing token through a different vulnerability):** mitigate with anomaly detection on signing *request patterns* themselves (unusual time, unusual component, unusual requester identity) — treat the signing service's own request log as a security-monitoring signal, not just an audit record.
- **Factory provisioning station's locally-cached credential is stolen (e.g., stolen laptop/HSM module at the factory):** the batch credential should be scoped tightly enough (single shift, single station, expected volume) that even full compromise only allows issuing a bounded number of device identities before the batch expires and is revoked at reconciliation — bound the blast radius by construction.
- **Reproducible build check fails unexpectedly (rebuild doesn't match recorded checksum):** don't assume malice first — nondeterministic build artifacts (embedded timestamps, unordered file inclusion, unpinned transitive dependencies) are a common root cause; but treat every mismatch as an incident to investigate, since it could also indicate a tampered build environment.
- **Auto-revert triggers on a false-positive canary signal:** exactly the same statistical-baseline mitigation as Document #1 (compare against a not-yet-updated control group rather than a fixed threshold) — an overly twitchy auto-revert that flaps between versions is itself an operational hazard.
- **A promotion gate is bypassed via a bug in the orchestrator (e.g., a race condition lets a Release skip straight to production):** design the promotion state machine so that `Release.current_stage` transitions are only ever written by the orchestrator after verifying the *previous* stage's gate evidence exists and is valid — never accept a stage-transition request that doesn't carry verifiable evidence for the prior gate, i.e., don't trust the caller's claim that "staging passed," recheck it.
- **Key rotation performed incorrectly, invalidating already-fielded artifacts' verifiability:** always rotate by adding a *new* signing key under the same (or a newly cross-signed) intermediate, never by deleting the old key's public verification material — verification keys for retired signing keys must remain available indefinitely (or for the vehicle's expected service lifetime) even after the key stops being used for new signatures.

---

## 10. Monitoring, Observability, and Security (brief)

- **Dashboards:** pipeline funnel per component (commits → CI-passed → HIL-passed → signed → promoted per stage), signing-request rate and requester-identity breakdown, factory provisioning throughput and reconciliation lag.
- **Alerting:** anomalous signing-request patterns (unusual requester, time-of-day, or component); factory station credential nearing budget exhaustion mid-shift; reproducible-build mismatches; any manual approval-gate bypass attempt.
- **Audit/compliance:** the hash-linked provenance chain plus the operator/approval action log directly supports both internal incident response and external regulatory audit (ISO/SAE 21434 cybersecurity engineering, UNECE R156 software-update-management-system expectations) — this pipeline's audit trail is frequently the artifact regulators actually ask to see.
- **Security:** HSM-backed key custody with strict build/sign separation; short-lived scoped credentials everywhere (no long-lived standing access for humans or most automation); mutual authentication between factory provisioning stations and the cloud PKI root; every privileged action (signing, promotion, credential issuance) individually attributable and logged.

---

## 11. Wrap-up / How to Close the Interview

Summarize in 30 seconds: *"To recap: we treat the pipeline itself as the security-critical asset, not just the fleet-side distribution — separating build-time access from signing-time access so a compromised CI job alone can never produce a trusted artifact, using an HSM-backed signing service with a small root-of-trust hierarchy, handling the factory's limited/air-gapped connectivity with locally-cached short-lived provisioning credentials that reconcile on reconnect, gating every environment promotion with automated checks (plus one deliberate human approval point for safety-impacting releases), and maintaining a hash-linked provenance chain so any fielded version can be traced back to its exact commit, build, and signing event — with a pipeline-level auto-revert that complements, rather than replaces, the vehicle-local A/B rollback from the general OTA design."*

Then proactively offer extension directions:
- How would you extend this to support **multi-region factories** with independent PKI roots that need to be cross-trusted by the same fleet backend?
- How would you design **key ceremony procedures** (multi-party control, dual authorization) for the root-of-trust key specifically, given how rarely it's used but how catastrophic its compromise would be?
- How would this pipeline need to change to support **third-party/supplier-delivered firmware** (e.g., a Tier 1 supplier ships a signed ADAS binary) where you don't control the build step at all — how do you extend provenance and trust to an artifact you didn't build?

---

## 12. Follow-up Questions Interviewers May Ask

- "Walk me through exactly what an attacker would need to compromise to push a malicious signed artifact to the fleet, end to end — where are the actual choke points?"
- "How do you handle a signing key compromise after the fact — what's the revocation and re-signing procedure, and what happens to vehicles that already received artifacts signed by the compromised key?"
- "What specifically changes about secrets management if a factory has zero cloud connectivity for an entire day due to a network outage — does the line stop?"
- "How would you extend build provenance to cover third-party/vendor-supplied binary components you don't build yourself?"
- "How do you prevent 'gate evidence forgery' — a compromised or buggy component claiming a HIL run passed when it didn't?"
- "What's your approach to reproducible builds for a large native/C++ codebase where perfect bit-for-bit reproducibility is genuinely hard (timestamps, build paths, parallel compilation ordering)?"
- "How does this pipeline's auto-revert interact with Document #1's fleet-side campaign halt — could they ever disagree, and how do you reconcile that?"

---

## References

- Rivian system design round context and exact question wording: see [`../rivian/index.md`](../rivian/index.md), section "Common Questions" (#9).
- General OTA distribution/rollout system this pipeline feeds into (delta updates, A/B partitions, canary rollout, offline-first vehicle agent): see [`./ota-update-system-for-connected-vehicle-fleet.md`](./ota-update-system-for-connected-vehicle-fleet.md).
- Conceptually related to standard software-supply-chain security practices (SLSA provenance levels, in-toto attestations, Sigstore-style keyless signing patterns) adapted to an embedded/automotive build pipeline with hardware-in-the-loop gates and factory-floor key provisioning.
