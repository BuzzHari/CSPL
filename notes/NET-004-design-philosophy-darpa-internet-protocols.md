# NET-004 — The Design Philosophy of the DARPA Internet Protocols

- **Author:** David D. Clark
- **Year:** 1988
- **Field:** Computer Networking / Internet Architecture / Protocol Design
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-02
- **Primary source:** https://groups.csail.mit.edu/ana/People/DDC/lbook-arch-V1.pdf
- **Original publication:** ACM SIGCOMM 1988

## Why it matters

Clark reconstructs the design priorities that shaped TCP/IP and explains why the Internet uses connectionless datagrams, heterogeneous underlying networks, endpoint-held transport state, and relatively simple gateways. The paper is especially important because it makes the ordering of architectural goals explicit: survivability came first, followed by support for multiple service types and heterogeneous networks, while cost, ease of attachment, and accountability were lower priorities.

The paper also introduced the enduring notion of **fate-sharing**: critical communication state should be placed in an entity that will fail at the same time as the state becomes useless. This helps explain why transport state is kept at endpoints rather than in routers.

## Prerequisites

- IP datagrams and routing
- TCP at a conceptual level
- packet switching
- connection-oriented vs. connectionless service
- end hosts vs. routers/gateways

## Reading guide

### 1. Introduction
Read fully. Separate architectural goals from mechanisms. Gateways and datagrams are design consequences, not goals in themselves.

### 2–3. Fundamental and second-level goals
Read very carefully. The ordering of goals is the central systems-design lesson: a different priority ordering would have produced a different Internet.

### 4. Survivability
Read extremely carefully. Focus on endpoint state and **fate-sharing**. Understand why keeping essential transport state in routers would make router failure destroy otherwise recoverable communication.

### 5. Types of service
Read fully. Note that the architecture needed to support services with different reliability and latency needs rather than assuming one universal transport behavior.

### 6–8. Network variety, distributed management, cost/accountability
Read selectively. These sections show how heterogeneity and decentralized operation constrained the architecture.

### Conclusion
Read fully. Be able to explain why datagrams, stateless gateways, and endpoint transport state follow from the original goals.

## Key ideas

1. **Architectural goals need an explicit priority order.** Requirements conflict; the ordering determines the design.
2. **Fate-share critical state with the entity that needs it.** State should not disappear merely because an intermediate component failed.
3. **A weak internetwork layer enables heterogeneity.** IP asks relatively little of the networks below it.
4. **Mechanisms are consequences of goals.** Datagrams and gateways make sense only in the context of the requirements they satisfy.
5. **Successful architectures preserve historical tradeoffs.** Security and accountability were not top original priorities, which helps explain later retrofit challenges.

## Linux / Aruba connection

For a WLAN/network datapath, fate-sharing is a useful way to review state placement across APs, gateways, datapath processes, control-plane services, and cloud/controller components. For every client/authentication/bridge/tunnel/flow state item, ask: if this component fails, should that state disappear? If the operation is expected to survive the component, keeping the only authoritative copy there is architecturally suspicious.

This is also a debugging heuristic for roam and failover bugs: enumerate state ownership and compare it with intended failure semantics.

## Related papers

- NET-002 — A Protocol for Packet Network Intercommunication
- NET-003 — Congestion Avoidance and Control
- ARCH-001 — End-to-End Arguments in System Design
- DS-003 — Time, Clocks, and the Ordering of Events in a Distributed System
