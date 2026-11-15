"""Slide 28: sketch of a synfire chain, 5 groups of neurons, the volley getting sharper from group to group.

Schematic only: the spike times are drawn from Gaussians with a shrinking spread, not simulated.
HPI slide palette (ink, greys, HPI Blue as the deck's secondary hue).
Run: uv run --with numpy --with matplotlib make_synfire_sketch.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

INK, GREY, RULE, BLUE, BLUE25 = "#212427", "#5a6065", "#d6d7d8", "#007a9e", "#bfdee7"
plt.rcParams.update({"font.sans-serif": ["Verdana", "DejaVu Sans"], "font.family": "sans-serif", "text.color": INK})

rng = np.random.default_rng(3)
n_groups, n_neurons = 5, 8
spreads = [1.0, 0.6, 0.35, 0.18, 0.06]  # schematic: spread of the volley shrinks from group to group
box_w, box_h, gap = 2.0, 2.0, 0.9

fig, ax = plt.subplots(figsize=(10, 3.2))
for g, sd in enumerate(spreads):
    x0 = g * (box_w + gap)
    ax.add_patch(FancyBboxPatch((x0, 0), box_w, box_h, boxstyle="round,pad=0,rounding_size=0.08",
                                fc=BLUE25, ec="none"))
    times = np.clip(rng.normal(0, sd, n_neurons), -0.85, 0.85)  # in units of half a box width
    for k, t in enumerate(times):
        x = x0 + box_w / 2 + t * box_w / 2
        y = 0.25 + k * (box_h - 0.5) / (n_neurons - 1)
        ax.plot([x, x], [y - 0.09, y + 0.09], color=INK, lw=2.5, solid_capstyle="butt")
    ax.text(x0 + box_w / 2, -0.3, f"group {g + 1}", ha="center", va="top", fontsize=13, color=INK)
    if g < n_groups - 1:
        ax.add_patch(FancyArrowPatch((x0 + box_w + 0.1, box_h / 2), (x0 + box_w + gap - 0.1, box_h / 2),
                                     arrowstyle="-|>", mutation_scale=18, color=BLUE, lw=2))
ax.text(-0.25, box_h / 2, "neurons", rotation=90, ha="right", va="center", fontsize=11, color=GREY)
total = n_groups * box_w + (n_groups - 1) * gap
ax.annotate("", xy=(total, -0.95), xytext=(0, -0.95),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1))
ax.text(total / 2, -1.05, "time (schematic, not simulated)",
        ha="center", va="top", fontsize=11, color=GREY)
ax.set_xlim(-0.6, total + 0.1)
ax.set_ylim(-1.55, box_h + 0.1)
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(Path(__file__).resolve().parent / "28_synfire_sketch.png", dpi=200, bbox_inches="tight", facecolor="white")
