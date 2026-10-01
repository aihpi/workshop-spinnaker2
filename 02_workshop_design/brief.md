# Workshop Brief

Draft, as of 2026-09-28, open questions updated on 2026-10-01 after the fact-check of the knowledge base.

## Audience

- Mostly PhD students with an ML background, plus some software developers interested in SpiNNaker2.
- Comfortable with Python and probably PyTorch. Assume no prior knowledge of neuroscience, spiking neural networks or neuromorphic hardware.

## Goal

After the workshop, participants understand why neuromorphic hardware can save energy, know the basics of spiking neurons and networks, and can build and run a spiking network on SpiNNaker2 chips themselves.

## Format

- 3 hours, hands-on.
- Participants with access to the HPI cluster run the code on the real chips.
- Fallback: the Brian2 simulation backend, for participants without cluster access or if the hardware fails on the day.
- Date: beginning of November 2026, to be fixed this week.

## Content pillars

1. **Motivation:** energy efficiency of neuromorphic computing compared to GPUs.
2. **Basics:** neuron models (LIF), spikes, synapses, clustered networks.
3. **Hands-on:** building a network in py-spinnaker2 (v0.8) and running it on the chip.
4. **ML bridge:** getting trained models onto the chip (Neuromorphic Intermediate Representation - NIR).

## Draft time budget

| Block | Time |
|---|---|
| Motivation: why neuromorphic, energy | 20 min |
| Basics: neurons, spikes, networks | 30 min |
| Hands-on 1: first network on the chip | 50 min |
| Break | 15 min |
| Hands-on 2: trained model via NIR, energy measurement | 45 min |
| Clustered networks demo, outlook, Q&A | 20 min |

## Open questions

- [ ] How do participants get cluster access, and how long does account creation take? 
- [ ] How many participants can use the chips at the same time? The HPI setup has 6 boards (48-node boards, confirmed on the cluster), runs use one board each, and the lock covers the whole board (SpiNNMan2 code), so at most 6 participants can run in parallel: plan for turns, pairs, or the Brian2 fallback for the rest. Still open: how many boards workshop accounts get. Details in `01_knowledge_base/02_hardware_energy.md`, section 5.
- [ ] Does power measurement work on our setup? The energy story depends on it. On a 48-node board, py-spinnaker2 reports one power value for the whole board, so a small network may vanish in the baseline; first thing to test on the cluster (`02_hardware_energy.md`, section 9). Without a visible difference, hands-on 2 shows reported numbers and how to read them instead of an own measurement.
- [ ] Which py-spinnaker2 features does the Brian2 backend support? Every notebook needs to run on both paths. From the code: `lif`, `lif_curr_exp`, `alif` (with their variants), `spike_list` and `poisson_process`; not `izhikevich`, `lif_prob`, `qubo_neuron` or the latency encoder; no power measurement or profiling. The clustered SNN example, the NMNIST NIR example and tutorial 08 run on Brian2, the QUBO and end-to-end NIR examples need a board. To be written up as plan task 1.
- [ ] Which py-spinnaker2 version on the cluster? It runs v0.8.0 plus a hotfix (`03_setup/README.md`). In v0.8.0 a hardware object runs only once and network names must be unique, so re-running notebook cells needs workarounds; v0.8.1 and later remove both. Upgrading to v0.8.2 means re-running the smoke test and the tutorials in `04_spinncloud_tutorials/`.
- [ ] Is the workshop open to people outside HPI? If so, they are on the Brian2 fallback.
- [ ] Date and room.
