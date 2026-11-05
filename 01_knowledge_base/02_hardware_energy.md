# Hardware and Energy

What the SpiNNaker2 chip consists of, how py-spinnaker2 uses it, which energy numbers are reported, and how energy can be measured on the chip. The groundwork for the "Motivation" block of the workshop (20 min) and for the energy measurement in hands-on 2. Complements the SNN primer (`01_primer_snn_basics.md`), whose section 9 explains *why* event-driven hardware can save energy.

Main sources: the chip paper [Scholze et al. 2026, arXiv:2607.24396](https://arxiv.org/abs/2607.24396), the PE architecture paper [Höppner et al. 2021, arXiv:2103.08392](https://arxiv.org/abs/2103.08392), [Nazeer et al. 2024, arXiv:2312.09084](https://arxiv.org/abs/2312.09084) (the source of the "18×"), and py-spinnaker2 v0.8: its [documentation](https://spinnaker2.gitlab.io/py-spinnaker2/) (tutorial 06, power measurement, profiling, memory structure) and its code, including the chip-side C code ([snn-core](https://gitlab.com/spinnaker2/snn-core)) and the host library SpiNNMan2. All numbers were checked against the full texts and tables on 2026-09-30.

Each section ends with a line **Workshop:** saying what of it is taught in the workshop.

## Contents

- [1. The chip at a glance](#1-the-chip-at-a-glance)
- [2. The processing element](#2-the-processing-element)
- [3. Memory](#3-memory)
- [4. Communication: spikes as packets](#4-communication-spikes-as-packets)
- [5. From one chip to a supercomputer](#5-from-one-chip-to-a-supercomputer)
- [6. Power management](#6-power-management)
- [7. Limits in practice: when a network doesn't fit](#7-limits-in-practice-when-a-network-doesnt-fit)
- [8. Reported energy numbers](#8-reported-energy-numbers)
- [9. Measuring on the chip](#9-measuring-on-the-chip)
- [To check on the cluster](#to-check-on-the-cluster)

## 1. The chip at a glance

SpiNNaker2 is a many-core chip: instead of a few powerful processors it has 152 small, independent ones, each with its own memory, connected by a network that is optimised for sending many small messages (spikes). The name comes from *Spiking Neural Network Architecture*. It was developed at TU Dresden with the University of Manchester, as the successor of SpiNNaker1 (University of Manchester, whose million-core machine was completed in 2018), and is produced by [Sparxity](https://sparxity.ai), called SpiNNcloud Systems until October 2026 (Silicon Saxony 2026).

Physically, the chips sit on boards, and the boards in a frame in a server rack of the computing centre. Figure 1 follows this hierarchy down to a single chip, with the numbers of the HPI installation (section 5):

![From the rack to the chip](figures/02_hardware_energy/01_installation_hierarchy.png)

***Figure 1.** Where the chips physically are, and how data from py-spinnaker2 reaches them (purple). A: the SpiNNaker2 frame is mounted in a server rack of the computing centre. py-spinnaker2 runs on a cluster node, which talks to the frame via Ethernet. B: the frame, seen from the front, holds 6 boards side by side, each with its own Ethernet connection, and a management controller that switches the boards on and boots them. A run reserves one board (red). C: that board, seen from above: 48 chips (a 48-node board), each with its own DRAM (red), which consists of separate memory chips next to it on the board. The chips are connected to their neighbours by links on the board (green). Each chip has 6 links: on the square grid of the drawing, these are the 4 horizontal and vertical neighbours plus one diagonal direction, which together form the hexagonal grid of the chip paper. Data from the host enters at a chip and travels over these links to the chips that need it. D: one of these chips, about 1 cm × 1 cm, with its 152 processing elements and their local SRAM (orange), shown in detail in Figure 2. The DRAM itself is outside the chip; on the chip sits only its interface (red, at the edge). Colours as in Figure 2: orange for on-chip SRAM, red for off-chip DRAM and its interface. For users, the relevant size is one board: 7,296 PEs, of which 7,104 are available to a run. **Source:** Diagram. Numbers from the HPI installation (boot log and vendor, see section 5) and the chip paper (die size 102 mm²). That the host talks to the board through one chip follows from the py-spinnaker2 code, which addresses the board through chip (0, 0). The arrangement of chips and links on the board and the position of the cluster node are not confirmed yet, the layout is schematic.*

![Schematic of the SpiNNaker2 chip](figures/02_hardware_energy/01_chip_schematic.png)

***Figure 2.** A SpiNNaker2 chip at three levels of zoom. A: the chip with its 38 quad processing elements (QPEs), each with 4 processing elements (PEs), every PE drawn as its core (blue) on top of its local memory (orange). Shared by all PEs: the router in the middle, the links to neighbouring chips, the DRAM interface and Ethernet. The red arrows show the path of one spike: the PE of the firing neuron sends one packet, the router looks up the packet's key and sends copies to every PE and to every neighbouring chip that has neurons listening to this sender (section 4). B: one QPE, whose 4 PEs share one connection to the network-on-chip. C: what one PE contains. **Source:** Diagram drawn here from the component list in Scholze et al. 2026 and py-spinnaker2 tutorial 06. The arrangement of the blocks and the spike path are schematic, not the physical floorplan.*

| Property | Value |
|---|---|
| Process | GlobalFoundries 22FDX (22 nm FD-SOI) |
| Die size | 102 mm² |
| Processing elements | 152 (38 QPEs × 4), 148 usable for applications in py-spinnaker2 (the 4 PEs of one QPE run the system software SCAMP2) |
| Processor per PE | ARM Cortex-M4F, 150 MHz at 0.5 V or 300 MHz at 0.8 V |
| Memory per PE | 128 KB SRAM |
| On-chip SRAM in total | 158.6 Mbit (about 19.8 MB) |
| External memory | 2 LPDDR4 interfaces, up to 4 GB each (2 GB per chip on the 48-node boards, of which py-spinnaker2 v0.8 can address 1 GB, section 3) |
| Chip-to-chip links | 6 |
| Host connection | 1 Gbit Ethernet (UDP) |

**Workshop:** 3 min, the figure and the key idea "many small cores with local memory, connected by a spike network".

## 2. The processing element

Each PE is a small computer of its own (a photo of a test chip and the layout of one QPE are in Höppner et al. 2021, Fig. 12, the layout of the whole chip in Scholze et al. 2026, Fig. 2):

- **ARM Cortex-M4F core.** A microcontroller-class processor with a single-precision floating-point unit, the kind found in embedded devices. It runs the neuron model code: in every timestep it updates the state of all its neurons and processes incoming spikes.
- **128 KB SRAM.** Holds everything the PE needs: about 32 KB for the compiled neuron model code and about 96 KB for data, i.e. neuron states, parameters, synaptic weights and recorded results. Part of the data memory goes to the model's own variables, so for `lif` about 68 KiB remain for the network (section 3).
- **Machine learning accelerator (MLA).** A 16 × 4 array of multiply-accumulate units for 8- and 16-bit integers, for dense matrix operations such as convolutions and DNN layers. Up to 4.56 TOPS (tera operations per second) for the whole chip at 300 MHz in matrix-matrix multiplication, and up to 34.3 times faster than the ARM core with its optimised library (CMSIS) for convolutional layers.
- **Numerical accelerator** for exponentials and logarithms, about 5 times faster than the software routines of the C library (3 to 3.5 times including the conversion from floating point), useful for neuron models with exponential terms.
- **Random number generators:** a pseudo-random generator per PE (32 bit per clock cycle), and one true random number generator for the chip. In py-spinnaker2, `qubo_neuron` draws from the hardware generator; `poisson_process` and `lif_prob` use a generator seeded with their `seed` parameter (snn-core code).
- **Rounding accelerator** for integer rounding and saturation, including stochastic rounding.
- **Event handler:** filters incoming spike packets and stores them in a buffer in SRAM, without interrupting the core.
- **DMA engines** (direct memory access), plus an interrupt controller and timers. DMA moves blocks of data, e.g. between SRAM and DRAM, while the core keeps computing, and writes every incoming spike packet into the spike buffer.

![How the parts of a PE work together](figures/02_hardware_energy/02_pe_function.png)

***Figure 3.** How the parts of a PE work together in one timestep, with the same colours as Figure 4: processing incoming spikes in orange, updating neurons in blue. ① The timer wakes the core. ② Spike packets that arrived from other PEs during the previous timestep have already been written into a spike buffer in the SRAM by the DMA, in the background and without interrupting the core. ③ The core reads the buffered spikes and, for each of them, the synapse tables that say which of its neurons are targets, and with which weights. ④ It adds the weights to these neurons and updates the states of all its neurons, also in SRAM. ⑤ Neurons that crossed their threshold send a spike packet into the network. The strip at the bottom shows where these steps fall within the timestep: after the work, the PE sleeps until the next timer tick. Everything the core needs sits in its own SRAM, so none of the steps has to wait for DRAM. The accelerators (dashed) are only used by some models, and the DRAM only for large data such as recordings with `record_on_dram`. **Source:** Schematic of the principle, not the physical layout. From the sources: the parts of the PE (chip paper, py-spinnaker2 tutorial 06), the SRAM regions (py-spinnaker2 memory structure), and the order of the steps, the spike buffer and the sleep (chip paper, section IV-D and supplement; py-spinnaker2 SNN intro; snn-core code). Durations in the strip are schematic. Which models use which accelerator is not known.*

The combination is what the PE architecture paper (Höppner et al. 2021) calls *hybrid*: the same chip can run event-driven SNNs on the ARM cores and dense DNN layers on the MAC arrays.

<details>
<summary><b>Why SpiNNaker2 is more than "many ARM cores":</b> what the specialised hardware adds</summary>

<br>

A chip with only 152 ARM cores could run SNNs in principle, but poorly. The hardware around the cores makes the difference:

- **MAC accelerator:** dense matrix operations run many times faster than on the ARM core (up to 34.3 times for convolutional layers).
- **exp/log accelerator:** exponential terms of neuron and synapse models take 7 to 22 clock cycles, about 5 times faster than in software.
- **Random number generators:** stochastic models get random numbers essentially for free.
- **DMA:** cores don't spend cycles copying memory.
- **Router with hardware multicast:** one neuron reaching thousands of targets costs one packet, not thousands (section 4). Without this, communication would swamp computation.
- **Chip-to-chip links:** the system scales to millions of cores without a shared bus (section 5).
- **Power management:** DVFS and power shut-off tie energy consumption to activity, and body biasing keeps the PEs fast enough at low voltage (section 6).

The ARM cores provide programmability (any neuron model, written in C), the specialised hardware provides speed and efficiency.

</details>

<br>

![How a PE spends its timesteps](figures/02_hardware_energy/02_pe_timestep.png)

***Figure 4.** What a PE does over ten timesteps, here of 1 ms each, a common choice (the length of a timestep is configurable). A timer interrupt starts every step. The PE first processes the spikes that arrived (orange), then updates its neurons and sends their spikes (blue), and sleeps for the rest of the step (grey). The more spikes arrive, the longer the orange part. In a sparse network, the PE sleeps most of the time, which is where the energy saving of event-driven hardware comes from (section 6). If too many spikes arrive in one step (step 6), the work doesn't fit into the step and the next step starts late, a violated real-time deadline (section 7). **Source:** Illustration, spike counts and durations made up, not measured on the chip. From the sources: timer-driven timesteps, the order of spike processing and neuron update, sleeping for the rest of the step, and that the processing time grows with the input spike rate (chip paper; snn-core code); the measurement of the work per timestep and of deadline misses, where work that overruns extends into the following timesteps (py-spinnaker2 profiling).*

**Is a PE a neuron?** No. Each PE simulates many neurons in software: up to 256 with most neuron models, up to 1024 with some variants (primer, section 4). A closer analogy: a PE corresponds to a small local population of neurons, the router and links play the role of the long-range axons, and synapses are not hardware at all but entries in weight tables in the SRAM.

**Workshop:** 1 min. The ARM core and SRAM matter for the hands-on parts; the accelerators only as an outlook.

## 3. Memory

| Level | Where | Size | Used for |
|---|---|---|---|
| PE-local SRAM | inside each PE | 128 KB | neuron states, parameters, synapses, recordings |
| DRAM (LPDDR4) | outside the chip, shared by all PEs | 2 GB per chip on the 48-node boards, of which py-spinnaker2 v0.8 can address 1 GB | large data, recordings with `record_on_dram=True` (a `Population` argument) |

Keeping weights in the local SRAM of each PE is central to the energy argument: reading from on-chip SRAM costs 10 to 100 times less energy than reading from external DRAM, depending on the size of the SRAM (primer, Figure 25). Each PE on its own is a small conventional computer. The chip does have memory that all PEs share, the DRAM, and a PE can also reach the SRAM of other PEs over the network-on-chip. But the SNN software keeps all neuron states and weights in the local SRAM of each PE, so in normal operation the PEs don't compete for a shared memory: the von Neumann bottleneck of conventional computers is avoided by how the chip is used (`00_computing_fundamentals.md`, section 2). DNN workloads whose data don't fit into the SRAM do run into the limited bandwidth of the DRAM (Scholze et al. 2026). The price of local memory is capacity: about 68 KiB of network data per PE (for `lif`) is small, and memory, not compute, is usually what limits how many neurons and synapses fit on a PE (section 7).

The chip paper specifies up to 4 GB per LPDDR4 interface. The 48-node boards carry 2 GB per chip (Gonzalez et al. 2024; tutorial 06: two 1 GB banks), and py-spinnaker2 v0.8 can address 1 GB of it (py-spinnaker2, SNNs on SpiNNaker2).

Figure 5 makes this concrete with two example networks from the primer. The first is the **MNIST network** of primer sections 6 and 8 (Figures 19 and 24), which classifies handwritten digits: 784 input neurons (one per pixel of a 28 × 28 image), 128 hidden neurons and 10 output neurons (one per digit). Its *layer 1* is the set of connections from the inputs to the hidden neurons: with every input connected to every hidden neuron, that is 784 × 128 = 100,352 synapses. Its *layer 2* connects the hidden neurons to the outputs, 128 × 10 = 1,280 synapses. The second is the **clustered network** of primer section 7 (Figure 21), with 250 neurons and about 12,000 synapses.

![Memory of a PE and the trade-off between SRAM and DRAM](figures/02_hardware_energy/03_memory.png)

***Figure 5.** Why SpiNNaker2 keeps the data local, and what that costs. A: reading all weights of the first MNIST layer (primer Figure 24) once, at 2 bytes per synapse, takes 0.25–0.96 µJ from SRAM, depending on its size, but about 33 µJ from the DRAM next to the chip, 34 to 130 times more. Synapses are read whenever a spike arrives, so over many timesteps this difference adds up. B: the price is capacity. Each box is the memory of one PE that is left for the network (about 68 KiB for `lif`). Every presynaptic neuron gets a row of synapses in each PE it projects to, with a 12-byte header and 2 bytes per synapse, plus a 12-byte routing entry. For the first MNIST layer, at most 26 of the 128 hidden neurons fit on one PE, so the layer is split across 5 PEs. The clustered network fits easily, but needs 2 PEs, because each PE holds only one population. The second MNIST layer fits into one PE. **Source:** A: estimate computed here; energy per 64-bit read from Horowitz 2014 (45 nm: 8 KB SRAM 10 pJ, DRAM 1.3 nJ; the 128 KB value interpolated between his 32 KB and 1 MB values), as an order of magnitude, not measured on SpiNNaker2. B: memory per PE and per synapse as computed by py-spinnaker2 v0.8 itself, with its mapping run without a board (`hw.run(..., mapping_only=True)`), which reports the 26 neurons per PE for the MNIST layer; the clustered network is estimated with the same rules from its expected synapse counts. Neuron parameters and recordings, which also need memory, are not drawn.*

<details>
<summary><b>Memory layout of a PE:</b> what lives where in the 128 KB</summary>

<br>

The 128 KB SRAM of a PE is split into two regions ([memory structure](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/memory-structure.html)):

- **ITCM** (instruction memory, about 32 KB): the compiled code of the neuron model.
- **DTCM** (data memory, about 96 KB): in this order, the program's own variables, then what the host writes before a run (error logs, a data specification, the memory regions with routing tables, synapse tables and user data, an optional log region), and a 4 KB heap and stack at the end.

The synapse format is defined per neuron model in py-spinnaker2 (a 16-bit word for most models, primer section 4), and the sizes of the synapse and recording regions are computed when the network is mapped. They can be inspected with the memory report and the memory visualisation tool of py-spinnaker2. For `lif`, the model's own variables occupy the start of the DTCM, and the regions the host writes start at address `0xE000`, which leaves about 68 KiB up to the heap and stack at `0x1F000` (py-spinnaker2 code).

</details>

<br>

**Workshop:** 2 min. "Local memory saves energy, but limits size" is the key trade-off.

## 4. Communication: spikes as packets

The chip's router supports **multicast packets**: a packet carries a 32-bit routing key that identifies the sending neuron, and no destination address. The **event router** looks up the key in its routing table (16 K entries) and forwards a copy of the packet to every PE, and every neighbouring chip, that has neurons listening to this sender. One spike can thus reach many targets while being sent only once. This is the core idea inherited from SpiNNaker1, and it suits the brain-like pattern of one neuron talking to thousands of others.

py-spinnaker2 v0.8 doesn't use multicast by default, but **core-to-core** routing: the sending PE emits one packet per target PE, each with the address of its destination (py-spinnaker2, simulation options; snn-core). That is still one packet per PE, not per synapse, but without the router's copying. Multicast has to be switched on with `backend_settings.set_routing_type("MC")`, supported since v0.8.0.

- **On the chip:** a network-on-chip (NoC), a small packet-switched network instead of a shared bus, connects the QPEs, the router and the memory interfaces, with a bisection bandwidth of 307 Gbit/s. Each block is attached through a NoC interface that packs outgoing data into packets and delivers incoming ones.
- **Between chips:** 6 links per chip, arranged as a hexagonal grid, each in one of two modes. On a board, a link sends 6 bits in parallel together with a clock signal, at only 0.5 V to save power, 6 Gbit/s in total. Between boards, over cables up to 1.5 m long, a link sends one serial stream per direction at 2 Gbit/s, and the receiver recovers the clock from the data itself, because separate clock and data wires are hard to keep synchronised over that distance (chip paper).
- **To the host:** 1 Gbit Ethernet with UDP. py-spinnaker2 uses it to load the network, start the run and read back the results.

![Multicast routing](figures/02_hardware_energy/04_multicast.png)

***Figure 6.** How one spike reaches many neurons. A: with multicast, a firing neuron's PE sends a single packet with the neuron's key. The router looks up the key in its table and sends one copy to every PE and link that has target neurons for this sender, here 3 PEs and one link to a neighbouring chip. Inside each target PE, the packet is handed to its own target neurons through the synapse table (step ③ in Figure 3), without any further packets. In total, this spike costs 1 packet plus 4 copies, however many target neurons the 3 PEs hold (red box). The neighbouring chip may copy the packet further to its own PEs. B: how many packets the sending PE emits for one spike, for two examples. A spike of an MNIST input neuron has 128 targets in the hidden layer, split across 5 PEs (Figure 5). One packet per target neuron would mean 128 packets; py-spinnaker2's default, core-to-core routing, sends one packet per target PE, i.e. 5; with multicast the PE sends 1 and the router makes the copies. For a cortex-like neuron with 1,000 targets on 10 PEs: 1,000, 10 and 1. Fewer packets mean less traffic in the network-on-chip and less energy per spike. **Source:** Diagram and computed illustration. Keys, table entries and the distribution of target neurons across PEs are made up or assumed; the principle follows the chip paper (multicast packets with 32-bit keys, routing table with 16 K entries) and the routing modes of py-spinnaker2 (simulation options; snn-core code).*

In py-spinnaker2, every PE has an address such as `Chip_1_0_QPE_4_5_2`: chip coordinates (1, 0), QPE coordinates (4, 5), PE 2 within the quad.

<details>
<summary><b>Why the router isn't a bottleneck</b>, although every spike passes through it</summary>

<br>

- **Tiny packets:** a multicast spike packet has only 40 bits (the 32-bit key plus control bits), optionally extended by up to 128 bits of payload, so what matters is the packet rate, not the bandwidth. The router runs at 400 MHz with a peak throughput of 1.8 Tbit/s towards the PEs.
- **Multicast in hardware:** with multicast routing, the sender emits one packet regardless of how many targets it has.
- **Precomputed routing tables:** a lookup is a table access, fast and predictable.
- **Sparse traffic:** in event-driven networks most neurons are silent, so the router is rarely saturated.
- **One router per chip:** in a multi-chip system, routing capacity grows with the number of chips, so there is no global choke point.

</details>

<br>

**Workshop:** 2 min, as the explanation of why spikes are cheap to send: one packet per target PE (default) or per spike (multicast), not one per synapse.

## 5. From one chip to a supercomputer

| System | Chips | PEs | Notes |
|---|---|---|---|
| Single-chip board | 1 | 152 (148 for applications) | `hardware.SpiNNaker2Chip()` in py-spinnaker2 |
| 48-node board | 48 | 7,296 (7,104 for applications) | `hardware.SpiNNcloud48NodeBoard()` |
| SpiNNcloud system at TU Dresden | about 35,000 | about 5 million | eight racks |
| Planned maximum | | 10 million | target of the SpiNNaker2 roadmap (Mayr et al. 2019), 10 times SpiNNaker1 |

![Scale of SpiNNaker2 systems](figures/02_hardware_energy/05_scale.png)

***Figure 7.** A: the number of processing elements, from one chip to the largest systems. One run on the HPI installation uses one 48-node board, 7,296 PEs (7,104 available). B: how many neurons that corresponds to, at about 150,000 neurons per chip, compared with the brains of a mouse and a human. This is an upper bound: it needs about 1000 neurons per PE, as in the `*_1024` model variants, while the default `lif` holds at most 256 per PE, i.e. about 38,000 per chip (section 7). Even the Dresden system reaches only a few percent of the neurons of a human brain, and far fewer of its synapses. **Source:** PE and chip counts reported (chip paper, py-spinnaker2 tutorial 06, section 5 for the HPI installation). Neuron capacities estimated here from the paper's figure of more than 150,000 neurons per chip (with a 1 ms timestep), which depends strongly on connectivity. Brain sizes: common estimates of about 70 million (mouse) and 86 billion (human) neurons.*

**The HPI setup** (as of 1 October 2026, from the vendor, the boot log and runs on the cluster; how to run is in [`03_setup/`](../03_setup/README.md)):

- **6 boards in one frame.** The board management controller of the frame reports 6 boards, and the vendor refers to the installation as a 6-board system.
- **48-node boards**, i.e. 6 × 48 = 288 chips in total. The boot log lists 49 devices on the management bus of a board (48 chips plus a controller), and runs with `hardware.SpiNNcloud48NodeBoard()` report 7,104 available cores (the SpiNNcloud tutorials run on the cluster).
- **One board per run, for now.** Multi-board simulations aren't supported yet and are expected in a few months, so the board-to-board cables aren't needed yet. A single 48-node board is far larger than any network planned for the workshop. Within a board, a network can be spread over several chips, with spikes routed between them by C2C or MC routing (py-spinnaker2, advanced SNN usage). Whether spikes between chips work on the HPI boards is not tested yet: the large power-measurement networks of 2026-10-19 used all 48 chips, but each population was connected only to itself. Published SpiNNaker2 work almost never uses more than one chip (`04_applications.md`, section 2.2).
- **Boards are locked per user.** When a run starts, the session software (SpiNNMan2, used by py-spinnaker2) reserves a board with a lock file ("The board is locked for you"). The lock covers the whole board, not single chips (SpiNNMan2 code), so at most 6 people can run on the chips simultaneously.

<details>
<summary><b>Reading the boot log:</b> what happens when a run starts</summary>

<br>

The start of a run on the cluster shows the boot sequence of a board:

- the machine configuration is read, and the frame's management controller (an STM32 microcontroller) finds the boards on its management bus
- a board is locked for the user
- the board is power-cycled and the chips are switched on: core clock, adaptive body biasing (`turn on ABB`, which may need a second attempt before it reports `locked`), the LPDDR4 DRAM interfaces, clock distribution, the network-on-chip router, and Ethernet
- `qgrid_adpll with default clk 1200.00 MHz` is the frequency of a clock generator (PLL). The clock of the PEs (150 or 300 MHz) is derived from it by dividing it down, so 1200 MHz is not the PE clock.
- a small operating program (SCAMP2) is loaded onto the chips, where it runs on the 4 PEs of one QPE, and the kernel status of each chip is checked

</details>

<br>

**Workshop:** 1 min, the scale as a motivation: the same chips scale from a desk to a supercomputer.

## 6. Power management

The chip adapts its power to the load with **dynamic voltage and frequency scaling (DVFS)**: each PE runs at one of four *performance levels*, combinations of two supply voltages and clock frequencies, e.g. 0.5 V with 150 MHz or 0.8 V with 300 MHz. The dynamic power of a digital circuit grows roughly with frequency × voltage², so the low level needs much less power per clock cycle. PEs that have nothing to do can sleep or be switched off entirely (power shut-off). **Adaptive body biasing** of the 22FDX process compensates for manufacturing and temperature variations, so that the PEs reach 150 MHz reliably at only 0.5 V, while keeping leakage low (chip paper; Höppner et al. 2021).

![Power per operating state](figures/02_hardware_energy/02_power_states.png)

***Figure 8.** Why SpiNNaker2 adapts its performance level to the load. A: the power of the 152 PEs of one chip against the work they do per second, measured as CoreMark throughput, at the two performance levels. Each level combines a supply voltage with a clock frequency. At full load, the low level (150 MHz) does a little less than half the work of the high level (300 MHz), so its line ends in the middle. For the same work, the low level needs much less power: about 404 mW instead of about 870 mW. The cheapest strategy (green) is therefore to stay at the low level as long as it can keep up, and to switch to the high level only when more work is needed. Only the endpoints are measured (all PEs sleeping, all PEs running CoreMark); the dotted lines assume that power grows linearly with the work. Even the sleeping chip draws a considerable baseline, which energy measurements have to subtract (section 9). B: this strategy in practice, for an SNN that classifies DVS gestures (1000 timesteps): automatic switching needs 28 % less energy than running at the high level all the time. Running at the low level all the time needs the most energy, because at 150 MHz the processing doesn't fit into 1 ms, so this run used 3 ms per step and took three times as long. **Source:** Reported (Scholze et al. 2026, Tables 2 and 4): the power of all PEs switched off, sleeping and running CoreMark at 0.5 V / 150 MHz and 0.8 V / 300 MHz, and the CoreMark throughput; the DVS gesture energies per inference and the timestep of each run; the 28 % saving; that the automatic mode switches to the high level above a spike threshold. Computed or assumed here: that sleeping means no work, the linear interpolation between the measured endpoints (including the 870 mW at the low level's maximum work), and the cheapest path (green), which is a conclusion from these assumptions, not a description of how the automatic mode in the paper is implemented.*

In SNNs, the load changes with the spike rate. In the DVS gesture experiment of the paper, each PE switches to the high performance level only when it has received more spikes than a threshold, and otherwise stays at the low level. This saved 28 % energy compared with always running at the high level, while still processing in real time (Figure 8B).

Running at the low level all the time needed the most energy in this experiment, even though it needs the least power for a given amount of work (Figure 8A). The reason is time: at 150 MHz many PEs needed close to 2 ms per step, so the paper used a timestep of 3 ms at the low level. The same 1000 steps then took 3 s instead of 1 s, the run was no longer real time, and the baseline power of the chip had to be paid three times as long (Scholze et al. 2026, p. 10 and Table 4). Slower is therefore not always cheaper: the energy of a run is power × time, and below some voltage the leakage that accumulates over a longer run outweighs what each operation saves (the *minimum energy point*, Höppner et al. 2021).

py-spinnaker2 v0.8 has no setting for the performance level, and its neuron models never switch it (snn-core code), so these results can be reported in the workshop, not reproduced. Which level the chips run at during a py-spinnaker2 run is still to be checked.

**Workshop:** 2 min. Energy saving on this chip is not only "fewer spikes", but also "slow down when there is little to do", as long as the work still fits into each timestep.

## 7. Limits in practice: when a network doesn't fit

A network runs on the chip only if, on every PE, its data fits into the **memory** (about 68 KiB of network data for `lif`, section 3 and Figure 5) and its work fits into one **timestep** (section 2 and Figure 4). py-spinnaker2 splits every population into slices of at most `max_atoms_per_core` neurons, one slice per PE, and each PE holds only one population (py-spinnaker2 tutorials 04 and 05).

**Which budget is tight?** For the workshop networks, memory: the first MNIST layer needs 5 PEs (Figure 5). The time budget is generous in comparison. The chip paper reports up to 12 million synaptic events per second per PE at 300 MHz with 1024 neurons per PE (about 12,000 per 1 ms timestep, up to about 16 million with fewer neurons). An MNIST image with latency coding causes only about 15,000 synaptic events in total (116 input spikes × 128 targets), spread over 50 timesteps and 5 PEs (estimated here). Tutorial 05 of py-spinnaker2 gives a data point for the limit: 10,000 synaptic events per step on one PE missed the 1 ms deadline in 14 of 100 steps. On the HPI chips the same network missed none, in runs with v0.8.0 and v0.8.2 (tutorial 05 run on the cluster, profiling output); why is open ([To check on the cluster](#to-check-on-the-cluster)). The time budget matters for large, brain-like networks with thousands of synapses per neuron, or with very high activity.

**How to notice that a budget is exceeded:**

- **Memory:** py-spinnaker2 stops with `MemoryError: PE memory exceeded: … KiB needed, … KiB available` while it maps the network onto the PEs, before anything is sent to the board, and lists the memory regions by size. `hw.run(net, T, mapping_only=True)` performs this check without a board.
- **Time:** the run continues. The chip logs "Deadline missed in systick …", py-spinnaker2 prints "Some PEs returned some errors! Results may be corrupted!" after the run, and the profiling reports `deadline_flag` > 0. The work of the late step extends into the following ones, and spikes that arrive in the meantime can be counted in the wrong step (chip paper; py-spinnaker2 tutorial 05 and profiling).

**What helps:**

- **Fewer neurons per PE:** `pop.set_max_atoms_per_core(n)` lowers the number of neurons per PE for one population, at the cost of more PEs. `hw.run(..., iterative_mapping=True)` searches for a value that fits automatically (py-spinnaker2, simulation options; tutorial 05).
- **Recording less:** recording `v` costs 4 bytes per neuron and timestep in the PE's memory; for 26 neurons over 400 steps that is already 42 KiB, more than half of the budget (py-spinnaker2 mapping). Alternatives: only the final membrane potential (`record=["v_last"]`), or recording to DRAM with `record_on_dram=True` (py-spinnaker2, SNNs on SpiNNaker2).
- **A longer timestep:** `sys_tick_in_s` gives each PE more time per step, if real time isn't needed.

**Orders of magnitude.** The chip paper gives more than 150,000 neurons per chip at a 1 ms timestep, roughly 1000 neurons on each PE. In py-spinnaker2 that corresponds to the variants with 1024 neurons per PE (148 × 1024 = 151,552). Most models, including the default `lif`, hold at most 256 neurons per PE, limited by the 8-bit target index of their synapse format (primer, section 4), i.e. at most about 38,000 neurons per chip. Densely connected layers fit far fewer (26 per PE in Figure 5). A measured example from the cluster: in the synfire chain of tutorial 00 (`lif_curr_exp`, 60 inputs per neuron, `v` and spikes recorded), more than 100 neurons per PE exceed the PE memory. These numbers depend strongly on connectivity, weight precision, recording and activity, so they are orders of magnitude, not guarantees.

**Workshop:** 2 min in hands-on 1, as a troubleshooting guide when participants make a network larger.

## 8. Reported energy numbers

![Reported energy comparisons](figures/02_hardware_energy/03_reported_energy.png)

***Figure 9.** Two ways to compare SpiNNaker2 with other hardware, and why they give different answers. A: efficiency for dense INT8 DNN layers under ideal conditions. SpiNNaker2 at 150 MHz reaches 2.77 TOPS/W, about as much as edge accelerators such as the Jetson Orin Nano (2.68) or the Coral Edge TPU (2.00); the ARM Ethos N77 is almost twice as efficient. The SpiNNaker2 values were measured with all data in the PEs' SRAM and extrapolated to all 152 PEs, the others are datasheet or survey values. B: measured energy per inference against an Nvidia A100 GPU, and how many times longer SpiNNaker2 takes (right column). The ratio ranges from 0.24 to 21: SpiNNaker2 needs less energy for small layers and for an event-based language model at batch size 1 (the "18 ×"), but more for large matrix multiplications and at batch size 6. It is always slower, by 8.6 to 721 times. **Source:** Reported data: Scholze et al. 2026, Table 3 (A) and Table 5 (B, dense INT8 layers, SpiNNaker2 at 150 MHz including DRAM transfers, A100 with torchao), and Nazeer et al. 2024, Tables II and III (B, event-based GRU, energy per inference or per sample). Ratios computed here.*

<details>
<summary><b>Dense vs. sparse workloads:</b> what the two kinds of workloads in Figure 9 mean</summary>

<br>

- **Dense:** every weight takes part in every computation. In a fully connected or convolutional DNN layer, each output is the sum over *all* inputs multiplied by their weights, whether an input is large, small or zero. The hardware has to do all these multiply-accumulates, so there is no work to skip. GPUs and edge accelerators are built for exactly this. Any energy advantage of SpiNNaker2 here has to come from lower power, not from skipped work.
- **Sparse, event-based:** only a small fraction of the units is active at any moment, and work is only done for the active ones. In an SNN, a synapse is only processed when a spike arrives; in the event-based language model of Figure 9 (EGRU, an event-based variant of the GRU recurrent network), a unit only emits an output when its internal state crosses a threshold, like a spiking neuron. If only 10 % of the units are active, about 90 % of the work disappears. For example, only 116 of the 784 input neurons of an MNIST digit spike with latency coding (primer, Figure 19).

"Sparse" here means sparse *activity* (few events per timestep). It is different from sparse *connectivity* (few synapses per neuron), which reduces memory rather than work. The energy advantage of event-driven hardware comes mainly from sparse activity (primer, section 9 and Figure 26).

</details>

<br>

What the numbers say, and what they don't:

- **Dense DNN layers under ideal conditions** (Figure 9A): SpiNNaker2 is in the same range as dedicated edge accelerators (0.34–5.13 TOPS/W in the same table, most around 2–2.7), not ahead of them. These values assume that the data fit into the on-chip SRAM and that all PEs are busy, and the comparison values are datasheet numbers, not measurements.
- **Dense DNN layers, measured** (Figure 9B): including the DRAM transfers, SpiNNaker2 needs less energy than an A100 for small layers (up to 21 times less for a fully connected layer), but more for large matrix multiplications, where the limited DRAM bandwidth dominates (Scholze et al. 2026, Fig. 11). It is always much slower, by 9 to 721 times. The energy ratio comes from power, not from sparsity: SpiNNaker2 draws less than 1 W, the A100 more than 100 W, even when a small layer leaves most of it idle.
- **The "18 ×" claim:** SpiNNcloud (now Sparxity) advertises "18× higher energy efficiency than GPUs", without a source. The factor matches one benchmark, quoted in the chip paper: an event-based language model (EGRU) that needs 65 mJ per inference (token or sequence not stated) on SpiNNaker2 and 1.19 J on an A100, a factor of 18.3 (Nazeer et al. 2024). That the advertised number comes from this benchmark is *(assumption, to check)*. Two caveats from the source itself: the comparison is at batch size 1, and SpiNNaker2 took 170 ms against 19.9 ms on the A100, 8.6 times longer. The language model only fitted on one chip with batch size 1. For an EGRU on DVS gestures (only its two recurrent layers on the chip; the CNN front end ran beforehand and is not in the chip's energy), the same paper shows what batching does, with batch sizes 1 and 6 measured: at batch size 1 SpiNNaker2 needs 2.9 times less energy than the A100, at batch size 6 the A100 needs half as much as SpiNNaker2 (0.011 J vs 0.023 J per sample), because a GPU processes a larger batch in about the same time and SpiNNaker2 doesn't. The "18 ×" is a real measurement, but for single-sample inference where latency doesn't matter, not a general property of the chip.
- **SNN on the chip:** the DVS gesture network (5 layers, 7,859 neurons on 57 PEs, plus 64 PEs for the input spikes) reaches 92 % accuracy on 1 s clips (94.0 % in PyTorch on the full gestures) and needs 0.74–2.0 J per second of input, depending on the performance level (Figure 8B). The chip paper gives no GPU comparison for this workload. The DVS gesture paper (Arfa et al. 2025) runs the same network with a different set-up (600 steps of 3.5 ms) and reports 459 mJ per inference; in its comparison table, IBM's TrueNorth chip needs 18.8 mJ for the same task with a different network. Other neuromorphic chips can be much more efficient for a fixed task.
- **Energy per synaptic event:** the chip paper reports energy per inference or per layer, but no pJ per synaptic operation. The PE architecture paper measured it on a 22FDX test chip with 8 PEs: about 0.2 nJ per synaptic event and about 1.5 nJ per neuron update, both processed in software on the ARM core, with the baseline power of the chip dominating the total (Höppner et al. 2021, Tables I and III). That is about 200 times the energy of the 32-bit addition assumed in primer Figure 26, so that estimate can't be transferred to the chip (primer, section 9).

The general lesson is more nuanced than "sparser is better". Energy ratios depend as much on utilisation, batch size and baseline power as on the workload, and SpiNNaker2 trades speed for energy: its strength is low absolute power for small workloads processed one sample at a time, and for event-driven networks in which most PEs sleep most of the time. The chip paper expects sparse, event-based networks to profit most (Scholze et al. 2026, p. 13), but the measured comparisons above don't isolate sparsity. This is why the workshop should show an own measurement rather than a marketing number, and ask two questions of every "× more efficient": at which batch size, and how much slower?

**Workshop:** 5 min, the core of the motivation block, with the "18 ×" as an example of how to read such claims.

## 9. Measuring on the chip

py-spinnaker2 can measure the power of the board while a network runs ([power measurement](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/power_measurement.html)):

```python
hw.run(net, timesteps, record_power=True)                    # record power samples
hw.run(net, timesteps, record_power=True, live_power=True)   # additionally show them live
```

- **What is measured** depends on the board (SpiNNMan2 power measurement documentation, the host library that py-spinnaker2 uses):
  - **single-chip board:** the power of five supply rails of the chip, read from shunt resistors by the board's microcontroller: `PL05` and `PL08` (the 0.5 V and 0.8 V supplies of the PEs), `PLL`, `IO` and `Q`, plus their sum (`total`).
  - **48-node board:** one value per board, queried from the frame's backbone controller via SNMP. It is the power of the whole board, i.e. 48 chips with their DRAM, not of the chip that runs the network.
- **Sampling:** every 0.1 s on the single-chip board and every 0.2 s on the 48-node board, according to the py-spinnaker2 documentation. On the HPI boards the library reads a value every 0.1 s, but the value comes in whole watts and changes at most about once per second (measured, [`05_measurements/01_power_baseline/`](../05_measurements/01_power_baseline/README.md)).
- **Output:** `power.parquet` (time, channels, total, markers for phases such as the start and end of the simulation) and `power.png`, in `spinnaker2_diagnostics/volatile_diagnostics/`. The console prints energy, duration and average power, e.g. `Power measurement (sim_start -> sim_end): 30.782 J over 0.513 s, average 60.000 W` (example from the documentation).
- **Limitation:** runs shorter than the sampling interval produce one or no sample. Runs should last several sampling intervals, i.e. at least a few seconds, which means thousands of timesteps at a timestep of 1 ms.

**Consequence for the HPI boards.** The HPI boards are 48-node boards (section 5), so a run reports the power of the whole board. Measured on 2026-10-19 ([`05_measurements/01_power_baseline/`](../05_measurements/01_power_baseline/README.md)): an empty board draws a steady **57 W**, read in 1 W steps. Up to 100 cores in which every neuron spikes every step (1 billion synaptic events per second) the reading doesn't move. Loaded cores without spikes add 3 W, whether 1,000 or 3,000 of them; with spikes, 1,000 cores add 9 W and the full board (7,000 cores) about 29 W. A workshop network on a handful of PEs is therefore invisible, while a large demo network shows the cost of spiking clearly. The increase is not proportional to the load, although every core does the same work at all sizes (checked with spike recording and profiling). Divided by the synaptic events per second, the spike-related power gives roughly 0.3–0.6 nJ per synaptic event including neuron updates, the same order of magnitude as the test chip's 0.20–0.26 nJ per synaptic event (Höppner et al. 2021) (estimated here from the 1 W readings).

The **profiling** of py-spinnaker2 complements this with timing ([profiling](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/profiling.html)): with `profile=True` on a population, each PE records per timestep how long its work took (`duration_us`) and how many timer periods it overran (`deadline_flag` > 0), in `profiling.parquet`. The file is only written when the persistency level of the diagnostic folder is `volatile` or `persistent`.

<details>
<summary><b>A measurement plan for the workshop:</b> how to get a meaningful energy number</summary>

<br>

A single power reading says little, because the board draws power even when nothing happens (Figure 8), and on a 48-node board this baseline belongs to 48 chips. A meaningful comparison needs:

1. **Baseline:** the power of the board while idle or running an empty network, to subtract, and its fluctuation between samples and runs.
2. **Long enough runs:** several seconds per measurement (thousands of timesteps), because of the 0.1–0.2 s sampling interval.
3. **A large enough difference:** a network spread over many PEs with high activity, so that its energy stands out from the baseline. Repeat each measurement several times.
4. **The same network at different activity levels:** e.g. the MNIST network with latency coding and with rate coding, or a network driven by Poisson inputs of different rates. If the energy above the baseline grows with the number of spikes, this shows the event-driven principle directly.
5. **Energy per inference:** (energy above baseline) / (number of inputs processed), so that numbers can be compared with other hardware.

A GPU comparison is optional and needs care: the same model, the same accuracy, the same batch size, and the energy of the GPU measured the same way (e.g. with `nvidia-smi`), including idle power (section 8).

</details>

<br>

**Workshop:** hands-on 2, where participants measure the energy of their own run.

## To check on the cluster

Answered from the sources and the py-spinnaker2 code on 2026-09-30, no longer on this list: DRAM per chip (section 3), board sharing (per board, section 5), neurons per PE and how populations are split (section 7), accelerators per PE (section 2), bytes per synapse (section 3), the timestep length (`sys_tick_in_s`, default 1 ms), what happens when a budget is exceeded (section 7), how incoming spikes are processed (Figure 3), and the low performance level's energy (section 6). Answered on the cluster on 2026-10-01: the boards are 48-node boards (section 5).

- [ ] Power measurement, follow-ups of the baseline measurement of 2026-10-19 (section 9, open points in [`05_measurements/01_power_baseline/`](../05_measurements/01_power_baseline/README.md)): find out what the controller's value covers (fans?) and why the increase is not proportional to the load, and compare the baseline of the other boards.
- [ ] How many of the 6 boards workshop accounts can use.
- [ ] Which performance level the chips run at during a py-spinnaker2 run (v0.8 has no setting for it, section 6). A hint: tutorial 05's deadline network (10,000 synaptic events per step on one PE) missed no deadline on the HPI chips, where the vendor's version of the tutorial reports 14 of 100 (section 7). Repeat the run a few times and with more load to find where misses start.
- [ ] Whether multicast routing (`set_routing_type("MC")`) works on the HPI boards, if the workshop shows it (section 4).
- [ ] Whether spikes between chips of one board work with py-spinnaker2 v0.8.2 (C2C and MC): a small network with projections across chips, a few chip runs (section 5).
- [ ] Where the vendor's "18×" comes from: the EGRU benchmark of Nazeer et al. 2024 or another one (ask the vendor), section 8.
