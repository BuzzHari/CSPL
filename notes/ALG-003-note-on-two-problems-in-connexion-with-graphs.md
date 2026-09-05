# ALG-003 — A note on two problems in connexion with graphs

- **Author:** E. W. Dijkstra
- **Year:** 1959
- **Field:** Algorithms / Graph Algorithms / Shortest Paths
- **Status:** Queued
- **Priority:** Core
- **Inclusion reason:** Daily CS Paper
- **Date recommended:** 2026-09-05
- **Primary source:** https://ir.cwi.nl/pub/9256
- **DOI:** https://doi.org/10.1007/BF01386390
- **Published in:** Numerische Mathematik, 1, 269–271

## Why it matters

This three-page paper presents two graph problems: constructing a minimum-total-length spanning tree and finding a minimum-length path between two specified nodes. The second problem contains the algorithm now universally known as **Dijkstra's shortest-path algorithm**. Its greedy structure—repeatedly fixing the unsettled vertex with minimum tentative distance and relaxing outgoing edges—became one of the canonical graph algorithms and a foundation for routing, navigation, network optimization, and algorithm education.

The minimum-spanning-tree procedure in the first half is essentially the greedy algorithm independently associated with Jarník and Prim; the shortest-path procedure in the second half is the paper's enduring namesake contribution.

## Prerequisites

- graphs, vertices, and edges
- weighted graphs and path length
- trees and spanning trees
- basic asymptotic reasoning
- the idea of a greedy algorithm

## Reading guide

### Opening setup
Read fully. Note that Dijkstra frames both problems in terms of a graph whose branches have nonnegative lengths. The paper predates modern pseudocode notation, so translate the prose into sets and tentative-distance labels as you read.

### Problem 1 — minimum spanning tree
Read fully but briefly. The procedure grows a tree by repeatedly choosing the shortest edge crossing from the selected set to an unselected vertex. Recognize the cut-style greedy invariant rather than memorizing the historical notation.

### Problem 2 — shortest path
Read extremely carefully. Track the three conceptual groups: vertices whose shortest distance is final, vertices with tentative labels, and unreached vertices. At each step choose the tentative vertex with minimum distance, make it permanent, and update neighboring tentative distances. This is the core of Dijkstra's algorithm.

### Storage and work remarks
Read fully. The paper is strikingly implementation-conscious: Dijkstra discusses what information must be retained and how much comparison work the method requires. Compare that with the modern priority-queue formulation, where a binary heap gives O((V+E) log V) time for nonnegative edge weights.

## Key ideas

1. **Greedy finalization can be correct when edge weights are nonnegative.** Once the minimum tentative-distance vertex is chosen, no later route can improve it.
2. **Relaxation is the fundamental local operation.** A known route to `u` plus edge `(u,v)` may improve the best-known route to `v`.
3. **Tentative versus permanent labels encode the algorithm's proof invariant.** The data structures mirror the correctness argument.
4. **Representation determines performance.** The original algorithm can be implemented with simple scans; priority queues substantially improve sparse-graph performance.
5. **Negative edge weights break the greedy guarantee.** That limitation explains why Bellman–Ford and related algorithms exist.

## Connection to Linux / Aruba networking

This paper has a direct routing connection. Link-state protocols such as OSPF build a topology database and run a shortest-path-first computation rooted at the local router. Conceptually, the control plane repeatedly computes a Dijkstra shortest-path tree over advertised link costs and derives next hops from that tree.

When debugging routing behavior on a gateway or network appliance, the paper gives a clean mental model for separating three questions: whether the link-state database is correct, whether the SPF computation is correct, and whether the resulting forwarding entries were programmed correctly into the datapath. A wrong route can therefore originate from bad topology/cost input, SPF logic, or FIB installation rather than from packet forwarding itself.

## Reading recommendation

**Read fully.** It is only three pages, and the historical presentation is worth seeing directly. Budget about **15–25 minutes** for a normal read, or **30–45 minutes** if you manually trace the shortest-path procedure on a small graph.