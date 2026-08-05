# System Design Mock Interview: Real-Time Navigation with Traffic and Charging Station Data

**Company theme:** Rivian-style (vehicle/EV), also broadly applicable to Tesla, Google Maps/Waze-for-EVs, or any connected-vehicle navigation provider.
**Round:** System Design (45-60 min onsite loop)
**Interviewer expectation:** Structured problem-solving, not a specific tech stack. Clarify → requirements → estimate → high-level → deep dive → trade-offs → wrap-up.

This document is written as a self-contained interview walkthrough: it includes the clarifying questions you should ask, a model answer for each section, and the follow-up probes an interviewer is likely to throw at you. It assumes charging-station availability is supplied by a separate system — see [`./charging-station-availability-reservation-network.md`](./charging-station-availability-reservation-network.md) for that design — and focuses in depth on what's distinctive to routing and navigation itself: road-graph representation, precomputed shortest-path structures, live traffic fusion, on-vehicle caching, incremental re-routing, and EV-specific range-aware routing.

---

## 0. Opening: Clarify the Problem (first 3-5 minutes)

Don't start designing immediately. Restate the prompt and ask clarifying questions to narrow scope. Sample dialogue:

> **You:** "Before I dive in — should I assume we own the base map/road-graph data ourselves, or are we licensing that from a provider (e.g., HERE, TomTom) and focusing on the routing engine, traffic fusion, and EV-specific logic on top of it?"
>
> **Interviewer:** "Assume base map data is licensed from a third party and refreshed periodically. Focus on the routing/traffic/charging integration layer."
>
> **You:** "Understood. A few more:
> 1. Is charging-stop insertion in scope, or should I treat 'is there enough range' as someone else's problem and just consume a charging-availability API?
> 2. What's the latency budget — is this turn-by-turn in-vehicle nav (needs sub-second updates) or a trip-planning tool (can tolerate a few seconds)?
> 3. How fresh does traffic data need to be, and where does it come from — our own fleet's GPS traces, a third-party feed, or both?
> 4. Should the vehicle be able to navigate at all with zero connectivity (e.g., in a tunnel or dead zone), or is that out of scope?
> 5. What's the fleet/query scale — how many vehicles are actively navigating concurrently?"

Assume the interviewer answers:
- Charging-stop insertion for range-constrained EV trips is in scope and is actually the most interesting part of the problem — assume charging availability comes from the existing charging-network system (a dependency, not something to redesign here).
- Both trip planning (initial route computation, can take a couple of seconds) and turn-by-turn in-vehicle nav (must feel instantaneous, sub-second for updates) — design for both.
- Traffic comes from a mix of our own connected fleet's anonymized GPS/speed traces plus a licensed third-party traffic feed (e.g., a commercial traffic data provider); fuse both.
- Yes — the vehicle must continue to navigate through a dead zone using cached data, with graceful acceptance of staleness, consistent with the connectivity constraints emphasized throughout this interview series.
- Scale: ~2 million vehicles in the fleet, with a peak of ~10-15% actively navigating at once during commute/travel peaks.

---

## 1. Functional Requirements

State these explicitly on the whiteboard before designing anything.

1. **Route computation** — given origin, destination, and vehicle state (current charge %, vehicle range/efficiency profile), compute a route that is both efficient (time/distance) and *feasible* (reachable given current state of charge, inserting charging stops if necessary).
2. **Real-time traffic overlay** — incorporate live/near-live traffic conditions (congestion, incidents, closures) into route cost, both for the initial route and for updates during the trip.
3. **Charging-stop insertion** — for trips exceeding the vehicle's range, identify optimal charging stops along viable route corridors, factoring in charger availability/reservation state from the charging-network system, not just raw distance-to-nearest-station.
4. **Incremental re-routing** — as traffic conditions change or the driver deviates from the planned route, update guidance without a jarring full route recomputation from scratch when a smaller adjustment suffices.
5. **Turn-by-turn guidance** — low-latency, in-vehicle-rendered directions updated as the vehicle progresses along the route.
6. **Offline / degraded-connectivity continuation** — navigation must keep functioning (with progressively staler traffic data) when the vehicle loses connectivity mid-route, rather than failing or freezing.
7. **Multi-source data ingestion** — merge our own fleet-sourced traffic telemetry with third-party traffic feeds and (via the charging-network system) charging availability into one consistent view used by the routing engine.
8. **Range/reachability computation** — given current state of charge, efficiency, and terrain/weather factors, compute how far the vehicle can actually go — the foundation that charging-stop insertion is built on.
9. **Route preferences** — support common preference constraints (avoid highways/tolls, prefer scenic route, minimize charging stops vs. minimize total time) as routing-cost modifiers.

