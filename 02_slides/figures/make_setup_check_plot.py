"""Slide 10: the plot of 04_workshop_material/00_setup_check.ipynb (code cells 2 and 3), saved as PNG.

Run with the conda env spinnaker2-085 from this folder:
    python make_setup_check_plot.py
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE.parents[1] / "04_workshop_material" / "00_setup_check.ipynb"

code_cells = ["".join(c["source"]) for c in json.load(open(NOTEBOOK))["cells"] if c["cell_type"] == "code"]
namespace = {}
exec(code_cells[1], namespace)  # the tiny network on Brian2
assert list(namespace["spikes"]) == [2, 6, 10], namespace["spikes"]
plt.show = lambda: plt.savefig(HERE / "10_setup_check_plot.png", dpi=200, bbox_inches="tight")
exec(code_cells[2], namespace)  # the plot, exactly as in the notebook
