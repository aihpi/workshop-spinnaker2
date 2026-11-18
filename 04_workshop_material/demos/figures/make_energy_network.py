"""Diagram for the energy demo (01_energy.ipynb, section 1): the network on one core and the three options.

Left: one core holds one population of 100 lif neurons, each connected to all 100 (10,000 synapses); drawn with 8
neurons for readability. Right: one 48-chip board per option, each chip a square; the cores the option uses are
coloured (1,000 cores fill about 7 of the 48 chips, at 148 cores per chip for applications). Diagram, not data.
Run from this folder: uv run --with numpy --with matplotlib python make_energy_network.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

COLORS = {"empty": "0.55", "silent": "#1f5fa8", "active": "#c0392b"}  # the same colours as the plot in the notebook
CORES_PER_CHIP = 148  # cores per chip available for applications (152 minus 4 for the system)

fig = plt.figure(figsize=(12, 4.8))
gs = fig.add_gridspec(1, 4, width_ratios=[1.25, 1, 1, 1], wspace=0.25)

# --- left: one core with 100 neurons, all-to-all ---
ax = fig.add_subplot(gs[0])
ax.set(xlim=(-1.6, 1.6), ylim=(-1.75, 1.6), aspect="equal")
ax.axis("off")
ax.add_patch(FancyBboxPatch((-1.35, -1.25), 2.7, 2.6, boxstyle="round,pad=0.05", fc="0.97", ec="0.4", lw=1.5))
angles = np.linspace(0, 2 * np.pi, 8, endpoint=False) + np.pi / 8
xy = np.c_[np.cos(angles), np.sin(angles)] * 0.9
for i in range(8):
    for j in range(i + 1, 8):
        ax.plot(*zip(xy[i], xy[j]), color="0.75", lw=0.8, zorder=1)
for x, y in xy:
    ax.add_patch(Circle((x, y), 0.14, fc="white", ec="0.2", lw=1.5, zorder=2))
ax.text(0, 1.45, "one core (processing element)", ha="center", fontsize=11, weight="bold")
ax.text(0, -1.5, "100 lif neurons, each connected to all 100\n= 10,000 synapses per core (8 neurons drawn)", ha="center", va="top", fontsize=9.5)

# --- right: one board per option ---
options = [
    ("empty", "empty board", 1, "1 neuron on 1 core,\nno input:\nnothing happens"),
    ("silent", "1,000 cores, silent", 1000, "the core on the left,\n1,000 times, no input:\nno neuron spikes"),
    ("active", "1,000 cores, active", 1000, "the same, with an input\nabove the threshold: every\nneuron spikes in every step"),
]
for k, (mode, title, cores, text) in enumerate(options):
    ax = fig.add_subplot(gs[k + 1])
    ax.set(xlim=(-0.3, 8.3), ylim=(-3.6, 6.9), aspect="equal")
    ax.axis("off")
    ax.text(4, 6.55, title, ha="center", fontsize=11, weight="bold", color=COLORS[mode])
    left = cores
    for chip in range(48):
        row, col = divmod(chip, 8)
        fill = min(left, CORES_PER_CHIP) / CORES_PER_CHIP
        left -= min(left, CORES_PER_CHIP)
        x, y = col, 5 - row
        ax.add_patch(Rectangle((x + 0.08, y + 0.08), 0.84, 0.84, fc="white", ec="0.6", lw=0.8))
        if fill > 0 and cores == 1:
            ax.add_patch(Circle((x + 0.5, y + 0.5), 0.2, fc=COLORS[mode], ec="none"))
        elif fill > 0:
            ax.add_patch(Rectangle((x + 0.08, y + 0.08), 0.84 * max(fill, 0.12), 0.84, fc=COLORS[mode], ec="none"))
            if mode == "active":
                ax.text(x + 0.5, y + 0.5, "⚡", ha="center", va="center", fontsize=8, color="white")
    ax.text(4, -0.35, "one board: 48 chips (squares)", ha="center", va="top", fontsize=8.5, color="0.4")
    ax.text(4, -1.25, text, ha="center", va="top", fontsize=9.5)

out = Path(__file__).with_name("energy_network.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print("saved", out)
