"""Slide figure for slide 9.4: steady board power against the number of loaded cores, silent and active.

Measured on the HPI cluster on 2026-10-19 (05_measurements/01_power_baseline/data/summary.csv, py-spinnaker2 v0.8.2):
one 48-node board, 20 s runs, 100 lif neurons per core. Active: every neuron spikes in every step, 10,000 synaptic
events per core and step. The script checks the values the slide quotes: 57 W empty board, 60 W for 1,000 silent
cores, 66 W for 1,000 active cores, i.e. (66 - 60) W / 1e10 events/s = 0.6 nJ per synaptic event (rough).
Run: uv run --with numpy --with matplotlib --with pandas python b9_make_power_vs_load.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ACCENT, GREY, DARK = "#B1063A", "#83888C", "#212427"  # accent: HPI red (slide style); change here for the block colour
DATA = Path(__file__).resolve().parents[2] / "05_measurements" / "01_power_baseline" / "data" / "summary.csv"

runs = pd.read_csv(DATA)
idle = runs[runs["mode"] == "idle"].steady_W.mean()
active = runs[runs["mode"] == "active"].sort_values("n_cores")
silent = runs[runs["mode"] == "silent"].sort_values("n_cores")
p_active, p_silent = (df.set_index("n_cores").steady_W[1000] for df in (active, silent))
assert (idle, p_silent, p_active) == (57, 60, 66), (idle, p_silent, p_active)
nj = (p_active - p_silent) / (1000 * 10_000 * 1000) * 1e9  # W / (events per second) -> nJ per event
assert round(nj, 1) == 0.6, nj

plt.rcParams.update({"font.size": 18, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(13, 6))
ax.axhline(idle, ls="--", color=GREY, lw=2)
ax.text(1.1, idle - 1.6, f"empty board: {idle:.0f} W", color=GREY, fontsize=16)
ax.plot(active.n_cores, active.steady_W, "o-", color=ACCENT, lw=3, ms=10)
ax.plot(silent.n_cores, silent.steady_W, "o-", color=DARK, lw=3, ms=10)
ax.text(5000, 86.3, "every neuron spikes", color=ACCENT, fontsize=17, ha="right", va="center")
ax.text(3600, 60, "silent", color=DARK, fontsize=17, va="center")
ax.annotate("", xy=(1000, p_active), xytext=(1000, p_silent), arrowprops=dict(arrowstyle="<->", color=DARK, lw=2))
ax.text(1150, (p_active + p_silent) / 2, f"+{p_active - p_silent:.0f} W from spikes\n≈ {nj:.1f} nJ per synaptic event", fontsize=15, va="center", color=DARK)
ax.set(xscale="log", xlim=(0.7, 1.2e4), ylim=(52, 90), xlabel="cores with a network (log scale; one board has 7,104)",
       ylabel="board power (W, 3 W steps)", xticks=[1, 10, 100, 1000, 10000], xticklabels=["1", "10", "100", "1,000", "10,000"])
fig.text(0.99, 0.01, "one 48-chip board, HPI cluster, measured 2026-10-19; 100 neurons per core", ha="right", va="bottom", fontsize=11, color=GREY)
fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.96)
out_path = Path(__file__).with_name("b9_power_vs_load.png")
fig.savefig(out_path, dpi=200)
print("saved", out_path, f"| {nj:.2f} nJ per event")
