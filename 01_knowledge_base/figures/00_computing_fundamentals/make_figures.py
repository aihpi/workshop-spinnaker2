"""Figures for 00_computing_fundamentals.md. Run: uv run --with numpy --with matplotlib make_figures.py"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY, RED = "#1f77b4", "#ff7f0e", "#2ca02c", "0.5", "#d62728"
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10})

# typical orders of magnitude (see the table in section 3): size in bytes, access time in seconds
HIERARCHY = [("registers", 1e2, 0.3e-9), ("L1 cache", 32e3, 1e-9), ("L2 cache", 1e6, 4e-9), ("L3 cache", 16e6, 15e-9),
             ("main memory (DRAM)", 16e9, 75e-9), ("SSD", 1e12, 100e-6)]


def box(ax, xy, w, h, text, color="white", fs=9, ec="k"):
    ax.add_patch(FancyBboxPatch((xy[0] - w / 2, xy[1] - h / 2), w, h, boxstyle="round,pad=0.03", fc=color, ec=ec, lw=1))
    ax.text(*xy, text, ha="center", va="center", fontsize=fs)


def arrow(ax, a, b, color="k", lw=1.5, both=True):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="<|-|>" if both else "-|>", mutation_scale=12, color=color, lw=lw))


def fig_core():
    fig, (ax_c, ax_m, ax_s) = plt.subplots(1, 3, figsize=(13, 5.6), gridspec_kw={"width_ratios": [1, 1.2, 1.2]})
    CORE, MEM = "#cfe2f3", "#fde0c5"
    # A: inside one core
    ax_c.add_patch(FancyBboxPatch((-1.6, -1.7), 3.2, 3.8, boxstyle="round,pad=0.05", fc=CORE, ec="k", lw=1.2))
    ax_c.text(0, 1.85, "one core", ha="center", fontsize=10, fontweight="bold")
    box(ax_c, (0, 1.05), 2.6, 0.6, "control unit\nfetches and decodes instructions", "white", fs=7.5)
    box(ax_c, (-0.65, 0.05), 1.3, 0.7, "ALU\ncomputes", "white", fs=7.5)
    box(ax_c, (0.7, 0.05), 1.2, 0.7, "registers\ntiny, fastest\nstorage", "white", fs=7)
    ax_c.add_patch(plt.Rectangle((-1.45, -0.45), 2.9, 1.95, fill=False, ec=RED, lw=1.5, ls="--"))
    ax_c.text(1.78, 0.55, "= CPU of\nFigure 2A", fontsize=8, color=RED, va="center")
    box(ax_c, (0, -1.15), 2.6, 0.55, "L1 cache (small SRAM)", MEM, fs=7.5)
    ax_c.text(0, -2.35, "the cache is an addition (section 3),\nnot part of the von Neumann model", ha="center",
              fontsize=8, color="0.3")
    ax_c.set_xlim(-2.0, 2.9)
    ax_c.set_ylim(-3.4, 2.7)
    # B: laptop chip, few large cores, main memory outside the chip, connected by a bus
    ax_m.add_patch(plt.Rectangle((-2.3, -1.25), 4.6, 3.45, fc="0.97", ec="k", lw=1.2))
    for k in range(4):
        box(ax_m, (-1.7 + 1.13 * k, 1.6), 0.95, 0.75, "P-core", CORE, fs=7)
    for k in range(6):
        box(ax_m, (-1.85 + 0.74 * k, 0.7), 0.6, 0.5, "E-core", CORE, fs=5.5)
    box(ax_m, (0, 0.05), 4.2, 0.4, "shared cache", MEM, fs=7.5)
    box(ax_m, (-1.15, -0.75), 1.9, 0.6, "GPU, 8–10 cores", "#d9ead3", fs=7)
    box(ax_m, (1.15, -0.75), 1.9, 0.6, "Neural Engine, 16 cores", "#d9ead3", fs=6.5)
    ax_m.plot([0, 0], [-1.25, -2.05], color=RED, lw=5, solid_capstyle="butt")
    ax_m.text(0.15, -1.65, "bus (as in Figure 2A)", fontsize=7.5, color=RED, va="center")
    box(ax_m, (0, -2.35), 3.0, 0.55, "main memory (DRAM), shared", MEM, fs=7.5)
    ax_m.text(0, -3.05, "10 CPU cores up to 4.4 GHz: the von Neumann\nstructure of Figure 2A with several cores",
              ha="center", fontsize=8, color="0.3")
    ax_m.set_xlim(-2.6, 2.6)
    ax_m.set_ylim(-3.4, 2.7)
    # C: SpiNNaker2, many small cores with their own memory
    ax_s.add_patch(plt.Rectangle((-2.3, -1.25), 4.6, 3.45, fc="0.97", ec="k", lw=1.2))
    cols, rows = 19, 8
    for k in range(cols * rows):
        r, c = divmod(k, cols)
        x, y = -2.15 + c * 0.227, 1.8 - r * 0.38
        ax_s.add_patch(plt.Rectangle((x, y), 0.19, 0.17, fc=CORE, ec="none"))
        ax_s.add_patch(plt.Rectangle((x, y - 0.16), 0.19, 0.14, fc=MEM, ec="none"))
    ax_s.text(0, -2.05, "no shared main memory for the network:\neach core has its own memory (orange)", ha="center",
              fontsize=8, color="0.3")
    ax_s.text(0, -3.05, "152 small cores at 150–300 MHz: the distributed\ndesign of Figure 2B (external DRAM only for large data)",
              ha="center", fontsize=8, color="0.3")
    ax_s.set_xlim(-2.6, 2.6)
    ax_s.set_ylim(-3.4, 2.7)
    for ax in (ax_c, ax_m, ax_s):
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    for ax, title in [(ax_c, "A: what a core is"), (ax_m, "B: laptop chip (Apple M4, schematic)"),
                      (ax_s, "C: SpiNNaker2 chip (schematic)")]:  # same height for all titles
        fig.text(ax.get_position().x0, 0.96, title, fontsize=10, va="top")
    fig.savefig(OUT / "01_what_is_a_core.png")
    plt.close(fig)


def fig_von_neumann():
    fig, (ax_v, ax_d) = plt.subplots(1, 2, figsize=(11, 5))
    MEM, CORE = "#fde0c5", "#cfe2f3"
    # A: von Neumann: one CPU, one memory, everything over one bus
    box(ax_v, (0, 2.6), 2.6, 1.0, "CPU\ncontrol unit, ALU, registers", CORE, fs=8.5)
    box(ax_v, (0, -1.9), 2.6, 1.0, "memory\ninstructions and data", MEM, fs=8.5)
    ax_v.add_patch(plt.Rectangle((-0.35, -1.4), 0.7, 3.5, fc="#f4cccc", ec=RED, lw=1.5))  # the bus
    ax_v.text(-0.5, 0.35, "one shared bus", rotation=90, ha="right", va="center", fontsize=8.5, color=RED)
    # transfers in single file: the lowest one is moving, the others wait for the bus
    for k, (t, moving) in enumerate([("instr.", False), ("data", False), ("instr.", False), ("data", True)]):
        y = 1.55 - 0.72 * k
        box(ax_v, (0, y), 0.56, 0.42, t, "white" if moving else "0.9", fs=6.5, ec=RED if moving else "0.6")
    ax_v.plot([0.5, 0.6, 0.6, 0.5], [1.8, 1.8, 0.1, 0.1], color="0.4", lw=1)
    ax_v.text(0.7, 0.95, "waiting for\nthe bus", fontsize=8, color="0.3", va="center")
    ax_v.text(0.7, -0.61, "← in transfer", fontsize=8, color=RED, va="center")
    ax_v.add_patch(FancyArrowPatch((1.8, 1.7), (1.8, -0.35), arrowstyle="<|-|>", mutation_scale=10, color=RED, lw=1))
    ax_v.text(1.95, 0.7, "either direction,\nbut only one\ntransfer at a time", fontsize=7.5, color=RED, va="center")
    for x, name in [(-2.4, "input"), (2.4, "output")]:
        box(ax_v, (x, -1.1), 1.1, 0.6, name, "#e8e8e8", fs=8)
        edge = x - 0.55 if x > 0 else x + 0.55  # box edge facing the bus
        ax_v.plot([edge, 0.35 if x > 0 else -0.35], [-1.1, -1.1], color="k", lw=1.2)
    ax_v.text(0, -2.85, "all traffic, instructions and data, goes through one path,\none transfer at a time: "
              "the von Neumann bottleneck", ha="center", fontsize=8.5, color=RED)
    ax_v.set_title("A: von Neumann computer", loc="left", fontsize=10)
    ax_v.set_xlim(-3.3, 4.2)
    ax_v.set_ylim(-3.3, 3.3)
    # B: distributed: each core with its own memory, cores linked through a router
    box(ax_d, (0, 0.3), 2.2, 0.7, "router / network", "#d9ead3", fs=8.5, ec=GREEN)
    xs = [-2.4, -0.8, 0.8, 2.4]
    for x in xs:
        for core_y, mem_y in [(1.55, 2.5), (-0.95, -1.9)]:  # core next to the router, memory on the outside
            box(ax_d, (x, core_y), 1.1, 0.55, "core", CORE, fs=8)
            box(ax_d, (x, mem_y), 1.1, 0.55, "local\nmemory", MEM, fs=7)
            ax_d.plot([x, x], [core_y + 0.28 * (1 if mem_y > core_y else -1), mem_y - 0.28 * (1 if mem_y > core_y else -1)],
                      color=BLUE, lw=6, solid_capstyle="butt")
            ax_d.plot([x, 0.9 * x / 2.4], [core_y - 0.28 * (1 if mem_y > core_y else -1), 0.3 + 0.35 * (1 if mem_y > core_y else -1)],
                      color=GREEN, lw=1)
    ax_d.text(3.05, 2.0, "thick: fast\nlocal access", fontsize=7.5, color=BLUE, va="center")
    ax_d.text(3.05, 0.3, "thin: rare\nmessages", fontsize=7.5, color=GREEN, va="center")
    ax_d.text(0.3, -2.85, "most traffic stays local between a core and its own memory,\n"
              "only small messages cross the network", ha="center", fontsize=8.5, color="0.25")
    ax_d.set_title("B: distributed memory, as in SpiNNaker2 (schematic)", loc="left", fontsize=10)
    ax_d.set_xlim(-3.2, 4.0)
    ax_d.set_ylim(-3.3, 3.3)
    for ax in (ax_v, ax_d):
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / "02_von_neumann_vs_distributed.png")
    plt.close(fig)


def fig_hierarchy():
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    colors = [GREY, BLUE, BLUE, BLUE, ORANGE, RED]
    for (name, size, t), c in zip(HIERARCHY, colors):
        ax.plot(size, t, "o", color=c, ms=9, mec="k", zorder=3)
        ax.annotate(name, (size, t), (8, -12 if name != "SSD" else 6), textcoords="offset points", fontsize=8.5)
    ax.plot([h[1] for h in HIERARCHY], [h[2] for h in HIERARCHY], color="0.8", lw=1, zorder=1)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(20, 1e14)
    ax.set_ylim(1e-10, 1e-3)
    ticks_s = [1e2, 1e3, 1e6, 1e9, 1e12]
    ax.set_xticks(ticks_s, ["100 B", "1 KB", "1 MB", "1 GB", "1 TB"])
    ticks_t = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4]
    ax.set_yticks(ticks_t, ["1 ns", "10 ns", "100 ns", "1 µs", "10 µs", "100 µs"])
    ax.set_xlabel("typical capacity (logarithmic scale)")
    ax.set_ylabel("typical access time\n(logarithmic scale)")
    ax.set_title("Larger memory is slower: the memory hierarchy", loc="left", fontsize=10)
    ax.text(1e8, 3e-10, "fast, small, on the chip (SRAM)", fontsize=8, color=BLUE)
    ax.text(1e9, 1.5e-6, "slow, large, off the chip", fontsize=8, color=RED)
    fig.tight_layout()
    fig.savefig(OUT / "03_memory_hierarchy.png")
    plt.close(fig)


def fig_bus_vs_noc():
    fig, (ax_b, ax_n) = plt.subplots(1, 2, figsize=(10.5, 3.8))
    # A: shared bus
    ax_b.plot([-3, 3], [0, 0], color="k", lw=4)
    names = ["CPU", "memory", "GPU", "network card"]
    for k, n in enumerate(names):
        x = -2.4 + 1.6 * k
        box(ax_b, (x, 1.1), 1.3, 0.7, n, "#cfe2f3" if k != 1 else "#fde0c5", fs=8.5)
        ax_b.plot([x, x], [0.75, 0], color="k", lw=1.5)
    arrow(ax_b, (-2.4, 0.25), (-0.8, 0.25), color=RED, lw=2.5, both=False)
    ax_b.text(-1.6, -0.45, "only one transfer\nat a time", ha="center", fontsize=8.5, color=RED)
    ax_b.text(1.8, -0.45, "the others wait", ha="center", fontsize=8.5, color=GREY)
    ax_b.set_title("A: shared bus", loc="left", fontsize=10)
    ax_b.set_xlim(-3.3, 3.3)
    ax_b.set_ylim(-1.2, 1.8)
    # B: network-on-chip, 3x3 mesh
    pos = {(i, j): (-1.6 + 1.6 * i, -0.9 + 1.2 * j) for i in range(3) for j in range(3)}
    for (i, j), (x, y) in pos.items():
        if i < 2:
            ax_n.plot([x, pos[(i + 1, j)][0]], [y, y], color="0.7", lw=2, zorder=1)
        if j < 2:
            ax_n.plot([x, x], [y, pos[(i, j + 1)][1]], color="0.7", lw=2, zorder=1)
    for (i, j), (x, y) in pos.items():
        box(ax_n, (x, y), 0.8, 0.5, "block", "#cfe2f3", fs=7.5)
    for a, b, c in [((0, 0), (1, 0), GREEN), ((2, 2), (2, 1), ORANGE), ((0, 2), (1, 2), BLUE)]:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        dx, dy = (x1 - x0), (y1 - y0)
        arrow(ax_n, (x0 + 0.42 * (dx != 0) * (1 if dx > 0 else -1), y0 + 0.27 * (dy != 0) * (1 if dy > 0 else -1)),
              (x1 - 0.42 * (dx != 0) * (1 if dx > 0 else -1), y1 - 0.27 * (dy != 0) * (1 if dy > 0 else -1)),
              color=c, lw=2.5, both=False)
    ax_n.text(2.4, 0.3, "several packets\ntravel at the\nsame time", fontsize=8.5, color="0.25")
    ax_n.set_title("B: network-on-chip", loc="left", fontsize=10)
    ax_n.set_xlim(-2.3, 3.6)
    ax_n.set_ylim(-1.5, 1.9)
    for ax in (ax_b, ax_n):
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / "04_bus_vs_noc.png")
    plt.close(fig)


def fig_bare_metal():
    """One storyline: code written and compiled on the host (with an OS), uploaded, run bare-metal on a core."""
    fig, ax = plt.subplots(figsize=(13, 5.4))
    CODE = "#d9ead3"
    # the two places
    ax.add_patch(FancyBboxPatch((-0.3, -2.3), 8.1, 5.4, boxstyle="round,pad=0.05", fc="0.97", ec="0.6", lw=1))
    ax.text(3.75, 2.75, "host computer (laptop or server), with an operating system", ha="center", fontsize=10,
            fontweight="bold")
    ax.add_patch(FancyBboxPatch((9.4, -2.3), 4.6, 5.4, boxstyle="round,pad=0.05", fc="0.97", ec="0.6", lw=1))
    ax.text(11.7, 2.75, "SpiNNaker2 board, no operating system", ha="center", fontsize=10, fontweight="bold")
    # 1 the user writes Python; the C code of the chosen neuron model ships with py-spinnaker2
    ax.text(0.0, 2.2, "① write the network in Python", fontsize=9, fontweight="bold")
    ax.add_patch(plt.Rectangle((0.0, 1.0), 3.6, 1.0, fc="white", ec="0.5"))
    ax.text(0.1, 1.9, 'pop = snn.Population(size=100,\n      neuron_model="lif", params=...)\nhw.run(net, timesteps=1000)',
            fontsize=6.5, family="monospace", va="top")
    ax.add_patch(plt.Rectangle((0.0, -0.05), 3.6, 0.85, fc="white", ec="0.5", ls="--"))
    ax.text(0.1, 0.72, "C code of the lif model, part of py-spinnaker2\n(written once by its developers;\n"
            "own C code only for custom models)", fontsize=6.5, va="top", color="0.3")
    ax.add_patch(FancyArrowPatch((2.9, 1.0), (2.9, 0.8), arrowstyle="-|>", mutation_scale=10, color="0.4", lw=1, ls=":"))
    ax.text(3.0, 0.9, "selects", fontsize=6.5, color="0.4", va="center")
    # 2 compile the C code, turn the Python network into data
    ax.text(4.1, 2.2, "② prepare", fontsize=9, fontweight="bold")
    box(ax, (4.9, 0.35), 1.5, 0.7, "GCC for ARM\n(cross-compiler)", "#cfe2f3", fs=7.5)
    box(ax, (4.9, 1.5), 1.5, 0.7, "py-spinnaker2\nmapping", "#cfe2f3", fs=7.5)
    ax.add_patch(plt.Rectangle((6.0, 1.05), 1.6, 0.9, fc="white", ec="0.5"))
    ax.text(6.8, 1.5, "network data:\nparameters,\nweights, routing", ha="center", va="center", fontsize=6.5)
    ax.add_patch(plt.Rectangle((6.0, -0.05), 1.6, 0.8, fc="white", ec="0.5"))
    ax.text(6.1, 0.65, "4b 68 1b 68\n03 fb 02 f0 ...", fontsize=6.5, family="monospace", va="top")
    ax.text(6.8, 0.05, "machine code", ha="center", fontsize=6.5, color="0.35")
    for a, b in [((3.6, 1.5), (4.15, 1.5)), ((3.6, 0.35), (4.15, 0.35)), ((5.65, 1.5), (6.0, 1.5)),
                 ((5.65, 0.35), (6.0, 0.35))]:
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color="k", lw=1.2))
    # host software stack
    ax.text(0.0, -0.35, "software stack of the host:", fontsize=8, color="0.3")
    for k, (t, c) in enumerate([("application: Python, py-spinnaker2, compiler", CODE),
                                ("operating system: scheduler, drivers, files, network", "#fde0c5"),
                                ("hardware: x86 or ARM CPU", "#e8e8e8")]):
        box(ax, (2.3, -0.75 - 0.5 * k), 4.6, 0.42, t, c, fs=7.5)
    # 3 upload
    ax.add_patch(FancyArrowPatch((7.7, 1.0), (9.9, 1.0), arrowstyle="-|>", mutation_scale=18, color=GREEN, lw=2.5))
    ax.text(8.6, 0.8, "③ py-spinnaker2\nuploads machine\ncode + network data\nvia Ethernet", ha="center", va="top", fontsize=8.5,
            fontweight="bold", color=GREEN)
    # 4 run bare-metal on one core
    ax.text(9.7, 2.2, "④ each core runs the code directly", fontsize=9, fontweight="bold")
    box(ax, (11.7, 1.2), 3.6, 0.6, "machine code of the lif model + its data", CODE, fs=8)
    box(ax, (11.7, 0.45), 3.6, 0.6, "hardware: ARM Cortex-M4F + 128 KB SRAM", "#e8e8e8", fs=8)
    ax.text(9.7, -0.2, "software stack of a core: no operating system in between", fontsize=8, color="0.3")
    for k, t in enumerate(["a timer interrupt (e.g. every 1 ms) wakes the core", "update all neurons, send spikes",
                           "go back to sleep until the next interrupt"]):
        ax.text(9.8, -0.7 - 0.45 * k, f"{k + 1}. {t}", fontsize=8)
    ax.annotate("", (13.75, -0.65), (13.75, -1.6), arrowprops={"arrowstyle": "-|>", "color": "0.4",
                                                               "connectionstyle": "arc3,rad=0.6"})
    ax.text(11.7, -2.05, "memory layout fixed by py-spinnaker2 before the run", ha="center", fontsize=7.5, color="0.35")
    ax.set_xlim(-0.5, 14.3)
    ax.set_ylim(-2.5, 3.4)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / "06_bare_metal_cross_compilation.png")
    plt.close(fig)


if __name__ == "__main__":
    fig_core()
    fig_von_neumann()
    fig_hierarchy()
    fig_bus_vs_noc()
    fig_bare_metal()
