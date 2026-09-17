# ALG-004 — The Complexity of Theorem-Proving Procedures

- **Author:** Stephen A. Cook
- **Year:** 1971
- **Field:** Algorithms / Computational Complexity / NP-Completeness / Polynomial-Time Reductions
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-17
- **Primary source:** https://www.cs.toronto.edu/~sacook/homepage/1971.pdf
- **DOI:** https://doi.org/10.1145/800157.805047
- **Published in:** Proceedings of the Third Annual ACM Symposium on Theory of Computing (STOC), pp. 151–158

## Why it matters

Cook's 1971 paper founded the theory of NP-completeness. In the terminology of the paper, it shows that every recognition problem accepted by a polynomial-time nondeterministic Turing machine can be polynomially reduced to a propositional tautology problem. In modern language, the construction is the core of what is now called the Cook–Levin theorem: Boolean satisfiability is NP-complete.

The conceptual breakthrough is not merely that one logic problem is difficult. Cook shows how an arbitrary polynomial-time nondeterministic computation can be encoded as a polynomial-size Boolean formula. That creates a general method for comparing apparently unrelated computational problems: if problem A can be transformed efficiently into problem B, then an efficient algorithm for B would also solve A efficiently.

This changed algorithm design permanently. It gave computer science a rigorous way to explain why many natural problems resist known polynomial-time algorithms, shifted attention from solving each hard problem independently to proving reductions between them, and established the P-versus-NP question as a central organizing problem in theoretical computer science.

## Prerequisites

- deterministic and nondeterministic computation at a conceptual level
- polynomial-time algorithms
- Boolean formulas, CNF/DNF, satisfiability, and tautologies
- basic graph terminology
- the idea of transforming one problem instance into another

You do not need a full complexity-theory course before reading it. The historical notation is more difficult than the underlying central idea.

## Reading guide

### Summary and opening definitions

Read fully. Cook immediately states the central result: recognition problems solved by polynomial-time nondeterministic Turing machines can be reduced to deciding propositional tautologies.

Pay attention to the paper's historical terminology. Cook defines **P-reducibility** using a polynomial-time query machine with an oracle. This is slightly different from the many-one reductions most textbooks use when defining NP-completeness today. Do not let that notation obscure the main idea: efficient reductions let the difficulty of one problem transfer to another.

### Section 1 — Tautologies and Polynomial Reducibility

This is the most important section. Read carefully.

Cook defines polynomial reducibility and then introduces several example languages, including subgraph isomorphism, graph isomorphism, primes, DNF tautologies, and a restricted DNF tautology problem.

Theorem 1 is the core result. Given a polynomial-time nondeterministic Turing machine `M` and input `w`, Cook constructs a propositional formula whose satisfying assignments encode an accepting computation of `M` on `w`.

Focus on the structure of the encoding rather than every symbol. The Boolean variables describe facts such as:

- which tape symbol occupies a particular tape cell at time `t`;
- which machine state is active at time `t`;
- which tape cell is being scanned;
- whether successive configurations obey the transition function;
- whether the initial configuration is correct;
- whether an accepting state is eventually reached.

The key invariant is:

```text
M accepts w
    iff
there exists a valid accepting computation history
    iff
an efficiently constructed Boolean formula has the corresponding truth assignment
```

The important complexity argument is that if `M` runs in polynomial time, then its computation tableau has polynomial size, so the Boolean formula describing it can also be constructed in polynomial time.

This encoding of a computation into local logical constraints is one of the most reusable ideas in all of theoretical computer science.

### Theorem 2 and reductions among concrete problems

Read for the technique, not every construction detail.

Cook shows polynomial equivalences among several problems and gives a reduction involving restricted tautologies and subgraph isomorphism. The lasting lesson is that reductions are a reusable language for proving that two apparently different problems share computational difficulty.

When reading the graph construction, ask:

1. what property of the source instance must be preserved?
2. what structure in the target instance represents a candidate solution?
3. why does every valid source solution correspond to a valid target solution, and vice versa?
4. why is the transformation polynomial in input size?

Those four questions remain the standard checklist for NP-hardness reductions.

### Section 2 — Discussion

Read fully.

