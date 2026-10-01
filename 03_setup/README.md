# Setup: running py-spinnaker2 on the HPI cluster

Everything needed to get a working SpiNNaker2 session on the cluster. Problems during a run are collected in [01_troubleshooting.md](01_troubleshooting.md).

| File | Purpose |
|---|---|
| `enter_cx51.sh` | Opens an interactive shell on the node the SpiNNaker2 frame is attached to |
| `smoke_test_lif_neuron.py` | Minimal single-neuron run, confirms the chips are reachable |

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

The library is **not** tracked in this repository. It is cloned next to the repository content as `py-spinnaker2/` (gitignored) and installed into a conda environment.

```bash
conda create --name spinnaker2 python=3.12
conda activate spinnaker2
conda install -c conda-forge cmake          # not covered by libs_install.sh

git clone --recursive https://gitlab.com/spinnaker2/py-spinnaker2.git
cd py-spinnaker2
git checkout v0.8.2                         # pinned, see below
git submodule update --init --recursive    # snn-core at the commit v0.8.2 points to
pip install .
```

Notes on the install:

- `--recursive` is required: `snn-core` is a separate repository included as a submodule.
- The system-level dependencies installed by `libs_install.sh` are already present on cx51 and persist across sessions. `cmake` is missing from that script and has to be installed per conda environment.
- The install is **non-editable**. Changes to the library source need another `pip install .`.
- Updating the clone needs `git pull --no-recurse-submodules` followed by `git submodule update --init --recursive`; a dangling submodule reference in intermediate history breaks the plain `git pull`.

### Pinned version

Release `v0.8.2` (2026-09-23), installed on 2026-10-01. Its `snn-core` submodule points to commit `ccd54d0`; `setup_libs.sh` names the commit before it (`0341893`), which differs only in how the random generators are seeded at start-up and in stricter compiler flags. `pip list` still reports `0.8.0`, because `pyproject.toml` was not bumped; the installed code is v0.8.2.

Compared with the previous pin (`6c9084fc`, v0.8.0 plus the circular-import hotfix), v0.8.1 and v0.8.2 allow repeated `run()` calls on the same `Hardware` object and several networks with the same name (both checked on a board on 2026-10-01). Neuron models and synapse formats are unchanged. The edits to the vendor tutorials made under v0.8.0 are kept as a `git stash` in the clone; their copies are in `04_spinncloud_tutorials/`.

## Smoke test

```bash
conda activate spinnaker2
python 03_setup/smoke_test_lif_neuron.py
```

The run needs **one** board. Boards are tried in order and the first success ends the search, so one or two boards powering up means the allocation worked. All six powering up means every attempt failed.

The script writes `lif_output.png`. `plt.show()` produces no visible output on the cluster, so figures have to be saved to file.

## Fallback without hardware

The Brian2 backend of py-spinnaker2 runs the same networks on the CPU and needs none of the above. It is the fallback for workshop participants if the frame is unavailable.
