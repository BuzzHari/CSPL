# OS-003 — The Working Set Model for Program Behavior

- **Author:** Peter J. Denning
- **Year:** 1968
- **Field:** Operating Systems / Virtual Memory / Resource Management
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://denninginstitute.com/pjd/PUBS/WSModel_1968.pdf
- **DOI:** https://doi.org/10.1145/363095.363141

## Why it matters

Denning's working-set model supplied a durable way to reason about program locality and virtual-memory allocation. Rather than treating every page referenced by a process as equally important, the model characterizes the process by the pages it has used in a recent window. That makes memory demand a property that can be observed dynamically and gives the operating system a principled basis for deciding how much memory a process needs to run efficiently.

The paper is especially important because it connects locality, paging, scheduling, memory allocation, and thrashing. Its central lesson remains visible in modern operating systems and caches: performance depends strongly on keeping the actively used subset of a workload close to the processor while preventing aggregate demand from exceeding available fast memory.

## Prerequisites

- Virtual memory and paging
- Page faults
- Physical versus virtual memory
- Process scheduling
- Basic notions of locality and caching
- Multiprogramming

## Key ideas

1. **Working set:** A process's current memory demand can be approximated by the distinct pages referenced during a recent execution window.
2. **Locality:** Programs tend to execute for meaningful periods within relatively small subsets of their address spaces rather than access all pages uniformly.
3. **Thrashing:** When the combined active working sets of runnable processes exceed physical memory, page-fault traffic can dominate useful computation.
4. **Memory and scheduling are coupled:** A process should not merely be runnable because a CPU is available; the system must also consider whether enough memory exists for its active working set.
5. **Dynamic observation beats static guesses:** The operating system can infer resource demand from recent behavior instead of relying entirely on users or compilers to predict it in advance.

## Recommended reading approach

**Read fully.** The paper is concise enough to merit a complete read, but do not get stuck on every historical implementation detail during the first pass.

### Section-by-section guide

- **Introduction:** Understand the resource-allocation problem and why Denning argues that users and compilers cannot reliably provide future memory demand.
- **Program behavior / locality:** Focus on the observation that execution moves through relatively stable localities rather than touching the address space uniformly.
- **Working-set definition:** Read carefully. Understand the role of the window parameter and why it is an approximation of the pages currently needed by a computation.
- **Memory demand:** Connect working-set size to the amount of physical memory a process needs to avoid excessive paging.
- **System demand and scheduling:** This is the architectural core. CPU scheduling and memory admission cannot be treated as independent decisions when physical memory is constrained.
- **Implementation policy:** Read for the principle rather than historical hardware details: measure recent use, retain active pages, and avoid admitting more demand than memory can sustain.
- **Conclusion:** Revisit the relationship among locality, allocation, and stable system throughput.

## Estimated reading time

- Focused first read: 45–60 minutes
- With worked page-reference examples and Linux comparisons: 90–120 minutes

## Connection to Linux and Aruba networking work

The working-set idea is directly useful when diagnosing memory-sensitive network software. A Linux process may have a large virtual address space or even a large resident set while only a subset of pages is actively needed on the hot path. Conversely, a process whose active working set no longer fits in available RAM can incur page faults, reclaim pressure, cache disruption, and latency spikes even if CPU utilization appears moderate.

For an Aruba gateway or controller, this matters when packet-processing, telemetry, logs, control-plane databases, and diagnostic tooling compete for memory. Heavy tracing or observability can increase the active memory footprint enough to perturb the system being measured. The paper therefore gives a useful performance question: not just 'how much memory does this process allocate?', but 'what memory must remain resident for the current workload to make progress efficiently?'

On Linux, modern tools such as `/proc/<pid>/smaps`, page-fault counters, PSI memory pressure, reclaim statistics, `perf`, and targeted eBPF instrumentation can help approximate the symptoms and causes of working-set pressure even though the kernel does not implement Denning's original policy literally.

## Questions to answer after reading

1. Why is total allocated memory a poor estimate of a process's immediate memory demand?
2. What does the working-set window parameter trade off?
3. Why can adding more runnable processes reduce total useful throughput?
4. How does thrashing differ from simply having a high page-fault count?
5. Why does Denning couple processor scheduling with memory allocation?
6. Which modern Linux metrics would you use to detect that a workload's active working set no longer fits comfortably in RAM?

## Related indexed papers

- OS-001 — The UNIX Time-Sharing System
- OS-002 — The Structure of the “THE”-Multiprogramming System
- CA-002 — A Case for Redundant Arrays of Inexpensive Disks (RAID)
