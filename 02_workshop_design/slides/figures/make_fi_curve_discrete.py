"""Slide 13: spike count in 1,000 steps against a constant input per step, computed with Brian2.

Same setup as the input-output cell of 04_workshop_material/01_single_neuron.ipynb, with the values of the
slide: 81 lif neurons, i_offset 0 to 0.4, threshold 1, alpha_decay 0.9, reset_by_subtraction, 1,000 steps.
The critical input (1 - alpha_decay) * threshold = 0.1 is marked; a ReLU through the critical input, scaled
to the same count axis, is drawn for comparison. HPI slide palette (ink, greys, HPI Blue).

Run with the conda env spinnaker2-085 (py-spinnaker2 with the Brian2 backend), from any directory:
    python make_fi_curve_discrete.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from spinnaker2 import brian2_sim, snn

INK, GREY, RULE, BLUE = "#212427", "#5a6065", "#d6d7d8", "#007a9e"
plt.rcParams.update({"font.sans-serif": ["Verdana", "DejaVu Sans"], "font.family": "sans-serif",
                     "text.color": INK, "axes.labelcolor": INK, "xtick.color": GREY, "ytick.color": GREY,
                     "axes.edgecolor": GREY, "font.size": 13})

params = {"threshold": 1.0, "alpha_decay": 0.9, "reset": "reset_by_subtraction"}
i_offsets = np.round(np.linspace(0, 0.4, 81), 3)  # one value per neuron
steps = 1000

pop = snn.Population(size=len(i_offsets), neuron_model="lif", params={**params, "i_offset": list(i_offsets)},
                     name="neurons", record=["spikes"])
net = snn.Network("input_output")
net.add(pop)
brian2_sim.Brian2Backend().run(net, steps)

counts = np.array([len(pop.get_spikes().get(i, [])) for i in range(len(i_offsets))])
critical = (1 - params["alpha_decay"]) * params["threshold"]

# checks of the numbers the slide states
assert np.isclose(critical, 0.1)
assert counts[i_offsets <= critical + 1e-9].sum() == 0, "spikes at or below the critical input"
assert (counts[i_offsets > critical + 1e-9] > 0).all(), "no spikes above the critical input"
assert (np.diff(counts) >= 0).all(), "count not monotonic"
print("max count:", counts.max(), "at i_offset", i_offsets[-1])

# ReLU for comparison, scaled to the count at the largest input
slope = counts[-1] / (i_offsets[-1] - critical)
relu = slope * np.maximum(0, i_offsets - critical)

fig, ax = plt.subplots(figsize=(7.5, 5.2))
ax.plot(i_offsets, relu, "--", color=BLUE, lw=2, label="ReLU (scaled)")
ax.plot(i_offsets, counts, "o", color=INK, ms=4.5, label="LIF neuron, Brian2")
ax.axvline(critical, ls=":", color=GREY, lw=1.5)
ax.text(critical + 0.006, counts.max() * 0.97, "critical input 0.1", va="top", color=GREY, fontsize=12)
ax.set_xlabel("constant input per step, i_offset (threshold = 1)")
ax.set_ylabel("spikes in 1,000 steps (count)")
ax.set_xlim(-0.005, 0.405)
ax.set_ylim(bottom=-5)
ax.grid(True, color=RULE, lw=0.6)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.legend(loc="lower right", frameon=False)
fig.savefig(Path(__file__).resolve().parent / "14_fi_curve_discrete.png", dpi=200, bbox_inches="tight",
            facecolor="white")
