# ML-004 — A Theory of the Learnable

- **Author:** Leslie G. Valiant
- **Year:** 1984
- **Field:** Machine Learning / Computational Learning Theory / PAC Learning / Learning Theory
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-12
- **Primary source:** https://doi.org/10.1145/1968.1972
- **Published in:** Communications of the ACM, 27(11), 1134–1142

## Why it matters

Valiant's paper turned the informal question “can a machine learn this concept?” into a computational question with explicit requirements on information, accuracy, confidence, runtime, and sample complexity. It founded computational learning theory and introduced the framework that became known as **Probably Approximately Correct (PAC) learning**.

The key shift is that learning does not require reconstructing a target concept perfectly on every possible input. Instead, a learner should efficiently produce a hypothesis that is approximately correct on the natural input distribution, with high probability. This made it possible to prove positive and negative results about what classes of concepts can be learned efficiently.

The paper also connects learning to complexity theory: some concept classes are efficiently learnable, while cryptographic hardness suggests that other efficiently computable functions may nevertheless be infeasible to learn from feasible amounts of information and computation.

## Prerequisites

- basic probability
- Boolean functions, CNF and DNF
- polynomial-time algorithms and computational complexity
- supervised/concept learning at a conceptual level
- confidence and error probability

## Reading guide

### 1. Introduction
Read fully. This is the conceptual core. Valiant explicitly compares the need for a theory of learning to the role computability theory plays for calculation. Focus on the three simultaneous goals: a nontrivial concept class, a precise learning protocol, and a feasible polynomial-time learning procedure.

Also notice the separation between the **learning protocol** (how information reaches the learner) and the **deduction procedure** (the algorithm that turns that information into a recognizer). That separation remains useful when reasoning about modern learning systems.

### 2. A Learning Protocol for Boolean Functions
Read carefully. Valiant defines Boolean concepts and two information sources: `EXAMPLES`, which supplies naturally distributed positive examples, and `ORACLE`, which answers membership-style questions.

The historically important idea is not the exact oracle interface but the insistence that a learning theorem must say what information the learner is allowed to obtain and under what distributional assumptions.

### 3. Learnability
Read extremely carefully. This section formalizes what it means for a class of programs to be learnable. Track three quantities separately:

- computational cost;
- probability that learning fails;
- approximation error of the learned recognizer on the underlying distribution.

This is the conceptual ancestor of the modern PAC requirement: with high probability, produce a hypothesis with small generalization error using polynomial resources.

### 4. A Combinatorial Bound
Read selectively but understand the purpose. The section supplies the probabilistic bound used later to show that a finite amount of sampled evidence suffices. The exact constants are less important on a first read than the pattern: derive a sample bound from the number of competing hypotheses and the desired confidence/error level.

### 5. Bounded CNF Expressions
Read carefully. This is the cleanest constructive example. Valiant shows that bounded-width CNF can be learned efficiently from examples. Follow how the learner starts with a large candidate set and eliminates clauses contradicted by observations.

### 6. DNF Expressions
Read selectively. The paper explores what remains learnable for DNF and shows how structural restrictions matter. Use this section to see that “learnability” is a property of both the concept class and the information model, not merely of an algorithm name.

### 7. μ-Expressions / More General Expressions
Read selectively on a first pass. This section uses stronger oracles to learn a broader structured class. The main lesson is that stronger teacher–learner interaction can enlarge the class of concepts that is feasibly learnable.

### 8. Remarks
Read fully. Valiant returns to the broader meaning of the framework: learning need only agree on natural inputs with overwhelming probability, and the limits of learnability may determine how complex concepts must be decomposed and taught.

## Key ideas

1. **Learning needs a computational definition.** A useful theory must specify the learner's information source, resource bounds, hypothesis class, error tolerance, and confidence.
2. **Approximate correctness is enough.** Exact identification on every possible input is often unnecessary; high-probability low error under the relevant distribution is a more realistic target.
3. **Sample complexity and computational complexity are separate constraints.** Having enough examples does not imply that an efficient algorithm can exploit them.
4. **Learnability depends on representation and concept class.** Restricting the structure of Boolean formulas can turn an infeasible problem into a provably learnable one.
5. **Cryptography and learning are deeply connected.** If an efficiently computable function can hide its behavior well enough to resist feasible inference, efficient computation does not imply efficient learnability.

## Connection to Linux and Aruba networking work

The paper's main value to systems work is methodological rather than algorithmic. When building automated diagnostics for Linux/network datapaths, it is tempting to say that an agent should “learn” which evidence predicts a failure. Valiant's framework forces the engineering question to become precise:

```text
What observations are available?
What is the target concept?
Under what production distribution?
How much error is acceptable?
How confident must we be?
How much data and computation are available?
```

For example, suppose you want to classify a roaming incident as “bridge-state inconsistency” from packet captures, `/proc` snapshots, eBPF traces, and gateway logs. A system that performs well on reproduced lab failures may still generalize poorly if the real production distribution differs. Valiant's viewpoint makes the distribution and error guarantee part of the problem definition rather than an afterthought.

That is useful for any ML-assisted triage or observability system: the correct question is not simply whether a model fits historical incidents, but whether the evidence-acquisition process and hypothesis class support reliable generalization to future incidents under operational constraints.

## Reading recommendation

**Read fully**, but do not get stuck on every proof during the first pass. Sections 1–3 and 8 are mandatory; Sections 4–7 can be read once for structure and revisited if you want the proof details.

**Estimated reading time:** 45–60 minutes for a conceptual pass; 90 minutes or more if you work through the probabilistic bounds and Boolean-learning proofs carefully.

## Related papers in this library

- ML-003 — Learning representations by back-propagating errors
- ML-001 — ImageNet Classification with Deep Convolutional Neural Networks
- AI-003 — Programs with Common Sense
