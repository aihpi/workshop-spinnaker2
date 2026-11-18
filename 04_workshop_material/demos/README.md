# Instructor demos

The demos shown in the last block of the workshop. They are not part of the hands-on: the instructor runs them, and you can run them yourself afterwards.

| Notebook | What it shows | Runs on |
|---|---|---|
| `01_energy.ipynb` | The power of a 48-chip board with an empty board, a large silent network and the same network with every neuron spiking | chip only (about 5 minutes); without the chip it shows the measurement of 19 October 2026 from `05_measurements/` |
| `02_nmnist.ipynb` | A convolutional spiking network, trained elsewhere and imported via NIR, classifies a digit recorded with an event camera (NMNIST) | chip (about 1 minute) or Brian2 |
| `03_maxcut.ipynb` | Noisy spiking neurons search for the best split of a graph (Max-Cut) | chip only |

## Additional packages

Two demos need packages that the workshop environment does not contain:

| Package | Needed by | What for |
|---|---|---|
| `tonic` | `02_nmnist.ipynb` | downloads and reads the NMNIST event-camera dataset (about 170 MB on the first run, see `data/README.md`) |
| `networkx` | `03_maxcut.ipynb` | builds and draws the graphs |

Install them into the environment you use for the workshop:

```bash
uv pip install tonic networkx      # laptop, in the repository folder (.venv)
pip install tonic networkx         # HPI cluster, with the conda environment active
```

Tested with `tonic` 1.7.0 and `networkx` 3.7. `uv pip install` adds them to `.venv` without changing `pyproject.toml`; the next `uv sync` removes them again.

## Why they are not in the workshop environment

- **Only the instructor needs them during the workshop.** The hands-on notebooks 00 to 04 don't use them, and every extra package is one more thing that can fail during the installation.
- **Smaller and faster installation.** `tonic` pulls in further packages for event data, and the NMNIST dataset adds about 170 MB of download, more on disk. With everyone installing over the same Wi-Fi at the start of the workshop, that matters.
- **Two of the three demos need the chip anyway.** Without access to the HPI cluster, only the NMNIST demo runs (on Brian2), and the energy demo shows the stored measurement.
