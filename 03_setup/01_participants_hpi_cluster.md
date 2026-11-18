# Workshop setup: HPI cluster (SpiNNaker2 chips)

For participants **with** an HPI cluster account. You install the environment once in your home directory on the cluster. During the workshop you work on cx51, the cluster node connected to the SpiNNaker2 chips, in VS Code, and run your networks on the chips as well as on the Brian2 simulator.

## Contents

- [What you have to do](#what-you-have-to-do)
- [Install](#install)
  - [A. You have not installed anything yet](#a-you-have-not-installed-anything-yet)
  - [B. You installed after our mail of 13 November](#b-you-installed-after-our-mail-of-13-november)
- [One-time: VS Code connection to cx51](#one-time-vs-code-connection-to-cx51)
- [During the workshop: working on cx51](#during-the-workshop-working-on-cx51)
- [If something fails](#if-something-fails)

## What you have to do

| Your situation | First | Then |
|---|---|---|
| nothing installed yet | [A](#a-you-have-not-installed-anything-yet) and the [VS Code connection](#one-time-vs-code-connection-to-cx51) | [working on cx51](#during-the-workshop-working-on-cx51) |
| installed after our mail of 13 November | [B](#b-you-installed-after-our-mail-of-13-november) (one check) and the [VS Code connection](#one-time-vs-code-connection-to-cx51) | [working on cx51](#during-the-workshop-working-on-cx51) |

The packages have not changed since 13 November: an environment installed after that mail is complete.

You need:

- an account on the HPI cluster and the Scientific Compute VPN, which is not the same as the HPI VPN ([access](https://docs.sc.hpi.de/cluster/processes/access/), [VPN](https://docs.sc.hpi.de/VPN/))
- an SSH connection to the cluster ([SSH](https://docs.sc.hpi.de/ssh/))
- VS Code with the extensions Remote - SSH, Python and Jupyter ([VS Code on the cluster](https://docs.sc.hpi.de/cluster/software_installation/VS-Code/))
- about 3 GB of free space in your home directory

## Install

### A. You have not installed anything yet

Install on a Run Node, `rx01.hpc.sci.hpi.de` or `rx02.hpc.sci.hpi.de` ([Run Nodes](https://docs.sc.hpi.de/cluster/Resources/Run-Nodes/)), not on the login nodes: they don't run scripts from your home directory. Your home directory is the same on all nodes, so the environment is available on cx51 later.

1. **conda**, if you don't have it on the cluster yet: run `setup-conda3`, answer `y`, then log out and in again. Miniconda is then in `~/conda3`, and your prompt starts with `(base)` ([Python / Conda](https://docs.sc.hpi.de/cluster/software_installation/Python-Conda/)).
2. **The environment:**
   ```bash
   conda create --name spinnaker2 python=3.12
   conda activate spinnaker2
   ```
3. **py-spinnaker2 0.8.5** from source (`--recursive` fetches the chip code, needed for runs on the chips):
   ```bash
   git clone --recursive https://gitlab.com/spinnaker2/py-spinnaker2.git
   cd py-spinnaker2
   git checkout v0.8.5
   git submodule update --init --recursive
   pip install .
   cd ..
   ```
4. **The other packages:**
   ```bash
   pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
   pip install snntorch==0.9.4 nirtorch==2.0.2 nir==1.0.4 numpy==2.3.4 matplotlib ipykernel
   ```
5. **This repository:**
   ```bash
   git clone https://github.com/aihpi/workshop-spinnaker2.git
   ```

Continue with the [VS Code connection](#one-time-vs-code-connection-to-cx51).

### B. You installed after our mail of 13 November

Check that the environment has the right versions:

```bash
conda activate spinnaker2
pip list | grep -E "^(spinnaker2|torch|snntorch|nir|nirtorch|numpy) "
```

Expected: spinnaker2 0.8.5, torch 2.15.0+cpu, snntorch 0.9.4, nir 1.0.4, nirtorch 2.0.2, numpy 2.3.4. If spinnaker2 shows an older version, repeat step 3 of [A](#a-you-have-not-installed-anything-yet) inside the environment.

Then fetch the newest workshop files:

```bash
cd ~/workshop-spinnaker2
git pull
```

If `git pull` complains about local changes (for example to a notebook you ran), discard them and pull again: `git reset --hard` followed by `git pull`. This undoes your changes to the workshop files; files you created yourself stay.

## One-time: VS Code connection to cx51

Only cx51 talks to the SpiNNaker2 boards, and you can only log in to cx51 while you hold a reservation for it (see below). VS Code reaches cx51 through a Run Node. Add two entries to the SSH configuration on your laptop (VS Code: `Ctrl+Shift+P`, macOS `Cmd+Shift+P` → **Remote-SSH: Open SSH Configuration File…**), with your cluster user name:

```
Host rx02
    HostName rx02.hpc.sci.hpi.de
    User <your user name>

Host cx51
    HostName cx51
    User <your user name>
    ProxyJump rx02
```

- If your cluster key is not your default key (`~/.ssh/id_ed25519` or `~/.ssh/id_rsa`), add the line `IdentityFile <path to your cluster key>` to both entries, as in your existing cluster configuration.
- If you already have an entry for a Run Node, use its name after `ProxyJump` instead of adding `rx02`. `rx01` works the same way.

## During the workshop: working on cx51

**1. Find your Slurm account** (once). On a Run Node (`ssh rx02`):

```bash
sacctmgr -n show assoc user=$USER format=account,qos
```

Use the account whose QOS list contains `early-access`: you get it for the workshop. If no line shows `early-access`, tell us at the start of the workshop.

**2. Reserve cx51.** In a terminal on a Run Node (`ssh rx02`, not a login node: login nodes don't run scripts from your home directory), in the repository:

```bash
cd ~/workshop-spinnaker2
bash 03_setup/enter_cx51.sh <your account>      # e.g. bash 03_setup/enter_cx51.sh my-group
```

The prompt changes to cx51. **Keep this terminal open** for the whole workshop: the reservation lasts as long as this shell runs (at most 6 hours), and your VS Code session on cx51 runs inside it. Typing `exit` ends the reservation.

**3. Connect VS Code.** `Ctrl+Shift+P` → **Remote-SSH: Connect to Host…** → `cx51`. The first connection installs the VS Code server in your home directory and takes a minute.

**4. Open the repository as a folder.** **File → Open Folder…** → `~/workshop-spinnaker2`. Open the whole folder, not a single notebook: then VS Code finds your conda environments.

**5. Select the kernel.** Open a notebook, click **Select Kernel** (upper right) → **Python Environments** → **spinnaker2** (`~/conda3/envs/spinnaker2`). Start with `04_workshop_material/00_setup_check.ipynb`: it prints "Brian2 works." and shows a small plot.

If `spinnaker2` is not in the list: `Ctrl+Shift+P` → **Python: Select Interpreter** → **Enter interpreter path…** and paste the full path, which this command prints in the cx51 terminal:

```bash
echo ~/conda3/envs/spinnaker2/bin/python
```

**6. Run on the chips.** Each hands-on notebook has one cell for the chips with `USE_HARDWARE = False` at the top. Set it to `True` and run the cell. There are 6 boards for everyone; a run takes about a minute and waits if all boards are busy. Everything else runs on Brian2.

**7. At the end:** type `exit` in the terminal from step 2. This frees the reservation.

## If something fails

- **`srun` refuses the account or the QOS:** you used an account without `early-access` (step 1), or the access has not been set up for you yet: tell us.
- **VS Code cannot connect to `cx51`:** check that the terminal from step 2 is still open (without a reservation, cx51 refuses the login) and that the Scientific Compute VPN is on.
- **The kernel dies or keeps restarting:** most likely out of memory. Shut down the kernels of notebooks you have finished and restart this one.
- **A chip run prints `All machines are busy … Retrying`:** all six boards are in use. The run waits by itself and starts when a board is free.
- Anything else: ask us.
