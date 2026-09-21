# EBPF-003 — Simple and Precise Static Analysis of Untrusted Linux Kernel Extensions

- **Authors:** Elazar Gershuni, Nadav Amit, Arie Gurfinkel, Nina Narodytska, Jorge A. Navas, Noam Rinetzky, Leonid Ryzhyk, Mooly Sagiv
- **Year:** 2019
- **Field:** eBPF / Static Analysis / Abstract Interpretation / Operating Systems
- **Status:** Queued
- **Priority:** Core
- **Recommended:** 2026-09-21
- **Primary source:** https://doi.org/10.1145/3314221.3314590
- **Author-hosted paper:** https://nadav.amit.zone/publications/pdfs/gershuni2019ebpf.pdf
- **Read:** Fully; skim some proof mechanics on the first pass
- **Estimated reading time:** 60–75 minutes; 90+ minutes if working through the abstract domains and soundness argument in detail

## Why this paper matters

The eBPF verifier is the mechanism that makes a remarkable systems bargain possible: allow user-supplied programs to execute inside the Linux kernel, but reject a program before loading it unless the kernel can establish that it is safe. That turns static analysis from a compiler optimization into part of a security boundary.

This 2019 PLDI paper studies the verifier problem as a program-analysis problem rather than as a collection of eBPF-specific heuristics. The authors identify several limitations of the Linux verifier of that era: path enumeration can explode, useful safe programs can be rejected because the analysis loses a relationship between variables, and loops were not generally accepted. They then build PREVAIL, a verifier based on abstract interpretation, and show that a carefully chosen abstraction can be both sound and practical for real eBPF programs.

The paper's most useful lesson is not that PREVAIL should replace today's Linux verifier. Mainline Linux has evolved substantially since the kernel 4.19 snapshot evaluated here, including major improvements in loop and function verification. The lasting contribution is the design reasoning: what information a verifier must retain, where precision is actually required, how joining abstract states avoids path explosion, and how a formal soundness argument constrains the implementation.

A central design choice is to represent a pointer as a memory-region identity plus an offset. eBPF's restricted execution environment makes those regions unusually tractable: stack, packet, map/value-like shared regions, and so on. The verifier can therefore reason precisely about the bounded stack while using coarser abstractions for regions where detailed byte-level contents are unnecessary.

The numerical domain matters just as much. Non-relational intervals are cheap but cannot express relationships such as `x - y <= C`, which arise naturally in packet bounds checks and pointer arithmetic. More expressive domains such as Octagons or Polyhedra can be expensive. The authors find that the Zone domain gives a useful middle ground. Their evaluation covers 192 real-world programs; Zone-based variants verify all but one, while the interval domain fails on many more. The prototype also demonstrates verification of loop-containing programs and better asymptotic behavior on path-explosion examples.

## Prerequisites

You should understand basic eBPF bytecode and the purpose of the Linux verifier, control-flow graphs, registers and pointer arithmetic, and the difference between proving a program safe and merely testing it. For the analysis sections, it helps to know the core idea of abstract interpretation: execute the program over an abstract state that conservatively over-approximates all concrete executions, join states at control-flow merges, and use widening or related convergence techniques around loops. Familiarity with intervals and data-flow fixed points is enough; you do not need prior expertise in Zones, Octagons, or Polyhedra.

`EBPF-001` gives the historical BPF virtual-machine lineage, `EBPF-002` gives the XDP/eBPF packet-processing architecture, and `COMP-003` gives useful background on fixed-point data-flow analysis.

## Section-by-section reading guide

### 1. Introduction — read fully

Start with the verifier's contract: accepting an unsafe program is a kernel-security failure, while rejecting a safe program is a false positive that makes the programming model harder to use. The authors want soundness without the path explosion and ad-hoc precision problems they observed in the Linux verifier of the time.

Pay particular attention to the two abstraction choices previewed here: region-plus-offset pointer representation, and a relational numerical domain. The evaluation summary is also useful because it tells you exactly what the rest of the paper must justify: precision, performance/scalability, and loop support.

### 2. Background on eBPF — read fully, but quickly if you already know eBPF

Review the execution model, register set, stack, packet access, maps/shared regions, helpers, and the load-time verification requirement. The important question is not how to write an eBPF program; it is what facts the verifier must establish before the program can safely run in kernel context.

Notice how eBPF's restrictions are an advantage for verification. The language is low level, but the verifier does not face arbitrary native code: the instruction set, control transfers, memory regions, and helper interface are constrained.

### 3. What makes eBPF verification difficult — read carefully

This is one of the most practically useful parts of the paper. Work through the examples rather than only reading the prose.

The first examples show why interval-like reasoning is insufficient. Bounds checks often depend on relationships between registers, not independent upper and lower bounds. The register-spilling example then shows why tracking only register facts is also insufficient: useful invariants can pass through the eBPF stack.

The loop/path-explosion example is particularly important. Enumerating paths can be attractive because each path is easy to reason about, but a modest amount of branching or an unrolled loop can make the number of paths grow much faster than the program itself. This motivates a fixed-point analysis that merges states at control-flow joins.

### 4. Programming Model — read carefully; do not memorize the notation

The paper defines a small eBPF-like language, eBPFPL, and an operational semantics whose error state captures the safety properties to be proved. This gives the later analyzer a precise target: if the abstract interpretation proves that the error state is unreachable, concrete execution is safe under the model.

Focus on the representation of pointers and memory regions and on why the authors separate region identity from numerical offset. The model also makes uninitialized memory explicit, because reading uninitialized bytes is itself unsafe and can leak kernel state.

### 5. Static Analysis — this is the core; read slowly

