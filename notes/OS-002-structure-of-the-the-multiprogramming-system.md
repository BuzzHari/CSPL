# OS-002 — The Structure of the “THE”-Multiprogramming System

- **Author:** Edsger W. Dijkstra
- **Year:** 1968
- **Field:** Operating Systems / Layered Architecture / Concurrency
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD196.html
- **DOI:** https://doi.org/10.1145/363095.363143

## Why it matters

This paper is a foundational statement of hierarchical operating-system design. Dijkstra describes the THE multiprogramming system as a stack of ordered abstraction levels, where each level depends only on lower levels whose correctness can be understood independently. The design was motivated not merely by implementation convenience, but by the need to make a concurrent operating system intellectually manageable and verifiable.

The paper helped establish layered system structure as a general technique for controlling complexity. Its influence extends beyond operating systems to protocol stacks, virtual machines, storage layers, middleware, and software architecture.

## Prerequisites

- Processes and multiprogramming
- Interrupts and peripheral I/O at a conceptual level
- Mutual exclusion / semaphores at a basic level
- Memory hierarchy and paging at a conceptual level
- Basic software abstraction and modularity

## Key ideas

1. **Hierarchical layering controls dependencies.** Higher layers use abstractions implemented by lower layers rather than depending directly on all system mechanisms.
2. **Each layer should create a more convenient abstract machine.** The goal is not simply code organization; each level hides details and raises the conceptual level for the next.
3. **Concurrency requires disciplined structure.** When multiple sequential processes interact, uncontrolled cross-dependencies quickly make reasoning about correctness intractable.
4. **Design for verification, not just execution.** The architecture is deliberately organized so that the logical soundness of one level can be established assuming the correctness of lower levels.
5. **Resource management can be separated by level.** Processor allocation, memory management, communication, and I/O can be assigned to distinct strata with explicit responsibilities.

## Recommended reading approach

**Read fully.** The published paper is only a few pages long, but its terminology is historical. Read slowly enough to translate each level into a modern operating-system concept.

### Section-by-section guide

- **Introduction:** Focus on Dijkstra’s stated goal of gaining experience in system conception, construction, and verification with a very small team.
- **Tool and goal:** Understand the EL X8 hardware constraints and why multiprogramming was chosen.
- **Sequential processes and synchronization:** Read carefully. The system is described in terms of cooperating sequential processes whose relative speeds are deliberately unspecified.
- **Hierarchy of levels:** This is the core of the paper. Track what abstraction each level provides and which lower-level details it hides.
- **Level 0:** Processor allocation and synchronization. Think of this as establishing the basic virtual processor environment for higher layers.
- **Level 1:** Memory allocation / segment management. Higher levels can reason about memory without directly managing drum transfers and physical placement.
- **Level 2:** Communication with operator consoles and related coordination.
- **Level 3:** I/O buffering and peripheral abstractions.
- **Level 4 and user programs:** Observe how successive layers transform the raw machine into progressively more convenient abstract machines.
- **Concluding discussion:** Revisit the claim that the hierarchy made verification and testing substantially more tractable.

## Estimated reading time

- Focused first read: 30–45 minutes
- With notes and mapping to Linux subsystems: 60–90 minutes

## Connection to Linux and Aruba networking work

The paper is directly useful when designing a Linux-based diagnostic or datapath subsystem. A common failure mode in systems software is that every component learns too much about every other component: a collector knows CLI output details, an analyzer knows eBPF map layouts, a policy module knows tunnel internals, and a debugging layer reaches directly into implementation-specific shared memory.

A THE-style hierarchy asks instead: what abstract machine does each layer expose to the next?

For an Aruba observability architecture, a possible hierarchy might be:

1. **Raw mechanisms:** eBPF hooks, `/proc`, shared memory, packet capture, device CLI.
2. **Collection layer:** stable event and state-source interfaces.
3. **Normalization layer:** client, tunnel, route, bridge, and process-state models.
4. **Correlation layer:** causal relationships and lifecycle reconstruction.
5. **Diagnostic layer:** fault hypotheses and user-facing explanations.

The important constraint is that higher layers should not bypass lower abstractions casually. If the diagnostic engine directly depends on a particular eBPF map layout or CLI column number, the hierarchy has leaked and change becomes harder to contain.

This also applies inside datapath software: carefully ordered abstractions between hardware access, packet parsing, forwarding state, policy, tunneling, and control-plane integration reduce the number of cross-component assumptions that must be held in one engineer’s head during debugging.

## Questions to answer after reading

1. What abstraction does each THE level provide to the level above it?
2. Why does Dijkstra insist that process speeds remain unspecified?
3. How does the hierarchy reduce the number of interactions that must be considered simultaneously?
4. Which modern Linux subsystems fit naturally into a layered model, and which intentionally violate strict layering for performance?
5. When is bypassing a layer justified, and what architectural debt does that create?

## Related indexed papers

- OS-001 — The UNIX Time-Sharing System
- ARCH-002 — On the Criteria To Be Used in Decomposing Systems into Modules
- SEC-001 — The Protection of Information in Computer Systems
- COMP-001 — Efficiently Computing Static Single Assignment Form and the Control Dependence Graph
