# ALG-002 — Space/Time Trade-offs in Hash Coding with Allowable Errors

- **Author:** Burton H. Bloom
- **Year:** 1970
- **Field:** Algorithms / Probabilistic Data Structures / Hashing
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://dl.acm.org/doi/10.1145/362686.362692
- **DOI:** https://doi.org/10.1145/362686.362692

## Why it matters

This paper introduced the data structure now known as the **Bloom filter**: a compact probabilistic representation of set membership that deliberately trades a controllable false-positive probability for dramatically lower memory use. It established an enduring systems technique: when an exact answer is expensive but false positives can be tolerated and verified later, a small approximate structure can eliminate most unnecessary work.

Bloom filters became standard building blocks in databases, storage systems, distributed systems, networking, caches, key-value stores, compilers, security tooling, and large-scale data-processing systems.

## Prerequisites

- Hash functions and hash tables
- Sets and membership queries
- Bits/bit arrays
- Basic probability
- The distinction between false positives and false negatives
- Basic space/time complexity

## Core construction

For a set of items, allocate a bit array of `m` bits and choose `k` hash functions.

To insert item `x`:

1. Compute `k` hash positions for `x`.
2. Set those `k` bits to 1.

To query item `x`:

1. Compute the same `k` positions.
2. If **any** corresponding bit is 0, `x` is definitely absent.
3. If **all** corresponding bits are 1, `x` is *possibly* present.

Thus a standard Bloom filter has:

- **no false negatives** for inserted items, assuming the structure is used as designed;
- **possible false positives** because unrelated items can set the same bits.

For the usual independent-hash approximation, after inserting `n` items into `m` bits with `k` hashes, the false-positive probability is approximately:

`p ≈ (1 - e^(-kn/m))^k`

For fixed `m` and `n`, the conventional approximate optimum is:

`k ≈ (m/n) ln 2`

The important lesson is not memorizing these formulas, but understanding the design triangle among **memory, query work, and tolerated error probability**.

## Key ideas

1. **Approximate membership can be much cheaper than exact membership.** If false positives are acceptable but false negatives are not, exact storage of every key may be unnecessary.
2. **Multiple hash probes encode membership probabilistically.** A tiny bit array can summarize a much larger set without storing the original keys.
3. **False positives are an explicit engineering budget.** Accuracy is not simply lost; it is traded quantitatively for memory and computation.
4. **Negative answers are especially valuable.** A Bloom filter can cheaply prove that an item is absent, avoiding an expensive lookup; positive answers can be verified by the authoritative data source.
5. **The useful data structure often sits in front of the exact mechanism.** A probabilistic prefilter accelerates the common case without becoming the source of truth.

## Recommended reading approach

**Read fully.** The paper is short, foundational, and the original terminology differs enough from modern textbook presentations that reading Bloom's own argument is worthwhile.

### Section-by-section guide

- **Problem statement and conventional hash coding:** Understand the workload Bloom targets: many membership tests where most queried messages are expected not to belong to the stored set.
- **First hash-coding method:** Follow how compact encoded information can reject most nonmembers without retaining a conventional full representation.
- **Second method / multiple hash transformations:** This is the conceptual ancestor of the modern Bloom filter. Focus on why several independently derived bit positions reduce the false-positive rate.
- **Space, reject-time, and error trade-offs:** Read carefully. This is the paper's real contribution: the data structure is valuable because its error rate is a tunable resource trade-off.
- **Comparisons and conclusions:** Separate the timeless idea from implementation assumptions specific to 1970-era hardware.

## Estimated reading time

- Focused first read: 30–45 minutes
- With probability derivation and worked examples: 60–90 minutes

## Connection to Linux / Aruba networking work

Bloom filters are useful when a fast path needs a very cheap test that can safely say **"definitely not present"** while tolerating occasional **"maybe present"** results that are verified through a slower authoritative lookup.

In networking software, that pattern can apply to large membership-style state such as known-flow keys, client identifiers, blocked/interesting addresses, telemetry deduplication, or deciding whether an expensive table lookup is worth attempting. A conceptual datapath design is:

`packet/client key -> Bloom filter -> definitely absent: skip expensive lookup`

`packet/client key -> Bloom filter -> maybe present: consult exact table`

The crucial correctness rule is that the probabilistic structure should normally remain a **prefilter or hint**, not the authoritative policy decision. A false positive should cost extra work, not incorrectly drop or authorize traffic.

The same idea can reduce observability overhead: a compact filter can cheaply determine whether an event might match a set of watched clients/flows before performing more expensive capture, symbolization, aggregation, or user-space export.

## Questions to answer after reading

1. Why can a Bloom filter safely return "definitely absent" but only "possibly present"?
2. What happens to the false-positive rate as more items are inserted into a fixed-size filter?
3. Why is increasing the number of hash functions not always beneficial?
4. Which applications can tolerate false positives but absolutely cannot tolerate false negatives?
5. When should the exact data structure remain behind the Bloom filter rather than be replaced by it?

## Related indexed papers

- ALG-001 — Quicksort
- DB-001 — A Relational Model of Data for Large Shared Data Banks
- DS-002 — The Google File System
