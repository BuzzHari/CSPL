# AI-003 — Programs with Common Sense

- **Author:** John McCarthy
- **Year:** 1959
- **Field:** Artificial Intelligence / Knowledge Representation / Automated Reasoning
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://www-formal.stanford.edu/jmc/mcc59.html
- **Date recommended:** 2026-08-31

## Why it matters

This paper is a foundational statement of logic-based artificial intelligence. McCarthy proposes the **Advice Taker**: a system whose knowledge is represented as sentences in a formal language and whose behavior can be improved by telling it new facts and goals rather than rewriting its program. The work helped establish knowledge representation, commonsense reasoning, and declarative approaches to intelligent systems as central AI research problems.

## Prerequisites

Basic propositional and first-order predicate logic; the distinction between declarative knowledge and procedural code; basic familiarity with inference and AI agents.

## Reading guide

### 1. Introduction
Read fully. Focus on McCarthy's definition of common sense and the proposed Advice Taker. The important shift is from hard-coding behavior to supplying knowledge declaratively and allowing the machine to derive consequences.

### 2. The Advice Taker and formal language
Read carefully. Track the separation among facts about the world, statements describing goals, and the inference mechanism. This is an early architecture for a knowledge-based agent.

### 3. Example construction and reasoning
Read carefully. Follow how statements are represented and how conclusions lead to actions. Do not get stuck on historical notation; concentrate on the representation/inference boundary.

### 4. Commonsense knowledge and limitations
Read fully. The difficult issue is not merely theorem proving but representing enough ordinary knowledge, context, change, and exceptions for useful reasoning.

### 5. Conclusions and open problems
Read fully. Many problems McCarthy identifies became long-running AI research areas: knowledge representation, planning, reasoning about actions, commonsense knowledge, and making systems extensible through declarative information.

## Key ideas

1. **Knowledge can be represented declaratively.** An intelligent system can manipulate statements about its world instead of encoding every behavior directly in procedural code.
2. **Reasoning turns stored knowledge into action.** Facts and goals become useful when an inference mechanism can derive consequences from them.
3. **A system should be improvable by telling it things.** McCarthy's central usability criterion is that adding knowledge should not require detailed knowledge of the program's implementation.
4. **Commonsense reasoning is a representation problem as much as an inference problem.** A powerful prover is insufficient if the system cannot express the relevant facts, actions, contexts, and assumptions.
5. **Declarative interfaces separate intent from mechanism.** This idea extends well beyond AI into databases, configuration systems, policy engines, planners, and modern agent systems.

## Connection to Linux / Aruba networking software

The useful connection is architectural rather than an argument for putting symbolic AI in a datapath. Operational diagnostics often encode troubleshooting knowledge procedurally: if event A occurs, run command B, inspect state C, then capture D. A more declarative system could represent facts, desired diagnostic goals, dependencies, and available observations separately from the engine that decides what evidence to collect. That resembles the Advice Taker's separation of knowledge from inference and could make diagnostic behavior extensible without continually modifying the core implementation.

## What to retain

The enduring idea is: **make a system more capable by adding knowledge, not by rewriting the mechanism that reasons over that knowledge.** This paper is an early blueprint for knowledge-based systems and remains useful context for modern discussions of agents, tool use, planning, and explicit versus learned knowledge.