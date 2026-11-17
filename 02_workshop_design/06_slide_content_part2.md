# Slide content, part 2

Content of the slides for the second half of the workshop (15:45 to 17:00), block by block. Same slide style and format as part 1 (`05_slide_content_part1.md`, section "Slide style"): a title that carries the message, a subtitle of one or two lines, one visual, no bullets. Open points are marked *open*.

## Block 7: from PyTorch to the chip (15:45, 10 min)

Style for all slides of this block: same elements as the content slides of blocks 1, 3 and 5 in `slides/block1_draft.pptx` (section label in the side band, kicker line above the title, title, subtitle, one visual, source line, slide number). Accent colour: *open*. The new figures use HPI red (#B1063A) as their one accent; the colour is one constant at the top of each script and can be changed to the block colour. Section label: "FROM PYTORCH TO THE CHIP". Kicker: "FROM PYTORCH TO THE CHIP · <topic>".

Role of the block: it comes right after the break and prepares hands-on 3 (notebooks 03 and 04). What the notebooks assume and the slides so far have not covered: that training happens off the chip, NIR, how a spiking network is trained, and that the conversion has to be checked. Covered earlier and only referred to here: coincidence detection and delays (3.5, 3.7), integer weights and the 16-bit synapse word (3.8, 5.6); the RNN cell is new here (moved from block 3). Not in this block: energy (blocks 9, 10), event cameras (the demo in block 9; notebook 04 explains them in one paragraph), how the trained network tells the direction (notebook 03, "After the workshop", and the heatmap in notebook 04). The conversion settings (dt, integrator, reset), the 8-bit weights of `lif_no_delay` and the one-step delay per projection are taught in notebook 03, section 5, where participants set them, not on the slides (decided 2026-11-18).

Structure (as in `slides/status_1811.pptx`, reworked 2026-11-18): why training happens off the chip (7.1), how a spiking layer is trained (7.2 to 7.4), and that the conversion must be checked (7.5). Five content slides in 10 minutes, about two minutes each. Dropped: the debrief slide "From the hand-built detector to a trained one" (its question is asked in the closing of block 6), and the separate slides on the conversion rule and on what changes on the chip (merged into 7.5; details in notebook 03).

### Slide 7.0: divider

- Same divider as the other blocks in the deck (section number, section title, time)
- Section number: 7
- Section title: From PyTorch to the chip
- Section time: 15:45 · 10 min

### Slide 7.1: Train here, run there

- Kicker: FROM PYTORCH TO THE CHIP · NIR
- Title: Train on a normal computer, run on the chip: NIR carries the network across
- Subtitle (two lines, no bullets): py-spinnaker2 has no learning rules, so training runs in PyTorch, on a CPU or GPU. NIR, a shared file format for spiking networks (like ONNX for deep learning), stores the trained graph, and py-spinnaker2 imports it as the populations and projections you built by hand in notebook 02.
- Visual: `01_knowledge_base/figures/01_primer_snn_basics/08_deployment_pipeline.png` (train, export to NIR, import with s2_nir, map onto the chip, run; the knowledge-base figure as it is, shown for an MNIST network)
- Source line: "Source: Spiking Neurons and Networks, section 8 (workshop knowledge base); Pedersen et al. 2024 (NIR)"
- No bullets, no boxes, no speaker notes

Facts behind the slide: Figure 24 of the SNN note; its stages 4 and 5 are schematic (core allocation estimated, output spikes made up), and the figure shows an MNIST network, not the direction task. py-spinnaker2 v0.8.5 has no learning rules: training happens off the chip, the chip runs the trained network (inference); on-chip learning exists in research, as custom code. NIR: [Pedersen et al. 2024, Nature Communications](https://doi.org/10.1038/s41467-024-52259-9), 7 simulators and 4 hardware platforms, SpiNNaker2 among them. The import is `s2_nir.from_nir(graph, config)` (notebook 03, section 5). *Open:* the figure's stage 5 refers to "the digit of Figure 19", a cross-reference inside the knowledge base; acceptable on the slide, or regenerate a slide version without it. Transition (spoken): "So the training happens in PyTorch. What does a spiking layer look like there?"

### Slide 7.2: An LIF layer is a recurrent cell with spikes as output

Moved here from the end of block 3 on 2026-11-16 (was slide 7.1 in `05_slide_content_part1.md`).

- Kicker: FROM PYTORCH TO THE CHIP · DEEP LEARNING
- Title: An LIF layer is a recurrent cell with spikes as output
- Subtitle (two lines, no bullets): Like an RNN, the layer carries its state from step to step: v[t] = α · v[t−1] + W · x[t]. The output is a spike, 0 or 1, instead of a continuous activation, and the same weights act in every step.
- Visual: `01_knowledge_base/figures/01_primer_snn_basics/08_lif_unrolled.png` (an LIF layer unrolled over three time steps, drawn like an RNN; the knowledge-base figure as it is)
- Source line: "Source: Spiking Neurons and Networks, section 8 (workshop knowledge base)"
- No bullets, no boxes, no speaker notes

Facts behind the slide: Figure 22 of the SNN note; training works as for an RNN, with backpropagation through time (BPTT), except that the step function has no useful gradient. In snnTorch, this layer is `snn.Leaky`: `beta` is the α of the formula, the same as `alpha_decay` in py-spinnaker2 (notebook 03, section 2). Transition (spoken): "So we can unroll it and backpropagate through time, like an RNN. One problem is left: the spike."

### Slide 7.3: The spike has no useful gradient

- Kicker: FROM PYTORCH TO THE CHIP · TRAINING
- Title: The spike has no useful gradient: training replaces it with a smooth stand-in
- Subtitle (two lines, no bullets): In the forward pass the neuron fires at the hard threshold, exactly as on the chip. In the backward pass the derivative of the step, zero almost everywhere, is replaced by a smooth bump, so that backpropagation through time can tell each weight which way to move.
- Visual: `01_knowledge_base/figures/01_primer_snn_basics/08_surrogate_gradient.png` (A: the spike as a step function; B: its true derivative and the surrogate; the knowledge-base figure as it is)
- Source line and "Read more" line: see the prompt "sources on the surrogate gradient slide" at the end of this block
- No bullets, no boxes, no speaker notes

Facts behind the slide: Figure 23 of the SNN note. The surrogate in the figure is snnTorch's fast sigmoid with slope 5, for visibility; snnTorch's default slope is 25 (`surrogate.fast_sigmoid(slope=25)`, checked in the installed snnTorch), and notebooks 03 and 04 use `surrogate.fast_sigmoid()` with that default. Only neurons whose potential is near the threshold get a gradient. The method is called surrogate-gradient learning ([Neftci, Mostafa and Zenke 2019, IEEE Signal Processing Magazine](https://doi.org/10.1109/MSP.2019.2931595)); the tutorial-style overview is [Eshraghian et al. 2023, Proceedings of the IEEE](https://doi.org/10.1109/JPROC.2023.3308088).

### Slide 7.4: Spike counts are the logits

- Kicker: FROM PYTORCH TO THE CHIP · TRAINING
- Title: The answer is the output neuron that fires most often: spike counts are the logits
- Subtitle (two lines, no bullets): One output neuron per class; its spike count is the logit. Cross-entropy trains the right neuron to fire most, and on the chip the neuron with the most spikes gives the answer.
- Visual: `02_workshop_design/slides/figures/b7_spike_counts.png` (the four output neurons of the trained network of notebook 04 for one test example, a bar moving right: spikes over 30 time steps and the count of each; "right" fires 5 times, "down" once, the others not)
- Source line: "Source: notebook 04, trained in snnTorch"
- No bullets, no boxes, no speaker notes

Facts behind the slide: notebooks 03 and 04, section 3: `loss = F.cross_entropy(counts, labels)` with `counts` the summed output spikes; the answer is the output with the highest count (a tie or no spike at all counts as wrong). Cross-entropy turns the counts into probabilities with softmax and penalises a low probability of the right class: for the counts 5, 0, 1, 0 of the figure, p(right) ≈ 0.97 and the loss ≈ 0.03; with no spikes at all, every p is 0.25 and the loss is ln 4 ≈ 1.39. The counts are raw counts over the 30 steps, not frequencies (softmax depends on the scale; the answer does not). Spoken explanation in one phrase: "Count the spikes, treat the counts as class scores, and train with the usual classification loss: the right neuron learns to fire most." The figure is generated by `b7_make_spike_counts.py`, which trains the network exactly as notebook 04 does (its code cells up to the training cell, seed 0) and picks the first test example moving right that is answered correctly with a clear margin (test example 4: counts 5, 0, 1, 0). Transition (spoken): "That is all the training needs. One thing is left before the chip runs it: checking that the conversion kept the network the same."

### Slide 7.5: Check the conversion

Replaces the former slides "The conversion rule for snnTorch models" and "What changes on the chip" (2026-11-18). No settings table on the slide: the settings are taught in notebook 03, section 5, where participants set them, with a collapsible that explains each one.

- Kicker: FROM PYTORCH TO THE CHIP · CONVERSION
- Title: A few settings must match the training framework, and a wrong one gives no error
- Subtitle (two lines, no bullets): NIR carries the weights and neurons across, but the time step, the integrator and the reset rule have to be set to match snnTorch. A mismatch only shows up as different spikes, so notebook 03 compares the converted network spike for spike with snnTorch.
- Visual: `02_workshop_design/slides/figures/b7_integrator.png` (one neuron, input 0.75 in steps 0 and 2: with decay 0.5, as trained, it stays below the threshold; with 0.607, the default conversion, it fires; illustration, computed here)
- Source line: "Source: py-spinnaker2 v0.8.5, s2_nir; illustration computed here; settings: notebook 03, section 5"
- No bullets, no boxes, no speaker notes

Facts behind the slide: snnTorch exports `beta` as τ = Δt / (1 − β) with Δt = 1e-4 s; py-spinnaker2 converts τ back with `FORWARD`, α = 1 − Δt/τ (= β), or `EXPONENTIAL` (its default), α = e^(−Δt/τ); for β = 0.5 that is 0.5 against 0.607. NIR does not store the reset rule. The rule for snnTorch models: `cfg.dt = 1e-4`, `cfg.integrator = FORWARD`, `cfg.reset` matching `reset_mechanism` (`ZERO` in the notebooks); the same rule is in the py-spinnaker2 tutorial 08 and the knowledge base, section 8. Measured in notebook 03 on Brian2, 60 inputs: correct settings, hidden and output spikes identical in 60 of 60; `EXPONENTIAL`, hidden identical in 30 and output in 44 of 60; reset `SUBTRACT`, hidden identical in 20 and output in 1 of 60. The answers barely change, the spikes do: that is why the notebook compares spike for spike. Two more differences, explained in the notebook only: the NIR import uses `lif_no_delay`, with 8-bit weights (−127 to 127) scaled by `scale_weights` and no delays; and each projection adds one time step, so the chip's output comes one step later per layer than in snnTorch. The figure is generated by `b7_make_integrator.py`, which checks the decay values and that only the 0.607 neuron fires. `b7_synapse_words.png` is no longer used on a slide. Transition to hands-on 3 (spoken): "Notebook 03 trains a network on your four pixels and runs exactly this check; notebook 04 does the same task on an 8 × 8 event camera."

### PowerPoint prompt: rework block 7 to five slides (2026-11-18)

```
In status_1811.pptx, block 7 ("FROM PYTORCH TO THE CHIP"), make the following changes. Do not change any other slide, and keep the style, layout and figures of the block as they are unless stated below.

1. Slide "The answer is the output neuron that fires most often: spike counts are the logits": replace the subtitle with
   "One output neuron per class; its spike count is the logit. Cross-entropy trains the right neuron to fire most, and on the chip the neuron with the most spikes gives the answer."

2. Merge the slides "Convert snnTorch models with dt = 1e-4 and FORWARD: a wrong setting gives no error" and "On the chip, a trained layer has no delays, 8-bit weights and one step of delay per layer" into one slide. Keep the first of the two slides and delete the second. If either slide contains a settings table, remove it. On the remaining slide:
   - Kicker: FROM PYTORCH TO THE CHIP · CONVERSION
   - Title: A few settings must match the training framework, and a wrong one gives no error
   - Subtitle (two lines): "NIR carries the weights and neurons across, but the time step, the integrator and the reset rule have to be set to match snnTorch. A mismatch only shows up as different spikes, so notebook 03 compares the converted network spike for spike with snnTorch."
   - Figure: 02_workshop_design/slides/figures/b7_integrator.png (path relative to /sc/home/david.goll/projects/spinnaker/workshop-spinnaker2/), below the subtitle, aspect ratio kept, as large as the space allows, centred
   - Source line: "Source: py-spinnaker2 v0.8.5, s2_nir; illustration computed here; settings: notebook 03, section 5"

3. Renumber the slide numbers of the block if they are fields that do not update by themselves.

Report the final order and titles of the block 7 slides.
```

### PowerPoint prompt: sources on the surrogate gradient slide (2026-11-18)

```
In status_1811.pptx, block 7 ("FROM PYTORCH TO THE CHIP"), change only the slide titled "The spike has no useful gradient: training replaces it with a smooth stand-in" (or its revised title "The spike has no useful gradient: training uses a smooth stand-in"). Do not change its title, subtitle, figure, layout or any other slide.

1. Replace the source line with:
   "Source: Neftci, Mostafa and Zenke 2019, Surrogate Gradient Learning in Spiking Neural Networks, IEEE Signal Processing Magazine (doi.org/10.1109/MSP.2019.2931595); Spiking Neurons and Networks, section 8 (workshop knowledge base)"
   Make "doi.org/10.1109/MSP.2019.2931595" a hyperlink to https://doi.org/10.1109/MSP.2019.2931595. Keep the source line's existing style (small, grey, bottom of the slide); if it no longer fits on one line, let it wrap to two.

2. Add one line directly above the source line, in the same small grey style, left-aligned with it:
   "Read more: Eshraghian et al. 2023, Training Spiking Neural Networks Using Lessons From Deep Learning, Proceedings of the IEEE · hands-on: snnTorch tutorials 5 and 6"
   Hyperlink "Eshraghian et al. 2023" to https://doi.org/10.1109/JPROC.2023.3308088 and "snnTorch tutorials 5 and 6" to https://snntorch.readthedocs.io/en/latest/tutorials/tutorial_5.html

3. Make sure neither line overlaps the figure; if necessary, shrink the figure slightly, keeping its aspect ratio.

Report the final text of both lines.
```

## Block 9: instructor demos (16:35, 10 min)

Same slide style as block 7 (section label in the side band, kicker, title, subtitle, one visual, source line, slide number). Section label: "DEMOS". Kicker: "DEMOS · <topic>".

Role of the block: no interactive part any more. The instructor shows, teases and links; no code, no details behind the curtain (decided 2026-11-18). Order: the basics of data encoding (9.1), the vendor's examples page shown live in the browser (9.2), then the energy measurement with the demo from the break (9.3, 9.4), and where to read on (9.5). The number of spikes links encoding and energy. No live NMNIST or Max-Cut run: both appear on the examples page (`demos/02_nmnist.ipynb` and `demos/03_maxcut.ipynb` stay prepared). Timing: 9.1 about 2 min, 9.2 about 1 to 2 min, 9.3 and 9.4 about 5 to 6 min, 9.5 under a minute.

### Slide 9.0: divider

- Section number: 9
- Section title: Demos: how data gets in, and energy
- Section time: 16:35 · 10 min

### Slide 9.1: Data enters as spikes, and the encoding decides how many

- Kicker: DEMOS · INPUT
- Title: Data enters as spikes, and the encoding decides how many
- Subtitle (two lines, no bullets): The same MNIST digit as latency code, where each pixel fires once and bright pixels fire first, needs 116 spikes; as rate code, where bright pixels fire often, 619 spikes in 50 steps. Event cameras need no encoding: they deliver spikes themselves.
- Visual: `01_knowledge_base/figures/01_primer_snn_basics/06_mnist_encoding.png` (A: the digit; B: spike time of each pixel; C: latency code, 116 spikes; D: rate code, 619 spikes; the knowledge-base figure as it is)
- Source line: "Source: Spiking Neurons and Networks, section 6 (workshop knowledge base); MNIST test set, first digit"
- No bullets, no boxes, no speaker notes

Facts behind the slide: Figure 19 of the SNN note; latency code t = t_max (x_max − x) / x_max, rate code with p = 0.25 · x / 255 per step over 50 steps. Both encoders are built into py-spinnaker2 (`spikes_from_array_latency_code`, `poisson_process`); notebooks 02 to 04 gave spike times directly (`spike_list`). SpiNNcloud has no notebook that explains encoding (checked 2026-11-18 for v0.8.5: the NMNIST example uses event-camera data, tutorial 03 a binary toy image with every bright pixel spiking in every step); the best explanation is snnTorch tutorial 1 (rate, latency and delta coding on MNIST), linked on 9.5. Transition (spoken): "How does this look in real applications? The vendor collects complete examples."

### Slide 9.2: The vendor's examples (live in the browser)

- Kicker: DEMOS · EXAMPLES
- Title: Complete examples: from event-camera digits to graph problems
- Subtitle (one line, no bullets): The py-spinnaker2 documentation collects complete examples; three of them, in one sentence each.
- Visual: screenshot of https://spinnaker2.gitlab.io/py-spinnaker2/examples/index.html (the table of the five examples), as the backup if the browser or the network fails. Live: switch to the page, opened in a browser tab before the workshop.
- Source line: "Source: py-spinnaker2 documentation, examples (spinnaker2.gitlab.io/py-spinnaker2/examples)"
- No bullets, no boxes, no speaker notes

What to say, one sentence per example (spoken, not on the slide):

- **05 NMNIST with a pre-trained NIR model:** MNIST recorded with an event camera; the camera delivers spikes itself, so no encoding is needed, and a converted network classifies them on the chip.
- **01 Clustered SNN:** a network driven by random (Poisson-like) input, a rate code.
- **02 QUBO Max-Cut:** the chip does more than classify: noisy spiking neurons search for the best split of a graph (we ran the 5- and 8-node graphs on our chips; the large graphs gave results no better than random).

Facts behind the slide: the examples page of py-spinnaker2 lists five examples (01 clustered SNN, 02 QUBO Max-Cut, 03 end-to-end NIR deployment, 04 bidirectional streaming, 05 NMNIST), checked 2026-11-18. NMNIST: Orchard et al. 2015, event camera with three saccades in front of a screen showing the MNIST digits; the example bins the events into 1 ms frames and gives each pixel and polarity one spike source (2 × 34 × 34 = 2,312). Max-Cut: `demos/03_maxcut.ipynb` and `04_applications.md`, section 2.1. *Open:* take the screenshot (`02_workshop_design/slides/figures/b9_examples_page.png`, browser at slide width, table fully visible). Transition (spoken): "Back to the spikes: every spike costs energy. How much? We measured it during the break."

### Slide 9.3: The board draws 57 W just for being on

Decided 2026-11-18: the slide shows the plot of the live run from `demos/01_energy.ipynb` (section 3) instead of `b9_power.png`; on 2026-11-17 it read 58 W silent and 63 W active against the measured empty board at 57 W. `b9_power.png` stays as the backup.

- Kicker: DEMOS · ENERGY
- Title: The board draws 57 W just for being on; spiking adds to that
- Subtitle (two lines, no bullets): The same network on 1,000 cores of one board, run during the break: silent, it barely moves the reading; with every neuron spiking in every step, it adds 6 to 9 W. The board reports power in 3 W steps, so a workshop network of a few cores would not show at all.
- Visual: `02_workshop_design/slides/figures/b9_power.png` (board power over a 20 s run: empty board 57 W, 1,000 silent cores 60 W, 1,000 active cores 66 W; measured)
- Source line: "Source: measured on one 48-chip board of the HPI cluster, 2026-10-19 (workshop repository, 05_measurements/01_power_baseline)"
- No bullets, no boxes, no speaker notes

Facts behind the slide: `05_measurements/01_power_baseline/README.md`. The power is that of the whole board (48 chips with their DRAM), read from the frame's controller in steps of 3 W (every reading is a multiple of 3), about once per second; the steady value is the mean after the first 2 s. Silent: 100 `lif` neurons per core, all-to-all, no input; active: the same with an input above the threshold, so every neuron spikes in every step, 10,000 synaptic events per core and step, 10 billion per second on the board. Up to 100 active cores the reading stays at 57 W. The figure is generated by `b9_make_power.py`, which checks the three steady values. Live: if the runs started in the break (`demos/01_energy.ipynb`, section 2) completed, switch to section 3 of the notebook, which plots the live runs next to the measured empty board; the live numbers differ by a few watts between runs (9 November: 60 W silent, 63 W active). With v0.8.5 the active run reported an error on one PE (to-do list); the measured figure on this slide is the main version, the live run a bonus. Transition (spoken): "So what does a watt here mean?"

### Slide 9.4: Above the baseline, energy follows the spikes

- Kicker: DEMOS · ENERGY
- Title: Above the baseline, the energy follows the spikes: roughly 0.6 nJ per synaptic event
- Subtitle (two lines, no bullets): The more cores spike, the more the board draws; silent cores cost almost nothing extra. The 6 W that spiking adds, divided by 10 billion synaptic events per second, give about 0.6 nJ per event. Ask of every energy number: what is the baseline, and what is included?
- Visual: `02_workshop_design/slides/figures/b9_power_vs_load.png` (steady board power against the number of cores with a network, log scale, active and silent, the empty board as a dashed line, the +6 W from spikes at 1,000 cores marked with ≈ 0.6 nJ per synaptic event; measured)
- Source line: "Source: measured on the HPI cluster, 2026-10-19; for comparison: Höppner et al. 2021 (test chip, about 0.2 nJ per synaptic event)"
- No bullets, no boxes, no speaker notes

Facts behind the slide: 1,000 cores active 66 W against silent 60 W: 6 W / 10¹⁰ events per second = 0.6 nJ per synaptic event, including the neuron updates and sending the spikes; 3,000 cores give 0.3 nJ, 7,000 cores 0.4 nJ. Given the 3 W resolution and the non-proportional increase, a rough estimate, not a measurement of the chip's energy per event (`05_measurements/01_power_baseline/README.md`, "Energy per synaptic event, roughly"). The PE architecture paper measured 0.20–0.26 nJ per synaptic event and 1.5–1.9 nJ per neuron update on a 22FDX test chip with 8 PEs ([Höppner et al. 2021](https://arxiv.org/abs/2103.08392); `01_knowledge_base/02_hardware_energy.md`, section 8). The 57 W baseline is spent whether the network computes or not: it is the reason to ask for the baseline and the batch size behind every "× more efficient" (block 10 picks this up). The figure is generated by `b9_make_power_vs_load.py` from `05_measurements/01_power_baseline/data/summary.csv`; it checks 57, 60 and 66 W and the 0.6 nJ. Transition (spoken): "That is why the 116 spikes of the latency code matter: fewer spikes, less energy above the baseline. Where to read on:"

### Slide 9.5: Read on

Exception to the slide style: a list of links, no figure; short, since the examples page (9.2) already covers the vendor's material.

- Kicker: DEMOS · READ ON
- Title: To read on after the workshop
- Body (three short groups, one line each, links clickable):
  - Getting data in: workshop note "Spiking Neurons and Networks", section 6 · snnTorch tutorial 1, spike encoding (https://snntorch.readthedocs.io/en/latest/tutorials/tutorial_1.html)
  - Examples: py-spinnaker2 examples (https://spinnaker2.gitlab.io/py-spinnaker2/examples/index.html)
  - Energy: py-spinnaker2 user guide, power measurement (https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/power_measurement.html) · our measurement: workshop repository, 05_measurements/01_power_baseline · workshop note "SpiNNaker2 hardware and energy", sections 8 and 9
- Source line: none

### PowerPoint prompt for block 9 (slides 9.0 to 9.5)

```
In status_1811.pptx, add block 9 ("DEMOS") directly after the last slide of block 8 (or, if block 8 has no slides, after the last slide of block 7). If an earlier version of block 9 is already in the deck, replace it completely. Use exactly the same slide elements as the block 7 content slides (section label in the side band, kicker line above the title, title, subtitle, one figure, source line, slide number) and the same divider design as the other blocks. Do not change any other slide.

Figure paths are relative to /sc/home/david.goll/projects/spinnaker/workshop-spinnaker2/. Place each figure below the subtitle, aspect ratio kept, as large as the space allows, centred. No bullets, no boxes, no speaker notes, except where stated for slide 9.5.

Slide 9.0 (divider)
- Section number: 9
- Section title: Demos: how data gets in, and energy
- Section time: 16:35 · 10 min

Slide 9.1
- Kicker: DEMOS · INPUT
- Title: Data enters as spikes, and the encoding decides how many
- Subtitle (two lines): "The same MNIST digit as latency code, where each pixel fires once and bright pixels fire first, needs 116 spikes; as rate code, where bright pixels fire often, 619 spikes in 50 steps. Event cameras need no encoding: they deliver spikes themselves."
- Figure: 01_knowledge_base/figures/01_primer_snn_basics/06_mnist_encoding.png
- Source line: "Source: Spiking Neurons and Networks, section 6 (workshop knowledge base); MNIST test set, first digit"

Slide 9.2
- Kicker: DEMOS · EXAMPLES
- Title: Complete examples: from event-camera digits to graph problems
- Subtitle (one line): "The py-spinnaker2 documentation collects complete examples; three of them, in one sentence each."
- Figure: 02_workshop_design/slides/figures/b9_examples_page.png (a screenshot of the examples page; if the file does not exist yet, leave a placeholder box labelled "screenshot: spinnaker2.gitlab.io/py-spinnaker2/examples")
- Source line: "Source: py-spinnaker2 documentation, examples (spinnaker2.gitlab.io/py-spinnaker2/examples)"; make it a hyperlink to https://spinnaker2.gitlab.io/py-spinnaker2/examples/index.html

Slide 9.3
- Kicker: DEMOS · ENERGY
- Title: The board draws 57 W just for being on; spiking adds to that
- Subtitle (two lines): "The same network on 1,000 cores of one board, run during the break: silent, it barely moves the reading; with every neuron spiking in every step, it adds 6 to 9 W. The board reports power in 3 W steps, so a workshop network of a few cores would not show at all."
- Figure: 02_workshop_design/slides/figures/b9_power.png
- Source line: "Source: measured on one 48-chip board of the HPI cluster, 2026-10-19 (workshop repository, 05_measurements/01_power_baseline)"

Slide 9.4
- Kicker: DEMOS · ENERGY
- Title: Above the baseline, the energy follows the spikes: roughly 0.6 nJ per synaptic event
- Subtitle (two lines): "The more cores spike, the more the board draws; silent cores cost almost nothing extra. The 6 W that spiking adds, divided by 10 billion synaptic events per second, give about 0.6 nJ per event. Ask of every energy number: what is the baseline, and what is included?"
- Figure: 02_workshop_design/slides/figures/b9_power_vs_load.png
- Source line: "Source: measured on the HPI cluster, 2026-10-19; for comparison: Höppner et al. 2021 (test chip, about 0.2 nJ per synaptic event)"

Slide 9.5 (links, no figure)
- Kicker: DEMOS · READ ON
- Title: To read on after the workshop
- Body: three groups, each a bold label followed by one line of links, in the subtitle's font size; make the URLs hyperlinks on the link text, do not print the URLs:
  - Getting data in: "workshop note: Spiking Neurons and Networks, section 6" (no link) · "snnTorch tutorial 1: spike encoding" -> https://snntorch.readthedocs.io/en/latest/tutorials/tutorial_1.html
  - Examples: "py-spinnaker2 examples" -> https://spinnaker2.gitlab.io/py-spinnaker2/examples/index.html
  - Energy: "py-spinnaker2 user guide: power measurement" -> https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/power_measurement.html · "our measurement: workshop repository, 05_measurements/01_power_baseline" (no link) · "workshop note: SpiNNaker2 hardware and energy, sections 8 and 9" (no link)
- No source line

Report the final order and titles of the block 9 slides.
```
