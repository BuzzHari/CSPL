# OBS-004 — Continuous Profiling: Where Have All the Cycles Gone?

- **Authors:** Jennifer M. Anderson, Lance M. Berc, Jeffrey Dean, Sanjay Ghemawat, Monika R. Henzinger, Shun-Tak A. Leung, Richard L. Sites, Mark T. Vandevoorde, Carl A. Waldspurger, William E. Weihl
- **Year:** 1997
- **Field:** Observability / Continuous Profiling / Performance Analysis / Operating Systems
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-23
- **Primary source:** https://www.waldspurger.org/carl/papers/dcpi-sosp97.pdf
- **DOI:** https://doi.org/10.1145/268998.266637
- **Published in:** Proceedings of the 16th ACM Symposium on Operating Systems Principles (SOSP '97), pp. 1–14; an expanded journal version appeared in ACM Transactions on Computer Systems, 15(4), 357–390.

## Why it matters

This paper describes the DIGITAL Continuous Profiling Infrastructure (DCPI), one of the foundational systems showing that detailed performance profiling does not have to be a special laboratory activity. A profiler can run continuously on production systems, observe essentially the whole machine rather than one specially rebuilt program, and still impose low enough overhead to be useful operationally.

The architectural move is important. Instead of instrumenting every function or instruction, DCPI uses hardware performance counters to interrupt execution at statistically chosen points. Each sample records enough context to attribute processor cycles and other hardware events back to executable images and instructions. A user-space daemon aggregates those samples into an on-disk profile database, while offline tools reconstruct higher-level performance explanations.

That gives a pipeline of roughly:

```text
hardware performance counters
          ↓
randomized sampling interrupts
          ↓
PC + process/image context
          ↓
low-overhead kernel buffering
          ↓
user-space aggregation
          ↓
persistent profile database
          ↓
post-processing / attribution
          ↓
program → procedure → source → instruction → stall reason
```

The system was designed to profile applications, shared libraries, device drivers, and the operating-system kernel together. The paper reports high-rate sampling with roughly 1–3% slowdown for most workloads, which was low enough for continuous production use. More importantly, the authors do not stop at hotspot counts: their analysis tries to distinguish whether an instruction appears frequently because it executes often or because it stalls, and then attributes stalls to causes such as cache misses, branch mispredictions, or functional-unit contention.

This is a direct ancestor of the operating model behind modern statistical profilers and fleet-wide continuous profiling: collect sparse measurements cheaply, preserve enough context to reconstruct where resources are going, and do expensive interpretation away from the hot path.

## Prerequisites

- processes, executables, shared libraries, and kernel/user address spaces
- program-counter sampling and statistical profiling
- CPU pipelines at a high level
- cache misses and branch mispredictions
- hardware performance counters at a conceptual level
- basic ideas from `OBS-003 — gprof` are helpful but not required

## Reading guide

### 1. Introduction
Read fully. This section contains the paper's architectural thesis. Focus on why the authors want **whole-system**, **unmodified-binary**, **continuous** profiling rather than a profiler that requires recompilation or one-off experiments. Also note the two explicit engineering problems: collecting samples at a high rate with low perturbation, and turning raw samples into useful explanations of processor stalls.

The most important distinction to retain is that a sample stream is only raw evidence. The real value comes from mapping that evidence back to the program and explaining why time was spent there.

### 2. Related Work
Read selectively. Use this section to understand the design space rather than memorizing each historical profiler. The key axes are:

- application-only versus whole-system visibility;
- instrumentation versus statistical sampling;
- instruction counts versus time attribution;
- whether stall causes can be explained;
- whether overhead is low enough for continuous production use.

The authors argue that direct instrumentation or simulation can provide detailed information but often at costs too high for always-on profiling, while conventional sampling is cheap but may lack enough precision or context.

### 3. Data Analysis Examples
Read fully. This section is useful because it starts with the questions a performance engineer actually asks rather than the implementation details. The tools move from coarse attribution—what process or procedure consumed cycles—to instruction-level explanations.

Pay attention to the examples where seemingly small low-level effects explain large application-level performance differences. The lesson is that a profiler should help move from **symptom** to **mechanism**, not merely produce a ranked list of hot addresses.

### 4. Data Collection System
Read very carefully. This is the systems core of the paper.

The collection architecture has three main pieces:

1. a kernel driver handling hardware performance-counter interrupts and buffering samples;
2. a user-space daemon draining those samples and aggregating them into persistent profiles;
3. loader/process bookkeeping that maps sampled addresses to the correct executable image and version.

Notice several ideas that remain current: per-CPU state, keeping interrupt work small, buffering before expensive processing, separating collection from symbolization/analysis, and tracking executable mappings so addresses retain meaning over time.

Also study why the sampling interval is randomized. Periodic sampling at a fixed interval can accidentally synchronize with periodic program behavior and bias measurements. Randomization reduces that risk.

### 5. Data Collection Performance
Read the aggregate-overhead results carefully; skim detailed historical machine constants.

The important question is not whether a profiler has *zero* overhead, but whether its overhead is low and predictable enough that it can remain enabled on realistic systems without invalidating the behavior being measured. The paper reports roughly 1–3% slowdown for most workloads and breaks the cost into interrupt handling and daemon-side processing.

This section is also a useful example of measuring the observer itself. A production observability system should profile its CPU cost, memory footprint, storage growth, and worst-case behavior rather than merely claiming to be lightweight.

### 6. Data Analysis Overview
Read carefully. Raw cycle samples alone do not tell you whether an instruction is expensive because it executes frequently or because each execution stalls. DCPI combines samples, control-flow information, instruction semantics, and a processor model to infer execution frequencies, cycles per instruction, and likely stall causes.

This is the intellectually subtle part of the paper. The collection mechanism is intentionally sparse; post-processing reconstructs richer information. Treat that as a general observability pattern:

```text
cheap lossy measurement
        +
structural model
        +
offline inference
        ↓
useful explanation
```

Do not try to memorize the Alpha-specific pipeline details on a first read. Focus on what information is directly observed versus what is inferred, and on the assumptions required for those inferences.

### 7. Future Directions
Skim, but notice how naturally the profile database becomes input to compilers, linkers, binary rewriters, and runtime optimization. Once measurements are continuously available and mapped back to code, observability can become part of an optimization loop rather than a passive debugging tool.

### 8. Conclusions
Read fully. Re-evaluate the system against three goals: low perturbation, whole-system coverage, and explanatory detail. The durable contribution is not an Alpha-specific profiler; it is the demonstration that high-quality profiling can be designed as continuously running systems infrastructure.

## Key ideas

1. **Profiling can be always-on rather than episodic.** If collection overhead is sufficiently low, production execution itself becomes the measurement environment instead of relying on specially reproduced runs.
2. **Statistical sampling is a powerful systems tradeoff.** Sparse samples can estimate where time is spent while avoiding the cost of tracing every event or function call.
3. **Whole-system visibility matters.** Application code, libraries, drivers, and the kernel contribute to one end-to-end latency or CPU budget; profiling only the application can miss the real bottleneck.
4. **Collection and interpretation should be separated.** Keep the hot-path collector small and cheap; do symbolization, aggregation, model-based attribution, and explanation later.
5. **Observability must measure its own perturbation.** CPU cost, memory, buffering, storage, dropped samples, and sampling bias are part of the correctness of a profiling system, not secondary implementation details.

## Connection to Linux, eBPF, and Aruba datapath work

This paper maps directly to Linux `perf`, hardware PMU sampling, eBPF profiling, and the design of a low-overhead datapath flight recorder.

Suppose an Aruba gateway shows intermittent CPU saturation, but the issue disappears when heavy tracing is enabled. A high-volume event trace may perturb scheduler behavior, cache locality, queueing, and packet timing enough to change the failure itself. DCPI's approach suggests a different first layer of evidence:

```text
PMU / timer samples
        ↓
per-CPU compact records
        ↓
process + symbol + kernel context
        ↓
post-processing
        ↓
where CPU cycles / misses / stalls accumulated
```

For a Linux datapath, this lets you distinguish questions such as:

```text
Is packet processing genuinely CPU-bound?
Is time concentrated in one lookup or policy path?
Are cycles actually being lost to cache misses?
Is a kernel path, interrupt path, or user process responsible?
Did a rare failure coincide with a different execution profile?
```

The paper also gives a useful design rule for eBPF observability. An always-on recorder should avoid doing expensive analysis in the probe itself. Capture compact evidence—timestamps, IDs, counters, sampled stack/context, state-transition identifiers—and move expensive correlation and explanation to user space or offline analysis. This preserves the principle that the observer should disturb the datapath as little as possible.

For a Vigil-style flight recorder, continuous profiling and event-triggered evidence complement each other:

```text
continuous low-rate sampling
        +
precise event-triggered snapshots
        +
packet / state-transition evidence
        ↓
post-failure reconstruction
```

Sampling tells you where resources were going over time; targeted probes tell you what semantic state changed. Combining the two is much more useful than treating tracing and profiling as separate debugging worlds.

## Reading recommendation

**Read fully.** Sections 4 and 6 deserve the most attention. In Section 5, understand the overhead methodology and aggregate results but do not memorize Alpha-specific constants or every table entry.

**Estimated reading time:** 50–70 minutes; 80–100 minutes if you work through the instruction-level analysis and sampling-accuracy arguments in detail.

## Related papers in this library

- OBS-001 — Dapper, a Large-Scale Distributed Systems Tracing Infrastructure
- OBS-002 — Dynamic Instrumentation of Production Systems
- OBS-003 — gprof: A Call Graph Execution Profiler
- DBG-003 — Valgrind: A Framework for Heavyweight Dynamic Binary Instrumentation
- CA-003 — An Efficient Algorithm for Exploiting Multiple Arithmetic Units
- COMP-004 — LLVM: A Compilation Framework for Lifelong Program Analysis & Transformation
