"""Slide figure for slide 9.1: board power of an empty board, a silent and an active network on 1,000 cores.

Measured on the HPI cluster on 2026-10-19 (05_measurements/01_power_baseline/, py-spinnaker2 v0.8.2): one 48-node
board, 20 s runs. Silent: 1,000 cores with 100 lif neurons each, all-to-all, no spikes. Active: the same network,
every neuron spikes in every step (10 billion synaptic events per second). The reading comes in 3 W steps and
changes about once per second; the steady value is the mean after the first 2 s, as in demos/01_energy.ipynb.
The script checks the steady values against the measurement (57, 60, 66 W).
Run: uv run --with numpy --with matplotlib --with pandas --with pyarrow python b9_make_power.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ACCENT, GREY, DARK = "#B1063A", "#83888C", "#212427"  # accent: HPI red (slide style); change here for the block colour
DATA = Path(__file__).resolve().parents[3] / "05_measurements" / "01_power_baseline" / "data"
RUNS = [("idle_1", "empty board", GREY, 57), ("silent_1000", "1,000 cores, silent", DARK, 60),
        ("active_1000", "1,000 cores, every neuron spikes", ACCENT, 66)]


def simulation_window(df):
    """Time since the start of the simulation and the board power, between the sim_start and sim_end markers."""
    marks = dict(zip(df.loc[df.marker.notna(), "marker"], df.loc[df.marker.notna(), "time_s"]))
    sim = df[(df.time_s > marks["sim_start"]) & (df.time_s < marks["sim_end"]) & df.total.notna()]
    return sim.time_s - marks["sim_start"], sim.total


plt.rcParams.update({"font.size": 18, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(13, 6))
for name, label, color, expected in RUNS:
    t, power = simulation_window(pd.read_parquet(DATA / f"{name}.parquet"))
    steady = power[t > 2].mean()
    assert round(steady) == expected, (name, steady)
    ax.step(t, power, where="post", color=color, lw=3)
    ax.text(20.4, steady, f"{label}: {steady:.0f} W", va="center", color=color, fontsize=17)
ax.set(xlim=(0, 20), ylim=(50, 70), yticks=range(50, 71, 5), xticks=range(0, 21, 5), xlabel="time since start of the simulation (s)", ylabel="board power (W, 3 W steps)")
fig.text(0.99, 0.01, "one 48-chip board, HPI cluster, measured 2026-10-19", ha="right", va="bottom", fontsize=11, color=GREY)
fig.subplots_adjust(left=0.09, right=0.62, bottom=0.15, top=0.96)  # room on the right for the labels
out_path = Path(__file__).with_name("b9_power.png")
fig.savefig(out_path, dpi=200)
print("saved", out_path)
