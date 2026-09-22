# DS-006 — Impossibility of Distributed Consensus with One Faulty Process

- **Authors:** Michael J. Fischer, Nancy A. Lynch, Michael S. Paterson
- **Year:** 1985
- **Field:** Distributed Systems / Consensus / Fault Tolerance / Impossibility Results
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-22
- **Primary source:** https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf
- **DOI:** https://doi.org/10.1145/3149.214121
- **Published in:** Journal of the ACM, 32(2), 374–382

## Why it matters

This paper establishes one of the most important limits in distributed computing: in a completely asynchronous message-passing system, no deterministic consensus protocol can guarantee termination if even one process may crash.

The result is usually called **FLP impossibility**, after Fischer, Lynch, and Paterson. It does not say that consensus is useless or that practical systems cannot reach agreement. It says that three properties cannot all be guaranteed under the paper's model: deterministic consensus, complete asynchrony, and guaranteed termination despite one crash failure.

The paper therefore changes how consensus protocols should be understood. Paxos, Raft, failure detectors, timeouts, partial-synchrony models, randomized consensus, leases, and practical leader-election mechanisms do not somehow refute FLP; they obtain liveness by adding assumptions or weakening guarantees that FLP deliberately excludes.

The proof is also worth learning as a general technique. Rather than enumerating protocols, the authors reason over all possible deterministic protocols by classifying global configurations according to which decisions remain reachable and showing that an adversarial but admissible message schedule can keep the system forever in an undecided state.

## Prerequisites

- asynchronous message passing
- deterministic state machines
- crash-stop failures
- consensus at the level of agreement, validity, and termination
- basic proof by contradiction and induction
- familiarity with `DS-003` (logical clocks), `DS-004` (Paxos), and `DS-005` (Byzantine Generals) is helpful but not required

## Reading guide

### 1. Introduction — read fully

Start by reading the assumptions with unusual care. The result depends on **complete asynchrony**: there is no bound on process speed or message delay, no synchronized clock, and no reliable way to distinguish a crashed process from one that is merely slow. Messages themselves are reliable in the model and processes fail only by stopping, so the theorem is already strong under a relatively benign failure model.

The central conclusion appears early: even one unannounced process death can leave a consensus protocol unable to guarantee progress. Pay attention to the paper's description of a protocol's unavoidable "window of vulnerability."

### 2. Consensus Protocols — read carefully

This section defines the formal model used by the proof. A global **configuration** consists of every process's local state plus the messages currently in transit. An **event** is essentially the delivery of one message to one process, followed by that process's deterministic transition and any messages it sends.

Understand four definitions:

- **schedule:** a sequence of events;
- **run:** the execution produced by a schedule;
- **admissible run:** at most one process is faulty and every message to a nonfaulty process is eventually delivered;
- **deciding run:** some process eventually enters a decision state.

Lemma 1 is a small but crucial commutativity result: steps performed by disjoint processes can be reordered without changing the final configuration. This lets the later proof rearrange schedules while preserving the relevant behavior.

### 3. Main Result — read extremely carefully

This is the heart of the paper.

The proof classifies each configuration by the decisions still reachable from it:

- **0-valent:** only decision 0 can still occur;
- **1-valent:** only decision 1 can still occur;
- **bivalent:** either 0 or 1 remains possible.

#### Lemma 2: a bivalent initial configuration exists

If every initial configuration were already 0-valent or 1-valent, consider a chain of initial configurations that changes one process's input at a time. Somewhere along that chain two adjacent configurations must have opposite valency. Now construct a run in which the one process whose input differs takes no steps. The rest of the system cannot distinguish those two starting configurations, creating a contradiction.

The important idea is **indistinguishability**: globally different executions may look identical to the processes that actually take steps.

#### Lemma 3: a critical event can be postponed while preserving bivalence

Take a bivalent configuration and an enabled event `e`. The authors show that there is a reachable configuration such that, after delaying `e` and doing other work first, applying `e` still leaves the system bivalent.

This is the technical core. It uses the commutativity lemma to show that if one event always forced the system from bivalent to univalent, neighboring executions could be reordered in ways that imply contradictory decision values.

