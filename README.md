<div style="background-color: #ffffff; color: #000000; padding: 10px;">
<img src="00_aisc/img/logo_aisc_bmftr.jpg">
<h1>Workshop: Neuromorphic Computing on SpiNNaker2</h1>
</div>

This repository holds the material for the 3-hour hands-on workshop on the SpiNNaker2 neuromorphic chip by the [AI Service Centre Berlin Brandenburg](https://hpi.de/kisz), for ML researchers and software developers. Participants learn why neuromorphic hardware can save energy, how spiking neurons and networks work, and how to build spiking networks in Python with [py-spinnaker2](https://spinnaker2.gitlab.io/py-spinnaker2/), by hand and from a PyTorch model via NIR.

Dates: 18 November 2026, 14:00 to 17:00, and 9 December 2026, 10:00 to 13:00, at HPI in Potsdam.

Right now the repository only contains the setup. The workshop notebooks follow shortly before the workshop; on the day, `git pull` fetches them into the same folder.

## Before the workshop: install the environment

Please install the environment on your laptop before the workshop. Participants with access to the HPI cluster work there and can skip this section.

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

The environment contains py-spinnaker2 0.8.2 with the Brian2 simulator, PyTorch (CPU version), snnTorch and NIR. `pip list` shows py-spinnaker2 as version 0.8.0; that is expected, because release 0.8.2 still carries the old version number.

## Contact

Questions or installation issues: kisz@hpi.de

## License

This project is licensed under the MIT license; see [LICENSE](LICENSE).

## Acknowledgements

<img src="00_aisc/img/logo_bmftr_de.png" alt="Logo of the Federal Ministry of Research, Technology and Space" style="width:170px;"/>

The [AI Service Centre Berlin Brandenburg](https://hpi.de/kisz) is funded by the [Federal Ministry of Research, Technology and Space](https://www.bmftr.bund.de/) under the funding code 01IS22092.
