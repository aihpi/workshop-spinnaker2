# Workshop setup: laptop (Brian2)

For participants **without** an HPI cluster account. You work with the Brian2 simulator, which computes the same spikes as the SpiNNaker2 chips. How to get access to the chips is explained at the end of the workshop.

## Contents

- [What you have to do](#what-you-have-to-do)
- [A. You have not installed anything yet](#a-you-have-not-installed-anything-yet)
- [B. You installed after our mail of 13 November](#b-you-installed-after-our-mail-of-13-november)
- [Open the repository in VS Code](#open-the-repository-in-vs-code)
- [Running the notebooks](#running-the-notebooks)
- [If something fails](#if-something-fails)

## What you have to do

| Your situation | What to do |
|---|---|
| nothing installed yet | [A](#a-you-have-not-installed-anything-yet), then [open the repository in VS Code](#open-the-repository-in-vs-code) |
| installed after our mail of 13 November | [B](#b-you-installed-after-our-mail-of-13-november) (two commands), then [open the repository in VS Code](#open-the-repository-in-vs-code) |

The packages have not changed since 13 November. Step B only fetches the newest workshop files and checks that your environment still matches.

## A. You have not installed anything yet

You need:

- about 3 GB of free disk space
- Linux, macOS 14 or newer with Apple silicon (M1 or newer), or Windows with WSL; macOS with an Intel processor is not supported, because PyTorch no longer provides packages for it
- [git](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/03_git_github.md), [uv](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/04_uv.md), [VS Code with Jupyter](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/06_jupyter.md); on Windows also [WSL](https://github.com/aihpi/workshop-getting-started/blob/main/03_workshop/guides/02_wsl.md)

Steps, in a terminal (on Windows: in WSL):

1. Clone the repository:
   ```bash
   git clone https://github.com/aihpi/workshop-spinnaker2.git
   cd workshop-spinnaker2
   ```
2. Install Python 3.12 and all packages into the folder `.venv/` inside the repository (5 to 15 minutes, about 0.5 GB download):
   ```bash
   uv sync
   ```

Continue with [Open the repository in VS Code](#open-the-repository-in-vs-code).

## B. You installed after our mail of 13 November

In a terminal (on Windows: in WSL), in your copy of the repository:

```bash
cd workshop-spinnaker2
git pull
uv sync
```

- `git pull` fetches the newest workshop files.
- `uv sync` makes your environment match the repository. If nothing has changed, it finishes within seconds.
- If `git pull` complains about local changes (for example to a notebook you ran), discard them and pull again: `git reset --hard` followed by `git pull`. This undoes your changes to the workshop files; files you created yourself stay.

Continue with [Open the repository in VS Code](#open-the-repository-in-vs-code).

## Open the repository in VS Code

VS Code finds the environment by itself if you open the **whole repository folder**, not a single notebook:

1. On Windows: first connect VS Code to WSL (green button in the lower left corner → "Connect to WSL").
2. **File → Open Folder…** → choose the folder `workshop-spinnaker2` (the one that contains `.venv/`).
3. Open `04_workshop_material/00_setup_check.ipynb`.
4. Click **Select Kernel** (upper right corner) → **Python Environments** → **.venv (Python 3.12)**.
5. Run all cells. If everything works, the notebook prints "Brian2 works." and shows a small plot.

If `.venv` is not in the list: press `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`) → **Python: Select Interpreter** → **Enter interpreter path…** → `.venv/bin/python`, then select the kernel again.

## Running the notebooks

All notebooks run on Brian2 as they are. Cells marked for the SpiNNaker2 chip (`USE_HARDWARE = True`) are for cluster participants; on your laptop, leave them at `False`.

## If something fails

- `uv sync` stops with a network timeout: run it again, it continues where it stopped. On a slow connection: `UV_HTTP_TIMEOUT=120 uv sync`.
- Anything else: ask us.
