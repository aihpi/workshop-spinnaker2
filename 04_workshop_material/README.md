# Workshop Material

Hands-on notebooks of the workshop "Neuromorphic Computing: Spiking Neural Networks on SpiNNaker2". Install and open them as described in the setup guides: [HPI cluster](../03_setup/01_participants_hpi_cluster.md) or [laptop](../03_setup/02_participants_laptop.md).

| Notebook | Content |
|---|---|
| `00_setup_check.ipynb` | Checks the packages and runs a tiny network on Brian2; run it first |
| `01_single_neuron.ipynb` | Hands-on 1: one spiking neuron with constant input, input spikes and synapses |
| `02_direction_detector.ipynb` | Hands-on 2: a direction detector built by hand from a weight and a delay matrix, with a run on the chip |
| `03_direction_nir.ipynb` | Hands-on 3: the same task trained in snnTorch, exported to NIR, converted and checked spike for spike; more under "After the workshop" |
| `04_direction_trained.ipynb` | Hands-on 3: the task on an 8 × 8 event camera with noise: train, test, run via NIR on the chip |

The folder `demos/` holds the instructor demos shown in the last block: the energy measurement on a 48-chip board, event-camera digits (NMNIST) and Max-Cut. The energy and Max-Cut demos need the chip (the energy demo falls back to measured data); NMNIST also runs on Brian2. NMNIST needs the extra package `tonic`, Max-Cut `networkx`.

All notebooks run on the Brian2 simulator as they are. Participants with access to the HPI cluster run one cell per notebook on the SpiNNaker2 chips: set `USE_HARDWARE = True` in that cell and run it.
