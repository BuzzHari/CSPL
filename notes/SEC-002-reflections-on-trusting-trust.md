# SEC-002 — Reflections on Trusting Trust

- **Author:** Ken Thompson
- **Year:** 1984
- **Field:** Computer Security / Compilers / Software Supply Chain
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://doi.org/10.1145/358198.358210
- **DOI:** https://doi.org/10.1145/358198.358210

## Why it matters

Ken Thompson's Turing Award lecture demonstrates a profound limit of source-code inspection: a compiler can be modified to recognize a particular source program, inject malicious behavior into the generated binary, and then reproduce that malicious compiler behavior when compiling future compiler source—even after the malicious source code has been removed. The result is a self-propagating compiler backdoor that is invisible in the source being inspected.

The paper established the classic "trusting trust" attack and made the trusted computing base and software provenance concrete engineering concerns. Its central lesson remains directly relevant to compiler bootstrapping, build systems, package managers, firmware, CI/CD pipelines, signed artifacts, reproducible builds, and modern software-supply-chain security.

## Prerequisites

- Basic compiler pipeline: source code to compiler to executable
- The distinction between source code and generated machine code
- Basic understanding of login/authentication programs
- Self-hosting compilers at a conceptual level
- Basic software-supply-chain terminology is useful but not required

## Key ideas

1. **Source review is not sufficient to establish trust.** The executable that processes trusted source may itself be malicious.
2. **A compiler can recognize special source patterns.** It can silently insert behavior only when compiling a chosen target such as a login program.
3. **The attack can reproduce itself.** A second trigger targeting the compiler source can inject the malicious compiler logic into the next compiler binary, allowing the source-level backdoor to disappear.
4. **Trust is transitive through the toolchain.** Applications inherit assumptions about compilers, assemblers, linkers, build systems, libraries, firmware, and the machines that produced them.
5. **Independent provenance matters.** Confidence improves when artifacts can be rebuilt and compared using independently derived toolchains or other mechanisms that do not share the same trust root.

## Section-by-section reading guide

### Introduction

Read fully. Thompson frames the lecture around how much trust can reasonably be placed in software and the people and tools that produce it.

### Stage I — Learning a compiler trick

Read carefully. Thompson first shows that a compiler can be taught to emit a program containing characters or behavior that are awkward to express directly in the source. This establishes that compilers can encode knowledge about the programs they compile.

### Stage II — Targeting a login program

This is the first security step. Imagine a compiler that recognizes the source of the system login program. Whenever that source is compiled, the compiler emits the normal authentication behavior plus a hidden password or bypass. The login source itself can remain clean.

### Stage III — Targeting the compiler

This is the core of the paper. The compiler is extended with a second trigger that recognizes the source code of the compiler itself and inserts both malicious triggers into the newly generated compiler binary. Once that binary exists, the malicious source can be deleted. Recompiling the apparently clean compiler source still regenerates the compromised compiler.

### Moral and conclusion

Read fully. Focus on the distinction between verifying source text and establishing the provenance of the executable toolchain that turned that text into running code.

## Estimated reading time

- First read: 15–25 minutes
- With a hand-worked compiler-bootstrapping trace: 40–60 minutes

## Recommended reading approach

**Read fully.** It is extremely short, foundational, and the three-stage construction is much more memorable when followed end to end.

## Connection to Linux and Aruba networking work

This maps directly onto the trust chain for network-appliance software. A reviewed source change does not by itself establish that a gateway image contains exactly that behavior. The resulting binary may depend on compilers, linkers, build containers, generated code, package repositories, CI workers, signing infrastructure, and firmware components.

For Linux/eBPF work, the same reasoning applies to the path from C source through Clang/LLVM to BPF bytecode and then through the kernel verifier and JIT to native instructions. A source-level review establishes only one part of that chain. Build provenance, trusted toolchains, artifact hashes, reproducible builds, and independent verification reduce the amount of implicit trust.

The practical diagnostic lesson is also useful: when observed runtime behavior appears impossible given the source, do not assume the source is the complete ground truth. Verify the exact binary, build ID, package/image provenance, compiler/toolchain version, loaded eBPF object, and runtime configuration.

## Questions to answer after reading

1. Why does inspecting the login program's source fail to reveal the first compiler attack?
2. What second trigger makes the attack self-reproducing?
3. Why does removing the malicious compiler source after producing a compromised binary not repair the system?
4. What components belong to the trusted computing base of a modern CI/CD build?
5. How do reproducible builds and diverse double compilation address parts of the trusting-trust problem, and what assumptions remain?

## Related indexed papers

- SEC-001 — The Protection of Information in Computer Systems
- COMP-001 — Efficiently Computing Static Single Assignment Form and the Control Dependence Graph
- OS-001 — The UNIX Time-Sharing System
