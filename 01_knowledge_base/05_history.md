# History of Neuromorphic Computing

Where neuromorphic computing comes from, which large programmes shaped it, and where SpiNNaker fits in. Material for the introduction of the motivation block and for answering questions such as "is SpiNNaker for brain research or for AI?" and "how is it different from Loihi?". Builds on `00_computing_fundamentals.md` (von Neumann bottleneck), `02_hardware_energy.md` (the SpiNNaker2 chip and its energy numbers) and `04_applications.md` (what the chips are used for today); details covered there are linked, not repeated.

Status 2026-11-05. Every fact names its source in brackets; the sources are listed at the end, with peer-reviewed papers, encyclopaedia entries and vendor or press material kept apart. Claims that no fetched source confirmed are marked *(assumption, to check)* and listed under [To check](#to-check).

## Contents

- [1. Summary and timeline](#1-summary-and-timeline)
- [2. Roots: why brain-inspired hardware](#2-roots-why-brain-inspired-hardware)
- [3. The big programmes](#3-the-big-programmes)
  - [3.1 United States: SyNAPSE and TrueNorth](#31-united-states-synapse-and-truenorth)
  - [3.2 Europe: FACETS, BrainScaleS and the Human Brain Project](#32-europe-facets-brainscales-and-the-human-brain-project)
  - [3.3 Intel: Loihi and Hala Point](#33-intel-loihi-and-hala-point)
  - [3.4 Others](#34-others)
- [4. SpiNNaker from brain simulator to AI hardware](#4-spinnaker-from-brain-simulator-to-ai-hardware)
  - [4.1 SpiNNaker1 in Manchester](#41-spinnaker1-in-manchester)
  - [4.2 SpiNNaker2 in Dresden](#42-spinnaker2-in-dresden)
  - [4.3 From SpiNNcloud to Sparxity](#43-from-spinncloud-to-sparxity)
- [5. A map of the approaches](#5-a-map-of-the-approaches)
- [6. Between three communities](#6-between-three-communities)
- [7. Likely questions and answers](#7-likely-questions-and-answers)
- [To check](#to-check)
- [Sources](#sources)

## 1. Summary and timeline

- **Neuromorphic computing started in analog circuit design, not in AI.** [Carver Mead](https://en.wikipedia.org/wiki/Carver_Mead) and his students at Caltech built silicon models of the retina and the cochlea in the late 1980s and named the field in 1990 (Mead 1990; Carver Mead, Wikipedia).
- **The large programmes of 2008–2023 had two goals that often got mixed up:** understanding the brain by simulating it (the EU's [Human Brain Project](https://en.wikipedia.org/wiki/Human_Brain_Project), with SpiNNaker and BrainScaleS) and building low-power computers for AI-like tasks (DARPA's [SyNAPSE](https://en.wikipedia.org/wiki/SyNAPSE) with IBM's TrueNorth, Intel's Loihi).
- **SpiNNaker is the digital, programmable, real-time branch.** Instead of copying neurons in analog circuits, it runs neuron models as software on many small ARM cores and sends spikes as tiny network packets (Knight & Furber 2016).
- **Its positioning moved from brain simulation to AI.** SpiNNaker1 was built to simulate up to 1 % of the human brain in real time (Manchester 2018); SpiNNaker2 was planned for "brain simulation and machine learning" (Mayr et al. 2019), and its vendor, renamed Sparxity in October 2026, now sells it as "sparse-native" hardware for AI inference (Silicon Saxony 2026).

| Year | Event | Source |
|---|---|---|
| 1977 | John Backus names the "von Neumann bottleneck" in his Turing Award lecture | Von Neumann architecture, Wikipedia |
| 1988 | Lyon and Mead describe an analog silicon cochlea | Carver Mead, Wikipedia |
| 1989 | Mead, *Analog VLSI and Neural Systems* (book) | Carver Mead, Wikipedia |
| late 1980s–1991 | Misha Mahowald's silicon retina; "The Silicon Retina" in *Scientific American* (1991) | Carver Mead, Wikipedia; Misha Mahowald, Wikipedia |
| 1990 | Mead, "Neuromorphic electronic systems", *Proceedings of the IEEE* | Mead 1990 |
| 1990 | Steve Furber leaves Acorn (BBC Micro, ARM) for the University of Manchester | Steve Furber, Wikipedia |
| 1992–1995 | Patent on asynchronous spike communication between chips (Mahowald, Sivilotti); the basis of address-event representation (AER) | Misha Mahowald, Wikipedia |
| 1995 | Institute of Neuroinformatics (INI) founded in Zurich, with Mahowald among the founders | Misha Mahowald, Wikipedia |
| 2004 | NEST simulator first released; BrainChip founded | NEST, Wikipedia; BrainChip, Wikipedia |
| 2006 | Construction of SpiNNaker starts in Manchester; EU project FACETS starts in Heidelberg (until 2010) | Manchester 2018; KIP Heidelberg |
| 2008 | DARPA funds SyNAPSE (IBM, HRL) | SyNAPSE, Wikipedia |
| 2009 | Neurogrid (Stanford) first operational | Neurogrid, Wikipedia |
| 2011 | EU project BrainScaleS (until 2015) | KIP Heidelberg |
| 2013 | Human Brain Project starts (1 Oct 2013, until 30 Sep 2023) | Human Brain Project, Wikipedia |
| 2014 | IBM TrueNorth: 1 million neurons on one chip | Merolla et al. 2014 |
| 2017 | Intel announces Loihi; SynSense (then aiCTX) spun out of INI Zurich | Intel Loihi, Wikipedia; eeNews Europe 2020 |
| 2018 | Million-core SpiNNaker machine switched on in Manchester (2 Nov) | Manchester 2018 |
| 2019 | SpiNNaker2 roadmap; HBP grants TU Dresden €8 million for SpiNNaker2; Tianjic hybrid chip in *Nature* | Mayr et al. 2019; SpiNNaker, Wikipedia; Pei et al. 2019 |
| 2021 | SpiNNaker2 tapeout (July); SpiNNcloud Systems GmbH active from summer; Loihi 2 (September); Akida development kits (October) | Design & Reuse 2021; SPRIND; Intel Loihi, Wikipedia; BrainChip, Wikipedia |
| 2023 | IBM NorthPole (not spiking); Human Brain Project ends, EBRAINS continues | Modha et al. 2023; Human Brain Project, Wikipedia |
| 2024 | Intel Hala Point (1.15 billion neurons) at Sandia; SpiNNcloud offers SpiNNaker2 systems commercially (May) | Intel 2024; The Register 2024 |
| 2025 | SpiNNaker2 system with 35,000 chips in operation at TU Dresden (April) | TU Dresden 2025 |
| 2026 | Intel archives its Loihi framework Lava (May); SpiNNcloud renamed Sparxity (28 Oct); HPI workshop (18 Nov) | `04_applications.md`; Silicon Saxony 2026 |

**Workshop:** 1 min, the timeline as one slide with four or five rows (1990 Mead, 2014 TrueNorth, 2018 million-core SpiNNaker, 2024 Hala Point, 2026 Sparxity).

## 2. Roots: why brain-inspired hardware

**Two problems of conventional computers.** In a [von Neumann computer](https://en.wikipedia.org/wiki/Von_Neumann_architecture), processor and memory are separate and every value has to travel between them; John Backus called this the "von Neumann bottleneck" in his 1977 Turing Award lecture (Von Neumann architecture, Wikipedia; details in `00_computing_fundamentals.md`, section 2). The brain keeps memory (synapses) and computation (neurons) in the same place and runs on a small, fixed power budget: the commonly cited figure is 20 W, of which, by one estimate, only about 0.1 W goes into cortical computation and about 3.5 W into communication, 35 times more (Levy & Calvert 2021, PNAS). Both observations, local memory and the high cost of communication, return in every neuromorphic design, and in SpiNNaker in particular (section 4).

**Carver Mead and analog VLSI.** Mead, a Caltech professor and co-author with Lynn Conway of the textbook *Introduction to VLSI Systems* on [VLSI](https://en.wikipedia.org/wiki/Very-large-scale_integration) chip design, turned to biology in the 1980s. His idea: a transistor operated at very low currents behaves like an ion channel in a neuron, so analog circuits can compute with physics instead of with digital arithmetic (Carver Mead, Wikipedia; the physics argument itself *(assumption, to check in Mead 1990)*). His group produced the analog silicon cochlea (Lyon and Mead, 1988) and, with his PhD student [Misha Mahowald](https://en.wikipedia.org/wiki/Misha_Mahowald), the silicon retina (late 1980s, *Scientific American* 1991). The book *Analog VLSI and Neural Systems* (1989) and the paper "Neuromorphic electronic systems" (*Proceedings of the IEEE*, October 1990) gave the field its name (Carver Mead, Wikipedia; Mead 1990).

**Spikes as addresses (AER).** Wiring every silicon neuron to every other one is impossible, so Mead's group sent spikes over a shared digital bus: each spike is transmitted as the *address* of the neuron that fired, and the time of the spike is simply the time the message arrives. Mahowald and Massimo Sivilotti filed a patent on this asynchronous communication between chips in 1992, granted in 1995 (Misha Mahowald, Wikipedia). This **address-event representation (AER)** became the standard way neuromorphic chips and [event cameras](https://en.wikipedia.org/wiki/Event_camera) talk to each other *(that AER is the standard for event cameras: assumption, to check)*. SpiNNaker's packets follow the same idea: a packet identifies only the source of a spike, the timing is implicit (Furber et al. 2014, abstract). In 1995 Mahowald co-founded the [Institute of Neuroinformatics](https://www.ini.uzh.ch/) in Zurich (Misha Mahowald, Wikipedia), which later produced the DYNAP chips and the company SynSense (section 3.4).

<details>
<summary><b>Side topic:</b> the physics of computation at Caltech</summary>

<br>

Mead's turn to neural systems happened in the same circle as two other later famous names: he worked with [John Hopfield](https://en.wikipedia.org/wiki/John_Hopfield) and Richard Feynman on the "physics of computation" (Carver Mead, Wikipedia). Hopfield's 1982 network, which computes by relaxing into an energy minimum, is one of the foundations of modern machine learning recognised by the 2024 Nobel Prize in Physics (see `sources.md`, further reading). The QUBO solvers that run on SpiNNaker2 today (`04_applications.md`, section 2.1) are a distant descendant of this line of thought.

</details>

<br>

**Workshop:** 1 min. The 20 W brain against a GPU, and "spikes are sent as addresses", which links directly to how SpiNNaker2 routes spikes (`02_hardware_energy.md`, section 4).

## 3. The big programmes

From about 2005 to 2023, neuromorphic hardware grew from single research chips to systems with millions of neurons, funded by a few large programmes. They had different goals, which still explains the differences between the chips.

### 3.1 United States: SyNAPSE and TrueNorth

DARPA's **SyNAPSE** programme funded IBM and HRL Laboratories from November 2008 (initially $4.9 million to IBM and $5.9 million to HRL, followed by larger tranches) (SyNAPSE, Wikipedia). Its best-known result is IBM's **TrueNorth** chip (2014): 5.4 billion transistors, 4,096 "neurosynaptic cores", 1 million programmable spiking neurons and 256 million synapses, drawing 63 mW while processing a 400 × 240 video at 30 frames per second (Merolla et al. 2014, *Science*). TrueNorth is digital and uses a simple, fixed leaky integrate-and-fire neuron with configurable parameters ([Cognitive computer](https://en.wikipedia.org/wiki/Cognitive_computer), Wikipedia). It was built for low-power inference, not for brain research.

IBM's successor **NorthPole** (2023) dropped spikes altogether: it is a digital inference chip for conventional neural networks that places memory next to compute and avoids off-chip memory. On ResNet-50 it reports about 25 times more frames per second per watt than a GPU in a comparable 12 nm process (Modha et al. 2023, *Science*, abstract). NorthPole shows that the "brain-inspired" idea that survived at IBM is *memory next to compute*, not spiking.

### 3.2 Europe: FACETS, BrainScaleS and the Human Brain Project

In Heidelberg, the EU projects **FACETS** (2006–2010) and **BrainScaleS** (2011–2015) built analog "physical model" systems (KIP Heidelberg): circuits whose voltages follow the equations of a neuron model, like Mead's chips, but running much faster than biology. **BrainScaleS-1** was a wafer-scale system that runs up to 10,000 times faster than real time (EBRAINS); **BrainScaleS-2** has chips with 512 analog neurons implementing the adaptive exponential integrate-and-fire (AdEx) model, a 1,000-fold speed-up, and embedded digital processors for programmable plasticity (Pehle et al. 2022). The speed-up makes it possible to simulate learning over days of biological time in minutes *(illustration, assumption to check)*; the price is that it can't interact with the real world in real time.

The **Human Brain Project (HBP)**, an EU flagship from 1 October 2013 to 30 September 2023 with a budget of about €1 billion and coordinated by EPFL (Human Brain Project, Wikipedia), brought the two European lines together in its neuromorphic computing platform: **SpiNNaker** in Manchester (digital, real time) and **BrainScaleS** in Heidelberg (analog, accelerated). Both remain available remotely, free for evaluation and basic research, through EBRAINS, the HBP's successor infrastructure, programmed with the [PyNN](https://neuralensemble.org/PyNN/) interface (EBRAINS). The HBP also funded the development of SpiNNaker2 (section 4.2).

<details>
<summary><b>Side topic:</b> the controversy around the Human Brain Project</summary>

<br>

The HBP was criticised from the start. In 2014, an open letter by European neuroscientists objected to its narrow focus on simulation and the reduced role of cognitive neuroscience and threatened a boycott; in 2015, the three-person executive committee led by Henry Markram was replaced by a larger governing board (Human Brain Project, Wikipedia). For the workshop, the relevant point is that the neuromorphic platforms were among the parts of the HBP that delivered working infrastructure, and that "simulate the whole brain" was a goal of the project's public image more than of the hardware teams *(assessment, assumption to check)*.

</details>

<br>

### 3.3 Intel: Loihi and Hala Point

Intel announced **Loihi** in 2017: a digital chip in Intel's 14 nm process with 128 cores *(Wikipedia says "clusters", to check)*, 131,072 neurons and on-chip learning (Intel Loihi, Wikipedia; Davies et al. 2018). **Loihi 2** followed in September 2021 (Intel Loihi, Wikipedia), with up to 1 million neurons per chip (press reports found by web search; *(assumption, to check)* in an Intel source) and programmable neuron models *(assumption, to check)*, together with the open-source framework Lava. In April 2024 Intel presented **Hala Point**, built from 1,152 Loihi 2 chips: 1.15 billion neurons, 128 billion synapses, at most 2,600 W, installed at Sandia National Laboratories (Intel 2024, press release). Intel ran Loihi as a research programme with an external research community and never sold it as a product; Lava was archived in May 2026 (`04_applications.md`, section 4.3). Measured Loihi results are in `04_applications.md`, section 4.1.

### 3.4 Others

- **Neurogrid** (Stanford, Kwabena Boahen's group): 16 mixed analog-digital "Neurocore" chips simulating 1 million neurons in real time on less than 2 W, first operational in late 2009 ([Neurogrid](https://en.wikipedia.org/wiki/Neurogrid), Wikipedia; Benjamin et al. 2014).
- **DYNAP and SynSense** (Zurich): the DYNAP chips from the INI combine analog neuron and synapse circuits with asynchronous digital spike routing (Moradi et al. 2017). SynSense was spun out of the INI in March 2017 (eeNews Europe 2020); its Speck chip puts an event camera and an asynchronous digital spiking processor on one die at below 1 mW (Yao et al. 2024).
- **Tianjic** (2019): a hybrid chip that runs both conventional neural networks and spiking networks; one chip steered an unmanned bicycle with object tracking, voice control and balance control at the same time (Pei et al. 2019, *Nature*).
- **Akida** (BrainChip, Australia): an event-based neuromorphic processor for edge devices; development kits from October 2021, second generation announced in March 2023 ([BrainChip](https://en.wikipedia.org/wiki/BrainChip), Wikipedia).

**Workshop:** 1 min, as the left half of the map in section 5: "the US built inference chips, Europe built brain simulators, Intel built a research platform".

## 4. SpiNNaker from brain simulator to AI hardware

### 4.1 SpiNNaker1 in Manchester

[Steve Furber](https://en.wikipedia.org/wiki/Steve_Furber) worked at Acorn Computers from 1981 to 1990 on the BBC Micro and, with [Sophie Wilson](https://en.wikipedia.org/wiki/Sophie_Wilson), on the first ARM processor; in 1990 he became ICL Professor of Computer Engineering at the University of Manchester (Steve Furber, Wikipedia). In 2022 he shared the Draper Prize with Wilson, John Hennessy and David Patterson (Steve Furber, Wikipedia). He conceived SpiNNaker as a computer that works more like a brain; the project took about 20 years from conception and more than 10 years of construction, starting in 2006, funded first by the UK research council EPSRC and later by the HBP, for about £15 million in total (Manchester 2018).

**The idea** was the opposite of Mead's: don't build neurons in analog circuits, but use many small, cheap, standard digital processors and run neuron models as software, so any model can be programmed. What had to be specialised was the communication, because a neuron sends each spike to thousands of others. On SpiNNaker1:

- each chip has 18 ARM cores (ARM968) at 200 MHz with 32 KiB instruction and 64 KiB data memory each, plus 128 MiB of external SDRAM per chip for the synapses (Knight & Furber 2016; SpiNNaker, Wikipedia), made in 130 nm CMOS (Mayr et al. 2019);
- a firing neuron sends one small packet carrying its ID to the chip's router, which copies it to every core that simulates a target neuron, across a network in which each chip connects to six neighbours (Knight & Furber 2016): AER, implemented as multicast packets;
- the cores update their neurons every 1 ms of simulated time and must finish within that 1 ms, so the machine runs in **biological real time**, which allows closed loops with robots and sensors (Knight & Furber 2016).

The **million-core machine** was switched on on 2 November 2018: 57,600 chips with 1,036,800 cores in 10 racks, drawing about 100 kW (Manchester 2018; SpiNNaker, Wikipedia). Its target was 1 billion neurons in real time, about 1 % of a human brain with just under 100 billion neurons (Manchester 2018). The best-known scientific result is a model of 1 mm² of cortex running in real time with less energy than HPC simulators (Rhodes et al. 2020, summarised in `04_applications.md`, section 3). The machine is used through PyNN and the sPyNNaker software, via EBRAINS (SpiNNaker Manchester software pages).

### 4.2 SpiNNaker2 in Dresden

The second generation was designed at TU Dresden in Christian Mayr's group, with Manchester and within the HBP. The 2019 roadmap named both goals in its title, "brain simulation and machine learning": a system of 10 million cores in 22 nm FDSOI, with adaptive body biasing, per-core power management and numerical accelerators, for more than 50 times the simulation capacity of SpiNNaker1, and applications beyond neuroscience such as automotive AI, tactile internet and biomedical processing (Mayr, Höppner & Furber 2019). In September 2019 the HBP granted TU Dresden €8 million for the second-generation machine (SpiNNaker, Wikipedia). The chip was taped out in July 2021 by TU Dresden, the University of Manchester, Racyics and GlobalFoundries in the 22FDX process, with processing elements at 0.50 V and dynamic voltage and frequency scaling (Design & Reuse 2021, press release).

Compared with SpiNNaker1, the design shifted from "simulate neurons in software" to "simulate neurons in software, and accelerate the arithmetic of neural networks in hardware": each of the 152 processing elements has an ARM Cortex-M4F plus a MAC array for matrix operations and accelerators for exponentials and random numbers (`02_hardware_energy.md`, sections 1 and 2). The MAC array is what allows conventional DNN layers and hybrid networks on the same chip.

### 4.3 From SpiNNcloud to Sparxity

SpiNNaker2 has been developed further since summer 2021 by **SpiNNcloud Systems GmbH** in Dresden, co-founded by Mayr (SPRIND), with Hector Gonzalez as co-founder and co-CEO (The Register 2024). In May 2024 SpiNNcloud made SpiNNaker2 systems commercially available as a "hybrid AI" high-performance computer, with 48 chips per board and 90 boards per rack (The Register 2024). The system at TU Dresden, with about 35,000 chips and more than 5 million cores, went into operation in April 2025 and is presented as infrastructure for energy-efficient AI, not for brain simulation (TU Dresden 2025). Further systems went to Sandia, Leipzig, Jülich, Göttingen and HPI (`04_applications.md`, section 2.2).

On 28 October 2026 SpiNNcloud renamed itself **Sparxity**, now describing its products as "sparse-native computing" and its next generation as relying entirely on sparsity for AI inference in data centres (Silicon Saxony 2026, press release). The word "neuromorphic" no longer appears in the company's positioning (`04_applications.md`, section 4.4).

**Workshop:** 2 min, the core of the history part: Furber and ARM, "1 % of the brain in real time", the million-core machine, then Dresden and the chips in the HPI rack.

## 5. A map of the approaches

The chips differ along four axes: how they compute (digital or analog), how flexible the neuron model is, how simulated time relates to wall-clock time, and what they are for.

| Platform | Origin, year | Circuits | Neuron model | Time | Main target | Source |
|---|---|---|---|---|---|---|
| SpiNNaker1 | Manchester, 2018 (full machine) | digital, ARM cores | programmable (software) | real time (1 ms steps) | brain simulation | Knight & Furber 2016; Manchester 2018 |
| SpiNNaker2 | TU Dresden + Manchester, 2021 (tapeout) | digital, ARM cores + MAC accelerators | programmable (software) | real time | hybrid SNN/DNN, now sparse AI inference | Mayr et al. 2019; `02_hardware_energy.md` |
| TrueNorth | IBM, 2014 | digital | fixed (leaky integrate-and-fire, configurable) | real time | low-power inference | Merolla et al. 2014; Cognitive computer, Wikipedia |
| NorthPole | IBM, 2023 | digital | not spiking | — | DNN inference | Modha et al. 2023 |
| Loihi / Loihi 2 | Intel, 2017 / 2021 | digital | configurable / programmable *(to check)* | not tied to real time; Hala Point up to 20× faster than biology (vendor) | research platform: optimisation, sparse inference, learning | Davies et al. 2018; Intel 2024 |
| BrainScaleS-1 / -2 | Heidelberg, 2011–2015 / later | mixed-signal, analog neurons | fixed (AdEx, analog), programmable plasticity (BSS-2) | accelerated, 10,000× / 1,000× | brain research, learning | EBRAINS; Pehle et al. 2022 |
| Neurogrid | Stanford, 2009 | mixed analog-digital | fixed (analog) | real time | brain simulation | Neurogrid, Wikipedia |
| DYNAP / Speck | INI Zurich / SynSense, 2017– | DYNAP mixed-signal; Speck asynchronous digital with on-die event camera | fixed | real time | edge sensing | Moradi et al. 2017; Yao et al. 2024 |
| Akida | BrainChip, 2021 | digital *(to check)* | fixed *(to check)* | real time *(to check)* | edge inference | BrainChip, Wikipedia |
| Tianjic | Pei et al., 2019 | digital *(to check)* | hybrid ANN and SNN | real time (bicycle demo) | robotics, general AI research | Pei et al. 2019 |

**Where GPUs and brain simulators fit.** Most brain simulation is still done in software on CPUs and GPUs, and the neuromorphic machines are compared against them. [NEST](https://en.wikipedia.org/wiki/NEST_(software)) (first released 2004) simulates large networks of simple point neurons on clusters and supercomputers (NEST, Wikipedia); [NEURON](https://en.wikipedia.org/wiki/Neuron_(software)) simulates single cells and networks with detailed morphology split into compartments (Neuron, Wikipedia); [GeNN](https://github.com/genn-team/genn) generates GPU code for spiking networks (GeNN repository); [Brian2](https://en.wikipedia.org/wiki/Brian_(software)) is the fallback of this workshop (`03_brian2_fallback.md`). The SpiNNaker1 cortical model of section 4.1 was benchmarked against exactly these kinds of systems (Rhodes et al. 2020). On the ML side, the competitors are GPUs and edge accelerators, discussed in `02_hardware_energy.md`, section 8.

<details>
<summary><b>Reading the map:</b> three trade-offs behind the table</summary>

<br>

- **Analog vs digital.** Analog circuits compute with the physics of the transistor and can be very efficient per operation, but they vary from chip to chip and need calibration (BrainScaleS-2 does on-chip calibration with its embedded processors, Pehle et al. 2022). Digital chips give the same result every time and follow the newest manufacturing processes. All large systems built after 2014, including the commercial ones, are digital *(observation from the table, not a sourced claim)*.
- **Fixed vs programmable neurons.** A fixed neuron circuit is small and efficient but locks in one model. SpiNNaker pays for flexibility with energy: about 0.2 nJ per synaptic event on the ARM core (`02_hardware_energy.md`, section 8), far more than dedicated circuits *(comparison to check per chip)*.
- **Real time vs accelerated.** Real time (SpiNNaker, TrueNorth, Neurogrid) allows closed loops with sensors and robots. Acceleration (BrainScaleS) allows long learning experiments, but no direct interaction with the world.

</details>

<br>

**Workshop:** the table as a backup slide for questions, not presented in full. In the talk one sentence: "SpiNNaker is the digital, programmable, real-time corner of the map".

## 6. Between three communities

SpiNNaker has always sat between three communities, and its public description followed whichever one funded it at the time.

| Period | Main community | How SpiNNaker was described | Source |
|---|---|---|---|
| 2006–2018 | brain research (EPSRC, then HBP) | a machine for real-time brain modelling, 1 % of the human brain | Manchester 2018 |
| 2019 | brain research and ML | "brain simulation and machine learning" | Mayr et al. 2019 |
| 2021 | hardware research and applications | event-based, real-time AI below 1 ms latency, for autonomous driving, smart cities, tactile internet | Design & Reuse 2021 |
| 2024 | ML | "event-based and asynchronous machine learning", "hybrid AI" HPC | Gonzalez et al. 2024; The Register 2024 |
| 2025 | AI infrastructure | energy-efficient AI at TU Dresden | TU Dresden 2025 |
| 2026 | AI inference market | "sparse-native computing" for data centres | Silicon Saxony 2026 |

- **Brain research** values real time, programmable neuron models and large scale. SpiNNaker1 was built for it; SpiNNaker2 still runs spiking networks, but none of the published SpiNNaker2 results is a brain simulation (`04_applications.md`, section 2.1).
- **Hardware research** values the chip itself: 22 nm FDSOI, adaptive body biasing, DVFS, many-core networks-on-chip (Höppner et al. 2021). The chip paper is the most complete record of it (Scholze et al. 2026).
- **ML and AI** value energy per inference and integration with PyTorch. Here SpiNNaker2 competes with GPUs and edge accelerators, and the measured advantages are limited to small, sparse workloads processed one input at a time (`04_applications.md`, section 1).

The shift is not unique to SpiNNaker: IBM went from spiking TrueNorth to non-spiking NorthPole, and Intel archived Lava. When the HBP ended in 2023, brain simulation lost its largest funder, while AI energy consumption became a commercial argument *(interpretation, assumption to check)*.

**Workshop:** 30 s, one sentence for the ML audience: "built to simulate the brain, now sold for sparse AI; this workshop uses both sides".

## 7. Likely questions and answers

<details>
<summary><b>Why does SpiNNaker exist at all?</b></summary>

<br>

Steve Furber, a co-designer of the ARM processor, wanted a computer that works more like a brain, and the goal was a million cores in one machine for real-time brain modelling (Manchester 2018). Instead of special neuron circuits, SpiNNaker uses many small standard ARM cores and a network optimised for very small spike packets, so neuroscientists can program any neuron model.

</details>

<br>

<details>
<summary><b>Is SpiNNaker for brain research or for AI?</b></summary>

<br>

Both, in sequence. SpiNNaker1 was built for brain simulation in real time; SpiNNaker2 was planned for "brain simulation and machine learning" (Mayr et al. 2019) and is now marketed for sparse AI inference (Silicon Saxony 2026). py-spinnaker2, used in this workshop, runs spiking networks and imports models trained in PyTorch via NIR (`04_applications.md`, section 4.3).

</details>

<br>

<details>
<summary><b>How is it different from Intel's Loihi?</b></summary>

<br>

Both are digital many-core chips with a spike network. Loihi implements neurons in dedicated digital circuits, SpiNNaker2 runs them as software on ARM cores and adds a MAC array for dense matrix operations. The only same-task comparison found: Loihi 1 was more efficient for small matrix operations, a SpiNNaker2 prototype for large ones (Yan et al. 2021, see `04_applications.md`, section 2.1). Loihi stayed a research chip and its framework Lava was archived in 2026; SpiNNaker2 is sold commercially.

</details>

<br>

<details>
<summary><b>How is it different from TrueNorth and BrainScaleS?</b></summary>

<br>

TrueNorth (IBM, 2014) is digital too, but has one fixed neuron model and was built for low-power inference (Merolla et al. 2014). BrainScaleS (Heidelberg) uses analog circuits that run 1,000 to 10,000 times faster than biology (EBRAINS; Pehle et al. 2022), good for long learning experiments but unable to interact with the world in real time. SpiNNaker is programmable and runs in real time.

</details>

<br>

<details>
<summary><b>Can SpiNNaker simulate a human brain?</b></summary>

<br>

No. The million-core SpiNNaker1 aimed at 1 billion neurons, about 1 % of a human brain (Manchester 2018). Even the 5-million-core SpiNNaker2 system in Dresden reaches only a few percent of the neurons of a human brain, and far fewer of its synapses (`02_hardware_energy.md`, section 5, Figure 7).

</details>

<br>

<details>
<summary><b>If neuromorphic chips are so efficient, why does everyone use GPUs?</b></summary>

<br>

Because the measured advantages are narrow: sparse activity, one input at a time, small networks. On dense deep learning with large batches, GPUs win on both time and energy (`04_applications.md`, section 4.2). GPUs also have a mature software stack, while each neuromorphic chip has its own. Even the vendors of neuromorphic systems now describe them as sparse AI hardware (section 6).

</details>

<br>

<details>
<summary><b>Why ARM cores instead of special neuron circuits?</b></summary>

<br>

Programmability: any neuron model, learning rule or even a non-neural algorithm can run on a general-purpose core, which is why SpiNNaker2 also runs QUBO solvers and graph search (`04_applications.md`, section 2.1). The price is energy per synaptic event, which is higher than in dedicated circuits (`02_hardware_energy.md`, section 8). ARM cores are small and efficient, and Furber had co-designed the first one (`00_computing_fundamentals.md`, section 5).

</details>

<br>

<details>
<summary><b>What does "neuromorphic" actually mean?</b></summary>

<br>

Mead used it in 1990 for electronic systems that copy the organisation of the nervous system (Mead 1990). Today it covers any hardware that borrows principles from the brain: spikes, events, memory next to compute, massive parallelism. The term is broad enough that IBM calls its non-spiking NorthPole "neural-inspired" (Modha et al. 2023) and Sparxity has dropped it (Silicon Saxony 2026).

</details>

<br>

**Workshop:** not presented; preparation for the questions after the motivation block.

## To check

- [ ] Mead's physics argument (subthreshold transistors behave like ion channels) and his definition of "neuromorphic": check in the full text of Mead 1990 (the PDF could not be fetched on 2026-11-05).
- [ ] AER: who introduced it and when (Sivilotti 1991, Mahowald 1992, Lazzaro et al. 1993 according to secondary sources); whether it is the standard interface of event cameras.
- [ ] Furber et al. 2014 (SpiNNaker project, *Proc. IEEE*): only the abstract was seen; check the design rationale and the 18-core / 1 W figures (Painkras et al. 2013).
- [ ] Loihi 2: programmable neuron models and the 1-million-neuron figure in an Intel source; Loihi 1 core count (Wikipedia speaks of 128 "clusters").
- [ ] Akida and Tianjic: digital or mixed-signal, fixed or programmable neurons, real-time operation.
- [ ] BrainScaleS: years of BrainScaleS-2, and the illustration "days of biological time in minutes".
- [ ] HBP controversy: whether the hardware teams themselves ever claimed whole-brain simulation as a goal.
- [ ] Section 6: that the end of the HBP shifted SpiNNaker2 towards AI is an interpretation; check against an interview with Mayr or Furber (e.g. EE Times podcast 2023 in `sources.md`).
- [ ] Energy per synaptic event of other chips (TrueNorth, Loihi), for the "programmable costs energy" claim in section 5.

## Sources

Retrieved 2026-11-05 unless noted. "Paper" = peer-reviewed (or preprint where stated), "Encyclopaedia" = Wikipedia, "Vendor/press" = company announcements, university news and trade press.

| Short name | Source | Type |
|---|---|---|
| Mead 1990 | [C. Mead, Neuromorphic electronic systems, Proceedings of the IEEE, October 1990](https://doi.org/10.1109/5.58356) (metadata only) | Paper |
| Levy & Calvert 2021 | [W. B. Levy, V. G. Calvert, Communication consumes 35 times more energy than computation in the human cortex, PNAS 118(18), 2021](https://pubmed.ncbi.nlm.nih.gov/33906943/) (abstract via Europe PMC) | Paper |
| Merolla et al. 2014 | [P. A. Merolla et al., A million spiking-neuron integrated circuit with a scalable communication network and interface, Science 345, 668–673, 2014](https://doi.org/10.1126/science.1254642) (abstract via Europe PMC) | Paper |
| Modha et al. 2023 | [D. S. Modha et al., Neural inference at the frontier of energy, space, and time, Science, 2023](https://doi.org/10.1126/science.adh1174) (abstract via Semantic Scholar) | Paper |
| Davies et al. 2018 | [M. Davies et al., Loihi: a neuromorphic manycore processor with on-chip learning, IEEE Micro, 2018](https://doi.org/10.1109/MM.2018.112130359) (metadata only) | Paper |
| Benjamin et al. 2014 | [B. V. Benjamin et al., Neurogrid: a mixed-analog-digital multichip system for large-scale neural simulations, Proc. IEEE, 2014](https://doi.org/10.1109/JPROC.2014.2313565) (metadata only) | Paper |
| Pei et al. 2019 | [J. Pei et al., Towards artificial general intelligence with hybrid Tianjic chip architecture, Nature 572, 106–111, 2019](https://doi.org/10.1038/s41586-019-1424-8) (abstract via Europe PMC) | Paper |
| Moradi et al. 2017 | [S. Moradi, N. Qiao, F. Stefanini, G. Indiveri, A scalable multi-core architecture with heterogeneous memory structures for DYNAPs, arXiv:1708.04198](https://arxiv.org/abs/1708.04198) | Paper (preprint) |
| Pehle et al. 2022 | [C. Pehle et al., The BrainScaleS-2 accelerated neuromorphic system with hybrid plasticity, Frontiers in Neuroscience, 2022](https://www.frontiersin.org/articles/10.3389/fnins.2022.795876/full) | Paper |
| Yao et al. 2024 | [M. Yao et al., Spike-based dynamic computing with asynchronous sensing-computing neuromorphic chip, Nature Communications, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11127998/) | Paper |
| Furber et al. 2014 | [S. Furber, F. Galluppi, S. Temple, L. Plana, The SpiNNaker project, Proc. IEEE 102(5), 652–665, 2014](https://doi.org/10.1109/JPROC.2014.2304638) (abstract only, via search) | Paper |
| Knight & Furber 2016 | [J. C. Knight, S. B. Furber, Synapse-centric mapping of cortical models to the SpiNNaker neuromorphic architecture, Frontiers in Neuroscience, 2016](https://www.frontiersin.org/articles/10.3389/fnins.2016.00420/full) | Paper |
| Rhodes et al. 2020 | [O. Rhodes et al., Real-time cortical simulation on neuromorphic hardware](https://arxiv.org/abs/1909.08665) (checked in `04_applications.md`) | Paper |
| Mayr et al. 2019 | [C. Mayr, S. Höppner, S. Furber, SpiNNaker 2: a 10 million core processor system for brain simulation and machine learning, arXiv:1911.02385](https://arxiv.org/abs/1911.02385) | Paper |
| Höppner et al. 2021 | [S. Höppner et al., The SpiNNaker 2 processing element architecture for hybrid digital neuromorphic computing, arXiv:2103.08392](https://arxiv.org/abs/2103.08392) | Paper (preprint) |
| Gonzalez et al. 2024 | [H. A. Gonzalez et al., SpiNNaker2: a large-scale neuromorphic system for event-based and asynchronous machine learning, arXiv:2401.04491](https://arxiv.org/abs/2401.04491) | Paper (workshop) |
| Scholze et al. 2026 | [The SpiNNaker2 chip, arXiv:2607.24396](https://arxiv.org/abs/2607.24396) (read for `02_hardware_energy.md`) | Paper (preprint) |
| Yan et al. 2021 | [Y. Yan et al., Comparing Loihi with a SpiNNaker 2 prototype, arXiv:2009.08921](https://arxiv.org/abs/2009.08921) (via `04_applications.md`) | Paper |
| Kudithipudi et al. 2025 | [D. Kudithipudi, …, S. Furber, Neuromorphic computing at scale, Nature 637, 801–812, 2025](https://doi.org/10.1038/s41586-024-08253-8) (abstract via Europe PMC); field overview, recommended background | Paper (review) |
| Carver Mead, Wikipedia | [Carver Mead](https://en.wikipedia.org/wiki/Carver_Mead) | Encyclopaedia |
| Misha Mahowald, Wikipedia | [Misha Mahowald](https://en.wikipedia.org/wiki/Misha_Mahowald) | Encyclopaedia |
| Von Neumann architecture, Wikipedia | [Von Neumann architecture](https://en.wikipedia.org/wiki/Von_Neumann_architecture) | Encyclopaedia |
| Steve Furber, Wikipedia | [Steve Furber](https://en.wikipedia.org/wiki/Steve_Furber) | Encyclopaedia |
| SpiNNaker, Wikipedia | [SpiNNaker](https://en.wikipedia.org/wiki/SpiNNaker) | Encyclopaedia |
| SyNAPSE, Wikipedia | [SyNAPSE](https://en.wikipedia.org/wiki/SyNAPSE) | Encyclopaedia |
| Cognitive computer, Wikipedia | [Cognitive computer](https://en.wikipedia.org/wiki/Cognitive_computer) (TrueNorth, NorthPole) | Encyclopaedia |
| Human Brain Project, Wikipedia | [Human Brain Project](https://en.wikipedia.org/wiki/Human_Brain_Project) | Encyclopaedia |
| Intel Loihi, Wikipedia | [Intel Loihi](https://en.wikipedia.org/wiki/Intel_Loihi) | Encyclopaedia |
| Neurogrid, Wikipedia | [Neurogrid](https://en.wikipedia.org/wiki/Neurogrid) | Encyclopaedia |
| BrainChip, Wikipedia | [BrainChip](https://en.wikipedia.org/wiki/BrainChip) | Encyclopaedia |
| NEST, Wikipedia | [NEST (software)](https://en.wikipedia.org/wiki/NEST_(software)) | Encyclopaedia |
| Neuron, Wikipedia | [Neuron (software)](https://en.wikipedia.org/wiki/Neuron_(software)) | Encyclopaedia |
| GeNN repository | [genn-team/genn](https://github.com/genn-team/genn) | Software |
| KIP Heidelberg | [Electronic Vision(s) group, BrainScaleS project page](https://www.kip.uni-heidelberg.de/vision/research/brainscales/) (project years) | University |
| EBRAINS | [EBRAINS neuromorphic computing](https://www.ebrains.eu/modelling-simulation-and-computing/computing/neuromorphic-computing/) | Research infrastructure |
| SpiNNaker Manchester software pages | [spinnakermanchester.github.io](https://spinnakermanchester.github.io/) | University |
| Manchester 2018 | [University of Manchester, 'Human brain' supercomputer with 1 million processors switched on for first time, 2 Nov 2018](https://www.manchester.ac.uk/about/news/human-brain-supercomputer-with-1million-processors-switched-on-for-first-time/) | University press |
| Design & Reuse 2021 | [Tapeout of SpiNNaker2 in GF 22FDX (TU Dresden, Manchester, Racyics, GlobalFoundries), 27 Jul 2021](https://www.design-reuse.com/news/50366/ai-chip-gf-22fdx-racyics-tu-dresden-manchester.html) | Vendor/press |
| SPRIND | [SPRIND, Artificial intelligence, inspired by nature: the SpiNNaker2 supercomputer](https://www.sprind.org/en/projects/mayr) | Funder page |
| The Register 2024 | [SpiNNcloud unveils Arm-based neuromorphic system, 8 May 2024](https://www.theregister.com/2024/05/08/spinncloud_systems_unveils_armbased_neuromorphic/) | Press |
| TU Dresden 2025 | [TU Dresden, Milestone for energy-efficient AI systems: TUD launches SpiNNcloud supercomputer, 15 Apr 2025](https://tu-dresden.de/cids/center/news/milestone-for-energy-efficient-ai-systems-tud-launches-spinncloud-supercomputer?set_language=en) | University press |
| Silicon Saxony 2026 | [Sparxity: sparse-native computing system announced at the Jülich Supercomputing Centre, 28 Oct 2026](https://silicon-saxony.de/en/sparxity-installation-of-a-sparse-native-computing-system-worth-several-million-dollars-announced-at-the-juelich-supercomputing-center/) | Vendor/press |
| Intel 2024 | [Intel, Intel builds world's largest neuromorphic system, 17 Apr 2024](https://www.intc.com/news-events/press-releases/detail/1691/intel-builds-worlds-largest-neuromorphic-system-to) | Vendor |
| eeNews Europe 2020 | [Swiss neuromorphic startup changes name, raises money, 12 May 2020](https://www.eenewseurope.com/en/swiss-neuromorphic-startup-changes-name-raises-money) (SynSense) | Press |
