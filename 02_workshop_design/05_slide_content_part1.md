# Slide content, part 1

Content of the slides for the first half of the workshop (14:00 to 15:30), block by block. Agreed here first; the style is agreed separately, then a PowerPoint agent builds a draft from this file.

Format per slide: a title that carries the message, a subtitle of one or two lines where words are needed, and one visual. No bullets. Figures are reused from `01_knowledge_base/figures/` as they are. Open points are marked *open*.

## Slide style

- Template: AISC Light (`hpi-corporate-design`, `202608_AISC-Template_Light.pptx`), 16:9.
- Layouts: "Titelfolie" for the title; one divider "Zwischentitel" per block with block number and title; "Inhalt 1" with the side band for content slides (section name in the band, red line under the title); "Inhalt" without band for slides that are only a large visual.
- Band colour: one colour per block. Block 1 deep red; block 3 HPI orange; the other blocks to be decided.
- Titles: carry the message of the slide, sentence case.
- Subtitle: one or two lines under the title, only where the visual needs words. Template fonts, not below 18 pt.
- One visual per slide, as large as possible below title and subtitle. No bullets.
- No cards, boxes or callouts.
- Figures from `01_knowledge_base/figures/` as they are. New figures (agenda, timeline, raster) are drawn plainly: grey plus the HPI red as the one accent, labels large enough for the back of the room.
- Sources: one small grey line at the bottom of the slide ("Source: …").
- Photo placeholders: a grey area labelled with what goes there, e.g. "Photo: HPI frame".
- No speaker notes.

## Goals of the first half

1. Orientation: what neuromorphic computing and SpiNNaker2 are and how the field evolved (block 1); what is installed at HPI (block 5); what it is used for (block 10).
2. Motivation: why neuromorphic hardware is built (local memory, communication through spikes, energy), and under which conditions the advantage holds.
3. SNN basics with deep learning as the anchor: the LIF neuron in discrete time, synapses with weight and delay, an LIF layer as a recurrent cell, why spike timing matters; each deep learning concept gets a short refresher first.
4. Hardware in practice: how a network ends up on chips and cores, what a core does per time step, what a run costs, why development happens on Brian2.
5. Practice: build a small network in py-spinnaker2 and run it on Brian2, and on the chip for HPI participants.

Not in the first half: training, PyTorch and NIR, energy measurement, the critical assessment of applications.

Audience: students with an ML background and developers with Python experience (announcement); no prior knowledge of neuroscience, spiking networks or neuromorphic hardware.

## Block 1: welcome and motivation (14:00, 15 min)

### Slide 1.1: Neuromorphic computing on SpiNNaker2

- Hands-on workshop
- David Goll, AI Service Centre Berlin Brandenburg, HPI
- 18 November 2026

### Slide 1.2: The afternoon

- Subtitle: Outside HPI, everything runs on the Brian2 simulator; HPI cluster participants can also run on the chip. Not installed yet? Start now: github.com/aihpi/workshop-spinnaker2
- Visual: agenda of the afternoon in two halves with times (existing draft figure `b1_agenda.png`)

### Slide 1.3: Running AI on today's hardware costs a lot of energy

- No subtitle
- Visual: horizontal bar chart of power on a logarithmic axis (the values span three orders of magnitude), each bar labelled with its value:

