# SEC-004 — A Lattice Model of Secure Information Flow

- **Author:** Dorothy E. Denning
- **Year:** 1976
- **Field:** Computer Security / Information Flow Control / Lattice Security / Program Analysis
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-20
- **Primary source:** https://faculty.nps.edu/dedennin/publications/lattice76.pdf
- **DOI:** https://doi.org/10.1145/360051.360056
- **Published in:** Communications of the ACM, 19(5), 236–243

## Why it matters

Traditional access control answers “may this subject read or write this object now?” Denning asks a stricter question: after a process has legitimately read information, **where may information derived from it subsequently flow?**

The paper formalizes that question by assigning information to security classes and defining a permitted-flow relation between classes. Under natural consistency assumptions, those classes form a lattice. Combining inputs raises information to the least security class that can contain all of them, and a flow is legal only when the source class is permitted to flow to the destination.

The lasting contribution is not simply military classification labels. It is a reusable model of **information dependencies and dissemination**. The paper also distinguishes explicit flows caused directly by assignments or I/O from implicit flows carried by control decisions, and shows how the same model can support runtime checking, dynamic labels, and compile-time program certification.

This work is a direct bridge from early operating-system protection to modern information-flow control, taint analysis, security type systems, data-label propagation, and static analyses that reason about whether secrets can affect public outputs.

## Prerequisites

- access control and privilege separation
- basic partial orders; intuitive familiarity with least upper bounds and lattices is enough
- program control flow, assignments, conditionals, and loops
- basic data-flow and static-analysis ideas
- SEC-003 is useful context because it motivates why controlling information after legitimate access matters

## Reading guide

### 1. Introduction

Read fully. Focus on Denning’s distinction between immediate access control and end-to-end information flow. An access matrix can prevent an unauthorized read, but it does not by itself guarantee that a process legitimately allowed to read sensitive information will not later disseminate information derived from it.

### 2.1 Description

Read carefully. Understand the storage objects, processes, security classes, permitted-flow relation, and class-combining operator. Keep static binding and dynamic binding separate.

The crucial invariant is: if information derived from objects in classes A1 through An is written to another object, the combined source class must be permitted to flow to the destination’s class.

### 2.2 Derivation of Lattice Structure

Read for the argument rather than every symbol on the first pass. Reflexivity, transitivity, and antisymmetry make permitted flow a partial order; information combination behaves as a least upper bound. The lattice is not arbitrary mathematical decoration—it follows from consistency requirements about how information can be combined and propagated.

### 2.3 Examples

Read fully. The simple chain of classification levels and the powerset/category example make the lattice concrete. Notice that practical policies can be products of a confidentiality level and compartments or tags rather than a single total order.

### 3. Enforcement of Security

Read extremely carefully. This is the conceptual core for modern engineers. Distinguish **explicit flows** from **implicit flows** caused by control dependencies. In code such as `if secret then public := 1`, information about `secret` can reach `public` even though the right-hand side never reads `secret`.

Trace how the paper’s abstract program structures propagate these dependencies through sequencing and conditionals.

### 4. Mechanisms for Static Binding

Read selectively, but read the program-certification subsection carefully. The runtime mechanisms are historically interesting; the certification idea is enduring: perform flow analysis before execution, use the lattice in a compiler or static analyzer, and reject programs whose flows violate policy.

Also note the boundary of the guarantee. Certification reasons about the flows represented by the program model and therefore still depends on the correctness of the language implementation, runtime, and hardware.

### 5. Mechanisms for Dynamic Binding

Read selectively. The important insight is that simply raising a destination label when secret data is written is not sufficient, because implicit flows can occur even when an assignment does not execute. Changes in labels or visibility can themselves become observable and therefore leak information.

### 6. Conclusions

Read fully. Denning positions information-flow control as complementary to—not a replacement for—ordinary access control. The confinement and database examples show why it is useful to reason separately about authority to access information and authority to disseminate it.

## Key ideas

1. **Access control and information-flow control are different.** Permission to read a secret does not imply permission to later reveal information derived from it.
2. **Security labels need algebraic structure.** A lattice gives a principled way to order classes and compute the class of combined information.
3. **Implicit control dependencies are real information flows.** Branching on a secret can leak it through public state without a direct assignment from the secret.
4. **Enforcement can be dynamic or static.** Denning sketches runtime tracking and compile-time certification, anticipating modern taint analysis and security type systems.
5. **Information-flow control has a defined boundary.** It complements access control and does not by itself solve covert or timing channels, making SEC-003 a useful companion.

## Connection to Linux and Aruba networking work

The most useful connection is to **provenance-aware diagnostic telemetry and policy enforcement**.

An Aruba or Linux datapath may combine information from different trust domains:

- packet contents and headers from clients
- authentication and policy state
- tenant, VLAN, or VRF identity
- kernel or driver state
- eBPF maps
- control-plane secrets or tokens
- debug traces exported to user space or support bundles

Ordinary access control can make each object individually readable by a privileged datapath or diagnostic process. Denning’s question is what happens **after those inputs are combined**.

For example:

```text
client packet + secret policy state
              ↓
       diagnostic event
              ↓
      support telemetry
```

If the diagnostic event’s contents—or even its control-dependent presence—reveal secret policy state, the output has inherited information from the higher-sensitivity input. A robust design therefore needs data-classification and provenance rules, not merely “this process is privileged.”

A modern eBPF analogy is taint or label propagation: imagine map values or context fields carrying labels such as `tenant-private`, `control-plane-sensitive`, or `exportable`. Every combine, write, or sink operation could be checked against a policy lattice. Even if a real BPF program never implements a literal Denning lattice, the model is useful when deciding which state may be exported from kernel instrumentation, which packet metadata may cross tenant boundaries, and which diagnostics can safely leave a device.

It also complements SEC-003. Lampson asks which unintended channels can escape confinement; Denning provides a formal framework for allowed flows through intended storage and communication paths. Together they suggest a stronger review question: **what can this component access, what information can affect its outputs, and where are those outputs allowed to go?**

## Reading recommendation

**Read fully**, but skim some historical mechanism details in Sections 4–5 on the first pass.

**Estimated reading time:** 35–50 minutes; about 60 minutes if you work through the lattice derivation and implicit-flow rules carefully.

## Related papers in this library

- SEC-003 — A Note on the Confinement Problem
- SEC-001 — The Protection of Information in Computer Systems
- COMP-003 — A Unified Approach to Global Program Optimization
- OS-005 — Monitors: An Operating System Structuring Concept
