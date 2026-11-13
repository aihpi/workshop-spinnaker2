# Setup: running py-spinnaker2 on the HPI cluster

Everything needed to get a working SpiNNaker2 session on the cluster. Problems during a run are collected in [01_troubleshooting.md](01_troubleshooting.md).

| File | Purpose |
|---|---|
| `enter_cx51.sh` | Opens an interactive shell on the node the SpiNNaker2 frame is attached to |
| `smoke_test_lif_neuron.py` | Minimal single-neuron run, confirms the chips are reachable |
| `compare_brian2_chip.py` | Runs the same small networks on the chip and on Brian2, for comparing the backends |
| `brian2_edge_cases.py` | Edge cases and known errors of the Brian2 backend, no board needed |

## The machine

The SpiNNaker2 frame (6 boards, 48 chips each, 148 usable cores per chip, so 7104 per board) is attached to the cluster node **cx51**. The boards sit on a private network together with a frame controller that handles power and boot. The controller is always on; the boards are powered off while idle and are powered up per run. Boards therefore do not answer pings between runs, which is the normal state and not a fault.

Power and boot commands travel from cx51 to the frame controller and from there to the boards over an internal bus. Application data, including the reachability ping, travels directly between cx51 and a board. These are two separate paths over two separate sets of cables, which matters when diagnosing a failure.

The cluster-wide configuration file is referenced by `/etc/opt/spinnaker/SPINNAKER_CONFIG_PATH`; allocation lockfiles live next to it. Neither needs to be edited for a normal run.

## Getting a shell on cx51

```bash
bash 03_setup/enter_cx51.sh
```

which runs

```bash
srun -A aisc --partition=pot-hpi-early-access --qos=early-access \
     --time=06:00:00 --mem=4G --nodelist=cx51 --pty bash
```

`ssh cx51` also works, including from outside the cluster through a ProxyJump over a login node. That is the path VSCode Remote-SSH uses, which is how the notebooks are run.

A single command can be sent to the node without an interactive session:

```bash
echo 'command' | srun -A aisc --partition=pot-hpi-early-access \
     --qos=early-access --nodelist=cx51 --pty bash
```

## Installing py-spinnaker2

The library is **not** tracked in this repository. It is cloned and installed into a conda environment. Since 2026-11-13 there are two environments on the cluster:

| Environment | Version | Use |
|---|---|---|
| `spinnaker2-085` | v0.8.5 | the version participants install (README on `main`); development and tests |
| `spinnaker2` | v0.8.2 | fallback, and the instructor demos (the energy demo shows a PE error with v0.8.5, see below) |

The `spinnaker2` environment is installed from the clone `py-spinnaker2/` next to the repository content (gitignored). The commands below install v0.8.5; for v0.8.2, check out `v0.8.2` instead.

```bash
conda create --name spinnaker2-085 python=3.12
conda activate spinnaker2-085

git clone --recursive https://gitlab.com/spinnaker2/py-spinnaker2.git
cd py-spinnaker2
git checkout v0.8.5                         # pinned, see below
git submodule update --init --recursive    # snn-core at the commit v0.8.5 points to
pip install .
```

Notes on the install:

- `--recursive` is required: `snn-core` is a separate repository included as a submodule.
- The system-level dependencies installed by `libs_install.sh` are already present on cx51 and persist across sessions. `cmake` is now installed system-wide on cx51 too (`/usr/bin/cmake` 3.28.3, checked 2026-11-13; the `spinnaker2` environment has no cmake of its own and builds the chip programs fine). Earlier it had to be installed per conda environment with `conda install -c conda-forge cmake`.
- The install is **non-editable**. Changes to the library source need another `pip install .`.
- Updating the clone needs `git pull --no-recurse-submodules` followed by `git submodule update --init --recursive`; a dangling submodule reference in intermediate history breaks the plain `git pull`.

### Pinned version

