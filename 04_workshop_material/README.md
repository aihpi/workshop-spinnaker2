# Workshop Material

Hands-on notebooks and demos of the workshop "Neuromorphic Computing: Spiking Neural Networks on SpiNNaker2". The schedule is in [`02_workshop_design/03_outline.md`](../02_workshop_design/03_outline.md).

## Contents

| File | Content | Block |
|---|---|---|
| `00_setup_check.ipynb` | Checks the packages and runs a tiny network on Brian2; run it before the workshop | 2 |
| `01_single_neuron.ipynb` | One spiking neuron: constant input, input spikes and synapses; points to the vendor tutorials for more | 4 (hands-on 1) |
| `02_synfire_chain.ipynb` | A network built by hand: a synfire chain, synaptic events, chip run | 6 (hands-on 2) |
| `03_nir_minimal.ipynb` | From snnTorch via NIR to SpiNNaker2, small network | 8 (hands-on 3) |
| `04_nir_end_to_end.ipynb` | Train in snnTorch, export, run | 8 (hands-on 3) |
| `data/` | Data for the notebooks (see its README for sources) | |
| `demos/` | Instructor demos: energy, event-camera digits, Max-Cut | 9 |

Demos tested on the chip on 2026-11-09: Max-Cut finds the optimum of both graphs, NMNIST classifies its sample like Brian2, the energy demo reads 57 W empty, 60 W silent and 63 W active (66 W in the measurement of 2026-10-19). The demos need `tonic` and `networkx` in addition to `requirements.txt`. Notebooks tested on 2026-11-09 on cx51 (Brian2 and chip): 02 (synfire chain) and 03 give identical spikes on Brian2 and on the chip; in 04, training takes about 2 minutes on cx51 and 96 % of the output spikes land on the target.

All notebooks run on the Brian2 simulator by default. Participants with access to the HPI cluster switch to the SpiNNaker2 chips at the end of each hands-on (`USE_HARDWARE = True`).

## Setup

The participant install guide is the README of the `main` branch: laptop with uv (`pyproject.toml` and `uv.lock` in the repository root), HPI cluster with conda. Both pin Python 3.12, py-spinnaker2 0.8.2, PyTorch 2.15.0 (CPU), snnTorch 0.9.4, nirtorch 2.0.2, NIR 1.0.4 and numpy 2.3.4. The instructor demos additionally need `tonic`, `networkx` and `pandas`.

