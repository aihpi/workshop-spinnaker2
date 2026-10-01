"""Figures for 02_hardware_energy.md. Run: uv run --with numpy --with matplotlib make_figures.py

Reported values from Scholze et al. 2026, "The SpiNNaker2 chip: a many-core platform for flexible and scalable
brain-inspired computing", arXiv:2607.24396 (checked against its tables on 2026-09-30), and from Nazeer et al. 2024,
"Language modeling on a SpiNNaker2 neuromorphic chip", arXiv:2312.09084 (the source of the "18x").
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY, RED = "#1f77b4", "#ff7f0e", "#2ca02c", "0.5", "#d62728"
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10})

# Chip power per operating state (Table 2), in mW: (power of all 152 PEs, total power of the chip)
POWER_STATES = {"PEs off": (59.7, 75.2), "PEs sleep, 0.5 V": (214.7, 235.4), "PEs sleep, 0.8 V": (544.0, 564.7),
                "CoreMark, 0.5 V, 150 MHz": (403.9, 424.6), "CoreMark, 0.8 V, 300 MHz": (1227.2, 1247.9)}
# CoreMark throughput of all 152 PEs at full load (Table 2), iterations per second
COREMARK_PER_S = {"0.5 V, 150 MHz": 65_968, "0.8 V, 300 MHz": 138_168}
# DVS gesture SNN, 1000 time steps, energy per inference (J) per performance level and the timestep used (Table 4)
DVS_ENERGY = {"low PL\n(0.5 V, 150 MHz)": 2.010, "high PL\n(0.8 V, 300 MHz)": 1.023, "automatic PL\n(switches by load)": 0.741}
DVS_TICK_MS = {"low PL\n(0.5 V, 150 MHz)": 3, "high PL\n(0.8 V, 300 MHz)": 1, "automatic PL\n(switches by load)": 1}
# INT8 DNN efficiency in TOPS/W (Table 3). SpiNNaker2: measured on some PEs with all data in SRAM and extrapolated to
# all 152 PEs (Fig. 8 of the paper); the other devices: datasheet or survey values quoted by the paper
TOPS_PER_W = {"SpiNNaker2, 150 MHz": 2.77, "SpiNNaker2, 300 MHz": 2.06, "ARM Ethos N77": 5.13, "Groq TSP": 2.73,
              "IBM NorthPole": 2.70, "Jetson Orin Nano": 2.68, "Mobileye EyeQ5": 2.40, "Google Coral Edge TPU": 2.00,
              "GreenWaves GAP9": 0.34}
# Measured comparisons with an Nvidia A100, per inference or sample:
# (SpiNNaker2 energy, SpiNNaker2 time in ms, A100 energy, A100 time in ms), energies in the same unit per row
# dense INT8 layers including DRAM transfers, SpiNNaker2 at 150 MHz (Table 5 of the chip paper), energies in mJ
DNN_LAYERS = {"FC 1": (0.064, 0.111, 1.332, 0.012), "FC 2": (0.755, 0.944, 2.648, 0.024),
              "CONV 1": (2.195, 3.035, 7.041, 0.053), "CONV 2": (2.339, 3.918, 4.599, 0.039),
              "MM 1": (2.429, 3.971, 1.590, 0.015), "MM 2": (17.073, 24.501, 4.176, 0.034)}
# event-based GRU (EGRU), Nazeer et al. 2024, Table II (language model) and Table III (DVS gesture), energies in J
EGRU = {"language model, batch size 1": (0.0653, 170.25, 1.1935, 19.9),
        "DVS gesture, batch size 1": (0.023, 60.19, 0.067, 1.09),
        "DVS gesture, batch size 6": (0.023, 56.20, 0.011, 0.19)}


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
    ax_b.text(2.5, -0.3, "top view: 48 chips (48-node board, layout\nschematic), each with its DRAM (red, outside the\n"
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
    fig.text(0.5, 0.015, "whole HPI installation: 6 boards ≈ 43,800 PEs. "
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
    for x, w, t in [(0.5, 1.2, "code of the\nneuron model"), (1.8, 1.5, "synapse tables:\nweights, targets"),
                    (3.4, 1.5, "neuron states\nand parameters"), (5.0, 1.1, "recordings\n(spikes, v)"),
                    (6.2, 0.9, "spike\nbuffer")]:
        box(ax, x, 0.45 + y0, w, 1.45, t, "white", fs=7)
    box(ax, 7.5, 0.8 + y0, 1.0, 0.7, "DMA", "white", fs=8.5)
    box(ax, 7.6, 2.9 + y0, 0.95, 1.2, "NoC\ninter-\nface", NET, fs=8)
    box(ax, 9.4, 2.85 + y0, 1.7, 1.3, "network-on-chip\nand router\n(other PEs,\nother chips)", NET, fs=7.5)
    box(ax, 9.4, 0.65 + y0, 1.7, 1.0, "DRAM\nnext to the chip", DRAM, fs=7.5)
    arrow = dict(arrowstyle="-|>", mutation_scale=13)
    both = dict(arrowstyle="<|-|>", mutation_scale=12)
    grey = dict(color="0.55", lw=1.2, ls="--")
    ax.add_patch(FancyArrowPatch((8.55, 3.5 + y0), (9.4, 3.5 + y0), color=GREEN, lw=2, **both))
    ax.add_patch(FancyArrowPatch((7.5, 1.15 + y0), (7.12, 1.15 + y0), color=ORANGE, lw=2.5, **arrow))
    ax.add_patch(FancyArrowPatch((8.5, 1.15 + y0), (9.4, 1.15 + y0), **grey, **arrow))
    ax.add_patch(FancyArrowPatch((4.1, 4.1 + y0), (4.1, 4.55 + y0), **grey, **both))
    ax.text(4.2, 4.3 + y0, "used by some models", fontsize=6.5, color="0.45", va="center")
    ax.text(10.25, 0.45 + y0, "used e.g. by record_on_dram", fontsize=6.5, color="0.45", ha="center", va="top")
    # the steps, coloured like the timestep figure: incoming spikes orange, neuron update blue
    ax.add_patch(FancyArrowPatch((1.2, 4.55 + y0), (2.6, 3.9 + y0), color="k", lw=2, **arrow))
    ax.text(0.45, 4.2 + y0, "① wake up", fontsize=8.5, fontweight="bold")
    ax.add_patch(FancyArrowPatch((7.8, 2.9 + y0), (7.8, 1.5 + y0), color=ORANGE, lw=2.5, **arrow))
    ax.text(7.9, 2.2 + y0, "② spikes in:\nDMA →\nbuffer", fontsize=7.5, fontweight="bold", color="#c65f00",
            va="center")
    ax.add_patch(FancyArrowPatch((2.6, 1.9 + y0), (3.0, 2.9 + y0), color=ORANGE, lw=2.5, **arrow))
    ax.add_patch(FancyArrowPatch((6.55, 1.9 + y0), (5.5, 2.95 + y0), color=ORANGE, lw=2.5, **arrow))
    ax.text(0.45, 2.62 + y0, "③ read buffered spikes\nand their synapses", fontsize=8, fontweight="bold",
            color="#c65f00", va="center")
    ax.add_patch(FancyArrowPatch((4.4, 2.9 + y0), (4.45, 1.9 + y0), color=BLUE, lw=2.5, **both))
    ax.text(4.6, 2.5 + y0, "④ add weights,\nupdate neurons", fontsize=8, fontweight="bold", color=BLUE)
    ax.add_patch(FancyArrowPatch((5.6, 3.2 + y0), (7.6, 3.2 + y0), color=BLUE, lw=2.5, **arrow))
    ax.text(6.6, 2.8 + y0, "⑤ spikes out", fontsize=8.5, fontweight="bold", color=BLUE, ha="center")
    # timeline strip: one timestep
    t_scale = 8.8  # one timestep drawn over the width of the PE
    segs = [(0.0, 0.03, "k", "①"), (0.03, 0.35, ORANGE, "③"), (0.35, 0.55, BLUE, "④ ⑤"), (0.55, 1.0, "0.9", "sleep")]
    for a, b, c, t in segs:
        ax.add_patch(plt.Rectangle((a * t_scale, 0.35), (b - a) * t_scale, 0.5, fc=c, ec="none"))
        ax.text((a + b) / 2 * t_scale, 0.6, t if t != "①" else "", ha="center", va="center", fontsize=8.5,
                color="white" if c != "0.9" else "0.3", fontweight="bold")
    ax.text(0.0, 1.05, "① timer        ② arrives in the background, during the previous timestep", fontsize=7.5)
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


# Memory of one PE in py-spinnaker2 v0.8 for `lif`, as reported by its own mapping (hw.run(..., mapping_only=True),
# checked on 2026-10-01): network data from 0xE000 to 0x1F000; per presynaptic source a synapse row of a 12-byte header
# plus 2 bytes per synapse, padded to a multiple of 16 bytes, plus a 12-byte entry in the master population table
PE_DATA_BYTES = 0x1F000 - 0xE000  # 68 KiB
ERROR_LOG_BYTES = 2304


def row_bytes(n_synapses):
    return -(-(12 + 2 * n_synapses) // 16) * 16


def slice_bytes(n_sources, synapses_per_source):
    return n_sources * (row_bytes(synapses_per_source) + 12) + ERROR_LOG_BYTES


def clustered_pe_bytes():
    """Approximate memory of the two populations of the clustered network, from the expected synapses per source:
    E population: 200 E sources with 19 * 0.5 + 180 * 0.05 = 18.5 targets each, 50 I sources with 200 * 0.4 = 80;
    I population: 200 E sources with 50 * 0.3 = 15 targets each, 50 I sources with 49 * 0.5 = 24.5."""
    e_pop = 200 * (row_bytes(19) + 12) + 50 * (row_bytes(80) + 12) + ERROR_LOG_BYTES
    i_pop = 200 * (row_bytes(15) + 12) + 50 * (row_bytes(25) + 12) + ERROR_LOG_BYTES
    return [e_pop, i_pop]


def max_neurons_per_pe(n_sources):
    """Largest slice of an all-to-all layer that fits into one PE (small regions such as parameters ignored)."""
    return max(n for n in range(1, 257) if slice_bytes(n_sources, n) <= PE_DATA_BYTES)


def fig_memory():
    """A: energy of reading MNIST layer 1 from SRAM vs DRAM. B: how many PEs the example networks fill."""
    n_l1 = 784 * 128
    reads = n_l1 * 2 / 8  # 64-bit reads for all weights at 2 bytes per synapse
    # pJ per 64-bit read, Horowitz 2014: 8 KB cache 10 pJ, DRAM 1.3 nJ; 128 KB interpolated log-log between 32 KB
    # (20 pJ) and 1 MB (100 pJ)
    e_128k = 20 * (128 / 32) ** (np.log(100 / 20) / np.log(1024 / 32))
    bars = [("DRAM\n(next to the chip)", reads * 1300e-6, "#f4cccc"),
            ("SRAM, 128 KB\n(interpolated)", reads * e_128k * 1e-6, MEM), ("SRAM, 8 KB", reads * 10e-6, MEM)]
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw={"width_ratios": [1, 1.45]})
    for yy, (name, e, c) in enumerate(bars):
        ax_a.barh(yy, e, color=c, ec="k", height=0.55)
        ax_a.text(e * 1.2, yy, f"{e:.2f} µJ" if e < 1 else f"{e:.0f} µJ", va="center", fontsize=9, fontweight="bold")
    ax_a.set_yticks(range(len(bars)), [b[0] for b in bars], fontsize=8.5)
    ax_a.set_xscale("log")
    ax_a.set_xlim(0.05, 2000)
    ax_a.set_ylim(-0.6, 2.9)
    e_dram, e_lo, e_hi = bars[0][1], bars[1][1], bars[2][1]
    ax_a.annotate("", (e_dram, 2.45), (e_lo, 2.45), arrowprops={"arrowstyle": "-|>", "color": RED, "lw": 1.3})
    ax_a.text(np.sqrt(e_lo * e_dram), 2.55, f"× {e_dram / e_lo:.0f} to {e_dram / e_hi:.0f} more energy", ha="center",
              fontsize=8.5, color=RED)
    ax_a.set_xlabel("energy to read all 100,352 weights of MNIST layer 1 once (µJ, log scale)")
    ax_a.set_title("A: why keep the weights in local SRAM", loc="left", fontsize=10)
    # B: the price: networks fill PE memories and have to be split
    n_per_pe = max_neurons_per_pe(784)
    l1 = [min(n_per_pe, 128 - k) for k in range(0, 128, n_per_pe)]
    nets = [("MNIST layer 1\n784 inputs → 128 hidden", [slice_bytes(784, n) for n in l1],
             f"{len(l1)} PEs: at most {n_per_pe}\nhidden neurons per PE"),
            ("clustered network\n(primer Figure 21)", clustered_pe_bytes(),
             "2 PEs: one per population\n(E: 200, I: 50 neurons)"),
            ("MNIST layer 2\n128 hidden → 10 outputs", [slice_bytes(128, 10)], "1 PE")]
    gap = 0.12
    for row, (name, fills, note) in enumerate(nets):
        yy = 2 - row
        for b, used in enumerate(fills):
            x = b * (1 + gap)
            ax_b.add_patch(plt.Rectangle((x, yy - 0.3), 1, 0.6, fc="white", ec="k", lw=1))
            ax_b.add_patch(plt.Rectangle((x, yy - 0.3), used / PE_DATA_BYTES, 0.6, fc=ORANGE, ec="none"))
        ax_b.text(5 * (1 + gap) + 0.1, yy, note, va="center", fontsize=8)
        ax_b.text(-0.15, yy, name, ha="right", va="center", fontsize=8.5)
    handles = [plt.matplotlib.patches.Patch(fc="white", ec="k", label="network data memory of one PE (≈ 68 KiB for lif)"),
               plt.matplotlib.patches.Patch(color=ORANGE, label="synapse rows, routing entries and error log")]
    ax_b.legend(handles=handles, frameon=False, fontsize=7.5, loc="lower left", bbox_to_anchor=(0.2, 0.86), ncol=1)
    ax_b.set_xlim(-3.0, 7.6)
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
    # B: packets the sending PE emits for one spike, per routing mode
    examples = [("one input spike of the\nMNIST network: 128 targets\non 5 PEs (Figure 5)", 128, 5),
                ("cortex-like neuron:\n1,000 targets on 10 PEs", 1000, 10)]
    x = np.arange(len(examples))
    modes = [("one packet per target neuron (no routing tables)", GREY), ("core-to-core (py-spinnaker2 default):\n"
             "one packet per target PE", ORANGE), ("multicast: one packet, copied by the router", RED)]
    for k, (name, n_targets, n_pes) in enumerate(examples):
        for m_, ((label, color), n) in enumerate(zip(modes, [n_targets, n_pes, 1])):
            xx = k + (m_ - 1) * 0.27
            ax_p.bar(xx, n, width=0.25, color=color, label=label if k == 0 else None)
            ax_p.text(xx, n * 1.15, f"{n:,}", ha="center", fontsize=8.5)
    ax_p.set_xticks(x, [e[0] for e in examples], fontsize=8)
    ax_p.set_yscale("log")
    ax_p.set_ylim(0.7, 3e4)
    ax_p.set_ylabel("packets the sending PE emits\nfor one spike (log scale)")
    ax_p.legend(frameon=False, fontsize=7.5, loc="upper left")
    ax_p.set_title("B: packets sent for one spike", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "04_multicast.png")
    plt.close(fig)


def fig_scale():
    """PEs per system (reported) and an estimate of neuron capacity at ~150,000 neurons per chip."""
    systems = [("single-chip board", 1, 152), ("48-node board\n(one HPI run)", 48, 7_296),
               ("HPI installation\n(6 boards, if 48-node)", 288, 43_776), ("SpiNNcloud system,\nTU Dresden", 35_000, 5e6),
               ("planned maximum\n(Mayr et al. 2019)", None, 10e6)]
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
    ax_n.set_title("B: upper bound at ~150,000 neurons per chip", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "05_scale.png")
    plt.close(fig)


def fig_power_states():
    """A: power against work per second at the two performance levels, and the cheapest path (automatic switching).
    B: DVS gesture energy per performance level."""
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12.5, 4.8), gridspec_kw={"width_ratios": [1.2, 1]})
    off = POWER_STATES["PEs off"][0]
    lo0, lo1 = POWER_STATES["PEs sleep, 0.5 V"][0], POWER_STATES["CoreMark, 0.5 V, 150 MHz"][0]
    hi0, hi1 = POWER_STATES["PEs sleep, 0.8 V"][0], POWER_STATES["CoreMark, 0.8 V, 300 MHz"][0]
    # x = CoreMark throughput of all PEs (thousand iterations per second): 0 when sleeping, the measured value at full load
    w_lo, w_hi = COREMARK_PER_S["0.5 V, 150 MHz"] / 1e3, COREMARK_PER_S["0.8 V, 300 MHz"] / 1e3
    ax_a.plot([0, w_lo], [lo0, lo1], ":", color=BLUE, lw=2)
    ax_a.plot([0, w_hi], [hi0, hi1], ":", color=RED, lw=2)
    ax_a.plot([0, w_lo], [lo0, lo1], "o", color=BLUE, ms=9)
    ax_a.plot([0, w_hi], [hi0, hi1], "o", color=RED, ms=9)
    hi_at_lo_max = hi0 + w_lo / w_hi * (hi1 - hi0)
    ax_a.plot([0, w_lo], [lo0, lo1], color=GREEN, lw=6, alpha=0.35, solid_capstyle="round", zorder=0)
    ax_a.plot([w_lo, w_hi], [hi_at_lo_max, hi1], color=GREEN, lw=6, alpha=0.35, solid_capstyle="round", zorder=0)
    ax_a.plot([w_lo, w_lo], [lo1, hi_at_lo_max], color=GREEN, lw=2, ls="--")
    ax_a.text(w_lo + 2, (lo1 + hi_at_lo_max) / 2, "switch: the low level\ncan't do more work", fontsize=7.5, color=GREEN,
              va="center")
    ax_a.text(w_lo + 2, hi_at_lo_max - 40, f"≈ {hi_at_lo_max:.0f}", fontsize=8, color=RED, ha="left")
    ax_a.text(2, lo0 - 70, f"{lo0:.0f}", fontsize=8, color=BLUE)
    ax_a.text(2, hi0 + 40, f"{hi0:.0f}", fontsize=8, color=RED)
    ax_a.text(w_lo, lo1 - 70, f"{lo1:.0f}", fontsize=8, color=BLUE, ha="center")
    ax_a.text(w_hi, hi1 + 50, f"{hi1:.0f}", fontsize=8, color=RED, ha="center")
    ax_a.text(14, 290, "low level: 0.5 V, 150 MHz", fontsize=8.5, color=BLUE, fontweight="bold", rotation=13)
    ax_a.text(10, 640, "high level: 0.8 V, 300 MHz", fontsize=8.5, color=RED, fontweight="bold", rotation=24)
    ax_a.axhline(off, color="k", ls="--", lw=1)
    ax_a.text(0.75 * w_hi, off + 25, f"all PEs switched off: {off:.0f} mW", ha="center", fontsize=7.5)
    ax_a.text(2, 1330, "green: automatic switching, the cheapest way to do a given amount of work\n"
              "points: measured (sleeping and CoreMark at full load), dotted lines: interpolated", fontsize=7, color="0.3",
              va="top")
    ax_a.set_xticks([0, w_lo, w_hi], ["0\n(sleeping)", f"{w_lo:.0f}\n(low level at full load)",
                                      f"{w_hi:.0f}\n(high level at full load)"], fontsize=8)
    ax_a.set_xlim(-7, 1.12 * w_hi)
    ax_a.set_ylim(0, 1400)
    ax_a.set_xlabel("work per second: CoreMark throughput of all PEs (thousand iterations per second)")
    ax_a.set_ylabel("power of all 152 PEs (mW)")
    ax_a.set_title("A: stay at the low level as long as it can keep up", loc="left", fontsize=10)
    vals = list(DVS_ENERGY.values())
    ax_b.bar(range(3), vals, color=[GREY, RED, GREEN], width=0.7)
    for i, v in enumerate(vals):
        ax_b.text(i, v + 0.04, f"{v:.2f} J", ha="center", fontsize=8.5)
    ax_b.annotate("−28 % compared\nwith always high", (2, 0.80), (2, 1.45), fontsize=8.5, color=GREEN, fontweight="bold",
                  ha="center", arrowprops={"arrowstyle": "->", "color": GREEN})
    ax_b.text(0.42, 1.75, "← 3 ms per step at the low level:\nthe 1000 steps take 3 s instead\nof 1 s, and the baseline power\n"
              "is paid three times as long", ha="left", va="center", fontsize=7.5, color="0.3")
    ticks = [f"{name}\n{DVS_TICK_MS[key]} ms per step: {DVS_TICK_MS[key]} s" for key, name in
             zip(DVS_ENERGY, ["always low\n(0.5 V, 150 MHz)", "always high\n(0.8 V, 300 MHz)", "automatic\n(switches by load)"])]
    ax_b.set_xticks(range(3), ticks, fontsize=7.5)
    ax_b.set_ylabel("energy per inference (J)")
    ax_b.set_ylim(0, 2.7)
    ax_b.set_title("B: SNN (DVS gesture, 1000 steps): adapting the level to the load", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "02_power_states.png")
    plt.close(fig)


def energy_ratios():
    """Rows of Figure 9B: (label, A100 energy / SpiNNaker2 energy, SpiNNaker2 time / A100 time, group)."""
    rows = [(f"EGRU {k}", a / s, ts / ta, "egru") for k, (s, ts, a, ta) in EGRU.items()]
    layers = sorted(DNN_LAYERS.items(), key=lambda kv: -kv[1][2] / kv[1][0])
    return rows + [(f"dense INT8 layer {k}", a / s, ts / ta, "dnn") for k, (s, ts, a, ta) in layers]


def fig_reported_energy():
    """A: ideal INT8 efficiency vs edge accelerators (Table 3). B: measured energy and time vs an A100 (Table 5, Nazeer)."""
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={"width_ratios": [0.8, 1.25]})
    # A: TOPS/W
    names = list(TOPS_PER_W)
    y = np.arange(len(names))[::-1]
    for yy, name in zip(y, names):
        s2 = name.startswith("SpiNNaker2")
        ax_a.barh(yy, TOPS_PER_W[name], color=BLUE if s2 else GREY, height=0.6)
        ax_a.text(TOPS_PER_W[name] + 0.08, yy, f"{TOPS_PER_W[name]:.2f}", va="center", fontsize=8)
    ax_a.set_yticks(y, names, fontsize=8.5)
    ax_a.set_xlim(0, 6)
    ax_a.set_xlabel("INT8 efficiency for dense DNN layers (TOPS/W)")
    ax_a.set_title("A: ideal efficiency: on par with edge accelerators", loc="left", fontsize=10)
    ax_a.text(5.95, y[-1], "blue: measured with all data in SRAM,\nextrapolated to all 152 PEs\ngrey: datasheet or survey values",
              ha="right", va="center", fontsize=7, color="0.35")
    # B: measured energy ratio vs A100, and how much longer SpiNNaker2 takes
    rows = energy_ratios()
    yb = np.arange(len(rows))[::-1].astype(float)
    yb[len(EGRU):] -= 0.6  # gap between the two groups
    for yy, (label, r, slow, group) in zip(yb, rows):
        c = GREEN if r > 1 else RED
        ax_b.barh(yy, r - 1, left=1, color=c, height=0.6)
        ax_b.text(r * 1.12 if r > 1 else r / 1.12, yy, f"{r:.0f} ×" if r >= 10 else f"{r:.{1 if r > 1 else 2}f} ×", va="center",
                  ha="left" if r > 1 else "right", fontsize=8.5, fontweight="bold", color=c)
        ax_b.text(150, yy, f"{slow:.{1 if slow < 10 else 0}f} ×", va="center", ha="right", fontsize=8.5, color="0.3")
    ax_b.text(150, yb[0] + 0.75, "SpiNNaker2\ntakes longer", ha="right", va="bottom", fontsize=7.5, color="0.3")
    ax_b.axvline(1, color="k", lw=1)
    ax_b.set_xscale("log")
    ax_b.set_xlim(0.08, 160)
    ax_b.set_xticks([0.1, 1, 10], ["0.1", "1", "10"])
    ax_b.set_yticks(yb, [r[0] for r in rows], fontsize=8.5)
    ax_b.set_ylim(yb[-1] - 0.7, yb[0] + 1.6)
    ax_b.text(1.15, yb[-1] - 0.55, "SpiNNaker2 needs less energy →", fontsize=7.5, color=GREEN)
    ax_b.text(0.87, yb[-1] - 0.55, "← more energy", fontsize=7.5, color=RED, ha="right")
    ax_b.set_xlabel("energy of the A100 / energy of SpiNNaker2 (log scale)")
    ax_b.set_title("B: measured against an Nvidia A100 GPU", loc="left", fontsize=10)
    fig.text(0.01, 0.01, "B: EGRU = event-based GRU (Nazeer et al. 2024), energy per inference or sample; dense layers: "
             "SpiNNaker2 at 150 MHz, including DRAM transfers (Scholze et al. 2026, Table 5).",
             fontsize=7.5, color="0.4")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT / "03_reported_energy.png")
    plt.close(fig)


def check():
    ratios = {label: (r, slow) for label, r, slow, _ in energy_ratios()}
    r18, slow18 = ratios["EGRU language model, batch size 1"]
    assert abs(r18 - 18.3) < 0.1 and abs(slow18 - 8.6) < 0.1  # the "18x", and 8.6 times slower
    assert ratios["EGRU DVS gesture, batch size 6"][0] < 0.5  # at batch size 6 the A100 needs less energy
    assert abs(ratios["dense INT8 layer FC 1"][0] - 20.8) < 0.1 and abs(ratios["dense INT8 layer MM 2"][0] - 0.24) < 0.01
    slows = [slow for _, slow in ratios.values()]
    assert min(slows) > 8 and max(slows) < 730  # SpiNNaker2 is always slower, by 8.6 to 721 times
    assert abs((1 - DVS_ENERGY["automatic PL\n(switches by load)"] / DVS_ENERGY["high PL\n(0.8 V, 300 MHz)"]) - 0.28) < 0.01
    hi_at_lo_max = 544.0 + COREMARK_PER_S["0.5 V, 150 MHz"] / COREMARK_PER_S["0.8 V, 300 MHz"] * (1227.2 - 544.0)
    assert abs(hi_at_lo_max - 870) < 1  # Figure 8A: high level at the work the low level reaches at full load
    assert round(clustered_synapses()) == 11925
    # synapse rows as reported by py-spinnaker2's mapping for MNIST layer 1: 208.2 KiB for all 128 hidden neurons,
    # 49.0 KiB for 26 and 61.2 KiB for 27 neurons per PE, and at most 26 neurons per PE
    assert [round(784 * row_bytes(n) / 1024, 1) for n in (128, 26, 27)] == [208.2, 49.0, 61.2]
    assert max_neurons_per_pe(784) == 26
    assert 6 * 48 * 152 == 43776 and 48 * 152 == 7296  # HPI installation and one board, if 48-node boards
    assert abs((1227.2 / 300) / (403.9 / 150) - 1.52) < 0.01  # energy per cycle at full load, high vs low level
    assert abs(2.281 / 0.825 - TOPS_PER_W["SpiNNaker2, 150 MHz"]) < 0.01  # Table 3: TOPS / W at 150 MHz


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
