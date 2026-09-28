# CLAUDE.md

Planning repository for a 3-hour hands-on SpiNNaker2 workshop (AISC, planned for November 2026). Audience: ML PhD students and software developers. Software: py-spinnaker2 v0.8, run on the chips via the HPI cluster, with the Brian2 backend as fallback.

## Structure

- `01_knowledge_base/`: notes, sources and figures. Tracked in git. Downloaded papers or other copyrighted raw material don't belong here, only links in `00_sources.md`.
- `02_workshop_design/`: brief, outline, demo plans. Tracked in git.
- `01_knowledge_base/figures/<markdown file name>/` holds the figures of one markdown file together with the script that generates them (e.g. `figures/01_primer_snn_basics/make_figures.py`). Figure file names start with the section number. The scripts also check the numbers the figures show. Run with `uv run --with numpy --with matplotlib --with schemdraw make_figures.py` (no global installs). Regenerate figures through the script, never edit PNGs by hand.

## Writing conventions for markdown notes

The notes serve three purposes: learning material, preparation for workshop slides, and a wiki inside the repo.

- **File names** start with a two-digit number (`01_`, `02_`, …) or a date (`2026-09-28_`). `README.md`, `CHANGELOG.md` and `CLAUDE.md` are exempt.
- **Neutral tone.** Don't address the reader or a specific person ("you", "we should", "your background").
- **Collapsible blocks** (`<details><summary>…</summary>`) for derivations, side topics and worked examples, so the main text stays lean. Leave a blank line after `</summary>` so markdown renders inside. Put `<br>` after every `</details>` (on its own line, after a blank line), otherwise the layout is too cramped.
- **Equation numbers** on every display equation, numbered sequentially per file with `\tag{n}` inside `$$…$$`. Refer to them as "Eq. (n)". Renumber when inserting a new equation.
- **Figure numbers** on every figure, numbered sequentially per file. The italic caption starts with `**Figure n.**`. Refer to figures as "Figure n", not "the figure above". Renumber when inserting a new figure.
- **Wikipedia links** at the first mention of important, well-known topics (models, concepts). Verify the URL exists.
- **Workshop lines:** each primer section ends with `**Workshop:**` saying what is taught and for how long.
- No hard line wraps in prose.

## Accuracy

- Chip-specific details (neuron models, parameter names, weight ranges) must match the py-spinnaker2 v0.8 docs: https://spinnaker2.gitlab.io/py-spinnaker2/
- Anything not yet verified on the hardware goes into the "To check on the cluster" list of the relevant note.
