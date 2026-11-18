"""Slide 1.2: agenda of the afternoon, drawn plainly (times, block numbers, block names, break at 15:30).

Content from 02_workshop_design/03_outline.md, section "Schedule". Grey and ink, block 1 (the current block) in HPI red.
Run: uv run --with matplotlib b1_make_agenda.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, GREY, RULE, RED = "#212427", "#5a6065", "#d6d7d8", "#b1063a"
plt.rcParams.update({"font.sans-serif": ["Verdana", "DejaVu Sans"], "font.family": "sans-serif", "text.color": INK})

first = [("14:00", "1", "Welcome and motivation"), ("14:15", "2", "Setup check"),
         ("14:20", "3", "Spiking neural networks"), ("14:40", "4", "Hands-on 1: one neuron, input spikes"),
         ("14:55", "5", "SpiNNaker2 hardware"), ("15:10", "6", "Hands-on 2: synfire chain, chip run")]
second = [("15:45", "7", "From PyTorch to the chip"), ("15:55", "8", "Hands-on 3: NIR"),
          ("16:35", "9", "Instructor demos"), ("16:45", "10", "Applications, an honest take, Q&A")]

fig, ax = plt.subplots(figsize=(7.2, 4.6))
row, fs = 1.0, 15
y = 0.0


def heading(text, y):
    ax.text(0, y, text, fontsize=fs - 2, color=GREY, va="center")
    ax.plot([0, 10], [y - 0.45, y - 0.45], color=RULE, lw=1)


def rows(items, y):
    for t, n, name in items:
        c = RED if n == "1" else INK
        ax.text(0, y, t, fontsize=fs, color=GREY, va="center")
        ax.text(1.75, y, n, fontsize=fs, color=c, va="center", ha="right", fontweight="bold" if n == "1" else None)
        ax.text(2.1, y, name, fontsize=fs, color=c, va="center", fontweight="bold" if n == "1" else None)
        y -= row
    return y


heading("First half", y)
y = rows(first, y - row)
ax.text(0, y, "15:30", fontsize=fs, color=GREY, va="center")
ax.text(2.1, y, "Break", fontsize=fs, color=GREY, va="center", style="italic")
ax.plot([0, 10], [y - 0.5, y - 0.5], color=RULE, lw=1)
y -= row
heading("Second half", y)
y = rows(second, y - row)
ax.text(0, y, "17:00", fontsize=fs, color=GREY, va="center")
ax.text(2.1, y, "End", fontsize=fs, color=GREY, va="center")
ax.set_xlim(0, 10)
ax.set_ylim(y - 0.5, 0.5)
ax.axis("off")
fig.savefig(Path(__file__).resolve().parent / "b1_agenda.png", dpi=200, bbox_inches="tight", facecolor="white")
