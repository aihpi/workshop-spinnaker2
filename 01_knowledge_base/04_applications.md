# Applications of SpiNNaker2 and Neuromorphic Computing

What SpiNNaker2 and other neuromorphic chips have actually been used for, with measured results, and where they don't beat conventional hardware. Material for the motivation part of the workshop and for choosing demos. Builds on `02_hardware_energy.md` (chip, energy, the "18×" claim) and `01_primer_snn_basics.md` (sparsity, event-driven computing).

Status 2026-11-04. Based on two web researches of that day (raw reports in `_local/`, not tracked). The numbers marked as checked were compared with the text of the paper on 2026-11-04; everything else is marked *(not checked yet)* and listed under [To check](#to-check).

## Contents

- [1. Summary](#1-summary)
- [2. Applications on SpiNNaker2](#2-applications-on-spinnaker2)
  - [2.1 Published results](#21-published-results)
  - [2.2 Large installations](#22-large-installations)
- [3. SpiNNaker1 highlights](#3-spinnaker1-highlights)
- [4. Neuromorphic computing across platforms](#4-neuromorphic-computing-across-platforms)
  - [4.1 Where measured advantages exist](#41-where-measured-advantages-exist)
  - [4.2 Where conventional hardware wins](#42-where-conventional-hardware-wins)
  - [4.3 Software](#43-software)
  - [4.4 Industry](#44-industry)
- [5. Consequences for the workshop](#5-consequences-for-the-workshop)
- [To check](#to-check)

## 1. Summary

- **Almost every published SpiNNaker2 result runs on one chip** on a test board, or on an older prototype. For 48-chip boards like the HPI ones, and for the large systems (TU Dresden, Sandia, Leipzig, Jülich), only press material exists, no measured application results.
- **The recurring pattern: less energy, often more time.** SpiNNaker2 needs about 3–30× less energy than the chosen baseline for single inputs (batch size 1), but is often slower, and a GPU that processes several inputs at once wins on both (section 2.1).
- **Across all platforms, the measured wins come from sparse data processed one input at a time:** always-on sensors, event cameras, streaming sequences. On dense deep learning with large batches, no neuromorphic chip has measured wins (section 4).
- **Spiking networks only save energy at very low activity:** below about 6 % spike rate, or 0.15–1.4 spikes per synapse per inference, depending on the study (section 4.2).
- **Many advertised factors (18×, 78×, 1000×) come without baseline or batch size.** The vendor of SpiNNaker2 renamed itself from SpiNNcloud to Sparxity in October 2026 and now markets the chip for sparse AI inference rather than as neuromorphic hardware (section 4.4).

## 2. Applications on SpiNNaker2

### 2.1 Published results

All on the full SpiNNaker2 chip (152 processing elements, PEs), each on a single chip. The GPU numbers are the baselines chosen by the authors.

| Application | Result on SpiNNaker2 | Baseline | Code | Source |
|---|---|---|---|---|
| [Reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning): spiking Q-network controlling CartPole and Acrobot in a closed loop, 8-bit weights | CartPole: same reward (200), 0.006 J, 0.020 s, 0.335 W. Acrobot: reward −67, 0.010 J | GTX 1650: 0.145 J (24×), 0.0197 s, 7.39 W. Acrobot: reward −75, 0.321 J (32×) | linked in the paper (GitLab), but private (checked 2026-11-04); uses py-spinnaker2 and snnTorch | Arfa et al. 2025, ICONS, checked |
| Gesture recognition from an [event camera](https://en.wikipedia.org/wiki/Event_camera) (DVS Gesture), imported via NIR, 8-bit | 94.13 % accuracy on chip | 32-bit float on GPU (close match) | public (Apache-2.0), but needs unreleased branches of py-spinnaker2 and NIR | Arfa et al. 2025, NICE, checked |
| Language model, event-based GRU (EGRU), WikiText-2 | same perplexity (81.4), 0.065 J and 170 ms per inference, 0.39 W | A100: 1.19 J (18×), 19.9 ms (8.6× faster), 60 W | none | Nazeer et al. 2024, checked; details in `02_hardware_energy.md`, section 8 |
| On-chip training with event-based [backpropagation](https://en.wikipedia.org/wiki/Backpropagation) (EventProp), Yin-Yang dataset | 61 ms per training sample, 0.45 W | RTX 4070: 6.61 ms, 13.5 W (card only) | not found | Béna et al. 2025, NICE, checked |
| [Shortest path](https://en.wikipedia.org/wiki/Shortest_path_problem) search (NEURO-MAPP), 3D city graph with 38,392 vertices | 6.1 ms and 2.4 mJ per query, < 0.5 W | [Dijkstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) on an M1 Pro CPU: 25.5 mJ, about 4 W. On road networks SpiNNaker2 is about 10× slower | not found | von Seeler et al. 2026 (preprint, Göttingen), checked |
| Optimisation: Ising machine (NeuroSA) for [Max-Cut](https://en.wikipedia.org/wiki/Maximum_cut), annealing with spiking neurons | 561.9 mW, solutions similar to or better than the CPU's | CPU system 15.93 W; one CPU core scaled to the chip's 300 MHz would draw 1.39 W (the authors' estimate) | CPU version public, SpiNNaker2 version on request | Chen et al. 2025, Nature Communications, checked |
| Non-spiking DNN inference, PyTorch → INT8 → chip (OctopuScheduler) | MNIST network 98.34 %, 688 µs per inference *(not checked yet)* | — | not found | Jobst et al. 2025 (preprint) |

The reinforcement learning table in the paper says "for one episode", but the numbers fit one inference step: 0.335 W × 0.020 s = 0.0067 J, while an episode of 200 steps at 10 ms lasts 2 s. The paper calls the chip's value "dynamic power"; whether the baseline power of the chip is included is not stated. It ran on a single-chip test board; on the HPI frame every run takes about a minute because the board is booted each time (`02_workshop_design/02_participant_access.md`), so a closed loop with one run per step would not work there.

The pattern for an ML audience is in the language model row: at batch size 1, SpiNNaker2 needs 18× less energy but takes 8.6× longer. In the same paper, the A100 wins on both energy and time on DVS Gesture as soon as it processes 6 inputs at once (`02_hardware_energy.md`, section 8). The training row shows the same trade: about 3.3× less energy per sample (0.45 W × 61 ms against 13.5 W × 6.61 ms), but 9× slower. The Ising row shows how the choice of baseline changes the factor: 28× against the whole CPU system, 2.5× against one CPU core at the same clock.

Older results on prototype chips (4 or 8 PEs) or on an FPGA include keyword spotting compared with Intel's Loihi 1 (Yan et al. 2021), online learning with e-prop (Rostami et al. 2022) and a radar gesture demo (Huang et al. 2022) *(numbers not checked yet)*. The comparison with Loihi 1 is the only same-task comparison with another neuromorphic chip: Loihi was more efficient for small matrix operations, SpiNNaker2 for large ones, thanks to its MAC array (Yan et al. 2021, abstract, checked).

**Workshop:** one slide with three or four rows of the table (reinforcement learning, language model, graph search), including the slower times. About 3 minutes.

### 2.2 Large installations

| Installation | Size | Source |
|---|---|---|
| TU Dresden | about 35,000 chips, about 5 million cores | `02_hardware_energy.md`, section 5 |
| Sandia National Laboratories (USA) | 24 boards with 48 chips each | The Next Platform 2025, checked |
| Leipzig University | about 650,000 cores *(not checked yet)* | HPCwire 2025 |
| UTSA "THOR" (USA), open access for US researchers | about 400,000 PEs *(not checked yet)* | UTSA 2026 |
| Forschungszentrum Jülich, "JUBIS" | "multi-million" system, size not stated | Silicon Saxony 2026, checked |
| GWDG Göttingen | SpiNNaker2 access, "eventually 4 boards", py-spinnaker2 in a container | GWDG docs, checked |
| HPI | 6 boards with 48 chips each | `02_hardware_energy.md`, section 5 |

No measured application results from these systems were found, only planned uses (sparse solvers, optimisation, random walks, drug discovery). The vendor's claims for Jülich (18× less energy for event-driven ML, 10× faster sparse solvers, faster optimisation) name no baseline (Silicon Saxony 2026).

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

- **Dense deep learning with large batches.** No platform shows measured wins there. Meyer et al. 2024 and Nazeer et al. 2024 both report the GPU winning once it processes several inputs at once.
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

- [x] Whether the CartPole code (`gitlab.com/Sirine_Arfa/interactive-reinforcement-learning-on-spinnaker2`) is public: no, private (checked 2026-11-04). Access to be requested from the first author.
- [ ] Whether the CartPole code runs with py-spinnaker2 v0.8.2 on the frame, and how its closed loop is implemented (one run per step or streaming).
- [ ] Whether the DVFS branch that the DVS Gesture code needs is part of v0.8.
- [ ] OctopuScheduler numbers (98.34 %, 688 µs), the prototype results (Yan et al. 2021, Rostami et al. 2022, Huang et al. 2022), Leipzig and THOR sizes, Galluppi et al. 2014, and the Davies et al. 2021 statement on feedforward DNNs: check in the papers.
- [ ] NeuroSA energy to solution (only in the paper's figures).
- [ ] Whether the vendor's "18× for event-driven ML" (Jülich) is the EGRU result of Nazeer et al. 2024 (also open in `02_hardware_energy.md`).
- [ ] What the GWDG access currently offers (number of boards, who can use it).
