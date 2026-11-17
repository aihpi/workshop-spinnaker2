# Workshop Material

Hands-on notebooks and demos of the workshop "Neuromorphic Computing: Spiking Neural Networks on SpiNNaker2". The schedule is in [`02_workshop_design/03_outline.md`](../02_workshop_design/03_outline.md).

## Contents

| File | Content | Block |
|---|---|---|
| `00_setup_check.ipynb` | Checks the packages and runs a tiny network on Brian2; run it before the workshop | 2 |
| `01_single_neuron.ipynb` | One spiking neuron: constant input, input spikes and synapses; points to the vendor tutorials for more | 4 (hands-on 1) |
| `02_direction_detector.ipynb` | A network built by hand: a direction detector from a weight and a delay matrix, chip run | 6 (hands-on 2) |
| `03_direction_nir.ipynb` | The same task trained in snnTorch, exported to NIR, converted and checked spike for spike; more under "After the workshop" | 8 (hands-on 3) |
| `04_direction_trained.ipynb` | The task on an 8 × 8 event camera with noise: train, test, run via NIR, chip run | 8 (hands-on 3) |
| `demos/` | Instructor demos: energy, event-camera digits, Max-Cut | 9 |
| `archive/` | Earlier notebooks the workshop no longer uses (synfire chain, the first NIR notebooks) | |

Demos tested on the chip on 2026-11-09: Max-Cut finds the optimum of both graphs, NMNIST classifies its sample like Brian2, the energy demo reads 57 W empty, 60 W silent and 63 W active (66 W in the measurement of 2026-10-19). The demos need `tonic` and `networkx` in addition to `requirements.txt`. Notebooks 02 to 04 tested on 2026-11-17 on cx51: on Brian2 after the last changes; on the chip in their state of the same day, before the final trimming (which did not touch the chip cells): 02 gives the same answer as Brian2, 03 the same hidden and output spikes as snnTorch, 04 the same answer as snnTorch. Training takes a few seconds in 03 and about half a minute in 04.

All notebooks run on the Brian2 simulator by default. Participants with access to the HPI cluster run one cell per hands-on on the SpiNNaker2 chips (`USE_HARDWARE = True`): in notebook 02 as soon as the network works, in notebook 04 once it is trained.

## Setup

The participant install guide is the README of the `main` branch: laptop with uv (`pyproject.toml` and `uv.lock` in the repository root), HPI cluster with conda. Both pin Python 3.12, py-spinnaker2 0.8.5, PyTorch 2.15.0 (CPU), snnTorch 0.9.4, nirtorch 2.0.2, NIR 1.0.4 and numpy 2.3.4. The instructor demos additionally need `tonic`, `networkx` and `pandas`.

