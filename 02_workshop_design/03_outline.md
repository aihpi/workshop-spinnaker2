# Workshop Outline

Draft of 2026-11-09 for the first date (18 November 2026, 14:00–17:00, H-2.57/58); the second date (9 December, 10:00–13:00) follows the same outline. Language: English. Supersedes the draft time budget in `brief.md`. Based on the demo ranking in `01_knowledge_base/04_applications.md`, section 5.

## Contents

- [Principles](#principles)
- [Schedule](#schedule)
- [Blocks](#blocks)
- [Chip time](#chip-time)
- [Coverage of the announcement](#coverage-of-the-announcement)
- [Dependencies](#dependencies)
- [Open points](#open-points)

## Principles

- **Theory just in time:** every hands-on follows directly on the theory it needs.
- **From simple to ML:** a hand-built network first, so participants know what the NIR import produces; then the bridge from PyTorch to the chip.
- **Brian2 for development, chip at the end:** every hands-on notebook runs on Brian2 by default; HPI participants switch to the chip for one final run. Outside participants stay on Brian2 (`02_participant_access.md`).
- **Pairs:** participants work in pairs, which halves the chip runs.
- **Honest about energy:** small networks are invisible in the board power (`05_measurements/01_power_baseline/`); energy is shown with a large network in an instructor demo, not promised for participants' own networks.

## Schedule

| Time | Min | # | Block | Type |
|---|---|---|---|---|
| 14:00 | 5 | 0 | Welcome and setup check | organisation |
| 14:05 | 15 | 1 | Motivation: why neuromorphic computing | theory |
| 14:20 | 20 | 2 | Spiking neural networks | theory |
| 14:40 | 15 | 3 | SpiNNaker2 hardware | theory |
| 14:55 | 35 | 4 | Hands-on 1: a first network | hands-on |
| 15:30 | 15 | – | Break (instructor starts the energy runs) | |
| 15:45 | 10 | 5 | From PyTorch to the chip | theory |
| 15:55 | 40 | 6 | Hands-on 2: NIR | hands-on |
| 16:35 | 10 | 7 | Instructor demos: energy, event-camera digits, Max-Cut | demo |
| 16:45 | 15 | 8 | Applications, an honest take, Q&A | theory and discussion |
| 17:00 | | | End | |

In total: theory 75 min, hands-on 75 min, demos 10 min, break 15 min, setup 5 min.

## Blocks

### 0. Welcome and setup check (5 min)

- Goal: every pair has a working environment before the first hands-on.
- HPI participants open the environment on cx51, outside participants their local Brian2 environment; everyone runs a test cell (imports, one tiny Brian2 run, about 10 s).
- Problems are collected and solved during the theory blocks by a second person, if available.

### 1. Motivation: why neuromorphic computing (15 min)

- The energy problem of AI hardware; the brain at about 20 W, with communication costing more than computation (`05_history.md`).
- Three slides of history: Mead's analog chips, the big programmes (TrueNorth, Human Brain Project, Loihi), SpiNNaker from Furber's idea to SpiNNaker2 (`05_history.md`).
- The core idea: neurons communicate with spikes and stay silent in between; sparse activity saves energy.
- Preview: energy gains exist, but under specific conditions; block 8 comes back to this.

### 2. Spiking neural networks (20 min)

- The LIF neuron: integrate, leak, fire, reset; discrete time steps as on the chip (primer, sections 2–3).
- Synapses, weights, spike trains, Poisson input, raster plots.
- **Comparison with deep learning:** an LIF layer is a recurrent cell with binary output; spikes instead of activations; why sparsity matters (primer, section 8; `04_applications.md`, section 4.2).
- Just enough to build the network in hands-on 1.

### 3. SpiNNaker2 hardware (15 min)

- Chip: 152 ARM cores, local SRAM, accelerators; neurons are software, so any model can run (`02_hardware_energy.md`; tutorial 09 as an outlook).
- From chip to board to frame: the HPI frame with 6 boards of 48 chips.
- What happens during a run: board reservation, power-up and boot, about one minute per run regardless of network size; why development happens on Brian2 (`02_participant_access.md`, capacity).
- Brian2 as the simulator behind the same Python code (`03_brian2_fallback.md`).

### 4. Hands-on 1: a first network (35 min)

- Notebook `04_workshop_material/01_first_network.ipynb`, a short path through the vendor's deep-dive tutorials 00–02; every section points to the tutorial section and API docs it draws on.
- One neuron with constant input (input–output curve vs. activation function), one neuron driven by input spikes (leak, timing), then a synfire chain of 5 groups of 50 `lif` neurons: a volley that sharpens from group to group.
- Exercises change one argument of `run_chain` (weight, input jitter, leak, threshold): the wave dies out or the synaptic events double; discussion questions on coincidence detection and on energy growing with synaptic events.
- Last 5 minutes: HPI pairs run the synfire chain on the chip and compare with Brian2 (identical spikes, tested on 2026-11-09).
- Chip runs: 1 per HPI pair.

### 5. From PyTorch to the chip (10 min)

- Training spiking networks: surrogate gradients in two slides (primer, section 8).
- NIR as an exchange format, "ONNX for spiking networks".
- The conversion rule for snnTorch models: `cfg.dt = 1e-4`, `FORWARD` integrator, matching reset rule, one-step delay per projection (primer, section 8).

### 6. Hands-on 2: NIR (40 min)

- **Part a (15 min), based on tutorial 08:** a small snnTorch network, exported to NIR, converted, run on Brian2; spike-for-spike comparison with snnTorch.
- **Part b (25 min), based on the end-to-end NIR example:** train a network in snnTorch to reproduce a logo spike pattern (about 3 min on the CPU of cx51, laptops to be tested), export, check on Brian2; HPI pairs run it on the chip.
- To mention: the example trains each time step independently, for simplicity.
- Chip runs: 1 per HPI pair (part b), part a optional.

### 7. Instructor demos (10 min)

- **Energy:** results of the runs started in the break, a silent and an active network on 1,000 cores (measured on 2026-10-19: 57 W empty board, 60 W silent, 66 W active). Message: small networks are invisible, the board costs 57 W just for being on, spiking activity is what costs energy. Backup: the measured curves.
- **Event-camera digits (NMNIST):** a pretrained convolutional spiking network, one sample live on the chip, connecting to the DVS Gesture paper.
- **Max-Cut:** the vendor's QUBO example on the 5- and 8-node graphs, with the 8-node bug fixed: spiking neurons with noise search for the best cut of a graph, so the chip does more than neural networks. Connects to the Ising-machine and graph-search papers (`04_applications.md`, section 2.1). The larger graphs are left out, they give random results.

### 8. Applications, an honest take, Q&A (15 min)

- What SpiNNaker2 is used for: published results run on single chips, energy gains at batch size 1, often with longer run times; about 40,000 chips installed, no published multi-chip result (`04_applications.md`, section 2).
- Where neuromorphic hardware wins and where it doesn't; vendors moving from "brain-like" to "sparse AI" (`04_applications.md`, section 4).
- Outlook: live streaming and custom neuron models, one slide each at most.
- How to get access to SpiNNaker2 chips after the workshop (HPI cluster, GWDG Göttingen via KISSKI/NHR).
- Take-home: sparsity, event-driven processing, quantisation, NIR, and asking for baseline and batch size behind every energy factor.

## Chip time

- Per HPI pair: 2–3 chip runs in total (hands-on 1, hands-on 2 part b, optionally part a).
- Instructor: 2 energy runs in the break; 1–2 NMNIST runs and 2 Max-Cut runs started at the end of hands-on 2, so the results are ready for block 7.
- The frame handles about 2 runs per minute for everyone together, and each run takes about one minute (`02_participant_access.md`). Even 10 HPI pairs starting at the same time would wait about 5 minutes; staggered starts at the end of each hands-on avoid this.
- If the frame fails, everyone continues on Brian2; the energy and NMNIST demos fall back to measured curves and recorded results.

## Coverage of the announcement

| Promise | Block |
|---|---|
| Basic ideas of spiking neural networks | 2 |
| Why neuromorphic hardware can save energy | 1, 3, 7 |
| Participants write their own networks in Python | 4, 6 |
| Run them on the SpiNNaker2 chips at HPI | 4, 6 for HPI participants; outside participants stay on Brian2 and get access instructions in block 8 |
| Comparison with deep learning | 2, 5, 8 |
| Potential of neuromorphic computing | 8 |
| Code to keep working with afterwards | the hands-on notebooks |

## Dependencies

Tracked in `_local/00_todos_workshop.md`:

- hands-on 1 notebook (new), hands-on 2 notebooks (adapted from the vendor's examples)
- Brian2 install guide for outside participants, and torch with snnTorch in the environment on cx51
- slides for blocks 1–3, 5 and 8
- energy demo script and NMNIST demo prepared
- mail to registered participants
- dry run on cx51 and on a laptop

## Open points

- [x] Maximum number of participants: 20 (decided 2026-11-09), i.e. 10 pairs.
- [ ] Whether a second person helps with setup problems and questions during the hands-on.
- [ ] Training time of the end-to-end NIR example on participants' laptops.
- [x] Max-Cut: live instructor demo in block 7 with the 5- and 8-node graphs (decided 2026-11-09).
