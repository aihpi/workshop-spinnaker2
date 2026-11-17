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
| 14:00 | 15 | 1 | Welcome and motivation: why neuromorphic computing | theory |
| 14:15 | 5 | 2 | Setup check | organisation |
| 14:20 | 35 | 3 + 4 | Spiking neural networks, interleaved with hands-on 1 (one neuron, input spikes): slides 12 min, notebook 01 15 min, debrief slides 6 min | theory and hands-on |
| 14:55 | 15 | 5 | SpiNNaker2 hardware | theory |
| 15:10 | 20 | 6 | Hands-on 2: direction detector, chip run | hands-on |
| 15:30 | 15 | – | Break (instructor starts the energy runs) | |
| 15:45 | 10 | 7 | From PyTorch to the chip | theory |
| 15:55 | 40 | 8 | Hands-on 3: the direction task, trained and run via NIR | hands-on |
| 16:35 | 10 | 9 | Instructor demos: energy, event-camera digits, Max-Cut | demo |
| 16:45 | 15 | 10 | Applications, an honest take, Q&A | theory and discussion |
| 17:00 | | | End | |

In total: theory 75 min, hands-on 75 min, demos 10 min, break 15 min, setup 5 min.

## Blocks

### 1. Welcome and motivation: why neuromorphic computing (15 min)

- Welcome, agenda; whoever hasn't installed the environment starts the install now (5 to 15 min, see block 2).
- The energy problem of AI hardware; the brain at about 20 W, with communication costing more than computation (`05_history.md`).
- Three slides of history: Mead's analog chips, the big programmes (TrueNorth, Human Brain Project, Loihi), SpiNNaker from Furber's idea to SpiNNaker2 (`05_history.md`).
- The core idea: neurons communicate with spikes and stay silent in between; sparse activity saves energy.
- Preview: energy gains exist, but under specific conditions; block 10 comes back to this.

### 2. Setup check (5 min)

- After block 1, so that problems can be fixed during block 3 and before hands-on 1.
- Goal: every pair has a working environment before the first hands-on. Installing should happen beforehand (participant mail, install guide), but is also possible in the room: a fresh install takes 5 to 15 min and downloads about 0.5 GB (README on `main`), so whoever hasn't installed starts at 14:00, and it finishes during block 1. HPI participants on cx51 need no install.
- HPI participants open the environment on cx51, outside participants their local Brian2 environment; everyone runs `00_setup_check.ipynb` (imports, one tiny Brian2 run, about 10 s).
- Pairs form now: one working laptop per pair is enough.
- Problems are collected and solved during block 3 by a second person, if available.

### 3 + 4. Spiking neural networks, interleaved with hands-on 1 (35 min)

Decided 2026-11-16: blocks 3 and 4 are interleaved. The slides explain what participants need before they can try anything; what they can find out by changing parameters is left to notebook 01; a short debrief collects it. Slide content in `05_slide_content_part1.md`, block 3.

- Slides before the notebook (about 12 min): from the biological neuron to LIF (Hodgkin-Huxley, FitzHugh-Nagumo, LIF; optional, with an optional detour on the FitzHugh-Nagumo equations), the artificial neuron next to the spiking neuron (refresher), the LIF neuron (integrate, leak, fire, reset), the update rule in discrete time as a map of the parameters, synapses with weight and delay (primer, sections 2–4).
- Notebook `04_workshop_material/01_single_neuron.ipynb` (about 15 min), Brian2 only: one neuron with constant input (critical input, input–output curve vs. activation function), one neuron driven by input spikes (leak, timing, delays, clipping). The notebook ends with a pointer back to the slides.
- Debrief slides after the notebook (about 6 min): what participants found (critical input and the ReLU-like curve; spikes that arrive together fire the neuron), weights as small integers (quantisation), the bridge to the hardware block.

### 5. SpiNNaker2 hardware (15 min)

- Between hands-on 1 and 2: answers "where does this run?" after participants have run their first neurons, and prepares the energy discussion and the chip run of hands-on 2.
- Chip: 152 ARM cores, local SRAM, accelerators; neurons are software, so any model can run (`02_hardware_energy.md`).
- From chip to board to frame: the HPI frame with 6 boards of 48 chips.
- Why weights are small integers: one synapse is one 16-bit word in the PE's memory (primer, section 4).
- Moved on 2026-11-16: the time per chip run and Brian2 for development to the hands-on slide of block 6; the energy cost of a run to blocks 9 and 10.

### 6. Hands-on 2: direction detector, chip run (20 min)

- Notebook `02_direction_detector.ipynb`: a dot moves across four pixels; two `lif` detectors, written as a weight matrix and a delay matrix, tell its direction by coincidence detection. Participants fill in the delays of the leftward detector.
- Chip run as soon as the network works (section 4, before the Try items): HPI pairs run the detector on the chip, compare the answer with Brian2 and read `time_done` (how busy the PE was per step). Pairs reach this point at different times, so the runs spread over the 6 boards.
- Exercises (section 5): a slower dot, a missing pixel, a lower threshold, a third detector for slow dots; discussion on where the direction information lies (timing, not which pixels fired).
- The API reference of notebook 01 is a collapsible in notebook 02, not part of the exercise time.
- Chip runs: 1 per HPI pair. The synfire-chain notebook is archived (`04_workshop_material/archive/`).

