"""Slide 1.8: illustration of a spike raster, 40 neurons over 100 time steps, sparse random spikes, one dot per spike.

Not simulated and not measured: each neuron fires in each step with probability 0.02 (random, seed fixed).
The figure says "illustration" in its top-right corner.
Run: uv run --with numpy --with matplotlib b1_make_raster.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

INK, GREY, RULE = "#212427", "#5a6065", "#d6d7d8"
plt.rcParams.update({"font.sans-serif": ["Verdana", "DejaVu Sans"], "font.family": "sans-serif", "text.color": INK,
                     "axes.edgecolor": GREY, "axes.labelcolor": INK, "xtick.color": GREY, "ytick.color": GREY})

rng = np.random.default_rng(7)
n_neurons, n_steps, p = 40, 100, 0.02
spikes = rng.random((n_neurons, n_steps)) < p
nrn, t = np.nonzero(spikes)
print(f"{spikes.sum()} spikes, {spikes.mean():.1%} of neuron-steps")

fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.scatter(t, nrn, s=22, color=INK, linewidths=0)
ax.set_xlim(-1, n_steps)
ax.set_ylim(-1, n_neurons)
ax.set_xlabel("time step", fontsize=15)
ax.set_ylabel("neuron", fontsize=15)
ax.tick_params(labelsize=13)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.text(1.0, 1.02, "illustration", transform=ax.transAxes, ha="right", va="bottom", fontsize=13, color=GREY,
        style="italic")
fig.savefig(Path(__file__).resolve().parent / "b1_raster.png", dpi=200, bbox_inches="tight", facecolor="white")