**Out of scope (state this explicitly):** the underlying base map/road-graph data collection and maintenance (assume licensed from a third-party map provider and refreshed on a regular cadence), the actual charging-station reservation/availability system (assume it's the dependency described in the referenced document), and voice/UI rendering of turn-by-turn instructions.

---

## 2. Non-Functional Requirements

| Requirement | Target / Reasoning |
|---|---|
| **Initial route computation latency** | p99 under ~2 seconds for a cross-country or multi-charging-stop trip; under ~500ms for a typical local trip — trip planning can tolerate slightly more latency than in-vehicle turn-by-turn updates. |
| **Turn-by-turn / re-route latency** | p99 under ~200-300ms for incorporating a new traffic update into guidance already in progress — this must feel instantaneous, since the driver is actively moving. |
| **Traffic data freshness** | Target under 60-90 seconds of staleness for fleet-sourced traffic on major roads; third-party feed freshness depends on the provider's SLA (commonly 2-5 minutes) — clearly distinguish and weight these two sources differently in the cost function. |
| **Availability (routing service)** | 99.9%+ for the backend routing service; but the in-vehicle client must be able to continue basic navigation using cached data even during a full backend outage — offline continuation is a hard requirement, not a nice-to-have, consistent with the fleet's core connectivity constraint. |
| **Feasibility guarantee (EV-specific)** | A computed route that includes charging stops must be reachable with extremely high confidence (>99.9% of the time it should not strand the driver) — treat "don't run out of charge" as close to a safety-adjacent guarantee, with a conservative range buffer built in. |
| **Scalability** | Support ~2M vehicles, ~200-300K concurrent active navigation sessions at peak, each potentially re-evaluating traffic-weighted routes every few seconds to minutes depending on trip progress. |
| **Map data size / precompute freshness** | Road graph refreshes (from the map provider) happen on the order of days to weeks; precomputed routing structures must be rebuildable within that cadence without disrupting live traffic (i.e., a blue-green precompute rollout, not a slow in-place mutation). |
| **Consistency of traffic view** | Eventual consistency across regions is fine (a traffic jam in Seattle doesn't need synchronized visibility with Miami), but within a single geographic routing region, traffic weights used for a single route computation should be internally consistent (not half old, half new). |

Call out explicitly to the interviewer: *"This system has two very different latency regimes living side by side — a 'few seconds is fine' trip-planning path and a 'must feel instant' turn-by-turn path — and the core technical challenge is combining a mostly-static road graph, a fast-changing traffic overlay, and a comparatively slow-changing charging-availability signal into one routing query without paying the full cost of shortest-path search from scratch every time."*

---

## 3. Back-of-the-Envelope Capacity Estimation

Doing this out loud shows quantitative rigor.

- **Road graph size:** a US-scale drivable road network has on the order of ~50-100 million road segments (edges) and a comparable number of intersections (nodes) at full fidelity; a more routing-practical simplified graph (collapsing dense local streets, keeping full fidelity on arterials/highways) is commonly modeled at **~10-20 million nodes and ~20-40 million edges** for a country-scale routing graph. At roughly 50-100 bytes/edge (endpoints, distance, speed limit, road class) that's **~1-4 GB** for the static graph alone — large, but very feasible to hold across a modestly sized cluster, and small enough that a *compressed regional subset* can live entirely on a vehicle for offline use.
- **Precomputed routing structure overhead:** contraction hierarchies or hub-labeling structures typically add roughly 1.5-3x the size of the base graph in precomputed shortcut/label data to achieve millisecond-scale shortest-path queries — call it **~5-10 GB** for a full-country precomputed structure. This is a batch-computed, periodically-refreshed artifact, not something built per-query.
- **On-vehicle cached map + routing data:** a vehicle doesn't need the whole country cached — a reasonable working set is "current region + planned route corridor + a buffer," say a few hundred MB to ~1-2 GB depending on trip length, easily fitting on modern in-vehicle storage.
- **Concurrent navigation sessions:** ~2M fleet vehicles, assume ~10-15% actively navigating at peak (commute hours) → **~200,000-300,000 concurrent sessions**.
- **Traffic update ingestion rate (fleet-sourced):** each actively-driving vehicle reports a GPS/speed sample roughly every 1-5 seconds; assume ~500,000 vehicles driving at any given moment (a superset of "actively navigating," since many drive without nav open) at 1 sample/3s average → `500,000 / 3 ≈ 165,000 samples/sec` of raw fleet telemetry feeding the traffic-fusion pipeline — a substantial but very manageable streaming ingestion rate for a Kafka-style pipeline, roughly comparable in order of magnitude to a large-scale telemetry system.
- **Route re-evaluation rate:** each of the ~250,000 concurrent sessions re-checks whether traffic conditions warrant a re-route roughly every 15-30 seconds → `250,000 / 20s ≈ 12,500 re-route-evaluations/sec` — this is the number that matters for sizing the live routing-query tier, and it's this number (not the raw telemetry ingestion) that drives how aggressively we need to precompute versus compute live.
- **Charging-stop-insertion rate:** only a minority of trips are long enough to require a charging stop — estimate ~5% of active sessions are long-haul trips needing range-aware planning → `250,000 × 0.05 ≈ 12,500` sessions needing the heavier reachability-polygon + stop-insertion computation, which is comparatively expensive (seconds, not milliseconds) but low-volume enough to run as an async enrichment rather than blocking the fast path.

Conclusion to state out loud: *"The numbers tell us three things: the static road graph and its precomputed shortest-path structure are large but batch-computable and cacheable; the live re-route evaluation rate (~12,500/sec) is what the online serving tier must be sized for, and it's an order of magnitude more frequent than the expensive charging-stop-insertion computation (~12,500 total sessions needing it at all, evaluated far less than every 20 seconds). That gap is exactly why we architect this as 'fast precomputed base routing + a cheap live traffic overlay adjustment, with an expensive EV-reachability computation invoked only when range is actually a constraint' — not as one monolithic per-query graph search."*

---

## 4. Data Model / Database Design

### Core entities

**`RoadGraphVersion`** (a versioned, immutable snapshot of the base road network)
```
graph_version_id (PK)
source_provider          -- licensed map vendor identifier
effective_from
node_count, edge_count
storage_uri               -- pointer to the serialized graph + precomputed structure
```
The road graph is versioned and immutable per release — routing queries pin to a specific `graph_version_id` for their duration so that a mid-query graph swap (during a scheduled map update) never produces an inconsistent route.

**`Edge`** (a road segment — the base unit of the graph, typically stored in a compact binary format rather than a traditional row-oriented table, but modeled here relationally for clarity)
```
edge_id (PK)
graph_version_id
from_node_id, to_node_id
distance_m
free_flow_speed_kmh        -- baseline speed with no traffic
road_class                  -- highway / arterial / local / etc.
```

**`TrafficWeight`** (the dynamic, fast-changing overlay — deliberately separate from the static `Edge` data)
```
edge_id (indexed)
region_id                    -- for partitioning/sharding
current_speed_kmh
confidence                    -- based on sample count and recency
source_mix                    -- e.g. {"fleet": 0.7, "third_party": 0.3}
updated_at
```
This is the highest-write-volume table in the system by far and is intentionally decoupled from the immutable `Edge` table — it lives in a fast, region-sharded key-value or in-memory store keyed by `edge_id`, refreshed continuously, and is *joined* against the static graph at query time rather than being part of the same storage engine. Mixing a table that changes every few seconds with one that changes every few weeks would force one storage engine to serve two incompatible access patterns.

**`Trip`** (a single navigation session)
```
trip_id (PK)
vehicle_id
origin, destination         -- lat/lon
graph_version_id             -- pinned for the duration of the trip
current_soc_pct               -- state of charge at trip start
vehicle_efficiency_profile    -- kWh/mile curve, used for range computation
computed_route_id
charging_stops                -- ordered list of station_id/connector references (from
                              --   the charging-network system) + planned arrival SOC
status                          -- PLANNING / ACTIVE / COMPLETED / ABANDONED
started_at
```

**`RouteSegmentPlan`** (the computed route, broken into segments for incremental update/patching)
```
route_id (PK)
trip_id (FK)
segment_index
edge_ids                       -- ordered list of edges comprising this segment
estimated_arrival_at_segment_end
traffic_weighted_eta_seconds
```
Breaking a route into segments (rather than one monolithic path blob) is what makes incremental re-routing cheap: when traffic changes on one segment, only that segment's ETA/path needs recomputation and patching, not the whole route.

**`ReachabilityPolygon`** (a cached, precomputed "how far can I get" shape — the EV-specific artifact)
```
trip_id (FK)
computed_at
current_soc_pct
polygon_geometry             -- serialized geo-polygon (e.g., isochrone-like reachable area)
buffer_margin_pct             -- conservative safety margin subtracted from raw range
```
Cached per active trip and recomputed opportunistically (SOC changes materially, or terrain/weather updates the efficiency model) rather than on every single routing tick, since it's one of the more expensive computations in the system.

### Why keep `Edge` (static) and `TrafficWeight` (dynamic) in separate stores?

This is a good trade-off to narrate explicitly, echoing the same principle from the charging-network and OTA designs in this series: *"The static graph and its precomputed shortest-path structure change on the order of weeks and are read-heavy/write-rarely — a great fit for an immutable, versioned, possibly memory-mapped structure optimized for traversal speed. `TrafficWeight` changes continuously and is looked up by edge as an overlay during query time — a great fit for a fast, region-sharded key-value store. Joining them at query time (base cost + traffic multiplier per edge) keeps each store doing what it's good at, instead of forcing the giant precomputed routing structure to be rebuilt every time a single edge's traffic changes."*

---

## 5. High-Level Design

This is an **infrastructure/topology view** — what pieces of infrastructure exist, what type each one is (immutable versioned store, live key-value store, stateless query service, external dependency...), and how they're wired together — not a step-by-step trace of one trip's journey through the system. Sequencing and per-hop algorithmic detail belong in the Deep Dives (§6); this section should stand on its own as "here's what we'd provision."

### Infrastructure tiers

**External data-source tier (outside our infrastructure footprint)**
- **Licensed Map Provider** — a third-party vendor supplying periodic (days-to-weeks cadence) road-graph releases; we consume, we don't operate this.
- **Fleet GPS/Speed Telemetry** — a continuous stream produced by vehicles already on the road, not something this system owns the collection of.
- **Third-Party Traffic Feed** — a licensed, externally-operated traffic data provider with its own latency/coverage characteristics.
- **Charging-Network System** — an external dependency (see [`./charging-station-availability-reservation-network.md`](./charging-station-availability-reservation-network.md)), consulted only when a trip's range is a binding constraint.

**Control-plane / precompute tier (batch, off the live query path)**
- **Graph Ingestion & Precompute Pipeline** — a periodic batch job that ingests map-provider updates and rebuilds the shortest-path acceleration structure (contraction hierarchies / hub labeling), publishing a new immutable `RoadGraphVersion`. It never runs inline with a routing query; it's a build system, not a request-serving service.

**Processing tier (streaming fusion)**
- **Traffic Fusion Service** — a stateless stream processor that merges fleet telemetry and the third-party feed per road edge (weighted by source confidence/recency) and continuously writes the fused result into the live traffic store below.

**Storage / serving tier**
- **`RoadGraphVersion` store** — an immutable, versioned, memory-mapped structure holding the static graph plus its precomputed shortcut/label data; read-heavy, write-rarely, rebuilt wholesale rather than mutated in place.
- **`TrafficWeight` store** — a fast, region-sharded key-value store; the highest-write-volume piece of state in the system, joined against the static graph at query time rather than baked into it.

**Query-time serving tier (stateless services, horizontally scaled)**
- **Routing Engine** — the fast path: given origin/destination/vehicle state and a pinned `graph_version_id`, runs shortest-path search over the precomputed structure with the live `TrafficWeight` overlay applied as a cost adjustment.
- **EV Range & Charging-Stop Planner** — a heavier, conditionally-invoked service, called only when the direct route is infeasible; it's the one component in this tier that reaches out to the external Charging-Network system.
- **Incremental Re-Route Service** — subscribes to traffic-weight changes relevant to an in-progress trip's remaining segments and decides whether a cheap, localized patch suffices or a fuller recompute is warranted.

**Edge/client tier (runs on the vehicle, outside our infrastructure footprint)**
- **On-Vehicle Navigation Client** — holds a cached regional map + routing sub-structure + the current route's segments, renders turn-by-turn guidance, and can keep operating (with staling traffic) fully offline.

### Topology diagram (infrastructure view, described in ASCII)

```
 EXTERNAL SOURCES (outside our infra)
 ┌────────────────────┐   ┌───────────────────────┐   ┌─────────────────────┐
 │ Licensed Map        │   │ Fleet GPS/Speed        │   │ Third-Party Traffic │
 │ Provider (periodic) │   │ Telemetry (streaming)  │   │ Feed                │
 └──────────┬───────────┘   └───────────┬────────────┘   └──────────┬──────────┘
            │                             └───────────────┬──────────┘
            ▼                                              ▼
 CONTROL PLANE / BATCH                          PROCESSING TIER
 ┌─────────────────────┐                    ┌───────────────────────────┐
 │ Graph Ingestion &     │                   │ Traffic Fusion Service      │
 │ Precompute Pipeline   │                   │ (confidence-weighted merge) │
 │ (CH / hub labeling)   │                   └──────────────┬──────────────┘
 └──────────┬─────────────┘                                  │ writes
            │ publishes                                       ▼
            ▼                                    STORAGE / SERVING TIER
 STORAGE / SERVING TIER                 ┌────────────────────────┐
 ┌─────────────────────┐                │ TrafficWeight Store      │
 │ RoadGraphVersion      │◄── read ──────┤ (region-sharded, fast KV,│
 │ (immutable, versioned,│               │  continuously updated)   │
 │  memory-mapped)       │               └────────────────────────┘
 └──────────┬─────────────┘                            ▲
            │ read (base cost)                          │ overlay read
            ▼                                            │
 QUERY-TIME SERVING TIER (stateless, horizontally scaled)
 ┌──────────────────────────────────────────────────────┴─────────┐
 │                        Routing Engine                            │
 │           base graph cost + live traffic overlay                 │
 └───────────────┬─────────────────────────────┬────────────────────┘
                 │ feasible                     │ infeasible → forks off
                 ▼                              ▼
      ┌────────────────────┐       ┌─────────────────────────────┐
      │ Incremental          │       │ EV Range & Charging-Stop    │
      │ Re-Route Service      │◄─────┤ Planner (conditional,        │
      │ (segment-level patch) │      │  heavier compute)             │
      └──────────┬─────────────┘     └───────────────┬───────────────┘
                 │ pushes update                       │ queries availability
                 ▼                                       ▼
      ┌────────────────────┐                ┌──────────────────────────┐
      │ On-Vehicle Nav      │                │ Charging-Network System   │
      │ Client — EDGE TIER  │                │ (external dependency,     │
      │ (cached, offline-   │                │  see companion doc)        │
      │  capable)           │                └──────────────────────────┘
      └────────────────────┘
```

Narrate the key architectural decision: *"There isn't one shared backbone here the way a telemetry pipeline has a durable log — instead, the topology insight is a deliberate split between two storage tiers with completely different write patterns: an immutable, versioned graph store rebuilt on a weeks-long cadence, and a continuously-written, region-sharded traffic store, joined together only at query time by a stateless Routing Engine. The EV range/charging-stop logic is drawn as a genuine fork off that engine, not a downstream pipeline stage — it's invoked conditionally, only when a route is infeasible, and it's the only query-time component that reaches out to an external system. Everything in the query-time tier is stateless and horizontally scalable precisely because all the state it needs lives in those two storage tiers, not in the service instances themselves."*

---

## 6. Detailed Design / Deep Dives

Pick 2-3 of these based on interviewer interest — you won't have time for all of them in 45 minutes, so ask: *"Which of these would you like me to go deeper on: the precomputed routing structure, live traffic fusion, incremental re-routing, or the EV reachability/charging-stop insertion algorithm?"*

### 6.1 Precomputed routing structures vs. live traffic overlay

- A naive Dijkstra/A* search over a 10-20 million node graph is far too slow for a sub-second query budget. Instead, precompute an acceleration structure at graph-build time:
  - **Contraction hierarchies (CH):** iteratively "contract" nodes (remove them, adding shortcut edges that preserve shortest-path distances between their neighbors), producing a hierarchy that lets bidirectional search examine a tiny fraction of the graph at query time — typically enabling millisecond-scale shortest-path queries even on continent-scale graphs.
  - **Hub labeling:** an alternative (often used to get even faster queries at the cost of more precompute time and memory) that assigns each node a small set of "hub" labels such that any shortest path can be reconstructed by intersecting the two endpoints' label sets — extremely fast at query time, well-suited when query volume is very high and precompute can be done offline.
- **The catch:** these structures are built assuming static edge weights. Live traffic changes edge weights continuously, which is exactly what the precomputed shortcuts assumed wouldn't happen mid-structure.
- **Resolution — layered cost model:** keep the precomputed structure based on free-flow/typical speeds (a good approximation for the *topology* of which shortcuts matter), and apply the live `TrafficWeight` as a multiplicative penalty on the *base* edge cost at query time, re-ranking candidate paths from the structure rather than re-deriving the whole hierarchy. This is an approximation (a true traffic-aware CH would need traffic-aware contraction, which is far more expensive to keep fresh) but is the standard, practical trade-off: *"We accept that the precomputed shortcuts are topologically optimal for typical conditions, not necessarily for this exact moment's traffic, and correct for that with a live overlay rather than paying full traffic-aware-CH rebuild costs continuously."*
- Full graph rebuilds (including the CH/hub-label structure) run on the map-data refresh cadence (days to weeks), published as a new immutable `RoadGraphVersion` and rolled out blue-green so in-flight trips keep using their pinned version until they complete.

### 6.2 Merging multiple real-time traffic data sources

- Two structurally different sources feed `TrafficWeight`: **fleet-sourced GPS/speed traces** (high volume on roads we have coverage on, essentially free, but sparse on low-traffic-fleet-density roads) and a **licensed third-party feed** (broader coverage, but higher latency and a per-query/per-region cost).
- Fusion logic per edge: compute a confidence-weighted blend, e.g. `speed = (fleet_confidence × fleet_speed + third_party_confidence × third_party_speed) / (fleet_confidence + third_party_confidence)`, where `fleet_confidence` scales with recent sample count and recency, and drops toward zero on edges with little fleet presence — naturally falling back to the third-party feed as the dominant signal in fleet-sparse areas.
- Disagreement between sources (e.g., fleet says free-flowing, third-party says a major incident) is itself a signal — surface a conservative estimate (favor the slower/more-congested reading) rather than averaging away a real incident, since under-estimating congestion has a worse user experience than over-estimating it.
- Both sources are timestamped and staleness-decayed: an edge's effective confidence decreases the longer since its last update, so a stale reading gradually loses influence over the blended weight rather than being trusted indefinitely.

### 6.3 On-vehicle route caching for dead-zone continuation

- When a route is computed, the on-vehicle client caches not just the turn-by-turn path but a **corridor buffer** — the routing sub-graph and last-known traffic weights for roughly the planned route plus some lateral/ahead buffer (e.g., next 50-100 miles and a few miles either side), sized to comfortably cover a typical dead-zone duration.
- While offline, the vehicle continues to navigate using this cached corridor: turn-by-turn guidance keeps working, and even *local* re-routing (e.g., driver takes a wrong turn) can be served from the cached sub-graph using an on-vehicle lightweight routing capability, without needing the full-scale server-side precomputed structure.
- Traffic weights used offline are simply the last-synced values, silently aging — the client surfaces a subtle "traffic data may be outdated" indicator rather than blocking navigation, mirroring the same "degrade gracefully rather than fail closed" principle used for offline charging-station data.
- On reconnect, the client reconciles by pulling fresh traffic weights for the remaining route and re-evaluating whether a re-route (see 6.4) is warranted based on what changed while it was offline.

### 6.4 Incremental re-routing without a jarring full recompute

- A full route recompute is disruptive: it can change the plan out from under a driver who's already committed to a maneuver, and it's computationally more expensive than necessary when only a small part of the route is affected.
- Because the route is stored as an ordered list of `RouteSegmentPlan`s (§4), a traffic-weight change on an edge only invalidates the ETA/cost of the segment(s) containing that edge — the Incremental Re-Route Service recomputes just the affected segment's optimal sub-path (a bounded, local shortest-path search between that segment's fixed entry/exit points) rather than the whole origin-to-destination path.
- **Decision threshold for full vs. patch:** if the local segment recompute suggests a meaningfully better alternative that diverges from the current path *ahead* of the vehicle's near-term position (e.g., more than ~2 minutes out, giving time to communicate the change smoothly), patch just that segment and update guidance seamlessly. Only trigger a full recompute when the accumulated drift between "as planned" and "as things now stand" crosses a threshold (e.g., a major incident invalidates the entire remaining corridor, or the driver has deviated far enough that segment-patching no longer makes sense).
- This mirrors delta-based thinking from the OTA design in this series: *"Don't resend/recompute the whole artifact when only a small piece changed — identify the minimal delta and patch it."*

### 6.5 EV reachability polygon and charging-stop insertion

- **Reachability polygon:** given current state of charge, a vehicle-specific efficiency curve (kWh/mile, itself a function of speed, elevation, temperature, and HVAC load), and the road graph, compute the set of reachable nodes/area — conceptually similar to an isochrone (reachable-within-time map) but bounded by energy instead of time. A conservative `buffer_margin_pct` (e.g., 10-15%) is subtracted from the raw computed range to protect against efficiency-model error and driving-style variance — treat this margin as non-negotiable given the near-safety-critical feasibility requirement from §2.
- **Feasibility check:** if the destination falls within the reachability polygon (accounting for the buffer), route directly — no charging stop needed. If not, the route *must* include at least one charging stop before the polygon's boundary.
- **Stop candidate selection:** query the charging-network system (external dependency) for stations within the reachable area, filtered to those near the route corridor (not just nearest to current position, since a station far off the direct path may cost more total time despite being "reachable") and weighted by the same distance/confidence/state signals that system exposes (§6.4 of the charging-network document) — a station reported as `inferred/likely-available` is still a valid candidate but ranked below a `confirmed available` one, with a fallback candidate held in reserve.
- **Optimal stop insertion:** for each viable candidate station, model the total trip cost as `drive_time_to_station + charging_time_at_station (function of arrival SOC and target SOC) + drive_time_from_station_to_destination_or_next_stop`, and choose the insertion point(s) that minimize total trip time (or number of stops, depending on the user's preference setting) subject to the hard reachability constraint at every leg — this is effectively a shortest-path problem over an augmented graph where "arrive at a charging station with X% SOC" is itself a graph state, not just a location.
- **Re-evaluation in flight:** if traffic materially changes ETA to the planned charging stop (affecting arrival SOC due to different driving conditions) or the charging-network system reports the planned connector became unavailable, re-run stop selection for just that leg — reusing the same incremental-recompute philosophy as §6.4, rather than replanning the entire multi-stop itinerary from scratch.

---

## 7. Minimal API Surface (illustrative)

```
# Trip planning
POST /v1/trips
     → { vehicle_id, origin, destination, current_soc_pct, preferences }
     → { trip_id, route_id, charging_stops[], estimated_arrival_at, estimated_soc_at_arrival }

GET  /v1/trips/{trip_id}/route
     → current RouteSegmentPlan list + turn-by-turn geometry

# Live updates (in-vehicle client polls or subscribes)
GET  /v1/trips/{trip_id}/route-updates?since_segment=
     → incremental patch: which segment(s) changed, new ETA, optional full-reroute flag

POST /v1/trips/{trip_id}/reachability
     → { current_soc_pct }
     → { polygon_geometry, destination_reachable: bool }

# Internal: charging-network client (calls into the system in doc A)
GET  /internal/charging-network/candidates?corridor_polygon=&min_kw=

# Map/graph management (operator-facing)
POST /internal/graph/publish       → publish a new RoadGraphVersion after precompute
GET  /internal/graph/versions      → list published versions and rollout status
```

---

## 8. Trade-offs and Alternatives Considered

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| Shortest-path acceleration | Precomputed contraction hierarchies / hub labeling, refreshed on map-update cadence | Live Dijkstra/A* per query | Live search over a 10-20M node graph can't meet a sub-second latency budget at the required query volume; precomputation trades a periodic, expensive offline build for millisecond-scale online queries. |
| Traffic incorporation | Live overlay cost applied on top of a static precomputed structure | Fully traffic-aware contraction hierarchies, rebuilt continuously | Traffic-aware CH gives more optimal shortcut selection under current conditions but is far too expensive to rebuild at traffic's update frequency; the overlay approach is a well-understood, practical approximation. |
| Route representation | Segmented (`RouteSegmentPlan` list) for incremental patching | Single monolithic path blob per trip | Segments let a local traffic change invalidate and recompute only the affected piece, avoiding both wasted compute and jarring full-route resets for the driver. |
| Static graph vs. traffic weights | Two separate stores (immutable versioned graph vs. fast region-sharded live weights) | One unified graph store with mutable edge weights | Keeps the expensive-to-rebuild structure stable and cacheable while letting traffic data update continuously and independently, avoiding lock contention or cache invalidation storms on the whole graph for every traffic tick. |
| EV charging-stop insertion | Separate, conditionally-invoked heavier computation (augmented-graph search with SOC as state) | Fold charging-stop logic into every base routing query | Charging-stop insertion is only relevant to a small fraction of trips (long-haul) and is meaningfully more expensive; invoking it conditionally keeps the common-case (short trip, no stop needed) query fast. |
| Offline continuation | On-vehicle corridor-buffer caching of route + sub-graph + last-known traffic | Require live connectivity for all navigation | Consistent with the fleet's core intermittent-connectivity constraint; a nav system that stops working in a tunnel is a non-starter for this product. |

---

## 9. Failure Modes & Edge Cases to Call Out Proactively

- **Vehicle deviates from the planned route (misses a turn):** the on-vehicle client detects the deviation locally (GPS position off-corridor) and attempts a local re-route from its cached sub-graph first; only escalates to the backend if the deviation takes it outside the cached corridor buffer entirely.
- **Traffic data source disagreement or an outright bad reading (e.g., a GPS glitch reporting a fleet vehicle "stopped" on a highway):** apply outlier filtering/sample-count thresholds before trusting a single-source reading enough to materially change a route's cost, and favor the third-party feed as a sanity check on isolated fleet anomalies.
- **Charging-network system is unreachable when a stop-insertion query is needed:** don't fail the whole trip-planning request — fall back to a conservative, cached/last-known set of major charging corridors (a much coarser, slower-changing dataset than live availability) so the driver still gets *a* feasible route, clearly flagged as "using cached charger data."
- **Reachability polygon says a route is feasible, but real-world efficiency is worse than modeled (headwind, cold weather, aggressive driving):** continuously re-evaluate reachability against actual observed consumption rate during the trip, not just the pre-trip estimate, and proactively suggest an earlier/additional charging stop if the trend suggests the buffer margin is being eroded faster than expected — better to suggest an extra stop early than to strand the driver.
- **Map data is stale or wrong for a specific segment (e.g., a road closure not yet reflected in the licensed provider's graph update):** treat a real-time incident feed (from the traffic sources) as capable of overriding graph-level assumptions temporarily — a closed road should manifest as an effectively-infinite cost edge in `TrafficWeight`, not require a full map republish to route around.
- **Two vehicles are routed to the exact same charging stop as their "optimal" choice, but the charging-network system only has one available connector:** this is fundamentally the charging-network system's concurrency problem to solve (per its own hold/TTL mechanism), but the navigation system should handle a late "actually, that connector is no longer available" response gracefully by re-running stop selection for the affected leg, not surfacing a hard error mid-trip.
- **Full graph version rollout mid-trip:** trips pin to a `graph_version_id` at start, so an in-progress trip is unaffected by a new graph publish; only new trip requests pick up the new version, avoiding router inconsistency for an active driver.

---

## 10. Monitoring, Observability, and Security (brief)

- **Dashboards:** route computation latency percentiles (split by trip-planning vs. turn-by-turn re-route), traffic data freshness/coverage by region and source, charging-stop-insertion success/failure rate, reachability-polygon "buffer erosion" alerts.
- **Alerting:** page on a spike in full-recompute rate (may indicate a traffic-fusion or graph-quality regression), on charging-network client error rate (may indicate the upstream system in doc A is degraded), and on any measurable increase in "stranded" incidents (reachability guarantee violations) — treated as a top-severity incident class given the near-safety-critical nature of that guarantee.
- **Security:** validate and rate-limit fleet-sourced telemetry ingestion to prevent a compromised or spoofed vehicle from injecting false traffic data that could manipulate routing at scale (e.g., falsely reporting congestion to divert traffic away from a road); authenticate the charging-network client integration; ensure route/trip data (which reveals a driver's travel patterns) is access-controlled and retained per relevant privacy policy.

---

## 11. Wrap-up / How to Close the Interview

Summarize in 30 seconds: *"To recap: we separated a slow-changing, precomputed, immutable road graph (accelerated via contraction hierarchies or hub labeling for millisecond-scale shortest-path queries) from a fast-changing, region-sharded live traffic overlay applied as a cost adjustment at query time. Routes are stored as segments so incremental traffic changes trigger cheap, localized patches instead of jarring full recomputes, and the on-vehicle client caches a corridor buffer so navigation keeps working through dead zones. The EV-specific layer — a reachability polygon derived from state of charge and a conservative safety buffer, with charging-stop insertion modeled as an augmented shortest-path search — is invoked conditionally rather than on every query, and it consumes the charging-network system's availability data as an external dependency rather than reimplementing it."*

Then proactively offer a couple of extension directions, showing you know where the design could go next:
- How would you extend the routing cost function to incorporate **predictive traffic** (e.g., "this highway is always congested at 5pm on weekdays") rather than only reactive, currently-observed traffic — blending historical patterns with live signal for a trip that starts now but takes hours?
- How would you support **multi-stop commercial/fleet routing** (e.g., a delivery vehicle with 20 stops), where the problem becomes closer to vehicle routing/TSP-adjacent rather than simple point-to-point navigation?
- How would you evolve charging-stop insertion to account for **reservation contention** proactively — e.g., preemptively holding a connector at the moment a route is computed rather than only checking availability, tying directly back into the reservation-hold mechanics of the charging-network system?

---

## 12. Follow-up Questions Interviewers May Ask

- "Why not just recompute the traffic-aware shortest path from scratch on every query if your servers are fast enough — what specifically breaks down at scale that forces precomputation?"
- "Walk me through what happens, step by step, if the vehicle loses connectivity exactly when it needed to be told about a new traffic incident that would have changed its route."
- "How do you decide the size of the on-vehicle cached corridor buffer — what happens if a driver takes an unplanned long detour that exceeds it?"
- "How would you validate that your fused traffic estimate (fleet + third-party) is actually more accurate than either source alone, in production?"
- "What's your fallback if the EV efficiency model is systematically wrong for a specific vehicle (e.g., a roof rack changing aerodynamics) — how would the system detect and adapt to that over time?"
- "How would this design change for a market with sparse fleet density (so little to no fleet-sourced traffic data) and a less reliable third-party traffic provider?"
- "If two different trips' optimal routes are recomputed independently and both decide to route through the same road segment based on current low traffic, could your own system cause the very congestion it was trying to avoid — and how would you mitigate that?"

---

## References

- Rivian system design round context: see [`../rivian/index.md`](../rivian/index.md), section "System Design Interview Questions."
- Depends on [`charging-station-availability-reservation-network.md`](./charging-station-availability-reservation-network.md) for real-time charging availability/reservation data — this document treats that system as an external dependency and focuses on routing, traffic fusion, and EV-specific reachability logic built on top of it.
- Shares the offline-first, degrade-gracefully-rather-than-fail-closed philosophy with [`ota-update-system-for-connected-vehicle-fleet.md`](./ota-update-system-for-connected-vehicle-fleet.md) — on-vehicle route caching for dead-zone continuation is conceptually the same store-and-forward/offline-first pattern applied to navigation instead of software updates.
