# ARCH-002 — On the Criteria To Be Used in Decomposing Systems into Modules

- **Author:** D. L. Parnas
- **Year:** 1972
- **Field:** Software Architecture / Modularity / Software Engineering
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://doi.org/10.1145/361598.361623
- **DOI:** 10.1145/361598.361623

## Why it matters

Parnas showed that modularity is not primarily about splitting a program into a convenient set of processing steps. The crucial design choice is *what decisions each module hides from the rest of the system*. He compares two decompositions of the same system and argues that modules organized around hidden design decisions are easier to change, understand, and develop independently.

This paper is one of the foundations of information hiding, encapsulation, stable interfaces, and modern software architecture. Its central lesson survives changes in programming languages, object-oriented design, services, plugins, and distributed systems: isolate volatile knowledge behind boundaries whose contracts remain stable.

## Prerequisites

- Functions and modules
- Interfaces and implementation details
- Basic software maintenance concepts
- Familiarity with changing requirements and parallel development

No advanced theory is required.

## Key ideas

1. **Decompose by hidden design decisions, not execution steps.** A module should encapsulate a decision likely to change, such as data representation, device formatting, or an algorithmic choice.
2. **Information hiding is stronger than merely grouping functions.** The important property is which facts other modules are *not allowed to depend on*.
3. **Interfaces should expose assumptions that are unlikely to change.** Volatile implementation choices belong behind those interfaces.
4. **Good modularization localizes change.** When a hidden decision changes, ideally only one module needs modification.
5. **Modularity is an architecture property.** A system can have many source files or functions and still be poorly modular if internal decisions leak across boundaries.

## Recommended reading approach

**Read fully.** It is only a few pages and the comparison between the two decompositions is the point of the paper.

### Section-by-section guide

- **Introduction:** Note the goals Parnas assigns to modularity: managerial independence, product flexibility, and comprehensibility.
- **Example system:** Understand the KWIC indexing problem well enough to see why multiple decompositions are possible.
- **First decomposition:** Observe that modules mirror the sequence of processing steps. Ask what representation and algorithmic assumptions leak between modules.
- **Second decomposition:** Focus on which design decision each module conceals and what its interface exposes.
- **Comparison:** This is the core. Track which modules must change under alternative storage formats, input formats, algorithms, or output requirements.
- **Efficiency discussion:** Do not skip it. Parnas explicitly addresses the concern that better abstraction boundaries may add overhead and shows how implementation techniques can mitigate it.
- **Conclusion:** Translate the criteria into a rule you could use in a design review: identify decisions likely to change and assign each to a module that hides it.

## Estimated reading time

- First focused read: 30–45 minutes
- With a decomposition exercise: 60–90 minutes

## Connection to Linux and Aruba networking software

This paper is directly applicable to datapath and observability architecture. Suppose one diagnostic system reads `/proc`, another attaches eBPF probes, another parses controller CLIs, and another consumes packet captures. A weak decomposition organizes the software around workflow steps such as `collect -> parse -> analyze -> report`, while allowing every stage to know details of `/proc` paths, eBPF map formats, CLI text, and device-version quirks.

A Parnas-style decomposition instead hides volatile decisions behind components such as `ProcessStateSource`, `PacketEventSource`, `ClientStateSource`, or `TraceStore`. Consumers depend on stable semantic contracts rather than knowing whether a value came from `/proc`, an eBPF map, a CLI command, or a future telemetry API.

This is especially important in Aruba software because hardware generations, AOS versions, datapath implementations, commands, and instrumentation mechanisms change. The architecture should make those changes local rather than forcing them through every debugging or analysis workflow.

## Questions to answer after reading

1. What is the difference between a module and a processing step?
2. Which design decisions are most likely to change in your current system?
3. Which interfaces currently leak storage formats, device details, or implementation mechanisms?
4. Can a module be well encapsulated even if it contains several processing phases?
5. Which dependencies would disappear if consumers depended on semantic interfaces instead of raw data representations?

## Related indexed papers

- ARCH-001 — End-to-End Arguments in System Design
- OS-001 — The UNIX Time-Sharing System
- COMP-001 — Efficiently Computing Static Single Assignment Form and the Control Dependence Graph
