# SEC-003 — A Note on the Confinement Problem

- **Author:** Butler W. Lampson
- **Year:** 1973
- **Field:** Computer Security / Confinement / Information Flow / Covert Channels
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-08
- **Primary source:** https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/acrobat-24.pdf
- **DOI:** https://doi.org/10.1145/362375.362389
- **Published in:** Communications of the ACM, 16(10), 613–615

## Why it matters

Lampson's short note isolates a security problem that ordinary access control does not solve: a program may be allowed to read sensitive input and still be untrustworthy about what it does with that information. Even if the operating system blocks unauthorized file or memory access, the program may leak data through other mechanisms.

The paper names this the **confinement problem** and systematically explores escape paths. Some are obvious, such as writing a file or sending an IPC message. Others are much subtler: lock state, resource consumption, paging behavior, system load, timing, or any shared mechanism that another process can observe. Lampson classifies these as storage channels, legitimate channels, and **covert channels**—channels not intended for information transfer at all.

This is foundational to information-flow security, sandboxing, multi-tenant isolation, covert-channel analysis, and the general idea that preventing direct access is not the same as preventing information leakage.

## Prerequisites

- basic operating-system protection and privilege separation
- processes, files, IPC, and shared resources
- access control at a conceptual level
- basic idea of timing/resource side channels
- trusted versus untrusted code

## Reading guide

### Introduction
Read fully. The central distinction appears immediately: traditional protection can prevent an untrusted service from reading arbitrary customer data, but once the customer intentionally supplies sensitive input to that service, access control alone cannot ensure the service will not leak it.

### The Problem
Read very carefully. Lampson enumerates concrete leakage mechanisms, beginning with persistent memory, files, and IPC and moving toward less obvious channels based on file interlocks and shared system performance.

Spend particular time on examples 5 and 6. They show why the confinement problem is difficult: a mechanism does not need to have been designed for communication in order to carry information.

### Confinement Rules
Read fully. This section develops the main principles:

- a confined program should not retain state across calls;
- **total isolation** would be sufficient but is impractical;
- **transitivity** requires untrusted programs called by a confined program to be confined as well;
- all channels exposed by trusted supervisory code must be considered;
- **masking** lets the caller determine the confined program's inputs to legitimate and covert channels;
- **enforcement** requires the supervisor to make the actual channel behavior conform to those constraints.

The paper also makes an important pragmatic point: completely eliminating some covert channels may be prohibitively expensive, so a system may instead bound their capacity.

### Summary
Read fully. It is brief and restates the taxonomy: retained state, supervisor-provided storage, legitimate outputs, and unintended channels can all become leakage paths.

## Key ideas

1. **Access control is not information-flow control.** A program can be legitimately given a secret and still leak it.
2. **Confinement is transitive.** If confined code invokes untrusted code, that code must inherit the confinement requirement or become an escape route.
3. **Shared mechanisms can become communication mechanisms.** Locks, scheduling, paging, CPU load, I/O behavior, or other observable resources may encode information even when they were never designed as channels.
4. **Covert channels are an architectural property.** They arise from what different principals can influence and observe, not merely from explicit APIs such as files or sockets.
5. **Perfect isolation may be too expensive.** Sometimes the engineering goal is to reduce or bound channel capacity rather than claim that every possible leak has been eliminated.

## Connection to Linux and Aruba networking work

This paper is directly relevant when evaluating isolation boundaries in Linux or a multi-tenant networking datapath.

Suppose two logically isolated clients, containers, services, or tenants cannot access one another's memory, files, or sockets. That does not by itself prove strong isolation if they still share observable state such as queues, counters, caches, CPU scheduling, packet-processing resources, rate limiters, buffer pools, or timing-sensitive control-plane behavior.

For example, in a gateway datapath the security review should distinguish:

```text
explicit channel:   packet / socket / IPC / shared map
shared state:       counter / queue / cache / resource pool
observable effect:  latency / drops / throughput / scheduling
```

The confinement mindset asks two questions for every shared mechanism: **what can one principal influence, and what can another principal observe?** If both are true, the mechanism deserves analysis as a possible information channel even if its normal purpose is unrelated to communication.

The same reasoning applies to Linux sandboxes, namespaces, seccomp, cgroups, containers, eBPF maps, and shared kernel subsystems. These mechanisms may strongly restrict authority while still requiring separate analysis of information leakage through shared resources.

## Reading recommendation

**Read fully.** The paper is only a few pages long, and the examples are the main value rather than material to skim.

**Estimated reading time:** 15–25 minutes; about 35 minutes if you stop to map each leakage example to a modern Linux mechanism.

## Related papers in this library

- SEC-001 — The Protection of Information in Computer Systems
- SEC-002 — Reflections on Trusting Trust
- OS-004 — Exokernel: An Operating System Architecture for Application-Level Resource Management
- OBS-002 — Dynamic Instrumentation of Production Systems
