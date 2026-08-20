# CA-002 — A Case for Redundant Arrays of Inexpensive Disks (RAID)

- **Authors:** David A. Patterson, Garth Gibson, Randy H. Katz
- **Year:** 1988
- **Field:** Computer Architecture / Storage Systems / Reliability
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://www2.eecs.berkeley.edu/Pubs/TechRpts/1987/5853.html
- **DOI:** https://doi.org/10.1145/50202.50214

## Why it matters

This paper established RAID as a systematic storage architecture: combine many inexpensive disks to obtain higher aggregate I/O performance and use redundancy to compensate for the increased probability of individual disk failure. It introduced the RAID terminology and five RAID levels, turning striping, mirroring, parity, and failure recovery into a design space with explicit cost/performance/reliability tradeoffs.

Its larger systems lesson is enduring: replacing one expensive, highly reliable component with many cheaper parallel components can improve performance and economics, but only if the architecture explicitly handles the new failure modes introduced by scale.

## Prerequisites

- Basic disk/storage concepts: blocks, seeks, transfer bandwidth, I/O requests
- Parallelism and throughput versus latency
- Basic probability intuition for component failures
- XOR/parity at a conceptual level
- The distinction between performance, capacity, and reliability

## Key ideas

1. **Parallel disks can remove an I/O bottleneck.** CPU and memory performance were improving faster than disk performance; spreading I/O across many disks creates aggregate bandwidth and concurrency.
2. **More components also mean more failures.** An array of many inexpensive disks has a shorter expected time between individual disk failures than a single disk, so redundancy is not optional.
3. **Striping granularity changes workload behavior.** Fine-grained striping can make many disks cooperate on one large request; coarse-grained striping can let independent requests proceed in parallel.
4. **RAID levels encode different tradeoffs.** Mirroring, dedicated parity, distributed parity, and different striping schemes trade usable capacity, read bandwidth, write cost, and failure recovery differently.
5. **The right metric is system-level cost/performance/reliability.** A component that is individually slower or less reliable can participate in a system that is faster and adequately reliable when redundancy and parallelism are designed together.

## Section-by-section reading guide

### Motivation and SLED versus RAID

Read carefully. Understand the authors' argument that faster CPUs and memories make storage increasingly important, and why arrays of commodity disks offer both aggregate performance and lower cost than a single large expensive disk.

### Reliability implications

Read fully. The important conceptual move is that parallelism increases both performance and the frequency of component failure. Work through why an array needs redundancy even if each individual disk has a respectable mean time to failure.

### Data striping

Read carefully. Distinguish striping at small units such as bits or sectors from striping at larger blocks. Ask whether the intended workload benefits more from making one request use many disks or from letting many requests use different disks concurrently.

### RAID levels 1–5

This is the core of the paper. Do not memorize the labels mechanically; understand the design dimensions behind them:

- duplication versus parity
- dedicated versus distributed redundancy
- small versus large striping units
- read behavior versus write behavior
- capacity overhead versus fault tolerance

Pay special attention to RAID 5's distributed parity and why it avoids concentrating parity traffic on one dedicated disk.

### Performance and cost comparisons

Read for methodology rather than obsolete device specifications. The numerical disk models are historical; the useful lesson is to compare architectures using workload-sensitive throughput, usable capacity, redundancy overhead, and failure behavior rather than a single device metric.

### Conclusions

Read fully. Reframe the RAID levels as examples in a broader architectural space rather than a fixed taxonomy that every modern system must implement literally.

## Estimated reading time

- Focused conceptual read: 45–60 minutes
- With RAID-level diagrams and write-path examples: 90–120 minutes

## Recommended reading approach

**Read fully.** The paper is short enough, historically foundational, and the comparison among RAID levels is much more useful when read as one coherent argument.

## Connection to Linux and Aruba networking work

The most relevant connection is the systems tradeoff between **parallelism and failure surface**. Network datapaths often scale by adding queues, cores, links, workers, APs, gateways, or replicated state holders. Parallelism can improve throughput, but every added component introduces additional partial-failure and consistency cases.

RAID's design pattern is therefore useful beyond disks: do not evaluate a scale-out design only by its fast path. Ask what redundancy exists, how failure is detected, how state is reconstructed, whether recovery creates a bottleneck, and whether the redundancy mechanism itself concentrates load.

There is also a concrete Linux connection. Linux software RAID (`md`), device-mapper targets, storage appliances, and many server systems expose RAID-derived layouts. When diagnosing an appliance whose logs, packet captures, crash dumps, or databases live on redundant storage, understanding degraded mode, rebuild I/O, parity-write amplification, and correlated failure can help distinguish an application performance regression from an underlying storage condition.

## Questions to answer after reading

1. Why does adding disks improve performance while simultaneously worsening the raw component-failure rate of the system?
2. What workload differences make fine-grained and coarse-grained striping behave differently?
3. Why can a dedicated parity disk become a bottleneck?
4. What is the read-modify-write penalty for small parity-protected writes?
5. Which assumptions in the 1988 RAID taxonomy are different for SSDs and modern distributed storage, and which principles remain unchanged?

## Related indexed papers

- CA-001 — RISC I: A Reduced Instruction Set VLSI Computer
- DB-002 — ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging
- DS-002 — The Google File System
