"""Slide 1.4: timeline of neuromorphic computing, one marker per row of the table in
02_workshop_design/05_slide_content_part1.md, slide 1.4 (source: 01_knowledge_base/05_history.md, section 1).

Markers are evenly spaced (ordinal), the year under each marker gives the date. SpiNNaker milestones in HPI red,
all other events grey. 16:9.
Run: uv run --with matplotlib b1_make_timeline.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, GREY, RULE, RED = "#212427", "#5a6065", "#d6d7d8", "#b1063a"
plt.rcParams.update({"font.sans-serif": ["Verdana", "DejaVu Sans"], "font.family": "sans-serif", "text.color": INK})

events = [  # (year label, short label, SpiNNaker milestone)
    ("1990", "Mead names\nthe field", False),
    ("2006", "SpiNNaker\nstarts", True),
    ("2013–23", "Human Brain\nProject", False),
    ("2014", "IBM\nTrueNorth", False),
    ("2018", "Intel Loihi;\nSpiNNaker\n1M cores", True),
    ("2021", "SpiNNaker2\nchip", True),
    ("2024–25", "Hala Point;\nSpiNNaker2\n35,000 chips", True),
    ("2026", "Loihi\nsoftware\narchived;\nSparxity", True),
]

fig, ax = plt.subplots(figsize=(7.2, 4.05))
n = len(events)
ax.annotate("", xy=(n - 0.35, 0), xytext=(-0.6, 0), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.5))
for i, (year, label, spin) in enumerate(events):
    c = RED if spin else GREY
    ax.plot(i, 0, "o", ms=13, color=c, zorder=3)
    up = i % 2 == 0
    stem = 0.9
    ax.plot([i, i], [0, stem if up else -stem], color=c, lw=1.2, zorder=2)
    ax.text(i, -0.22 if up else 0.22, year, ha="center", va="top" if up else "bottom", fontsize=13, color=GREY)
    ax.text(i, stem + 0.08 if up else -stem - 0.08, label, ha="center", va="bottom" if up else "top",
            fontsize=14, color=RED if spin else INK, linespacing=1.15)
ax.set_xlim(-0.8, n - 0.2)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_ylim(-2.05, 2.05)
ax.axis("off")
fig.savefig(Path(__file__).resolve().parent / "b1_timeline.png", dpi=200, facecolor="white")
