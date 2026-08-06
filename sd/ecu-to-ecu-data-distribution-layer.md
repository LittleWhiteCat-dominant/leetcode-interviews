# System Design Mock Interview: Real-Time Data Distribution Layer Between ECUs (CAN / Automotive Ethernet)

**Company theme:** Rivian-style (vehicle/EV), also broadly applicable to Tesla, traditional OEMs, or any automotive electronics/embedded-systems team.
**Round:** System Design (45-60 min onsite loop) — often given to candidates with an embedded/firmware or vehicle-networking background, but appears as a general system design prompt too.
**Interviewer expectation:** Structured problem-solving with real-time-systems rigor. Clarify → requirements → estimate → high-level → deep dive → trade-offs → wrap-up. This prompt rewards knowing that "real-time" here means deterministic worst-case latency bounds, not just "fast."

This document is written as a self-contained interview walkthrough: it includes the clarifying questions you should ask, a model answer for each section, and the follow-up probes an interviewer is likely to throw at you.

---

## 0. Opening: Clarify the Problem (first 3-5 minutes)

Don't start designing immediately. Restate the prompt and ask clarifying questions to narrow scope. Sample dialogue:

> **You:** "I want to make sure I'm scoping this correctly — this is an in-vehicle, ECU-to-ECU network, not the vehicle's connection to the cloud, correct? Very different problem: bounded bandwidth, hard real-time requirements, and safety criticality, versus the cloud side which is more about tolerating outages."
>
> **Interviewer:** "Correct, this is entirely inside the vehicle. Assume the cloud connectivity problem is solved elsewhere — you don't need to design that."
>
> **You:** "Good. A few more questions:
> 1. Are we designing for a classic distributed architecture (many small ECUs, each with a dedicated function, connected via CAN buses) or a modern centralized/zonal architecture (a few powerful domain controllers connected via automotive Ethernet)?
> 2. Roughly how many ECUs and how many distinct signals/messages are we distributing?
> 3. What's the mix of safety-critical (e.g., braking, steering) versus non-critical (e.g., infotainment, seat memory) traffic on this network?
> 4. Should I assume we're designing this from scratch for a new vehicle platform, or integrating with existing CAN-based subsystems that can't be redesigned?
> 5. Is there a requirement to bridge this internal network to the vehicle's cloud connectivity layer (e.g., for telemetry or OTA), or is that entirely out of scope?"

Assume the interviewer answers:
- Assume a **modern, mixed architecture**: legacy/cost-sensitive domains (body control, HVAC, seats) still use classic CAN or CAN-FD; safety- and performance-critical domains (ADAS, powertrain, braking) sit behind a central **zonal/domain-controller architecture bridged by automotive Ethernet**, which is the realistic state of the industry today and lets us discuss both.
- Roughly 60-100 ECUs across the vehicle, exchanging on the order of 1,500-3,000 distinct signals (individual data points like wheel speed, pedal position, door status) packed into a few hundred distinct message IDs.
- Mixed criticality: braking, steering, and powertrain traffic is hard real-time and safety-critical (ISO 26262 ASIL-B/C/D); body/comfort/infotainment is soft real-time or best-effort.
- Design from scratch for a new platform, but be aware that CAN and CAN-FD are effectively fixed, mature standards you're applying, not reinventing — the design work is in topology, message prioritization, gateway architecture, and how it integrates with a modern Ethernet backbone.
- Yes — mention briefly how this internal network connects to the vehicle-to-cloud layer via a gateway, but keep the two systems' concerns architecturally separate; don't redesign the cloud layer here.

---

## 1. Functional Requirements

**Core function** — the 1-3 things this system must fundamentally do; everything else below is elaboration on how:

1. Deliver a signal from its producing ECU to every consuming ECU within a bounded, provable worst-case latency.
2. Prevent a single faulty or misbehaving ECU from degrading or halting communication for the rest of the vehicle.
3. Arbitrate access to a shared, bandwidth-constrained medium so higher-criticality traffic always wins over lower-criticality traffic.

The fuller requirement list:

1. **Deterministic, low-latency signal delivery** — safety-critical signals (e.g., brake pedal position, wheel speed, steering angle) must be delivered from producing ECU to consuming ECU(s) within a bounded, predictable worst-case latency (typically single-digit milliseconds), not just "usually fast."
2. **Message prioritization / arbitration** — when multiple ECUs want to transmit simultaneously on a shared bus, higher-priority (more safety/time-critical) messages must always win access to the bus over lower-priority ones, without a central arbiter introducing its own latency or failure point.
3. **Broadcast and multicast signal distribution** — a single signal (e.g., vehicle speed) is often needed by many consuming ECUs (instrument cluster, ADAS, transmission control, infotainment) — the network must support efficient one-to-many delivery rather than point-to-point duplication.
4. **Bandwidth-efficient framing** — pack multiple small signals (each a few bits to a few bytes) into shared message frames to make efficient use of a fundamentally bandwidth-constrained medium (classic CAN: ~1 Mbps shared across the entire bus).
5. **Domain segmentation with cross-domain bridging** — partition ECUs into logical domains/buses (powertrain, chassis/safety, body, infotainment) to contain bus load and fault domains, with a gateway/domain controller relaying only the signals that legitimately need to cross domains.
6. **Deterministic scheduling for the highest-criticality traffic** — for the most safety-critical, hardest-real-time signals, support time-triggered (schedule-based) transmission in addition to (or instead of) purely priority-based arbitration, to guarantee jitter bounds that pure event-triggered priority arbitration cannot.
7. **Fault detection and graceful degradation** — detect a faulty/babbling ECU (one that floods the bus or sends corrupt frames) and isolate it (bus-off state) without taking down the rest of the network.
8. **Extensibility for new ECUs/signals** — adding a new ECU or a new signal to an existing message should be possible without requiring every existing ECU's software to be re-certified, as much as the architecture allows.
9. **Diagnostics and signal introspection** — support standard diagnostic access (e.g., reading live signal values, error frame counters) for factory and service-tool use, without that traffic contending with real-time safety traffic for bus priority.
10. **Bridging to the vehicle-to-cloud gateway** — a subset of signals (aggregated/sampled, not the raw high-frequency bus traffic) must be made available to the vehicle's connectivity/telemetry layer via a designated gateway ECU, without exposing the safety-critical bus directly to that outward-facing path.