| System | Power | What the number is | Source |
|---|---|---|---|
| Laptop processor (Intel Core Ultra 7 155H) | 28 W, up to 115 W in short bursts | rated base and maximum turbo power | Intel product specifications (ark.intel.com) |
| Data-centre GPU (NVIDIA H100 SXM) | up to 700 W | rated maximum (configurable) | NVIDIA H100 datasheet |
| GPU server with 8 GPUs (NVIDIA DGX H100) | up to 10.2 kW | rated maximum system power | NVIDIA DGX H100 datasheet; NVIDIA DGX SuperPOD planning guide |
| Human brain | about 20 W (estimates: 10 to 20 W) | estimate | Yu et al. 2018, J Cereb Blood Flow Metab 38(8):1339, doi:10.1177/0271678X17708691 ("estimated to require 10–20 watts"); Raichle and Gusnard 2002, PNAS 99(16):10237, doi:10.1073/pnas.172399499 (about 20 % of the body's oxygen and calories at about 2 % of its weight) |

- Note in the figure: rated maximum power, not measured consumption; the brain value is an estimate
- Source line: Intel and NVIDIA datasheets; Yu et al. 2018; Raichle and Gusnard 2002

The explanation of why fetching from memory costs so much follows on the next two slides (von Neumann bottleneck, energy per operation).

### Slide 1.4: Why is the brain so efficient?

- Title: Why is the brain so efficient?
- Subtitle: Three features of the brain that inspired neuromorphic hardware
- Visual: the neuron image (Bruce Blaus, CC BY, via Wikimedia Commons) with the three features of the brain: mostly quiet; memory where it is used; many simple units at once (about 86 billion neurons)
- Source line: Attwell and Laughlin 2001, J Cereb Blood Flow Metab 21:1133; Lennie 2003, Curr Biol 13:493; Azevedo et al. 2009, J Comp Neurol 513:532. Image: Bruce Blaus, CC BY 3.0, via Wikimedia Commons

Facts behind the labels (abstracts read via Europe PMC):
- Attwell and Laughlin 2001: action potentials 47 % and postsynaptic glutamate effects 34 % of the predicted energy use of signalling in rodent grey matter, resting potential 13 %; energy use depends strongly on the action potential rate; "≤15 % of neurons simultaneously active". doi:10.1097/00004647-200110000-00001
- Lennie 2003: the cost of spikes limits, "possibly to fewer than 1%", the number of cortical neurons that can be substantially active concurrently (human cortex). doi:10.1016/s0960-9822(03)00135-0
- Levy and Calvert 2021 (optional, for questions): in the human cortex, 0.1 W for computation against 3.5 W for long-distance communication, 35 times more. doi:10.1073/pnas.2008173118
- "Memory where it is used": learning changes the connections between neurons (synaptic plasticity and memory hypothesis; textbook knowledge, not covered by the two papers above).
- Azevedo et al. 2009: "the adult male human brain contains on average 86.1 +/- 8.1 billion" neurons. doi:10.1002/cne.21974

### Slide 1.5: What neuromorphic hardware borrows from the brain

Split off from slide 1.4 in the deck (built by the PowerPoint agent): the two-column table "The brain" / "Inspired in hardware" from the slide 1.4 prompt.

### Slide 1.6: From brain simulation to AI hardware: how the field evolved

- Layout: same as the other content slides of block 1 (deep red side band)
- Title: From brain simulation to AI hardware: how the field evolved
- Subtitle (one or two lines, no bullets): Neuromorphic computing had two goals: simulating the brain, and building low-power computers for AI. Over time the weight shifted towards AI.
- Visual: a drawn timeline with a true time axis from 1985 to 2026 and two lanes. Top lane "Simulating the brain", bottom lane "Low-power AI hardware". The 1990 event sits on the axis between the lanes as the common start. Each event has its year and a short explanation of three to eight words. SpiNNaker events in HPI red, all others in grey, with a small legend "red: SpiNNaker". Labels readable from the back of the room.

| Year | Lane | Label on the slide | Fact in the knowledge base |
|---|---|---|---|
| 1990 | start (between the lanes) | Carver Mead: chips modelled on the brain | Mead names the field in 1990; analog silicon retina and cochlea in the late 1980s |
| 2006 | brain | SpiNNaker: built to simulate up to 1 % of the human brain in real time (red) | construction starts in Manchester in 2006; the 1 % goal from Manchester 2018 |
| 2013 to 2023 | brain | Human Brain Project (EU): brain simulation, with SpiNNaker | HBP from 1 Oct 2013 to 30 Sep 2023, with SpiNNaker and BrainScaleS |
| 2014 | AI | IBM TrueNorth: 1 million neurons on one chip | Merolla et al. 2014; funded by DARPA's SyNAPSE programme from 2008 |
| 2017 | AI | Intel announces Loihi | Intel Loihi, Wikipedia |
| 2021 | AI | SpiNNaker2 chip, planned for brain simulation and machine learning (red) | tapeout in July 2021; "brain simulation and machine learning" from Mayr et al. 2019 |
| 2024 | AI | Intel Hala Point: 1.15 billion neurons | Intel 2024 |
| 2025 | AI | SpiNNaker2 system with 35,000 chips in Dresden (red) | in operation at TU Dresden since April 2025 |

- Source line, small and grey at the bottom: "Source: History of Neuromorphic Computing, section 1 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Not on this slide: Intel archiving its Loihi software (2026) and the renaming of the SpiNNaker2 vendor to Sparxity (2026); both go to block 10, where this slide returns with an open row, "what next?". Corrections against the first draft: Loihi was announced in 2017, not 2018; 2021 was the tapeout of SpiNNaker2, not the start of production.

### Slide 1.7: SpiNNaker: from brain simulator to AI hardware

- Layout: same as the other content slides of block 1 (deep red side band)
- Title: SpiNNaker: from brain simulator to AI hardware
- Subtitle (one line, no bullets): From a brain simulator to a chip for brain simulation and machine learning, with eight times as many cores per chip
- Visual: a simple two-column table across the slide (no fill colours, thin grey lines, bold column headers and row labels), at least 16 pt:

| | SpiNNaker1 | SpiNNaker2 |
|---|---|---|
| Where | University of Manchester, Steve Furber (co-designer of the first ARM processor); built from 2006 | TU Dresden (Christian Mayr) with Manchester; chip finished in 2021 |
| Goal | Simulate up to 1 % of the human brain in real time | Brain simulation and machine learning |
| Chip | 18 small ARM cores | 152 small ARM cores, plus accelerators for neural-network arithmetic |
| Largest system | 1 million cores, Manchester 2018 | About 35,000 chips, more than 5 million cores, Dresden 2025 |

- Sentence below the table, one line, normal text size: "Unlike chips with fixed neuron circuits, such as IBM TrueNorth or the analog neurons of BrainScaleS, SpiNNaker runs neurons as software on many small standard processors, so any neuron model can be programmed."
- Source line, small and grey at the bottom: "Source: History of Neuromorphic Computing, sections 4 and 5 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Facts behind the table (`05_history.md`, section 4): Furber worked on the first ARM processor at Acorn and became professor in Manchester in 1990; construction of SpiNNaker1 started in 2006; 18 ARM968 cores per chip at 200 MHz, 130 nm; the million-core machine (57,600 chips, 1,036,800 cores, about 100 kW) was switched on on 2 November 2018, target 1 billion neurons, about 1 % of a human brain. SpiNNaker2: designed at TU Dresden (Mayr) with Manchester; roadmap 2019 "brain simulation and machine learning"; tapeout July 2021; 152 processing elements with ARM Cortex-M4F, MAC array and accelerators; the Dresden system with about 35,000 chips and more than 5 million cores in operation since April 2025, presented as infrastructure for energy-efficient AI.

Not on this slide: the chip in detail, the boards at HPI and how to program them (block 5); the vendor SpiNNcloud and its renaming to Sparxity (block 10). The word "spike" is introduced on slide 1.9; here it is "pulses".

### Slide 1.8: The von Neumann bottleneck: data has to travel to the processor

- Layout: same as the other content slides of block 1 (deep red side band)
- Title: The von Neumann bottleneck: data has to travel to the processor
- Subtitle (two lines, no bullets): Memory and processor are separate, so every weight and instruction crosses one connection; processors became faster than memory, so this connection limits the computer
- Visual: `01_knowledge_base/figures/00_computing_fundamentals/02_von_neumann_vs_distributed.png`, whole figure, as large as possible (panel A von Neumann; panel B, each core with its own memory, is the preview for block 5)
- Source line, small and grey at the bottom: "Source: Computing Fundamentals, section 2 (workshop knowledge base); von Neumann 1945; Backus 1977"
- No bullets, no boxes, no speaker notes

What to say (not on the slide): almost every computer keeps program and data in a memory separate from the processor; processors became much faster than memory, so the computer often waits for data; caches soften this but do not solve it. For AI, the weights of a model sit in RAM or in the DRAM of a GPU and are fetched again on every pass. Panel B is how SpiNNaker2 does it (block 5). Transition to the next slide: this traffic also costs energy, more than the computation itself.

### Slide 1.9: Moving data costs more energy than computing on it

- Layout: same as the other content slides of block 1 (deep red side band)
- Title: Moving data costs more energy than computing on it
- Subtitle (one line, no bullets): Reading one value from off-chip memory costs more than a thousand additions; reading it from a small memory on the chip costs about a hundred times less
- Visual: horizontal bar chart on a linear axis (the small values shrink to almost nothing next to the DRAM bar, which is the point), each bar labelled with its value. DRAM bar in HPI red, all others grey. Bars from top to bottom:

| Bar label | Value |
|---|---|
| 32-bit integer add | 0.1 pJ |
| 32-bit float add | 0.9 pJ |
| 32-bit float multiply | 3.7 pJ |
| SRAM read, 64 bit, small (8 KB), on chip | 10 pJ |
| SRAM read, 64 bit, large (1 MB), on chip | 100 pJ |
| DRAM read, 64 bit, off chip | 1,300 pJ (at least; Horowitz gives 1.3 to 2.6 nJ) |

- Axis label: "energy per operation (pJ)"
- Source line, small and grey at the bottom: "Source: Horowitz 2014, ISSCC, 45 nm process at 0.9 V; values are lower in newer processes, the ratios are what matter"
- No bullets, no boxes, no speaker notes

Left out on purpose: the instruction overhead of a programmable core (about 70 pJ, Horowitz 2014), which matters for SpiNNaker's software neurons in block 5, not for this message; the multiply-accumulate (4.6 pJ), which is computed as multiply plus add and not a Horowitz value. Values as in `01_knowledge_base/figures/01_primer_snn_basics/make_figures.py` (HOROWITZ_PJ).

### Slide 1.10: Spiking neural networks: neurons that stay quiet until they have something to say

- Layout: same as the other content slides of block 1 (deep red side band)
- Title: Spiking neural networks: neurons that stay quiet until they have something to say
- Subtitle (two lines, no bullets): Like a real neuron, a spiking neuron collects its input and sends a short pulse, a spike, only when it crosses a threshold. An artificial neuron passes on a number in every step, and every connection computes with it, whether it matters or not.
- Visual: one figure with two panels side by side, same size:
  - left, "Artificial neural network": a small layer of neurons over time, every cell filled with a value (dense grid in shades of grey)
  - right, "Spiking neural network": the sparse raster, one dot per spike, most neurons silent most of the time (existing draft figure `b1_raster.png`, redrawn at the same size as the left panel)
  - small note in the figure: "illustration"
- Source line, small and grey at the bottom: "Source: Spiking Neurons and Networks, sections 1 and 9 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

How a spiking neuron computes in detail (leak, threshold, reset, time steps) is block 3; the comparison with deep learning is also deepened there.

### Slide 1.11: Two ways to run a spiking network: the SpiNNaker2 chip or the Brian2 simulator

- Layout: same as the other content slides of block 1 (deep red side band), content in two columns of equal width
- Title: Two ways to run a spiking network: the SpiNNaker2 chip or the Brian2 simulator
- Subtitle (one line, no bullets): You write the network once in Python with py-spinnaker2, and it runs on either
- Left column, heading "SpiNNaker2 chip": photo of a SpiNNaker2 chip or board (placeholder until David's photo), below it one or two lines: "Many small cores, each simulating neurons in software with the connections in its own memory; only spikes travel between cores. At HPI: 6 boards, for participants with an HPI cluster account."
- Right column, heading "Brian2 simulator": image of a laptop with a notebook (placeholder, or a screenshot of the setup notebook's plot), below it one or two lines: "A simulator that runs the same Python code on your laptop, in seconds, and gives the same spikes in the networks of this workshop. For everyone."
- Source line, small and grey at the bottom: "Source: Hardware and Energy, sections 1 to 5; Brian2 Fallback, section 1 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Transition (spoken, not on the slide): "This is what you will program today. Before we look at how a spiking neuron computes, we check that your setup runs." Then the setup check (slide 2.1, same two columns) and block 3. Whether spikes save energy, and under which conditions, comes back at the end of the afternoon (block 10).

Correctness: "the same spikes in the networks of this workshop" is what the notebooks show (identical spike times on Brian2 and the chip for notebooks 02 to 04); Brian2 and the chip can differ in edge cases, e.g. a potential landing exactly on the threshold (`03_brian2_fallback.md`, section 3). Not claimed: that a core only works when a spike arrives; every neuron is updated in every time step (block 5). The chip in detail, the boards and the cost of a run are block 5.

Time: 10 content slides (1.2 to 1.11) in 15 minutes, about 1.5 minutes each; tight.

## Block 2: setup check (14:15, 5 min)

### Slide 2.1: Setup check

Layout: two columns of equal width, same arrangement as slide 1.11: left the HPI cluster (chip), right the laptop (Brian2).

Left column, "On the HPI cluster (chip)":

- *open*: the steps to reach cx51 and open the environment there, filled in once the access for the workshop is set up with the cluster admins

Right column, "On your laptop (Brian2)":

- Open the folder `workshop-spinnaker2` in VS Code
- Select the kernel `.venv (Python 3.12)`
- Open `04_workshop_material/00_setup_check.ipynb` and run all cells
- Expected: "Brian2 works." and the plot below
- Not installed yet? Run `uv sync` in the folder (5 to 15 min, README on github.com/aihpi/workshop-spinnaker2)

Visual: the plot of the setup notebook, output spikes one step after each input spike (`02_workshop_design/slides/figures/10_setup_check_plot.png`, or a screenshot of the notebook output), below the right column (laptop).

## Block 3 and hands-on 1: spiking neural networks (14:20, 35 min)

Style for all slides of this block: same elements as the block 1 slides in `slides/block1_draft.pptx` (section label in the side band, kicker line above the title, title, subtitle, one visual, source line, slide number), with HPI orange as the accent colour instead of deep red. Section label: "SPIKING NETWORKS". Kicker: "SPIKING NETWORKS · <topic>".

Structure (decided 2026-11-16): blocks 3 and 4 of the outline are interleaved. Part 1, slides before the notebook (about 12 min); part 2, notebook 01 (about 15 min); part 3, slides after the notebook (about 6 min). The slides of part 1 explain what participants need before they can try anything; what they can find out by changing parameters is left to the notebook, and part 3 collects it as a debrief.

### Part 1: slides before the notebook (14:20, about 12 min)

### Slide 3.0: divider

- Same divider as block 2 in the deck (section number, section title, time), in HPI orange
- Section number: 3
- Section title: Spiking neural networks
- Section time: 14:20 · 20 min

### Slide 3.1: From the biological neuron to a simple model (optional, can be skipped)

- Kicker: SPIKING NETWORKS · BIOLOGY
- Title: From the biological neuron to a simple model
- Subtitle (two lines, no bullets): Hodgkin-Huxley describes the ion channels in detail with four variables, FitzHugh-Nagumo keeps two, the leaky integrate-and-fire model (LIF) only one. Fitted to the same input, all three fire at the same times; only the spike shape and the computing cost differ.
- Visual: `01_knowledge_base/figures/01_primer_snn_basics/02_models_hh_fhn_lif.png`, as large as possible (the knowledge-base figure as it is)
- Source line, small and grey at the bottom: "Source: Spiking Neurons and Networks, section 2 (workshop knowledge base); Hodgkin and Huxley 1952; FitzHugh 1961, Nagumo et al. 1962"
- No bullets, no boxes, no speaker notes

Facts behind the slide (`01_primer_snn_basics.md`, section 2 and Figure 1): Hodgkin-Huxley has the membrane potential plus three gating variables for the sodium and potassium channels, four coupled non-linear equations; FitzHugh-Nagumo has two variables; LIF has one. In Figure 1 the FitzHugh-Nagumo time axis is stretched and the LIF parameters are fitted so that all three fire at the same times as Hodgkin-Huxley. The message: computing only needs when spikes happen, so the useful direction is down the ladder. Caveat for questions: to match Hodgkin-Huxley, the fitted LIF in the figure resets below rest and has an 11 ms refractory period; the `lif` model of the chip has no refractory period. Historically, integrate-and-fire is older (Lapicque 1907) than Hodgkin-Huxley (1952) and FitzHugh-Nagumo (1961/62).

Transition to slide 3.2 (spoken): "LIF is the model we use on the chip today. Let us put it next to the neuron you know from deep learning."

### Slide 3.1b: Detour: how a neuron produces a spike (optional, shown only briefly)

- Mark clearly as a detour: kicker "SPIKING NETWORKS · DETOUR", and a small label "Detour" in the top right corner of the content area (grey, not orange), so the audience sees it is not needed for the rest
- Title: Detour: two equations that produce a spike
- Subtitle (two lines, no bullets): FitzHugh-Nagumo reduces Hodgkin-Huxley to a fast variable v (the membrane potential) and a slow recovery variable w. With enough input, the state runs around a loop: slow drift, a fast jump (the spike), slow recovery, a fast fall back.
- Visual, left (about 40 % of the width): the two equations, large:
  - dv/dt = v − v³/3 − w + I
  - τ_w · dw/dt = v + a − b · w
  - under them, three short lines in grey: "v: fast, the membrane potential", "w: slow, recovery after a spike", "the cubic term makes the neuron excitable"
- Visual, right (about 60 %): the phase plane with the loop, `01_knowledge_base/figures/01_primer_snn_basics/02_fhn_phase_plane.png` (David adds the image later; until then a grey placeholder "Figure: 02_fhn_phase_plane.png")
- Source line: "Source: Spiking Neurons and Networks, section 2.2 (workshop knowledge base); FitzHugh 1961, Nagumo et al. 1962"
- No bullets, no boxes, no speaker notes

Facts behind the slide (`01_primer_snn_basics.md`, section 2.2, Eq. 1 and Figure 2): v plays the role of Hodgkin-Huxley's membrane potential together with the fast sodium activation, w the slow gates; the cubic term makes the neuron excitable (a small push decays, a push past a critical point triggers the spike). The phase plane shows the nullclines (dv/dt = 0 cubic, dw/dt = 0 straight line); with constant input I = 0.5 the trajectory runs on a limit cycle, repeated spiking, in five steps: drift along the left branch, the knee, the jump to the right branch (spike), recovery on the right branch, the fall back. Parameters as in Figure 1: a = 0.7, b = 0.8, τ_w = 12.5. For questions: weak input leaves a stable resting point (the counterpart of LIF's critical input); for these parameters the switch to spiking is at I ≈ 0.33 (Hopf bifurcation).

Transition (spoken): "LIF keeps only what matters for computing from this loop: a threshold and a reset. That is the neuron we use on the chip."

### Slide 3.3: The LIF neuron: integrate, leak, fire, reset

- Kicker: SPIKING NETWORKS · LIF
- Title: The LIF neuron: integrate, leak, fire, reset
- Subtitle (one line, no bullets): Input charges the membrane potential, a leak pulls it back towards rest, and when it crosses the threshold the neuron fires and resets.
- Equation, large, directly under the subtitle, with two short grey labels under its terms:
  - τ_m · dV/dt = −(V − V_rest) + R · I(t)
  - under "−(V − V_rest)": "leak: pulls V back to rest"
  - under "R · I(t)": "input: pushes V up"
  - next to it, one line: "if V reaches V_th: spike, then V → V_reset"
- Visual: `02_workshop_design/slides/figures/b3_lif_basics.png` below the equation, full content width (drawn for this slide by `b3_make_lif_basics.py`: continuous-time LIF with τ = 10 ms, evenly spaced input spikes, one output spike, labels integrate, leak, fire, reset; replaces the knowledge-base figure with three constant inputs, which anticipated the results of notebook 01, section 1)
- Source line: "Source: Spiking Neurons and Networks, sections 2.4 and 2.5, Eq. 5 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Facts behind the slide: Eq. 5 of the SNN note (`01_primer_snn_basics.md`, section 2.4): the membrane as an RC circuit, τ_m = R·C; the first term is the leak towards the resting potential V_rest, the second the input. The threshold and the reset are not part of the equation but a rule on top of it (section 2.5). Not on the slide, on purpose: that below a certain input the neuron never fires, and the spike-count curve against the input; participants find both in notebook 01, section 1; the debrief (slide 3.6) collects them. The discrete form that the chip computes follows on slide 3.4.

### Slide 3.2: Spiking neuron vs. artificial neuron

- Kicker: SPIKING NETWORKS · COMPARISON
- Title: Spiking neuron vs. artificial neuron
- Subtitle (two lines, no bullets): Both weight their inputs and add them up. The artificial neuron forgets everything after each step and passes on a number; the spiking neuron keeps its state from step to step and passes on a spike, 0 or 1, only when it crosses the threshold.
- Visual: the existing diagram in the deck (two rows with the same structure from left to right), kept as it is:
  - top row, "Artificial neuron": inputs x1 … xn as numbers → weights w1 … wn → sum Σ → activation ReLU → output: a number, in every step
  - bottom row, "Spiking neuron (LIF)": input spikes → weights → sum Σ → membrane potential v with leak and threshold → output: one spike when v crosses the threshold, otherwise nothing
  - grey for everything both rows share, HPI orange only for what differs (ReLU vs. membrane potential with threshold; number vs. spike)
- One equation per row, at the right end of the row or directly under it, same notation as slide 3.3:
  - artificial neuron: y = ReLU(Σᵢ wᵢ · xᵢ + b)
  - spiking neuron: τ_m · dV/dt = −(V − V_rest) + Σᵢ wᵢ · sᵢ(t), spike when V reaches V_th (with sᵢ(t) the input spikes of input i, short pulses)
- Source line: "Source: Spiking Neurons and Networks, sections 2.4 and 8 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Facts behind the slide: the artificial neuron computes a weighted sum and an activation in every step, without memory of the previous step (a feed-forward unit); the LIF neuron integrates the weighted input spikes into a state that leaks (Eq. 5 of the SNN note with the input as a weighted sum of spike trains) and emits a binary spike at the threshold. Here R · I(t) of slide 3.3 is written as Σᵢ wᵢ · sᵢ(t): the weights take the role of R. Not on the slide, on purpose: that the spike count of an LIF neuron grows like a ReLU with its input; participants find it in notebook 01, section 1 (debrief, slide 3.6). The recurrent-cell view (state carried over steps, like an RNN) is slide 3.9.

### Slide 3.4: On the chip, the neuron advances in steps of 1 ms

- Kicker: SPIKING NETWORKS · DISCRETE TIME
- Title: On the chip, the neuron advances in steps of 1 ms
- Subtitle (one line, no bullets): Each step, the potential keeps a share α of its value and adds the input of the step; after a spike it is reset
- Visual, top: the update rule as a large equation, v[t] = α · v[t−1] + I_syn[t] + i_offset, with three short labels under the terms: "α = alpha_decay: share kept per step (the leak)", "I_syn: weights of the spikes arriving in this step", "i_offset: a constant input"
- Visual, below: `01_knowledge_base/figures/01_primer_snn_basics/03_discrete_update.png` (the knowledge-base figure as it is)
- One line below the figure, normal text size: "After a spike: v → v − threshold (reset_by_subtraction, the default; the overshoot is carried over) or v → v_reset (reset_to_v_reset, default v_reset = 0)"
- Source line: "Source: Spiking Neurons and Networks, section 3, Eq. 9 (workshop knowledge base); py-spinnaker2 lif model"
- No bullets, no boxes, no speaker notes

Facts behind the slide: Eq. 9 of the SNN note, the update rule of py-spinnaker2's `lif`; Figure 7 uses alpha_decay = 0.8, threshold 10 and reset to 0; default reset of `lif` is reset_by_subtraction. These are exactly the parameters participants set in notebook 01 (threshold, alpha_decay, i_offset, reset). Two caveats: Figure 7 draws input spikes where they arrive and shows v above the threshold in the spike step, while notebook 01 draws input spikes as sent and records v after the reset; if a participant asks, the notebook convention is the one the chip uses.

### Slide 3.5: Synapses: each connection has a weight and a delay

- Kicker: SPIKING NETWORKS · SYNAPSES
- Title: Synapses: each connection has a weight and a delay
- Subtitle (two lines, no bullets): The weight says how strongly one spike pushes the potential, up or down; the delay says how many steps the spike travels. In py-spinnaker2, a connection is one line: [pre, post, weight, delay].
- Visual, top: a simple sketch (to be drawn in the slide, grey with HPI orange labels): two neurons as circles, "input neuron" on the left and "neuron" on the right, an arrow from left to right; on the arrow two labels, "weight" and "delay"
- Visual, below: the code line `[0, 0, 6, 2]` in monospace, large, with four short labels under its parts: "input neuron 0", "→ neuron 0", "weight 6", "delay 2 steps"
- Source line: "Source: Spiking Neurons and Networks, section 4 (workshop knowledge base); py-spinnaker2 snn.Projection"
- No bullets, no boxes, no speaker notes

Left for notebook 01, section 2, on purpose: the exact arrival rule (a spike sent in step t arrives in step t + 1 + delay; the notebook explains it and asks for it in Try 4), what a negative weight does (Try 3), that spikes arriving together fire the neuron (timing debrief, slide 3.7), and that values outside the range are clipped (Try 5). The knowledge-base figure on the delay (Figure 10, spike at step 2 with delay 3 arrives at step 6) is no longer used here; it would give away the arrival rule.

Transition to the notebook (spoken): "Now you try it: notebook 01, section 1 is one neuron with a constant input, section 2 adds input spikes with weights and delays. 15 minutes, then we collect what you found."

### Part 2: notebook 01 (14:32, about 15 min)

Not slides: participants work in `04_workshop_material/01_single_neuron.ipynb` on Brian2. On screen during the hands-on: one slide with the notebook path, the two sections and the time (as the hands-on slides of the deck).

- Section 1, one neuron with a constant input: participants change `i_offset`, `alpha_decay`, `threshold` and `reset` and find out themselves that below a critical input nothing happens, and that above it the spike count grows like a ReLU, in steps. Minimum: Try 1 and 2.
- Section 2, input spikes: participants change weights and delays and find out that spikes arriving together fire the neuron, that the leak makes it forget, that delays can make spikes coincide, and that values outside the range are clipped without a warning. Minimum: Try 1, 3 and 4.
- *Open*: an interactive version of section 1 with sliders for `i_offset`, `alpha_decay` and `threshold` (the RC charging picture of the knowledge base, Figure 4, as a live plot). Needs `ipywidgets`, which is not in the participants' environment yet (would have to go into `pyproject.toml`, `uv.lock` and the conda steps on `main`). Without it, the existing "change these" cell does the same job.
- The notebook needs a clear stopping point at its end ("back to the slides").

### Part 3: slides after the notebook (14:47, about 6 min)

### Slide 3.6: What you found: below a critical input nothing happens, above it the neuron fires almost like a ReLU

- Kicker: SPIKING NETWORKS · DEBRIEF
- Title: What you found: below a critical input nothing happens, above it the neuron fires almost like a ReLU
- Subtitle (two lines, no bullets): Each step, the input only has to replace what leaks away, so the critical input is (1 − α) · threshold. Above it, the spike count grows almost linearly, in small steps, because the neuron can only fire on a whole time step.
- Visual: `02_workshop_design/slides/figures/b3_debrief_fi.png` (made by `b3_make_debrief_fi.py`, py-spinnaker2 on Brian2 with the values of notebook 01, section 1: 81 neurons, i_offset 0 to 4, threshold 10, alpha_decay 0.9, 1,000 steps; critical input 1.0 marked; a ReLU through the critical input with a least-squares slope for comparison, labelled as such)
- Source line: "Source: notebook 01, section 1 (Brian2); Spiking Neurons and Networks, section 2.5 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Facts and talking points: no spikes up to i_offset 1.0; just above it the count jumps to about 35 and then grows almost linearly to 343 at i_offset 4 (the figure script checks the critical input). Why the ReLU comparison matters: a spiking neuron with a constant input behaves on average like a ReLU, which is the basis of converting trained deep networks into spiking networks (the NMNIST demo in block 9 is such a converted network). Its limit: this holds for a constant or averaged input (a rate code), and carrying a value precisely as a rate costs many steps and spikes. Slide 3.7 shows the other side, where the neuron is not like a ReLU.

### Slide 3.7: What you found: spikes that arrive together fire the neuron

- Kicker: SPIKING NETWORKS · DEBRIEF
- Title: What you found: spikes that arrive together fire the neuron
- Subtitle (two lines, no bullets): Because the potential leaks, spikes spread out in time fade before the next one arrives, while the same spikes arriving together cross the threshold. A delay can make spikes coincide: the neuron becomes a coincidence detector, which a ReLU is not.
- Visual: keep the figure that is on this slide in the deck now (unchanged)
- Source line: "Source: notebook 01, section 2 (Brian2); Spiking Neurons and Networks, section 3 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Facts and talking points: left, input 0 fires the neuron at step 10 (three spikes, two steps apart), inputs 1 and 2 reach only 9.85 (two spikes, two steps apart); right, with delay 2 both spikes of inputs 1 and 2 arrive in step 33 and fire the neuron. Optional, from Try 6: an input at step 20 still leaves 0.83 at step 30, enough to make inputs 1 and 2 fire; the neuron remembers a spike from twelve steps earlier. Notebook 02 builds a network of such coincidence detectors.

### Slide 3.8: On the chip, weights are small integers

- Kicker: SPIKING NETWORKS · WEIGHTS
- Title: On the chip, weights are small integers
- Subtitle (two lines, no bullets): For lif, weights are whole numbers from −15 to 15 and delays from 0 to 7. Like quantising a deep network, trained weights have to be scaled and rounded; values outside the range are clipped without a warning.
- Visual: `01_knowledge_base/figures/01_primer_snn_basics/04_weight_quantization.png` (the knowledge-base figure as it is)
- Source line: "Source: Spiking Neurons and Networks, section 4 (workshop knowledge base); py-spinnaker2 v0.8 code"
- No bullets, no boxes, no speaker notes

Facts behind the slide: Figure 12 of the SNN note, 5000 normally distributed weights mapped onto [−15, 15]; with a scale that keeps 99 % in range, 13 % of the weights become 0 and the rest take 30 distinct values. Why the range is so narrow (each synapse is one packed word in the core's memory) is block 5. Role: refresher of quantisation in deep learning.

Transition to the hardware block (spoken): "Why only −15 to 15? The answer is in the hardware, the next block."

Time: part 1 about 12 min (3.1 and 3.1b optional), notebook 01 about 15 min, part 3 about 5 min; about 32 min of the 35 min of blocks 3 and 4 together. The slide "An LIF layer is a recurrent cell" moved to block 7 on 2026-11-16 (see the end of this file).

### PowerPoint prompt for part 3 (debrief slides 3.6 to 3.8)

```
Rework the three debrief slides of block 3 (SPIKING NETWORKS) that come after the hands-on slide for notebook 01. Keep the block 3 style exactly (section label, kicker, title, subtitle, source line, slide number, HPI orange accent). Do not change any other slide.

Order after the hands-on slide: (1) input and output, (2) timing, (3) weights. If the deck has a slide "An LIF layer is a recurrent cell with spikes as output" in block 3, move it out of block 3 to the end of the deck (it belongs to block 7, after the break). Create a slide if it does not exist yet; otherwise update it.

Slide 1 (debrief, input and output)
- Kicker: SPIKING NETWORKS · DEBRIEF
- Title: What you found: below a critical input nothing happens, above it the neuron fires almost like a ReLU
- Subtitle (two lines): "Each step, the input only has to replace what leaks away, so the critical input is (1 − α) · threshold. Above it, the spike count grows almost linearly, in small steps, because the neuron can only fire on a whole time step."
- Figure: /sc/home/david.goll/projects/spinnaker/workshop-spinnaker2/02_workshop_design/slides/figures/b3_debrief_fi.png, below the subtitle, full content width, aspect ratio kept (2:1), as large as the space allows, centred. Replace any placeholder or older figure on this slide.
- Source line: "Source: notebook 01, section 1 (Brian2); Spiking Neurons and Networks, section 2.5 (workshop knowledge base)"

Slide 2 (debrief, timing)
- Kicker: SPIKING NETWORKS · DEBRIEF
- Title: What you found: spikes that arrive together fire the neuron
- Subtitle (two lines): "Because the potential leaks, spikes spread out in time fade before the next one arrives, while the same spikes arriving together cross the threshold. A delay can make spikes coincide: the neuron becomes a coincidence detector, which a ReLU is not."
- Figure: keep the current figure and its annotations as they are.
- Source line: "Source: notebook 01, section 2 (Brian2); Spiking Neurons and Networks, section 3 (workshop knowledge base)"

Slide 3 (weights), last slide of block 3
- Kicker: SPIKING NETWORKS · WEIGHTS
- Title: On the chip, weights are small integers
- Subtitle (two lines): "For lif, weights are whole numbers from −15 to 15 and delays from 0 to 7. Like quantising a deep network, trained weights have to be scaled and rounded; values outside the range are clipped without a warning."
- Figure: keep 04_weight_quantization.png as it is.
- Source line: "Source: Spiking Neurons and Networks, section 4 (workshop knowledge base); py-spinnaker2 v0.8 code"

No bullets, no boxes, no speaker notes. Report the final slide order of block 3.
```

## Block 5: SpiNNaker2 hardware (14:55, 15 min)

Style for all slides of this block: same elements as the block 1 and block 3 slides in `slides/block1_draft.pptx` (section label in the side band, kicker line above the title, title, subtitle, one visual, source line, slide number). Accent colour: to be decided. Section label: "SPINNAKER2 HARDWARE". Kicker: "SPINNAKER2 HARDWARE · <topic>".

Structure: a zoom from the code down to one processing element (PE). The block starts with the path from Python to the cores, then follows the work step by step: where it lands (installation), inside the chip, inside one PE in one time step, one PE over many time steps. Figures are the knowledge-base figures as they are. What py-spinnaker2's code looks like is not on the slides (notebook 01 introduces it, notebook 02 sums it up); this block explains what py-spinnaker2 does with the network.

### Slide 5.0: divider

- Same divider as the other blocks in the deck (section number, section title, time)
- Section number: 5
- Section title: SpiNNaker2 hardware
- Section time: 14:55 · 15 min

### Slide 5.1: From Python to the cores

- Kicker: SPINNAKER2 HARDWARE · FROM PYTHON TO THE CHIP
- Title: From Python to the cores: what happens when you call hw.run
- Subtitle (two lines, no bullets): You describe the network in Python and choose the neuron model by name. py-spinnaker2 turns it into network data (parameters, weights, routing tables) and compiles the neuron model's C code for the ARM cores, sends both to the board, and every core runs its part directly on the hardware, without an operating system.
- Visual: `01_knowledge_base/figures/00_computing_fundamentals/06_bare_metal_cross_compilation.png` (computing fundamentals, Figure 5), as large as possible
- Source line: "Source: Computing Fundamentals, section 6 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Facts behind the slide (`00_computing_fundamentals.md`, section 6, Figure 5): ① the user describes the network in Python and selects the model by name (e.g. `lif`); the C code of the models is part of py-spinnaker2; ② on the host, py-spinnaker2 creates the network data and cross-compiles the model's C code for the ARM cores (CMake, `arm-none-eabi-gcc`, results cached); ③ both are sent to the board via Ethernet; ④ each core runs the machine code bare-metal: a timer interrupt wakes it once per time step, it updates its neurons and sends spikes, then sleeps. Own C code is only needed for custom neuron models (an outlook, not part of the workshop). Transition: "Where does this land? Let us follow it."

### Slide 5.2: Where your network runs

- Kicker: SPINNAKER2 HARDWARE · INSTALLATION
- Title: Where your network runs: from the cluster to one chip
- Subtitle (two lines, no bullets): py-spinnaker2 runs on the cluster node cx51, which talks to a frame of 6 boards over Ethernet. A run reserves one board with 48 chips, 7,104 cores available for your network; each chip is about 1 cm × 1 cm with 152 processing elements.
- Visual: `01_knowledge_base/figures/02_hardware_energy/01_installation_hierarchy.png` (hardware note, Figure 1), as large as possible
- Source line: "Source: Hardware and Energy, sections 1 and 5 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Facts behind the slide (`02_hardware_energy.md`, Figure 1): panels A to D: rack, frame with 6 boards and a management controller that powers and boots them, one board with 48 chips with their own DRAM and links to their neighbours, one chip with 152 PEs and their local SRAM. One board: 7,296 PEs, 7,104 available to a run. The arrangement of chips and links on the board is schematic.

### Slide 5.3: Inside one chip

- Kicker: SPINNAKER2 HARDWARE · CHIP
- Title: Inside one chip: 152 small cores, each with its own memory
- Subtitle (two lines, no bullets): Four processing elements (PEs) form a quad PE (QPE); each PE is an ARM core with 128 KB of local memory. A spike leaves its PE as a small packet: by default py-spinnaker2 sends one packet to each PE with target neurons; the router can also copy a single packet to all of them (multicast).
- Visual: `01_knowledge_base/figures/02_hardware_energy/01_chip_schematic.png` (hardware note, Figure 2), as large as possible
- Source line: "Source: Hardware and Energy, sections 1, 2 and 4 (workshop knowledge base); Scholze et al. 2026; py-spinnaker2 tutorial 06"
- No bullets, no boxes, no speaker notes

Facts behind the slide (`02_hardware_energy.md`, Figure 2): A: 38 QPEs of 4 PEs, the router in the middle, links to neighbouring chips, the DRAM interface and Ethernet; the red arrows show the path of one spike. B: one QPE, whose 4 PEs share one connection to the network-on-chip. C: what one PE contains. Arrangement and spike path are schematic, not the physical floorplan. A neuron is software on a PE; one PE simulates up to 256 `lif` neurons.

### Slide 5.4: Inside one PE, in one time step

- Kicker: SPINNAKER2 HARDWARE · ONE TIME STEP
- Title: Inside one PE: what happens in one time step
- Subtitle (two lines, no bullets): A timer wakes the core. It reads the spikes that arrived, looks up their synapses in its memory and adds the weights to its neurons, updates all its neurons and sends the new spikes. Then it sleeps until the next tick.
- Visual: `01_knowledge_base/figures/02_hardware_energy/02_pe_function.png` (hardware note, Figure 3), as large as possible
- Source line: "Source: Hardware and Energy, section 2 (workshop knowledge base); Scholze et al. 2026; py-spinnaker2 tutorial 06; snn-core code"
- No bullets, no boxes, no speaker notes

Facts behind the slide (`02_hardware_energy.md`, Figure 3): ① the timer wakes the core; ② spike packets from the previous step were written into a spike buffer in SRAM by the DMA, in the background; ③ the core reads the buffered spikes and the synapse tables (targets and weights); ④ it adds the weights and updates the states of all its neurons in SRAM; ⑤ neurons that crossed the threshold send a spike packet. Everything the core needs sits in its own SRAM, so no step waits for DRAM. This is the step of slide 3.4 (v[t] = α · v[t−1] + I_syn[t] + i_offset) as the chip executes it.

### Slide 5.5: One PE over ten time steps

- Kicker: SPINNAKER2 HARDWARE · TIME STEPS
- Title: One PE over ten time steps: work, then sleep
- Subtitle (two lines, no bullets): Each step starts with a timer tick. The more spikes arrive, the longer the core works; in a sparse network it sleeps most of the time. If too many spikes arrive in one step, the work does not fit and the next step starts late.
- Visual: `01_knowledge_base/figures/02_hardware_energy/02_pe_timestep.png` (hardware note, Figure 4), as large as possible
- Source line: "Source: Hardware and Energy, sections 2 and 7 (workshop knowledge base); illustration, durations made up"
- No bullets, no boxes, no speaker notes

Facts behind the slide (`02_hardware_energy.md`, Figure 4): timer-driven steps of 1 ms (configurable); first processing the arrived spikes (orange), then updating the neurons and sending spikes (blue), sleeping for the rest of the step (grey); spike counts and durations are made up (illustration). Important for the energy discussion: every neuron is updated in every step, spiking or not; the part that grows with activity is the spike processing. In a sparse network the PE sleeps most of the time, which is where the saving comes from (section 6). Step 6 shows a violated real-time deadline (section 7).

For questions: "What happens if a step overruns?"

- No crash: the run continues, the chip logs "Deadline missed in systick …" (`lif` chip code, `lib/lif_neuron/main.c`)
- The results may be off: the late work spills into the next steps, spikes can land in the wrong step
- How you notice: py-spinnaker2 prints "Some PEs returned some errors! Results may be corrupted!" after the run; `profile=True` gives `deadline_flag` > 0 per step; `record=["time_done"]` shows the margin per step
- Not on Brian2: it has no real time and silently ignores `sys_tick_in_s`
- Remedy: a longer time step, `hw.run(net, steps, sys_tick_in_s=2e-3)` (same spikes, twice the wall-clock time), or fewer neurons per core with `pop.set_max_atoms_per_core(n)` or `iterative_mapping=True`
- Unlikely in this workshop: memory is the tighter limit; tutorial 05 (10,000 synaptic events per step on one PE) missed no deadline on the HPI chips

Sources: `02_hardware_energy.md`, section 7; `01_primer_snn_basics.md`, section 3; `03_brian2_fallback.md`, section 1; py-spinnaker2 v0.8.5 source (`hardware.py`, `tools/chip_logger.py`, `tools/profiling.py`).

### Slide 5.6: Why weights are small integers

- Kicker: SPINNAKER2 HARDWARE · MEMORY
- Title: Why weights are small integers: one synapse is one 16-bit word
- Subtitle (two lines, no bullets): Every PE keeps the synapses of its neurons in its own 128 KB of memory, about 68 KiB of which is left for the network with lif. To fit, each synapse is packed into 16 bits: 4 bits weight plus a sign, 3 bits delay, 8 bits for the target neuron.
- Visual: a drawing of the 16-bit word (to be drawn): 16 boxes in a row, grouped into four labelled fields, "weight (4 bits)" and "sign (1 bit)" in the block's accent colour, "delay (3 bits)", "target neuron (8 bits)" in grey; under each field what follows from it: "−15 to 15", "0 to 7", "at most 256 neurons per PE". Order of the fields schematic.
- Source line: "Source: Spiking Neurons and Networks, section 4; Hardware and Energy, section 3 (workshop knowledge base); py-spinnaker2 v0.8.5 code"
- No bullets, no boxes, no speaker notes

Facts behind the slide: py-spinnaker2 v0.8.5, `neuron_models/lif_neuron.py`: the synapse word of `lif` is `SynapseWordSpec(word_size=16, weight=4, delay=3, synapse_type=1, target=8)`; the 1-bit field is called `synapse_type` in the code (excitatory or inhibitory) and acts as the sign. `01_primer_snn_basics.md`, section 4: "each synapse is stored as one 16-bit word with 4 bits for the weight, 3 for the delay, 1 for the sign and 8 for the target"; weights outside the range are clipped and fractions rounded toward zero; `02_hardware_energy.md`, section 3 and Figure 5: about 68 KiB per PE left for the network with `lif`; section 7: most models, including `lif`, hold at most 256 neurons per PE, limited by the 8-bit target index. Variants trade the budgets: `lif_no_delay` drops the delay for 8-bit weights. The physical order of the fields in the word is not claimed. This answers the question left open in block 3 ("Why only −15 to 15?").

Transition to slide 5.7 (spoken): "Other neuron models split these 16 bits differently, or compute differently."

### Slide 5.7: Neurons are software: the chip runs more than LIF

- Kicker: SPINNAKER2 HARDWARE · NEURON MODELS
- Title: Neurons are software: the chip runs more than LIF
- Subtitle (two lines, no bullets): Other models add an adaptive threshold, noise or richer dynamics, and variants split the 16 bits differently. Today we only use lif; the other models are documented for you to explore.
- Visual: a simple table (thin grey lines, bold header, model names in monospace), at least 16 pt:

| Model | What it adds | Used for |
|---|---|---|
| `lif` | the model of this workshop | – |
| `lif_no_delay` | no delay, weights −127 to 127 | trained networks imported via NIR (after the break) |
| `alif` | a threshold that rises after each spike and decays back | longer memory, e.g. sequence tasks |
| `lif_prob` | fires with a probability once above the threshold | sampling, optimisation |
| `izhikevich` | biological firing patterns such as bursting | neuroscience |
| `qubo_neuron` | built for optimisation problems | the Max-Cut demo at the end of the afternoon |

- One line below the table, normal text size: "Read more: Spiking Neurons and Networks, section 5 (workshop knowledge base) · vendor tutorial 01, section 2 (neuron models) · your own model: vendor tutorial 09 · all models and parameters: py-spinnaker2 API docs, neuron models"
- Source line: "Source: Spiking Neurons and Networks, section 5 (workshop knowledge base); py-spinnaker2 v0.8.5"
- No bullets, no boxes, no speaker notes

Facts behind the slide: all six model names checked in py-spinnaker2 v0.8.5 (`snn.Population(neuron_model=...)`); `lif_no_delay` uses `SynapseWordSpec(weight=7, delay=0, synapse_type=1, target=8)`, i.e. weights −127 to 127 and no delay (`neuron_models/lif_neuron.py`); the NIR import maps LIF neurons onto `lif_no_delay` (`01_primer_snn_basics.md`, section 8). "What it adds" and "used for" follow `01_primer_snn_basics.md`, section 5 (ALIF, Izhikevich, probabilistic LIF, QUBO neuron). Vendor tutorial 01 is "Core concepts: populations, neuron models & parameters", section 2 "Neuron models"; tutorial 09 is "Custom neuron models basics". The SNN note plans 1 min for this ("name them, show that the chip is programmable and not fixed to one model"). Custom neuron models in C are an outlook for block 10.

Transition (spoken): "That is where your network runs. Now you build a larger one yourself: notebook 02."

Moved to other blocks (decided 2026-11-16): what a chip run costs in energy (board baseline 57 W, cost per neuron and step and per spike, small networks invisible on the power meter) goes to block 9 (energy demo) and block 10; the time per chip run (about a minute, mostly power-up and boot, 6 boards shared) and why development happens on Brian2 go to the hands-on slide of block 6 (notebook 02).

### PowerPoint prompt for block 5 (slides 5.0 to 5.5; slides 5.6 and 5.7 in the prompt below)

```
Add block 5 ("SPINNAKER2 HARDWARE") to the deck, directly after the last slide of block 3 ("On the chip, weights are small integers"). Use exactly the same slide elements as the block 1 and block 3 content slides (section label in the side band, kicker line above the title, title, subtitle, one figure, source line, slide number) and the same divider design as the other blocks. Accent colour for this block: HPI blue (#007A9E) for the side band, the divider and the title rule. Do not change any other slide.

Figure paths are relative to /sc/home/david.goll/projects/spinnaker/workshop-spinnaker2/. Place each figure below the subtitle, aspect ratio kept, as large as the space allows, centred. No bullets, no boxes, no speaker notes.

Slide 5.0 (divider)
- Section number: 5
- Section title: SpiNNaker2 hardware
- Section time: 14:55 · 15 min

Slide 5.1
- Kicker: SPINNAKER2 HARDWARE · FROM PYTHON TO THE CHIP
- Title: From Python to the cores: what happens when you call hw.run
- Subtitle (two lines): "You describe the network in Python and choose the neuron model by name. py-spinnaker2 turns it into network data (parameters, weights, routing tables) and compiles the neuron model's C code for the ARM cores, sends both to the board, and every core runs its part directly on the hardware, without an operating system."
- Figure: 01_knowledge_base/figures/00_computing_fundamentals/06_bare_metal_cross_compilation.png
- Source line: "Source: Computing Fundamentals, section 6 (workshop knowledge base)"

Slide 5.2
- Kicker: SPINNAKER2 HARDWARE · INSTALLATION
- Title: Where your network runs: from the cluster to one chip
- Subtitle (two lines): "py-spinnaker2 runs on the cluster node cx51, which talks to a frame of 6 boards over Ethernet. A run reserves one board with 48 chips, 7,104 cores available for your network; each chip is about 1 cm × 1 cm with 152 processing elements."
- Figure: 01_knowledge_base/figures/02_hardware_energy/01_installation_hierarchy.png
- Source line: "Source: Hardware and Energy, sections 1 and 5 (workshop knowledge base)"

Slide 5.3
- Kicker: SPINNAKER2 HARDWARE · CHIP
- Title: Inside one chip: 152 small cores, each with its own memory
- Subtitle (two lines): "Four processing elements (PEs) form a quad PE (QPE); each PE is an ARM core with 128 KB of local memory. A spike leaves its PE as a small packet: by default py-spinnaker2 sends one packet to each PE with target neurons; the router can also copy a single packet to all of them (multicast)."
- Figure: 01_knowledge_base/figures/02_hardware_energy/01_chip_schematic.png
- Source line: "Source: Hardware and Energy, sections 1, 2 and 4 (workshop knowledge base); Scholze et al. 2026; py-spinnaker2 tutorial 06"

Slide 5.4
- Kicker: SPINNAKER2 HARDWARE · ONE TIME STEP
- Title: Inside one PE: what happens in one time step
- Subtitle (two lines): "A timer wakes the core. It reads the spikes that arrived, looks up their synapses in its memory and adds the weights to its neurons, updates all its neurons and sends the new spikes. Then it sleeps until the next tick."
- Figure: 01_knowledge_base/figures/02_hardware_energy/02_pe_function.png
- Source line: "Source: Hardware and Energy, section 2 (workshop knowledge base); Scholze et al. 2026; py-spinnaker2 tutorial 06; snn-core code"

Slide 5.5
- Kicker: SPINNAKER2 HARDWARE · TIME STEPS
- Title: One PE over ten time steps: work, then sleep
- Subtitle (two lines): "Each step starts with a timer tick. The more spikes arrive, the longer the core works; in a sparse network it sleeps most of the time. If too many spikes arrive in one step, the work does not fit and the next step starts late."
- Figure: 01_knowledge_base/figures/02_hardware_energy/02_pe_timestep.png
- Source line: "Source: Hardware and Energy, sections 2 and 7 (workshop knowledge base); illustration, durations made up"

Report the final slide order of block 5.
```

### PowerPoint prompt for block 5, slides 5.6 and 5.7

```
Add two slides at the end of block 5 ("SPINNAKER2 HARDWARE"), directly after the slide "One PE over ten time steps: work, then sleep". Use the same slide elements and accent colour as the other block 5 slides. Do not change any other slide. No bullets, no boxes, no speaker notes.

Slide 5.6
- Kicker: SPINNAKER2 HARDWARE · MEMORY
- Title: Why weights are small integers: one synapse is one 16-bit word
- Subtitle (two lines): "Every PE keeps the synapses of its neurons in its own 128 KB of memory, about 68 KiB of which is left for the network with lif. To fit, each synapse is packed into 16 bits: 4 bits weight plus a sign, 3 bits delay, 8 bits for the target neuron."
- Visual, drawn with shapes, centred below the subtitle, as wide as the content area: a row of 16 equal small squares (one per bit), grouped into four fields by a thicker outline and a label above each field:
  "weight (4 bits)" | "sign (1 bit)" | "delay (3 bits)" | "target neuron (8 bits)"
  Fill the weight and sign squares in the block's accent colour, the delay and target squares in light grey.
  Under the fields, in larger text: under weight and sign together "weights −15 to 15", under delay "delays 0 to 7", under target "at most 256 neurons per PE".
  Small grey note below the row: "order of the fields schematic"
- Source line: "Source: Spiking Neurons and Networks, section 4; Hardware and Energy, section 3 (workshop knowledge base); py-spinnaker2 v0.8.5 code"

Slide 5.7 (last slide of block 5)
- Kicker: SPINNAKER2 HARDWARE · NEURON MODELS
- Title: Neurons are software: the chip runs more than LIF
- Subtitle (two lines): "Other models add an adaptive threshold, noise or richer dynamics, and variants split the 16 bits differently. Today we only use lif; the other models are documented for you to explore."
- Visual: a table with three columns (thin grey lines, bold header, model names in a monospace font), at least 16 pt:
  Model | What it adds | Used for
  lif | the model of this workshop | –
  lif_no_delay | no delay, weights −127 to 127 | trained networks imported via NIR (after the break)
  alif | a threshold that rises after each spike and decays back | longer memory, e.g. sequence tasks
  lif_prob | fires with a probability once above the threshold | sampling, optimisation
  izhikevich | biological firing patterns such as bursting | neuroscience
  qubo_neuron | built for optimisation problems | the Max-Cut demo at the end of the afternoon
- One line below the table, normal text size: "Read more: Spiking Neurons and Networks, section 5 (workshop knowledge base) · vendor tutorial 01, section 2 (neuron models) · your own model: vendor tutorial 09 · all models and parameters: py-spinnaker2 API docs, neuron models"
- Source line: "Source: Spiking Neurons and Networks, section 5 (workshop knowledge base); py-spinnaker2 v0.8.5"

Report the final slide order of block 5.
```

## Block 6: hands-on 2 (15:10, 20 min)

Notebook `04_workshop_material/02_direction_detector.ipynb`. Accent colour: HPI orange, as for hands-on 1 (to be confirmed).

### Slide 6.0: divider

- Section number: 6
- Section title: Hands-on 2: a network on the chip
- Section time: 15:10 · 20 min

### Slide 6.1: Hands-on 2: a network on the chip

- Kicker: HANDS-ON 2 · NOTEBOOK 02
- Title: Hands-on 2: build a network and run it on the chip
- Subtitle (two lines, no bullets): Notebook 04_workshop_material/02_direction_detector.ipynb, 20 minutes. Build a layer of two neurons that tells in which direction a dot moves across four pixels, with weights and delays as matrices.
- Visual: `02_workshop_design/slides/figures/b6_detector.png` (made by `b6_make_detector.py`: four pixels in a row, each connected to two detectors; the rightward connections labelled with their delays 3, 2, 1, 0, the leftward ones with "?" (to fill in); a dot moving right makes all four spikes arrive in step 9; schematic)
- Below the figure, a short two-column text block (the one exception to "no bullets" on this slide, because it is the task):
  - left, "Everyone (Brian2)": "Sections 1 to 3: fill in the delays of the leftward detector and run it · Section 5: Try 1, 2 and 4, then 3 if time"
  - right, "HPI cluster pairs (chip)": "Section 4, as soon as section 3 works: set USE_HARDWARE = True and run the cell once · A chip run takes about a minute, mostly powering up and booting the board · 6 boards for everyone: if all are busy, your run waits"
- Source line: none (task slide)
- No boxes, no speaker notes

Facts behind the slide: notebook 02 sections 1 (the input, animation and raster), 2 (weight and delay matrices; participants fill in the leftward delays), 3 (run and read the answer, animation), 4 (chip run, compares with Brian2 and reads `time_done`, once per pair as soon as section 3 works), 5 (Try 1, 2 and 4 core, 3 if time), 6 (what you built); the API reference is a collapsible at the start; about one minute per chip run, mostly power-up and boot, regardless of network size; one run reserves one of 6 boards and waits if all are busy (`02_participant_access.md`, capacity; notebook 02, section 3). Why development happens on Brian2 (moved here from block 5): same code, seconds instead of a minute, no waiting for a board.

### PowerPoint prompt for block 6 (slides 6.0 and 6.1)

```
Add block 6 to the deck, directly after the last slide of block 5 ("Neurons are software: the chip runs more than LIF"). Use the same slide elements as the hands-on slide of block 3 (section label in the side band, kicker, title, subtitle, figure, slide number) and the same divider design as the other blocks. Accent colour: HPI orange (#DD6108). Do not change any other slide. No boxes, no speaker notes.

Slide 6.0 (divider)
- Section number: 6
- Section title: Hands-on 2: a network on the chip
- Section time: 15:10 · 20 min

Slide 6.1
- Section label: HANDS-ON 2
- Kicker: HANDS-ON 2 · NOTEBOOK 02
- Title: Hands-on 2: build a network and run it on the chip
- Subtitle (two lines): "Notebook 04_workshop_material/02_direction_detector.ipynb, 20 minutes. Build a layer of two neurons that tells in which direction a dot moves across four pixels, with weights and delays as matrices."
- Figure: /sc/home/david.goll/projects/spinnaker/workshop-spinnaker2/02_workshop_design/slides/figures/b6_detector.png, below the subtitle, centred, aspect ratio kept, using about the upper half of the remaining space.
- Below the figure, two text columns of equal width (at least 16 pt, plain text, short bullet lines allowed here because this is the task):
  Left, heading "Everyone (Brian2)":
    · Sections 1 to 3: fill in the delays of the leftward detector and run it
    · Section 5: Try 1, 2 and 4, then 3 if time
  Right, heading "HPI cluster pairs (chip)":
    · Section 4, as soon as section 3 works: set USE_HARDWARE = True and run the cell once
    · A chip run takes about a minute, mostly powering up and booting the board
    · 6 boards for everyone: if all are busy, your run waits
- No source line.

Report the final slide order of blocks 5 and 6.
```

## Block 7 onwards

Part 2 (block 7 onwards, including the slide on the LIF layer as a recurrent cell, moved from block 3) is in `06_slide_content_part2.md`.
