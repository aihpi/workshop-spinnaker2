# Workshop Brief

Draft, as of 2026-09-28.

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
- [ ] How many participants can use the chips at the same time? How many chips and boards do we have?
- [ ] Does power measurement work on our setup? The energy story depends on it.
- [ ] Which py-spinnaker2 features does the Brian2 backend support? Every notebook needs to run on both paths.
- [ ] Is the workshop open to people outside HPI? If so, they are on the Brian2 fallback.
- [ ] Date and room.
