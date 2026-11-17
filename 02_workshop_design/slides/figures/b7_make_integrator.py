"""Slide figure for slide 7.6: the same exported neuron, converted with FORWARD or EXPONENTIAL.

snnTorch exports beta = 0.5 (notebook 03) as tau = dt / (1 - beta) with dt = 1e-4 s. py-spinnaker2 turns tau back
into a decay per step: FORWARD gives 1 - dt/tau = 0.5 (snnTorch's beta), the default EXPONENTIAL gives
exp(-dt/tau) = exp(-0.5) = 0.607 (convert_LIF in s2_nir.py). Illustration, computed here: one neuron, threshold 1,
input 0.75 in steps 0 and 2, reset to zero. With 0.5 the potential stays below the threshold, with 0.607 the neuron
fires. The effect on the trained network of notebook 03 (hidden spikes identical in 30 of 60 inputs with
EXPONENTIAL) is measured in the notebook, not here.
Run: uv run --with numpy --with matplotlib python b7_make_integrator.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ACCENT, GREY, DARK = "#B1063A", "#83888C", "#212427"  # accent: HPI red (slide style); change here for the block colour
beta, dt = 0.5, 1e-4
tau = dt / (1 - beta)
alphas = {"FORWARD (as in snnTorch)": 1 - dt / tau, "EXPONENTIAL (default)": np.exp(-dt / tau)}
assert np.isclose(alphas["FORWARD (as in snnTorch)"], beta) and np.isclose(alphas["EXPONENTIAL (default)"], 0.6065, atol=1e-4)
inputs, threshold, steps = {0: 0.75, 2: 0.75}, 1.0, 7


def run(alpha):
    """v per step (after the reset), the value before the reset at spike steps, and the spike steps."""
    v, trace, spikes = 0.0, [], []
    for t in range(steps):
        v = alpha * v + inputs.get(t, 0.0)
        if v >= threshold:
            spikes.append((t, v))
            v = 0.0
        trace.append(v)
    return trace, spikes


plt.rcParams.update({"font.size": 18, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(13, 6))
for (name, alpha), color in zip(alphas.items(), [DARK, ACCENT]):
    trace, spikes = run(alpha)
    shown = list(trace)
    for t, before in spikes:
        shown[t] = before  # draw the value before the reset, then the drop
    ax.plot(range(steps), shown, "o-", color=color, lw=2.5, ms=8, label=f"{name}: decay {alpha:.3g} per step")
    for t, before in spikes:
        ax.plot([t, t + 1], [before, trace[t + 1]], ":", color=color)
        ax.plot(t, before + 0.08, "v", color=color, ms=14)
        ax.text(t + 0.12, before + 0.08, "spike", color=color, va="center")
run_fwd, run_exp = run(alphas["FORWARD (as in snnTorch)"]), run(alphas["EXPONENTIAL (default)"])
assert not run_fwd[1] and [t for t, _ in run_exp[1]] == [2]  # FORWARD stays silent, EXPONENTIAL fires in step 2
ax.axhline(threshold, ls="--", color=GREY, lw=1.5)
ax.text(steps - 1, threshold - 0.03, "threshold", color=GREY, ha="right", va="top")
for t, w in inputs.items():
    ax.annotate(f"input {w}", xy=(t, -0.02), xytext=(t, -0.2), ha="center", color=GREY, fontsize=14,
                arrowprops=dict(arrowstyle="->", color=GREY))
ax.set(xlabel="time step", ylabel="membrane potential v (threshold = 1)", ylim=(-0.25, 1.55), xticks=range(steps))
ax.legend(loc="upper right", frameon=False)
fig.text(0.99, 0.01, "illustration, computed here: snnTorch beta = 0.5 exported as tau = dt / (1 − beta), dt = 1e-4 s; reset to zero",
         ha="right", va="bottom", fontsize=11, color=GREY)
plt.tight_layout(rect=(0, 0.03, 1, 1))
out = Path(__file__).with_name("b7_integrator.png")
fig.savefig(out, dpi=200)
print("saved", out, "| FORWARD peak", round(max(run_fwd[0]), 3), "| EXPONENTIAL spike at", run_exp[1])