**v0.8.5** (2026-11-10), tested on 2026-11-13. Changes since v0.8.2: a fix for spikes injected from the host (v0.8.3), `LIBS_COMMIT` in `setup_libs.sh` matching the submodule pointer and a newer SpiNNMan (v0.8.4), options for board power-on and power-off in `hardware.run()` (v0.8.5). The chip code (`snn-core` `ccd54d0`) is the same as with v0.8.2, and `pip list` reports the correct version. Why the upgrade: with v0.8.2, a git install runs `setup_libs.sh`, which fails on macOS (bash 3.2, see `01_troubleshooting.md`). Tested with v0.8.5: all participant notebooks on Brian2 (uv, Linux and macOS) and 02–04 on the chip, identical to v0.8.2; Max-Cut and NMNIST demos as before. **Open issue:** in the energy demo (1,000 cores), the active run reported an error on PE `Chip_1_0_QPE_7_6_3` with undecodable logs, in 2 of 2 runs; v0.8.2 showed no error in the same demo. Reported to the vendor: to do.

**v0.8.2**, the previous pin: release `v0.8.2` (2026-09-23), installed on 2026-10-01. Its `snn-core` submodule points to commit `ccd54d0`; `setup_libs.sh` names the commit before it (`0341893`), which differs only in how the random generators are seeded at start-up and in stricter compiler flags. `pip list` still reports `0.8.0`, because `pyproject.toml` was not bumped; the installed code is v0.8.2.

Compared with the previous pin (`6c9084fc`, v0.8.0 plus the circular-import hotfix), v0.8.1 and v0.8.2 allow repeated `run()` calls on the same `Hardware` object and several networks with the same name (both checked on a board on 2026-10-01). Neuron models and synapse formats are unchanged. The edits to the vendor tutorials made under v0.8.0 are kept as a `git stash` in the clone; their copies are in `_local/04_spinncloud_tutorials/`.

## Smoke test

```bash
conda activate spinnaker2
python 03_setup/smoke_test_lif_neuron.py
```

The run needs **one** board. Boards are tried in order and the first success ends the search, so one or two boards powering up means the allocation worked. All six powering up means every attempt failed.

The script writes `lif_output.png`. `plt.show()` produces no visible output on the cluster, so figures have to be saved to file.

## Fallback without hardware

The Brian2 backend of py-spinnaker2 runs the same networks on the CPU and needs none of the above. It is the fallback for workshop participants if the frame is unavailable. What it supports and where it differs from the chip: [`01_knowledge_base/03_brian2_fallback.md`](../01_knowledge_base/03_brian2_fallback.md).

### Laptop install for Brian2 only

Participants without cluster access use Brian2 on their own laptop. Since 2026-11-13 they install with uv from `pyproject.toml` and `uv.lock` in the repository root; the step-by-step guide is the README of the `main` branch. Findings of the first install test of 2026-11-09 (fresh virtual environment on cx51, Python 3.12, pip only; the uv test of 2026-11-13 confirmed them and showed that py-spinnaker2 0.8.2 needs Python 3.12 or newer, because PACMAN2 requires it):

- **py-spinnaker2 is not on PyPI.** pip installs it from GitLab (`spinnaker2 @ git+https://gitlab.com/spinnaker2/py-spinnaker2.git@v0.8.5`; v0.8.2 at the time of this test), together with the vendor packages PACMAN2, SpiNNMan2, SpiNNMachine2, SpiNNUtilities2 and spinnaker2_stm. git must be installed.
- **No chip toolchain needed.** The install works without cmake or ARM compilers; those are only needed to compile chip programs for runs on the hardware.
- **Size and time:** 1.5 GB, of which torch (CPU version) about 1 GB; about 12 minutes on cx51 (torch 4.6 min, the rest 7 min).
- **Version number:** pip reports `spinnaker2 0.8.0` after installing v0.8.2, because the vendor did not update the version in `pyproject.toml` (as for the cluster install above).
- **Checked:** a small `lif` network on Brian2 and the NIR path snnTorch → NIR → py-spinnaker2 → Brian2.
- **Not tested yet:** macOS, Windows, Python 3.13 and newer. Planned: a test on a Mac and on a Windows or Linux laptop before the workshop.

