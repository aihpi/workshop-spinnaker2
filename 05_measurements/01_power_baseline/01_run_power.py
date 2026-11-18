"""Run one power measurement on a 48-node board and store the power trace.

Usage (on cx51, conda env spinnaker2):
    python 01_run_power.py <name> <n_cores> <mode> [time_steps]

    name        label of the run, used as file name in data/
    n_cores     number of cores (PEs) to load; each core holds one population
    mode        "idle"   : 1 neuron that never spikes (n_cores is ignored)
                "silent" : n_cores populations of 100 lif neurons with recurrent
                           synapses, but no input, so nothing spikes
                "active" : same network, but every neuron spikes in every step
                           (i_offset above threshold), so each core processes
                           100 x 100 = 10,000 synaptic events per step
    time_steps  default 20000, i.e. 20 s at the default 1 ms per step

Writes data/<name>.parquet (the power trace as recorded by py-spinnaker2) and
appends one line with the summary to data/runs.csv. Nothing is recorded from
the neurons, so long runs don't fill the core memory.
"""

import csv
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from spinnaker2 import hardware, snn
from spinnaker2.tools import diagnostic_folder_utils as dfu

NEURONS_PER_CORE = 100
HERE = Path(__file__).parent
DATA = HERE / "data"


def build(n_cores, mode):
    net = snn.Network(f"power_{mode}_{n_cores}")
    if mode == "idle":
        net.add(snn.Population(size=1, neuron_model="lif", params={"threshold": 1.0}, name="idle", record=[]))
        return net
    # all-to-all within each population, weight 1, delay 0; one array shared by all populations
    pre, post = np.meshgrid(np.arange(NEURONS_PER_CORE), np.arange(NEURONS_PER_CORE), indexing="ij")
    conns = np.stack([pre.ravel(), post.ravel(), np.ones(pre.size), np.zeros(pre.size)], axis=1).astype(int)
    # active: i_offset 2 > threshold 1, so every neuron spikes every step; silent: no drive at all
    params = {"threshold": 1.0, "alpha_decay": 0.9, "i_offset": 2.0 if mode == "active" else 0.0}
    for k in range(n_cores):
        pop = snn.Population(size=NEURONS_PER_CORE, neuron_model="lif", params=params, name=f"p{k}", record=[])
        net.add(pop, snn.Projection(pre=pop, post=pop, connections=conns))
    return net


def main():
    name, n_cores, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    steps = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
    DATA.mkdir(exist_ok=True)
    dfu.set_level("persistent")  # every run gets its own diagnostic folder

    t0 = time.time()
    net = build(n_cores, mode)
    hardware.SpiNNcloud48NodeBoard().run(net, steps, record_power=True)
    wall = time.time() - t0

    df = pd.read_parquet(dfu.get_path() / "power.parquet")
    shutil.copy(dfu.get_path() / "power.parquet", DATA / f"{name}.parquet")
    marks = dict(zip(df.loc[df.marker.notna(), "marker"], df.loc[df.marker.notna(), "time_s"]))
    sim = df[(df.time_s > marks["sim_start"]) & (df.time_s < marks["sim_end"]) & df.total.notna()].total

    row = {
        "name": name, "mode": mode, "n_cores": n_cores if mode != "idle" else 1,
        "time_steps": steps, "sim_s": round(marks["sim_end"] - marks["sim_start"], 3),
        "samples": len(sim), "mean_W": round(sim.mean(), 3), "std_W": round(sim.std(), 3),
        "min_W": sim.min(), "max_W": sim.max(), "wall_s": round(wall, 1),
        "started": datetime.now().isoformat(timespec="seconds"),
    }
    new = not (DATA / "runs.csv").exists()
    with open(DATA / "runs.csv", "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row)
        if new:
            w.writeheader()
        w.writerow(row)
    print("RESULT", row)


if __name__ == "__main__":
    main()
