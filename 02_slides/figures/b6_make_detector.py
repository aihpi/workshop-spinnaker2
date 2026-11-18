"""Slide figure for slides 6.1 and 7.1: the direction detector of notebook 02 as a schematic.

Four pixels in a row, two lif detectors, every pixel connected to both. The connections of the rightward detector
carry the delays of notebook 02 (3, 2, 1, 0 from pixels 0 to 3); those of the leftward detector are left open,
as in the notebook. A dot moving right makes pixels 0 to 3 fire in steps 5 to 8 (moving_dot("right"), start 5);
with the arrival rule of py-spinnaker2 (a spike sent in step t arrives in step t + 1 + delay) all four arrive in
step 9, where the detector fires (checked on Brian2 in notebook 02, section 3: detector spike at step 9).
Run: uv run --with numpy --with matplotlib python b6_make_detector.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

ACCENT, GREY, DARK = "#B1063A", "#83888C", "#212427"  # accent: HPI red (slide style); change here for the block colour
fire_steps = [5, 6, 7, 8]  # dot moving right: pixel 0 fires first
delays = [3, 2, 1, 0]  # rightward detector, from pixels 0 to 3 (notebook 02, section 2)
arrivals = [t + 1 + d for t, d in zip(fire_steps, delays)]
assert arrivals == [9, 9, 9, 9], arrivals  # all four spikes arrive together
assert 4 * 3 > 10  # weight 3 each, threshold 10: four coinciding spikes fire the detector, three do not (9 < 10)

plt.rcParams.update({"font.size": 18})
fig, ax = plt.subplots(figsize=(13, 6.5))
ax.set(xlim=(-1.2, 9.2), ylim=(-1.9, 5.0), aspect="equal")
ax.axis("off")

px_x = [1.5, 3.5, 5.5, 7.5]
det = {"rightward": (2.5, 3.6), "leftward": (6.5, 3.6)}
for (name, (x, y)) in det.items():
    for k, px in enumerate(px_x):
        right = name == "rightward"
        ax.plot([px, x], [0.45, y - 0.45], color=ACCENT if right else GREY, lw=2.5 if right else 1.5, zorder=1)
        frac = 0.24  # label near the pixel, where the two lines from one pixel are still apart
        lx, ly = px + frac * (x - px), 0.45 + frac * (y - 0.9)
        label = f"{delays[k]}" if right else "?"
        ax.text(lx, ly, label, ha="center", va="center", fontsize=16, color=ACCENT if right else GREY,
                bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec="none"), zorder=3)
    ax.add_patch(Circle((x, y), 0.45, fc="white", ec=DARK, lw=2, zorder=2))
    ax.text(x, y + 0.75, f"{name} detector", ha="center", va="bottom", color=DARK)

for k, px in enumerate(px_x):
    ax.add_patch(Rectangle((px - 0.45, -0.45), 0.9, 0.9, fc="0.9", ec=DARK, lw=1.5, zorder=2))
    ax.text(px, 0, str(k), ha="center", va="center", color=DARK, zorder=3)
    ax.text(px, -0.75, f"fires in step {fire_steps[k]}", ha="center", va="top", fontsize=14, color=GREY)
ax.text(-1.1, 0, "pixel", ha="left", va="center", color=DARK)
ax.annotate("", xy=(8.4, -1.65), xytext=(0.6, -1.65), arrowprops=dict(arrowstyle="->", color=DARK, lw=1.5))
ax.text(4.5, -1.6, "dot moving right", ha="center", va="bottom", fontsize=14, color=DARK)
ax.text(-1.1, 1.15, "delay (steps)", ha="left", va="center", fontsize=14, color=ACCENT)
ax.text(9.15, 1.15, "? = to fill in\n(notebook 02)", ha="right", va="center", fontsize=13, color=GREY)
ax.text(9.15, 3.6, f"all four spikes\narrive in step {arrivals[0]}:\nthe rightward\ndetector fires", ha="right", va="center",
        fontsize=13, color=DARK)
fig.text(0.99, 0.01, "schematic; notebook 02: weight 3 per connection, threshold 10, a spike sent in step t arrives in step t + 1 + delay",
         ha="right", va="bottom", fontsize=11, color=GREY)
plt.tight_layout()
out = Path(__file__).with_name("b6_detector.png")
fig.savefig(out, dpi=200)
print("saved", out, "| arrivals", arrivals)
