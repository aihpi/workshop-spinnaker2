# SpiNNaker2 Sources

Library of everything worth reading for the workshop. Status: `todo` = not read yet, `read` = read and notes taken, `skim` = looked at, not in depth.

**Version used: py-spinnaker2 v0.8.** The HPI cluster runs v0.8.0 plus a hotfix (commit `6c9084fc`, see `03_setup/README.md`). For the fact-check of 2026-09-30, the docs, tutorials, examples and code were read in full from the repository at tag v0.8.2, together with the chip-side code (snn-core) it pins; v0.8.0 to v0.8.2 differ in no neuron model or synapse format. The online docs currently match it (latest migration guide is v0.8.0). Before relying on a docs page, check it hasn't moved on to a newer release.

## Core: py-spinnaker2

The main software for the workshop. Python interface for running experiments on SpiNNaker2 chips (Apache 2.0).

| Source | What | Status |
|---|---|---|
| [Docs: Quick Start](https://spinnaker2.gitlab.io/py-spinnaker2/) | Entry point of the documentation | read |
| [Repository (GitLab)](https://gitlab.com/spinnaker2/py-spinnaker2) | Source code, examples | read |
| [README](https://gitlab.com/spinnaker2/py-spinnaker2/-/blob/main/README.md) · [CHANGELOG](https://gitlab.com/spinnaker2/py-spinnaker2/-/blob/main/CHANGELOG.md) · [Releases](https://gitlab.com/spinnaker2/py-spinnaker2/-/releases) | Project overview, version history | read |
| [Docker images](https://hub.docker.com/r/spinnaker2/py-spinnaker2/tags) | Prebuilt environments | todo |
| [Zenodo record](https://zenodo.org/records/18312495) · [older record](https://zenodo.org/records/13354891) | Citable software releases | todo |

### User guide

| Source | What | Status |
|---|---|---|
| [SNNs on SpiNNaker2](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/snn-intro.html) | Intro to building SNNs | read |
| [Simulation options](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/snn-advanced.html) | Run configuration | read |
| [Logging](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/logging.html) | | skim |
| [Diagnostic folder](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/diagnostic_folder.html) | | read |
| [Performance profiling](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/profiling.html) | Timing per core, useful for workshop demos | read |
| [Power measurement](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/power_measurement.html) | Energy numbers, likely a workshop highlight | read |
| [Brian2 backend](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/brian2.html) | Simulator without chips, fallback for the workshop: check which features it supports | read |
| [Data streaming](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/data-streaming.html) | Real-time I/O | read |
| [NIR](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/qs-nir.html) | Import models trained elsewhere | read |

### Tutorials (deep dive), likely backbone of the workshop

| Source | What | Status |
|---|---|---|
| [00 Welcome](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/00_welcome.html) | | skim |
| [01 Core concepts](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/01_core_concepts.html) | | read |
| [02 Connectivity](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/02_connectivity.html) | | read |
| [03 Convolutional layers](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/03_lif_conv2d.html) | | skim |
| [04 Hardware allocation](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/04_hardware_allocation.html) | | read |
| [05 Debugging and output](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/05_debugging.html) | | read |
| [06 Hardware architecture](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/06_hardware_architecture.html) | | read |
| [07 Real-time spike streaming](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/07_streaming.html) | | read |
| [08 NIR workflow](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/08_nir.html) | | read |
| [09 Custom neuron models](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/09_custom-neuron-models_basics.html) | | skim |

### Examples, candidate workshop demos

| Source | What | Status |
|---|---|---|
| [Clustered SNN](https://spinnaker2.gitlab.io/py-spinnaker2/examples/clustered_snn.html) | Neuroscience-style network | read |
| [QUBO Max-Cut](https://spinnaker2.gitlab.io/py-spinnaker2/examples/QUBO_Maxcut.html) | Optimisation with SNNs | read |
| [End-to-end NIR](https://spinnaker2.gitlab.io/py-spinnaker2/examples/end_to_end_NIR.html) | Train, export, deploy | read |
| [Bidirectional streaming pipeline](https://spinnaker2.gitlab.io/py-spinnaker2/examples/streaming_pipeline.html) | Closed-loop I/O | skim |
| [NMNIST with pre-trained NIR model](https://spinnaker2.gitlab.io/py-spinnaker2/examples/nir_demo.html) | Classic neuromorphic benchmark | read |

### Advanced topics

| Source | What | Status |
|---|---|---|
| [Hardware allocation](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/hardware-allocation.html) | Mapping networks to cores | read |
| [Execution workflow](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/execution_workflow/index.html): [setup](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/execution_workflow/run-walkthrough-1.html), [chip-side](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/execution_workflow/run-walkthrough-2.html), [results](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/execution_workflow/run-walkthrough-3.html) | What happens during `run()` | read |
| [Memory](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/index.html): [structure](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/memory-structure.html), [allocation](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/memory-allocation.html), [visualisation](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/memory-visualization.html) | Memory limits per core | read |
| [Custom neuron models](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/index.html): [backend (C)](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/custom-model-guide-hw.html), [frontend (Python)](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/custom-model-guide-py.html), [state variables](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/monitoring-state-variables.html), [32-bit synapses](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/custom-model-guide-syn.html), [registration](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/custom-model-registration.html) | Writing own models | todo |
| [Experiment runner](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/experiment-runner.html) | Host-chip communication layer | read |
| [LIF Conv2d allocation rules](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/lifconv2d.html) | | skim |
| [Neuron model C data structures](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/extras-data-structures.html) | | todo |
| [Running tests](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/running-tests.html) · [Hooks](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/hooks.html) | | todo |
| [Migration guides](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/migration/index.html) | API changes v0.3 to v0.8. With v0.8 installed, only the [v0.8.0 changes](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/migration/v0.8.0.html) matter, mainly to spot outdated older examples | skim |

### Reference

| Source | What | Status |
|---|---|---|
| API: [neuron models](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/neuron-models.html), [configuration](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/configuration-api.html), [snn](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/snn-api.html), [s2_nir](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/s2_nir-api.html), [hardware](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/hardware-api.html), [graph](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/graph-api.html), [synapses](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/synapses-api.html), [helpers](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/helpers-api.html), [coordinates](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/coordinates-api.html), [regions](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/regions-api.html) | Python API | read |
| [Chip-side monitor library](https://spinnaker2.gitlab.io/py-spinnaker2/snn-lib/monitor_8h.md) | C API | todo |
| [Known issues](https://spinnaker2.gitlab.io/py-spinnaker2/troubleshooting/known-issues.html) | Pitfalls to avoid during the workshop | read |
| [About](https://spinnaker2.gitlab.io/py-spinnaker2/about.html) | | todo |

## Other SpiNNaker2 software

| Source | What | Status |
|---|---|---|
| [SpiNNaker2 GitLab group](https://gitlab.com/spinnaker2) | All public repos | skim |
| [snn-core](https://gitlab.com/spinnaker2/snn-core) | Chip-side C code of the neuron models, pinned by py-spinnaker2 (`setup_libs.sh`, commit `0341893` for v0.8.2). The ground truth for update rules, synapse format and spike handling | read |
| [SpiNNMan2](https://gitlab.com/spinnaker2/SpiNNMan2) (v0.2.4) | Host library used by py-spinnaker2: board locks, UDP communication, power measurement backends | read |
| [SpiNNaker2 Developer Portal](https://spinnaker2.gitlab.io/) | General chip intro. Redirects to a GitLab login, so possibly restricted | todo |
| [Software configuration guide](https://spinnaker2.gitlab.io/external/get_started/software_configuration) | Setup, on the portal (may need login) | todo |
| [SpiNNMan2](https://spinnman2-spinnaker2-cfed5092d1bac452b1096ec19e2826cf9bbd0eade7.gitlab.io/) | Low-level machine control, for experienced developers | todo |

## Papers

### Hardware and architecture

| Source | What | Status |
|---|---|---|
| [Scholze et al. 2026, The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing](https://arxiv.org/abs/2607.24396) | Newest and most complete chip paper (152 PEs, ARM M4F, accelerators) | read |
| [Gonzalez et al. 2024, SpiNNaker2: A Large-Scale Neuromorphic System for Event-Based and Asynchronous Machine Learning](https://arxiv.org/abs/2401.04491) | System view, ML focus | read |
| [Höppner et al. 2021, The SpiNNaker 2 Processing Element Architecture for Hybrid Digital Neuromorphic Computing](https://arxiv.org/abs/2103.08392) | Processing element in detail (22nm FDSOI, DVFS, accelerators) | read |
| [Mayr, Höppner, Furber 2019, SpiNNaker 2: A 10 Million Core Processor System for Brain Simulation and Machine Learning](https://arxiv.org/abs/1911.02385) | Roadmap SpiNNaker1 to SpiNNaker2 | read |
| [Furber et al. 2014, The SpiNNaker Project (Proc. IEEE)](https://doi.org/10.1109/JPROC.2014.2304638) | SpiNNaker1 background, origin of the design ideas | todo |

### Applications on SpiNNaker2

| Source | What | Status |
|---|---|---|
| [DVS gesture recognition via NIR (2025)](https://arxiv.org/abs/2504.06748) | Quantisation (PTQ, QAT) and 8-bit on-chip inference | read |
| [Hardware-aware fine-tuning of spiking Q-networks (2025)](https://arxiv.org/abs/2507.23562) | Reinforcement learning on chip | read |
| [Nazeer et al. 2024, Language modeling on a SpiNNaker2 neuromorphic chip (IEEE AICAS)](https://arxiv.org/abs/2312.09084) | Event-based GRU language model; the source of the "18×" (batch size 1, 8.6× slower than an A100) | read |

### Ecosystem and context

| Source | What | Status |
|---|---|---|
| [Pedersen et al. 2024, Neuromorphic Intermediate Representation (Nature Communications)](https://www.nature.com/articles/s41467-024-52259-9) | Cross-platform model format that py-spinnaker2 supports | read |
| [NIR website](https://neuroir.org/) · [docs](https://neuroir.org/docs/) · [GitHub](https://github.com/neuromorphs/NIR) | | read |
| [snnTorch export to NIR](https://snntorch.readthedocs.io/en/latest/snntorch.export_nir.html) | Export step on the training side | read |
| [Horowitz 2014, Computing's energy problem (and what we can do about it), ISSCC](https://doi.org/10.1109/ISSCC.2014.6757323) | Energy per operation and memory access (45 nm), the standard reference for energy arguments | read |
| [Blem, Menon, Sankaralingam 2013, Power struggles: revisiting the RISC vs. CISC debate (HPCA)](https://research.cs.wisc.edu/vertical/papers/2013/hpca13-isa-power-struggles.pdf) | Measurement study: the instruction set matters little for energy efficiency, the design point does (computing fundamentals, section 5) | read |
| [Kudithipudi et al. 2025, Neuromorphic computing at scale (Nature)](https://www.nature.com/articles/s41586-024-08253-8) | Field overview, good for the workshop intro | todo |
| [Brian2 simulator](https://briansimulator.org/) | Out of scope for now | skip |

## Further reading: optimisation and energy-based models

Not for the workshop (at most a short outlook on QUBO), but worth reading later. Background for the QUBO neuron in section 5 of the primer.

| Source | What | Status |
|---|---|---|
| [QUBO](https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization) · [Ising model](https://en.wikipedia.org/wiki/Ising_model) · [spin glass](https://en.wikipedia.org/wiki/Spin_glass) | The problem class and its physics formulation | todo |
| [Lucas 2014, Ising formulations of many NP problems](https://arxiv.org/abs/1302.5843) | How Max-Cut, colouring, scheduling, TSP etc. map onto QUBO/Ising | todo |
| [Kirkpatrick, Gelatt, Vecchi 1983, Optimization by simulated annealing (Science)](https://doi.org/10.1126/science.220.4598.671) · [Wikipedia](https://en.wikipedia.org/wiki/Simulated_annealing) | Annealing as an optimisation method, borrowed from statistical physics | todo |
| [Quantum annealing](https://en.wikipedia.org/wiki/Quantum_annealing) | Principle behind D-Wave; digital annealers (Fujitsu) as the classical counterpart | todo |
| [Hopfield 1982, Neural networks and physical systems with emergent collective computational abilities (PNAS)](https://doi.org/10.1073/pnas.79.8.2554) · [Wikipedia](https://en.wikipedia.org/wiki/Hopfield_network) | Networks that compute by relaxing into energy minima | todo |
| [Ackley, Hinton, Sejnowski 1985, A learning algorithm for Boltzmann machines (Cognitive Science)](https://doi.org/10.1207/s15516709cog0901_7) · [Wikipedia](https://en.wikipedia.org/wiki/Boltzmann_machine) | Stochastic version of the Hopfield network, with learning | todo |
| [Nobel Prize in Physics 2024](https://www.nobelprize.org/prizes/physics/2024/summary/) | Hopfield and Hinton, for these foundations of machine learning | todo |

## Company and press

Useful for the motivation part of the workshop.

| Source | What | Status |
|---|---|---|
| [SpiNNcloud Systems](https://spinncloud.com) | Manufacturer | read |
| [IEEE Spectrum 2025, Brain-inspired computing is ready for the big time](https://spectrum.ieee.org/neuromorphic-computing-2671121824) | | todo |
| [BBC 2024, Could brain-like computers be a 'competition killer'?](https://www.bbc.com/news/articles/cx99qv2w1ddo) | | todo |
| [The Register 2024, SpiNNcloud unveils Arm-based neuromorphic system](https://www.theregister.com/2024/05/08/spinncloud_systems_unveils_armbased_neuromorphic/) | | todo |
| [EE Times podcast 2023, Steve Furber on SpiNNaker 1, 2 and beyond](https://www.eetimes.com/podcasts/arm-inventor-steve-furber-on-spinnaker-1-2-and-beyond/) | | todo |

## Local sources

Material on the cluster or from colleagues that isn't public. Add path and a short note.

| Source | What | Status |
|---|---|---|
| | | |
