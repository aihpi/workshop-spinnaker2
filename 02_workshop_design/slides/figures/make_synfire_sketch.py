"""Slide 26: sketch of a synfire chain as in notebook 02, a kick followed by groups 0 to 4, the volley
getting sharper from group to group.

Schematic only: the spike times are drawn from Gaussians with a shrinking spread, not simulated; the figure
says so in its top-right corner. HPI slide palette (ink, greys, HPI Blue as the deck's secondary hue).
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
n_neurons = 8
# schematic: the kick is spread out, the volley sharpens and, from group 2 on, fires in one step (notebook 02)
stages = [("kick", 1.0), ("group 0", 0.5), ("group 1", 0.22), ("group 2", 0.0), ("group 3", 0.0), ("group 4", 0.0)]
box_w, box_h, gap = 1.7, 1.7, 0.7

fig, ax = plt.subplots(figsize=(10, 2.9))
for g, (name, sd) in enumerate(stages):
    x0 = g * (box_w + gap)
    is_kick = g == 0
    ax.add_patch(FancyBboxPatch((x0, 0), box_w, box_h, boxstyle="round,pad=0,rounding_size=0.08",
                                fc=RULE if is_kick else BLUE25, ec="none"))
    times = np.clip(rng.normal(0, sd, n_neurons), -0.85, 0.85)  # in units of half a box width
    for k, t in enumerate(times):
        x = x0 + box_w / 2 + t * box_w / 2
        y = 0.22 + k * (box_h - 0.44) / (n_neurons - 1)
        ax.plot([x, x], [y - 0.08, y + 0.08], color=GREY if is_kick else INK, lw=2.5, solid_capstyle="butt")
    ax.text(x0 + box_w / 2, -0.25, name, ha="center", va="top", fontsize=13, color=GREY if is_kick else INK)
    if g < len(stages) - 1:
        ax.add_patch(FancyArrowPatch((x0 + box_w + 0.08, box_h / 2), (x0 + box_w + gap - 0.08, box_h / 2),
                                     arrowstyle="-|>", mutation_scale=16, color=BLUE, lw=2))
total = len(stages) * box_w + (len(stages) - 1) * gap
ax.text(-0.2, box_h / 2, "neurons", rotation=90, ha="right", va="center", fontsize=11, color=GREY)
ax.annotate("", xy=(total, -0.85), xytext=(0, -0.85), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1))
ax.text(total / 2, -0.93, "time", ha="center", va="top", fontsize=11, color=GREY)
ax.text(total, box_h + 0.12, "schematic, not simulated", ha="right", va="bottom", fontsize=11, color=GREY,
        style="italic")
ax.set_xlim(-0.55, total + 0.05)
ax.set_ylim(-1.35, box_h + 0.45)
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(Path(__file__).resolve().parent / "28_synfire_sketch.png", dpi=200, bbox_inches="tight", facecolor="white")
