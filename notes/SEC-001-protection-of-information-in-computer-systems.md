# SEC-001 — The Protection of Information in Computer Systems

- **Authors:** Jerome H. Saltzer, Michael D. Schroeder
- **Year:** 1975
- **Field:** Computer Security / Operating Systems / Protection Architecture
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://web.mit.edu/Saltzer/www/publications/protection/
- **Publication:** Proceedings of the IEEE, Volume 63, Issue 9, September 1975, pages 1278–1308

## Why it matters

This paper is one of the foundational works of computer security. It organized protection as an architectural problem rather than a collection of isolated countermeasures and articulated design principles that remain central to secure systems: least privilege, fail-safe defaults, complete mediation, economy of mechanism, open design, separation of privilege, least common mechanism, and psychological acceptability.

It also gives a rigorous treatment of authentication, authorization, access-control lists, capabilities, protection domains, revocation, protected subsystems, and the distinction between policy and mechanism.

## Prerequisites

- Basic operating-system concepts: processes, address spaces, files, and system calls
- User and kernel privilege levels
- Basic authentication and authorization concepts
- Familiarity with access permissions
- A conceptual understanding of shared multi-user systems

## Key ideas

1. **Least privilege** — every program and user should operate with only the privileges needed for the current task.
2. **Fail-safe defaults** — access should be denied unless it is explicitly permitted.
3. **Complete mediation** — every access to every protected object should be checked, not merely the first access.
4. **Economy of mechanism and open design** — security mechanisms should be small, understandable, and not depend on secrecy of their design.
5. **Policy–mechanism separation** — systems should distinguish what access is permitted from the machinery that enforces that decision.

## Recommended reading approach

**Read Section I fully; read Section II selectively on the first pass; skim Section III for historical context.**

### Abstract and introduction

Establish the paper’s scope. It focuses on architectural mechanisms required to prevent unauthorized use or modification of stored information, not only on cryptography or physical security.

### Section I — Basic principles of information protection

Read fully. This is the most durable and broadly applicable part of the paper.

Focus on:

- the goals of protection;
- design principles;
- authentication;
- authorization;
- protected objects and domains;
- why security must be designed as a system property.

Spend particular time on the eight design principles. For each one, identify a modern example and a violation.

### Section II — Descriptor-based protection systems

Read selectively during the first pass.

Prioritize:

- access-control lists versus capabilities;
- protection domains;
- controlled domain switching;
- revocation;
- protected subsystems and protected objects.

The detailed descriptor-machine examples are historically valuable but can be skimmed unless protection hardware or capability systems are your immediate focus.

### Section III — State of the art

Skim for historical perspective. Many named systems are dated, but the discussion shows which security problems were already understood in 1975 and which remained unresolved.

### Conclusion and glossary

Use the glossary while reading. Revisit the design principles after finishing the architectural sections.

## Estimated reading time

- Focused first pass: 75–100 minutes
- Full technical read with notes: 3–4 hours

## Connection to Linux and Aruba networking work

The principles map directly to Linux-based network appliances and engineering tooling:

- **Least privilege:** packet-capture, eBPF, device-access, and diagnostic tools should receive only the capabilities and device scope they require rather than unrestricted root access.
- **Complete mediation:** authorization should be checked on each sensitive operation, not only when a CLI session, API token, or device connection is first established.
- **Fail-safe defaults:** an unknown role, incomplete policy, failed authentication dependency, or malformed configuration should not silently grant broader forwarding or management access.
- **Least common mechanism:** avoid a single shared privileged agent, cache, credential, or mutable state store when narrower per-service mechanisms can reduce cross-component compromise.
- **Economy of mechanism:** security-critical datapath and control-plane enforcement should remain small enough to audit and reason about.

For `aructl`-style agent tooling, the paper provides a precise architectural warning: convenience integrations that can access Jira, repositories, devices, Jenkins, logs, and test systems should not automatically share one broad authority boundary. Each tool invocation should carry explicit identity, target, operation, and least-privilege authorization.

## Questions to answer after reading

1. How do protection and security differ in the paper’s terminology?
2. Why is checking permission only when an object is opened insufficient for complete mediation?
3. What are the practical trade-offs between access-control lists and capabilities?
4. Why does least privilege apply to time as well as scope?
5. Which modern systems violate least common mechanism for operational convenience?
6. How would you apply fail-safe defaults to authentication and role installation on a network gateway?

## Related indexed papers

- OS-001 — The UNIX Time-Sharing System
- ARCH-001 — End-to-End Arguments in System Design
