# Neuromorphic computing on SpiNNaker2, part 1

## Header

- Level: single
- Mode: lite
- Format: slides
- Language: en-US
- Slot: 90 min (14:00 to 15:30, 18 Nov 2026), of which slides about 50 min, hands-on 35 min, setup check 5 min
- Setting: H-2.57/58, up to 20 participants in pairs
- Template: AISC Light
- Quiz: none
- Inspiration: 02_workshop_design/04_slide_plan.md (blocks 1 to 6), 01_knowledge_base figures
- Learner: ML PhD students and software developers who know PyTorch, ReLU, RNNs and backprop, but not spiking networks or neuromorphic hardware
- Key message: spiking hardware saves energy only where activity is sparse, because it works only when a spike arrives
- Goals: G1 explain how an LIF neuron integrates, leaks, fires and resets in discrete time; G2 build and run a small spiking network with py-spinnaker2; G3 describe where the network runs on SpiNNaker2 and what a chip run costs
- Output: 02_workshop_design/slides/part1.pptx (deck folder 02_workshop_design/slides/, plan.md next to it)
- Status log:
  - 2026-11-15 plan written
  - 2026-11-15 plan approved in the plan panel (ExitPlanMode accepted by the user)
  - 2026-11-15 creator, lite, complete (29 slides; not rendered in PowerPoint or LibreOffice, none installed)

# Slide 1
## Title: Neuromorphic computing on SpiNNaker2
## Content:
- Hands-on workshop
- David Goll, AI Service Centre Berlin Brandenburg, HPI
- 18 November 2026

# Slide 2
## Title: The afternoon
## Content:
A timeline of the afternoon in two halves, with a break between them:
- 14:00 Why neuromorphic computing
- 14:15 Setup check
- 14:20 Spiking neural networks
- 14:40 Hands-on 1: one neuron
- 14:55 SpiNNaker2 hardware
- 15:10 Hands-on 2: a network on the chip
- 15:30 Break
- 15:45 From PyTorch to the chip
- 15:55 Hands-on 3: NIR
- 16:35 Demos: energy, event camera, Max-Cut
- 16:45 Applications, an honest take

# Slide 3
## Title: How we work today
## Content:
- Theory, then hands-on, then discussion
- Work in pairs: one laptop with a working setup is enough
- Everything runs on Brian2, a simulator that computes the same spikes as the chip
- HPI cluster accounts: one run per pair on the SpiNNaker2 chips
- Not installed yet? Start now: github.com/aihpi/workshop-spinnaker2

# Slide 4
## Title: AI costs energy, the brain runs on 20 W
## Content:
- One data-center GPU: up to 400 W (NVIDIA A100)
- Human brain: about 20 W
-- about 0.1 W for computation in the cortex
-- about 3.5 W for communication, 35 times more
- Source: Levy and Calvert, PNAS 2021

# Slide 5
## Title: Moving data costs more than computing on it
## Content:
- An addition is 5 times cheaper than a multiply-accumulate (32-bit float)
- Reading from off-chip DRAM costs 13 to 130 times more than from on-chip SRAM
- One DRAM read costs more than 1000 additions
- Source: Horowitz, ISSCC 2014, 45 nm
Figure: energy per operation, bar chart (01_knowledge_base/figures/01_primer_snn_basics/09_energy_per_operation.png)

# Slide 6
## Title: One shared memory or many local memories
## Content:
- Von Neumann: every value travels over one bus between CPU and memory
- SpiNNaker2: every core has its own memory next to it
- Cores exchange only small messages
Figure: von Neumann vs. distributed design (01_knowledge_base/figures/00_computing_fundamentals/02_von_neumann_vs_distributed.png)

# Slide 7
## Title: The idea: compute only when something happens
## Content:
- Neurons send short pulses (spikes) and stay silent in between
- No spike, no work
- Fewer spikes, less energy
Figure: an LIF neuron charging and spiking (01_knowledge_base/figures/01_primer_snn_basics/02_lif_spiking.png)

