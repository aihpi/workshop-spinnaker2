# Workshop Material

Hands-on notebooks and demos of the workshop "Neuromorphic Computing: Spiking Neural Networks on SpiNNaker2". The schedule is in [`02_workshop_design/03_outline.md`](../02_workshop_design/03_outline.md).

## Contents

| File | Content | Block |
|---|---|---|
| `00_setup_check.ipynb` | Checks the packages and runs a tiny network on Brian2; run it before the workshop | 0 |
| `01_first_network.ipynb` | A first spiking network built by hand | 4 (hands-on 1) |
| `02a_nir_minimal.ipynb` | From snnTorch via NIR to SpiNNaker2, small network | 6 (hands-on 2) |
| `02b_nir_end_to_end.ipynb` | Train in snnTorch, export, run | 6 (hands-on 2) |
| `data/` | Data for the notebooks (see its README for sources) | |
| `demos/` | Instructor demos: energy, event-camera digits, Max-Cut | 7 |

Demos tested on the chip on 2026-11-09: Max-Cut finds the optimum of both graphs, NMNIST classifies its sample like Brian2, the energy demo reads 57 W empty, 60 W silent and 63 W active (66 W in the measurement of 2026-10-19). The demos need `tonic` and `networkx` in addition to `requirements.txt`. Notebooks tested on 2026-11-09 on cx51 (Brian2 and chip): 01 and 02a give identical spikes on Brian2 and on the chip; in 02b, training takes about 2 minutes on cx51 and 96 % of the output spikes land on the target.

All notebooks run on the Brian2 simulator by default. Participants with access to the HPI cluster switch to the SpiNNaker2 chips at the end of each hands-on (`USE_HARDWARE = True`).

## Setup for HPI participants (cluster)

To be completed once the workshop environment on cx51 is set up with the cluster admins.

## Setup for participants without cluster access (laptop)

Participants without access to the HPI cluster run everything on the Brian2 simulator on their own laptop. Install the environment **before the workshop**: the download is about 1.5 GB and takes 10–15 minutes.

Requirements: Python 3.10–3.12 (tested with 3.12), [git](https://git-scm.com/downloads) (py-spinnaker2 is installed directly from GitLab), and Jupyter or VS Code with the Python and Jupyter extensions.

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv spinnaker2-workshop
   source spinnaker2-workshop/bin/activate
   ```
   On Windows, activate with `spinnaker2-workshop\Scripts\activate`.
2. Install PyTorch (CPU version, smaller download):
   ```bash
   pip install --upgrade pip
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```
3. Install py-spinnaker2 and the pinned packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Optional, if Jupyter is not installed yet: `pip install jupyterlab`.
5. Open `00_setup_check.ipynb` with the environment as kernel and run all cells. The last line should read "Brian2 works."

Tested on Linux on 2026-11-09 (fresh environment, Python 3.12). Not tested yet on macOS and Windows.

Note: after installing, `pip list` shows `spinnaker2 0.8.0`. That is expected: version 0.8.2 still carries the old version number. Install findings and details: [`03_setup/README.md`](../03_setup/README.md), section "Laptop install for Brian2 only".
