# DB-003 — Access Path Selection in a Relational Database Management System

- **Authors:** P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie, T. G. Price
- **Year:** 1979
- **Field:** Databases / Query Optimization / Relational Systems
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://research.ibm.com/publications/access-path-selection-in-a-relational-database-management-system
- **DOI:** https://doi.org/10.1145/582095.582099
- **Recommended:** 2026-08-29

## Why it matters

This System R paper established the architecture of practical cost-based relational query optimization. SQL deliberately lets users state *what* result they want without specifying the physical access path or join order. Selinger and colleagues showed how a DBMS can bridge that declarative/physical gap by enumerating candidate plans, estimating their costs from statistics, pruning the search space, and selecting a low-cost execution plan.

The core ideas—table and index access paths, selectivity estimation, cardinality estimation, join-order search, interesting orders, and dynamic-programming-style plan construction—became foundational to commercial relational optimizers and remain visible in PostgreSQL, Db2, SQL Server, Oracle, MySQL, and modern analytical systems.

## Prerequisites

You should be comfortable with:

- the relational model and basic SQL;
- tables/relations, tuples/rows, and predicates;
- B-tree-style indexes and sequential scans;
- joins, especially nested-loop joins;
- basic probability and rough cost estimation;
- the distinction between logical query semantics and physical execution.

Reading `DB-001` (Codd's relational-model paper) first is useful but not mandatory.

## Reading guide

### 1. Introduction

Read fully. Focus on the central abstraction boundary: SQL is nonprocedural, so the optimizer must select access paths and an execution strategy automatically.

The important pipeline is approximately:

```text
SQL
 ↓
parse
 ↓
logical query
 ↓
optimizer
 ↓
physical access plan
 ↓
code/execution
```

### 2. System R storage and access paths

Read carefully enough to understand the cost model. Distinguish a segment/relation scan from an index scan, and note why a clustered index changes the number of data-page accesses.

The lasting concept is not the exact System R storage format; it is that different physical organizations create different costs for the *same* logical query.

### 3. Single-relation access-path selection

Read closely. This is where the optimizer estimates predicate selectivity and compares alternatives such as full scans and index scans.

A simplified model is:

```text
estimated rows
    = input cardinality × estimated selectivity

estimated cost
    = I/O component + CPU component
```

The exact constants are historical. The architecture—statistics → cardinality estimate → cost estimate → plan choice—is still current.

### 4. Join optimization

This is the most important section.

Study how System R searches possible join orders without exhaustively exploring every permutation. It incrementally constructs increasingly large joins, retaining useful low-cost partial plans.

Pay special attention to **interesting orders**: a plan that is not locally cheapest may be worth preserving because its output ordering can make a later join, `ORDER BY`, or grouping step cheaper. This is a key example of why optimizer decisions cannot always be greedy.

### 5. Nested queries and remaining cases

Read selectively on a first pass. The details reflect the SQL and execution machinery of the era, while the broader lesson is that query structure creates additional optimization opportunities and constraints.

### 6. Examples / cost calculations

Work through at least one example. The paper becomes much clearer once you manually compare two access paths or join orders using the estimated costs.

## Key ideas

### 1. Declarative languages require physical optimization

SQL separates semantics from execution strategy. That abstraction is practical only because the DBMS can automatically choose physical plans.

### 2. Query optimization is cost-based search

The optimizer considers alternative equivalent execution plans and assigns estimated costs to them rather than relying solely on fixed rules.

### 3. Cardinality estimation drives plan quality

To estimate plan cost, the optimizer must estimate how many tuples survive predicates and joins. Errors in those estimates propagate upward and can lead to dramatically bad plans.

### 4. Join order matters enormously

Relational joins are logically associative/commutative in many cases, but intermediate result sizes can differ by orders of magnitude depending on execution order. Searching join orders is therefore a central optimizer problem.

### 5. Locally cheapest is not always globally cheapest

System R's notion of interesting output orders preserves some plans that cost more *now* because they may avoid work later. This is a general dynamic-programming systems lesson: retain state that captures future value, not just immediate cost.

## Connection to Linux / Aruba networking work

The paper's strongest connection is architectural rather than database-specific: it demonstrates how to translate a high-level request into an efficient low-level execution strategy using statistics and a cost model.

Imagine a programmable diagnostic system where an engineer asks:

```text
observe client 8c:xx:xx
when roam occurs
capture auth state + bridge state + selected packets
for 30 seconds
```

There may be several ways to implement that request:

```text
uprobes
tracepoints
kprobes
USDT
BPF maps
packet capture filters
/proc reads
userspace polling
```

A naive implementation could enable everything. A System-R-like diagnostic planner could instead estimate:

- event frequency;
- expected data volume;
- probe overhead;
- filter selectivity;
- required ordering/correlation;
- memory and export cost;

and choose an execution plan that obtains the required evidence at minimum expected overhead.

That is essentially query optimization applied to observability: declarative diagnostic intent above, cost-aware probe and data-path selection below.

## What to retain

If you remember only one model, remember:

```text
logical request
      ↓
enumerate equivalent physical strategies
      ↓
estimate cardinalities/selectivities
      ↓
estimate costs
      ↓
retain strategically useful partial plans
      ↓
choose physical plan
```

This pattern extends far beyond databases—to compilers, packet-processing pipelines, distributed query engines, observability systems, and automated diagnostic tooling.

## Suggested exercise

Take this query:

```sql
SELECT *
FROM clients c
JOIN sessions s ON c.id = s.client_id
WHERE c.site = 'BLR'
  AND s.state = 'FAILED';
```

Assume indexes exist on `clients.site`, `sessions.client_id`, and `sessions.state`. Sketch at least three physical plans, estimate intermediate cardinalities, and decide which one should win under different selectivity assumptions.

The purpose is to feel why optimizer quality depends less on SQL syntax than on statistics and intermediate-result estimation.