# Slide 8
## Title: A short history
## Content:
A table with five rows:
- 1990: Carver Mead names the field "neuromorphic"
- 2014: IBM TrueNorth, 1 million neurons on one chip
- 2018: million-core SpiNNaker machine in Manchester
- 2024: Intel Hala Point, 1.15 billion neurons
- 2026: SpiNNaker2 vendor renamed Sparxity, sold for AI inference

# Slide 9
## Title: The promise and the catch
## Content:
- Promise: large energy savings for AI
- Catch: only under specific conditions
-- sparse activity
-- small batches, streaming input
- We come back to this at the end of the afternoon

# Slide 10
## Title: Setup check
## Content:
- Form pairs
- HPI cluster: open the environment on cx51
- Laptop: open your local environment
- Run 04_workshop_material/00_setup_check.ipynb
- Expected: "Brian2 works." and the plot on the right
- Not working? Raise your hand
Figure: the plot of the setup notebook, output spikes one step after each input spike (screenshot of the notebook output)

# Slide 11
## Title: Spiking neural networks

# Slide 12
## Title: From the biological neuron to a simple model
## Content:
- Hodgkin-Huxley: detailed and expensive
- FitzHugh-Nagumo: two variables
- Leaky integrate-and-fire (LIF): one variable, the simplest model that still spikes
- All three fire at the same times; only the shape and the cost differ
Figure: HH, FHN and LIF under the same input (01_knowledge_base/figures/01_primer_snn_basics/02_models_hh_fhn_lif.png)

# Slide 13
## Title: LIF: integrate, leak, fire, reset
## Content:
- Integrate: input charges the membrane potential v
- Leak: without input, v decays back to rest
- Fire: v crosses the threshold and the neuron sends a spike
- Reset: v starts again from the reset value
Figure: LIF potential for three constant inputs (01_knowledge_base/figures/01_primer_snn_basics/02_lif_spiking.png)

# Slide 14
## Title: Input and output: almost a ReLU
## Content:
- Below a critical input: no spikes at all
- Above it: the firing rate grows almost linearly
- Same shape as a ReLU, but the output is a count of spikes
Figure: firing rate against constant input, with a ReLU for comparison (01_knowledge_base/figures/01_primer_snn_basics/02_fi_curve.png)

# Slide 15
## Title: LIF in discrete time, as the chip computes it
## Content:
- v[t] = α · v[t-1] + I[t]
- α = alpha_decay: how much of v remains after one step (leak)
- I[t]: weights of the spikes arriving in step t, plus a constant input
- One step = 1 ms
Figure: v step by step with input spikes and output spikes (01_knowledge_base/figures/01_primer_snn_basics/03_discrete_update.png)

# Slide 16
## Title: Synapses: weight and delay
## Content:
- Weight: how much one spike changes v (positive or negative)
- Delay: how many steps the spike is held back
- A spike sent in step t arrives in step t + 1 + delay
Figure: a spike through a connection with delay 3 (01_knowledge_base/figures/01_primer_snn_basics/04_delay.png)

# Slide 17
## Title: Weights are small integers
## Content:
- lif: weights from -15 to 15, delays from 0 to 7
- Fractions are cut off without a warning
- What counts is the ratio of weight to threshold
- Compare: quantization of a deep network to 4 or 8 bits
Figure: weight quantization (01_knowledge_base/figures/01_primer_snn_basics/04_weight_quantization.png)

# Slide 18
## Title: An LIF layer is a recurrent cell
## Content:
- v[t] = α · v[t-1] + W · x[t]
- Output: a binary spike, not a continuous activation
- Same weights in every step: trained like an RNN, with backpropagation through time
- Back to this after the break
Figure: an LIF layer unrolled over three time steps (01_knowledge_base/figures/01_primer_snn_basics/08_lif_unrolled.png)

# Slide 19
## Title: Deep learning and spiking networks side by side
## Content:
A two-column table:
- Activation (float) | spike (0 or 1)
- One pass per input | many time steps per input
- ReLU | LIF with threshold and leak
- Every connection computes | only connections with a spike compute
- Float or 8-bit weights | small integer weights
- Time is a sequence dimension | time is built into every neuron

