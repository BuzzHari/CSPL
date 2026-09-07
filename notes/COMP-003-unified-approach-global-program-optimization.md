# COMP-003 — A Unified Approach to Global Program Optimization

- **Author:** Gary A. Kildall
- **Year:** 1973
- **Field:** Compilers / Data-Flow Analysis / Program Optimization / Static Analysis
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-07
- **Primary source:** https://hdl.handle.net/10945/42162
- **Publication record / DOI:** https://doi.org/10.1145/512927.512945
- **Published in:** Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL '73), pp. 194–206

## Why it matters

Kildall presents a general method for performing global compiler analysis over a program's control-flow graph. Rather than designing a separate whole-program traversal for every optimization, the paper separates the problem into a reusable flow-analysis engine plus an optimization-specific transfer ("optimizing") function and meet operation.

The paper develops the framework from concrete optimizations—constant propagation, common-subexpression elimination, live-expression analysis, and register-related optimization—and then formalizes why iterative propagation over a finite lattice converges to a unique result under the stated conditions. This fixed-point view became foundational to classical compiler data-flow analysis and, more broadly, static program analysis.

The historical qualification matters: global flow analysis existed before this paper. Kildall's contribution was a particularly influential unifying formal framework and correctness/convergence treatment, not the invention of every individual optimization it demonstrates.

## Prerequisites

- control-flow graphs and basic blocks
- compiler intermediate representations
- constant propagation and common-subexpression elimination at a conceptual level
- sets, partial orders, meet operations, and lattices
- fixed points / iterative algorithms
- basic liveness analysis

## Reading guide

### 1. Introduction
**Read fully.** Kildall frames the goal: take optimizations that work on straight-line code and make them work across arbitrary branching structure with one general flow-analysis algorithm.

### 2. Constant Propagation
**Read carefully.** This section motivates the entire framework with a concrete control-flow graph. Follow why facts valid at a node must be valid along every path reaching that node. The naive "enumerate all paths and intersect the results" idea is correct in spirit but may never terminate in a graph containing loops.

### 3. A Global Analysis Algorithm
**Read extremely carefully.** This is the core of the paper. Kildall iteratively propagates information through the graph, combines incoming information with a meet operation, and revisits successors whenever a node's information changes. Pay attention to the optimizing function, the finite lattice, the termination theorem, the correctness theorem, and the fact that the final result is independent of the order in which pending nodes are processed.

A useful modern mental model is:

```text
worklist = entry blocks

while worklist not empty:
    block = pop(worklist)
    in[block] = meet(out[p] for p in predecessors(block))
    new_out = transfer(block, in[block])

    if new_out != out[block]:
        out[block] = new_out
        add successors(block) to worklist
```

The notation differs, but this is recognizably the ancestor of worklist-style data-flow solvers.

### 4. Common Subexpression Elimination
**Read carefully.** The paper changes the data-flow facts from sets of constants to partitions/equivalence classes of expressions, while retaining the same global analysis machinery. This is the key demonstration that the framework is reusable rather than specific to constant propagation.

### 5. Constant Propagation and Common Subexpression Elimination
**Read fully.** Notice how analyses can be enriched and combined. The framework is not "one algorithm per optimization"; the transfer domain can encode more information while the fixed-point machinery remains largely unchanged.

### 6. Expression Optimization
**Read selectively but understand the direction.** Kildall extends the framework toward register optimization and live-expression information. The important point is that both forward and backward information-flow problems can be expressed in this style.

### 7. A Tabular Form for Algorithm A
**Read selectively.** This is useful if you want to manually execute the algorithm. Work through at least one example so that "fixed point" becomes operational rather than abstract.

### 8. Implementation Notes
**Read fully.** This section is surprisingly modern. It discusses intermediate representations, basic-block worklists, compact set representations, convergence, and value numbers for representing equivalence classes.

### 9. Conclusions
**Read fully.** Revisit the central separation: a generic global flow-analysis algorithm plus optimization-specific functions.

### Appendices
**Selective.** Appendix A is useful for tracing an execution of the algorithm. Appendix B is worth reading if you want the correctness proof in detail.

## Key ideas

### 1. Program analysis is a fixed-point computation

Loops make path enumeration impractical. Instead, propagate facts repeatedly until no node's state changes:

```text
initial approximation
        ↓
propagate through CFG
        ↓
merge at control-flow joins
        ↓
facts change? ── yes ──> propagate again
        │
        no
        ↓
fixed point
```

This pattern is now ubiquitous in compilers and static analysis.

### 2. Separate the solver from the analysis

The control-flow/worklist machinery can stay generic. What changes between analyses is primarily:

- the abstract information being tracked,
- the meet operation used when control-flow paths join, and
- the transfer function for each block.

This separation is one reason modern compiler infrastructures can host many analyses on the same IR and CFG.

### 3. Joins must conservatively reconcile paths

At a merge point, the compiler cannot assume which predecessor executed. Facts must therefore be combined according to the analysis's lattice/meet semantics.

For constant propagation, for example, a variable can be treated as a particular constant after a branch only when the incoming information justifies that conclusion for all relevant paths.

### 4. Convergence depends on structure

Kildall does not merely say "iterate until it works." He places the information in a finite ordered structure and imposes properties on the optimizing function, allowing termination and correctness to be proved.

Later data-flow frameworks generalize these conditions, but this paper makes the mathematical structure explicit.

### 5. Forward and backward analyses are variations of the same idea

The paper performs live-expression analysis by reversing the program graph. That exposes a powerful abstraction: some facts flow in execution direction, while others flow backward from uses toward definitions, yet both can use essentially the same solver.

## Connection to Linux, eBPF, and Aruba datapath work

This paper is directly useful for understanding both compiler diagnostics and the Linux eBPF verifier.

Consider a simplified eBPF control-flow graph:

```text
        R1 = packet pointer
               |
        if (R2 < len)
          /         \
   safe path       other path
          \         /
             join
              |
        packet access
```

The verifier must track abstract facts such as:

```text
R1 = PTR_TO_PACKET
R2 range = [0, 127]
packet_end >= R1 + R2 + 8
```

through each basic block. At branches it refines those facts; at joins it merges them conservatively; when a state changes, downstream blocks may need to be revisited. That is not literally Kildall's 1973 optimizer, but it belongs to the same control-flow + abstract-state + transfer + merge + fixed-point family of program analysis.

The same reasoning is useful when inspecting optimized C datapath code. A value visible in source may disappear, become constant-folded, merge with another value, or live only on certain control-flow paths because compiler analyses established facts globally. Understanding data-flow analysis therefore connects directly to your ELF/DWARF questions about why an optimized variable may have no single stable location.

It also suggests a design pattern for a static diagnostic pass over Aruba datapath code: define an abstract state such as "client pointer validated", "lock held", "packet bounds established", or "error path reachable"; specify transfer rules for operations; merge states at control-flow joins; and iterate to a fixed point. The solver can stay generic while the diagnostic property changes.

## What to retain after reading

If you remember only one picture, make it this:

```text
             control-flow graph
                    |
       +------------+-------------+
       |                          |
 generic fixed-point solver   analysis-specific rules
       |                          |
       +------------+-------------+
                    |
          facts at every block
```

That architecture is one of the foundations beneath optimizing compilers and static-analysis engines.

## Reading recommendation

**Read fully.** The paper is roughly thirteen proceedings pages plus appendices/references, and Sections 2–4 are worth working through with pencil and paper. Spend the most time on Section 3; skim some of the detailed partition manipulation if it starts obscuring the central fixed-point framework.