Understand the abstraction before following the formal rules. The analysis tracks both numerical values and abstract tags identifying pointer regions. Stack memory is modeled precisely enough to preserve spilled values and relationships; other safe regions can often be treated more coarsely.

Then focus on the numerical domain. A Zone can represent constraints of the form `X - Y <= C`, which is exactly the kind of relation needed for many pointer-range proofs. This is more expressive than independent intervals but cheaper than more general relational domains.

The key systems idea is the join at control-flow merges: instead of remembering every concrete path independently, the analyzer computes one conservative abstract state representing all of them. Around loops it computes a fixed point. Precision is deliberately traded against state-space growth, but soundness must never be traded away.

Read the soundness statements, especially Theorem 5.6, for the contract they establish. On a first pass, it is fine to skim the detailed lemma mechanics once you understand why the abstract transition relation over-approximates the concrete semantics.

### 6. Verifying eBPF Programs — read fully

This section turns the model into PREVAIL. The prototype translates eBPF binaries into a CFG-based language used by the Crab abstract-interpretation framework. Pay attention to the gap between mathematical integers in the formal model and 64-bit machine arithmetic in real eBPF. Integer and pointer overflow are not incidental implementation details; they can invalidate an otherwise convincing bounds proof.

This is a useful reminder for verifier engineering in general: a proof over an idealized arithmetic model is only valuable if the implementation preserves the proof assumptions of the real machine.

### 7. Empirical Results — read fully

The evaluation uses 192 programs from Linux, Open vSwitch, Suricata, and Cilium-related suites. Compare the abstract domains rather than only the raw timings. The interval domain is fast but too imprecise. Zone gives practically the same acceptance power as more expensive relational domains on these programs while running much more efficiently.

Also read the comparison with the Linux verifier carefully. The authors explicitly note the benchmark bias: production programs were already written to pass Linux verification. Their more interesting examples are safe programs that developers had to rewrite because of verifier false positives, plus the synthetic path-explosion and loop cases.

The paper reports that Zone/Octagon variants prove all but one of the 192 programs safe, and that the verifier successfully handles additional loop-containing benchmarks. Treat these as evidence for the abstraction choices, not as a timeless benchmark against modern Linux; the comparison is against kernel 4.19-era behavior.

### 8. Related Work — skim, then revisit selectively

Use this section to place eBPF verification among safe languages, hardware isolation, software fault isolation, binary rewriting, static analyzers, and other kernel-extension mechanisms. The interesting contrast is that eBPF aims for native-like execution after load-time proof rather than paying an isolation cost on every instruction.

### 9. Conclusions — read fully

The closing claim is the right one to retain: eBPF is unusually well suited to principled static verification because developers already accept verification as part of the programming model. A sound theoretical foundation can therefore directly improve both security guarantees and programmability.

## Five key ideas

1. **The verifier is part of the kernel security boundary.** A false negative can admit memory corruption or information disclosure, while false positives impose real costs by rejecting valid programs or forcing unnatural rewrites.
2. **Path enumeration is not a scalable abstraction.** Abstract interpretation merges many concrete executions into a conservative state and uses fixed-point computation to reason about loops without enumerating every path.
3. **eBPF's restricted machine model is a verification asset.** Memory regions and control flow are constrained enough that a domain-specific analyzer can reason about pointers much more effectively than a general native-code analyzer.
4. **Precision should be spent where the proof needs it.** Precise bounded-stack tracking and region/offset pointer reasoning matter; unnecessarily precise modeling of every safe region does not.
5. **The choice of numerical abstract domain is an engineering trade-off.** Intervals are too weak for many relational pointer checks, while very general domains are expensive; Zones capture the common `X - Y <= C` relationships at practical cost.

## Practical connection to Linux, eBPF, and Aruba datapath debugging

This paper maps directly to the experience of writing eBPF instrumentation for a Linux datapath. A program can be semantically safe in your head and still fail verification because the verifier cannot prove the invariant you are relying on.

For a packet parser, for example, you may know that a header pointer remains within `data_end` after a check, but the verifier must establish that fact on every feasible control-flow path using the information it tracks about pointer provenance and offsets. A small source rewrite can preserve runtime behavior while making the proof much easier: keep bounds checks close to dereferences, make pointer arithmetic explicit, avoid creating unnecessary branch combinations, and keep loop bounds and state transitions structurally obvious.

When debugging a verifier rejection, read the verifier log as a static-analysis trace rather than as an arbitrary compiler complaint. Ask: which invariant was lost, at which join did precision disappear, which pointer provenance became unknown, or which relation between registers could no longer be represented? That mental model is much more productive than trial-and-error rewrites.

For a production flight-recorder or Aruba datapath observability system, the verifier is also what lets you deploy instrumentation into sensitive kernel paths without trusting every probe as kernel code. The design goal is therefore dual: collect rich evidence at failure time while keeping the proof obligations simple enough that instrumentation remains loadable, bounded, and safe. The paper explains why those two concerns—observability expressiveness and static verifiability—are tightly coupled.

## Connections to the CSPL library

`EBPF-001 — The BSD Packet Filter` establishes the original safe in-kernel filtering VM. `EBPF-002 — The eXpress Data Path` shows modern eBPF/XDP as a high-performance packet-processing substrate. `COMP-003 — A Unified Approach to Global Program Optimization` provides the fixed-point/data-flow-analysis lineage behind this style of static reasoning. `SEC-004 — A Lattice Model of Secure Information Flow` reinforces the broader theme that security properties can be enforced by constraining and proving program behavior rather than only checking permissions at runtime.

## One-sentence takeaway

**eBPF is powerful not merely because the kernel can run user-defined code, but because a verifier can conservatively prove enough about that code before execution to make in-kernel programmability compatible with a strong safety boundary.**
