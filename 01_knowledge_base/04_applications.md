# Applications of SpiNNaker2 and Neuromorphic Computing

What SpiNNaker2 and other neuromorphic chips have actually been used for, with measured results, and where they don't beat conventional hardware. Material for the motivation part of the workshop and for choosing demos. Builds on `02_hardware_energy.md` (chip, energy, the "18×" claim) and `01_primer_snn_basics.md` (sparsity, event-driven computing).

Status 2026-11-05. Based on two web researches of 2026-11-04 (raw reports in `_local/`, not tracked). The papers of section 2.1 were checked in full text on 2026-11-05; in the other sections, numbers marked as checked were compared with the paper's text or abstract. Everything else is marked *(not checked yet)* and listed under [To check](#to-check).

## Contents

- [1. Summary](#1-summary)
- [2. Applications on SpiNNaker2](#2-applications-on-spinnaker2)
  - [2.1 Published results](#21-published-results)
  - [2.2 Large installations and the multi-chip gap](#22-large-installations-and-the-multi-chip-gap)
- [3. SpiNNaker1 highlights](#3-spinnaker1-highlights)
- [4. Neuromorphic computing across platforms](#4-neuromorphic-computing-across-platforms)
  - [4.1 Where measured advantages exist](#41-where-measured-advantages-exist)
  - [4.2 Where conventional hardware wins](#42-where-conventional-hardware-wins)
  - [4.3 Software](#43-software)
  - [4.4 Industry](#44-industry)
- [5. Consequences for the workshop](#5-consequences-for-the-workshop)
- [To check](#to-check)

## 1. Summary

- **Every published SpiNNaker2 application result found runs on one chip** on a test board, or on an older prototype. About 40,000 chips are installed in large systems (TU Dresden, Leipzig, Jülich, UTSA, Sandia), but no published result uses more than one chip; the vendor says the software for large systems is still under development (section 2.2).
- **The recurring pattern: less energy, often more time.** SpiNNaker2 needs about 3–30× less energy than the authors' baseline for single inputs (batch size 1), but is often slower, and a GPU that processes several inputs at once can win on energy too (section 2.1).
- **Across all platforms, the measured wins come from sparse data processed one input at a time:** always-on sensors, event cameras, streaming sequences. On dense deep learning with large batches, no neuromorphic chip has measured wins (section 4).
- **Spiking networks only save energy at very low activity:** below about 6 % spike rate, or 0.15–1.4 spikes per synapse per inference, depending on the study (section 4.2).
- **Many advertised factors (18×, 78×, 1000×) come without baseline or batch size.** The vendor of SpiNNaker2 renamed itself from SpiNNcloud to Sparxity in October 2026 and now markets the chip for sparse AI inference rather than as neuromorphic hardware (section 4.4).

## 2. Applications on SpiNNaker2

### 2.1 Published results

Each result ran on a single chip on a test board. The baselines are the ones the authors chose, and what exactly they measure differs between papers (notes below the table). All rows were checked against the full text of the papers on 2026-11-05 (PDFs in `_local/paper/`, not tracked).

| Application | Result on SpiNNaker2 | Baseline | Code | Source |
|---|---|---|---|---|
| [Reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning): spiking Q-network controlling CartPole and Acrobot in a closed loop, 8-bit weights | CartPole: reward 200, 0.006 J, 0.020 s, 0.335 W. Acrobot: reward −67, 0.010 J | GTX 1650: CartPole 0.145 J (24×), 0.0197 s, 7.39 W. Acrobot: reward −75, 0.321 J (32×) | linked in the paper, but private (checked 2026-11-04); uses py-spinnaker2 and snnTorch | Arfa, Vogginger, Mayr 2025, ICONS |
| Gesture recognition from an [event camera](https://en.wikipedia.org/wiki/Event_camera) (DVS Gesture), imported via NIR, 8-bit weights | 94.13 % (quantisation-aware training; 94.0 % with post-training quantisation), 459 mJ per gesture (0.765 mJ per 1 ms frame). Only about 600 ms of each 6 s gesture is processed, at 3.5 ms per 1 ms frame | same model off-chip in 32-bit float: 94.69 % and 95.07 %. No GPU energy or time measured; TrueNorth needs 18.8 mJ with a different network | public, link in the paper | Arfa et al. 2025 (preprint) |
| Language model, event-based GRU (EGRU), WikiText-2, 95 % of the weights pruned | perplexity 81.4 (same as the GPU), 0.065 J and 170 ms per inference, 0.39 W. 32-bit float on 150 PEs, MAC array not used | A100 at batch size 1: 1.19 J (18×), 19.9 ms (8.6× faster), 60 W | not stated | Nazeer et al. 2024, AICAS; details in `02_hardware_energy.md`, section 8 |
| On-chip training with event-based [backpropagation](https://en.wikipedia.org/wiki/Backpropagation) (EventProp), Yin-Yang dataset, network 5–120–3 | 61 ms per training step (30 ms of input in real time, then the backward pass), 0.45 W ("full-system") | RTX 4070 running the authors' PyTorch version: 6.61 ms, 13.5 W (card only) | PyTorch version named "pytorch-eventprop" without a link; on-chip code not stated | Béna et al. 2024, NeurIPS workshop MLNCP |
| [Shortest path](https://en.wikipedia.org/wiki/Shortest_path_problem) search (NEURO-MAPP), 3D city graph with 38,392 vertices | 6.1 ms and 2.4 mJ per query, chip below 0.5 W (on-chip current sensors) | [Dijkstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) on one core of an M1 Pro: 6.8 ms, 25.5 mJ, about 4 W (whole M1 Pro). On German road networks SpiNNaker2 is about 10× slower | not stated | von Seeler et al. 2026 (preprint, Göttingen) |
| Optimisation: Ising machine (NeuroSA) for [Max-Cut](https://en.wikipedia.org/wiki/Maximum_cut), annealing with spiking neurons | chip power 561.9 mW at 300 MHz. Solutions similar to or better than the CPU version on some Gset graphs, but slower in absolute time | laptop CPU (Intel Core Ultra 9): system 15.93 W, of which "CPU core" 11.63 W; scaled linearly to 300 MHz by the authors: 1.39 W | CPU version public, SpiNNaker2 version on request | Chen et al. 2025, Nature Communications, supplement S5 |
| Non-spiking DNN inference, PyTorch → ONNX → INT8 → chip (OctopuScheduler) | MNIST network 784–512–256–16, called a "dummy model" by the authors: 98.34 % on chip, 688 µs per inference at batch size 1, host transfers excluded, at most 8 PEs | none, no energy measured | not stated | Jobst et al. 2025 (preprint) |

The reinforcement learning table in the paper says "for one episode", but the numbers fit one inference step: 0.335 W × 0.020 s = 0.0067 J, while an episode of 200 steps at 10 ms lasts 2 s. The paper calls the chip's value "dynamic power"; whether the baseline power of the chip is included is not stated. It ran on a single-chip test board; on the HPI frame every run takes about a minute because the board is booted each time (`02_workshop_design/02_participant_access.md`), so a closed loop with one run per step would not work there.

**Energy wins at batch size 1, often with longer run times.**

- **Language model:** 18× less energy, but 8.6× longer. The language model only fitted on one chip at batch size 1. In the same paper, an EGRU on DVS Gesture needs 2.9× less energy than the A100 at batch size 1, while at batch size 6 the A100 needs half as much (only these two batch sizes were measured; `02_hardware_energy.md`, section 8). The paper doesn't say whether one inference is one token or one sequence, nor how power was measured on either side.
- **On-chip training:** estimated here from power × time, about 27 mJ against 89 mJ per step, so about 3.3× less energy and 9× slower. The paper itself reports only power, compares the GPU card alone with the chip's "full-system" value, and calls its efficiency result preliminary.
- **Ising machine:** the factors are power ratios, not energy: 28× against the whole CPU system, 21× against the CPU core power, 2.5× against the core power scaled linearly to 300 MHz (which ignores voltage). The authors report lower energy to solution for SpiNNaker2 at both system and processor level, with values only in a figure (supplement, Fig. S3c).
- **Graph search:** lower energy in all evaluated cases, faster on some graph types (random graphs about 25 %), slower on others (3D grids up to 2×, road networks about 10×). The baseline is sequential Dijkstra on one CPU core against 152 cores in parallel, which the authors themselves say "may seem unfair".

**What else matters for an ML audience.**

- **Memory, not arithmetic, limits the chip.** In the DNN inference, the MAC array computes during only 9 % of the first layer's run time; the rest is spent loading weights from DRAM (Jobst et al. 2025). The language model is also dominated by memory access (Nazeer et al. 2024). Several networks were shrunk to fit into the SRAM of the PEs (EventProp: 5–120–3; DVS Gesture: 25,500 parameters, only 10 % of each gesture).
- **Hand tuning is needed.** The DVS Gesture network needed neurons per PE set by hand, the reinforcement learning network thresholds re-tuned by a grid search on the chip after quantisation.
- **Most results use custom on-chip code.** Graph search, EventProp, the language model and the DNN scheduler run their own programs on the PEs rather than the neuron models of py-spinnaker2. Only the reinforcement learning and DVS Gesture work use the standard py-spinnaker2 workflow.
- **Authors:** almost all papers come from the group at TU Dresden where the chip was developed; in the NeuroSA paper several co-authors declare financial interests in SpiNNcloud.

**Older results on prototypes.** Yan et al. 2021 compared the second SpiNNaker2 prototype (8 PEs, 22 nm, run at 0.5 V and 250 MHz) with Intel's Loihi 1, the only direct comparison with another neuromorphic chip found in the research:

| Task | SpiNNaker2 prototype | Loihi 1 | Caveat |
|---|---|---|---|
| Keyword spotting | 7.1 µJ per inference, 1,000 inferences/s | 37 µJ, 296 inferences/s | different networks: a DNN with ReLU on the MAC array against an SNN on Loihi; the 1,000/s is projected from cycle counts; the Loihi values come from another paper, with Loihi's x86 overhead removed (originally 270 µJ) |
| Adaptive robot control, same SNN on both | energy ratio 1 : 0.81 at 1 input dimension | 0.36 : 1 at 100 input dimensions | the MAC array pays off for many inputs |

All values are active energy, idle power subtracted. The authors call it "by far not a comprehensive comparison". Further prototype and FPGA results (e-prop, Rostami et al. 2022; radar gestures, Huang et al. 2022) are *(not checked yet)*.

**Workshop:** one slide with three or four rows of the table (reinforcement learning, language model, graph search), including the slower times. About 3 minutes.

### 2.2 Large installations and the multi-chip gap

| Installation | Chips | As stated in the source | Published results | Source |
|---|---|---|---|---|
| TU Dresden | about 35,000 | about 35,000 chips, about 5 million cores, running since April 2025 | none found; free academic access "planned" (Jimenez Siegert et al. 2026) | `02_hardware_energy.md`, section 5 |
| Leipzig University | about 4,320 | 656,640 cores, about 4,320 chips (vendor release, July 2025) | the drug-discovery project published a single-chip result (below) | BeBeez 2025 (repeating the vendor release) |
| Forschungszentrum Jülich, "JUBIS" | 4,320 | 90 boards with 48 chips, 656,640 cores, installed April 2026, project ESAB (2026–2028, EU regional fund and NRW), EUR 3.36 M | none yet | JSC ESAB project page, checked |
| UTSA "THOR" (USA), access by application | 2,688 (computed here) | 56 boards, installed August 2025; "roughly 400,000" PEs | none found | THOR news page, checked; UTSA 2026 |
| Sandia National Laboratories (USA) | 1,152 | 24 boards with 48 chips each | first random-walk heat-flow simulations, no numbers | The Next Platform 2025, checked |
| HPI | 288 | 6 boards with 48 chips each | — | `02_hardware_energy.md`, section 5 |
| GWDG Göttingen | 192 (computed here) | four 48-node boards, py-spinnaker2 in a container, access via KISSKI and NHR | graph search (single chip, section 2.1); a bachelor's thesis on one board (below) | GWDG docs, checked; Göttingen thesis 2026 |

Leipzig and Jülich have the same size, 90 boards; this is not a mix-up of the two systems: the Leipzig figure was published in July 2025, before the Jülich contract of February 2026. Chips computed here assume 48 chips per board. The vendor's claims for Jülich (18× less energy for event-driven ML, 10× faster sparse solvers, faster optimisation) are single-board benchmarks against an H100 or CPUs, according to a quote of the vendor's CEO; the workloads are not published *(press quote, not checked against a primary source)*.

**No published result uses more than one chip.** About 40,000 SpiNNaker2 chips are installed, but a web research of 2026-11-05 found no paper, preprint or lab report with results measured on more than one chip of any of these systems (raw report in `_local/`, not tracked). The vendor's own chip paper says so: "While the focus in this paper was on single-chip results …", and of the Dresden system, "The software stack for large-scale deployment on this system is currently under development" (Scholze et al. 2026, checked). Examples:

- The Leipzig drug-discovery project screened 19 billion molecules on a single chip: inference about 4× faster and about 86 % less energy than an NVIDIA Jetson Orin Nano (Jimenez Siegert et al. 2026, Communications Chemistry, abstract checked).
- The only multi-chip work found is a bachelor's thesis at GWDG: ant colony optimisation on one full 48-chip board, where direct communication between chips "did not work at all" and the host relayed the data (Göttingen thesis 2026, existence checked, content from the research report).
- Graph search and a radio-burst detection pipeline extrapolate from one chip to boards without running on them (von Seeler et al. 2026; Magro 2026, preprint).

Reasons given in the sources: the software for large systems is still under development, py-spinnaker2 v0.8 runs a network on at most one board (`02_hardware_energy.md`, section 5), researchers had access to single chips only, and the systems are new (2025–2026). That the gap is mainly one of software and access, plus the delay before results are published, is an interpretation *(assumption, to check)*. For the workshop it means that one HPI board (7,104 cores) is already larger than the hardware used in nearly all published SpiNNaker2 work.

## 3. SpiNNaker1 highlights

These ran on the first SpiNNaker generation (18 cores per chip) with other software (sPyNNaker, PyNN), not with py-spinnaker2.

- **Brain simulation in real time:** a model of 1 mm² of cortex (77,000 neurons, 0.3 billion synapses) ran 10 s of biological time in 10 s, while HPC simulators needed 3× and GPUs 2× longer, with 10× less energy than the HPC systems and similar energy to GPUs (Rhodes et al. 2020, abstract, checked).
- **Robotics:** a mobile robot with event-based sensors, closed loop on SpiNNaker (Galluppi et al. 2014) *(not checked yet)*.
- **The million-core machine** in Manchester, open through EBRAINS (`02_hardware_energy.md`).

**Workshop:** at most one line in the history part.

## 4. Neuromorphic computing across platforms

### 4.1 Where measured advantages exist

| Domain | Example | Result | Source |
|---|---|---|---|
| Always-on audio, [keyword spotting](https://en.wikipedia.org/wiki/Keyword_spotting) | SynSense Xylo Audio 2 | 291 µW, 6.6 µJ per inference, 95 % accuracy | Bos & Muir 2024 (preprint), checked |
| Event vision | SynSense Speck (chip with integrated event camera) | 0.42 mW at rest, from 0.70 mW in operation | Yao et al. 2024, Nature Communications, checked |
| Streaming sequences, one token at a time | [State space model](https://en.wikipedia.org/wiki/State-space_representation) S4D on Intel Loihi 2 | 1000× less energy, 75× lower latency than a Jetson Orin Nano; the Jetson wins in batched processing | Meyer et al. 2024 (preprint), checked |
| Small language model | 370M-parameter model on Loihi 2 | up to 3× throughput, 2× less energy than a transformer on an unnamed edge GPU, preliminary | Abreu et al. 2025 (preprint), checked |
| Optimisation, graph search | Loihi survey | large gains for optimisation and graph search, little benefit for feedforward DNNs *(not checked yet)* | Davies et al. 2021, Proc. IEEE |

The advantage for sensors is absolute power in the microwatt to milliwatt range. Their competitors are small microcontrollers and DSPs, not GPUs.

### 4.2 Where conventional hardware wins

- **Dense deep learning with large batches.** No platform shows measured wins there. Meyer et al. 2024 and Nazeer et al. 2024 both report the GPU winning once it processes several inputs at once (Nazeer et al.: on DVS Gesture at batch size 6).
- **Low activity is required.** Compared with an optimised ANN accelerator, a spiking network only matches it at 0.15–1.38 spikes per synapse per inference (Dampfhoffer et al. 2023, abstract, checked). Compared with a quantised ANN of the same capacity, a spiking network with 5 time steps needs a spike rate below 5.7 % to win (Yan, Bai et al. 2024, preprint, checked). Both papers find that memory access, not arithmetic, dominates the energy; many earlier comparisons counted only operations.
- **Benchmark practice.** Many results compare against an unnamed GPU, at batch size 1 only, across manufacturing processes, or chip power against board power. The Ising result in section 2.1 shows how much the baseline matters. NeuroBench (Yik et al. 2025) is a community benchmark framework to make such comparisons fair.

### 4.3 Software

- **Training converges on PyTorch-style libraries plus NIR.** NIR lists snnTorch, Norse, Rockpool (Xylo), Sinabs (Speck), hxtorch (BrainScaleS-2), Lava-DL (Loihi) and SpiNNaker2 (NIR repository, checked). py-spinnaker2 reads NIR but doesn't write it.
- **Deployment stays vendor-specific.** Intel archived its Loihi framework Lava on 13 May 2026 (GitHub, checked).

### 4.4 Industry

- Commercial products are small edge chips (SynSense, BrainChip, Innatera) and event cameras; large systems go to research labs (Sandia, TU Dresden, Jülich).
- The vendors of large systems now advertise sparsity and AI inference rather than "neuromorphic". SpiNNcloud renamed itself Sparxity on 28 October 2026 and targets "hyperscalers, neoclouds and cloud providers" and model builders (sparxity.ai, checked; Silicon Saxony 2026). The website's factors (30× and 44× more tokens per second per user) name no baseline.

**Workshop:** one slide "where neuromorphic wins, where it doesn't" from 4.1 and 4.2, and the warning about advertised factors. Together with section 2, about 5 minutes of the motivation block.

## 5. Consequences for the workshop

- **Motivation:** be honest about the trade. The energy gains are real, but at batch size 1 and often with longer run times. This matches the HPI measurement: small networks are invisible in the board power (`05_measurements/01_power_baseline/`).
- **Demo candidates** from this research, to be evaluated on cx51:
  1. the official QUBO Max-Cut example of py-spinnaker2, with NeuroSA and the graph search as published context;
  2. the official NMNIST/NIR example, with the DVS Gesture paper as "a real paper does exactly this";
  3. the CartPole reinforcement learning (Arfa et al. 2025), the most engaging for ML people, only if the authors grant access to the private repository and the code runs with v0.8 on the frame;
  4. the official streaming pipeline, to show how a closed loop works.
- **Access elsewhere:** GWDG Göttingen offers SpiNNaker2 access with py-spinnaker2, relevant for participants after the workshop and for the contact with KISSKI.

## To check

- [x] Whether the CartPole code (`gitlab.com/Sirine_Arfa/interactive-reinforcement-learning-on-spinnaker2`) is public: no, private (checked 2026-11-04). Access requested from the first author by email, no answer as of 2026-11-05.
- [ ] Whether the CartPole code runs with py-spinnaker2 v0.8.2 on the frame, and how its closed loop is implemented (one run per step or streaming).
- [ ] Which py-spinnaker2 and NIR versions the DVS Gesture code needs (the web research found unreleased branches in its repository; the paper doesn't say).
- [x] OctopuScheduler numbers and Yan et al. 2021: checked in full text on 2026-11-05.
- [ ] Rostami et al. 2022, Huang et al. 2022, a primary source for the Leipzig size, how external users get access to the Dresden system, Galluppi et al. 2014, and the Davies et al. 2021 statement on feedforward DNNs: check in the papers.
- [ ] NeuroSA energy to solution: values only in supplement Fig. S3c.
- [ ] Whether the vendor's "18× for event-driven ML" (Jülich) is the EGRU result of Nazeer et al. 2024 (also open in `02_hardware_energy.md`).
- [ ] What the GWDG access currently offers (number of boards, who can use it).
