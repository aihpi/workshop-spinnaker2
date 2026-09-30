# Hardware and Energy

What the SpiNNaker2 chip consists of, how py-spinnaker2 uses it, which energy numbers are reported, and how energy can be measured on the chip. The groundwork for the "Motivation" block of the workshop (20 min) and for the energy measurement in hands-on 2. Complements the SNN primer (`01_primer_snn_basics.md`), whose section 9 explains *why* event-driven hardware can save energy.

Main sources: the chip paper [Scholze et al. 2026, arXiv:2607.24396](https://arxiv.org/abs/2607.24396) and the [py-spinnaker2 v0.8 documentation](https://spinnaker2.gitlab.io/py-spinnaker2/) (tutorial 06, power measurement, profiling, memory structure). Numbers from the paper were extracted from its text and still need to be checked against its tables (see the list at the end).

Each section ends with a line **Workshop:** saying what of it is taught in the workshop.

## Contents

- [1. The chip at a glance](#1-the-chip-at-a-glance)
- [2. The processing element](#2-the-processing-element)
- [3. Memory](#3-memory)
- [4. Communication: spikes as packets](#4-communication-spikes-as-packets)
- [5. From one chip to a supercomputer](#5-from-one-chip-to-a-supercomputer)
- [6. Power management](#6-power-management)
- [7. How large a network fits](#7-how-large-a-network-fits)
- [8. Reported energy numbers](#8-reported-energy-numbers)
- [9. Measuring on the chip](#9-measuring-on-the-chip)
- [To check on the cluster](#to-check-on-the-cluster)

## 1. The chip at a glance

SpiNNaker2 is a many-core chip: instead of a few powerful processors it has 152 small, independent ones, each with its own memory, connected by a network that is optimised for sending many small messages (spikes). The name comes from *Spiking Neural Network Architecture*. It was developed at TU Dresden with the University of Manchester, the successor of SpiNNaker1 (Manchester, 2011), and is produced by [SpiNNcloud Systems](https://spinncloud.com).

![Schematic of the SpiNNaker2 chip](figures/02_hardware_energy/01_chip_schematic.png)

***Figure 1.** The main parts of a SpiNNaker2 chip. 152 processing elements (PEs) are grouped into 38 quad processing elements (QPEs) of 4 PEs each. Each PE has its own processor, memory and accelerators (left). Shared by all PEs: the event router and network-on-chip that deliver spikes, the interfaces to external DRAM, six links to neighbouring chips, and Ethernet to the host computer. **Source:** Diagram drawn here from the component list in Scholze et al. 2026. The arrangement of the blocks is schematic, not the physical floorplan.*

| Property | Value |
|---|---|
| Process | GlobalFoundries 22FDX (22 nm FD-SOI) |
| Die size | 102 mm² |
| Processing elements | 152 (38 QPEs × 4), 148 usable for applications in py-spinnaker2 |
| Processor per PE | ARM Cortex-M4F, 150 MHz at 0.5 V or 300 MHz at 0.8 V |
| Memory per PE | 128 KB SRAM |
| On-chip SRAM in total | 158.6 Mbit (about 19.8 MB) |
| External memory | 2 LPDDR4 interfaces, up to 4 GB each (2 GB on the py-spinnaker2 boards, see section 3) |
| Chip-to-chip links | 6 |
| Host connection | 1 Gbit Ethernet |

**Workshop:** 3 min, the figure and the key idea "many small cores with local memory, connected by a spike network".

## 2. The processing element

Each PE is a small computer of its own:

- **ARM Cortex-M4F core.** A microcontroller-class processor with a single-precision floating-point unit, the kind found in embedded devices. It runs the neuron model code: in every timestep it updates the state of all its neurons and processes incoming spikes.
- **128 KB SRAM.** Holds everything the PE needs: about 32 KB for the compiled neuron model code and about 96 KB for data, i.e. neuron states, parameters, synaptic weights and recorded results.
- **Machine learning accelerator (MLA).** A 16 × 4 array of multiply-accumulate units for 8- and 16-bit integers, for dense matrix operations such as convolutions and DNN layers. Up to 4.56 TOPS (tera operations per second) for the whole chip at 300 MHz in matrix-matrix multiplication, and up to 34.3 times faster than the ARM core with its optimised library (CMSIS) for convolutional layers.
- **Numerical accelerator** for exponentials and logarithms, useful for neuron models with exponential terms.
- **Random number generators:** a pseudo-random generator per PE (32 bit per clock cycle), and one true random number generator for the chip. They drive, for example, `poisson_process` and `lif_prob`.
- **DMA engines** (direct memory access), plus an interrupt controller and timers. DMA moves blocks of data, e.g. between SRAM and DRAM, while the core keeps computing.

The combination is what the paper calls *hybrid*: the same chip can run event-driven SNNs on the ARM cores and dense DNN layers on the MAC arrays.

<details>
<summary><b>Why SpiNNaker2 is more than "many ARM cores":</b> what the specialised hardware adds</summary>

<br>

A chip with only 152 ARM cores could run SNNs in principle, but poorly. The hardware around the cores makes the difference:

- **MAC accelerator:** dense matrix operations run many times faster than on the ARM core (up to 34.3 times for convolutional layers).
- **exp/log accelerator:** exponential terms of neuron and synapse models take a few clock cycles instead of a software routine.
- **Random number generators:** stochastic models get random numbers essentially for free.
- **DMA:** cores don't spend cycles copying memory.
- **Router with hardware multicast:** one neuron reaching thousands of targets costs one packet, not thousands (section 4). Without this, communication would swamp computation.
- **Chip-to-chip links:** the system scales to millions of cores without a shared bus (section 5).
- **Power management:** DVFS, power shut-off and body biasing tie energy consumption to activity (section 6).

The ARM cores provide programmability (any neuron model, written in C), the specialised hardware provides speed and efficiency.

</details>

<br>

**Workshop:** 1 min. The ARM core and SRAM matter for the hands-on parts; the accelerators only as an outlook.

## 3. Memory

| Level | Where | Size | Used for |
|---|---|---|---|
| PE-local SRAM | inside each PE | 128 KB | neuron states, parameters, synapses, recordings |
| DRAM (LPDDR4) | outside the chip, shared | 2 GB on the py-spinnaker2 boards (two 1 GB banks) | large data, recordings with `record_on_dram=True` |

Keeping weights in the local SRAM of each PE is central to the energy argument: reading from on-chip SRAM costs about 100 times less energy than reading from external DRAM (primer, Figure 25). Each PE on its own is a small conventional computer, but there is no shared memory or bus for all PEs, so the system as a whole avoids the von Neumann bottleneck of conventional computers (`00_computing_fundamentals.md`, section 2). The price is capacity: 96 KB of data per PE is small, and memory, not compute, is usually what limits how many neurons and synapses fit on a PE (section 7).

The chip paper specifies up to 4 GB per LPDDR4 interface, while tutorial 06 lists 2 GB for the boards used with py-spinnaker2. This is the difference between what the chip supports and what is installed on a board.

<details>
<summary><b>Memory layout of a PE:</b> what lives where in the 128 KB</summary>

<br>

The 128 KB SRAM of a PE is split into two regions ([memory structure](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/memory-structure.html)):

- **ITCM** (instruction memory, about 32 KB): the compiled code of the neuron model.
- **DTCM** (data memory, about 96 KB): everything the host writes before a run, in this order: reserved sections for the program's variables, error logs, a data specification, the memory regions with routing tables, synapse tables and user data, an optional log region, and a 4 KB heap and stack at the end.

The exact number of bits per synapse and the sizes of the synapse and recording regions aren't documented on that page. They are defined in the linker scripts of the neuron models in py-spinnaker2 and can be visualised with the memory visualisation tool of py-spinnaker2.

</details>

<br>

**Workshop:** 2 min. "Local memory saves energy, but limits size" is the key trade-off.

## 4. Communication: spikes as packets

A spike leaves its PE as a small **multicast packet**: it carries a 32-bit routing key that identifies the sending neuron, and no destination address. The **event router** looks up the key in its routing table (16 K entries) and forwards a copy of the packet to every PE, and every neighbouring chip, that has neurons listening to this sender. One spike can thus reach many targets while being sent only once. This is the core idea inherited from SpiNNaker1, and it suits the brain-like pattern of one neuron talking to thousands of others.

- **On the chip:** a network-on-chip (NoC), a small packet-switched network instead of a shared bus, connects the QPEs, the router and the memory interfaces, with a bisection bandwidth of 307 Gbit/s. Each block is attached through a NoC interface that packs outgoing data into packets and delivers incoming ones.
- **Between chips:** 6 serial links per chip, 6 Gbit/s each on a board and 2 Gbit/s between boards, arranged as a hexagonal grid. Inside the chip, data travels on many parallel wires; for the links, SerDes blocks (serialiser/deserialiser) convert it to a fast serial stream and back, because many parallel wires between chips are hard to keep synchronised.
- **To the host:** 1 Gbit Ethernet. py-spinnaker2 uses it to load the network, start the run and read back the results.

In py-spinnaker2, every PE has an address such as `Chip_1_0_QPE_4_5_2`: chip coordinates (1, 0), QPE coordinates (4, 5), PE 2 within the quad.

<details>
<summary><b>Why the router isn't a bottleneck</b>, although every spike passes through it</summary>

<br>

- **Tiny packets:** a spike packet has a 40-bit base payload, so what matters is the packet rate, not the bandwidth. The router runs at 400 MHz with a peak throughput of 1.8 Tbit/s towards the PEs.
- **Multicast in hardware:** the sender emits one packet regardless of how many targets it has.
- **Precomputed routing tables:** a lookup is a table access, fast and predictable.
- **Sparse traffic:** in event-driven networks most neurons are silent, so the router is rarely saturated.
- **One router per chip:** in a multi-chip system, routing capacity grows with the number of chips, so there is no global choke point.

</details>

<br>

**Workshop:** 2 min, as the explanation of why spikes are cheap to send: one packet per spike, copied only where needed.

## 5. From one chip to a supercomputer

| System | Chips | PEs | Notes |
|---|---|---|---|
| Single-chip board | 1 | 152 | `hardware.SpiNNaker2Chip()` in py-spinnaker2 |
| 48-node board | 48 | 7,296 (7,104 for applications) | `hardware.SpiNNcloud48NodeBoard()` |
| SpiNNcloud system at TU Dresden | about 35,000 | about 5 million | eight racks |
| Design limit | | 10 million | hexagonal chip grid |

Which of these the HPI cluster provides, and how many participants can use it at the same time, is still to be checked (brief, open questions).

**Workshop:** 1 min, the scale as a motivation: the same chips scale from a desk to a supercomputer.

## 6. Power management

The chip adapts its power to the load with **dynamic voltage and frequency scaling (DVFS)**: each PE runs at one of four *performance levels*, combinations of two supply voltages and clock frequencies, e.g. 0.5 V with 150 MHz or 0.8 V with 300 MHz. The dynamic power of a digital circuit grows roughly with frequency × voltage², so the low level needs much less power per clock cycle. PEs that have nothing to do can sleep or be switched off entirely (power shut-off), and **adaptive body biasing** of the 22FDX process reduces leakage at low voltage.

![Power per operating state](figures/02_hardware_energy/02_power_states.png)

***Figure 2.** Power of the 152 PEs of one chip in different states, and of the whole chip where reported. Voltage matters most: sleeping PEs at 0.8 V draw more power than busy PEs at 0.5 V, and busy PEs at 0.8 V and 300 MHz draw three times as much as at 0.5 V and 150 MHz, for twice the speed. **Source:** Reported data, Scholze et al. 2026 (baseline power characterisation, CoreMark benchmark).*

In SNNs, the load changes with the spike rate. In the DVS gesture experiment of the paper, each PE switches to the high performance level only when it has received more spikes than a threshold, and otherwise stays at the low level. This saved 28 % energy compared with always running at the high level, while still processing in real time (Figure 3B).

**Workshop:** 2 min. Energy saving on this chip is not only "fewer spikes", but also "slow down when there is little to do".

## 7. How large a network fits

- **Per chip:** more than 150,000 neurons with a 1 ms timestep, according to the paper. The number depends strongly on connectivity, weight precision, recording and timestep, so it is an order of magnitude, not a guarantee.
- **Per PE:** up to 12 million synaptic events per second in a sparse network with 1024 neurons (paper), i.e. 12,000 synaptic events per 1 ms timestep.
- **Limits:** memory (all neuron parameters, states and weights must fit into the 96 KB of data SRAM) and time (all work of a timestep must be done before the next one starts).

The **real-time constraint** is specific to neuromorphic hardware: the chip runs in lockstep with a timer, typically one timestep per millisecond. If a PE needs longer than one timestep for its neurons and incoming spikes, it misses the deadline. py-spinnaker2's profiling records this per timestep (section 9). A network that is too large or too active for its PEs therefore doesn't just run slower, it violates the timing. Spreading a population over more PEs reduces the work per PE.

**Is a PE a neuron?** No. Each PE simulates many neurons, hundreds to about a thousand, in software. A closer analogy: a PE corresponds to a small local population of neurons, the router and links play the role of the long-range axons, and synapses are not hardware at all but entries in weight tables in the SRAM.

How many neurons py-spinnaker2 places on one PE by default for each neuron model isn't stated in the pages read so far (only the `*_1024` variants state 1024 neurons per core). To check.

**Workshop:** 1 min, and relevant for hands-on 1 when participants scale up a network.

## 8. Reported energy numbers

![Reported energy comparisons](figures/02_hardware_energy/03_reported_energy.png)

***Figure 3.** Energy results reported in the chip paper. A: efficiency for dense matrix operations (DNN inference), SpiNNaker2 at its two clock frequencies compared with an edge TPU and an Nvidia Jetson, as quoted in the paper (TOPS/W computed here from the reported TOPS and watts). B: energy for one inference of an SNN that classifies DVS gestures, 1 s of input, at the three performance modes. C: energy per inference of an event-based recurrent language model (EGRU) on SpiNNaker2 and on an Nvidia A100 GPU. **Source:** Reported data, Scholze et al. 2026, extracted from the paper text.*

What the numbers say, and what they don't:

- **Dense DNNs (A):** SpiNNaker2 is in the same range as dedicated edge accelerators (about 2–2.8 TOPS/W), not far ahead of them. For dense workloads there is no neuromorphic advantage, because every operation has to be computed anyway. The paper also notes that the limited DRAM bandwidth reduces practical utilisation.
- **The "18 ×" claim (C):** SpiNNcloud advertises "18× higher energy efficiency than GPUs". The chip paper reports exactly this factor for one workload: an event-based language model that needs 65 mJ per inference on SpiNNaker2 and 1.19 J on an A100, a factor of 18.3. The advertised number therefore appears to come from this benchmark. It is a real measurement, but for one sparse, event-driven model, not a general property of the chip.
- **SNN on the chip (B):** the DVS gesture network (5 layers, 7,859 neurons on 57 PEs, 92 % accuracy) needs 0.74–2.0 J per second of input. The paper gives no GPU comparison for this workload.
- **No energy per synaptic event:** the paper reports energy per inference or per layer, but no pJ per synaptic operation. Comparisons at the level of single operations, as in primer Figure 26, therefore rest on estimates.

The general lesson, which matches primer section 9: the advantage is large where activity is sparse and event-driven, and small or absent for dense computation. This is the message to show with an own measurement rather than with a marketing number.

**Workshop:** 5 min, the core of the motivation block, with the "18 ×" as an example of how to read such claims.

## 9. Measuring on the chip

py-spinnaker2 can measure the power of the board while a network runs ([power measurement](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/power_measurement.html)):

```python
hw.run(net, timesteps, record_power=True)                    # record power samples
hw.run(net, timesteps, record_power=True, live_power=True)   # additionally show them live
```

- **What is measured:** power samples per measurement channel in watts, plus their sum (`total`). Which rails the channels correspond to isn't stated in the documentation.
- **Sampling:** every 0.1 s on the single-chip board, every 0.2 s on the 48-node board.
- **Output:** `power.parquet` (time, channels, total, markers for phases such as the start and end of the simulation) and `power.png`, in `spinnaker2_diagnostics/volatile_diagnostics/`. The console prints energy, duration and average power, e.g. `Power measurement (sim_start -> sim_end): 30.782 J over 0.513 s, average 60.000 W`.
- **Limitation:** runs shorter than the sampling interval produce one or no sample. Runs should last several sampling intervals, i.e. at least a few seconds, which means thousands of timesteps at 1 ms.

The **profiling** of py-spinnaker2 complements this with timing ([profiling](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/profiling.html)): with `profile=True` on a population, each PE records per timestep how long its work took (`duration_us`) and whether it missed the deadline (`deadline_flag` > 0), in `profiling.parquet`.

<details>
<summary><b>A measurement plan for the workshop:</b> how to get a meaningful energy number</summary>

<br>

A single power reading says little, because the board draws power even when nothing happens (Figure 2). A meaningful comparison needs:

1. **Baseline:** the power of the board while idle or running an empty network, to subtract.
2. **Long enough runs:** several seconds per measurement (thousands of timesteps), because of the 0.1–0.2 s sampling interval.
3. **The same network at different activity levels:** e.g. the MNIST network with latency coding and with rate coding, or a network driven by Poisson inputs of different rates. If the energy above the baseline grows with the number of spikes, this shows the event-driven principle directly, and it checks the estimate in primer Figure 26.
4. **Energy per inference:** (energy above baseline) / (number of inputs processed), so that numbers can be compared with other hardware.

A GPU comparison is optional and needs care: the same model, the same accuracy, and the energy of the GPU measured the same way (e.g. with `nvidia-smi`), including idle power.

</details>

<br>

**Workshop:** hands-on 2, where participants measure the energy of their own run.

## To check on the cluster

- [ ] Which boards the HPI cluster has (single-chip, 48-node), and how many can be used at the same time.
- [ ] Power measurement on the HPI setup: which channels are reported, the idle baseline, and the energy of a simple network at different spike rates (measurement plan in section 9).
- [ ] Default number of neurons per PE for each neuron model, and how py-spinnaker2 splits populations.
- [ ] Whether the chip runs at a fixed performance level in py-spinnaker2 or switches automatically, and whether this can be set.
- [ ] Verify the numbers taken from the chip paper against its tables (extracted from the text with a summarisation tool).
- [ ] Whether the accelerators (MLA, exp/log unit, random number generators) belong to each PE or are shared by the 4 PEs of a QPE. The chip paper lists them per PE; an earlier note claimed they are shared per QPE.
- [ ] Why the low performance level needs more energy than the high level in the DVS gesture experiment (Figure 3B), according to the paper.
