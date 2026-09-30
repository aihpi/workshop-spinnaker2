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


CORE, MEM, NET = "#cfe2f3", "#fde0c5", "#d9ead3"  # same colours as in 00_computing_fundamentals


def box(ax, x, y, w, h, text, color, fs=8, ec="k"):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=color, ec=ec, lw=0.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def pe_icon(ax, x, y, w, h, highlight=None):
    """One PE: core (blue) on top of its local memory (orange)."""
    ax.add_patch(plt.Rectangle((x, y + h * 0.45), w, h * 0.55, fc=CORE, ec=highlight or "none", lw=1.5 if highlight else 0))
    ax.add_patch(plt.Rectangle((x, y), w, h * 0.42, fc=MEM, ec="none"))


def fig_installation():
    """Physical hierarchy of the HPI installation: rack -> frame -> board -> chip, and the Ethernet path of a run."""
    from matplotlib.patches import ConnectionPatch
    ETH = "#9467bd"  # Ethernet path from the host to the chip (purple, distinct from the on-chip network in green)
    FRAME, BOARD = "0.9", "0.96"
    DRAM = "#f4cccc"  # off-chip DRAM and its interface, as in Figure 2 (on-chip SRAM stays orange)
    fig = plt.figure(figsize=(15, 6.6))
    gs = fig.add_gridspec(1, 4, width_ratios=[0.9, 1.25, 1.35, 1.0], wspace=0.25)
    ax_r, ax_f, ax_b, ax_c = (fig.add_subplot(gs[k]) for k in range(4))
    # A: rack with the cluster node and the SpiNNaker2 frame
    ax_r.add_patch(plt.Rectangle((0, 0), 2.4, 7.4, fc="0.8", ec="k", lw=1.2))
    for k in range(12):
        ax_r.add_patch(plt.Rectangle((0.2, 0.25 + k * 0.58), 2.0, 0.48, fc="0.97", ec="0.6", lw=0.6))
    frame_y = 0.25 + 3 * 0.58
    ax_r.add_patch(plt.Rectangle((0.2, frame_y), 2.0, 4 * 0.58 - 0.1, fc=FRAME, ec="k", lw=1.5))
    ax_r.text(1.2, frame_y + 1.1, "SpiNNaker2\nframe", ha="center", va="center", fontsize=8)
    host_y = 0.25 + 9 * 0.58
    ax_r.add_patch(plt.Rectangle((0.2, host_y), 2.0, 0.48, fc="white", ec=ETH, lw=1.5))
    ax_r.text(1.2, host_y + 0.24, "cluster node*", ha="center", va="center", fontsize=7)
    ax_r.annotate("", (2.25, frame_y + 2.0), (2.25, host_y + 0.1), arrowprops={"arrowstyle": "-|>", "color": ETH, "lw": 2,
                                                                         "connectionstyle": "arc3,rad=-0.5"})
    ax_r.text(2.75, host_y - 0.6, "Ethernet", fontsize=7.5, color=ETH, rotation=90, va="center")
    ax_r.text(1.2, -0.45, "other slots: other equipment\n* runs py-spinnaker2, may sit\nin a different rack", ha="center",
              va="top", fontsize=7, color="0.35")
    ax_r.set_xlim(-0.3, 3.1)
    ax_r.set_ylim(-1.4, 7.8)
    # B: frame, front view: 6 boards, each with its own Ethernet connection, and a management controller
    ax_f.add_patch(plt.Rectangle((0, 0), 4.6, 5.6, fc=FRAME, ec="k", lw=1.5))
    xs = [0.25 + k * 0.72 for k in range(6)]
    ax_f.plot([-0.2, xs[-1] + 0.29], [5.2, 5.2], color=ETH, lw=1.2)
    for k, x in enumerate(xs):
        ax_f.add_patch(plt.Rectangle((x, 0.95), 0.58, 3.8, fc=BOARD, ec="k", lw=0.8))
        ax_f.text(x + 0.29, 0.7, str(k + 1), ha="center", va="center", fontsize=7.5)
        active = k == 5
        ax_f.annotate("", (x + 0.29, 4.75), (x + 0.29, 5.2),
                      arrowprops={"arrowstyle": "-|>", "color": ETH, "lw": 2.2 if active else 0.8, "shrinkA": 0, "shrinkB": 0})
    ax_f.add_patch(plt.Rectangle((xs[-1], 0.95), 0.58, 3.8, fill=False, ec=RED, lw=2))
    ax_f.text(2.3, 5.38, "Ethernet: every board has its own address", ha="center", fontsize=6.5, color=ETH)
    box(ax_f, 0.25, 0.1, 4.1, 0.38, "management controller (STM32)", "white", fs=6.5)
    ax_f.text(2.3, -0.3, "front view: 6 boards (numbered) side by side.\nA run reserves one board (red).", ha="center",
              va="top", fontsize=8, color="0.25")
    ax_f.set_xlim(-0.3, 4.9)
    ax_f.set_ylim(-1.4, 6.2)
    # C: board, top view: 48 chips, each with its DRAM, connected to its neighbours by links
    ax_b.add_patch(plt.Rectangle((0, 0), 5.0, 5.6, fc=BOARD, ec="k", lw=1.2))
    pos = {}
    for r in range(8):
        for c in range(6):
            pos[(r, c)] = (0.35 + c * 0.75, 0.3 + r * 0.6)
    for (r, c), (x, y) in pos.items():  # links to the neighbours (grid + one diagonal = hexagonal pattern)
        for dr, dc in [(0, 1), (1, 0), (-1, 1)]:
            if (r + dr, c + dc) in pos:
                x2, y2 = pos[(r + dr, c + dc)]
                ax_b.plot([x + 0.21, x2 + 0.21], [y + 0.18, y2 + 0.18], color=GREEN, lw=0.8, zorder=1)
    for (r, c), (x, y) in pos.items():
        ax_b.add_patch(plt.Rectangle((x, y), 0.42, 0.36, fc="0.45", ec="k", lw=0.5, zorder=2))
        ax_b.add_patch(plt.Rectangle((x + 0.45, y + 0.04), 0.1, 0.28, fc=DRAM, ec="#cc6666", lw=0.4, zorder=2))
    chip_xy = pos[(5, 2)]
    ax_b.add_patch(plt.Rectangle(chip_xy, 0.42, 0.36, fill=False, ec=RED, lw=2, zorder=3))
    box(ax_b, 0.35, 5.1, 1.6, 0.35, "Ethernet port", "white", fs=6.5, ec=ETH)
    box(ax_b, 2.9, 5.05, 1.8, 0.45, "board-to-board links\n(not used yet)", "white", fs=6)
    path = [pos[(7, 0)], pos[(6, 1)], pos[(5, 2)]]  # host packets enter at a chip and travel over the links
    ax_b.plot([1.15, path[0][0] + 0.21], [5.1, path[0][1] + 0.36], color=ETH, lw=2.2, zorder=4)
    ax_b.plot([p[0] + 0.21 for p in path], [p[1] + 0.18 for p in path], color=ETH, lw=2.2, zorder=4)
    ax_b.text(2.5, -0.3, "top view: 48 chips (probably, 48-node board, layout\nschematic), each with its DRAM (red, outside the\n"
              "chip), linked to its neighbours (green)", ha="center", va="top", fontsize=7.5, color="0.25")
    ax_b.set_xlim(-0.3, 5.3)
    ax_b.set_ylim(-1.4, 6.2)
    # D: one chip
    ax_c.add_patch(plt.Rectangle((0, 0), 4.0, 4.0, fc="0.97", ec="k", lw=1.2))
    for k in range(40):
        r, c = divmod(k, 8)
        if (r, c) in [(2, 3), (2, 4)]:
            continue
        x, y = 0.2 + c * 0.46, 0.35 + r * 0.66
        ax_c.add_patch(plt.Rectangle((x, y + 0.3), 0.4, 0.26, fc=CORE, ec="none"))
        ax_c.add_patch(plt.Rectangle((x, y + 0.04), 0.4, 0.22, fc=MEM, ec="none"))
    rtr = (0.2 + 3 * 0.46, 0.35 + 2 * 0.66)
    ax_c.add_patch(plt.Rectangle(rtr, 0.86, 0.56, fc=NET, ec=GREEN, lw=1))
    ax_c.annotate("", (rtr[0] + 0.43, rtr[1] + 0.56), (rtr[0] + 0.43, 4.35),
                  arrowprops={"arrowstyle": "-|>", "color": ETH, "lw": 2.2})
    ax_c.text(rtr[0] + 0.55, 4.45, "data from the host", fontsize=7, color=ETH)
    ax_c.add_patch(plt.Rectangle((4.0, 1.6), 0.18, 0.8, fc=DRAM, ec="#cc6666", lw=0.8))  # DRAM interface at the edge
    ax_c.plot([4.18, 4.4], [2.0, 2.0], color="#cc6666", lw=1.2)
    ax_c.text(4.45, 2.0, "DRAM\ninterface\n→ DRAM\nnext to\nthe chip", fontsize=6.5, color="#aa4444", va="center")
    ax_c.text(2.0, -0.3, "152 PEs (38 QPEs × 4), each a core with\nits own SRAM (orange), ≈ 1 cm × 1 cm:\nsee Figure 2",
              ha="center", va="top", fontsize=8, color="0.25")
    ax_c.set_xlim(-0.3, 5.3)
    ax_c.set_ylim(-1.4, 6.2)
    for ax in (ax_r, ax_f, ax_b, ax_c):
        ax.set_aspect("equal")
        ax.axis("off")
    zooms = [(ax_r, ax_f, (2.2, frame_y + 4 * 0.58 - 0.1), (2.2, frame_y), (0, 5.6), (0, 0)),
             (ax_f, ax_b, (xs[-1] + 0.58, 4.75), (xs[-1] + 0.58, 0.95), (0, 5.6), (0, 0)),
             (ax_b, ax_c, (chip_xy[0] + 0.42, chip_xy[1] + 0.36), (chip_xy[0] + 0.42, chip_xy[1]), (0, 4.0), (0, 0))]
    for a, b, pa1, pa2, pb1, pb2 in zooms:
        for pa, pb in [(pa1, pb1), (pa2, pb2)]:
            fig.add_artist(ConnectionPatch(pa, pb, "data", "data", axesA=a, axesB=b, color="0.6", lw=0.7))
    for ax, t in [(ax_r, "A: server rack in\nthe computing centre"), (ax_f, "B: one frame"), (ax_b, "C: one board"),
                  (ax_c, "D: one chip")]:  # titles at the same height
        fig.text(ax.get_position().x0, 0.95, t, fontsize=10, va="top")
    fig.text(0.5, 0.055, "One run = one board: 48 chips × 152 PEs = 7,296 PEs (7,104 for applications)",
             ha="center", fontsize=11, fontweight="bold")
    fig.text(0.5, 0.015, "whole HPI installation: 6 boards ≈ 43,800 PEs, if all are 48-node boards. "
             "Purple: the path of data from py-spinnaker2 to a chip.", ha="center", fontsize=9, color="0.3")
    fig.savefig(OUT / "01_installation_hierarchy.png", bbox_inches="tight")
    plt.close(fig)


