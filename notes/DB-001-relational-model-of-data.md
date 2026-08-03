# DB-001 — A Relational Model of Data for Large Shared Data Banks

- **Author:** E. F. Codd
- **Year:** 1970
- **Field:** Databases / Data Models
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://research.ibm.com/publications/a-relational-model-of-data-for-large-shared-data-banks
- **DOI:** https://doi.org/10.1145/362384.362685

## Why it matters

This paper introduced the relational model of data. It argued that users and applications should work with a logical model based on relations rather than depend on the physical storage layout, pointer structure, or access paths chosen by the database implementation.

That separation between logical representation and physical organization became the conceptual foundation of relational database systems and SQL-based data management. The paper also introduced ideas around normalization, relational operations, data independence, redundancy, and consistency that shaped database research and commercial systems for decades.

## Prerequisites

- Tables, rows, and columns
- Sets, tuples, and Cartesian products
- Keys and duplicate data
- Basic understanding of file-based data storage
- No prior SQL knowledge is required

## Key ideas

1. **Data independence** — applications should not need to change when the database changes its internal storage or access methods.
2. **Relations as the logical model** — data is represented as sets of tuples rather than navigable trees or pointer-linked networks.
3. **Keys and domains** — relations are structured through attributes, domains, and identifiers rather than physical addresses.
4. **Normalization** — relation structure can reduce redundancy and avoid inconsistent updates.
5. **Relational operations** — data manipulation can be described through operations over relations instead of record-by-record navigation.

## Recommended reading approach

**Read fully, but expect a mathematically dense paper.** The terminology predates modern SQL vocabulary and may initially feel unfamiliar.

### Section-by-section guide

- **Abstract and introduction:** Focus on the demand for data independence and the limitations of tree and network data models.
- **Section 1 — Relational model:** Read carefully. Translate `relation`, `tuple`, `domain`, `primary key`, and `foreign key` into modern table terminology.
- **Normal form discussion:** Understand the problem being solved—repeating groups, redundancy, and ambiguous representations—rather than trying to memorize every formal statement.
- **Section 2 — Operations on relations:** Identify the conceptual ancestors of projection, selection, join, and other relational operations.
- **Redundancy and consistency examples:** Connect the formal model to practical update anomalies and duplicated state.

## Estimated reading time

- First focused read: 60–90 minutes
- With worked examples and notes: 2–3 hours

## Connection to Aruba/Linux networking work

The paper is broadly foundational rather than specifically about networking. Its practical connection is configuration and operational-state modelling.

A network-management system may store controllers, APs, clients, interfaces, VLANs, tunnels, roles, and incidents. The relational model encourages expressing those entities and relationships independently of how the backend lays them out on disk. That separation makes it possible to change indexes, partitioning, storage engines, or query plans without rewriting every consuming tool.

It also highlights a recurring systems-design problem: duplicated state across bridge tables, ARP tables, authentication state, tunnel state, and management databases can become inconsistent unless ownership and relationships are modelled explicitly.

## Questions to answer after reading

1. What distinction does Codd make between logical data representation and physical storage?
2. Why were navigational tree and network models difficult for applications to depend on safely?
3. What is a relation in the paper's terminology?
4. How do keys represent relationships without embedding physical pointers?
5. What kinds of redundancy and update anomalies does normalization attempt to prevent?
6. Which modern SQL concepts can be recognized in the relational operations described?

## Related indexed papers

None currently indexed.
