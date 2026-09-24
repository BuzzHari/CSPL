# DBG-004 — AddressSanitizer: A Fast Address Sanity Checker

- **Title:** AddressSanitizer: A Fast Address Sanity Checker
- **Authors:** Konstantin Serebryany, Derek Bruening, Alexander Potapenko, Dmitry Vyukov
- **Year:** 2012
- **Field:** Debugging / Memory Safety / Dynamic Analysis / Compiler Instrumentation
- **Status:** Queued
- **Priority:** Core
- **Date recommended:** 2026-09-24
- **Primary source:** https://www.usenix.org/conference/atc12/addresssanitizer-fast-address-sanity-checker
- **Venue:** 2012 USENIX Annual Technical Conference (USENIX ATC ’12)

## Why it matters

AddressSanitizer (ASan) made a major class of C and C++ memory bugs practical to catch during ordinary testing. Earlier tools often forced an uncomfortable tradeoff: comprehensive memory checking with very high overhead, or lower overhead with weaker coverage. ASan combined compiler instrumentation, a compact shadow-memory representation, redzones, and allocator cooperation to detect heap, stack, and global out-of-bounds accesses plus heap use-after-free with substantially lower runtime cost than heavyweight binary-instrumentation tools of the time.

The paper’s enduring contribution is not just the specific implementation. It is the systems-design insight that a carefully chosen representation can make an apparently expensive safety property cheap enough to deploy broadly. ASan reserves shadow memory, maps each application address to a compact metadata byte, instruments memory accesses with a short check, poisons redzones around objects, and delays reuse of freed heap memory through quarantine. This shifts memory-corruption debugging from postmortem symptom hunting toward immediate detection close to the faulty access.

The authors reported an average 73% slowdown on SPEC CPU2006, about 3.4× peak memory use in their configuration, and more than 300 previously unknown Chromium bugs found during the first ten months of deployment. The paper also shows how ASan’s speed changed debugging practice: it became practical to run large regression suites and fuzzers under memory checking rather than reserving such tools for small reproductions.

## Prerequisites

You should be comfortable with:

- C/C++ pointers, arrays, stack and heap allocation;
- `malloc`, `free`, use-after-free, buffer overflow, and buffer underflow;
- virtual address spaces and page mappings;
- basic compiler instrumentation;
- the idea of shadow metadata associated with application state.

Reading `DBG-003 — Valgrind: A Framework for Heavyweight Dynamic Binary Instrumentation` first is useful because ASan makes a very different engineering tradeoff: compile-time instrumentation and a specialized memory model in exchange for much lower runtime overhead.

## Reading guide

### 1. Introduction — read fully

Start with the problem statement and the two-part architecture: compiler instrumentation plus a runtime library. The compiler inserts checks around application memory accesses and creates redzones around stack and global objects. The runtime reserves/manages shadow memory, replaces allocation functions, poisons heap redzones, delays reuse of freed objects, and reports failures.

The key question for the whole paper is:

> How little work can the common memory-access path do while still preserving useful memory-safety information?

Do not focus only on the reported slowdown. Notice that the architecture is designed around keeping the inserted check extremely simple.

### 2. Related Work — skim selectively

Read enough to understand the design space:

- **shadow-memory tools** can be precise but historically paid translation overhead;
- **binary instrumentation** tools such as Valgrind are general but substantially slower;
- **debug allocators / guard pages** can catch some heap errors but often consume large amounts of memory and may detect corruption only later;
- **canaries** protect particular control-data boundaries but do not provide general object-bounds checking.

The important point is that ASan deliberately chooses a narrower problem than a universal dynamic-analysis framework and then optimizes hard for that problem.

### 3. AddressSanitizer Algorithm — read very carefully

This is the core of the paper.

#### 3.1 Shadow Memory

The central mapping is conceptually:

```text
application address Addr
        |
        v
shadow address = (Addr >> 3) + Offset
```

With the common 8:1 mapping, one shadow byte describes eight bytes of application memory. Because heap allocations are suitably aligned, those eight application bytes have only a small number of relevant addressability states: all eight bytes valid, the first `k` bytes valid, or the whole region poisoned. Negative shadow values distinguish kinds of poisoned memory such as heap redzones, stack redzones, globals, and freed memory.

This compact encoding is what makes direct shadow translation practical.

#### 3.2 Instrumentation

For an aligned 8-byte access, the fast path is roughly:

```text
ShadowAddr = (Addr >> 3) + Offset
if (*ShadowAddr != 0)
    report_error()
```

Smaller accesses require a slightly richer bounds check when only part of the corresponding eight-byte block is addressable.

Notice where the compiler pass is inserted: late in the LLVM optimization pipeline. This avoids instrumenting source-level memory operations that earlier optimization eliminated, while also avoiding instrumentation of machine-level artifacts such as ordinary register spills introduced later.

#### 3.3 Runtime Library

Read this section closely. The runtime is not incidental glue; it completes the design.

Heap allocations receive poisoned redzones. `free()` poisons the released region and moves it into a quarantine queue rather than making it immediately available for reuse. That increases the window during which a dangling pointer will still point to poisoned memory and therefore turn a temporal bug into a deterministic diagnostic.

Allocation and deallocation call stacks are retained so reports can identify where an object was created and freed, not merely where the invalid access occurred.

