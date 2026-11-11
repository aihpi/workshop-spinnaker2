# Slide Plan

Draft of 2026-11-10. Distils `01_knowledge_base/` into the theory blocks of the outline (`03_outline.md`): what goes on the slides, what the notebooks cover, what stays in the knowledge base. Not the slides themselves; one line per slide, plus the content of the hands-on blocks in between, in the order of the afternoon.

Abbreviations for figures: **P** = `01_primer_snn_basics.md`, **H** = `02_hardware_energy.md`, **C** = `00_computing_fundamentals.md`, **M** = `05_measurements/01_power_baseline/`. "P 6" means Figure 6 of the primer.

## Contents

- [Principles](#principles)
- [Block 1: Motivation (15 min)](#block-1-motivation-15-min)
- [Block 2: Setup check (5 min)](#block-2-setup-check-5-min)
- [Block 3: Spiking neural networks (20 min)](#block-3-spiking-neural-networks-20-min)
- [Block 4: Hands-on 1, one neuron and input spikes (15 min)](#block-4-hands-on-1-one-neuron-and-input-spikes-15-min)
- [Block 5: SpiNNaker2 hardware (15 min)](#block-5-spinnaker2-hardware-15-min)
- [Block 6: Hands-on 2, synfire chain and chip run (20 min)](#block-6-hands-on-2-synfire-chain-and-chip-run-20-min)
- [Block 7: From PyTorch to the chip (10 min)](#block-7-from-pytorch-to-the-chip-10-min)
- [Block 8: Hands-on 3, NIR (40 min)](#block-8-hands-on-3-nir-40-min)
- [Block 9: Instructor demos (10 min)](#block-9-instructor-demos-10-min)
- [Block 10: Applications, an honest take (15 min)](#block-10-applications-an-honest-take-15-min)
- [Split between slides and notebooks](#split-between-slides-and-notebooks)
- [Left out](#left-out)
- [New figures needed](#new-figures-needed)
- [Open questions](#open-questions)

## Principles

- **Slides give the idea, notebooks give the details.** A slide states what a concept is and why it matters; parameter values, edge cases and "why delay + 1" live in the notebooks (Try, Discuss, collapsibles).
- **Every slide prepares a hands-on or a demo.** Content that neither hands-on nor demo needs goes to the knowledge base.
- **About 2 minutes per slide:** about 33 slides for the theory blocks and demos.
- **One figure per slide**, except 5.1 (H 1, then H 2 as a zoom). Knowledge-base figures are reused; they still need restyling to the HPI slide design (`hpi-corporate-design`).
- **Order:** block 1 → 2 (setup check) → 3 (spiking networks) → 4 (hands-on 1) → 5 (hardware) → 6 (hands-on 2) → 7 (PyTorch to the chip) → 8 (hands-on 3) → 9 (demos) → 10 (applications). Participants apply the LIF model before the hardware explains where it runs.
- **Comparison with deep learning throughout:** the audience knows ReLU, RNNs, backprop, quantisation, ONNX; every new concept is anchored to one of these.

## Block 1: Motivation (15 min)

| # | Slide | Figure |
|---|---|---|
| 1.1 | Welcome, title, agenda, how the afternoon runs (theory → hands-on → demo, pairs, Brian2 and chip); **not installed yet? start the install now** (link to the install guide) | – |
| 1.2 | AI costs energy; the brain does with about 20 W | – (one number, one source) |
| 1.3 | Moving data costs more than computing on it | P 25 (energy per operation) |
| 1.4 | Von Neumann bottleneck vs. many cores with local memory | C 2 |
| 1.5 | The core idea: neurons send spikes and stay silent in between; work only when a spike arrives | P 5 (LIF spiking, as a teaser) |
| 1.6 | Timeline in five rows: 1990 Mead, 2014 TrueNorth, 2018 million-core SpiNNaker, 2024 Hala Point, 2026 Sparxity | – (table from `05_history.md`, section 1) |
| 1.7 | The promise and the catch: gains exist, under specific conditions; block 10 comes back to them | – |

## Block 2: Setup check (5 min)

After block 1, so that problems can be fixed while block 3 runs and before hands-on 1.

| # | Slide | Figure |
|---|---|---|
| 2.1 | Form pairs; open the environment (HPI: cx51; outside: local Brian2); run `00_setup_check.ipynb`; the expected plot; raise a hand if it fails | the plot of the setup notebook (output one step after each input) |

Participants run the three cells of `00_setup_check` (about 10 s): package versions, a tiny network on Brian2, the input/output plot. Installs started at 14:00 (slide 1.1) take about 12 min and are done by now. Failed setups are fixed by a second person during block 3, if available; a pair with one working laptop can continue.

## Block 3: Spiking neural networks (20 min)

| # | Slide | Figure |
|---|---|---|
Reduced to what block 5 and the hands-ons need: a neuron integrates, leaks, fires and resets; it advances in discrete time steps; connections carry an integer weight and a delay; an LIF layer is a recurrent cell (needed in block 7). About 12 min instead of 20.

| # | Slide | Figure |
|---|---|---|
| 3.1 | From the biological neuron to LIF: the simplest model that still spikes (brief motivation) | P 1 (HH, FHN, LIF) |
| 3.2 | LIF: integrate, leak, fire, reset | P 5 |
| 3.3 | LIF in discrete time, as the chip computes it: $v[t] = \alpha v[t-1] + I[t]$ | P 7 |
| 3.4 | Synapses: weight and delay; a spike arrives delay + 1 steps later | P 10 → notebook 01, section 2 |
| 3.5 | An LIF layer is a recurrent cell with binary output | P 22 |

Moved out of the slides: the input–output curve vs. ReLU (participants find it in notebook 01 §1, Try and Discuss), weight quantisation in detail (P 12; comes back in block 7 with the 8-bit NIR weights), rate vs. timing codes (P 17; at most a remark at the NMNIST demo), the synfire preview (introduced in notebook 02).

## Block 4: Hands-on 1, one neuron and input spikes (15 min)

Notebook `01_single_neuron`, Brian2 only. On screen: one slide with the task, the time and the notebook path.

| Section | Participants do | Take-away |
|---|---|---|
| 0. Setup | run the imports and the backend helper | the same `run(net, steps)` for Brian2 and the chip |
| 1. One neuron, constant input | predict before running: the smallest spiking input and the shape of the spike-count curve; then check | below a critical input nothing happens; above it, the spike count grows with the input, in small steps (discrete time) |
| 2. Input spikes, weights and delays | one cell with a "change these" block: spike times, one weight and one delay per input, leak; predict, then run | a spike adds its weight one step (plus delay) later; the leak makes the neuron forget; delays can make spikes coincide |

**Discuss (plenary, about 3 min):** spike count vs. input compared with ReLU (§1); why timing matters here but not in a deep network; what delays plus coincidence could detect (both §2).

The notebook ends with a pointer back to the slides.

## Block 5: SpiNNaker2 hardware (15 min)

Comes between hands-on 1 and 2. Reduced to what hands-on 2, the energy demo and block 10 need: many small cores with local memory, work only when spikes arrive, the scale from chip to system, and what a run means in practice. About 12 min.

| # | Slide | Figure |
|---|---|---|
| 5.1 | Where the chips are and how code reaches them; zoom into one chip: 152 ARM cores (PEs), each with 128 KB of local memory; neurons are software running on them; the path of one spike | H 1, then H 2 |
| 5.2 | What a PE does per time step: process incoming spikes, update neurons, idle; this is why spikes, not neurons, cost energy | H 4 |
| 5.3 | From chip to board to the 35,000-chip system; the HPI frame with 6 boards of 48 chips | H 7 |
| 5.4 | What happens during a run: compile, place, power up, boot; about one minute regardless of network size | C 5 |
| 5.5 | Brian2: the same Python code on a laptop; identical spikes for `lif`; why development happens there | – (short table from `03_brian2_fallback.md`) |

Moved out of the slides: neurons as software in detail (H 3; one sentence on 5.1, custom models return in block 10), multicast routing (H 6; H 2 shows the spike path, details in `02_hardware_energy.md` §4), local memory in detail (H 5; "128 KB per PE" on 5.1, the consequence for neurons per core in the 04 collapsible and `02_hardware_energy.md` §3 and §7).

## Block 6: Hands-on 2, synfire chain and chip run (20 min)

Notebook `02_synfire_chain`. On screen: the synfire sketch (see [New figures needed](#new-figures-needed)) and the task.

| Section | Participants do | Take-away |
|---|---|---|
| 0–1. Setup, synfire chain | run the baseline (5 groups × 50 neurons, the volley sharpens); then change one argument of `run_chain`: `weight=3`, `kick_spread=4`, `alpha_decay=0.5`, `threshold=20` | the wave dies out when inputs are too weak or not synchronous enough; a lower threshold doubles the synaptic events |
| 2. Recap | read | populations, projections, network, backend |
| 3. Chip run | HPI pairs set `USE_HARDWARE = True` (about one minute) | identical spikes on Brian2 and the chip |

**Discuss (plenary, about 4 min):** neurons as coincidence detectors (is the information in which neurons fire or when?); energy grows with synaptic events, not neurons, linked to slide 5.2 and the energy demo.

**Chip runs:** staggered, one per HPI pair, started in the last 5 minutes.

## Block 7: From PyTorch to the chip (10 min)

| # | Slide | Figure |
|---|---|---|
| 7.1 | Training spiking networks: the step function has no gradient | P 23, panels A–B |
| 7.2 | Surrogate gradients: step forward, smooth backward | P 23, panel C |
| 7.3 | NIR: an exchange format for spiking networks, like ONNX | – (list of frameworks and chips from the NIR paper) |
| 7.4 | The path: train → export → import → map → run | P 24 → notebooks 03 and 04 |
| 7.5 | The conversion rule for snnTorch models: `dt = 1e-4`, `FORWARD`, matching reset, one step per projection; why (03 shows what breaks otherwise) | – (code snippet) |

## Block 8: Hands-on 3, NIR (40 min)

### Notebook 03: from snnTorch to the chip, spike for spike (15 min)

Notebook `03_nir_minimal`, Brian2; chip optional.

| Section | Participants do | Take-away |
|---|---|---|
| 1–2 | define a tiny snnTorch network, run it, export it to NIR | NIR stores the graph, not the framework |
| 3–4 | set the conversion rule, convert, run on Brian2 | the rule from slide 7.5 in code |
| 5 | compare with snnTorch: identical spikes; then break the rule on purpose (default integrator, wrong reset, no shift) | wrong settings give a different network without an error message |

**Discuss:** which of these errors a spike-counting classifier would notice, and which only a spike-for-spike comparison.

### Notebook 04: train, export, run (25 min)

Notebook `04_nir_end_to_end`.

| Section | Participants do | Take-away |
|---|---|---|
| 1–2 | look at input (random spikes) and target (the SpiNNaker2 logo); read the network | 256 → 512 → 256 LIF neurons, learnable thresholds and decay |
| 3 | train (about 2–3 min on a CPU; start early, read meanwhile) | surrogate gradients at work (slides 7.1–7.2) |
| 4–5 | evaluate in snnTorch, export, run on Brian2; compare the three rasters | the logo appears; py-spinnaker2 is close but not exact (8-bit weights) |
| 6 | HPI pairs run on the chip | identical to Brian2 |

**Try:** train with fewer epochs; explain why 04, unlike 03, doesn't match snnTorch exactly.

**Discuss:** the training shortcut (no memory across time) and for which tasks it would fail.

**Chip runs:** one per HPI pair in part b, staggered; the instructor starts the NMNIST and Max-Cut runs at the end of this block.

## Block 9: Instructor demos (10 min)

| # | Slide | Figure |
|---|---|---|
| 9.1 | Energy: empty, silent and active board; small networks are invisible | live result of `demos/01_energy`, backup M `01_power_traces.png`, `02_power_vs_load.png` |
| 9.2 | Event-camera digits: a pretrained spiking CNN on NMNIST | live notebook `demos/02_nmnist` |
| 9.3 | Max-Cut: noisy spiking neurons search for the best cut of a graph | P 16, live notebook `demos/03_maxcut` |

## Block 10: Applications, an honest take (15 min)

| # | Slide | Figure |
|---|---|---|
| 10.1 | Published results on SpiNNaker2: all on one chip; about 40,000 chips installed | – (condensed table from `04_applications.md`, section 2.1) |
| 10.2 | Less energy, often more time; batch size decides | H 9 |
| 10.3 | When sparsity pays off (an estimate, labelled as such) | P 26 |
| 10.4 | Where neuromorphic hardware wins (sparse, streaming, batch size 1) and where it doesn't (dense, large batches) | – (`04_applications.md`, section 4) |
| 10.5 | Outlook: other neuron models, live input, custom models | P 13 or P 14, one at most |
| 10.6 | Access to SpiNNaker2 after the workshop | – |
| 10.7 | Take-home: sparsity, event-driven, quantisation, NIR; ask for baseline and batch size behind every energy factor | – |

## Split between slides and notebooks

| Topic | Slides | Notebook |
|---|---|---|
| LIF equation, $\alpha$, threshold | idea and discrete update (3.2–3.3) | parameter effects, collapsible on the derivation (01 §1) |
| Input–output curve vs. ReLU | not on slides | 01 §1, Try and Discuss |
| Reset modes | not on slides | 01 §1 and §2, 03 exercises |
| `alpha_decay` and memory | not on slides | 01 §1–2 |
| Delay + 1 | one sentence (3.4) | 01 §2, collapsible and exercise |
| Weight range | one line on 5.1 (128 KB per PE → packed synapses) | rule only in 01 §2; collapsible "why −15 to 15" in 02 §1 |
| Synfire chain | not on slides | 02 §1 with exercises; sketch at the start of the hands-on |
| Synaptic events and energy | link in 5.2, 9.1 | 02 §1 collapsible, Discuss |
| Surrogate gradients | 7.1–7.2 | collapsible in 04 |
| NIR primitives, integrators, `scale_weights` | rule only (7.5) | 03 collapsibles and exercises |
| Training shortcut (no memory across time) | not on slides | 04 note and collapsible |
| Neurons per core, memory | "128 KB per PE" on 5.1 | 04 collapsible |

## Left out

Stays in the knowledge base; can come up in questions.

- **Primer:** FHN phase plane (P 2), RC circuit and charging (P 3–4), input–output curve (P 6, the notebook covers it), $\alpha$ decay and reset-mode plots (P 8–9, the notebook covers them), synapse types (P 11), weight quantisation (P 12), probabilistic neurons (P 15), rate vs. latency coding and rate precision (P 17–18), MNIST encoding (P 19), network architectures and clustered network (P 20–21).
- **Hardware:** PE function (H 3), local memory (H 5), multicast (H 6), power states (H 8), memory layout of a PE, boot log, router details.
- **Computing fundamentals:** what a core is (C 1), memory hierarchy (C 3), bus vs. network-on-chip (C 4); C 2 and C 5 are used.
- **History:** the big programmes in detail, AER, Mahowald, the three communities; the Q&A list of `05_history.md` serves as instructor backup.
- **Applications:** per-paper details, SpiNNaker1 highlights, industry overview.

## New figures needed

- Agenda graphic for the afternoon (1.1).
- Synfire chain sketch: groups, fan-in, a volley sharpening (start of hands-on 2, on a slide or in notebook 02).
- NIR as a hub between frameworks and chips (7.3), drawn here, not copied from the NIR paper.
- Possibly a two-column "deep learning ↔ spiking" summary slide at the end of block 3.

## Open questions

- Block 3 now takes about 12 of its 20 minutes: do the remaining 8 minutes go to hands-on 3 (block 8) or to the Q&A (block 10)?
- Whether 1.4 (von Neumann) is needed for an ML audience or 1.3 already makes the point.
- Restyling: knowledge-base figures use their own colours; decide whether they are redrawn in the HPI slide palette or used as they are for the first run.
