# SpiNNaker2 Sources

Library of everything worth reading for the workshop. Status: `todo` = not read yet, `read` = read and notes taken, `skim` = looked at, not in depth.

**Version used: py-spinnaker2 v0.8** (installed on the HPI cluster). The online docs currently match it (latest migration guide is v0.8.0). Before relying on a docs page, check it hasn't moved on to a newer release.

## Core: py-spinnaker2

The main software for the workshop. Python interface for running experiments on SpiNNaker2 chips (Apache 2.0).

| Source | What | Status |
|---|---|---|
| [Docs: Quick Start](https://spinnaker2.gitlab.io/py-spinnaker2/) | Entry point of the documentation | todo |
| [Repository (GitLab)](https://gitlab.com/spinnaker2/py-spinnaker2) | Source code, examples | todo |
| [README](https://gitlab.com/spinnaker2/py-spinnaker2/-/blob/main/README.md) · [CHANGELOG](https://gitlab.com/spinnaker2/py-spinnaker2/-/blob/main/CHANGELOG.md) · [Releases](https://gitlab.com/spinnaker2/py-spinnaker2/-/releases) | Project overview, version history | todo |
| [Docker images](https://hub.docker.com/r/spinnaker2/py-spinnaker2/tags) | Prebuilt environments | todo |
| [Zenodo record](https://zenodo.org/records/18312495) · [older record](https://zenodo.org/records/13354891) | Citable software releases | todo |

### User guide

| Source | What | Status |
|---|---|---|
| [SNNs on SpiNNaker2](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/snn-intro.html) | Intro to building SNNs | todo |
| [Simulation options](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/snn-advanced.html) | Run configuration | todo |
| [Logging](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/logging.html) | | todo |
| [Diagnostic folder](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/diagnostic_folder.html) | | todo |
| [Performance profiling](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/profiling.html) | Timing per core, useful for workshop demos | todo |
| [Power measurement](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/power_measurement.html) | Energy numbers, likely a workshop highlight | todo |
| [Brian2 backend](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/brian2.html) | Simulator without chips, fallback for the workshop: check which features it supports | todo |
| [Data streaming](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/data-streaming.html) | Real-time I/O | todo |
| [NIR](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/qs-nir.html) | Import models trained elsewhere | todo |

### Tutorials (deep dive), likely backbone of the workshop

| Source | What | Status |
|---|---|---|
| [00 Welcome](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/00_welcome.html) | | todo |
| [01 Core concepts](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/01_core_concepts.html) | | todo |
| [02 Connectivity](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/02_connectivity.html) | | todo |
| [03 Convolutional layers](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/03_lif_conv2d.html) | | todo |
| [04 Hardware allocation](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/04_hardware_allocation.html) | | todo |
| [05 Debugging and output](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/05_debugging.html) | | todo |
| [06 Hardware architecture](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/06_hardware_architecture.html) | | todo |
| [07 Real-time spike streaming](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/07_streaming.html) | | todo |
| [08 NIR workflow](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/08_nir.html) | | todo |
| [09 Custom neuron models](https://spinnaker2.gitlab.io/py-spinnaker2/tutorials/deep_dive/09_custom-neuron-models_basics.html) | | todo |

### Examples, candidate workshop demos

| Source | What | Status |
|---|---|---|
| [Clustered SNN](https://spinnaker2.gitlab.io/py-spinnaker2/examples/clustered_snn.html) | Neuroscience-style network | todo |
| [QUBO Max-Cut](https://spinnaker2.gitlab.io/py-spinnaker2/examples/QUBO_Maxcut.html) | Optimisation with SNNs | todo |
| [End-to-end NIR](https://spinnaker2.gitlab.io/py-spinnaker2/examples/end_to_end_NIR.html) | Train, export, deploy | todo |
| [Bidirectional streaming pipeline](https://spinnaker2.gitlab.io/py-spinnaker2/examples/streaming_pipeline.html) | Closed-loop I/O | todo |
| [NMNIST with pre-trained NIR model](https://spinnaker2.gitlab.io/py-spinnaker2/examples/nir_demo.html) | Classic neuromorphic benchmark | todo |

### Advanced topics

| Source | What | Status |
|---|---|---|
| [Hardware allocation](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/hardware-allocation.html) | Mapping networks to cores | todo |
| [Execution workflow](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/execution_workflow/index.html): [setup](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/execution_workflow/run-walkthrough-1.html), [chip-side](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/execution_workflow/run-walkthrough-2.html), [results](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/execution_workflow/run-walkthrough-3.html) | What happens during `run()` | todo |
| [Memory](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/index.html): [structure](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/memory-structure.html), [allocation](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/memory-allocation.html), [visualisation](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/memory/memory-visualization.html) | Memory limits per core | todo |
| [Custom neuron models](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/index.html): [backend (C)](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/custom-model-guide-hw.html), [frontend (Python)](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/custom-model-guide-py.html), [state variables](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/monitoring-state-variables.html), [32-bit synapses](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/custom-model-guide-syn.html), [registration](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/custom_model/custom-model-registration.html) | Writing own models | todo |
| [Experiment runner](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/experiment-runner.html) | Host-chip communication layer | todo |
| [LIF Conv2d allocation rules](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/lifconv2d.html) | | todo |
| [Neuron model C data structures](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/extras-data-structures.html) | | todo |
| [Running tests](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/running-tests.html) · [Hooks](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/hooks.html) | | todo |
| [Migration guides](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/migration/index.html) | API changes v0.3 to v0.8. With v0.8 installed, only the [v0.8.0 changes](https://spinnaker2.gitlab.io/py-spinnaker2/advanced_topic/migration/v0.8.0.html) matter, mainly to spot outdated older examples | todo |

### Reference

| Source | What | Status |
|---|---|---|
| API: [neuron models](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/neuron-models.html), [configuration](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/configuration-api.html), [snn](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/snn-api.html), [s2_nir](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/s2_nir-api.html), [hardware](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/hardware-api.html), [graph](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/graph-api.html), [synapses](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/synapses-api.html), [helpers](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/helpers-api.html), [coordinates](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/coordinates-api.html), [regions](https://spinnaker2.gitlab.io/py-spinnaker2/api_reference/regions-api.html) | Python API | todo |
| [Chip-side monitor library](https://spinnaker2.gitlab.io/py-spinnaker2/snn-lib/monitor_8h.md) | C API | todo |
| [Known issues](https://spinnaker2.gitlab.io/py-spinnaker2/troubleshooting/known-issues.html) | Pitfalls to avoid during the workshop | todo |
| [About](https://spinnaker2.gitlab.io/py-spinnaker2/about.html) | | todo |

## Other SpiNNaker2 software

| Source | What | Status |
|---|---|---|
| [SpiNNaker2 GitLab group](https://gitlab.com/spinnaker2) | All public repos | todo |
| [SpiNNaker2 Developer Portal](https://spinnaker2.gitlab.io/) | General chip intro. Redirects to a GitLab login, so possibly restricted | todo |
| [Software configuration guide](https://spinnaker2.gitlab.io/external/get_started/software_configuration) | Setup, on the portal (may need login) | todo |
| [SpiNNMan2](https://spinnman2-spinnaker2-cfed5092d1bac452b1096ec19e2826cf9bbd0eade7.gitlab.io/) | Low-level machine control, for experienced developers | todo |

## Papers

### Hardware and architecture

| Source | What | Status |
|---|---|---|
| [Scholze et al. 2026, The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing](https://arxiv.org/abs/2607.24396) | Newest and most complete chip paper (152 PEs, ARM M4F, accelerators) | todo |
| [Gonzalez et al. 2024, SpiNNaker2: A Large-Scale Neuromorphic System for Event-Based and Asynchronous Machine Learning](https://arxiv.org/abs/2401.04491) | System view, ML focus | todo |
| [Höppner et al. 2021, The SpiNNaker 2 Processing Element Architecture for Hybrid Digital Neuromorphic Computing](https://arxiv.org/abs/2103.08392) | Processing element in detail (22nm FDSOI, DVFS, accelerators) | todo |
| [Mayr, Höppner, Furber 2019, SpiNNaker 2: A 10 Million Core Processor System for Brain Simulation and Machine Learning](https://arxiv.org/abs/1911.02385) | Roadmap SpiNNaker1 to SpiNNaker2 | todo |
| [Furber et al. 2014, The SpiNNaker Project (Proc. IEEE)](https://doi.org/10.1109/JPROC.2014.2304638) | SpiNNaker1 background, origin of the design ideas | todo |

### Applications on SpiNNaker2

| Source | What | Status |
|---|---|---|
| [DVS gesture recognition via NIR (2025)](https://arxiv.org/abs/2504.06748) | Quantisation (PTQ, QAT) and 8-bit on-chip inference | todo |
| [Hardware-aware fine-tuning of spiking Q-networks (2025)](https://arxiv.org/abs/2507.23562) | Reinforcement learning on chip | todo |
| Nazeer et al. 2024, Language modeling on a SpiNNaker2 neuromorphic chip (IEEE AICAS) | LLM-style workload, link still to find | todo |

### Ecosystem and context

| Source | What | Status |
|---|---|---|
| [Pedersen et al. 2024, Neuromorphic Intermediate Representation (Nature Communications)](https://www.nature.com/articles/s41467-024-52259-9) | Cross-platform model format that py-spinnaker2 supports | todo |
| [NIR website](https://neuroir.org/) · [docs](https://neuroir.org/docs/) · [GitHub](https://github.com/neuromorphs/NIR) | | todo |
| [Kudithipudi et al. 2025, Neuromorphic computing at scale (Nature)](https://www.nature.com/articles/s41586-024-08253-8) | Field overview, good for the workshop intro | todo |
| [Brian2 simulator](https://briansimulator.org/) | Out of scope for now | skip |

## Company and press

Useful for the motivation part of the workshop.

| Source | What | Status |
|---|---|---|
| [SpiNNcloud Systems](https://spinncloud.com) | Manufacturer | todo |
| [IEEE Spectrum 2025, Brain-inspired computing is ready for the big time](https://spectrum.ieee.org/neuromorphic-computing-2671121824) | | todo |
| [BBC 2024, Could brain-like computers be a 'competition killer'?](https://www.bbc.com/news/articles/cx99qv2w1ddo) | | todo |
| [The Register 2024, SpiNNcloud unveils Arm-based neuromorphic system](https://www.theregister.com/2024/05/08/spinncloud_systems_unveils_armbased_neuromorphic/) | | todo |
| [EE Times podcast 2023, Steve Furber on SpiNNaker 1, 2 and beyond](https://www.eetimes.com/podcasts/arm-inventor-steve-furber-on-spinnaker-1-2-and-beyond/) | | todo |

## Local sources

Material on the cluster or from colleagues that isn't public. Add path and a short note.

| Source | What | Status |
|---|---|---|
| | | |
