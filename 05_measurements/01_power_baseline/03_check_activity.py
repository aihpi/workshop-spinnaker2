"""Check that the "active" networks of 01_run_power.py really do what they should.

Usage (on cx51, conda env spinnaker2):
    python 03_check_activity.py <n_cores> [time_steps]

Builds the same active network as 01_run_power.py (n_cores populations of 100 lif
neurons, every neuron driven above threshold, all-to-all within the population),
but runs it shorter (default 2000 steps = 2 s) and observes 10 populations spread
over the network:
  - spikes recorded to DRAM, to check that every neuron spikes in every step
  - profiling on, to count missed deadlines (deadline_flag > 0)
Power is recorded as well. Appends one line to data/activity_checks.csv.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from spinnaker2 import hardware, snn
from spinnaker2.tools import diagnostic_folder_utils as dfu

N = 100  # neurons per population, as in 01_run_power.py
DATA = Path(__file__).parent / "data"


def main():
    n_cores = int(sys.argv[1])
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    dfu.set_level("persistent")

    pre, post = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
    conns = np.stack([pre.ravel(), post.ravel(), np.ones(pre.size), np.zeros(pre.size)], axis=1).astype(int)
    params = {"threshold": 1.0, "alpha_decay": 0.9, "i_offset": 2.0}
    watched = set(np.linspace(0, n_cores - 1, min(10, n_cores)).astype(int))

    net = snn.Network(f"check_{n_cores}")
    pops = {}
    for k in range(n_cores):
        obs = k in watched
        pop = snn.Population(size=N, neuron_model="lif", params=params, name=f"p{k}",
                             record=["spikes"] if obs else [], record_on_dram=obs, profile=obs)
        net.add(pop, snn.Projection(pre=pop, post=pop, connections=conns))
        if obs:
            pops[k] = pop

    hardware.SpiNNcloud48NodeBoard().run(net, steps, record_power=True)
    folder = dfu.get_path()

    # spikes: every neuron should spike in (almost) every step
    counts = np.array([len(s) for p in pops.values() for s in p.get_spikes().values()])
    # deadlines, read as in py-spinnaker2 tutorial 05
    prof = pd.read_parquet(folder / "profiling.parquet")
    cb = prof[prof["idx_name"] == "PROFILE_CALLBACK_IDX"]
    missed = int((cb.groupby("timestamp")["deadline_flag"].sum() > 0).sum())
    per_pe = cb.groupby("population")["deadline_flag"].apply(lambda f: int((f > 0).sum()))
    dur = cb["duration_us"]
    # power over the second half of the run
    pw = pd.read_parquet(folder / "power.parquet")
    marks = dict(zip(pw.marker.dropna(), pw.time_s[pw.marker.notna()]))
    sim = pw[(pw.time_s > marks["sim_start"] + (marks["sim_end"] - marks["sim_start"]) / 2)
             & (pw.time_s < marks["sim_end"]) & pw.total.notna()].total

    row = {
        "n_cores": n_cores, "time_steps": steps, "watched_pops": len(pops),
        "spikes_per_neuron_min": int(counts.min()), "spikes_per_neuron_mean": round(counts.mean(), 1),
        "spikes_per_neuron_max": int(counts.max()),
        "steps_with_missed_deadline": missed, "watched_pes_with_misses": int((per_pe > 0).sum()),
        "callback_us_median": round(dur.median(), 1), "callback_us_max": round(dur.max(), 1),
        "power_second_half_W": round(sim.mean(), 2),
        "started": datetime.now().isoformat(timespec="seconds"),
    }
    new = not (DATA / "activity_checks.csv").exists()
    with open(DATA / "activity_checks.csv", "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row)
        if new:
            w.writeheader()
        w.writerow(row)
    print("RESULT", row)
    print("profiling columns:", list(prof.columns))


if __name__ == "__main__":
    main()