This is historically valuable because Cook recognizes the consequence of Theorem 1: finding a polynomial-time algorithm for the tautology problem would imply polynomial-time algorithms for a broad collection of apparently difficult combinatorial problems.

The language predates the now-standard `P`, `NP`, and `NP-complete` vocabulary, but the conceptual structure is already present.

Cook also discusses the Davis–Putnam procedure. This is worth noticing because SAT is unusual: it is theoretically complete for NP while also being extraordinarily useful in practice through modern SAT solvers. Worst-case hardness does not mean that useful real instances cannot often be solved efficiently.

### Section 3 — The Predicate Calculus

Read selectively on a first pass.

The paper turns from propositional complexity to measuring the efficiency of proof procedures for predicate calculus. The historical proof-complexity material is less essential for understanding NP-completeness.

Understand the goal: Cook wants complexity measures that characterize theorem-proving procedures rather than merely asking whether they eventually terminate.

If proof complexity, SAT/SMT, automated theorem proving, or formal verification interests you, return to this section later and read it carefully.

### Section 4 — More Discussion

Read fully, but do not spend time reproducing every bound.

Cook discusses gaps between upper and lower bounds for theorem-proving procedures and explicitly points toward major unresolved complexity questions. The important theme is methodological: empirical solver performance is useful, but theoretical complexity measures are needed to expose fundamental limitations and compare classes of procedures.

## Key ideas

1. **Polynomial-time reductions turn difficulty into a transferable property.** If every problem in a broad class efficiently reduces to one problem, a fast algorithm for that one problem would solve the entire class efficiently.

2. **Computation can be encoded as logic.** A bounded execution of a machine can be represented by Boolean variables and local constraints describing each time step and the relationship between adjacent configurations.

3. **Polynomial size is the critical resource bound.** The reduction is useful because a polynomial-time computation produces only a polynomial-size tableau and therefore a polynomial-size Boolean encoding.

4. **NP-completeness changes the algorithm designer's question.** Instead of repeatedly searching for polynomial algorithms for every difficult problem in isolation, first ask whether the problem can encode a known hard problem or reduce to a known complete problem.

5. **Worst-case hardness and practical solvability are different claims.** SAT can be NP-complete while modern SAT solvers still solve large structured instances effectively; complexity theory constrains general worst-case behavior rather than declaring every instance difficult.

## Practical connection to Linux and Aruba networking work

This paper is not primarily a systems paper, so the connection should not be forced. The useful connection is to **constraint-based reasoning about network state and configuration**.

Suppose a debugging or verification tool asks whether there exists a combination of configuration and runtime state satisfying constraints such as:

```text
client authenticated
AND policy allows traffic
AND tunnel terminates on gateway G
AND route selects interface I
AND ACL does not deny packet
AND forwarding state is internally consistent
```

A large family of verification problems can be encoded as Boolean or SMT constraints. The resulting solver may search for either:

- a satisfying assignment representing a valid configuration/state; or
- a counterexample representing a failure condition.

Cook's core idea explains why this works as a general methodology: many complicated combinatorial questions can be compiled into a common constraint language. Modern SAT/SMT-based verification systems build on exactly this style of reduction, even though their encodings and solvers are far more sophisticated.

It also gives a useful caution for automated debugging. If an RCA system attempts to search all combinations of events, configurations, state transitions, and failure hypotheses, the search space can become combinatorial very quickly. Better representations, domain constraints, decomposition, incremental solving, and good heuristics may matter more than raw compute.

For everyday packet-path debugging, no NP-completeness machinery is required. The value is broader: this paper teaches how to recognize when a seemingly domain-specific search problem may actually be an instance of a much more general computational difficulty.

## Reading recommendation

**Read Sections 1 and 2 fully. Read Sections 3 and 4 selectively on the first pass.** The paper is only eight pages, but the original notation is dense.

**Estimated reading time:** 40–55 minutes for a conceptual pass; 75–100 minutes if you work through the computation-tableau encoding and graph reduction in detail.

## Related papers in this library

- ALG-003 — A note on two problems in connexion with graphs
- COMP-003 — A Unified Approach to Global Program Optimization
- AI-003 — Programs with Common Sense
- ML-004 — A Theory of the Learnable