#### 3.4 Stack and Globals

The compiler creates redzones around stack and global objects and arranges for their corresponding shadow bytes to be poisoned and unpoisoned at the right times. This is one of the significant coverage differences from many older heap-oriented tools.

#### 3.5–3.7 Limitations, false positives, threads — read fully

The false-negative discussion is important because it defines what ASan actually proves. The paper explicitly accepts some rare misses when eliminating them would make the common path more expensive. It also discusses interactions with compiler transformations and unusual runtime behavior.

This is a useful lesson for instrumentation design: the detector and compiler cannot be reasoned about independently. An optimization that widens a load, for example, can make an otherwise legal source access appear to cross an object boundary unless the compiler pipeline is coordinated with the sanitizer.

### 4. Evaluation — read fully, do not memorize every benchmark

The headline result is an average 73% slowdown on SPEC CPU2006 in the evaluated configuration, with substantially larger memory overhead. The exact numbers are historical; the important comparison is architectural. ASan trades address space and memory for a very short per-access check and thus runs much faster than heavyweight dynamic binary instrumentation tools in the paper’s comparison.

Section 4.2 is especially worth reading. ASan found more than 300 previously unknown Chromium bugs in roughly ten months, dominated by heap use-after-free and heap-buffer-overflow defects. The tool was fast enough to pair effectively with existing unit tests and fuzzing.

Section 4.3 shows how quarantine size, redzone size, and stack-unwind depth move the precision/resource tradeoff. These controls make the general lesson explicit: better diagnostic retention usually costs memory or CPU.

### 5. Future Work — skim, but read the compile-time optimization ideas

The authors discuss eliminating redundant checks, proving some accesses safe statically, instrumenting libraries, and potential hardware support. Several of these ideas became recurring themes in later sanitizer and hardware-memory-safety work.

The useful compiler insight is that instrumentation itself is an optimization problem. Once a safety check exists, normal compiler reasoning can ask whether multiple checks are redundant or whether an access can be proven safe without a runtime check.

### 6. Conclusion — read fully

Return to the architectural result: compact shadow metadata plus compiler-inserted checks made broad memory-error detection cheap enough to be integrated into normal engineering workflows. The paper reports that ASan was already integrated into LLVM 3.1 at publication time.

## Key ideas

1. **Compact shadow memory turns a global safety property into a cheap local lookup.** A deterministic address mapping gives each application access a small metadata check rather than requiring expensive object-table searches.

2. **Redzones convert spatial memory corruption into an immediate fault at the bad access.** Poisoned bytes around heap, stack, and global objects let the detector identify the instruction that crossed an object boundary.

3. **Quarantine extends the lifetime of evidence for temporal bugs.** Freed objects remain poisoned and are not immediately recycled, increasing the probability that a dangling-pointer access is detected as use-after-free instead of silently hitting a new allocation.

4. **Compiler and runtime design are inseparable.** Instrumentation placement, allocator behavior, stack layout, globals, unwinding, and compiler optimizations all cooperate to maintain the detector’s invariants.

5. **A debugging tool becomes transformative when it is cheap enough to run routinely.** ASan’s practical impact came not only from detecting memory errors but from making large test suites and fuzzing campaigns feasible under instrumentation.

## Connection to Linux, Aruba datapath engineering, and debugging

The paper is directly relevant to native datapath software because packet-processing code is full of exactly the operations ASan targets: parsing variable-length headers, indexing rings and descriptor arrays, manipulating session structures, managing object lifetimes, and copying data across independently sized buffers.

Consider a packet parser:

```c
struct iphdr *ip = (struct iphdr *)(buf + l2_len);
if (ip->protocol == IPPROTO_UDP) {
    ...
}
```

If `l2_len` or the captured packet length is wrong, the eventual symptom may be far from this access: corrupted state, a later crash, or a seemingly unrelated forwarding failure. With ASan, the useful goal is to stop at the first invalid load/store and preserve the allocation and stack context around it.

That makes ASan particularly effective in a datapath test matrix containing malformed packets, fuzzed protocol inputs, roam/state churn, repeated client connect/disconnect cycles, and concurrency-heavy lifecycle transitions. A sanitizer build will not have production datapath performance, but it can be extremely valuable in CI and focused stress/fuzz runs because it converts latent heap/stack corruption into a precise failure close to the cause.

There is also a strong architectural parallel to a flight-recorder design. ASan does not log every byte operation in rich form. It keeps **compact state continuously**—shadow bytes, redzones, quarantine metadata—and performs a cheap check on the hot path. Expensive symbolization and human-readable reporting happen only after a violation is detected.

That pattern is broadly useful for low-overhead observability:

```text
compact always-on metadata
        +
cheap hot-path predicate
        +
rich reporting only on violation
```

For Linux/eBPF tooling, the equivalent design question is often whether the hot path can maintain a small invariant or summary instead of emitting every event. ASan is a strong example of how representation choice can determine whether continuous checking is operationally practical.

## Read fully or selectively?

**Read fully.** It is only about ten pages and the core mechanism is directly useful systems knowledge. On a first pass, skim most of Related Work and some detailed benchmark tables, but read Sections 1, 3, 4.2, 4.3, and 6 closely.

**Estimated reading time:** 45–60 minutes; about 75 minutes if you trace the shadow encoding and instrumentation examples carefully.
