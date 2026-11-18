"""Slide figure for slide 7.4: the answer of a spiking classifier is the output neuron that fires most often.

Trains the network of notebook 04 exactly as the notebook does (its code cells up to the training cell are executed,
without the animation), then runs one test example (a bar moving right) and draws the four output neurons' spikes over the
30 time steps, with the spike count of each. The counts are what the loss sees: cross-entropy of the counts, as
with the logits of a classifier. Measured in snnTorch (the converted network gives the same answer, notebook 04,
section 5).
Run in the conda env spinnaker2-085, from this folder: python b7_make_spike_counts.py
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ACCENT, GREY, DARK = "#B1063A", "#83888C", "#212427"  # accent: HPI red (slide style); change here for the block colour
NOTEBOOK = Path(__file__).resolve().parents[2] / "04_workshop_material" / "04_direction_trained.ipynb"

# --- train the network as notebook 04 does (its code cells up to and including the training cell) ---
cells = ["".join(c["source"]) for c in json.load(open(NOTEBOOK))["cells"] if c["cell_type"] == "code"]
last = next(k for k, code in enumerate(cells) if "optimizer = torch.optim.Adam" in code)
g = {}
for code in cells[:last + 1]:
    code = "\n".join(line for line in code.split("\n") if not line.startswith("animate("))  # keeps the rng sequence
    exec(compile(code, "notebook04", "exec"), g)
plt.close("all")
torch, utils, net, x_test, y_test, speed_test, DIRECTIONS = (g[k] for k in ["torch", "utils", "net", "x_test", "y_test", "speed_test", "DIRECTIONS"])

# --- one test example: the first bar moving right that is answered correctly with a clear margin ---
with torch.no_grad():
    counts = g["spike_counts"](x_test)
for i in range(x_test.shape[1]):
    c = counts[i].int().tolist()
    if y_test[i] == 0 and c[0] == max(c) and sorted(c)[-1] - sorted(c)[-2] >= 3 and sum(c) - c[0] > 0:
        break
utils.reset(net)
with torch.no_grad():
    out = torch.stack([net(x_t)[0] for x_t in x_test[:, i:i + 1]])[:, 0]  # (time steps, 4 outputs)
spikes = {n: torch.nonzero(out[:, n]).flatten().tolist() for n in range(4)}
c = [len(spikes[n]) for n in range(4)]
assert c == counts[i].int().tolist() and c.index(max(c)) == 0, (c, counts[i])

plt.rcParams.update({"font.size": 18, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(13, 5.5))
for n in range(4):
    color = ACCENT if n == 0 else DARK
    ax.plot(spikes[n], [n] * len(spikes[n]), "|", color=color, ms=26, mew=3)
    ax.text(g["STEPS"] + 0.8, n, f"{c[n]} spike{'' if c[n] == 1 else 's'}", va="center", color=color, fontsize=18)
ax.set(xlim=(-0.5, g["STEPS"] - 0.5), ylim=(3.6, -0.6), yticks=range(4), yticklabels=[f"output: {d}" for d in DIRECTIONS],
       xlabel="time step (1 step = 1 ms)")
ax.text(g["STEPS"] + 0.8, -0.55, "counts = logits", va="bottom", color=GREY, fontsize=15)
ax.text(g["STEPS"] + 0.8, 3.95, f"answer: {DIRECTIONS[0]}", va="top", color=ACCENT, fontsize=18)
fig.text(0.99, 0.01, f"notebook 04, one test example (bar moving right, 1 pixel every {speed_test[i]} step{'' if speed_test[i] == 1 else 's'}), snnTorch after training",
         ha="right", va="bottom", fontsize=11, color=GREY)
plt.tight_layout(rect=(0, 0.03, 0.84, 1))
out_path = Path(__file__).with_name("b7_spike_counts.png")
fig.savefig(out_path, dpi=200)
print("saved", out_path, "| test example", i, "| counts", c)
