# EBPF-001 — The BSD Packet Filter: A New Architecture for User-level Packet Capture

- **Authors:** Steven McCanne, Van Jacobson
- **Year:** 1993
- **Field:** eBPF / Packet Filtering / Operating Systems / Networking
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://www.usenix.org/conference/usenix-winter-1993-conference/bsd-packet-filter-new-architecture-user-level-packet
- **Paper:** https://www.usenix.org/legacy/publications/library/proceedings/sd93/mccanne.pdf

## Why it matters

This paper introduced the BSD Packet Filter (BPF), a kernel architecture and compact virtual instruction set for efficient user-level packet capture. BPF moved packet selection into the kernel so unwanted traffic could be rejected before crossing the kernel/user boundary, while keeping filtering programmable through a constrained, analyzable instruction language.

The design became the ancestor of classic BPF and, ultimately, Linux eBPF. Modern eBPF has expanded far beyond packet capture into tracing, observability, security, networking, scheduling, and programmable kernel extensions, but several foundational ideas are already visible here: a small virtual machine, safe execution of user-supplied programs in the kernel, early filtering, and minimizing unnecessary data movement.

## Prerequisites

- Basic Ethernet/IP packet structure
- Kernel versus user space
- System calls and device drivers
- Packet capture tools such as tcpdump at a conceptual level
- Basic CPU register and instruction concepts

## Key ideas

1. **Filter packets before copying them to user space** — reduce kernel/user data movement by rejecting irrelevant packets as early as possible.
2. **Use a small virtual instruction set** — packet-selection logic is expressed as a compact program interpreted inside the kernel.
3. **Register-based execution** — BPF replaces an older stack-oriented packet-filter design with a register-oriented model better suited to contemporary RISC processors.
4. **Batch packet delivery** — buffering multiple accepted packets amortizes system-call and wakeup overhead.
5. **Programmability with constrained execution** — user applications can install expressive packet filters without being allowed to run arbitrary unsafe kernel code.

## Recommended reading approach

**Read fully.** The paper is short, directly relevant to modern eBPF, and its performance arguments are still instructive.

### Section-by-section guide

- **Introduction:** Focus on the central cost model: capturing packets requires kernel/user copying, so filters should discard irrelevant packets before that copy.
- **The Network Tap:** Understand where BPF sits relative to the NIC driver and normal protocol stack, and how packet copies are delivered to listeners.
- **The Packet Filter:** Read carefully. Study the virtual instruction set, accumulator/index registers, packet loads, branches, and return semantics.
- **Filter examples / compilation:** Follow how a high-level capture expression can be translated into a compact filter program.
- **Buffering:** Pay attention to why packet batching matters independently of filter execution speed.
- **Performance:** Separate filtering cost from packet-copy and system-call cost. The paper reports large gains over contemporary packet-capture mechanisms.
- **Conclusions:** Revisit the broader architectural choice: do the minimum safe programmable work in the kernel, and move only useful data across the protection boundary.

## Estimated reading time

- Focused first read: 40–60 minutes
- With instruction-level examples and comparison to eBPF: 90–120 minutes

## Connection to Linux, eBPF, and Aruba networking work

This paper is directly connected to modern Linux eBPF. Classic BPF survives in Linux packet filtering and capture paths, while eBPF generalizes the virtual-machine idea into a much richer execution environment with more registers, maps, helpers, verifier analysis, JIT compilation, and many additional hook points.

For Aruba datapath and observability work, the architectural lesson is particularly useful: **filter and aggregate as close to the event source as safely possible**. If a device generates a very high volume of packets or telemetry events, copying everything to a user-space collector and filtering there wastes memory bandwidth, CPU cycles, queue capacity, and context-switch overhead.

An eBPF-based diagnostic system can instead perform bounded work at the kernel hook—filtering by client MAC, VLAN, interface, packet type, process, or event condition—and emit only the subset or aggregate needed for diagnosis.

The paper also gives useful historical context for why verifier-constrained programmable execution is attractive: it combines much of the flexibility of user-defined logic with the performance advantage of running close to the kernel datapath.

## Questions to answer after reading

1. Why is filtering in user space fundamentally more expensive for high packet rates?
2. Why did BPF move from a stack-based model to a register-based evaluator?
3. How does batching improve performance even when the filter itself is fast?
4. What properties make it reasonable to execute a user-supplied BPF program inside the kernel?
5. Which ideas in this 1993 design are still visible in modern Linux eBPF?
6. For an Aruba diagnostic collector, which events should be filtered in-kernel and which should be sent raw to user space?

## Related indexed papers

- NET-001 — The Click Modular Router
- OS-001 — The UNIX Time-Sharing System
- COMP-001 — Efficiently Computing Static Single Assignment Form and the Control Dependence Graph
- CA-001 — RISC I: A Reduced Instruction Set VLSI Computer
