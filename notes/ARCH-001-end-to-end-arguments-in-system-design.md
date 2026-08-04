# ARCH-001 — End-to-End Arguments in System Design

- **Authors:** Jerome H. Saltzer, David P. Reed, David D. Clark
- **Year:** 1984
- **Field:** Systems Architecture / Computer Networking / Distributed Systems
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf
- **Official publication record:** https://web.mit.edu/saltzer/www/publications/pubs.html

## Why it matters

This paper introduced the end-to-end argument, one of the most influential principles in systems and network architecture. Its central claim is that some functions cannot be implemented completely and correctly inside lower layers because correctness ultimately depends on application-level knowledge available only at the endpoints.

Lower layers may still provide partial versions of those functions for performance or reliability, but those mechanisms do not remove the need for an end-to-end check. This reasoning influenced the architecture of the Internet, operating systems, distributed systems, storage, security, and application protocols.

## Prerequisites

- Layered system and protocol architecture
- Basic networking concepts: packets, links, hosts, and transport protocols
- Checksums and retransmission at a conceptual level
- File transfer and distributed application basics
- Distinction between correctness and performance optimization

## Key ideas

1. **Correctness belongs at the layer with complete knowledge** — only the application or endpoint may know whether the intended operation actually succeeded.
2. **Lower-layer reliability is often incomplete** — link checksums, retries, and replication can reduce failures but cannot prove application-level correctness.
3. **Duplicate functionality can be rational** — a lower layer may implement a function for efficiency even when the endpoint must implement it again for correctness.
4. **Function placement is a trade-off, not a slogan** — the principle structures design decisions but does not require a featureless network or substrate.
5. **End-to-end checks define the real success condition** — validate the result the application cares about, not merely intermediate delivery events.

## Recommended reading approach

**Read fully.** It is short, conceptually dense, and the examples are essential to understanding the argument's limits.

### Section-by-section guide

- **Introduction:** Identify the paper's main question: where in a layered system should a function be implemented?
- **Careful file transfer example:** Read closely. This is the clearest demonstration that reliable communication and storage components cannot independently guarantee a correct final file.
- **Performance aspects:** Note why lower-level checks and retries can still be justified even when endpoints must verify correctness.
- **Further examples:** Compare encryption, duplicate-message suppression, transaction processing, and delivery acknowledgement. For each example, ask which layer has enough semantic information to decide success.
- **Discussion and conclusion:** Focus on the authors' qualifications. The argument is a design heuristic about completeness and placement, not a prohibition on intelligent lower layers.

## Estimated reading time

- Focused first read: 35–50 minutes
- With case-by-case notes: 60–90 minutes

## Connection to Linux and Aruba networking work

The principle is directly relevant to datapath and control-plane debugging. A successful intermediate event does not necessarily prove end-to-end success:

- a packet entering the gateway does not prove delivery to the client;
- a tunnel encapsulation success counter does not prove decapsulation and application receipt;
- an ARP or neighbor entry does not prove the bridge path is usable;
- a successful authentication transaction does not prove subsequent policy installation and traffic forwarding;
- a configuration write acknowledgement does not prove the intended runtime state is active on every component.

For observability, the lesson is to instrument both intermediate mechanisms and the final semantic outcome. Datapath counters, eBPF traces, logs, and packet captures help locate failures, but the decisive check should represent what the user or application needed to happen.

## Questions to answer after reading

1. Why can reliable links not guarantee a correct file transfer?
2. When is lower-layer duplication of an endpoint function justified?
3. What is the difference between an acknowledgement of receipt and proof of successful application processing?
4. Which functions in a network appliance require endpoint or application-level validation?
5. Where can an over-simplified interpretation of the end-to-end argument lead to poor design?

## Related indexed papers

- NET-001 — The Click Modular Router
- DS-001 — MapReduce: Simplified Data Processing on Large Clusters
- DS-002 — The Google File System
