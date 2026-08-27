# DBG-002 — Simplifying and Isolating Failure-Inducing Input

- **Authors:** Andreas Zeller, Ralf Hildebrandt
- **Year:** 2002
- **Field:** Debugging / Automated Debugging / Software Testing
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://www.st.cs.uni-saarland.de/papers/tse2002/
- **DOI:** https://doi.org/10.1109/32.988498

## Why it matters

This paper established Delta Debugging as a practical, general method for automatically reducing a failure-inducing test case to a small set of circumstances that still reproduces the same failure. Instead of asking an engineer to manually delete inputs, actions, or configuration changes until the bug disappears, Delta Debugging repeatedly runs an automated test while systematically partitioning the difference between passing and failing cases.

The paper's Mozilla case study reduced a failure sequence of 95 user actions to three relevant actions, and reduced 896 lines of HTML to the single failure-inducing line. The deeper contribution is a reusable debugging abstraction: when failure can be tested automatically, the search for a minimal failure-inducing difference can itself be automated.

## Prerequisites

- Basic software testing and regression testing
- Deterministic or sufficiently reproducible failures
- Sets, subsets, and divide-and-conquer reasoning
- Basic understanding of test harnesses and automated pass/fail oracles

## Key ideas

1. **Debugging as experimental search** — repeatedly change circumstances, run the program, and use the observed outcome to narrow the causal search space.
2. **Failure-inducing input minimization** — `ddmin` finds a 1-minimal failing configuration: no single remaining subset element can be removed while preserving the failure under the chosen granularity/model.
3. **Passing and failing configurations define a difference** — Delta Debugging can isolate which changes distinguish a known-good execution from a known-bad one.
4. **Automation depends on a reliable test oracle** — the algorithm needs a machine-checkable outcome such as PASS, FAIL, or UNRESOLVED; ambiguous/non-reproducible outcomes complicate minimization.
5. **Minimal does not necessarily mean globally smallest or uniquely causal** — a 1-minimal result is a locally irreducible failure-inducing configuration under the tested decomposition, not necessarily the only or mathematically smallest explanation.

## Recommended reading approach

**Read fully.** The paper is approachable, the algorithms are directly useful, and the case studies make the formal model concrete.

### Section-by-section guide

- **1. Introduction:** Understand the central question: given a failing execution, which circumstances actually matter? Note the authors' goal of turning manual experimental debugging into an automated procedure.
- **2. Testing for Change:** Read carefully. Learn the formal model of configurations, decomposable changes, and the three-valued test outcome (`PASS`, `FAIL`, `UNRESOLVED`). This vocabulary drives the algorithms that follow.
- **3. Minimizing Test Cases:** This is the core section. Work through `ddmin`, understand how subsets and complements are tested, and distinguish 1-minimality from a globally minimum input.
- **4. Case Studies:** Read fully. The GCC, Mozilla, and fuzz examples show what the algorithm does when applied to real failure-inducing inputs and user interactions.
- **5. Isolating Failure-Inducing Differences:** Read carefully. This extends minimization from 'make the failing input small' to 'isolate the difference between a passing and failing configuration.'
- **6. Case Studies Revisited:** Read selectively but do not skip. It demonstrates the difference between pure minimization and isolation.
- **7. Related Work:** Skim on the first pass.
- **8. Future Work:** Read briefly for limitations and possible generalizations beyond program input.
- **9. Conclusion:** Revisit the authors' argument that automatic simplification should become part of automated testing whenever failures have a repeatable oracle.

## A compact mental model

Suppose a packet-processing test reproduces a crash with 128 configuration changes or traffic actions:

```text
c1, c2, c3, ... c128  -> FAIL
```

Instead of removing one item at a time, Delta Debugging partitions the set and asks questions such as:

```text
first 64 changes  -> PASS?
second 64 changes -> FAIL?
```

It recursively narrows the difference, adapting the granularity when neither simple half explains the failure. The output is a much smaller reproducible case that an engineer can inspect directly.

## Connection to Linux / Aruba networking work

This paper is directly applicable to rare datapath and control-plane failures where the initial reproducer contains too much irrelevant context.

Examples include minimizing:

- a long packet capture or packet sequence that triggers a crash;
- a configuration diff containing dozens of unrelated commands;
- a client roam/authentication sequence with many preceding events;
- a set of enabled features needed to reproduce a forwarding bug;
- a sequence of API/CLI operations that leads to inconsistent state;
- a collection of log-triggered replay events for an offline reproducer.

A practical workflow could be:

```text
large reproducer
      ↓
automated replay in lab/VM
      ↓
PASS / FAIL oracle
      ↓
delta-debug partitions
      ↓
small reproducer
      ↓
packet/eBPF/source-level investigation
```

For example, if an Aruba gateway crashes only after a 200-packet trace is replayed, the test oracle can be 'does the target process crash with the same signature?' Delta Debugging can then automatically determine whether 200 packets can be reduced to 20, five, or perhaps a single malformed transition. The same method can minimize an AOS configuration or a sequence of roam/control-plane events.

This is complementary to observability: tracing helps capture what happened, while Delta Debugging helps reduce a reproducible failure to the smallest experimentally relevant circumstances.

## Estimated reading time

- Focused first read: 50–70 minutes
- With hand-tracing of `ddmin` and case studies: 90–120 minutes

## Questions to answer after reading

1. What exactly does 1-minimal mean, and how is it weaker than globally minimum?
2. Why does the algorithm need an `UNRESOLVED` outcome in addition to PASS and FAIL?
3. Under what assumptions can removing input fragments change the *kind* of failure being observed?
4. How would you define a robust failure oracle for a crash, packet drop, latency regression, or stale-client-state bug?
5. Which artifacts in a networking bug report could be automatically delta-debugged today?

## Related indexed papers

- DBG-001 — Eraser: A Dynamic Data Race Detector for Multithreaded Programs
- OBS-002 — Dynamic Instrumentation of Production Systems
- ALG-001 — Quicksort
