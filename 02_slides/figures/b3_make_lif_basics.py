"""Slide figure for block 3: the four steps of an LIF neuron in continuous time.

Leaky integrate-and-fire, tau_m dV/dt = -V, with input spikes as instantaneous jumps of size w.
V is measured relative to rest, in units of the threshold. Evenly spaced input spikes, so the figure shows
integrate, leak, fire and reset without anticipating notebook 01 (no constant input, no timing comparison).
Run: uv run --with numpy --with matplotlib python b3_make_lif_basics.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ORANGE, GREY, DARK = "#DD6108", "#83888C", "#212427"
TAU, W, THRESH, DT = 10.0, 0.5, 1.0, 0.01  # ms, jump per spike, threshold, integration step
inputs = [8, 14, 20, 26, 46]  # ms; evenly spaced train that crosses on the 4th spike, then one spike after the reset
t = np.arange(0, 75, DT)
in_idx = {int(round(s / DT)) for s in inputs}
v = np.zeros_like(t)
out = []
tp, vp = [t[0]], [0.0]  # trace for plotting, with the jump above threshold drawn before the reset
for k in range(1, len(t)):
    v[k] = v[k - 1] * np.exp(-DT / TAU)  # leak: exact exponential decay over one integration step
    if k in in_idx:
        v[k] += W  # integrate: each input spike pushes V up
    if v[k] >= THRESH:  # fire and reset
        out.append(t[k])
        tp.append(t[k]); vp.append(v[k])  # the potential reaches the threshold ...
        v[k] = 0.0  # ... and is reset
    tp.append(t[k]); vp.append(v[k])
assert len(out) == 1, out  # exactly one output spike
t_fire = out[0]

plt.rcParams.update({"font.size": 18, "font.family": "sans-serif", "axes.spines.top": False, "axes.spines.right": False})
fig, (ax_in, ax_v) = plt.subplots(2, 1, figsize=(13, 6.5), sharex=True, gridspec_kw={"height_ratios": [1, 4]})

ax_in.vlines(inputs, 0, 1, color=GREY, lw=3)
ax_in.set(ylim=(0, 1.2), yticks=[])
ax_in.set_ylabel("input\nspikes", rotation=0, ha="right", va="center")
ax_in.spines["left"].set_visible(False)

ax_v.plot(tp, vp, color=DARK, lw=2.5)
ax_v.axhline(THRESH, ls="--", color=GREY, lw=1.5)
ax_v.text(74, THRESH + 0.04, "threshold", ha="right", va="bottom", color=GREY)
ax_v.vlines(t_fire, THRESH, 1.45, color=ORANGE, lw=4)
ax_v.text(t_fire, 1.5, "output spike", ha="center", va="bottom", color=ORANGE)
ax_v.set(ylim=(-0.05, 1.75), xlim=(0, 75), yticks=[0, 1], yticklabels=["rest", "1"])
ax_v.set_xlabel("time (ms)")
ax_v.set_ylabel("membrane potential\n(units of threshold)")

def label(text, xy, xytext):
    ax_v.annotate(text, xy=xy, xytext=xytext, color=ORANGE, fontweight="bold", ha="center",
                  arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1.5))

v_at = lambda x: v[np.searchsorted(t, x)]
label("integrate", (20.2, v_at(20.2)), (12, 1.25))
label("leak", (23, v_at(23)), (24, 0.25))
label("fire", (t_fire, THRESH), (t_fire + 9, 1.25))
label("reset", (t_fire + 0.4, 0.02), (t_fire + 10, 0.55))
label("leak", (54, v_at(54)), (60, 0.75))
fig.text(0.99, 0.01, "illustration: LIF with τ = 10 ms, evenly spaced input spikes", ha="right", va="bottom", fontsize=12, color=GREY)

plt.tight_layout()
out_path = Path(__file__).with_name("b3_lif_basics.png")
fig.savefig(out_path, dpi=200)
print("saved", out_path, "output spike at", round(t_fire, 2), "ms")