**Out of scope (state this explicitly):** the vehicle-to-cloud communication protocol itself (assume the connectivity layer from the companion design exists and consumes what this gateway exposes), the specific application logic running on any individual ECU (e.g., the ADAS perception algorithm), and the electrical/physical-layer specification of the bus (voltage levels, connector types) beyond what's needed to reason about bandwidth and topology.

---

## 2. Non-Functional Requirements

| Requirement | Target / Reasoning |
|---|---|
| **Determinism / worst-case latency** | Safety-critical signals (braking, steering): bounded worst-case latency in the low single-digit milliseconds, with provable (not just empirical) upper bounds via arbitration/scheduling analysis. This is the defining NFR — "usually fast" is not acceptable for these signals. |
| **Jitter** | Time-triggered/periodic safety signals must have bounded jitter (e.g., sub-millisecond) so consuming control loops (e.g., a braking controller) can rely on a predictable sample rate, not just a fast average. |
| **Bandwidth utilization** | Classic CAN bus utilization should stay under ~70-80% sustained load in the worst case to preserve headroom for priority arbitration to actually work (a saturated bus starves low-priority traffic and risks unpredictable queuing delay even for medium-priority messages). |
| **Reliability / safety** | Functional safety alignment (ISO 26262) for ASIL-B/C/D signal paths: error detection (CRC per frame), fault confinement (bus-off isolation of a misbehaving node), and redundancy where required (e.g., dual-path delivery for the most critical braking signals). |
| **Fault isolation** | A single faulty ECU (e.g., stuck-transmitting, "babbling idiot" fault) must not be able to degrade or halt communication for the rest of its domain, let alone the whole vehicle — enforced via bus-off / fault confinement at the protocol level and domain segmentation at the architecture level. |
| **Scalability (engineering, not just runtime)** | Support 60-100+ ECUs and 1,500-3,000+ signals across the platform without a redesign; adding a new ECU to a domain should be a bounded, local integration effort. |
| **Bandwidth headroom for growth** | Zonal Ethernet backbone should be provisioned with significant headroom (design target: <30-40% utilization at launch) since ADAS/sensor fusion bandwidth needs grow substantially across a vehicle's model lifecycle (new camera/radar/lidar generations). |
| **Security** | Frames should not be trivially spoofable by an unauthorized or compromised ECU on the same bus; at minimum, gateway-enforced filtering of which domains can originate which message IDs, plus (on newer platforms) message authentication for the highest-risk safety signals. |
| **Diagnosability** | Standard diagnostic protocols (e.g., UDS over CAN or Ethernet) must be supported without contending with real-time traffic for arbitration priority — typically via lower-priority message IDs or a separate diagnostic-only channel. |

Call out explicitly to the interviewer: *"This is a fundamentally different NFR profile from a typical distributed system — we're not optimizing for throughput or eventual consistency, we're optimizing for provable worst-case latency bounds on a shared, extremely bandwidth-constrained medium, with hard safety consequences for getting it wrong. Every design choice below should be justifiable in terms of its effect on worst-case latency and fault containment, not just average-case performance."*

---

## 3. Back-of-the-Envelope Capacity Estimation

- **Bus bandwidth (classic CAN):** ~1 Mbps raw bit rate on a classic high-speed CAN bus (typical for powertrain/chassis domains). CAN-FD (flexible data rate), used on newer platforms, extends the data phase to 2-8 Mbps while keeping arbitration at the classic 1 Mbps rate — we'll reason with classic CAN numbers first since the arithmetic is cleaner, then note CAN-FD relaxes it.
- **Frame overhead:** a classic CAN data frame carries up to 8 bytes of payload but has substantial overhead — ID (11 or 29 bits), control/CRC/ACK/stuffing bits — a typical 8-byte-payload frame is roughly ~110-130 bits on the wire including worst-case bit-stuffing. Round to **~120 bits/frame** for estimation.
- **Max frame rate on one bus:** `1,000,000 bps / 120 bits/frame ≈ 8,300 frames/sec` theoretical ceiling on a single classic CAN bus at 100% utilization (never actually run this high — see the utilization NFR above).
- **Realistic signal load on one domain bus:** assume a chassis/safety domain bus carries ~40-60 distinct message IDs, with the fastest-changing ones (wheel speed, steering angle, yaw rate) transmitted every **10 ms** (100 Hz) and slower ones (door status, seat position on a body bus) every 100-1000ms. A reasonable weighted estimate: ~30 "fast" messages at 100 Hz + ~30 "slow" messages at ~5-10 Hz.
  `Fast: 30 messages × 100/sec × 120 bits ≈ 360,000 bps`
  `Slow: 30 messages × 8/sec × 120 bits ≈ 28,800 bps`
  `Total ≈ 389,000 bps ≈ 39% bus utilization` on a 1 Mbps bus — comfortably under the 70-80% target, leaving headroom for arbitration losers (lower-priority messages) to still get bounded worst-case delay, and for bursts (e.g., diagnostic requests, transient event messages like a fault code).
