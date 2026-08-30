# ML-003 — Learning representations by back-propagating errors

- **Authors:** David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams
- **Year:** 1986
- **Field:** Machine Learning / Neural Networks / Representation Learning
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://www.nature.com/articles/323533a0
- **DOI:** 10.1038/323533a0
- **Date recommended:** 2026-08-30

## Why it matters

This short Nature paper gave the modern neural-network community its canonical demonstration of error back-propagation as a practical learning procedure for multilayer networks. Instead of hand-designing intermediate features, the algorithm repeatedly propagates output error backward through differentiable layers and adjusts weights so hidden units learn useful internal representations. The idea became the basic optimization mechanism behind the later deep-learning revolution.

The paper did not invent every mathematical ingredient of reverse-mode differentiation or neural-network training, and related backpropagation ideas predate it. Its historical importance is that Rumelhart, Hinton, and Williams presented a clear, compelling learning procedure and demonstrated that hidden representations could be learned automatically.

## Prerequisites

- Basic feed-forward neural networks
- Weighted sums and nonlinear activation functions
- Derivatives and the chain rule
- Gradient descent
- Mean-squared/error objectives

## Reading guide

### Opening description

Read closely. The paper states the essential learning loop: perform a forward computation, compare the output with the desired output, propagate error information backward, and adjust connection weights to reduce the discrepancy.

### Derivation of the learning rule

Read carefully. Track how the derivative of the global error with respect to each weight factors through downstream units. This is the chain rule expressed as a reusable computational procedure. Focus on why hidden units can receive a useful learning signal even though no target value is supplied directly for them.

### Hidden representations

Read fully. This is the conceptual payoff. Backpropagation does more than fit an input-output mapping: hidden units organize themselves into features useful for solving the task. This is an early, concise statement of representation learning.

### Experiments and examples

Read fully but do not over-focus on the tiny networks by modern standards. Ask what each experiment establishes about distributed representations, generalization, and the ability to discover latent structure.

### Closing discussion

Read fully. Separate the durable algorithmic insight from historically specific claims about biological plausibility and the scale of the experiments.

## Key ideas

1. **Credit assignment through the chain rule.** A unit deep inside a network can receive a learning signal by measuring how changing it would affect downstream error.
2. **Forward computation and backward differentiation form a reusable training procedure.** The same graph used to compute outputs provides the dependency structure needed to compute gradients.
3. **Hidden features can be learned rather than engineered.** Intermediate units develop representations that capture regularities useful to the task.
4. **Local parameter updates can optimize a global objective.** Each weight update uses information derived from the final error while requiring only quantities associated with its local connections and propagated derivatives.
5. **Differentiable composition scales conceptually.** Modern automatic differentiation and deep-learning frameworks generalize the same principle to far larger computational graphs.

## Practical connection

The most useful connection to Linux/networking engineering is not that backpropagation belongs in a datapath; it usually does not. The transferable idea is **automatic credit assignment through a dependency graph**. In a complicated packet-processing or control-plane failure, the observed symptom may occur many transformations after the state transition that caused it. Backpropagation formalizes, in a differentiable setting, how downstream error can be attributed backward through a chain of dependencies. That mental model is useful when designing causal telemetry, provenance, and debugging systems: preserve enough dependency information that a late failure can be traced back toward the operations and state that contributed to it.

## Reading recommendation

Read the entire paper. It is only four Nature pages and is historically important enough that selective reading saves little time. Budget roughly 30–45 minutes for a first pass and 60–90 minutes if deriving the equations by hand.
