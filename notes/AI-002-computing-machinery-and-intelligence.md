# AI-002 — Computing Machinery and Intelligence

- **Author:** Alan M. Turing
- **Year:** 1950
- **Field:** Artificial Intelligence / Philosophy of AI / Machine Intelligence
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://turingarchive.kings.cam.ac.uk/computing-machinery-and-intelligence
- **DOI:** https://doi.org/10.1093/mind/LIX.236.433

## Why it matters

Turing reframed the vague question “Can machines think?” into an operational test based on observable conversational behavior: the imitation game, later known as the Turing Test. More importantly, the paper systematically considers objections to machine intelligence, sketches learning machines, and treats intelligence as something that might emerge from computation and training rather than requiring a special non-mechanical essence.

The paper is foundational to artificial intelligence not because the Turing Test is a complete definition of intelligence—it is not—but because it established a durable way to reason about machine intelligence through behavior, computation, learning, and falsifiable objections.

## Prerequisites

- Basic idea of a digital computer
- Algorithms and computation at a conceptual level
- No machine-learning mathematics required
- Some familiarity with the distinction between behavior and internal mechanism is useful

## Key ideas

1. **Replace an ill-defined metaphysical question with an operational one.** Instead of defining “thinking” directly, Turing proposes the imitation game as a concrete behavioral criterion.
2. **Digital computers are general-purpose symbol manipulators.** The paper builds on the universality of digital computation and asks what behaviors sufficiently programmed machines might exhibit.
3. **Many objections to machine intelligence are empirical, not decisive proofs.** Turing examines theological, mathematical, consciousness, disability, continuity-of-nervous-system, and other objections rather than treating them as self-evident barriers.
4. **Learning may be more practical than hand-programming intelligence.** Turing proposes constructing a child machine and training it, anticipating important ideas in machine learning and reinforcement-based adaptation.
5. **Prediction about machine intelligence should be tested against future capability.** The paper is strikingly forward-looking about computers eventually exhibiting behavior that people would describe as intelligent.

## Recommended reading approach

**Read fully.** The paper is accessible, historically central, and much richer than the popular summary “Turing invented the Turing Test.”

### Section-by-section guide

- **1. The Imitation Game:** Read closely. Understand why Turing changes the original question and what the test does—and does not—claim.
- **2. Critique of the New Problem:** Note the distinction between defining intelligence internally and judging externally observable performance.
- **3. The Machines Concerned in the Game:** Understand why Turing restricts attention to digital computers rather than arbitrary machines.
- **4–5. Digital Computers and Universality:** Focus on the conceptual idea that a general-purpose digital computer can simulate many specialized machines when appropriately programmed.
- **6. Contrary Views on the Main Question:** This is the longest and most important section. Work through the objections individually; many still appear in modern AI debates in updated form.
- **7. Learning Machines:** Read carefully. Turing’s child-machine proposal anticipates the idea that complex intelligent behavior may be learned rather than explicitly programmed rule by rule.

## Estimated reading time

- Focused first read: 60–75 minutes
- With notes on each objection: 90–120 minutes

## Connection to Linux / Aruba engineering work

The paper’s direct value is broader than networking, so a forced datapath analogy would be misleading. The useful engineering connection is methodological: when a system property is vague—“intelligent,” “healthy,” “correct,” or “diagnosable”—Turing’s move is to define an observable test that makes the claim operational.

For a diagnostic system, for example, “good observability” is vague. A stronger criterion is behavioral: given a real failure, can the system identify the causal component and relevant state without reproducing the issue? That kind of operational definition makes architecture measurable rather than rhetorical.

## Questions to answer after reading

1. What does the imitation game actually test, and what does it leave unresolved?
2. Which of Turing’s objections still appear in current AI debates under different names?
3. Why does universality matter to his argument?
4. Why does Turing propose a child machine rather than directly programming an adult mind?
5. Is behavioral indistinguishability a sufficient criterion for intelligence, or merely a useful engineering test?

## Related indexed papers

- AI-001 — Attention Is All You Need
- ML-001 — ImageNet Classification with Deep Convolutional Neural Networks
- ML-002 — Deep Residual Learning for Image Recognition
