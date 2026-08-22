# COMP-002 — Register Allocation via Coloring

- **Authors:** Gregory J. Chaitin, Marc A. Auslander, Ashok K. Chandra, John Cocke, Martin E. Hopkins, Peter W. Markstein
- **Year:** 1981
- **Field:** Compilers / Register Allocation / Graph Algorithms
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://research.ibm.com/publications/register-allocation-via-coloring
- **DOI:** https://doi.org/10.1016/0096-0551(81)90048-5

## Why it matters

This paper turned global register allocation into a graph-coloring problem and demonstrated the approach in an optimizing PL/I compiler. A node represents a value that would ideally reside in a machine register; an edge connects two values whose live ranges overlap, meaning they cannot occupy the same register at the same time. Assigning a finite set of physical registers then becomes assigning colors to the interference graph.

This formulation became one of the canonical compiler back-end techniques. It made register allocation a clean global optimization problem and directly influenced decades of production compiler design, later work on spilling and coalescing, and the way compiler engineers reason about register pressure.

## Prerequisites

- Basic compiler pipeline and intermediate representations
- Machine registers and assembly-level execution
- Basic blocks and control-flow graphs
- Variable liveness / live ranges
- Elementary graph theory and graph coloring

## Key ideas

1. **Interference graph** — each node is a computed value; an edge means two values are simultaneously live and therefore cannot share a register.
2. **Registers as colors** — assigning one of `k` physical registers is modeled as coloring the graph with `k` colors.
3. **Global allocation** — allocation decisions are made across control-flow boundaries rather than independently inside each basic block.
4. **Spilling is the escape hatch** — if the graph cannot be colored with the available registers, some values must live in memory instead; the 1981 paper establishes the coloring formulation, while Chaitin's 1982 follow-up develops spilling further.
5. **Compiler quality is machine performance** — good allocation reduces loads/stores, shortens critical instruction sequences, and can approach hand-written assembly quality.

## Recommended reading approach

**Read fully.** It is compact and the graph model is much easier to retain if you work through one example by hand.

### Section-by-section guide

- **Introduction / motivation:** Understand why local register allocation leaves performance on the table and why a global formulation is valuable.
- **Register-conflict / interference graph construction:** Read carefully. Connect liveness to edges: values that are live simultaneously must receive different registers.
- **Coloring formulation:** This is the conceptual core. Translate each compiler concept into its graph counterpart: value → node, interference → edge, register → color.
- **Allocation procedure:** Follow how the compiler tries to simplify and color the graph. Focus on the invariant rather than implementation details of the historical PL/I compiler.
- **Code generation / consequences of allocation:** Watch how successful coloring removes unnecessary memory traffic and lets values remain in registers across larger regions of code.
- **Experimental results:** Read for the engineering claim: the technique was implemented and could produce allocation approaching hand-coded assembly, not merely described as a theoretical analogy.
- **Limitations and follow-on questions:** Ask what happens when the graph is not colorable with the machine's available registers; this leads naturally to spilling, coalescing, live-range splitting, and later allocator designs.

## Estimated reading time

- Focused first read: 45–60 minutes
- With a hand-built interference graph: 75–100 minutes

## Connection to Linux, eBPF, and Aruba datapath work

This paper is directly relevant whenever C/C++ or eBPF code is compiled into a constrained register set. Source-level variables do not map one-to-one to physical registers: the compiler must decide which simultaneously live values deserve registers and which values must be spilled or recomputed.

For eBPF, register pressure matters twice. LLVM first performs ordinary compiler allocation and transformations, and the resulting BPF program itself targets a small architectural register set before the kernel JIT maps BPF registers to native machine registers. Code with many values simultaneously live across branches can therefore generate more moves, stack accesses, or verifier-visible complexity than source code suggests.

For performance-sensitive Aruba datapath code, the practical lesson is that two algorithms with similar source-level complexity can compile very differently. Long live ranges, many simultaneous temporaries, helper calls, and branch-heavy code can increase register pressure and memory traffic. When profiling a hot path, inspecting generated assembly and spill/reload behavior can explain costs that are invisible at the C source level.

## Exercise

Take the following pseudo-code:

```text
a = load()
b = load()
c = a + b
d = c * b
return d
```

Mark the live range of each value, then draw an edge between every pair that is simultaneously live. Try coloring the graph with two registers, then three. The exercise makes the paper's central reduction concrete.

## Related indexed papers

- COMP-001 — Efficiently Computing Static Single Assignment Form and the Control Dependence Graph
- CA-001 — RISC I: A Reduced Instruction Set VLSI Computer
- EBPF-001 — The BSD Packet Filter: A New Architecture for User-level Packet Capture