# Slide 20
## Title: Hands-on 1: one neuron
## Content:
- Notebook 04_workshop_material/01_single_neuron.ipynb, on Brian2
- Section 1: a neuron with constant input; predict, then run
- Section 2: input spikes with weights and delays
- Change only the "change these" block of each cell
- 15 minutes, in pairs; then we discuss

# Slide 21
## Title: SpiNNaker2 hardware

# Slide 22
## Title: Where the chips are
## Content:
- A frame with 6 boards in the HPI data center, next to the cluster node cx51
- One board: 48 chips
- One run reserves one board: 7,104 cores
Figure: from the cluster node to the frame, the board and one chip (01_knowledge_base/figures/02_hardware_energy/01_installation_hierarchy.png)

# Slide 23
## Title: One chip: 152 small cores with local memory
## Content:
- 152 ARM cores (processing elements, PEs), each with 128 KB of local memory
- Neurons are software running on the cores
- A spike is a small packet; the router copies it to every core that needs it
Figure: the chip, one QPE and one PE, with the path of one spike (01_knowledge_base/figures/02_hardware_energy/01_chip_schematic.png)

# Slide 24
## Title: What a core does in one time step
## Content:
- Process the spikes that arrived
- Update its neurons and send their spikes
- Sleep until the next step
- More spikes, more work: spikes cost energy, not neurons
Figure: ten time steps of one PE (01_knowledge_base/figures/02_hardware_energy/02_pe_timestep.png)

# Slide 25
## Title: From one chip to a system
## Content:
- One chip: 152 cores
- One board: 48 chips
- HPI: 6 boards, 288 chips
- TU Dresden: 35,000 chips, still a few percent of the neurons of a human brain
Figure: number of cores and neurons from chip to system (01_knowledge_base/figures/02_hardware_energy/05_scale.png)

# Slide 26
## Title: What happens during a run
## Content:
- Python describes the network
- py-spinnaker2 places it on the cores and compiles the neuron code
- The board is powered up and booted
- About one minute per run, whatever the size of the network
Figure: from Python to machine code on the cores (01_knowledge_base/figures/00_computing_fundamentals/06_bare_metal_cross_compilation.png)

# Slide 27
## Title: Brian2: the same code on a laptop
## Content:
A two-column table:
- Brian2 | SpiNNaker2
- Laptop, no account | HPI cluster account
- Seconds per run | about one minute per run
- As many runs as you like | 6 boards for everyone
- Identical spikes for lif | identical spikes for lif
- No energy measurement | real hardware, real power draw

# Slide 28
## Title: Hands-on 2: a network on the chip
## Content:
- Notebook 04_workshop_material/02_synfire_chain.ipynb
- A chain of 5 groups passes a wave of spikes
- Change one value at a time: when does the wave die out?
- HPI pairs: run section 3 on the chip, one pair at a time
- 20 minutes, in pairs; then we discuss
Figure: sketch of the synfire chain, 5 groups of neurons with the volley getting sharper from group to group

# Slide 29
## Title: Break
## Content:
- Back at 15:45
- Next: from PyTorch to the chip

# Notes
- Template AISC Light, sentence case in titles (switch off the all-caps property of the placeholders).
- Figures from 01_knowledge_base/figures are used as they are for this draft (own colors, not the HPI palette); redrawing comes later.
- New figures to draw: the agenda timeline (slide 2), the setup-check plot (slide 10, take the output of 00_setup_check), the synfire sketch (slide 28; can reuse the spikes-per-step panel of notebook 02 if a sketch takes too long).
- Slide 4: the 400 W of the A100 (SXM, NVIDIA datasheet) still needs a source check before the workshop.
- Slides 19 and 27: tables, not bullet lists; the "|" separates the two columns.
- Slides 13 and 7 share one figure on purpose (teaser, then explanation); drop one later if it feels repetitive.
- Block 3 (slides 11 to 19) is planned for about 15 minutes and deliberately has more content than needed; cut later.
- No speaker notes.