- **Worst-case latency for the highest-priority message:** in CAN's non-destructive bitwise arbitration, the highest-priority message (lowest ID) *always* wins arbitration immediately when it wants to transmit — its worst-case latency is bounded by, at most, the transmission time of one lower-priority frame already in flight (arbitration is decided bit-by-bit during the ID field itself, so a higher-priority frame can only ever be blocked by a frame *already transmitting*, never queued behind one that hasn't started). At ~120 bits and 1 Mbps, that's a worst-case blocking time of **~120 microseconds** for the top-priority message — this is the core mathematical argument for why CAN's priority scheme gives near-deterministic guarantees for the most critical signal, and it's worth stating explicitly in the interview.
- **Scaling to zonal Ethernet backbone:** modern platforms move high-bandwidth domains (ADAS camera/radar/lidar fusion, high-resolution displays) to 100 Mbps-1 Gbps Automotive Ethernet. A single forward-facing camera alone can produce tens to hundreds of Mbps of raw or lightly-compressed video; a sensor-fusion domain controller aggregating 5-8 cameras plus radar/lidar easily justifies a dedicated ~1 Gbps segment — three orders of magnitude beyond what CAN could ever carry, which is *why* the industry is moving perception/ADAS traffic off CAN entirely rather than trying to scale CAN itself.
- **ECU/domain count:** ~60-100 ECUs distributed across, say, 4-6 domains (powertrain, chassis/safety, body, infotainment/HMI, ADAS/perception, and a zonal aggregation layer) — each domain's local bus stays well within its own bandwidth budget, and only the (much smaller) set of signals that must cross domains adds load to the central Ethernet backbone via gateways.

Conclusion to state out loud: *"The headline number isn't a huge one — a modern car's internal network moves nowhere near the data volume of, say, its own cloud telemetry link. The real engineering constraint is that a handful of kilobits per second of the *wrong* signal delayed by milliseconds is a safety incident, so the entire design is organized around provable worst-case bounds and fault containment on a deliberately narrow, shared medium — not around maximizing throughput."*

---

## 4. Message / Frame Format Design

Given the low-level networking nature of this prompt, the core "data model" is the wire frame format and the signal-packing convention layered on top of it, rather than a database schema.

### CAN data frame (classic CAN, 11-bit standard identifier shown; 29-bit extended ID variant exists for more ID space)

```
┌───────────┬─────┬─────┬──────┬──────────────────┬─────┬─────┬─────┐
│ Identifier│ RTR │ IDE │ DLC  │   Data (0-8 bytes) │ CRC │ ACK │ EOF │
│  (11 bit) │ (1) │ (1) │(4bit)│                      │(15b)│ (2) │ (7) │
└───────────┴─────┴─────┴──────┴──────────────────┴─────┴─────┴─────┘
```
```
identifier          -- lower numeric value = higher priority (arbitration field)
rtr                 -- remote transmission request bit (data frame vs. remote/request frame)
ide                 -- identifier extension bit (standard 11-bit vs. extended 29-bit ID)
dlc                 -- data length code, 0-8 (classic CAN) / 0-64 (CAN-FD)
data                -- up to 8 bytes, densely packed with multiple signals (see DBC below)
crc                 -- 15-bit CRC for frame integrity
ack                 -- acknowledgment slot, any receiving node can assert
eof                 -- end-of-frame marker
```
The **identifier doubles as the priority key**: during arbitration, every node wanting to transmit puts its ID on the bus bit-by-bit; a node sending a recessive bit (1) while another sends a dominant bit (0) at the same position loses arbitration immediately and silently backs off to retry after the winning frame completes — this is CAN's defining mechanism and requires zero central arbiter, no negotiation round-trip, and no wasted bandwidth from collisions (unlike, say, classic Ethernet CSMA/CD).

### DBC-style signal definition (how multiple signals pack into one frame's data bytes)

```
BO_ 100 BRAKE_STATUS: 8 Vector__XXX          -- message ID 0x064 (100 decimal), 8-byte payload
 SG_ BrakePedalPosition : 0|10@1+ (0.1,0)   [0|100]   "%"      ADAS_ECU,ESC_ECU
 SG_ BrakePressureFront : 10|12@1+ (0.05,0) [0|200]   "bar"    ESC_ECU
 SG_ BrakePressureRear  : 22|12@1+ (0.05,0) [0|200]   "bar"    ESC_ECU
 SG_ BrakeSwitchActive  : 34|1@1+  (1,0)    [0|1]     ""       ADAS_ECU,BCM
 SG_ ABSFaultFlag       : 35|1@1+  (1,0)    [0|1]     ""       ESC_ECU,Instrument_Cluster
```
```
message_id                -- 0x064; also encodes priority via arbitration
signal_name
start_bit, bit_length     -- exact bit position/width within the 8-byte payload
byte_order                 -- @1 = little-endian (Intel), @0 = big-endian (Motorola)
scale, offset               -- raw integer value → physical unit: physical = raw*scale + offset
min, max, unit
receiver_ecus               -- which ECUs on the bus are expected to consume this signal
```
This is the **classic DBC (CAN database) convention**: rather than one signal per frame (wasteful given the fixed per-frame overhead computed in the estimation section), related signals that change together and share consumers are packed bit-for-bit into a shared frame. This is a direct, deliberate trade-off of message-definition complexity (a shared frame format must be agreed upon and versioned across every producing/consuming ECU) for bandwidth efficiency and fewer arbitration events — critical given the ~1 Mbps ceiling.

