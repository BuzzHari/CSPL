# Computer Science Paper Library

A curated index of landmark and must-read computer science papers.

The library prioritizes papers that materially changed research, industry practice, or the direction of computer science across artificial intelligence, machine learning, operating systems, networking, eBPF, algorithms, databases, distributed systems, compilers, security, computer architecture, observability, debugging, and software architecture.

## Master Paper Index

| ID | Paper | Year | Field | Status | Priority |
|---|---|---:|---|---|---|
| [NET-001](notes/NET-001-click-modular-router.md) | The Click Modular Router | 2000 | Networking / Operating Systems | Reading | Core |
| [DS-001](notes/DS-001-mapreduce.md) | MapReduce: Simplified Data Processing on Large Clusters | 2004 | Distributed Systems | Queued | Core |
| [DS-002](notes/DS-002-google-file-system.md) | The Google File System | 2003 | Distributed Storage | Queued | Core |
| [AI-001](notes/AI-001-attention-is-all-you-need.md) | Attention Is All You Need | 2017 | Artificial Intelligence / Machine Learning | Queued | Core |
| [OS-001](notes/OS-001-unix-time-sharing-system.md) | The UNIX Time-Sharing System | 1974 | Operating Systems / Systems Software | Queued | Core |
| [DB-001](notes/DB-001-relational-model-of-data.md) | A Relational Model of Data for Large Shared Data Banks | 1970 | Databases / Data Models | Queued | Core |
| [ARCH-001](notes/ARCH-001-end-to-end-arguments-in-system-design.md) | End-to-End Arguments in System Design | 1984 | Systems Architecture / Networking | Queued | Core |
| [COMP-001](notes/COMP-001-efficiently-computing-static-single-assignment-form.md) | Efficiently Computing Static Single Assignment Form and the Control Dependence Graph | 1991 | Compilers / Program Analysis | Queued | Core |
| [SEC-001](notes/SEC-001-protection-of-information-in-computer-systems.md) | The Protection of Information in Computer Systems | 1975 | Computer Security / Operating Systems | Queued | Core |
| [CA-001](notes/CA-001-risc-i-reduced-instruction-set-vlsi-computer.md) | RISC I: A Reduced Instruction Set VLSI Computer | 1981 | Computer Architecture / ISA | Queued | Core |
| [EBPF-001](notes/EBPF-001-bsd-packet-filter.md) | The BSD Packet Filter: A New Architecture for User-level Packet Capture | 1993 | eBPF / Packet Filtering / Networking | Queued | Core |
| [ALG-001](notes/ALG-001-quicksort.md) | Quicksort | 1962 | Algorithms / Sorting | Queued | Core |
| [DBG-001](notes/DBG-001-eraser-dynamic-data-race-detector.md) | Eraser: A Dynamic Data Race Detector for Multithreaded Programs | 1997 | Debugging / Concurrency | Queued | Core |
| [ARCH-002](notes/ARCH-002-criteria-decomposing-systems-into-modules.md) | On the Criteria To Be Used in Decomposing Systems into Modules | 1972 | Software Architecture / Modularity | Queued | Core |
| [ML-001](notes/ML-001-imagenet-classification-deep-convolutional-neural-networks.md) | ImageNet Classification with Deep Convolutional Neural Networks | 2012 | Machine Learning / Deep Learning / Computer Vision | Queued | Core |
| [NET-002](notes/NET-002-protocol-for-packet-network-intercommunication.md) | A Protocol for Packet Network Intercommunication | 1974 | Computer Networking / Internet Architecture | Queued | Core |
| [DS-003](notes/DS-003-time-clocks-ordering-events-distributed-system.md) | Time, Clocks, and the Ordering of Events in a Distributed System | 1978 | Distributed Systems / Logical Clocks | Queued | Core |
| [OS-002](notes/OS-002-structure-of-the-the-multiprogramming-system.md) | The Structure of the “THE”-Multiprogramming System | 1968 | Operating Systems / Layered Architecture | Queued | Core |
| [DB-002](notes/DB-002-aries-transaction-recovery.md) | ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging | 1992 | Databases / Transaction Recovery | Queued | Core |
| [OBS-001](notes/OBS-001-dapper-large-scale-distributed-systems-tracing-infrastructure.md) | Dapper, a Large-Scale Distributed Systems Tracing Infrastructure | 2010 | Observability / Distributed Tracing | Queued | Core |

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
