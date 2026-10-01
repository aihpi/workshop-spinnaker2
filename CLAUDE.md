# CLAUDE.md

Planning repository for a 3-hour hands-on SpiNNaker2 workshop (AISC, planned for November 2026). Audience: ML PhD students and software developers. Software: py-spinnaker2 v0.8, run on the chips via the HPI cluster, with the Brian2 backend as fallback.

## Structure

- `01_knowledge_base/`: notes, sources and figures. The notes build on each other: `00_computing_fundamentals.md` (general computing), `01_primer_snn_basics.md` (neural computing), `02_hardware_energy.md` (SpiNNaker2 hardware and energy). Each topic lives in exactly one note; the others link to it. Tracked in git. Downloaded papers or other copyrighted raw material don't belong here, only links in `sources.md`.
- `02_workshop_design/`: brief, outline, demo plans. Tracked in git.
- `03_setup/`: how to run on the cluster (`README.md`) and the failure modes seen so far (`01_troubleshooting.md`), plus `enter_cx51.sh` and the smoke test. Tracked in git.
- `04_spinncloud_tutorials/`: SpiNNcloud's deep-dive tutorial notebooks, run on our chips so the outputs are real. Reference material for learning the API and for checking what works on the hardware — **not** the workshop's own hands-on material, which does not exist yet. Apache-2.0, see the folder README. Tracked in git.
- `py-spinnaker2/`: clone of the vendor library (gitlab, pinned at commit `6c9084fc`), installed non-editable into the conda env `spinnaker2`. **Gitignored**, never commit it. Library source changes need `pip install .` again.
- `_local/`: gitignored working notes, e.g. dated handover plans for the next conversation (`_local/2026-09-30_plan_next_steps.md`). Read the newest plan there when starting a new session.
- `01_knowledge_base/figures/<markdown file name>/` holds the figures of one markdown file together with the script that generates them (e.g. `figures/01_primer_snn_basics/make_figures.py`). Figure file names start with the section number. The scripts also check the numbers the figures show. Run with `uv run --with numpy --with matplotlib --with schemdraw make_figures.py` (no global installs). Regenerate figures through the script, never edit PNGs by hand.

## Writing conventions for markdown notes

The notes serve three purposes: learning material, preparation for workshop slides, and a wiki inside the repo.

- **File names** start with a two-digit number (`01_`, `02_`, …) or a date (`2026-09-28_`). `README.md`, `CHANGELOG.md`, `CLAUDE.md` and `01_knowledge_base/sources.md` are exempt.
- **Neutral tone.** Don't address the reader or a specific person ("you", "we should", "your background").
- **Collapsible blocks** (`<details><summary>…</summary>`) for derivations, side topics and worked examples, so the main text stays lean. Leave a blank line after `</summary>` so markdown renders inside. Put `<br>` after every `</details>` (on its own line, after a blank line), otherwise the layout is too cramped.
- **Equation numbers** on every display equation, numbered sequentially per file with `\tag{n}` inside `$$…$$`. Refer to them as "Eq. (n)". Renumber when inserting a new equation.
- **Axis labels** on every figure axis, always with a unit or scale description ("time (ms)", "v[t] (dimensionless)", "V (units of threshold)"). Spike raster panels get a label too. Never produce a figure without them.
- **Figure numbers** on every figure, numbered sequentially per file. The italic caption starts with `**Figure n.**`. Refer to figures as "Figure n", not "the figure above". Renumber when inserting a new figure.
- **Wikipedia links** at the first mention of important, well-known topics (models, concepts). Verify the URL exists.
- **Table of contents:** long notes start with a `## Contents` list linking all `##` and `###` headings (GitHub anchor format). Update it whenever headings change.
- **Figure sources:** every caption ends with `**Source:**` saying whether the figure is a diagram, simulated or computed here (and whether it has been run on the chip), or reported data with citation.
- **Workshop lines:** each primer section ends with `**Workshop:**` saying what is taught and for how long.
- No hard line wraps in prose.

## Cluster and hardware

The 6-board SpiNNaker2 frame is attached to the cluster node cx51; boards are powered off while idle and powered up per run. Details, install steps and diagnostics are in `03_setup/`, which is the single source for them — don't duplicate them in this file.

The repository is **public**. Internal infrastructure detail (board and controller addresses, MAC addresses, vendor correspondence) does not belong in tracked files; `03_setup/` is written without it and notebook outputs are redacted where they exposed an address. Raw diagnostic logs belong in `_local/`.

## Accuracy

- Chip-specific details (neuron models, parameter names, weight ranges) must match the py-spinnaker2 v0.8 docs: https://spinnaker2.gitlab.io/py-spinnaker2/
- Anything not yet verified on the hardware goes into the "To check on the cluster" list of the relevant note.
- In the text, claims that the sources read so far don't confirm are marked *(assumption, to check)* and listed in the note's "To check on the cluster" list. Sourced claims name their source in brackets, e.g. (py-spinnaker2, profiling) or (chip paper).
- Every figure and number says where it comes from: measured on the chip, reported in a source (with citation), or estimated / simulated here. Estimates and illustrations are labelled as such in the figure itself and in its caption, together with their assumptions.
