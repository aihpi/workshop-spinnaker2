<div style="background-color: #ffffff; color: #000000; padding: 10px;">
<img src="00_aisc/img/logo_aisc_bmftr.jpg">
<h1>Workshop: Neuromorphic Computing on SpiNNaker2</h1>
</div>

This repository holds the material for the 3-hour hands-on workshop on the SpiNNaker2 neuromorphic chip by the [AI Service Centre Berlin Brandenburg](https://hpi.de/kisz), for ML researchers and software developers. Participants learn why neuromorphic hardware can save energy, how spiking neurons and networks work, and how to build spiking networks in Python with [py-spinnaker2](https://spinnaker2.gitlab.io/py-spinnaker2/), by hand and from a PyTorch model via NIR.

Dates: 18 November 2026, 14:00 to 17:00, and 9 December 2026, 10:00 to 13:00, at HPI in Potsdam.

Right now the repository only contains the setup. The workshop notebooks follow shortly before the workshop; on the day, `git pull` fetches them into the same folder.

## Before the workshop: install the environment

Please install the environment before the workshop. There are two ways:

| You are | You work on | Section |
|---|---|---|
| HPI participant with an account on the HPI cluster | the cluster node cx51, which is connected to the SpiNNaker2 chips | [On the HPI cluster (conda)](#on-the-hpi-cluster-conda) |
| everyone else | your laptop, with the Brian2 simulator | [On your laptop (uv)](#on-your-laptop-uv) |

### On your laptop (uv)

You need about **3 GB of free disk space**, an internet connection and 5 to 15 minutes. The workshop runs on the Brian2 simulator, which computes the same spikes as the SpiNNaker2 chip, so no special hardware is needed.

| System | Status |
|---|---|
| Linux | tested |
| macOS with Apple silicon (M1 or newer) | supported, not tested yet |
| Windows | use WSL (Windows Subsystem for Linux) |
| macOS with an Intel processor | not supported: PyTorch no longer provides packages for it |

The setup uses [git](https://git-scm.com/downloads), [uv](https://docs.astral.sh/uv/) and VS Code with the Jupyter extension. If any of them is new to you, the guides of our Getting Started workshop explain how to install them: [WSL](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/02_wsl.md) (Windows only), [git](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/03_git_github.md), [uv](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/04_uv.md) and [Jupyter in VS Code](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/06_jupyter.md).

1. Clone the repository and change into it:
   ```bash
   git clone https://github.com/aihpi/workshop-spinnaker2.git
   cd workshop-spinnaker2
   ```
2. Install the environment. uv downloads Python 3.12 and all packages into the folder `.venv/`:
   ```bash
   uv sync
   ```
3. Open the folder in VS Code (`code .`), open `04_workshop_material/00_setup_check.ipynb`, select the kernel `.venv (Python 3.12)` and run all cells. The last cell shows a small plot, and the cell before it prints "Brian2 works."

If a step fails, please send the error message to kisz@hpi.de before the workshop, or bring it along.

### On the HPI cluster (conda)

On the cluster, the environment is a conda environment, as recommended by py-spinnaker2: runs on the chips compile a small program for the chip, which needs the full source of py-spinnaker2 and `cmake`. The home directory is the same on all cluster nodes, so you can install now on any node you can reach. During the workshop you get access to cx51, the node connected to the chips, and use the same environment there. You need about 3 GB of free space in your home directory, plus the space for Miniforge if you install it.

If you have no conda yet, install [Miniforge](https://github.com/conda-forge/miniforge) into your home directory first. Then, on the cluster:

1. Create the environment with Python 3.12 and `cmake`:
   ```bash
   conda create --name spinnaker2 python=3.12
   conda activate spinnaker2
   conda install -c conda-forge cmake
   ```
2. Install py-spinnaker2 from its source, at release 0.8.2. `--recursive` is needed, because the chip program is a separate repository included as a submodule:
   ```bash
   git clone --recursive https://gitlab.com/spinnaker2/py-spinnaker2.git
   cd py-spinnaker2
   git checkout v0.8.2
   git submodule update --init --recursive
   pip install .
   cd ..
   ```
3. Install PyTorch (CPU version) and the other packages of the workshop:
   ```bash
   pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cpu
   pip install snntorch==0.9.4 nirtorch==2.0.2 nir==1.0.4 numpy==2.3.4 matplotlib ipykernel
   ```
4. Clone this repository:
   ```bash
   git clone https://github.com/aihpi/workshop-spinnaker2.git
   ```
5. Open `workshop-spinnaker2/04_workshop_material/00_setup_check.ipynb` in VS Code (connected to the cluster with Remote-SSH), select the kernel `spinnaker2` and run all cells. The check uses the Brian2 simulator, so it works on any node. The cell before the plot prints "Brian2 works."

How to connect VS Code to cx51 and how to start runs on the chips follows in the workshop.

### Versions

Both environments contain py-spinnaker2 0.8.2 with the Brian2 simulator, PyTorch (CPU version), snnTorch and NIR, with the same version of each of these packages. `pip list` shows py-spinnaker2 as version 0.8.0; that is expected, because release 0.8.2 still carries the old version number.

## Contact

Questions or installation issues: kisz@hpi.de

## License

This project is licensed under the MIT license; see [LICENSE](LICENSE).

## Acknowledgements

<img src="00_aisc/img/logo_bmftr_de.png" alt="Logo of the Federal Ministry of Research, Technology and Space" style="width:170px;"/>

The [AI Service Centre Berlin Brandenburg](https://hpi.de/kisz) is funded by the [Federal Ministry of Research, Technology and Space](https://www.bmftr.bund.de/) under the funding code 01IS22092.