#### Constructing the nondeciding run

Starting from a bivalent initial configuration, repeatedly choose a process/message event that fairness eventually requires, schedule enough other events to preserve bivalence, then execute the required event while remaining bivalent.

The constructed infinite run is still admissible: every nonfaulty process continues taking steps and every message to a nonfaulty process is eventually delivered. Yet the system never reaches a decision, contradicting guaranteed termination.

Do not reduce the theorem to the slogan "consensus is impossible." The precise statement is that **no deterministic consensus protocol can guarantee termination in every admissible execution of this fully asynchronous crash-failure model**.

### 4. Initially Dead Processes — read selectively

This section is useful because it separates the hard case from a nearby solvable case. The authors give a protocol that works when a strict majority is initially alive and no additional process dies during execution.

The lesson is that *when* failures may occur matters. FLP's impossibility comes from uncertainty that persists while the protocol is executing; if the failure pattern is restricted enough, agreement can again be guaranteed.

Read the graph construction once, but do not spend much time memorizing it on the first pass.

### 5. Conclusion — read fully

The final paragraph is unusually important. The authors explicitly say that the result does **not** mean practical distributed agreement cannot be achieved. Instead, it motivates more realistic timing models and weaker termination requirements, including randomized approaches.

That is exactly how later systems escaped the theorem's conditions.

## Key ideas

1. **Asynchrony makes a crashed process indistinguishable from an arbitrarily slow one.** Without timing assumptions, waiting longer cannot prove that a peer has failed.
2. **Safety and liveness are different kinds of guarantees.** A protocol can preserve agreement while an adversarial schedule prevents it from ever deciding.
3. **Bivalence captures unresolved global choice.** FLP shows an admissible execution can be constructed that keeps the system bivalent forever.
4. **Indistinguishability and commutativity are powerful impossibility-proof tools.** The argument reasons about what processes can observe rather than about the internal structure of any one protocol.
5. **Practical consensus works by changing the model.** Timeouts, partial synchrony, leader leases, failure detectors, randomness, and operational assumptions provide the extra structure needed for progress.

## Connection to Linux / Aruba networking work

The strongest connection is to clustered gateways, controllers, and other distributed control-plane state.

Suppose two gateways must agree on which one owns a client after a roam. One gateway stops hearing from the other:

```text
GW1                           GW2
 |                             |
 |------ ownership update ---->|
 |                             |
 |<----- no response ----------|
```

From GW1's local view, several realities may be indistinguishable:

- GW2 crashed;
- GW2 is alive but CPU-starved;
- the control message is delayed;
- the acknowledgement is delayed;
- a tunnel or control channel is temporarily stalled.

In a truly asynchronous model, no timeout value can prove which explanation is correct. A timeout is therefore not a fact about failure; it is an **additional timing assumption encoded as policy**.

That distinction is useful when debugging cluster failover, AP/gateway ownership changes, stale client state, or split-brain-like symptoms. If one component changes ownership because a peer exceeded a timeout, capture the evidence that made the system cross that timing threshold: send time, receive time, retransmissions, peer liveness state, epochs/generations, and the state transition triggered by the timeout.

It also matters for diagnostic architecture. A flight recorder should distinguish:

```text
"peer was proven dead"
```

from the much more common operational statement:

```text
"peer failed to respond within the system's chosen bound"
```

FLP explains why that difference is not semantic nitpicking; it is fundamental to distributed-system correctness.

## What to retain after reading

You should be able to state the FLP assumptions precisely, explain what 0-valent, 1-valent, and bivalent configurations mean, outline why a bivalent initial configuration must exist, and explain how an adversarial but fair schedule can postpone the decisive event forever.

Most importantly, be able to explain why Paxos or Raft does not contradict FLP: their safety properties can hold under asynchrony, while guaranteed liveness requires additional timing/failure assumptions about the execution.

## Reading recommendation

Read Sections 1–3 and 5 fully. Read Section 4 selectively on the first pass. The paper is short, but Section 3 deserves a slow second reading; tracing Lemmas 2 and 3 on paper is more valuable than rushing through the proof.