def fig_chip():
    """Three-level zoom (chip -> QPE -> PE) and the path of one spike through the router."""
    from matplotlib.patches import ConnectionPatch, FancyArrowPatch
    fig = plt.figure(figsize=(14, 5.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[2.3, 1, 1.25], wspace=0.15)
    ax_c, ax_q, ax_p = (fig.add_subplot(gs[k]) for k in range(3))
    # A: chip
    ax_c.add_patch(plt.Rectangle((0, 0), 10, 6.2, fc="0.97", ec="k", lw=1.2))
    cols, rows = 8, 5
    qpe_pos = [(c, r) for r in range(rows) for c in range(cols) if (c, r) not in [(3, 2), (4, 2)]]
    assert len(qpe_pos) == 38
    origin = {}
    for c, r in qpe_pos:
        x0, y0 = 0.5 + c * 1.1, 0.4 + r * 1.1
        ax_c.add_patch(plt.Rectangle((x0, y0), 1.0, 1.0, fc="white", ec="0.6", lw=0.6))
        for q in range(4):
            pe_icon(ax_c, x0 + 0.07 + (q % 2) * 0.46, y0 + 0.07 + (q // 2) * 0.46, 0.4, 0.4)
        origin[(c, r)] = (x0, y0)
    rx, ry = 0.5 + 3 * 1.1, 0.4 + 2 * 1.1
    ax_c.add_patch(plt.Rectangle((rx, ry), 2.1, 1.0, fc=NET, ec=GREEN, lw=1.2))
    ax_c.text(rx + 1.05, ry + 0.5, "router\n② looks up the key", ha="center", va="center", fontsize=7.5)
    for x, y, w, h, t in [(-0.55, 2.5, 0.5, 1.2, "links"), (10.05, 2.5, 0.5, 1.2, "links"),
                          (6.0, 6.25, 3.9, 0.4, "2 × LPDDR4 DRAM interface"), (0.1, -0.5, 2.4, 0.4, "Ethernet to host")]:
        box(ax_c, x, y, w, h, t, NET if t == "links" else ("#f4cccc" if "DRAM" in t else "#e8e8e8"), fs=6 if t == "links" else 7)
    # spike path: source PE -> router -> copies to target PEs and to a link
    src = origin[(1, 4)]
    pe_icon(ax_c, src[0] + 0.07, src[1] + 0.53, 0.4, 0.4, highlight=RED)
    arrow = {"arrowstyle": "-|>", "mutation_scale": 11, "lw": 1.6}
    ax_c.add_patch(FancyArrowPatch((src[0] + 0.5, src[1] + 0.2), (rx + 0.3, ry + 1.0), color=RED,
                                   connectionstyle="arc3,rad=0.2", **arrow))
    for c, r in [(6, 4), (7, 0), (1, 0)]:
        t = origin[(c, r)]
        pe_icon(ax_c, t[0] + 0.53, t[1] + 0.07, 0.4, 0.4, highlight=RED)
        ax_c.add_patch(FancyArrowPatch((rx + 1.05, ry + (1.0 if r > 2 else 0)), (t[0] + 0.7, t[1] + (0.1 if r > 2 else 0.5)),
                                       color=RED, connectionstyle="arc3,rad=-0.15", **arrow))
    ax_c.add_patch(FancyArrowPatch((rx + 2.1, ry + 0.5), (10.05, 3.1), color=RED, **arrow))
    ax_c.text(0.0, 6.45, "① a neuron fires: its PE sends one packet (red)", fontsize=7.5, color=RED, va="center")
    ax_c.text(10.0, -0.3, "③ copies go to every PE and chip with listening neurons", ha="right", fontsize=7.5, color=RED, va="center")
    ax_c.set_title("A: one chip: 38 QPEs × 4 PEs = 152 PEs, and the path of one spike", loc="left", fontsize=10)
    ax_c.set_xlim(-0.7, 10.7)
    ax_c.set_ylim(-0.6, 6.8)
    # B: one QPE
    ax_q.add_patch(plt.Rectangle((0, 0), 4, 4, fc="white", ec="0.3", lw=1.2))
    for q in range(4):
        x, y = 0.3 + (q % 2) * 1.9, 0.3 + (q // 2) * 1.9
        ax_q.add_patch(plt.Rectangle((x, y + 0.75), 1.5, 0.75, fc=CORE, ec="k", lw=0.8))
        ax_q.text(x + 0.75, y + 1.12, f"PE {q}\ncore", ha="center", va="center", fontsize=7)
        ax_q.add_patch(plt.Rectangle((x, y), 1.5, 0.7, fc=MEM, ec="k", lw=0.8))
        ax_q.text(x + 0.75, y + 0.35, "local\nmemory", ha="center", va="center", fontsize=6.5)
    ax_q.text(2, -0.4, "4 PEs share one connection\nto the network-on-chip", ha="center", va="top", fontsize=8, color="0.3")
    ax_q.set_title("B: one QPE", loc="left", fontsize=10)
    ax_q.set_xlim(-0.3, 4.3)
    ax_q.set_ylim(-1.6, 4.4)
    # C: one PE
    parts = [("ARM Cortex-M4F core, 150 / 300 MHz\nruns the neuron model code", CORE),
             ("128 KB SRAM: ≈ 32 KB code, ≈ 96 KB data\n(neuron states, weights, recordings)", MEM),
             ("ML accelerator: 16 × 4 MAC array,\n8/16 bit, for dense matrix operations", "white"),
             ("exp/log accelerator, random number\ngenerator, DMA, timers", "white")]
    for k, (t, c) in enumerate(parts):
        box(ax_p, 0, 3.0 - k * 1.05, 5, 0.9, t, c, fs=7.5)
    ax_p.set_title("C: one PE", loc="left", fontsize=10)
    ax_p.set_xlim(-0.2, 5.2)
    ax_p.set_ylim(-1.6, 4.4)
    for ax in (ax_c, ax_q, ax_p):
        ax.set_aspect("equal")
        ax.axis("off")
    # zoom lines: QPE (0, 4) of the chip -> panel B, PE 2 of the QPE -> panel C
    z = origin[(7, 4)]
    ax_c.add_patch(plt.Rectangle(z, 1.0, 1.0, fill=False, ec="k", lw=1.6))
    for (xa, ya), (xb, yb) in [((z[0] + 1.0, z[1] + 1.0), (0, 4)), ((z[0] + 1.0, z[1]), (0, 0))]:
        fig.add_artist(ConnectionPatch((xa, ya), (xb, yb), "data", "data", axesA=ax_c, axesB=ax_q, color="0.5", lw=0.8))
    ax_q.add_patch(plt.Rectangle((2.2, 2.2), 1.5, 1.5, fill=False, ec="k", lw=1.6))
    for (xa, ya), (xb, yb) in [((3.7, 3.7), (0, 3.9)), ((3.7, 2.2), (0, -0.15))]:
        fig.add_artist(ConnectionPatch((xa, ya), (xb, yb), "data", "data", axesA=ax_q, axesB=ax_p, color="0.5", lw=0.8))
    fig.savefig(OUT / "01_chip_schematic.png", bbox_inches="tight")
    plt.close(fig)


def fig_pe_function():
    """Functional schematic of one PE and the steps of one timestep (colours as in the timestep figure)."""
    from matplotlib.patches import FancyArrowPatch
    fig, ax = plt.subplots(figsize=(12, 7.4))
    DRAM = "#f4cccc"
    ax.add_patch(plt.Rectangle((0, 1.6), 8.8, 6.0, fc="0.97", ec="k", lw=1.5))
    ax.text(0.15, 7.3, "one processing element (PE)", fontsize=10, fontweight="bold", va="center")
    y0 = 1.6  # shift of the PE drawing above the timeline strip
    box(ax, 0.4, 4.55 + y0, 1.6, 0.6, "timer", "white", fs=8.5)
    for x, t in [(2.6, "ML accelerator\n(MAC array)"), (4.25, "exp / log\naccelerator"), (5.9, "random number\ngenerator")]:
        box(ax, x, 4.55 + y0, 1.5, 0.6, t, "white", fs=7)
    box(ax, 2.6, 2.9 + y0, 3.0, 1.2, "ARM Cortex-M4F core\nruns the neuron model", CORE, fs=9)
    ax.add_patch(plt.Rectangle((0.4, 0.3 + y0), 6.8, 2.0, fc=MEM, ec="k", lw=1))
    ax.text(0.5, 2.12 + y0, "128 KB SRAM", fontsize=8.5, fontweight="bold", va="center")
    for x, w, t in [(0.5, 1.35, "code of the\nneuron model"), (1.95, 1.6, "synapse tables:\nweights, targets"),
                    (3.65, 1.6, "neuron states\nand parameters"), (5.35, 1.7, "recordings\n(spikes, v)")]:
        box(ax, x, 0.45 + y0, w, 1.45, t, "white", fs=7)
    box(ax, 7.5, 0.8 + y0, 1.0, 0.7, "DMA", "white", fs=8.5)
    box(ax, 7.6, 2.9 + y0, 0.95, 1.2, "NoC\ninter-\nface", NET, fs=8)
    box(ax, 9.4, 2.85 + y0, 1.7, 1.3, "network-on-chip\nand router\n(other PEs,\nother chips)", NET, fs=7.5)
    box(ax, 9.4, 0.65 + y0, 1.7, 1.0, "DRAM\nnext to the chip", DRAM, fs=7.5)
    arrow = dict(arrowstyle="-|>", mutation_scale=13)
    both = dict(arrowstyle="<|-|>", mutation_scale=12)
    grey = dict(color="0.55", lw=1.2, ls="--")
    ax.add_patch(FancyArrowPatch((8.55, 3.5 + y0), (9.4, 3.5 + y0), color=GREEN, lw=2, **both))
    ax.add_patch(FancyArrowPatch((7.2, 1.15 + y0), (7.5, 1.15 + y0), **grey, **both))
    ax.add_patch(FancyArrowPatch((8.5, 1.15 + y0), (9.4, 1.15 + y0), **grey, **arrow))
    ax.add_patch(FancyArrowPatch((4.1, 4.1 + y0), (4.1, 4.55 + y0), **grey, **both))
    ax.text(4.2, 4.3 + y0, "used by some models", fontsize=6.5, color="0.45", va="center")
    ax.text(8.0, 0.55 + y0, "e.g. record_on_dram", fontsize=6.5, color="0.45", ha="center")
    # the steps, coloured like the timestep figure: incoming spikes orange, neuron update blue
    ax.add_patch(FancyArrowPatch((1.2, 4.55 + y0), (2.6, 3.9 + y0), color="k", lw=2, **arrow))
    ax.text(0.45, 4.2 + y0, "① wake up", fontsize=8.5, fontweight="bold")
    ax.add_patch(FancyArrowPatch((7.6, 3.8 + y0), (5.6, 3.8 + y0), color=ORANGE, lw=2.5, **arrow))
    ax.text(6.6, 3.95 + y0, "② spikes in", fontsize=8.5, fontweight="bold", color="#c65f00", ha="center")
    ax.add_patch(FancyArrowPatch((2.75, 1.9 + y0), (3.1, 2.9 + y0), color=ORANGE, lw=2.5, **arrow))
    ax.text(1.35, 2.5 + y0, "③ read synapses\n(targets, weights)", fontsize=8, fontweight="bold", color="#c65f00")
    ax.add_patch(FancyArrowPatch((4.4, 2.9 + y0), (4.45, 1.9 + y0), color=BLUE, lw=2.5, **both))
    ax.text(4.6, 2.5 + y0, "④ add weights,\nupdate neurons", fontsize=8, fontweight="bold", color=BLUE)
    ax.add_patch(FancyArrowPatch((5.6, 3.2 + y0), (7.6, 3.2 + y0), color=BLUE, lw=2.5, **arrow))
    ax.text(6.6, 2.8 + y0, "⑤ spikes out", fontsize=8.5, fontweight="bold", color=BLUE, ha="center")
    # timeline strip: one timestep
    t_scale = 8.8  # one timestep drawn over the width of the PE
    segs = [(0.0, 0.03, "k", "①"), (0.03, 0.35, ORANGE, "② ③"), (0.35, 0.55, BLUE, "④ ⑤"), (0.55, 1.0, "0.9", "sleep")]
    for a, b, c, t in segs:
        ax.add_patch(plt.Rectangle((a * t_scale, 0.35), (b - a) * t_scale, 0.5, fc=c, ec="none"))
        ax.text((a + b) / 2 * t_scale, 0.6, t if t != "①" else "", ha="center", va="center", fontsize=8.5,
                color="white" if c != "0.9" else "0.3", fontweight="bold")
    ax.text(0.0, 1.05, "① timer", fontsize=7.5)
    for x, lab in [(0, "start of the timestep"), (t_scale, "next timestep")]:
        ax.plot([x, x], [0.25, 0.95], color="k", lw=1)
        ax.text(x, 0.05, lab, fontsize=7.5, ha="center" if x == 0 else "right")
    ax.text(t_scale + 0.3, 0.6, "one timestep, e.g. 1 ms (length\nconfigurable, durations schematic;\nsee Figure 4 for several steps)", fontsize=7.5,
            color="0.35", va="center")
    ax.set_xlim(-0.2, 11.4)
    ax.set_ylim(-0.2, 7.8)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / "02_pe_function.png", bbox_inches="tight")
    plt.close(fig)


def fig_pe_timestep():
    """Illustration: a PE's work per timestep grows with the incoming spikes, and it sleeps for the rest of the step."""
    rng = np.random.default_rng(3)
    steps, period = 10, 1.0  # ms
    spikes = np.array([12, 30, 8, 55, 20, 140, 25, 10, 40, 18])  # incoming spikes per step (made up)
    neuron_update = 0.18  # ms per step for the neuron updates (made up)
    per_spike = 0.0062  # ms per incoming spike (made up)
    fig, (ax_t, ax_s) = plt.subplots(2, 1, figsize=(10, 4.2), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    end = 0.0
    for k in range(steps):
        t0 = k * period
        start = max(t0, end)  # if the previous step overran, this one starts late
        busy_syn = spikes[k] * per_spike
        ax_t.add_patch(plt.Rectangle((start, 0.2), busy_syn, 0.6, fc=ORANGE, ec="none"))
        ax_t.add_patch(plt.Rectangle((start + busy_syn, 0.2), neuron_update, 0.6, fc=BLUE, ec="none"))
        end = start + busy_syn + neuron_update
        if end < t0 + period:
            ax_t.add_patch(plt.Rectangle((end, 0.2), t0 + period - end, 0.6, fc="0.9", ec="none"))
        else:
            ax_t.annotate("deadline missed:\nwork spills into the\nnext timestep", (t0 + period, 0.8), (t0 - 1.2, 1.25),
                          fontsize=7.5, color=RED, arrowprops={"arrowstyle": "->", "color": RED})
        ax_t.axvline(t0, color="k", lw=0.8)
    ax_t.axvline(steps * period, color="k", lw=0.8)
    ax_t.text(0.02, 1.02, "timer interrupt", fontsize=7.5)
    handles = [plt.matplotlib.patches.Patch(color=c, label=l) for l, c in
               [("process incoming spikes", ORANGE), ("update neurons, send spikes", BLUE), ("sleep", "0.9")]]
    ax_t.legend(handles=handles, frameon=False, fontsize=8, loc="upper right", ncol=3, bbox_to_anchor=(1, 1.35))
    ax_t.set_ylim(0, 1.6)
    ax_t.set_yticks([])
    ax_t.set_ylabel("one PE")
    ax_s.bar(np.arange(steps) * period + 0.5, spikes, width=0.6, color=ORANGE)
    ax_s.set_ylabel("incoming spikes\nper timestep")
    ax_s.set_xlabel("time (ms), assuming a timestep of 1 ms (common choice, configurable)")
    ax_s.set_xlim(0, steps * period)
    fig.suptitle("How a PE spends its timesteps (illustration, durations made up)", x=0.02, ha="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "02_pe_timestep.png")
    plt.close(fig)


def clustered_synapses():
    """Expected number of synapses of the clustered network in primer section 7 (connection table of the example)."""
    ee_in = 10 * 20 * 19 * 0.5
    ee_out = 200 * 180 * 0.05
    return ee_in + ee_out + 50 * 200 * 0.3 + 200 * 50 * 0.4 + 50 * 49 * 0.5


def fig_memory():
    """A: energy of reading MNIST layer 1 from SRAM vs DRAM. B: how many PEs the example networks fill."""
    budget_kb = 92  # 96 KB data memory minus 4 KB heap and stack; routing tables and recordings reduce it further
    n_l1 = 784 * 128
    reads = n_l1 * 4 / 8  # 64-bit reads for all weights at 4 bytes per synapse
    e_sram, e_dram = reads * 10e-6, reads * 1300e-6  # µJ, Horowitz 2014 (pJ per 64-bit read)
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw={"width_ratios": [1, 1.45]})
    # A: why keep the weights local
    for yy, (name, e, c) in enumerate([("DRAM\n(next to the chip)", e_dram, "#f4cccc"), ("SRAM of the PEs\n(on the chip)", e_sram, MEM)]):
        ax_a.barh(yy, e, color=c, ec="k", height=0.55)
        ax_a.text(e * 1.2, yy, f"{e:.1f} µJ", va="center", fontsize=9, fontweight="bold")
    ax_a.set_yticks([0, 1], ["DRAM\n(next to the chip)", "SRAM of the PEs\n(on the chip)"], fontsize=8.5)
    ax_a.set_xscale("log")
    ax_a.set_xlim(0.1, 2000)
    ax_a.set_ylim(-0.6, 1.9)
    ax_a.annotate("", (e_dram, 1.45), (e_sram, 1.45), arrowprops={"arrowstyle": "-|>", "color": RED, "lw": 1.3})
    ax_a.text(np.sqrt(e_sram * e_dram), 1.55, f"× {e_dram / e_sram:.0f} more energy", ha="center", fontsize=8.5, color=RED)
    ax_a.set_xlabel("energy to read all 100,352 weights of MNIST layer 1 once (µJ, log scale)")
    ax_a.set_title("A: why keep the weights in local SRAM", loc="left", fontsize=10)
    # B: the price: networks fill PE memories and have to be split
    nets = [("MNIST layer 1\n784 inputs → 128 hidden", n_l1), ("clustered network\n(primer Figure 21)", clustered_synapses()),
            ("MNIST layer 2\n128 hidden → 10 outputs", 128 * 10)]
    gap = 0.12
    for row, (name, n_syn) in enumerate(nets):
        yy = 2 - row
        kb1, kb4 = n_syn / 1024, 4 * n_syn / 1024
        n_boxes = int(np.ceil(kb4 / budget_kb))
        for b in range(n_boxes):
            x = b * (1 + gap)
            fill = min(1.0, kb4 / budget_kb - b)
            ax_b.add_patch(plt.Rectangle((x, yy - 0.3), 1, 0.6, fc="white", ec="k", lw=1))
            ax_b.add_patch(plt.Rectangle((x, yy - 0.3), fill, 0.6, fc=ORANGE, ec="none"))
        pos1 = kb1 / budget_kb
        x1 = int(pos1) * (1 + gap) + (pos1 - int(pos1))
        ax_b.plot([x1, x1], [yy - 0.38, yy + 0.38], color="k", ls="--", lw=1.2)
        need = f"{n_boxes} PE" + ("s" if n_boxes > 1 else "") + " at 4 bytes"
        need1 = int(np.ceil(pos1))
        ax_b.text(5 * (1 + gap) + 0.1, yy, f"{need},\n{need1} PE{'s' if need1 > 1 else ''} at 1 byte", va="center", fontsize=8)
        ax_b.text(-0.15, yy, name, ha="right", va="center", fontsize=8.5)
    handles = [plt.matplotlib.patches.Patch(fc="white", ec="k", label="data memory of one PE (≈ 92 KB)"),
               plt.matplotlib.patches.Patch(color=ORANGE, label="filled by the synapses at 4 bytes each"),
               plt.Line2D([], [], color="k", ls="--", lw=1.2, label="end of the synapses at 1 byte each")]
    ax_b.legend(handles=handles, frameon=False, fontsize=7.5, loc="lower left", bbox_to_anchor=(0.2, 0.86), ncol=2)
    ax_b.set_xlim(-3.0, 7.3)
    ax_b.set_ylim(-0.6, 3.1)
    ax_b.axis("off")
    ax_b.set_title("B: the price: local memory is small, networks are split across PEs", loc="left", fontsize=10)
    fig.text(0.5, 0.97, "keep the data local (A)  →  but local memory is small  →  split the network across PEs (B)",
             ha="center", fontsize=10, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT / "03_memory.png")
    plt.close(fig)


def fig_multicast():
    """A: one packet, copied by the router, fanned out inside the target PE. B: packets per spike for two examples."""
    fig, (ax_d, ax_p) = plt.subplots(1, 2, figsize=(13.5, 4.6), gridspec_kw={"width_ratios": [1.45, 1]})
    # A: routing table lookup and fan-out inside a target PE
    box(ax_d, 0, 1.6, 1.4, 0.7, "PE 12\nneuron 57 fires", CORE, fs=7.5)
    ax_d.annotate("", (2.2, 1.95), (1.4, 1.95), arrowprops={"arrowstyle": "-|>", "color": RED, "lw": 1.8})
    ax_d.text(1.75, 2.1, "1 packet\nkey 0x2A39", ha="center", va="bottom", fontsize=6.5, color=RED)
    ax_d.add_patch(plt.Rectangle((2.2, 0.4), 3.3, 3.1, fc=NET, ec=GREEN, lw=1.2))
    ax_d.text(3.85, 3.25, "router: routing table", ha="center", fontsize=8.5)
    rows = [("key", "send copies to"), ("0x2A39", "PE 3, PE 17, PE 40, link E"), ("0x2A3A", "PE 5"), ("…", "…")]
    for k, (a, b) in enumerate(rows):
        y = 2.8 - 0.5 * k
        w = "bold" if k == 1 else "normal"
        ax_d.text(2.35, y, a, fontsize=7.5, family="monospace", fontweight=w)
        ax_d.text(3.2, y, b, fontsize=7, fontweight=w, color=RED if k == 1 else "k")
    targets = [("PE 3", 3.0), ("PE 17", 2.25), ("PE 40", 1.5), ("link E →\nneighbour chip", 0.75)]
    for k, (t, y) in enumerate(targets):
        box(ax_d, 6.3, y - 0.28, 1.4, 0.56, t, CORE if k < 3 else NET, fs=7)
        ax_d.annotate("", (6.3, y), (5.5, 2.3), arrowprops={"arrowstyle": "-|>", "color": RED, "lw": 1.2})
    ax_d.text(5.9, 3.55, "3 copies + 1 link", fontsize=7, color=RED, ha="center")
    # zoom into PE 3: synapse table, then the target neurons
    ax_d.add_patch(plt.Rectangle((8.4, 1.4), 2.9, 2.4, fc="0.97", ec="k", lw=1))
    ax_d.text(8.5, 3.6, "inside PE 3", fontsize=7.5, fontweight="bold")
    box(ax_d, 8.55, 2.35, 1.1, 0.8, "synapse\ntable", MEM, fs=7)
    ax_d.annotate("", (8.55, 2.75), (7.7, 3.0), arrowprops={"arrowstyle": "-|>", "color": RED, "lw": 1.2})
    for n in range(7):
        ny = 1.6 + n * 0.3
        ax_d.plot(10.9, ny, "o", color=BLUE, ms=6, mec="k", mew=0.5)
        ax_d.plot([9.65, 10.83], [2.75, ny], color=ORANGE, lw=1)
    ax_d.text(11.2, 3.6, "target neurons", fontsize=6.5, ha="right", color="0.3")
    ax_d.text(9.85, 0.85, "packets for this spike:\n1 sent + 4 copies = 5,\nhowever many target\nneurons the 3 PEs hold",
              ha="center", va="center", fontsize=7.5, color=RED,
              bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": RED, "lw": 1})
    ax_d.plot([7.7, 8.4], [3.28, 3.8], color="0.6", lw=0.7)
    ax_d.plot([7.7, 8.4], [2.72, 1.4], color="0.6", lw=0.7)
    ax_d.text(5.6, 0.0, "1 packet out → the router copies it once per target PE or link → each PE hands it to its own\n"
              "target neurons through its synapse table (Figure 3, step ③)", ha="center", fontsize=7.5, color="0.3", va="top")
    ax_d.set_xlim(-0.2, 11.6)
    ax_d.set_ylim(-0.9, 3.9)
    ax_d.set_aspect("equal")
    ax_d.axis("off")
    ax_d.set_title("A: multicast: one packet, copied only where needed (keys and targets made up)", loc="left", fontsize=10)
    # B: packets per spike for two examples
    examples = [("one input spike of the\nMNIST network: 128 targets\non 5 PEs (Figure 5)", 128, 5),
                ("cortex-like neuron:\n1,000 targets on 10 PEs", 1000, 10)]
    x = np.arange(len(examples))
    for k, (name, n_targets, n_pes) in enumerate(examples):
        ax_p.bar(k - 0.2, n_targets, width=0.36, color=GREY, label="without multicast: one packet per target neuron" if k == 0 else None)
        ax_p.bar(k + 0.2, 1 + n_pes, width=0.36, color=RED, label="with multicast: 1 packet sent + 1 copy per target PE" if k == 0 else None)
        ax_p.text(k - 0.2, n_targets * 1.15, f"{n_targets:,}", ha="center", fontsize=8.5)
        ax_p.text(k + 0.2, (1 + n_pes) * 1.15, f"1 + {n_pes}", ha="center", fontsize=8.5)
        ax_p.text(k, n_targets * 2.6, f"≈ {n_targets / (1 + n_pes):.0f} × fewer", ha="center", fontsize=9, fontweight="bold")
    ax_p.set_xticks(x, [e[0] for e in examples], fontsize=8)
    ax_p.set_yscale("log")
    ax_p.set_ylim(1, 1e4)
    ax_p.set_ylabel("packets for one spike (log scale)")
    ax_p.legend(frameon=False, fontsize=7.5, loc="upper left")
    ax_p.set_title("B: packets needed for one spike", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "04_multicast.png")
    plt.close(fig)


def fig_scale():
    """PEs per system (reported) and an estimate of neuron capacity at ~150,000 neurons per chip."""
    systems = [("single-chip board", 1, 152), ("48-node board\n(one HPI run)", 48, 7_296),
               ("HPI installation\n(6 boards, if 48-node)", 288, 43_776), ("SpiNNcloud system,\nTU Dresden", 35_000, 5e6),
               ("design limit", None, 10e6)]
    fig, (ax_p, ax_n) = plt.subplots(1, 2, figsize=(12, 4.3), gridspec_kw={"width_ratios": [1.1, 1]})
    y = np.arange(len(systems))[::-1]
    colors = [GREY, ORANGE, ORANGE, BLUE, "0.75"]
    for yy, (name, chips, pes), c in zip(y, systems, colors):
        ax_p.barh(yy, pes, color=c, height=0.6)
        ax_p.text(pes * 1.3, yy, f"{pes:,.0f} PEs" + (f" ({chips:,} chip{'s' if chips > 1 else ''})" if chips else ""), va="center", fontsize=8)
    ax_p.set_yticks(y, [s_[0] for s_ in systems], fontsize=8)
    ax_p.set_xscale("log")
    ax_p.set_xlim(50, 3e9)
    ax_p.set_xlabel("processing elements (log scale)")
    ax_p.set_title("A: the same chips, from one board to a supercomputer", loc="left", fontsize=10)
    per_chip = 150_000
    items = [("one chip", per_chip, BLUE), ("48-node board (one HPI run)", 48 * per_chip, ORANGE), ("HPI installation", 288 * per_chip, ORANGE),
             ("SpiNNcloud, Dresden", 35_000 * per_chip, BLUE), ("mouse brain", 7e7, GREY), ("human brain", 8.6e10, GREY)]
    y2 = np.arange(len(items))[::-1]
    for yy, (name, n, c) in zip(y2, items):
        ax_n.barh(yy, n, color=c, height=0.6)
        label = f"{n / 1e9:.1f} billion" if n >= 1e9 else (f"{n / 1e6:.0f} million" if n >= 1e6 else f"{n / 1e3:.0f} thousand")
        ax_n.text(n * 1.3, yy, label, va="center", fontsize=8)
    ax_n.set_yticks(y2, [i[0] for i in items], fontsize=8)
    ax_n.set_xscale("log")
    ax_n.set_xlim(1e4, 5e12)
    ax_n.set_xlabel("neurons (log scale)")
    ax_n.set_title("B: estimated capacity at ~150,000 neurons per chip", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "05_scale.png")
    plt.close(fig)


def fig_power_states():
    """A: power against work per second at the two performance levels, and the cheapest path (automatic switching).
    B: DVS gesture energy per performance level."""
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12.5, 4.8), gridspec_kw={"width_ratios": [1.2, 1]})
    off = POWER_STATES["PEs off"][0]
    lo0, lo1 = POWER_STATES["PEs sleep, 0.5 V"][0], POWER_STATES["all PEs busy (CoreMark),\n0.5 V, 150 MHz"][0]
    hi0, hi1 = POWER_STATES["PEs sleep, 0.8 V"][0], POWER_STATES["all PEs busy (CoreMark),\n0.8 V, 300 MHz"][0]
    # x = work per second relative to the maximum of the high level; the low level reaches at most half of it
    ax_a.plot([0, 0.5], [lo0, lo1], ":", color=BLUE, lw=2)
    ax_a.plot([0, 1], [hi0, hi1], ":", color=RED, lw=2)
    ax_a.plot([0, 0.5], [lo0, lo1], "o", color=BLUE, ms=9)
    ax_a.plot([0, 1], [hi0, hi1], "o", color=RED, ms=9)
    hi_at_half = hi0 + 0.5 * (hi1 - hi0)
    ax_a.plot([0, 0.5], [lo0, lo1], color=GREEN, lw=6, alpha=0.35, solid_capstyle="round", zorder=0)
    ax_a.plot([0.5, 1], [hi_at_half, hi1], color=GREEN, lw=6, alpha=0.35, solid_capstyle="round", zorder=0)
    ax_a.plot([0.5, 0.5], [lo1, hi_at_half], color=GREEN, lw=2, ls="--")
    ax_a.text(0.52, (lo1 + hi_at_half) / 2, "switch: the low level\ncan't do more work", fontsize=7.5, color=GREEN,
              va="center")
    ax_a.text(0.02, lo0 - 70, f"{lo0:.0f}", fontsize=8, color=BLUE)
    ax_a.text(0.02, hi0 + 40, f"{hi0:.0f}", fontsize=8, color=RED)
    ax_a.text(0.5, lo1 - 70, f"{lo1:.0f}", fontsize=8, color=BLUE, ha="center")
    ax_a.text(1.0, hi1 + 50, f"{hi1:.0f}", fontsize=8, color=RED, ha="center")
    ax_a.text(0.12, 300, "low level: 0.5 V, 150 MHz", fontsize=8.5, color=BLUE, fontweight="bold", rotation=12)
    ax_a.text(0.25, 780, "high level: 0.8 V, 300 MHz", fontsize=8.5, color=RED, fontweight="bold", rotation=24)
    ax_a.axhline(off, color="k", ls="--", lw=1)
    ax_a.text(0.75, off + 25, f"all PEs switched off: {off:.0f} mW", ha="center", fontsize=7.5)
    ax_a.text(0.02, 1330, "green: automatic switching, the cheapest way to do a given amount of work\n"
              "points: measured (sleeping and full load), dotted lines: interpolated", fontsize=7, color="0.3", va="top")
    ax_a.set_xticks([0, 0.5, 1], ["0\n(sleeping)", "0.5\n(low level at full load)", "1\n(high level at full load)"],
                    fontsize=8)
    ax_a.set_xlim(-0.05, 1.12)
    ax_a.set_ylim(0, 1400)
    ax_a.set_xlabel("work per second (relative to the maximum of the high level)")
    ax_a.set_ylabel("power of all 152 PEs (mW)")
    ax_a.set_title("A: stay at the low level as long as it can keep up", loc="left", fontsize=10)
    names = list(DVS_ENERGY)
    vals = list(DVS_ENERGY.values())
    ax_b.bar(range(3), vals, color=[GREY, RED, GREEN], width=0.7)
    for i, v in enumerate(vals):
        ax_b.text(i, v + 0.04, f"{v:.2f} J", ha="center", fontsize=8.5)
    ax_b.annotate("−28 % compared\nwith always high", (2, 0.85), (1.4, 1.65), fontsize=8.5, color=GREEN, fontweight="bold",
                  arrowprops={"arrowstyle": "->", "color": GREEN})
    ax_b.text(0, 2.12, "highest energy despite\nlow voltage: reason not\ngiven, to check", ha="center", va="bottom",
              fontsize=7, color="0.35")
    ax_b.set_xticks(range(3), ["always low\n(0.5 V, 150 MHz)", "always high\n(0.8 V, 300 MHz)", "automatic\n(switches by load)"],
                    fontsize=7.5)
    ax_b.set_ylabel("energy per inference (J)")
    ax_b.set_ylim(0, 2.7)
    ax_b.set_title("B: SNN (DVS gesture): adapting the level to the load", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "02_power_states.png")
    plt.close(fig)


def fig_reported_energy():
    eff_s2 = TOPS_W["SpiNNaker2\n150 MHz"][0] / TOPS_W["SpiNNaker2\n150 MHz"][1]
    items = [("dense DNN layers\nvs. Nvidia Jetson Orin Nano", eff_s2 / (67.0 / 25.0), "0.55"),
             ("dense DNN layers\nvs. Google Coral Edge TPU", eff_s2 / (4.0 / 2.0), "0.55"),
             ("event-based language model\nvs. Nvidia A100 GPU", EGRU["Nvidia A100"] / EGRU["SpiNNaker2"], BLUE)]
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    y = np.array([2.3, 1.5, 0])
    ax.axhspan(1.05, 2.75, color="0.93", zorder=0)
    ax.axhspan(-0.45, 0.45, color="#dbe9f6", zorder=0)
    ax.text(19.8, 2.62, "dense workloads", ha="right", va="top", fontsize=9, color="0.35", fontweight="bold")
    ax.text(19.8, 0.38, "sparse, event-based", ha="right", va="top", fontsize=9, color=BLUE, fontweight="bold")
    for yy, (name, r, c) in zip(y, items):
        ax.barh(yy, r, color=c, height=0.5)
        ax.text(r + 0.3, yy, f"{r:.1f} ×" if r < 10 else f"{r:.0f} ×", va="center", fontsize=13, fontweight="bold",
                color=c if c != "0.55" else "0.3")
    ax.axvline(1, color="k", ls="--", lw=1)
    ax.text(1.15, -0.62, "1 × = same energy", fontsize=8, va="top")
    ax.set_yticks(y, [i[0] for i in items], fontsize=9)
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.95, 2.75)
    ax.set_xticks([0, 1, 5, 10, 15, 20], ["0", "1", "5", "10", "15", "20"])
    ax.set_xlabel("how many times less energy SpiNNaker2 needs than the comparison hardware")
    ax.set_title("SpiNNaker2's energy advantage grows with sparsity", loc="left", fontsize=11, fontweight="bold")
    fig.text(0.01, 0.01, "Different workloads, devices and measurement set-ups: the bars show the trend, not an exact comparison.",
             fontsize=7.5, color="0.4")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT / "03_reported_energy.png")
    plt.close(fig)


def check():
    assert abs(EGRU["Nvidia A100"] / EGRU["SpiNNaker2"] - 18.3) < 0.1  # the "18x" figure
    assert abs((1 - DVS_ENERGY["automatic PL\n(switches by load)"] / DVS_ENERGY["high PL\n(0.8 V, 300 MHz)"]) - 0.28) < 0.01
    assert 784 * 128 / 1024 > 92 and round(clustered_synapses()) == 11925  # MNIST layer 1 exceeds one PE at 1 byte
    assert 6 * 48 * 152 == 43776 and 48 * 152 == 7296  # HPI installation and one board, if 48-node boards
    assert abs((1227.2 / 300) / (403.9 / 150) - 1.52) < 0.01  # energy per cycle at full load, high vs low level
    assert abs(TOPS_W["SpiNNaker2\n150 MHz"][0] / TOPS_W["SpiNNaker2\n150 MHz"][1] - 2.77) < 0.01


if __name__ == "__main__":
    check()
    fig_installation()
    fig_chip()
    fig_pe_function()
    fig_pe_timestep()
    fig_memory()
    fig_multicast()
    fig_scale()
    fig_power_states()
    fig_reported_energy()
