# DB-005 — Dynamo: Amazon’s Highly Available Key-value Store

- **Authors:** Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall, Werner Vogels
- **Year:** 2007
- **Field:** Databases / Distributed Databases / Key-Value Stores / Eventual Consistency
- **Status:** Queued
- **Priority:** Core
- **Date recommended:** 2026-09-25
- **Primary source:** https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store
- **DOI:** https://doi.org/10.1145/1294261.1294281

## Why it matters

Dynamo is one of the defining production distributed-storage papers. Amazon designed it for services where remaining writable and meeting stringent latency targets mattered more than immediate replica consistency during some failures. The system combines consistent hashing, replication, vector clocks, sloppy quorums, hinted handoff, Merkle-tree anti-entropy, gossip membership, and application-assisted reconciliation into one operational design.

Its lasting lesson is not any single mechanism. It is how partitioning, replication, conflict detection, failure handling, repair, and latency goals must be designed together.

## Prerequisites

- Replication and crash/network failures
- Hashing and consistent hashing
- Basic quorum replication
- Eventual consistency
- Causal ordering / versioning
- High-percentile latency

Useful related papers in this library: DS-003, DS-004, DS-006, and DB-004.

## Reading guide

### 1. Introduction — read fully
Focus on the workload and operational objective. Component failure is assumed to be routine, and some services must continue accepting operations while infrastructure is degraded. That requirement drives the architecture.

### 2. Background — read fully
Pay particular attention to the design considerations. Dynamo is not intended to be a general relational database: workloads are mostly primary-key reads/writes, need incremental scale-out, and care strongly about availability and tail latency.

### 3. Related Work — read selectively
Use this section to understand where Dynamo differs from systems optimized for stronger consistency or richer query semantics.

### 4. System Architecture — read very carefully
This is the core of the paper.

- **Interface:** understand `get(key)` and `put(key, context, object)`; the context carries version information.
- **Partitioning:** study consistent hashing and virtual nodes.
- **Replication:** understand the preference list and replication factor `N`.
- **Versioning:** spend time on vector clocks and concurrent versions.
- **Reads/writes:** understand `N`, `R`, and `W`.
- **Temporary failures:** read sloppy quorum and hinted handoff carefully.
- **Permanent failures:** understand Merkle-tree anti-entropy.
- **Membership/failure detection:** distinguish temporary unreachability from permanent membership change.

### 5. Implementation — read fully
Study request coordination, state-machine based operations, local storage, and read repair.

### 6. Experiences & Lessons Learned — read fully
This section is especially valuable. Focus on load imbalance, high-percentile latency, divergent versions, coordinator placement, and how background work such as repair and rebalancing can interfere with foreground requests.

### 7. Conclusion — read fully
Revisit how the mechanisms combine to achieve an availability-first operating point.

## Key ideas

1. **Consistency is a workload decision, not a universal maximum.** Some applications rationally prefer accepting an update during failure and reconciling later.
2. **Distributed-storage mechanisms are coupled.** Partitioning, replication, versioning, failure handling, and repair cannot be designed independently.
3. **N, R, and W are operational policy knobs.** They directly affect latency, availability, durability, and consistency behavior.
4. **Temporary failure is not the same as permanent membership change.** Conflating them causes unnecessary data movement and instability.
5. **Background correctness work needs resource governance.** Repair and rebalancing can themselves become production problems if they interfere with foreground latency.

## Connection to Linux / Aruba networking work

A useful analogy is distributed client or session ownership across gateways or control-plane nodes. Different state types should have explicit consistency semantics: telemetry counters may tolerate eventual convergence, while forwarding ownership or security policy may require much stronger ordering.

Dynamo also suggests what a flight recorder should retain around distributed-state incidents: version or epoch, coordinator, replica/peer set, unreachable peers, timeout decisions, temporary fallback ownership, reconciliation events, and background synchronization activity.

Its treatment of background repair is particularly relevant to datapath systems. State synchronization, cleanup, telemetry export, and diagnostics can all be logically correct while still damaging packet-processing latency if they do not have admission control or resource budgets.

## Read fully or selectively?

Read Sections 1, 2, 4, 5, 6, and 7 fully. Read Section 3 selectively on the first pass.

**Estimated reading time:** 60–75 minutes for a first pass; roughly 90 minutes for a careful pass.
