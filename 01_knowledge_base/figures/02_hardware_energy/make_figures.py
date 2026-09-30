"""Figures for 02_hardware_energy.md. Run: uv run --with numpy --with matplotlib make_figures.py

All numbers are reported values from Scholze et al. 2026, "The SpiNNaker2 chip: a many-core platform for flexible and
scalable brain-inspired computing", arXiv:2607.24396, extracted from the paper text (to be verified against its tables).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY, RED = "#1f77b4", "#ff7f0e", "#2ca02c", "0.5", "#d62728"
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10})

# Chip-level power per operating state (mW): (PE power, total power); coremark only reports PE power
POWER_STATES = {"PEs off": (59.7, 75.2), "PEs sleep, 0.5 V": (214.7, 235.4), "PEs sleep, 0.8 V": (544.0, 564.7),
                "all PEs busy (CoreMark),\n0.5 V, 150 MHz": (403.9, None),
                "all PEs busy (CoreMark),\n0.8 V, 300 MHz": (1227.2, None)}
# DNN inference efficiency (TOPS, W) for matrix-matrix multiplication; other devices as quoted in the paper
TOPS_W = {"SpiNNaker2\n150 MHz": (2.281, 0.825), "SpiNNaker2\n300 MHz": (4.563, 2.219),
          "Coral EdgeTPU": (4.0, 2.0), "Jetson Orin Nano": (67.0, 25.0)}
# DVS gesture SNN, 1000 time steps (1 s), energy per inference (J) per performance level
DVS_ENERGY = {"low PL\n(0.5 V, 150 MHz)": 2.010, "high PL\n(0.8 V, 300 MHz)": 1.023, "automatic PL\n(switches by load)": 0.741}
# EGRU language model, energy per inference (J)
EGRU = {"SpiNNaker2": 0.065, "Nvidia A100": 1.19}


def box(ax, x, y, w, h, text, color, fs=8):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=color, ec="k", lw=0.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def fig_chip():
    """Schematic of the chip: 38 quad processing elements (QPEs) with 4 PEs each, plus shared components."""
    fig, ax = plt.subplots(figsize=(10, 5.2))
    cols, rows = 8, 5  # 40 slots, 38 used: schematic arrangement, not the physical floorplan
    k = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) in [(2, 3), (2, 4)]:
                continue  # centre: event router / NoC
            x, y = 1 + c * 1.0, 0.6 + r * 0.9
            ax.add_patch(plt.Rectangle((x, y), 0.9, 0.8, fc="#cfe2f3", ec="k", lw=0.6))
            for q in range(4):
                ax.add_patch(plt.Rectangle((x + 0.07 + (q % 2) * 0.42, y + 0.07 + (q // 2) * 0.36), 0.34, 0.3,
                                           fc="white", ec=BLUE, lw=0.5))
            k += 1
    assert k == 38
    box(ax, 4.0, 2.4, 1.9, 0.8, "event router\n+ network-on-chip", "#fde0c5", fs=7.5)
    box(ax, 9.4, 3.2, 1.9, 1.3, "2 × LPDDR4\nDRAM interface", "#f4cccc")
    box(ax, 9.4, 1.6, 1.9, 1.3, "6 chip-to-chip\nlinks", "#d9ead3")
    box(ax, 9.4, 0.6, 1.9, 0.8, "Ethernet\nto host", "#e8e8e8")
    ax.text(5.0, 5.35, "38 quad processing elements (QPEs) × 4 PEs = 152 PEs", ha="center", fontsize=10)
    # zoom on one PE
    ax.annotate("", (-0.1, 4.4), (1.1, 4.45), arrowprops={"arrowstyle": "-|>", "color": BLUE})
    ax.text(-3.4, 5.0, "one processing element (PE)", fontsize=9, fontweight="bold")
    for i, (t, c) in enumerate([("ARM Cortex-M4F core\n150 / 300 MHz", "white"),
                                ("128 KB SRAM\n(≈ 32 KB code, ≈ 96 KB data)", "white"),
                                ("ML accelerator\n16 × 4 MAC array, 8/16 bit", "white"),
                                ("exp / log accelerator,\nrandom number generator", "white")]):
        box(ax, -3.4, 3.9 - i * 0.95, 3.1, 0.8, t, c, fs=7.5)
    ax.set_xlim(-3.6, 11.5)
    ax.set_ylim(-0.1, 5.6)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / "01_chip_schematic.png")
    plt.close(fig)


def fig_power_states():
    names = list(POWER_STATES)
    pe = np.array([v[0] for v in POWER_STATES.values()])
    y = np.arange(len(names))[::-1]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.barh(y, pe, color=[GREY, BLUE, BLUE, ORANGE, ORANGE], height=0.6)
    for yy, (p, tot) in zip(y, POWER_STATES.values()):
        label = f"{p:.0f} mW" + (f"  (whole chip: {tot:.0f} mW)" if tot else "")
        ax.text(p + 15, yy, label, va="center", fontsize=8)
    ax.set_yticks(y, names, fontsize=8)
    ax.set_xlim(0, 1700)
    ax.set_xlabel("power of all PEs (mW)")
    ax.set_title("Measured power of one SpiNNaker2 chip per operating state", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "02_power_states.png")
    plt.close(fig)


def fig_reported_energy():
    fig, (ax_t, ax_d, ax_e) = plt.subplots(1, 3, figsize=(12, 3.8), gridspec_kw={"width_ratios": [1.2, 1.1, 0.8]})
    names = list(TOPS_W)
    eff = np.array([t / w for t, w in TOPS_W.values()])
    ax_t.bar(range(len(names)), eff, color=[BLUE, BLUE, GREY, GREY])
    for i, e in enumerate(eff):
        ax_t.text(i, e + 0.05, f"{e:.2f}", ha="center", fontsize=8)
    ax_t.set_xticks(range(len(names)), names, fontsize=7.5)
    ax_t.set_ylabel("efficiency (TOPS/W)")
    ax_t.set_ylim(0, 3.3)
    ax_t.set_title("A: DNN inference (dense matrix ops)", loc="left", fontsize=10)
    ax_d.bar(range(len(DVS_ENERGY)), list(DVS_ENERGY.values()), color=[GREY, ORANGE, GREEN])
    for i, e in enumerate(DVS_ENERGY.values()):
        ax_d.text(i, e + 0.03, f"{e:.2f} J", ha="center", fontsize=8)
    ax_d.set_xticks(range(len(DVS_ENERGY)), list(DVS_ENERGY), fontsize=7.5)
    ax_d.set_ylabel("energy per inference (J)")
    ax_d.set_ylim(0, 2.4)
    ax_d.set_title("B: SNN, DVS gesture, 1 s of input", loc="left", fontsize=10)
    ax_e.bar(range(2), list(EGRU.values()), color=[BLUE, GREY])
    for i, e in enumerate(EGRU.values()):
        ax_e.text(i, e * 1.25, f"{e * 1000:.0f} mJ" if e < 1 else f"{e:.2f} J", ha="center", fontsize=8)
    ax_e.set_yscale("log")
    ax_e.set_ylim(0.02, 5)
    ax_e.set_xticks(range(2), list(EGRU), fontsize=7.5)
    ax_e.set_ylabel("energy per inference (J, log scale)")
    ax_e.set_title("C: event-based language\nmodel (EGRU): factor 18", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "03_reported_energy.png")
    plt.close(fig)


def check():
    assert abs(EGRU["Nvidia A100"] / EGRU["SpiNNaker2"] - 18.3) < 0.1  # the "18x" figure
    assert abs((1 - DVS_ENERGY["automatic PL\n(switches by load)"] / DVS_ENERGY["high PL\n(0.8 V, 300 MHz)"]) - 0.28) < 0.01
    assert abs(TOPS_W["SpiNNaker2\n150 MHz"][0] / TOPS_W["SpiNNaker2\n150 MHz"][1] - 2.77) < 0.01


if __name__ == "__main__":
    check()
    fig_chip()
    fig_power_states()
    fig_reported_energy()
