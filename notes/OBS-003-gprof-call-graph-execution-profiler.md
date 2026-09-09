# OBS-003 — gprof: A Call Graph Execution Profiler

- **Authors:** Susan L. Graham, Peter B. Kessler, Marshall K. McKusick
- **Year:** 1982
- **Field:** Observability / Performance Profiling / Call-Graph Profiling / Debugging
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-09
- **Primary source:** https://doi.org/10.1145/800230.806987
- **Published in:** Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, pp. 120–126

## Why it matters

`gprof` changed profiling from a flat list of hot routines into an attempt to explain *where execution time comes from in the program's calling structure*. Graham, Kessler, and McKusick combine statistical program-counter sampling with instrumentation that records caller→callee arcs and call counts, then propagate measured time through the dynamic call graph so a programmer can see both a routine's own cost and the cost attributable to its descendants.

That distinction is fundamental. A small wrapper may consume almost no self CPU time yet be responsible for a large fraction of total execution time because it repeatedly invokes expensive work below it. A flat profiler can hide that architectural relationship; a call-graph profile exposes it.

The paper also illustrates a systems lesson that remains important in modern observability: instrumentation should collect a deliberately small amount of information online and defer expensive interpretation to post-processing. Its approach influenced decades of Unix performance tooling and made `gprof` a standard part of the Unix programming environment.

## Prerequisites

- C/Unix process execution at a conceptual level
- function calls and call stacks
- basic performance profiling
- sampling versus instrumentation
- directed graphs and strongly connected components at a high level

## Reading guide

### Introduction
Read fully. Focus on the motivation: routine-level self time is not enough for modular programs because expensive work is often performed by callees on behalf of callers. The profiler should reflect the program's logical decomposition, not merely where the program counter happened to land.

### Gathering the call graph
Read carefully. Understand the instrumentation mechanism that records arcs from caller to callee and counts how often each arc executes. Separate this from time measurement: call relationships and execution-time samples are gathered by different mechanisms.

### Gathering execution-time information
Read carefully. The paper uses periodic sampling of the program counter rather than timing every function entry/exit. This keeps measurement overhead lower but makes timing statistical rather than exact.

### Post-processing
Read very carefully. This is the conceptual core. The profiler builds the dynamic call graph, handles cycles, and propagates child execution time toward callers. Notice the assumption used when one callee is reached from multiple parents: the callee's measured time is apportioned among parents in proportion to call counts.

### Presentation of the profile
Read fully. Compare the flat profile with the call-graph view. The useful distinction is **self time** versus **descendant/children time**. This is the ancestor of the inclusive/exclusive cost distinction you still see in modern profilers and flame-graph-style analysis.

### Experience / conclusions
Read fully. Pay attention to how the authors use profiles to guide optimization rather than assuming that source-level intuition identifies bottlenecks correctly.

## Key ideas

1. **Self cost and responsible cost are different.** A caller can be responsible for expensive descendants even if its own instructions are cheap.
2. **Combine sampling with instrumentation.** Sampling estimates where CPU time is spent; lightweight call-arc instrumentation reconstructs dynamic calling relationships.
3. **Collect cheaply, analyze later.** The runtime records compact measurements, while call-graph construction, cycle handling, attribution, sorting, and reporting happen after execution.
4. **Attribution requires assumptions.** `gprof` distributes a callee's measured time among callers using call frequencies, which is useful but can be inaccurate when different call sites have very different costs.
5. **Profiles should answer architectural questions, not just identify hot addresses.** The call graph connects low-level measurements back to the program structure a developer reasons about.

## Connection to Linux and Aruba networking work

This paper maps directly to performance debugging in a packet-processing datapath. Suppose `process_packet()` itself appears cheap, but it fans out into classification, policy lookup, tunnel handling, statistics, and output processing. A flat profile might identify `policy_lookup()` as hot; a call-graph profile can additionally show *which packet path and which caller* are responsible for invoking it enough to dominate CPU time.

For a Linux datapath, keep the distinction between **exclusive** and **inclusive** cost explicit:

```text
rx_worker
  └─ process_packet
       ├─ classify
       ├─ session_lookup
       │    └─ hash_lookup
       └─ encapsulate
```

If `hash_lookup` consumes 20% of CPU, the debugging question is not only “why is `hash_lookup` expensive?” but also “which higher-level path is responsible for those calls?” That is the central insight of `gprof`.

Modern Linux tooling such as `perf`, sampled stack profiling, eBPF profiling, and flame graphs uses more capable mechanisms and can retain full calling contexts that classic `gprof` cannot. But the conceptual decomposition—sample cost, recover calling relationships, distinguish self from inherited cost, and attribute expensive descendants to higher-level operations—remains directly useful when analyzing Aruba gateway or AP datapath CPU bottlenecks.

## Reading recommendation

**Read fully.** It is short and historically important. The post-processing/time-propagation section deserves the most attention.

**Estimated reading time:** 25–35 minutes; 45–60 minutes if you manually trace time propagation through the example call graph.

## Related papers in this library

- OBS-001 — Dapper, a Large-Scale Distributed Systems Tracing Infrastructure
- OBS-002 — Dynamic Instrumentation of Production Systems
- DBG-001 — Eraser: A Dynamic Data Race Detector for Multithreaded Programs
- COMP-003 — A Unified Approach to Global Program Optimization
- CA-003 — An Efficient Algorithm for Exploiting Multiple Arithmetic Units
