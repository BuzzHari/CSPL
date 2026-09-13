# DB-004 — The Case for Shared Nothing

- **Author:** Michael Stonebraker
- **Year:** 1986
- **Field:** Databases / Parallel Databases / Shared-Nothing Architecture / Distributed Systems
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-13
- **Primary source:** https://db.cs.berkeley.edu/papers/hpts85-nothing.pdf
- **Published in:** IEEE Database Engineering Bulletin, 9(1), 4–9

## Why it matters

Stonebraker compares three architectures for high-transaction-rate multiprocessor database systems: shared memory, shared disk, and shared nothing. His central argument is that shared-nothing systems—where each processor has private memory and private storage—avoid the centralized resource contention that limits shared-memory and shared-disk designs and therefore offer a cleaner path to scale-out.

The paper is short, opinionated, and historically important. Its architectural vocabulary became standard in database systems and later generalized to distributed storage and data-processing systems. Modern distributed SQL engines, data warehouses, key-value stores, and large-scale stream/data-processing systems often use designs whose core scaling intuition is recognizably shared-nothing: partition data and work across independent nodes, communicate explicitly, and avoid a globally shared memory or storage bottleneck.

The paper is also valuable because it does not claim that architecture alone guarantees linear scaling. Stonebraker discusses the practical constraints that remain: partitioning, load balance, interconnect cost, skew, transaction locality, and the difficulty of operations that span nodes.

## Prerequisites

- basic database architecture
- transactions and transaction processing
- CPU, memory, disk, and I/O bottlenecks
- basic distributed-systems communication
- data partitioning/sharding at a conceptual level

## Reading guide

### Abstract and Introduction
Read fully. Internalize the three architectures:

- **Shared memory (SM):** processors share a common memory.
- **Shared disk (SD):** processors have private memory but share disks.
- **Shared nothing (SN):** processors share neither memory nor storage; communication is explicit.

Do not read "shared nothing" as "nodes never coordinate." They coordinate through messages; what they avoid is a globally shared hardware resource that all processors directly contend for.

### Section 2 — Back-of-the-envelope comparison
Read carefully. This section frames the main argument in terms of cost, bandwidth, contention, and scaling. The historical hardware assumptions are dated, but the method is still useful: identify which resource becomes globally contended as nodes are added.

### Sections 3–5 — Detailed comparison
Read fully but focus on the architectural reasoning rather than old machine names or prices.

For shared-memory designs, watch the contention and memory-bandwidth argument. For shared-disk designs, focus on the shared I/O path, cache-coherence/coordination burden, and the limits of a common disk subsystem. For shared-nothing designs, focus on partitioned ownership and aggregate bandwidth: adding a node can add CPU, memory, and I/O capacity together.

### Data placement and transaction locality
This is the most important modern systems lesson. Shared-nothing works best when data and computation can be partitioned so most operations are local to one node or a small subset of nodes. Cross-partition work introduces communication and coordination, which can erase the hoped-for scale-out gains.

### Conclusion
Read fully. Treat the conclusion as a strong architectural thesis, not a universal law. Modern systems use shared-nothing ideas extensively, but many also deliberately reintroduce shared services, disaggregated storage, distributed coordination, caches, or replicated metadata when those tradeoffs are worthwhile.

## Key ideas

1. **Scalability is often about eliminating global contention.** A design that requires every node to compete for one shared memory or storage path eventually meets that path's limit.
2. **Partitioned ownership lets capacity scale with node count.** In a shared-nothing system, adding nodes can add CPU, memory, storage, and I/O bandwidth together.
3. **Data placement is part of the architecture.** Performance depends on assigning data so common transactions execute locally; poor partitioning creates expensive cross-node communication.
4. **Scale-out is not automatically linear.** Skew, distributed transactions, coordination, interconnect cost, and hot partitions can dominate.
5. **"Shared nothing" is a resource-ownership model, not an absence of communication.** Nodes still exchange messages and coordinate; they simply avoid direct sharing of memory and peripheral storage.

## Connection to Linux and Aruba networking work

The paper maps naturally to datapath architecture. Consider a packet-processing system with multiple cores or workers.

A heavily shared design might have all workers contend on a global session table, allocator, queue, lock, or statistics structure. Adding cores can then increase contention faster than useful throughput.

A shared-nothing-inspired datapath instead tries to partition ownership:

```text
flow hash -> worker/core
             |
             +-- private/local flow state
             +-- local queues
             +-- local counters
             +-- local cache
```

Most packets stay on the owning worker, while cross-worker communication is explicit and relatively rare. This is closely related to per-CPU state in Linux, RSS/RPS steering, queue affinity, sharded hash tables, DPDK worker models, and avoiding cache-line bouncing on hot global data.

The same warning from database systems applies: partitioning only helps when ownership is stable and work is sufficiently local. Roaming clients, shared tunnels, global policy changes, multicast/broadcast state, or control-plane events may require cross-partition coordination. A good datapath design therefore asks not just "can we shard this?" but "what is the expected rate and cost of operations that violate the shard boundary?"

## Reading recommendation

**Read fully.** The paper is only a few pages and its value lies in the architectural comparison rather than any one theorem.

**Estimated reading time:** 20–30 minutes; 40–50 minutes if you pause to map each architecture to modern database and packet-processing systems.

## Related papers in this library

- DB-001 — A Relational Model of Data for Large Shared Data Banks
- DB-003 — Access Path Selection in a Relational Database Management System
- DS-001 — MapReduce: Simplified Data Processing on Large Clusters
- DS-002 — The Google File System
- ARCH-001 — End-to-End Arguments in System Design
