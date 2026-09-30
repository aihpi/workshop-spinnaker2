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
- [7. Limits in practice: when a network doesn't fit](#7-limits-in-practice-when-a-network-doesnt-fit)
- [8. Reported energy numbers](#8-reported-energy-numbers)
- [9. Measuring on the chip](#9-measuring-on-the-chip)
- [To check on the cluster](#to-check-on-the-cluster)

## 1. The chip at a glance

SpiNNaker2 is a many-core chip: instead of a few powerful processors it has 152 small, independent ones, each with its own memory, connected by a network that is optimised for sending many small messages (spikes). The name comes from *Spiking Neural Network Architecture*. It was developed at TU Dresden with the University of Manchester, the successor of SpiNNaker1 (Manchester, 2011), and is produced by [SpiNNcloud Systems](https://spinncloud.com).

Physically, the chips sit on boards, and the boards in a frame in a server rack of the computing centre. Figure 1 follows this hierarchy down to a single chip, with the numbers of the HPI installation (section 5):

![From the rack to the chip](figures/02_hardware_energy/01_installation_hierarchy.png)

***Figure 1.** Where the chips physically are, and how data from py-spinnaker2 reaches them (purple). A: the SpiNNaker2 frame is mounted in a server rack of the computing centre. py-spinnaker2 runs on a cluster node, which talks to the frame via Ethernet. B: the frame, seen from the front, holds 6 boards side by side, each with its own Ethernet connection, and a management controller that switches the boards on and boots them. A run reserves one board (red). C: that board, seen from above: 48 chips (probably, as a 48-node board), each with its own DRAM (red), which consists of separate memory chips next to it on the board. The chips are connected to their neighbours by links on the board (green). Each chip has 6 links: on the square grid of the drawing, these are the 4 horizontal and vertical neighbours plus one diagonal direction, which together form the hexagonal grid of the chip paper. Data from the host enters at a chip and travels over these links to the chips that need it. D: one of these chips, about 1 cm × 1 cm, with its 152 processing elements and their local SRAM (orange), shown in detail in Figure 2. The DRAM itself is outside the chip; on the chip sits only its interface (red, at the edge). Colours as in Figure 2: orange for on-chip SRAM, red for off-chip DRAM and its interface. For users, the relevant size is one board, 7,296 PEs per run. **Source:** Diagram. Numbers from the HPI installation (boot log and vendor, see section 5) and the chip paper (die size 102 mm²). The number of chips per board, the arrangement of chips and links on the board, the position of the cluster node and the entry point of Ethernet traffic on the board are not confirmed yet, the layout is schematic.*

![Schematic of the SpiNNaker2 chip](figures/02_hardware_energy/01_chip_schematic.png)

***Figure 2.** A SpiNNaker2 chip at three levels of zoom. A: the chip with its 38 quad processing elements (QPEs), each with 4 processing elements (PEs), every PE drawn as its core (blue) on top of its local memory (orange). Shared by all PEs: the router in the middle, the links to neighbouring chips, the DRAM interface and Ethernet. The red arrows show the path of one spike: the PE of the firing neuron sends one packet, the router looks up the packet's key and sends copies to every PE and to every neighbouring chip that has neurons listening to this sender (section 4). B: one QPE, whose 4 PEs share one connection to the network-on-chip. C: what one PE contains. **Source:** Diagram drawn here from the component list in Scholze et al. 2026 and py-spinnaker2 tutorial 06. The arrangement of the blocks and the spike path are schematic, not the physical floorplan.*

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

![How the parts of a PE work together](figures/02_hardware_energy/02_pe_function.png)

***Figure 3.** How the parts of a PE work together in one timestep, with the same colours as Figure 4: processing incoming spikes in orange, updating neurons in blue. ① The timer wakes the core. ② Spike packets that arrived from other PEs are read from the network-on-chip interface. ③ For each spike, the core reads from the synapse tables in its SRAM which of its neurons are targets, and with which weights. ④ It adds the weights to these neurons and updates the states of all its neurons, also in SRAM. ⑤ Neurons that crossed their threshold send a spike packet into the network. The strip at the bottom shows where these steps fall within the timestep: after the work, the PE sleeps until the next timer tick. Everything the core needs sits in its own SRAM, so none of the steps has to wait for DRAM. The accelerators and the DMA engine (dashed) are only used by some models or for recording to DRAM. **Source:** Schematic of the principle, not the physical layout. From the sources: the parts of the PE (chip paper, py-spinnaker2 tutorial 06), the SRAM regions (py-spinnaker2 memory structure) and the timer-driven timesteps (py-spinnaker2 profiling). Assumed here, not confirmed for py-spinnaker2: the order of the steps and their timing, taken from how SNN simulators generally work and from SpiNNaker1, and that the PE sleeps after its work. In particular, incoming spikes may be processed as they arrive, spread over the timestep and triggered by interrupts as on SpiNNaker1, rather than in one block at the start as drawn in the strip. Which models use which accelerator is not known.*

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

![How a PE spends its timesteps](figures/02_hardware_energy/02_pe_timestep.png)

***Figure 4.** What a PE does over ten timesteps, here of 1 ms each, a common choice (the length of a timestep is configurable). A timer interrupt starts every step. The PE first processes the spikes that arrived (orange), then updates its neurons and sends their spikes (blue), and sleeps for the rest of the step (grey). The more spikes arrive, the longer the orange part. In a sparse network, the PE sleeps most of the time, which is where the energy saving of event-driven hardware comes from (section 6). If too many spikes arrive in one step (step 6), the work doesn't fit into the step and the next step starts late, a violated real-time deadline (section 7). **Source:** Illustration, spike counts and durations made up. From the sources: timer-driven timesteps and the measurement of the work per timestep and of deadline misses, where work that overruns extends into the following timesteps (py-spinnaker2 profiling). Assumed here: that the work per timestep grows with the number of incoming spikes, the split into spike processing and neuron update, and sleeping for the rest of the step. Not measured on the chip.*

**Is a PE a neuron?** No. Each PE simulates many neurons, hundreds to about a thousand, in software. A closer analogy: a PE corresponds to a small local population of neurons, the router and links play the role of the long-range axons, and synapses are not hardware at all but entries in weight tables in the SRAM.

**Workshop:** 1 min. The ARM core and SRAM matter for the hands-on parts; the accelerators only as an outlook.

## 3. Memory

| Level | Where | Size | Used for |
|---|---|---|---|
| PE-local SRAM | inside each PE | 128 KB | neuron states, parameters, synapses, recordings |
| DRAM (LPDDR4) | outside the chip, shared | 2 GB on the py-spinnaker2 boards (two 1 GB banks) | large data, recordings with `record_on_dram=True` |

Keeping weights in the local SRAM of each PE is central to the energy argument: reading from on-chip SRAM costs about 100 times less energy than reading from external DRAM (primer, Figure 25). Each PE on its own is a small conventional computer, but there is no shared memory or bus for all PEs, so the system as a whole avoids the von Neumann bottleneck of conventional computers (`00_computing_fundamentals.md`, section 2). The price is capacity: 96 KB of data per PE is small, and memory, not compute, is usually what limits how many neurons and synapses fit on a PE (section 7).

The chip paper specifies up to 4 GB per LPDDR4 interface, while tutorial 06 lists 2 GB for the boards used with py-spinnaker2. The likely explanation is the difference between what the chip supports and what is installed on a board, but this is not confirmed (see the list at the end).

Figure 5 makes this concrete with two example networks from the primer. The first is the **MNIST network** of primer sections 6 and 8 (Figures 19 and 24), which classifies handwritten digits: 784 input neurons (one per pixel of a 28 × 28 image), 128 hidden neurons and 10 output neurons (one per digit). Its *layer 1* is the set of connections from the inputs to the hidden neurons: with every input connected to every hidden neuron, that is 784 × 128 = 100,352 synapses. Its *layer 2* connects the hidden neurons to the outputs, 128 × 10 = 1,280 synapses. The second is the **clustered network** of primer section 7 (Figure 21), with 250 neurons and about 12,000 synapses.

![Memory of a PE and the trade-off between SRAM and DRAM](figures/02_hardware_energy/03_memory.png)

***Figure 5.** Why SpiNNaker2 keeps the data local, and what that costs. A: reading all weights of the first MNIST layer (primer Figure 24) once takes about 0.5 µJ from the local SRAM, but about 65 µJ from the DRAM next to the chip, 130 times more. Synapses are read whenever a spike arrives, so over many timesteps this difference adds up. B: the price is capacity. Each box is the data memory of one PE (about 92 KB after heap and stack). The first MNIST layer, with about 100,000 synapses, fills 5 PEs at 4 bytes per synapse, and still 2 PEs at 1 byte per synapse (dashed line). The clustered network (about 12,000 synapses) and the second MNIST layer each fit into one PE. Larger networks therefore have to be split across several PEs; how py-spinnaker2 does this is still to be checked (section 7). **Source:** Estimate computed here. Synapse counts from the example networks (for the clustered network, the expected number from its connection probabilities). The memory per synapse is assumed (1 to 4 bytes, 4 bytes in A), as the synapse format of py-spinnaker2 is not confirmed yet. Energy per 64-bit read from Horowitz 2014 (45 nm, 8 KB SRAM and DRAM), as an order of magnitude, not measured on SpiNNaker2. Memory sizes from the py-spinnaker2 documentation (memory structure, tutorial 06). Routing tables and recordings, which also need memory, are ignored.*

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

![Multicast routing](figures/02_hardware_energy/04_multicast.png)

***Figure 6.** How one spike reaches many neurons. A: when a neuron fires, its PE sends a single packet with the neuron's key. The router looks up the key in its table and sends one copy to every PE and link that has target neurons for this sender, here 3 PEs and one link to a neighbouring chip. Inside each target PE, the packet is handed to its own target neurons through the synapse table (step ③ in Figure 3), without any further packets. In total, this spike costs 1 packet plus 4 copies, however many target neurons the 3 PEs hold (red box). The neighbouring chip may copy the packet further to its own PEs. B: the same count for two examples. A spike of an MNIST input neuron has 128 targets in the hidden layer. If layer 1 is split across 5 PEs as in Figure 5, multicast needs 1 packet plus 5 copies instead of 128 packets, about 21 times fewer. For a cortex-like neuron with 1,000 targets on 10 PEs, it is about 91 times fewer. Fewer packets mean less traffic in the network-on-chip and less energy per spike. **Source:** Diagram and computed illustration. Keys, table entries and the distribution of target neurons across PEs are made up or assumed; the principle follows the chip paper (multicast packets with 32-bit keys, routing table with 16 K entries).*

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

![Scale of SpiNNaker2 systems](figures/02_hardware_energy/05_scale.png)

***Figure 7.** A: the number of processing elements, from one chip to the largest systems. One run on the HPI installation uses one 48-node board, 7,296 PEs. B: how many neurons that corresponds to, at about 150,000 neurons per chip, compared with the brains of a mouse and a human. Even the Dresden system reaches only a few percent of the neurons of a human brain, and far fewer of its synapses. **Source:** PE and chip counts reported (chip paper, py-spinnaker2 tutorial 06, section 5 for the HPI installation, whose board type is not confirmed). Neuron capacities estimated here from the paper's figure of about 150,000 neurons per chip (with a 1 ms timestep), which depends strongly on connectivity. Brain sizes: common estimates of about 70 million (mouse) and 86 billion (human) neurons.*

**The HPI setup** (as of end of September 2026, from the vendor and from the boot log of a run):

- **6 boards in one frame.** The board management controller of the frame reports 6 boards, and the vendor refers to the installation as a 6-board system.
- **Probably 48-node boards**, i.e. up to 6 × 48 = 288 chips in total. The boot log lists 49 devices on the management bus of a board (48 chips plus a controller), but the board type isn't confirmed yet.
- **One board per run, for now.** Multi-board simulations aren't supported yet and are expected in a few months, so the board-to-board cables aren't needed yet. A single 48-node board is far larger than any network planned for the workshop.
- **Boards are locked per user.** When a run starts, the session software (SpiNNMan2, used by py-spinnaker2) reserves a board with a lock file ("The board is locked for you"). If one board can only be used by one user at a time, at most 6 people can run on the chips simultaneously.

<details>
<summary><b>Reading the boot log:</b> what happens when a run starts</summary>

<br>

The start of a run on the cluster shows the boot sequence of a board:

- the machine configuration is read, and the frame's management controller (an STM32 microcontroller) finds the boards on its management bus
- a board is locked for the user
- the board is power-cycled and the chips are switched on: core clock, adaptive body biasing (`turn on ABB`, which may need a second attempt before it reports `locked`), the LPDDR4 DRAM interfaces, clock distribution, the network-on-chip router, and Ethernet
- `qgrid_adpll with default clk 1200.00 MHz` is the frequency of a clock generator (PLL). The clock of the PEs (150 or 300 MHz) is derived from it by dividing it down, so 1200 MHz is not the PE clock.
- a small operating program (SCAMP) is loaded onto the chips, and the kernel status of each chip is checked

</details>

<br>

**Workshop:** 1 min, the scale as a motivation: the same chips scale from a desk to a supercomputer.

## 6. Power management

The chip adapts its power to the load with **dynamic voltage and frequency scaling (DVFS)**: each PE runs at one of four *performance levels*, combinations of two supply voltages and clock frequencies, e.g. 0.5 V with 150 MHz or 0.8 V with 300 MHz. The dynamic power of a digital circuit grows roughly with frequency × voltage², so the low level needs much less power per clock cycle. PEs that have nothing to do can sleep or be switched off entirely (power shut-off), and **adaptive body biasing** of the 22FDX process reduces leakage at low voltage.

![Power per operating state](figures/02_hardware_energy/02_power_states.png)

***Figure 8.** Why SpiNNaker2 adapts its performance level to the load. A: the power of the 152 PEs of one chip against the work they do per second, at the two performance levels. Each level combines a supply voltage with a clock frequency. At full load, the low level (150 MHz) does only half as much work as the high level (300 MHz), so its line ends in the middle. For the same work, the low level needs much less power: at half the maximum work, about 404 mW instead of about 885 mW. The cheapest strategy (green) is therefore to stay at the low level as long as it can keep up, and to switch to the high level only when more work is needed. Only the endpoints are measured (all PEs sleeping, all PEs at full load); the dotted lines assume that power grows linearly with the work. Even the sleeping chip draws a considerable baseline, which energy measurements have to subtract (section 9). B: this strategy in practice, for an SNN that classifies DVS gestures (1 s of input): automatic switching needs 28 % less energy than running at the high level all the time. That running at the low level all the time needs the most energy is reported, but not explained in the sources read so far (see section 6 and the list at the end). **Source:** Reported (Scholze et al. 2026, extracted from the paper text): the power of all PEs switched off, sleeping and at full load (CoreMark benchmark) at 0.5 V / 150 MHz and 0.8 V / 300 MHz; the DVS gesture energies per inference; the 28 % saving; that the automatic mode switches to the high level above a spike threshold. Computed or assumed here: the work axis (work per second assumed proportional to the clock frequency, since no benchmark scores are given), that sleeping means no work, the linear interpolation between the measured endpoints (including the 885 mW at half the maximum work), and the cheapest path (green), which is a conclusion from these assumptions, not a description of how the automatic mode in the paper is implemented.*

In SNNs, the load changes with the spike rate. In the DVS gesture experiment of the paper, each PE switches to the high performance level only when it has received more spikes than a threshold, and otherwise stays at the low level. This saved 28 % energy compared with always running at the high level, while still processing in real time (Figure 8B). Running at the low level all the time needed the most energy in this experiment, even though it needs the least power for a given amount of work (Figure 8A). The sources read so far don't explain this. One possible reason, not confirmed, is that at 150 MHz the chip can't keep up with the input in real time, so the run takes longer overall.

**Workshop:** 2 min. Energy saving on this chip is not only "fewer spikes", but also "slow down when there is little to do".

## 7. Limits in practice: when a network doesn't fit

A network runs on the chip only if, on every PE, its data fits into the **memory** (about 92 KB after heap and stack, section 3 and Figure 5) and its work fits into one **timestep** (section 2 and Figure 4). If either budget is exceeded, the network has to be spread over more PEs. Claims marked *(assumption, to check)* are not confirmed by the sources read so far and are listed at the end.

**Which budget is tight?** For the workshop networks, memory: the first MNIST layer already needs several PEs (Figure 5). The time budget is generous in comparison. The chip paper reports up to 12 million synaptic events per second per PE (about 12,000 per 1 ms timestep), while an MNIST image with latency coding causes only about 15,000 synaptic events in total, spread over 50 timesteps and several PEs (my estimate). The time budget matters for large, brain-like networks with thousands of synapses per neuron.

**How to notice that a budget is exceeded:**

- **Time:** the profiling reports a deadline miss (`deadline_flag` > 0), and the work extends into the following timesteps (py-spinnaker2, profiling). Whether py-spinnaker2 also warns or stops the run is *(assumption, to check)*.
- **Memory:** presumably py-spinnaker2 fails with an error when it maps the network onto the PEs, before the run starts *(assumption, to check)*.

**What helps:**

- **Fewer neurons per PE:** less data and less work per PE, at the cost of more PEs. Whether and how the number of neurons per PE can be set is *(assumption, to check)* (tutorial 04, advanced topic "hardware allocation").
- **Recording less:** only the final membrane potential (`record=["v_last"]`) instead of every timestep, or recording to DRAM with `record_on_dram=True` (py-spinnaker2, SNNs on SpiNNaker2).

**Orders of magnitude.** The chip paper gives more than 150,000 neurons per chip at a 1 ms timestep, roughly 1000 neurons on each of the 152 PEs (my calculation). The `*_1024` variants of the neuron models are documented for 1024 neurons per PE (py-spinnaker2, neuron models); the default for the other models is *(assumption, to check)*. These numbers depend strongly on connectivity, weight precision, recording and activity, so they are orders of magnitude, not guarantees.

**Workshop:** 2 min in hands-on 1, as a troubleshooting guide when participants make a network larger.

## 8. Reported energy numbers

![Reported energy comparisons](figures/02_hardware_energy/03_reported_energy.png)

***Figure 9.** How many times less energy SpiNNaker2 needs than other hardware, for the workloads the chip paper compares (dashed line: same energy). For dense DNN layers (matrix operations), SpiNNaker2 at 150 MHz (2.77 TOPS/W) is about as efficient as an Nvidia Jetson Orin Nano (1.0 ×) and 1.4 times as efficient as a Google Coral Edge TPU. For an event-based language model (EGRU), which only computes when its units are active, SpiNNaker2 needs 65 mJ per inference and an Nvidia A100 GPU 1.19 J, 18 times more. The workloads, the comparison devices and the measurement set-ups differ, so the bars only show the trend: the sparser the computation, the larger the advantage. **Source:** Reported data, Scholze et al. 2026, extracted from the paper text. Ratios computed here from the reported TOPS/W and energies.*

<details>
<summary><b>Dense vs. sparse workloads:</b> what the two groups in Figure 9 mean</summary>

<br>

- **Dense:** every weight takes part in every computation. In a fully connected or convolutional DNN layer, each output is the sum over *all* inputs multiplied by their weights, whether an input is large, small or zero. The hardware has to do all these multiply-accumulates, so there is no work to skip. GPUs and edge accelerators are built for exactly this, and a neuromorphic chip has no inherent advantage.
- **Sparse, event-based:** only a small fraction of the units is active at any moment, and work is only done for the active ones. In an SNN, a synapse is only processed when a spike arrives; in the event-based language model of Figure 9 (EGRU, an event-based variant of the GRU recurrent network), a unit only sends an update when its state has changed enough. If only 10 % of the units are active, about 90 % of the work disappears. For example, only 116 of the 784 input neurons of an MNIST digit spike with latency coding (primer, Figure 19).

"Sparse" here means sparse *activity* (few events per timestep). It is different from sparse *connectivity* (few synapses per neuron), which reduces memory rather than work. The energy advantage of event-driven hardware comes mainly from sparse activity (primer, section 9 and Figure 26).

</details>

<br>

What the numbers say, and what they don't:

- **Dense DNNs:** SpiNNaker2 is in the same range as dedicated edge accelerators (about 2–2.8 TOPS/W), not far ahead of them. For dense workloads there is no neuromorphic advantage, because every operation has to be computed anyway. The paper also notes that the limited DRAM bandwidth reduces practical utilisation.
- **The "18 ×" claim:** SpiNNcloud advertises "18× higher energy efficiency than GPUs". The chip paper reports exactly this factor for one workload: an event-based language model that needs 65 mJ per inference on SpiNNaker2 and 1.19 J on an A100, a factor of 18.3. The advertised number therefore appears to come from this benchmark. It is a real measurement, but for one sparse, event-driven model, not a general property of the chip.
- **SNN on the chip:** the DVS gesture network (5 layers, 7,859 neurons on 57 PEs, 92 % accuracy) needs 0.74–2.0 J per second of input, depending on the performance level (Figure 8B). The paper gives no GPU comparison for this workload.
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
- **Limitation:** runs shorter than the sampling interval produce one or no sample. Runs should last several sampling intervals, i.e. at least a few seconds, which means thousands of timesteps at a timestep of 1 ms.

The **profiling** of py-spinnaker2 complements this with timing ([profiling](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/profiling.html)): with `profile=True` on a population, each PE records per timestep how long its work took (`duration_us`) and whether it missed the deadline (`deadline_flag` > 0), in `profiling.parquet`.

<details>
<summary><b>A measurement plan for the workshop:</b> how to get a meaningful energy number</summary>

<br>

A single power reading says little, because the board draws power even when nothing happens (Figure 8). A meaningful comparison needs:

1. **Baseline:** the power of the board while idle or running an empty network, to subtract.
2. **Long enough runs:** several seconds per measurement (thousands of timesteps), because of the 0.1–0.2 s sampling interval.
3. **The same network at different activity levels:** e.g. the MNIST network with latency coding and with rate coding, or a network driven by Poisson inputs of different rates. If the energy above the baseline grows with the number of spikes, this shows the event-driven principle directly, and it checks the estimate in primer Figure 26.
4. **Energy per inference:** (energy above baseline) / (number of inputs processed), so that numbers can be compared with other hardware.

A GPU comparison is optional and needs care: the same model, the same accuracy, and the energy of the GPU measured the same way (e.g. with `nvidia-smi`), including idle power.

</details>

<br>

**Workshop:** hands-on 2, where participants measure the energy of their own run.

## To check on the cluster

- [ ] **Once the cluster is available:** check how much DRAM each chip of the HPI boards has (2 GB as in tutorial 06, or up to 2 × 4 GB as the chip supports), e.g. from the board information or by allocating DRAM in a test run.
- [ ] Confirm that the 6 boards of the HPI setup are 48-node boards, and whether one board can be shared by several users at the same time (e.g. on different chips). This decides how many participants can run on the chips in parallel.
- [ ] How the Ethernet port of a board is connected to its chips: only to one chip (as on SpiNNaker1 boards), to several, or to all (every SpiNNaker2 chip has its own Ethernet interface). Figure 1C assumes a single entry chip. Ask the admins or the vendor.
- [ ] Power measurement on the HPI setup: which channels are reported, the idle baseline, and the energy of a simple network at different spike rates (measurement plan in section 9).
- [ ] Default number of neurons per PE for each neuron model, and how py-spinnaker2 splits populations.
- [ ] Whether the chip runs at a fixed performance level in py-spinnaker2 or switches automatically, and whether this can be set.
- [ ] Verify the numbers taken from the chip paper against its tables (extracted from the text with a summarisation tool).
- [ ] Whether the accelerators (MLA, exp/log unit, random number generators) belong to each PE or are shared by the 4 PEs of a QPE. The chip paper lists them per PE; an earlier note claimed they are shared per QPE.
- [ ] **Once the cluster is available:** how many bytes py-spinnaker2 uses per synapse (weight, target, delay), e.g. with its memory visualisation tool. Figure 5A assumes 1 to 4 bytes.
- [ ] **Once the cluster is available:** where the length of a timestep is set in py-spinnaker2 and what its default is (the chip paper uses 1 ms), section 7. Also on the primer's list.
- [ ] What happens when a network exceeds the memory budget of a PE (error during mapping?) or the time budget (only `deadline_flag`, or also a warning or abort?), section 7.
- [ ] Whether and how the number of neurons per PE can be set by the user (tutorial 04, advanced topic "hardware allocation"), section 7.
- [ ] How py-spinnaker2 processes an incoming spike in detail: interrupt or polling, whether DMA is involved, how the synapse tables are laid out (Figure 3 shows only the principle).
- [ ] Whether Höppner et al. 2021 (PE architecture paper) contains a layout image or chip photo of a PE, and link it from section 2.
- [ ] Why the low performance level needs more energy than the high level in the DVS gesture experiment (Figure 8B), according to the paper.
