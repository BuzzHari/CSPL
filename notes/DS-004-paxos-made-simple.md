# DS-004 — Paxos Made Simple

- **Author:** Leslie Lamport
- **Year:** 2001
- **Field:** Distributed Systems / Consensus / Fault Tolerance
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://www.microsoft.com/en-us/research/publication/paxos-made-simple/
- **Author bibliography:** https://lamport.azurewebsites.net/pubs/pubs.html

## Why it matters

Paxos Made Simple gives the compact derivation of Paxos, one of the foundational crash-fault consensus protocols in distributed systems. Paxos provides a way for a collection of processes to agree on one value despite message delay, duplication, reordering, and the failure and recovery of participants, provided a majority of acceptors can communicate.

The paper matters because consensus sits underneath replicated state machines, metadata services, coordinators, configuration stores, distributed databases, and many systems that must keep multiple machines from making contradictory decisions after failures.

## Prerequisites

- Basic distributed-systems failure model
- Reliable versus unreliable communication at a conceptual level
- Quorums and majorities
- Replication
- Leader/coordinator concepts
- Safety versus liveness

Reading DS-003, *Time, Clocks, and the Ordering of Events in a Distributed System*, first is useful but not required.

## Key ideas

1. **Separate safety from progress** — Paxos first guarantees that two different values cannot both be chosen; liveness depends on additional assumptions such as eventual leadership and communication.
2. **Majority intersection is the foundation** — any two majorities overlap, so information carried by one successful round cannot be completely forgotten by a later successful round.
3. **Proposal numbers impose rounds** — higher-numbered proposals supersede lower-numbered attempts while preserving values that may already have been chosen.
4. **Prepare before accept** — a proposer first learns enough history from a majority, then selects a value consistent with that history before asking acceptors to accept it.
5. **Consensus is a building block** — repeated consensus instances can order commands for a replicated state machine, which is the practical route from single-value Paxos to a fault-tolerant service.

## Reading approach

**Read fully.** It is short, but do not rush the derivation. The value of the paper is seeing why each rule is forced by the safety requirement.

### 1. The Problem

Understand the participants—proposers, acceptors, and learners—and the goal that exactly one value may be chosen while allowing multiple competing proposers and failures.

### 2. Choosing a Value

This is the core of the paper. Follow the progression of safety properties P1, P2, P2a, P2b, and P2c. Do not memorize the labels; understand why each attempted simplification is insufficient and why a proposer must consult a majority before issuing a higher-numbered proposal.

### 3. Learning a Chosen Value

Understand how learners discover the result and why the learning mechanism can be optimized independently from the core safety rules.

### 4. Progress

Read carefully. Paxos safety does not by itself guarantee that proposals stop colliding. A distinguished proposer/leader is used to obtain progress under suitable failure-detection assumptions.

### 5. The Implementation

Connect the abstract algorithm to persistent acceptor state, message handlers, and crash recovery. Proposal/acceptance information that affects safety must survive restart.

## A compact mental model

Phase 1 — Prepare / Promise:

```text
Proposer:  prepare(n) ───────────────► acceptor majority

Acceptors:
  promise not to accept proposals < n
  return highest proposal/value already accepted
```

Phase 2 — Accept:

```text
Proposer chooses:
  value from highest-numbered prior accepted proposal,
  or its own value if none exists

Proposer: accept(n, value) ──────────► acceptor majority
```

Once a majority accepts the same proposal, its value is chosen.

The critical structural fact is:

```text
any majority ∩ any later majority ≠ ∅
```

so a later round must encounter at least one participant carrying evidence relevant to an earlier chosen value.

## Connection to Linux / Aruba networking software

The direct connection is control-plane state that must remain singular and consistent across redundant controllers, gateways, or services.

Suppose two nodes can both become responsible for programming a client or tunnel after a failure. Without an agreement mechanism, partitions or delayed messages can allow contradictory decisions:

```text
node A: client generation 42 belongs on gateway A
node B: client generation 42 belongs on gateway B
```

The Paxos lesson is not simply “use Paxos everywhere.” It is to identify state for which split-brain decisions are unacceptable and make the ownership/ordering rule explicit. Examples include leader election, cluster configuration, generation numbers, replicated metadata, or any operation where two independently committed outcomes would violate correctness.

For debugging, it also suggests logging proposal/term or generation identifiers rather than relying only on timestamps. Seeing that two components acted under different epochs is often much more diagnostic than seeing that their log lines occurred milliseconds apart.

## Questions to answer after reading

1. Why is a majority required rather than any fixed number of acceptors?
2. Why can a proposer not simply choose an arbitrary value in every new round?
3. What exact information must an acceptor persist across crashes?
4. Which parts of Paxos establish safety, and which parts are only for progress?
5. How does repeated consensus become a replicated state machine?
6. What failure does a leader solve, and what failure does it not solve?

## Related indexed papers

- DS-003 — Time, Clocks, and the Ordering of Events in a Distributed System
- DS-002 — The Google File System
- ARCH-001 — End-to-End Arguments in System Design
