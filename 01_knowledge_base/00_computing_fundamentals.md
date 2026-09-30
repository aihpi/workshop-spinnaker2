# Computing Fundamentals

General computing concepts that the other notes build on: bits and cores, the von Neumann architecture and its bottleneck, the memory hierarchy, buses, CPU architectures, compilers and bare-metal programming, and a few practical shell basics. Background for readers without a computer engineering background. The neural computing basics are in `01_primer_snn_basics.md`, the SpiNNaker2 hardware in `02_hardware_energy.md`.

Sources: standard computer architecture knowledge, written up from a learning conversation. Where terms relate to SpiNNaker2, they follow the chip paper (Scholze et al. 2026) and the [py-spinnaker2 documentation](https://spinnaker2.gitlab.io/py-spinnaker2/).

Each section ends with a line **Workshop:** saying what of it is taught in the workshop.

## Contents

- [1. Computing basics](#1-computing-basics)
- [2. The von Neumann architecture](#2-the-von-neumann-architecture)
- [3. Memory hierarchy](#3-memory-hierarchy)
- [4. Buses and communication](#4-buses-and-communication)
- [5. CPU architectures: x86 and ARM](#5-cpu-architectures-x86-and-arm)
- [6. Compilers and bare-metal programming](#6-compilers-and-bare-metal-programming)
- [7. Practical basics: shell scripts and connectivity checks](#7-practical-basics-shell-scripts-and-connectivity-checks)

## 1. Computing basics

Everything a computer stores is ultimately binary. A **bit** is 0 or 1, and eight bits form a **byte** (256 possible values). Larger units are kilobyte (KB), megabyte (MB), gigabyte (GB) and terabyte (TB).

The **CPU** (central processing unit) executes instructions. A **core** is one independent processing engine: modern CPUs have several cores, each running its own stream of instructions. SpiNNaker2 takes this to an extreme with 152 cores per chip.

A **chip** (integrated circuit) is a piece of silicon with etched circuits. A **microcontroller** is a small, self-contained chip that combines a CPU, memory and input/output, designed for embedded devices. The ARM Cortex-M4F cores of SpiNNaker2 are microcontroller-class processors.

The **clock** is a timing signal, measured in hertz (Hz): a 3 GHz CPU performs three billion clock cycles per second. SpiNNaker2 cores run at a modest 150 or 300 MHz, trading the speed of a single core for parallelism and energy efficiency.

**Workshop:** not taught, assumed background.

## 2. The von Neumann architecture

The **von Neumann architecture**, described by John von Neumann in 1945, is the blueprint of almost every general-purpose computer. Its central idea is the **stored-program concept**: instructions and data live together in the same memory, in the same binary format. A CPU repeats the **fetch–decode–execute cycle**: fetch an instruction from memory, decode it, execute it, move on to the next one. The classical components are memory, a control unit, an arithmetic logic unit (ALU), input and output. Control unit and ALU together form the CPU.

### The von Neumann bottleneck

Instructions and data share one memory and one connection to the CPU, so only one transfer can happen at a time. CPUs became much faster than memory over the decades, and this shared path became the performance limit: the **von Neumann bottleneck**, a term coined by John Backus in his 1977 Turing Award lecture. Caches, prefetching, wider buses and out-of-order execution are all workarounds for it.

The main alternative is the **Harvard architecture**, with separate memories and paths for instructions and data. Most modern CPUs use a "modified Harvard" design internally (separate caches for instructions and data) while presenting a single von Neumann memory to software.

Neuromorphic chips like SpiNNaker2 attack the bottleneck differently: each core has its own local memory next to it, and there is no single shared memory for all cores (`02_hardware_energy.md`, section 3).

**Workshop:** 2 min in the motivation block, as the problem that neuromorphic hardware addresses.

## 3. Memory hierarchy

Computers combine several kinds of memory, trading speed against capacity and cost:

| Level | Technology | Typical size | Access time | Role |
|---|---|---|---|---|
| Registers | inside the core | bytes | < 1 ns | fastest working storage |
| L1 cache | SRAM, per core | ~32 KB | ~1 ns | most recently used data |
| L2 cache | SRAM, near the core | ~256 KB | ~3–5 ns | second-level cache |
| L3 cache | SRAM, shared | ~8–32 MB | ~10–20 ns | shared by all cores |
| Main memory | DRAM | ~16 GB | ~50–100 ns | working memory of programs |
| SSD / HDD | flash / magnetic | TB | µs–ms | persistent storage |

- **RAM** (random access memory): volatile working memory in which any location can be accessed directly.
- **DRAM** (dynamic RAM): dense and cheap, but slower, and it needs constant refreshing. Used as main memory. LPDDR4 is a low-power variant.
- **SRAM** (static RAM): faster and more expensive, no refresh needed. Used for caches, and for the local memory of each SpiNNaker2 processing element.
- **VRAM:** the dedicated memory of GPUs, typically GDDR or HBM.
- **Cache:** a small, fast SRAM buffer between the CPU and main memory that holds recently or frequently used data.

### How caches fight the bottleneck

Caches hide the von Neumann bottleneck, without removing it, by exploiting **locality**: programs reuse the same data (temporal locality) and access neighbouring addresses together (spatial locality). If 95 % of accesses hit the cache, the average access time is close to that of the cache rather than that of DRAM. Prefetchers watch the access pattern and load data before it is requested.

This fails for workloads with poor locality, such as sparse graphs or large, sparsely connected neural networks, which access memory in unpredictable patterns. This is one reason why architectures like SpiNNaker2 distribute memory directly among the cores instead.

**Workshop:** not taught separately. The energy cost of memory access is in the primer (Figure 25).

## 4. Buses and communication

A **bus** is a shared communication path, a bundle of wires plus a protocol, that carries data between components. It typically has address lines (where), data lines (what) and control lines (read, write, ready). Only one sender can use a bus at a time.

The **memory bus** connects the CPU with main memory. It is the physical form of the von Neumann bottleneck. Two properties matter: **bandwidth** (bytes per second) and **latency** (time per transfer). Buses are relieved by making them wider or faster, by giving CPUs several memory channels, and by caches, which reduce how often the bus is needed.

Other buses in a computer are **PCIe** (CPU to GPUs, SSDs, network cards) and USB (external devices). Inside large chips, a **network-on-chip** replaces simple buses: a small packet-switched network in which many transfers can happen at the same time. SpiNNaker2 uses one (`02_hardware_energy.md`, section 4).

**Workshop:** not taught.

## 5. CPU architectures: x86 and ARM

An **instruction set architecture** (ISA) is the vocabulary of instructions a CPU understands. Two families dominate:

- **x86** (Intel, AMD, since 1978): a CISC design (complex instruction set computer), developed for desktops and servers. Powerful and backwards-compatible to the 1970s, but with higher power consumption.
- **ARM** (Arm Holdings, since the 1980s): a RISC design (reduced instruction set computer), developed for embedded and mobile devices. Simpler, smaller and more power-efficient. Arm licenses its designs to many companies, which build their own chips.

**RISC vs. CISC:** CISC offers powerful instructions that may do several things at once, which needs complex hardware. RISC uses simple, uniform instructions, arithmetic only between registers, and separate load and store instructions, which keeps the hardware simple. Modern x86 chips internally translate their instructions into RISC-like micro-operations, so the difference has blurred, but ARM designs remain smaller and more efficient per watt.

**Why ARM for SpiNNaker2:** in a system with millions of cores, the power and silicon area per core dominate the design. The Cortex-M4F is small and efficient, so 152 of them fit on one chip at low power. The workload consists of many small parallel updates, so the high single-core performance of x86 isn't needed, and mature ARM compilers and debuggers are available. Apple's M-series chips chose ARM for similar reasons: energy efficiency and the freedom to design their own chips. **RISC-V**, a newer, royalty-free RISC instruction set, may appear in future neuromorphic chips for the same reasons.

**Workshop:** 1 min at most, as background to "why small ARM cores".

## 6. Compilers and bare-metal programming

A **compiler** translates source code (C, C++, Rust, …) into machine code for a specific CPU. The main phases are lexical analysis, parsing, semantic analysis, optimisation and code generation. Machine code is specific to an instruction set: a program compiled for x86 doesn't run on ARM without recompiling it or emulating the other architecture (as Apple's Rosetta 2 does).

**Cross-compilation** means compiling on one architecture for another. It is essential for embedded systems: code is compiled on a laptop or server and runs on ARM Cortex-M4F cores. The chip software of SpiNNaker2 is written in C and compiled with a GCC toolchain for ARM (chip paper). py-spinnaker2 does this automatically for the neuron models, and the option `make_clean=True` of `hw.run` forces a rebuild.

**CMake** is a meta build tool: one `CMakeLists.txt` describes the project, and CMake generates the platform-specific build files (Makefiles, Ninja files, Visual Studio projects). It is widely used for C and C++ projects.

**Bare-metal** programming means running code directly on the hardware, without an operating system in between: no file system, no scheduler, no drivers, but full control over the hardware and predictable timing. Each SpiNNaker2 core runs its neuron model as bare-metal C code. There is no Linux on the cores and no automatic memory management, which is why the memory of each core is laid out explicitly by py-spinnaker2 (`02_hardware_energy.md`, section 3).

**Workshop:** not taught. Relevant for custom neuron models in C, which are an advanced topic.

## 7. Practical basics: shell scripts and connectivity checks

### Writing an executable script

```bash
cat > /path/to/script.sh <<'EOF'
#!/bin/bash
set -euo pipefail
# ... contents ...
EOF
chmod +x /path/to/script.sh
```

- `cat > file <<'EOF' … EOF` is a **heredoc**: everything up to `EOF` is written into `file`. The quotes around `'EOF'` disable variable expansion, so the content is written literally.
- `set -euo pipefail` is a strict mode: `-e` stops at the first error, `-u` treats undefined variables as errors, `-o pipefail` makes a pipeline fail if any of its commands fails.
- `chmod +x` makes the file executable. Without it, `./script.sh` fails with "Permission denied", because files on Linux aren't executable by default. `bash script.sh` works without it.

### A container setup for SpiNNaker2 development

A setup script for a fresh environment typically:

1. updates the package lists and installs basic tools (`curl`, `ca-certificates`, `git`, `build-essential`),
2. runs SpiNNcloud's `libs_install.sh`, which installs SpiNNaker2-specific dependencies (presumably including the ARM cross-compiler and the Digilent Adept drivers),
3. installs `cmake` and `pkg-config`,
4. installs `uv`, a fast Python package and environment manager,
5. checks each tool with `--version`.

### Checking whether the boards are reachable

- **Ping:** checks whether a board answers on the network at all (`ping -c 1 -W 2 <ip>` for each board address). Only works if the network doesn't block ICMP.
- **UDP probe:** sends a small UDP packet to the port used by the board software (port 1800 in the setup scripts used so far) and waits for an answer. This checks that the board's software is actually running, not only that the network interface is up. A diagnostic variant reports the reason for a failure (send failed, timeout, receive failed).

Ping answers "is the board on the network?", the UDP probe "is the board's service running?". Both together give the clearest picture.

**Workshop:** not taught, but useful for preparing the cluster access.

## To check on the cluster

- [ ] Which port and protocol the SpiNNaker2 boards on the HPI cluster use for the UDP probe, and what `libs_install.sh` installs exactly.
