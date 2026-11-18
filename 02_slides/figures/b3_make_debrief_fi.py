"""Slide figure for block 3, debrief after notebook 01, section 1: spike count against constant input.

Same network as notebook 01, section 1 (81 lif neurons, i_offset 0 to 4 in steps of 0.05, threshold 10,
alpha_decay 0.9, reset_by_subtraction, 1,000 steps), run with py-spinnaker2 on Brian2. A ReLU starting at the
critical input is drawn for comparison; its slope is a least-squares fit to the points above it (labelled as such).
Run in the conda env spinnaker2-085: python b3_make_debrief_fi.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from spinnaker2 import brian2_sim, snn

ORANGE, GREY, DARK = "#DD6108", "#83888C", "#212427"
threshold, alpha, steps = 10.0, 0.9, 1000
i_offsets = np.round(np.arange(0, 4.01, 0.05), 2)

pop = snn.Population(size=len(i_offsets), neuron_model="lif", record=["spikes"],
                     params={"threshold": threshold, "alpha_decay": alpha, "i_offset": list(i_offsets), "reset": "reset_by_subtraction"})
net = snn.Network("fi_curve")
net.add(pop)
brian2_sim.Brian2Backend().run(net, steps)
counts = np.array([len(pop.get_spikes().get(i, [])) for i in range(len(i_offsets))])

critical = (1 - alpha) * threshold  # 1.0: below it, v never reaches the threshold
assert counts[i_offsets <= critical].sum() == 0 and (counts[i_offsets > critical + 0.01] > 0).all()
above = i_offsets > critical
x = i_offsets[above] - critical
slope = (x @ counts[above]) / (x @ x)  # least-squares slope of a ReLU through the critical input
relu = slope * np.maximum(0, i_offsets - critical)

plt.rcParams.update({"font.size": 18, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(13, 6.5))
ax.plot(i_offsets, relu, color=ORANGE, lw=2.5, label="ReLU, for comparison (slope fitted)")
ax.plot(i_offsets, counts, "o", color=DARK, ms=6, label="LIF neuron (Brian2)")
ax.axvline(critical, ls="--", color=GREY, lw=1.5)
ax.text(critical - 0.04, counts.max() * 0.45, "critical input\n(1 − α) · threshold = 1.0", color=GREY, va="top", ha="right")
ax.set(xlabel="constant input per step, i_offset (threshold = 10)", ylabel=f"spikes in {steps} steps", xlim=(0, 4.05))
ax.legend(loc="upper left", frameon=False)
fig.text(0.99, 0.01, "notebook 01, section 1: threshold 10, alpha_decay 0.9, reset_by_subtraction", ha="right", va="bottom", fontsize=12, color=GREY)
plt.tight_layout()
out = Path(__file__).with_name("b3_debrief_fi.png")
fig.savefig(out, dpi=200)
print("saved", out, "| max count", counts.max(), "| slope", round(slope, 1))
