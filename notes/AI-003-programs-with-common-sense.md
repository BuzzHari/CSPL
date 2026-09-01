# AI-003 — Programs with Common Sense

- **Author:** John McCarthy
- **Year:** 1959
- **Field:** Artificial Intelligence / Knowledge Representation / Automated Reasoning
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://www-formal.stanford.edu/jmc/mcc59.html
- **Date recommended:** 2026-08-31

## Why it matters

McCarthy's Advice Taker proposal established a foundational program for symbolic AI: represent facts, goals, and rules declaratively, then use a general inference mechanism to derive consequences and actions. It helped launch logic-based knowledge representation, commonsense reasoning, planning, and the separation of domain knowledge from reasoning machinery.

## Prerequisites

Basic propositional and first-order logic, inference, and the distinction between declarative and procedural representations.

## Reading guide

1. **Introduction:** Understand the common-sense reasoning problem McCarthy is trying to formalize.
2. **Advice Taker:** Focus on the separation between knowledge supplied to the system and the general inference mechanism.
3. **Formal representation/examples:** Follow what facts and relations must be made explicit for useful deductions.
4. **Actions and changing worlds:** Connect this to later work on planning, situation calculus, and the frame problem.
5. **Discussion:** Note how representation limits what a reasoning system can infer.

## Key ideas

1. Knowledge about the world can be represented explicitly as data.
2. A general inference mechanism can be separated from domain-specific knowledge.
3. Intelligent behavior can be extended by supplying new facts and rules rather than rewriting procedural code.
4. Representation is a core bottleneck: a system cannot reason about distinctions its language cannot express.
5. Commonsense reasoning is difficult because real environments contain incomplete information, exceptions, context, and changing state.

## Practical connection

A programmable diagnostics system can separate troubleshooting knowledge from collection mechanisms: rules such as `roam + traffic failure -> inspect forwarding transition` can declare evidence dependencies while a general engine decides which packet, bridge, tunnel, authentication, or process-state observations to collect. This is a useful architectural model for a programmable flight recorder.

## Reading recommendation

Read fully. Estimated time: 35–50 minutes.

## Related papers

- AI-001 — Attention Is All You Need
- AI-002 — Computing Machinery and Intelligence
- ARCH-002 — On the Criteria To Be Used in Decomposing Systems into Modules
