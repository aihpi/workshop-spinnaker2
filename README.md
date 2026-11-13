<div style="background-color: #ffffff; color: #000000; padding: 10px;">
<img src="00_aisc/img/logo_aisc_bmftr.jpg">
<h1>Workshop: Neuromorphic Computing on SpiNNaker2</h1>
</div>

Setup for the SpiNNaker2 workshop. The notebooks follow before the workshop; get them on the day with `git pull`.

## Which setup?

| You have | Setup | During the workshop |
|---|---|---|
| no HPI cluster account | [laptop (uv)](#laptop-uv) | you work with the Brian2 simulator; how to get access to the chips is explained at the end |
| an HPI cluster account | [HPI cluster (conda)](#hpi-cluster-conda) | you get access to cx51, the node connected to the SpiNNaker2 chips |

Install before the workshop. If something fails, send the error message to kisz@hpi.de.

## Laptop (uv)

Needs:

- about 3 GB free disk space
- Linux, macOS with Apple silicon, or Windows with WSL (macOS with Intel processor is not supported)
- [git](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/03_git_github.md), [uv](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/04_uv.md), [VS Code with Jupyter](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/06_jupyter.md); on Windows also [WSL](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/02_wsl.md)

Steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/aihpi/workshop-spinnaker2.git
   cd workshop-spinnaker2
   ```
2. Install Python 3.12 and all packages into `.venv/` (5 to 15 minutes):
   ```bash
   uv sync
   ```
3. Open `04_workshop_material/00_setup_check.ipynb` in VS Code, select the kernel `.venv (Python 3.12)` and run all cells. Expected output: "Brian2 works." and a small plot.

## HPI cluster (conda)

Needs:

- about 3 GB free space in your home directory
- conda; if missing, install [Miniforge](https://github.com/conda-forge/miniforge) into your home directory

Install on any cluster node; the home directory is the same on cx51.

Steps:

1. Create the environment:
   ```bash
   conda create --name spinnaker2 python=3.12
   conda activate spinnaker2
   conda install -c conda-forge cmake
   ```
2. Install py-spinnaker2 0.8.2 from source (`--recursive` fetches the chip code, needed for runs on the chips):
   ```bash
   git clone --recursive https://gitlab.com/spinnaker2/py-spinnaker2.git
   cd py-spinnaker2
   git checkout v0.8.2
   git submodule update --init --recursive
   pip install .
   cd ..
   ```
3. Install the other packages:
   ```bash
   pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cpu
   pip install snntorch==0.9.4 nirtorch==2.0.2 nir==1.0.4 numpy==2.3.4 matplotlib ipykernel
   ```
4. Clone this repository:
   ```bash
   git clone https://github.com/aihpi/workshop-spinnaker2.git
   ```
5. Open `workshop-spinnaker2/04_workshop_material/00_setup_check.ipynb` in VS Code (Remote-SSH to the cluster), select the kernel `spinnaker2` and run all cells. Expected output: "Brian2 works." and a small plot.

How to connect to cx51 is explained at the start of the workshop.

## Notes

- `pip list` shows py-spinnaker2 as version 0.8.0. That is expected: release 0.8.2 still carries the old number.
- PyTorch is installed without GPU support (smaller download, enough for the workshop).

## License

MIT, see [LICENSE](LICENSE).

## Acknowledgements

<img src="00_aisc/img/logo_bmftr_de.png" alt="Logo of the Federal Ministry of Research, Technology and Space" style="width:170px;"/>

The [AI Service Centre Berlin Brandenburg](https://hpi.de/kisz) is funded by the [Federal Ministry of Research, Technology and Space](https://www.bmftr.bund.de/) under the funding code 01IS22092.
