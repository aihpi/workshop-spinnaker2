"""Plot the power measurements stored in data/ and print a summary table.

Usage: uv run --with pandas --with pyarrow --with matplotlib 02_analyse.py

Reads data/runs.csv and the traces data/<name>.parquet written by 01_run_power.py.
The reported value lags the start of the simulation by up to about 1 s, so the
"steady" mean skips the first SKIP_S seconds of each simulation window.
Writes 01_power_traces.png, 02_power_vs_load.png and data/summary.csv.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
DATA = HERE / "data"
SKIP_S = 2.0
EVENTS_PER_CORE_PER_STEP = 100 * 100  # 100 neurons spiking every step, 100 targets each


def sim_window(name):
    df = pd.read_parquet(DATA / f"{name}.parquet")
    marks = dict(zip(df.loc[df.marker.notna(), "marker"], df.loc[df.marker.notna(), "time_s"]))
    s = df[(df.time_s > marks["sim_start"]) & (df.time_s < marks["sim_end"]) & df.total.notna()]
    return (s.time_s - marks["sim_start"]).to_numpy(), s.total.to_numpy()


runs = pd.read_csv(DATA / "runs.csv")
steady = []
for r in runs.itertuples():
    t, p = sim_window(r.name)
    steady.append(p[t > SKIP_S].mean())
runs["steady_W"] = [round(x, 2) for x in steady]
idle = runs.loc[runs["mode"] == "idle", "steady_W"].mean()
runs["above_idle_W"] = (runs.steady_W - idle).round(2)
runs.to_csv(DATA / "summary.csv", index=False)
print(f"idle baseline: {idle:.2f} W (mean of {sum(runs['mode'] == 'idle')} runs)")
print(runs[["name", "mode", "n_cores", "samples", "steady_W", "above_idle_W", "min_W", "max_W"]].to_string(index=False))

# Figure 1: power over time, one panel per mode, colour = number of cores
fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
cmap = plt.get_cmap("viridis")
order = sorted(runs.n_cores.unique())
for ax, mode in zip(axes, ["idle", "silent", "active"]):
    for r in runs[runs["mode"] == mode].sort_values("n_cores").itertuples():
        t, p = sim_window(r.name)
        ax.step(t, p, where="post", color=cmap(order.index(r.n_cores) / max(1, len(order) - 1)),
                label=r.name if mode == "idle" else f"{r.n_cores} core{'s' if r.n_cores > 1 else ''}")
    ax.axvline(SKIP_S, color="0.6", ls=":", lw=1)
    ax.set_title({"idle": "empty board (1 idle neuron)", "silent": "loaded cores, no spikes",
                  "active": "loaded cores, every neuron spikes every step"}[mode], fontsize=9)
    ax.set_xlabel("time since simulation start (s)")
    ax.legend(fontsize=7)
axes[0].set_ylabel("board power (W, 1 W steps)")
fig.suptitle("Power of one 48-node board during 20 s runs (measured on the HPI cluster, 2026-10-19; dotted: start of the steady part)", fontsize=9)
fig.tight_layout()
fig.savefig(HERE / "01_power_traces.png", dpi=150)

# Figure 2: steady power against number of loaded cores
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.axhline(idle, color="0.4", ls="--", lw=1, label=f"empty board ({idle:.0f} W)")
for mode, color in [("silent", "tab:blue"), ("active", "tab:red")]:
    g = runs[runs["mode"] == mode].sort_values("n_cores")
    ax.plot(g.n_cores, g.steady_W, "o-", color=color, label=mode)
ax.set_xscale("log")
ax.set_xlabel("loaded cores (PEs) on the board, log scale; one board has 7,104")
ax.set_ylabel("steady board power (W)")
sec = ax.secondary_xaxis("top", functions=(lambda n: n * EVENTS_PER_CORE_PER_STEP * 1000 / 1e9,
                                           lambda e: e * 1e9 / (EVENTS_PER_CORE_PER_STEP * 1000)))
sec.set_xlabel("active runs: synaptic events per second (billions)")
fig.suptitle("Board power vs. load (measured on the HPI cluster, 2026-10-19, 1 W resolution)", fontsize=9)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "02_power_vs_load.png", dpi=150)
print("figures written")