### 7. From PyTorch to the chip (10 min)

- An LIF layer is a recurrent cell with binary output, as the opening (primer, section 8; moved here from block 3 on 2026-11-16).
- Training spiking networks: surrogate gradients in two slides (primer, section 8).
- NIR as an exchange format, "ONNX for spiking networks".
- The conversion rule for snnTorch models: `cfg.dt = 1e-4`, `FORWARD` integrator, matching reset rule, one-step delay per projection (primer, section 8).

### 8. Hands-on 3: the direction task, trained and run via NIR (40 min)

- **Notebook `03_direction_nir.ipynb` (about 12 min), adapted in parts from tutorial 08:** the four-pixel task of notebook 02, trained in snnTorch (a few seconds), exported to NIR and converted with the rule for snnTorch models (`dt = 1e-4`, `FORWARD`, the right reset); the converted network has integer weights and fires exactly the same spikes as snnTorch, shifted by one step per projection. No exercises in the workshop part: participants run and read. A marked section "After the workshop" holds breaking the conversion on purpose, how the trained network tells the direction without delays (inhibition as a veto), and a chip run.
- **Notebook `04_direction_trained.ipynb` (about 17 min):** a bar moving across an 8 × 8 event camera, four directions, three speeds, noise and lost events; training about half a minute, test accuracy per direction and speed, wrong examples as animations, NIR conversion on Brian2, weight images and hidden activity per direction, chip run. One Try (a strong leak, `beta = 0.3`), one Discuss (training off the chip, inference on it); further Try items under "If you want more".
- About 10 min buffer.
- Chip runs: 1 per HPI pair (notebook 04).
- The old notebooks `03_nir_minimal.ipynb` and `04_nir_end_to_end.ipynb` are archived in `04_workshop_material/archive/`.

### 9. Instructor demos (10 min)

- **Energy:** results of the runs started in the break, a silent and an active network on 1,000 cores (measured on 2026-10-19: 57 W empty board, 60 W silent, 66 W active). Message: small networks are invisible, the board costs 57 W just for being on, spiking activity is what costs energy. Backup: the measured curves.
- **Event-camera digits (NMNIST):** a pretrained convolutional spiking network, one sample live on the chip, connecting to the DVS Gesture paper.
- **Max-Cut:** the vendor's QUBO example on the 5- and 8-node graphs, with the 8-node bug fixed: spiking neurons with noise search for the best cut of a graph, so the chip does more than neural networks. Connects to the Ising-machine and graph-search papers (`04_applications.md`, section 2.1). The larger graphs are left out, they give random results.

### 10. Applications, an honest take, Q&A (15 min)

- What SpiNNaker2 is used for: published results run on single chips, energy gains at batch size 1, often with longer run times; about 40,000 chips installed, no published multi-chip result (`04_applications.md`, section 2).
- Where neuromorphic hardware wins and where it doesn't; vendors moving from "brain-like" to "sparse AI" (`04_applications.md`, section 4).
- Outlook: live streaming and custom neuron models, one slide each at most.
- How to get access to SpiNNaker2 chips after the workshop (HPI cluster, GWDG Göttingen via KISSKI/NHR).
- Take-home: sparsity, event-driven processing, quantisation, NIR, and asking for baseline and batch size behind every energy factor.

## Chip time

- Per HPI pair: 2–3 chip runs in total (notebooks 02 and 04, optionally 03).
- Instructor: 2 energy runs in the break; 1–2 NMNIST runs and 2 Max-Cut runs started at the end of hands-on 3, so the results are ready for block 9.
- The frame handles about 2 runs per minute for everyone together, and each run takes about one minute (`02_participant_access.md`). Even 10 HPI pairs starting at the same time would wait about 5 minutes; staggered starts at the end of each hands-on avoid this.
- If the frame fails, everyone continues on Brian2; the energy and NMNIST demos fall back to measured curves and recorded results.

## Coverage of the announcement

| Promise | Block |
|---|---|
| Basic ideas of spiking neural networks | 3 |
| Why neuromorphic hardware can save energy | 1, 5, 9 |
| Participants write their own networks in Python | 4, 6, 8 |
| Run them on the SpiNNaker2 chips at HPI | 6, 8 for HPI participants; outside participants stay on Brian2 and get access instructions in block 10 |
| Comparison with deep learning | 3, 7, 10 |
| Potential of neuromorphic computing | 10 |
| Code to keep working with afterwards | the hands-on notebooks |

## Dependencies

Tracked in `_local/00_todos_workshop.md`:

- notebooks 01 and 02 (new), notebooks 03 and 04 (adapted from the vendor's examples)
- Brian2 install guide for outside participants, and torch with snnTorch in the environment on cx51
- slides for blocks 1–3, 5, 7, 9 and 10 (plan: `04_slide_plan.md`)
- energy demo script and NMNIST demo prepared
- mail to registered participants
- dry run on cx51 and on a laptop

## Open points

- [x] Maximum number of participants: 20 (decided 2026-11-09), i.e. 10 pairs.
- [ ] Whether a second person helps with setup problems and questions during the hands-on.
- [ ] Training time of the end-to-end NIR example on participants' laptops.
- [x] Max-Cut: live instructor demo in block 9 with the 5- and 8-node graphs (decided 2026-11-09).
