# Computer Science Paper Library

A curated index of landmark and must-read computer science papers.

The library prioritizes papers that materially changed research, industry practice, or the direction of computer science across artificial intelligence, machine learning, operating systems, networking, eBPF, algorithms, databases, distributed systems, compilers, security, computer architecture, observability, debugging, and software architecture.

## Master Paper Index

| ID | Paper | Year | Field | Status | Priority |
|---|---|---:|---|---|---|
| [NET-001](notes/NET-001-click-modular-router.md) | The Click Modular Router | 2000 | Networking / Operating Systems | Reading | Core |
| [DS-001](notes/DS-001-mapreduce.md) | MapReduce: Simplified Data Processing on Large Clusters | 2004 | Distributed Systems | Queued | Core |
| [DS-002](notes/DS-002-google-file-system.md) | The Google File System | 2003 | Distributed Storage | Queued | Core |

The canonical machine-readable index is [`papers.yaml`](papers.yaml).

## Inclusion policy

A paper is added when either:

1. it is selected as a **Daily CS Paper**; or
2. it is explicitly requested for inclusion.

Papers that are merely discovered, compared, cited, or mentioned during general research are not automatically added.

Before adding a paper, the index is checked for duplicates. Existing IDs are permanent.

## Statuses

- `Queued`
- `Reading`
- `Completed`
- `Skimmed`
- `Revisit`
- `Reference`

## Priorities

- `Core`
- `Important`
- `Optional`

## PDF policy

The repository stores metadata, links, and original reading notes by default. A paper PDF should be committed only when its licence or rights statement clearly permits redistribution. Otherwise, the index links to an official or primary source.
