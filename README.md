<div style="background-color: #ffffff; color: #000000; padding: 10px;">
<img src="00_aisc/img/logo_aisc_bmftr.jpg">
<h1>Workshop: Neuromorphic Computing on SpiNNaker2</h1>
</div>

This repository contains the setup for the SpiNNaker2 workshop. The workshop materials will be added shortly before the workshop; on the day, you get them with `git pull`.

## Which setup?

| You have | Setup | During the workshop |
|---|---|---|
| no HPI cluster account | [laptop (uv)](#laptop-uv) | you work with the Brian2 simulator, which computes the same spikes as the chips; how to get access to the chips is explained at the end of the workshop |
| an HPI cluster account | [HPI cluster (conda)](#hpi-cluster-conda) | you get access to cx51, the cluster node connected to the SpiNNaker2 chips, for the duration of the workshop |

Please install the environment before the workshop. If something fails, send the error message to kisz@hpi.de or bring it to the workshop.

## Laptop (uv)

You need:

- about 3 GB of free disk space
- Linux, macOS 14 or newer with Apple silicon (M1 or newer), or Windows with WSL; macOS with an Intel processor is not supported, because PyTorch no longer provides packages for it
- [git](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/03_git_github.md), [uv](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/04_uv.md), [VS Code with Jupyter](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/06_jupyter.md); on Windows also [WSL](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/02_wsl.md)

Steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/aihpi/workshop-spinnaker2.git
   cd workshop-spinnaker2
   ```
2. Install Python 3.12 and all packages into the folder `.venv/` (takes 5 to 15 minutes):
   ```bash
   uv sync
   ```
3. Open `04_workshop_material/00_setup_check.ipynb` in VS Code, select the kernel `.venv (Python 3.12)` and run all cells. If everything works, the notebook prints "Brian2 works." and shows a small plot.

## HPI cluster (conda)

You need:

- an account on the HPI cluster and the Scientific Compute VPN, which is not the same as the HPI VPN ([access](https://docs.sc.hpi.de/cluster/processes/access/), [VPN](https://docs.sc.hpi.de/VPN/))
- an SSH connection to the cluster ([SSH](https://docs.sc.hpi.de/ssh/))
- about 3 GB of free space in your home directory

Where to install:

- Not on the login nodes (`hpc.sci.hpi.de`): they don't run scripts from your home directory.
- Use a Run Node instead, `rx01.hpc.sci.hpi.de` or `rx02.hpc.sci.hpi.de` ([Run Nodes](https://docs.sc.hpi.de/cluster/Resources/Run-Nodes/)). Connect there with SSH in a terminal, or with VS Code Remote-SSH ([VS Code](https://docs.sc.hpi.de/cluster/software_installation/VS-Code/)).
- Your home directory is the same on all nodes, so the environment is also available on cx51 during the workshop.

conda:

- If you don't have conda on the cluster yet, run `setup-conda3`, answer `y`, then log out and in again. The script installs Miniconda into `~/conda3`; afterwards your prompt starts with `(base)` ([Python / Conda](https://docs.sc.hpi.de/cluster/software_installation/Python-Conda/), [Install Miniconda3](https://docs.sc.hpi.de/cloud/software-installations/Install-Miniconda3/)).

Steps:

1. Create the environment:
   ```bash
   conda create --name spinnaker2 python=3.12
   conda activate spinnaker2
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
   pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
   pip install snntorch==0.9.4 nirtorch==2.0.2 nir==1.0.4 numpy==2.3.4 matplotlib ipykernel
   ```
4. Clone this repository:
   ```bash
   git clone https://github.com/aihpi/workshop-spinnaker2.git
   ```
5. Open `workshop-spinnaker2/04_workshop_material/00_setup_check.ipynb` in VS Code (Remote-SSH to the Run Node), select the kernel `spinnaker2` and run all cells. If everything works, the notebook prints "Brian2 works." and shows a small plot.

How to connect to cx51 and run your networks on the chips is explained at the start of the workshop.

## Notes

- `pip list` shows py-spinnaker2 as version 0.8.0. That is expected: release 0.8.2 still carries the old number.
- PyTorch is installed without GPU support: the download is much smaller, and the workshop doesn't need a GPU.

## License

MIT, see [LICENSE](LICENSE).

## Acknowledgements

<img src="00_aisc/img/logo_bmftr_de.png" alt="Logo of the Federal Ministry of Research, Technology and Space" style="width:170px;"/>

The [AI Service Centre Berlin Brandenburg](https://hpi.de/kisz) is funded by the [Federal Ministry of Research, Technology and Space](https://www.bmftr.bund.de/) under the funding code 01IS22092.
