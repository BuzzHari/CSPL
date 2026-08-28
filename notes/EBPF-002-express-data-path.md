# EBPF-002 — The eXpress Data Path: Fast Programmable Packet Processing in the Operating System Kernel

- **Authors:** Toke Høiland-Jørgensen, Jesper Dangaard Brouer, Daniel Borkmann, John Fastabend, Tom Herbert, David Ahern, David Miller
- **Year:** 2018
- **Field:** eBPF / XDP / Computer Networking / Operating Systems / Packet Processing
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://doi.org/10.1145/3281411.3281443
- **Accessible author/institutional copy:** https://www.diva-portal.org/smash/get/diva2:1256181/FULLTEXT01.pdf
- **DOI:** 10.1145/3281411.3281443

## Why it matters

This paper gives the first complete architectural description and evaluation of XDP, the Linux kernel's high-performance programmable receive path. Instead of bypassing the kernel completely, XDP runs verified eBPF programs in the network-device receive path before the normal networking stack has allocated and populated its usual packet structures. This retains Linux's device management, isolation and networking integration while moving programmable packet processing close enough to the hardware to reach very high packet rates.

The authors report single-core processing rates up to roughly 24 million packets per second and demonstrate layer-3 routing, inline DDoS mitigation and layer-4 load balancing. More important than the benchmark is the design point: XDP combines programmable fast-path execution with the kernel's security boundary, eBPF verifier, maps, JIT compilation and normal networking stack.

## Prerequisites

- Linux receive-path basics: NIC, driver, kernel networking stack and sockets
- Classic BPF/eBPF at a conceptual level
- Kernel space versus user space
- Packet parsing, forwarding and dropping
- Basic understanding of DPDK/kernel bypass
- JIT compilation and program verification at a high level

Reading `EBPF-001 — The BSD Packet Filter` first is useful because this paper explicitly builds on the BPF lineage.

## Key ideas

1. **Execute before expensive kernel packet construction** — the XDP hook runs in the driver receive path before the normal stack performs much of its per-packet work, so packets that will be dropped or redirected can avoid that cost.
2. **Keep the kernel instead of bypassing it** — XDP seeks kernel-bypass-class performance while preserving Linux device ownership, isolation, configuration, routing and deployment mechanisms.
3. **Safe programmability through eBPF** — programs are verified before loading and JIT-compiled to native instructions, permitting dynamically loaded packet-processing logic without arbitrary kernel modules.
4. **Maps separate fast-path code from state/control** — BPF maps provide persistent/shared state and a communication channel between eBPF programs and user-space control planes.
5. **Explicit packet verdicts create composable fast paths** — XDP programs can drop, pass, transmit back out, or redirect packets, allowing selective acceleration while retaining access to the normal kernel stack.

## Recommended reading approach

**Read fully.** It is only 13 pages and is directly relevant to Linux/eBPF datapath engineering.

### Section-by-section guide

- **1. Introduction:** Read fully. Understand the paper's central trade-off between DPDK-style kernel bypass and a programmable path that remains integrated with Linux. Note the claimed benefits: security boundary, standard management, dynamic reprogramming and CPU use that scales with packet load.
- **2. Related Work:** Read selectively. Focus on DPDK/kernel bypass, kernel modules and programmable hardware. The comparison clarifies exactly where XDP positions itself.
- **3. The Design of XDP:** Read very carefully. This is the core. Study the driver hook, packet actions, the eBPF VM, BPF maps, verifier and execution model. Figure 1 is especially useful for locating XDP relative to the driver, regular network stack, AF_XDP and user space.
- **4. Performance Evaluation:** Read carefully, but separate architecture from benchmark numbers. Look at drop, forwarding and CPU-scaling results and why minimum-sized packets stress packets-per-second throughput.
- **5. Example Applications:** Read fully. Routing, DDoS filtering and load balancing show that XDP is not only a microbenchmark mechanism but a general packet-processing substrate.
- **6. Future Directions:** Read selectively. Some details are historical because XDP/eBPF evolved significantly after 2018, but this section helps distinguish the paper's then-current limitations from its architectural core.
- **7. Conclusion:** Read fully and restate the design trade-off in your own words.

## Connection to Linux and Aruba networking work

This paper maps almost directly onto datapath questions in Linux-based networking products. If a packet must be classified, dropped, redirected, counted or sampled, doing so at XDP can avoid allocations and deeper stack traversal that would otherwise happen before the decision is made.

For an Aruba-style gateway or diagnostic prototype, useful patterns include:

- early filtering of traffic for one client, VLAN, tunnel or flow;
- high-rate drop or anomaly counters stored in per-CPU maps;
- selective packet metadata export instead of copying every packet to user space;
- redirection to another interface, CPU or AF_XDP consumer;
- temporary, dynamically loaded diagnostic logic without rebuilding the kernel or datapath process.

The important architectural comparison with DPDK is also relevant: DPDK maximizes control and performance by taking the device into a user-space dataplane, whereas XDP deliberately keeps Linux in control of the NIC and uses eBPF to insert bounded custom logic at the earliest receive point. The right choice depends on whether the system values absolute isolation from the kernel stack or cooperative integration with Linux networking and management.

For observability, the paper reinforces a principle already visible in BPF and DTrace: filter and aggregate close to the event source. If only a tiny fraction of packets are diagnostically interesting, exporting the entire packet stream to user space is often the wrong architecture.

## Questions to answer after reading

1. Where exactly does native-driver XDP execute relative to skb allocation and the normal Linux receive path?
2. What are the semantic differences among XDP_DROP, XDP_PASS, XDP_TX and XDP_REDIRECT?
3. Which safety properties come from the verifier, and which still depend on driver/kernel correctness?
4. Why can XDP retain Linux integration while avoiding much of the normal per-packet cost?
5. When would DPDK still be a better architectural choice?
6. How do BPF maps turn an otherwise stateless packet program into part of a larger control/data-plane system?
7. Which measurements would you collect before deciding whether a packet-processing function belongs in XDP, TC, the normal socket path, or a user-space dataplane?

## Related indexed papers

- EBPF-001 — The BSD Packet Filter: A New Architecture for User-level Packet Capture
- NET-001 — The Click Modular Router
- NET-003 — Congestion Avoidance and Control
- OBS-002 — Dynamic Instrumentation of Production Systems
- CA-001 — RISC I: A Reduced Instruction Set VLSI Computer