### Automotive Ethernet frame (zonal/domain-controller backbone, simplified)

```
ethernet_header             -- standard 802.3 MAC framing (source/dest MAC, EtherType)
vlan_tag (802.1Q)            -- domain/priority segmentation across the shared switched backbone
  pcp (3 bits)                -- priority code point, maps to a traffic class (TSN-style)
avb_tsn_scheduling_metadata  -- for time-sensitive streams: talker/listener stream reservation,
                              -- credit-based shaping or time-aware shaper gate schedule
payload                       -- e.g., SOME/IP service-oriented payload, or tunneled/gatewayed
                              -- CAN frames (CAN-over-Ethernet for legacy signal bridging)
```
Automotive Ethernet doesn't have CAN's built-in bitwise-priority arbitration (it's a switched, full-duplex medium, not a shared broadcast bus in the same sense) — priority and determinism instead come from **Time-Sensitive Networking (TSN)** standards layered on top: VLAN priority tagging (802.1Q), time-aware traffic shaping (802.1Qbv gate schedules that reserve specific time slots for specific traffic classes on each switch port), and stream reservation protocols that pre-allocate bandwidth for known periodic flows before they start — conceptually the Ethernet-world equivalent of CAN's arbitration-by-ID, but achieved through switch configuration and time-slicing rather than physical bus contention.

### Why keep classic CAN's format for existing domains rather than migrating everything to Ethernet immediately?

Narrate this trade-off explicitly: *"CAN's simplicity and its physics-based, zero-overhead priority arbitration are genuinely hard to beat for low-bandwidth, extremely cost-sensitive, safety-critical signals — a $2 CAN transceiver on a door-lock ECU doesn't need a switch port, a MAC address, or TSN configuration. The industry's actual trajectory (and what I'd propose here) isn't 'replace CAN with Ethernet everywhere,' it's a hybrid: keep CAN/CAN-FD within cost- and bandwidth-appropriate domains, and use Ethernet as the high-bandwidth backbone connecting domain/zonal controllers, with gateways translating between the two where signals need to cross that boundary."*

---

## 5. High-Level Design

This is an **infrastructure/topology view** of the in-vehicle network — what physical/logical pieces of infrastructure exist, what type each one is (a shared deterministic bus, a protocol-translating gateway, a TSN-scheduled backbone...), and how they're wired together — not a step-by-step trace of one signal's journey from producer to consumer. Sequencing, arbitration mechanics, and per-hop logic belong in the Deep Dives (§6); this section should stand on its own as "here's what topology we'd wire into the vehicle."

### Infrastructure tiers

**Producing/consuming ECU tier (physically distinct per domain, not a cloud-style service)**
- **Chassis/Safety Domain ECUs** — Brake ECU, Steering ECU, ESC/ABS; the highest-priority, hardest-real-time producers and consumers on the network.
- **Powertrain Domain ECUs** — Motor Controller, BMS.
- **Body/Comfort Domain ECUs** — Door, Seat, HVAC controllers; lowest-criticality, highest ECU count.
- **ADAS / Perception Domain Controller** — a special case in this tier: aggregates high-bandwidth camera/radar/lidar data over dedicated Ethernet links, fuses it locally, and only publishes much lower-bandwidth *derived* signals (e.g., "object at bearing X, distance Y") onto the shared backbone.

**In-vehicle network/bus tier (the physical medium itself — deterministic, not a general-purpose network)**
- **Per-domain CAN/CAN-FD buses** — a shared, bandwidth-constrained, hardware-arbitrated medium local to each domain (Safety/Chassis, Powertrain, Body/Comfort each get their own).
- **Domain Gateway / Zonal Controller** — sits at each domain's boundary; the *only* path a signal can take to leave its domain, enforced by a static, pre-certified signal-routing table (a control-plane artifact that's part of the vehicle's safety case, not just wiring); performs CAN ↔ Ethernet protocol translation.
- **Central Automotive Ethernet Backbone (TSN)** — the shared, higher-bandwidth spine joining every domain gateway and the ADAS controller; uses VLAN priority tagging and time-aware shaping (802.1Qbv) in place of CAN's bitwise arbitration to give bounded-latency guarantees to specific traffic classes.

**Diagnostic/logging tap (side-car, non-critical, off the main data path)**
- **Diagnostic/Service Access Point** — standardized diagnostic access (UDS) for factory/service tools; arbitrated at the lowest priority so it can never contend with real-time safety traffic. It taps signals for read access; it is not a participant in the main producer→consumer signal flow.

**Bridge to external systems**
- **Connectivity Gateway ECU** — the single, deliberately narrow, rate-limited, mostly-read-only bridge point to the vehicle-to-cloud connectivity layer (an external system — see the companion design); architecturally incapable of injecting arbitrary traffic back onto the safety-critical domains.

### Topology diagram (infrastructure view, described in ASCII)

```
 PRODUCING/CONSUMING ECU TIER (per domain, physically separate)
 ┌───────────────────────┐   ┌───────────────────────┐   ┌───────────────────────┐
 │ Chassis/Safety Domain  │   │ Powertrain Domain      │   │ Body/Comfort Domain    │
 │ Brake, Steering,       │   │ Motor Ctrl, BMS        │   │ Door, Seat, HVAC ECUs  │
 │ ESC/ABS                │   │                        │   │                        │
 └───────────┬────────────┘   └───────────┬────────────┘   └───────────┬────────────┘
             │ per-domain CAN/CAN-FD bus   │ per-domain CAN/CAN-FD bus  │ per-domain CAN/CAN-FD bus
             ▼                             ▼                            ▼
 IN-VEHICLE NETWORK/BUS TIER
 ┌────────────────────┐        ┌────────────────────┐        ┌────────────────────┐
 │ Domain Gateway A     │        │ Domain Gateway B     │        │ Domain Gateway C     │
 │ (CAN ↔ Ethernet,      │        │ (CAN ↔ Ethernet,      │        │ (CAN ↔ Ethernet,      │
 │  static routing table)│        │  static routing table)│        │  static routing table)│
 └──────────┬────────────┘        └──────────┬────────────┘        └──────────┬────────────┘
            │                                  │                               │
            └──────────────────┬───────────────┴───────────────┬───────────────┘
                                ▼                                ▼
                  ┌─────────────────────────────────────────────────────┐
                  │      Central Automotive Ethernet Backbone (TSN)        │
                  │  the shared spine every domain gateway attaches to —   │
                  │  VLAN/priority-tagged, time-aware shaped traffic       │
                  └───────┬─────────────────────────────────┬───────────────┘
                          │                                   │
                          ▼                                   ▼
             ┌────────────────────────┐          ┌──────────────────────────┐
             │ ADAS / Perception       │          │ Connectivity Gateway ECU  │
             │ Domain Controller        │          │ — BRIDGE TIER             │
             │ (cameras/radar/lidar →   │          │ (narrow, rate-limited,     │
             │  fused derived signals)  │          │  mostly-read-only)         │
             └────────────────────────┘          └─────────────┬─────────────┘
                                                                 ▼
                                                  (out of scope: vehicle-to-cloud
                                                   connectivity layer — external
                                                   system, see companion doc)

 DIAGNOSTIC/LOGGING TAP (side-car, off the main path, attaches to any domain bus):
   • Diagnostic/Service Access Point — lowest-priority UDS read access for factory/service tools
```

Narrate the key architectural decision: *"There's no single shared bus for the whole vehicle — that's the point. Each domain keeps its own local CAN bus with its own priority space and its own fault domain, so a babbling body-control ECU can bus-off itself and take down, at worst, the body domain, never chassis/safety. The one piece of shared infrastructure everything hangs off is the Central Ethernet Backbone, and it's reached only through domain gateways enforcing a static, pre-certified routing table — never a raw, unfiltered relay. The diagnostic tap and the Connectivity Gateway ECU are both deliberately drawn off to the side rather than in the main producer-to-consumer path: one is a lowest-priority read-only tool interface, the other is a narrow, mostly-read-only bridge to an entirely separate external system with its own, much looser latency and consistency constraints."*

---

## 6. Detailed Design / Deep Dives

Pick 2-3 of these based on interviewer interest — you won't have time for all of them in 45 minutes, so ask: *"Which of these would you like me to go deeper on: CAN's arbitration mechanism, time-triggered vs. event-triggered scheduling, the gateway/domain-bridging architecture, or bandwidth/utilization analysis?"*

### 6.1 Message-ID-based priority arbitration (non-destructive bitwise arbitration)

- Every CAN frame's identifier field doubles as its priority: **numerically lower ID = higher priority**. Safety-critical signals (brake, steering) are assigned the lowest available IDs on their domain bus; diagnostics and infrequent status messages get the highest (lowest-priority) IDs.
- **Mechanism:** CAN uses "wired-AND" physical signaling — a dominant bit (logical 0) always overpowers a recessive bit (logical 1) when both are driven simultaneously. During arbitration, every transmitting node writes its ID bit-by-bit while simultaneously reading the bus; if a node writes recessive but reads dominant (meaning some other node is transmitting a lower/higher-priority... specifically a dominant bit where it sent recessive), it immediately knows it lost arbitration and stops transmitting, silently retrying after the current frame completes. The winning node never even notices a collision occurred — this is what "non-destructive" means, contrasted with, say, classic Ethernet's CSMA/CD, where a genuine electrical collision occurs and both frames are destroyed and must be retransmitted.
- **Why this matters for determinism:** because arbitration is resolved *before* any data is transmitted (during the ID field itself) and takes a bounded, fixed number of bit-times, the worst-case delay for the highest-priority message is simply "wait for whatever lower-priority frame happened to already be transmitting" — never "wait behind an arbitrary queue of higher-priority traffic," because by definition nothing has higher priority. This is the basis for the ~120 microsecond worst-case bound computed in the estimation section, and it's a genuinely elegant, hardware-level solution to a problem that costs a lot of engineering effort to approximate in software-arbitrated systems.
- **Practical ID assignment discipline:** ID allocation across the fleet's signal database is itself a governed process — a new supplier's ECU can't just pick any ID; it's assigned based on its signal's actual criticality/timing requirement, and changing an ID later is a breaking change requiring re-validation of every consuming ECU's expectations, which is worth flagging as a real-world process constraint, not just a technical one.

### 6.2 Deterministic scheduling: time-triggered vs. event-triggered messaging

- **Event-triggered (standard CAN arbitration, described above):** a node transmits when it has new data and wins arbitration. Simple, flexible, bandwidth-efficient (no bus time consumed when there's nothing to say), and sufficient for the vast majority of signals — but worst-case latency for a given message technically depends on bus load and what else happens to be contending at that instant, even though we showed the *top*-priority message's bound is very tight.
- **Time-triggered (e.g., TTCAN, or the TSN time-aware shaper concept on Ethernet):** the bus schedule is divided into a repeating time cycle with pre-allocated slots for specific messages, coordinated by a synchronized global time base (a reference clock broadcast periodically). A message assigned to a slot transmits in that slot, period — no arbitration contention at all for anything in a reserved slot, giving extremely tight, provable jitter bounds independent of what other traffic exists.
- **Why not make everything time-triggered?** Time-triggered scheduling requires knowing, ahead of time, exactly which signals need which slots at design time — it's far less flexible for infrequent, sporadic, or genuinely event-driven signals (e.g., a fault code that occurs rarely and unpredictably) and wastes bus time reserving slots for messages that mostly have nothing to say. The practical answer used across the industry (and worth stating explicitly): a **hybrid** — reserve time-triggered slots only for the small set of hardest-real-time, tightest-jitter periodic signals (e.g., the core braking control loop's sensor feedback, often literally on a dedicated bus or dedicated Ethernet TSN stream), and leave everything else on standard event-triggered priority arbitration, which is already extremely good for the general case per the arbitration analysis above.
- **TSN equivalent on the Ethernet backbone:** IEEE 802.1Qbv (time-aware shaper) implements essentially the same idea for switched Ethernet — each switch port has a repeating gate-control schedule that opens/closes per traffic class at precise times, giving time-triggered-style guarantees to specific high-priority streams (e.g., a safety signal bridged from a CAN domain onto the backbone) even though the underlying medium is a shared, switched network rather than a single electrical bus.

### 6.3 Gateway / domain-controller architecture and cross-domain signal bridging

- Each domain gateway holds a **static, pre-certified signal-routing table**: "relay message ID 0x064 (BRAKE_STATUS) from the chassis bus onto the backbone, tagged for consumption by the ADAS domain controller and the connectivity gateway" — this table is part of the vehicle's safety case and changes go through the same validation rigor as any other safety-relevant configuration, not an ad-hoc runtime routing decision.
- **Protocol translation responsibilities:** converting a CAN frame's raw bytes into whatever the Ethernet backbone's payload convention is (e.g., a SOME/IP service event, or a simple CAN-frame-over-Ethernet tunnel for the simplest case), preserving or re-deriving priority semantics (mapping CAN ID priority onto an Ethernet VLAN priority tag / TSN traffic class), and enforcing rate limits so a burst on one side can't overwhelm the other.
- **Fault containment at the gateway boundary:** the gateway is also the natural enforcement point for "this domain should never be able to inject traffic outside its certified signal set" — even a fully compromised body-domain ECU flooding its local bus can only affect that local bus and whatever narrow, pre-defined set of signals the gateway was already relaying; it cannot suddenly start injecting arbitrary new message IDs onto the backbone or another domain's bus.
- **Why not a single flat network for everything?** A flat, single-bus (or single flat switched network) design would mean every ECU's traffic — from a door-lock status to a braking signal — contends for the same shared resource and the same fault domain; a single misbehaving low-criticality ECU could then directly degrade a safety-critical signal's worst-case latency or, worse, its availability. Domain segmentation with governed gateway bridging is what makes the safety-critical domain's guarantees provable independent of everything else in the vehicle.

### 6.4 Bandwidth constraint management and utilization headroom

- As computed in the estimation section, keeping steady-state bus utilization around ~40% (well under the ~70-80% ceiling) is deliberate: CAN's arbitration guarantees are about *who wins when there's contention*, not about eliminating queuing delay for lower-priority messages entirely — as utilization climbs, lower-priority messages can experience increasing worst-case queuing delay (priority inversion-like buildup), so utilization headroom is itself a latency-bound-preserving design parameter, not just a "nice to have" margin.
- **CAN-FD as a relief valve for existing domains:** where a domain's bandwidth needs grow beyond what classic CAN comfortably provides, CAN-FD raises the data-phase bit rate (up to 8 Mbps) and payload size (up to 64 bytes) while keeping the same arbitration mechanism and physical bus topology — a lower-disruption upgrade path than jumping straight to Ethernet for domains that don't need Ethernet's raw bandwidth.
- **Moving genuinely high-bandwidth traffic (ADAS sensor fusion, camera feeds) off CAN entirely** rather than trying to force-fit it: a single camera can dwarf an entire CAN bus's total capacity, so this traffic is architected from the start to live on dedicated Ethernet links to the perception domain controller, which performs fusion locally and only publishes much smaller, derived signals (e.g., "object at bearing X, distance Y") onto the shared backbone — keeping the shared/bridged traffic volume manageable.

### 6.5 Relationship to the vehicle-to-cloud connectivity layer (bridge point, not shared concerns)

- The Connectivity Gateway ECU is the *only* component in this design that talks to the vehicle-to-cloud layer, and it does so as a **consumer** of a curated, sampled, rate-limited signal subset off the Ethernet backbone — never as a raw tap into a safety-critical CAN domain, and never with a return path that can inject arbitrary commands back onto those domains.
- This is a deliberate architectural boundary, not just an implementation detail: the cloud-facing side operates under a completely different set of constraints (intermittent connectivity, store-and-forward, eventual consistency, minutes-to-hours acceptable latency, as covered in the companion vehicle-to-cloud design) that must never be allowed to leak backward and affect the hard real-time, deterministic guarantees inside the vehicle. A cellular dead zone, a cloud outage, or a backpressure signal from the connectivity layer should have precisely zero effect on braking or steering signal latency.
- Any command path that *does* need to go from cloud to a vehicle-internal actuator (e.g., a remote-start command, or — in the OTA design — flashing an ECU) is treated as its own carefully gated, authenticated, rate-limited flow through this same narrow gateway boundary, with the gateway enforcing that such commands can only ever land in appropriately non-safety-critical domains or through an explicit, validated OTA/diagnostic-mode pathway — never as an unmediated write onto the live chassis/safety bus during normal driving.

---

## 7. Minimal API Surface (illustrative)

Note this "API" is really a signal-database and configuration surface (DBC-style definitions plus gateway routing tables), since ECUs communicate via broadcast frames rather than request/response calls.

```
# Signal database (build-time / configuration-time interface, not a runtime API)
DEFINE_MESSAGE   { message_id, dlc, transmitting_ecu, bus_domain, cycle_time_ms? }
DEFINE_SIGNAL    { message_id, signal_name, start_bit, bit_length, byte_order,
                   scale, offset, min, max, unit, receiver_ecus[] }

# Gateway routing table (per domain gateway, also configuration-time / part of the safety case)
ROUTE_RULE       { source_domain, message_id, destination_domain_or_backbone,
                   rate_limit_hz?, priority_class_on_destination }

# Runtime diagnostic/introspection interface (lowest arbitration priority)
UDS_READ_DATA_BY_ID    { ecu_address, data_identifier }  → current signal value + timestamp
UDS_READ_DTC            { ecu_address }                   → active/stored diagnostic trouble codes

# Connectivity Gateway's outward-facing interface (consumed by the vehicle-to-cloud layer)
GET  /internal/signals/{signal_name}/latest     → sampled, rate-limited current value
                                                    (never the raw, full-rate bus stream)
```

---

## 8. Trade-offs and Alternatives Considered

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| Bus topology for cost-sensitive domains | Classic CAN/CAN-FD shared bus per domain | Point-to-point Ethernet to every ECU | CAN transceivers are far cheaper and simpler for low-bandwidth signals; a full Ethernet switch fabric to every door-lock ECU is unjustified cost/complexity given the bandwidth those signals actually need. |
| Priority mechanism | Non-destructive bitwise arbitration via message ID | Centralized/software-scheduled bus arbiter | Arbitration is resolved in hardware, in bounded time, with zero central point of failure and no negotiation round-trip — strictly better for the hard-real-time case than any software arbiter that itself introduces latency and a single point of failure. |
| Scheduling model | Hybrid: time-triggered slots for the hardest-real-time signals, event-triggered priority arbitration for everything else | Fully time-triggered (TTCAN-style) for all traffic | Fully time-triggered wastes bandwidth reserving slots for sporadic/infrequent signals and is inflexible to add new signals later; a hybrid gets tight guarantees where they matter most without sacrificing the flexibility event-triggered arbitration provides elsewhere. |
| Network segmentation | Domain-partitioned buses joined by governed gateways | One flat shared network for the whole vehicle | A flat network means a single misbehaving low-criticality ECU can degrade or endanger safety-critical signal delivery; domain segmentation makes the safety-critical domain's worst-case guarantees provable independent of everything else. |
| High-bandwidth sensor traffic (ADAS) | Dedicated Ethernet links to a perception domain controller; only derived/fused signals cross onto the shared backbone | Force camera/radar/lidar traffic onto CAN/CAN-FD | CAN/CAN-FD bandwidth (1-8 Mbps) is orders of magnitude below what raw sensor data requires; attempting it would either be infeasible or would consume the entire bus, starving every other signal. |
| Cloud/telemetry bridging | Single narrow, rate-limited, read-mostly Connectivity Gateway ECU | Direct access from the vehicle-to-cloud layer into CAN domains | Keeps the hard real-time, safety-critical internal network's guarantees completely decoupled from the very different (intermittent, eventually-consistent) constraints of the cloud-facing layer; also closes off a large potential attack surface. |

---

## 9. Failure Modes & Edge Cases to Call Out Proactively

- **"Babbling idiot" ECU (stuck transmitting, or transmitting garbage at high rate):** CAN's built-in fault-confinement state machine (error-active → error-passive → bus-off) automatically disconnects a node whose error rate crosses a threshold, preventing it from monopolizing or corrupting the bus for everyone else; this must be paired with domain segmentation so even a bus-off event's transient disruption is contained to one domain.
- **Bus saturation from an unexpected traffic burst (e.g., many ECUs simultaneously reporting a fault after a shared upstream event):** even with priority arbitration protecting the *highest*-priority message, sustained near-100% utilization increases worst-case latency for medium/low-priority messages — mitigated by keeping steady-state headroom (per the ~40% utilization target) and by rate-limiting/debouncing fault-reporting logic at the source rather than letting every ECU report on every cycle.
- **Clock/time-base drift for time-triggered segments:** a time-triggered schedule depends on a synchronized global time reference; a drifting or lost time-sync source degrades to worse-than-event-triggered behavior if not detected — requires a monitored, redundant time-sync source (and a defined fallback to event-triggered behavior) for any domain relying on time-triggered scheduling.
- **Gateway misconfiguration or a stale routing table** (e.g., a signal that should have been added to the cross-domain relay list after a design change, but wasn't) — silently drops a signal that a downstream domain expected, potentially without any error indication; mitigated by treating the routing table as a certified, versioned artifact validated alongside the signal database, with automated consistency checks (does every signal a domain expects to receive actually have a corresponding route rule?) as part of the build/release process, not a runtime discovery mechanism.
- **A new ECU or supplier component with a subtly incorrect signal-packing implementation** (wrong bit offset, wrong scale/offset, wrong byte order) — produces a frame that's structurally valid CAN but semantically wrong; caught via integration testing against the shared DBC signal database, not something the network layer itself can detect at runtime (this is a strong argument for rigorous, automated DBC-conformance testing in the ECU validation pipeline).
- **Connectivity Gateway compromised or malfunctioning:** because it's architected as a narrow, mostly read-only bridge with no direct write path to safety-critical domains, the blast radius of a compromised gateway is limited to whatever curated data it forwards outward and whatever explicitly-gated, validated command types it's allowed to relay inward (e.g., a diagnostic/OTA-mode command, itself subject to its own authentication) — never an unmediated path onto the live chassis bus.
- **Legacy domain (older CAN-based subsystem) that can't be re-validated/re-certified for a new signal or ID change:** a real-world constraint worth naming — sometimes the pragmatic answer is a compatibility shim at the domain gateway (translating between an old signal definition and a new one) rather than forcing every legacy ECU through a costly re-certification cycle.

---

## 10. Monitoring, Observability, and Security (brief)

- **Diagnostics/telemetry:** per-domain bus utilization, per-message-ID observed latency/jitter (sampled, compared against the certified worst-case bound), error-frame counters and bus-off events per ECU — surfaced both to factory/service diagnostic tools (via UDS) and, in curated/sampled form, to the cloud-facing telemetry pipeline via the Connectivity Gateway.
- **Alerting (in-vehicle and fleet-level):** an ECU trending toward bus-off (rising error-passive rate) should be flagged for service before it actually disconnects; fleet-level aggregation of bus-off events across many vehicles can surface a systemic issue (e.g., a specific ECU hardware batch or software version with a wiring/EMI susceptibility) faster than any single vehicle's local diagnostics would.
- **Security:** gateway-enforced allow-listing of which domains/ECUs may originate which message IDs (prevents a compromised low-criticality ECU from spoofing a high-priority safety signal's ID); message authentication codes for the highest-risk signals on newer platforms (mitigating spoofing even from a physically-connected malicious device, at the cost of some computational overhead on constrained ECUs); physical/architectural isolation of any external-facing interface (OBD-II port, connectivity gateway) from direct access to the safety-critical bus.
- **Functional safety process note:** unlike a typical software system, changes to message IDs, signal definitions, or gateway routing rules here go through a formal safety-case review (ISO 26262) — this is worth mentioning explicitly as a real organizational/process constraint that shapes how "agile" this particular subsystem's evolution can realistically be compared to, say, a cloud backend service.

---

## 11. Wrap-up / How to Close the Interview

Summarize in 30 seconds: *"We segmented the vehicle's internal network into domains by criticality and bandwidth need — cost-sensitive, low-bandwidth signals stay on classic CAN/CAN-FD, using its hardware-level, non-destructive priority arbitration to give the highest-criticality signals a provable, near-deterministic worst-case latency bound with zero central point of failure. High-bandwidth sensor/perception traffic lives on dedicated Ethernet links instead of being force-fit onto CAN. Domains are joined by governed gateways that relay only a certified, static set of signals, which contains faults and keeps each domain's guarantees provable independent of the others. And critically, the vehicle-to-cloud connectivity layer only ever touches this network through one narrow, rate-limited, mostly-read-only gateway — the hard real-time internal network and the intermittent, eventually-consistent cloud layer are architecturally separate systems that happen to share one bridge point, not one unified network with two use cases."*

Then proactively offer a couple of extension directions, showing you know where the design could go next:
- How would this design evolve for a fully centralized "vehicle computer" architecture (a small number of very powerful zonal controllers, with most legacy ECU functions consolidated into software) — does CAN's role shrink to just the lowest-cost sensor/actuator edges, with everything else moving to Ethernet/TSN?
- How would you extend fault tolerance for the very highest ASIL signals (e.g., steer-by-wire with no mechanical backup) — dual/redundant physical bus paths, voting logic across redundant sensors, and how does that interact with the priority/arbitration scheme?
- How would you validate, before shipping, that the certified worst-case latency bounds actually hold under real-world conditions (EMI, temperature extremes, aging connectors) rather than just in a clean bench/simulation environment?

---

## 12. Follow-up Questions Interviewers May Ask

- "Walk me through exactly what happens, bit by bit, when two ECUs start transmitting frames with different IDs at the exact same time."
- "Why does CAN-FD keep the same arbitration bit rate as classic CAN even though it speeds up the data phase — what would break if arbitration itself ran faster?"
- "How would you detect, at design time, whether a proposed set of message cycle times and priorities will actually meet a given signal's worst-case latency requirement, before you ever build hardware?"
- "If you had to add a brand-new, very high-priority safety signal to an already-deployed vehicle platform via an OTA software update, what would you need to verify before allowing that ID to actually be used on the live bus?"
- "How does Time-Sensitive Networking's time-aware shaper actually guarantee a bounded-latency slot for a stream when the underlying switches are also carrying ordinary best-effort traffic?"
- "What's your argument for why a compromised infotainment ECU on the body/comfort domain can't be used to inject a malicious signal onto the chassis/safety domain?"
- "How would bandwidth and latency requirements change this design for a heavy-duty or autonomous-focused platform with many more cameras/lidars than a typical passenger EV?"

---

## References

- Rivian system design round context: see [`../rivian/index.md`](../rivian/index.md), section "System Design Interview Questions."
- This is an in-vehicle, hard-real-time system, architecturally distinct from the [vehicle-to-cloud connectivity layer](./vehicle-to-cloud-connectivity-layer.md) design — the two meet only at the Connectivity Gateway ECU bridge point described in section 6.5 above, and are otherwise governed by very different constraints (deterministic/bounded latency here vs. offline-tolerant/eventually-consistent there).
