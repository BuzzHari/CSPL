# NET-001 — The Click Modular Router

- **Authors:** Eddie Kohler, Robert Morris, Benjie Chen, John Jannotti, M. Frans Kaashoek
- **Year:** 2000
- **Field:** Networking / Operating Systems / Packet Processing
- **Status:** Reading
- **Priority:** Core
- **Primary source:** https://pdos.csail.mit.edu/papers/click:tocs00/paper.pdf

## Why it matters

Click demonstrated that a router datapath could be expressed as an explicit graph of small, reusable packet-processing elements without abandoning high performance.

## Key ideas

1. Fine-grained packet-processing elements
2. Explicit directed processing graphs
3. Push and pull execution models
4. Modular scheduling and queueing
5. Runtime handlers for observability and control

## Work connection

Directly relevant to Aruba datapath architecture, modular packet pipelines, eBPF/XDP composition, and operational observability.
