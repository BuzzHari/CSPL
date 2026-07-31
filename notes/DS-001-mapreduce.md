# DS-001 — MapReduce: Simplified Data Processing on Large Clusters

- **Authors:** Jeffrey Dean, Sanjay Ghemawat
- **Year:** 2004
- **Field:** Distributed Systems / Large-Scale Data Processing
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://research.google.com/archive/mapreduce-osdi04.pdf

## Why it matters

MapReduce showed how a deliberately constrained programming model could let a runtime automate partitioning, scheduling, data movement, retries, and fault tolerance across large clusters.

## Key ideas

1. Map and reduce as a restricted distributed programming interface
2. Shuffle as the central data-movement boundary
3. Locality-aware scheduling
4. Recomputation as fault recovery
5. Speculative execution for stragglers

## Work connection

Useful for designing fleet-wide processing of Aruba logs, counters, crash signatures, and diagnostic bundles.
