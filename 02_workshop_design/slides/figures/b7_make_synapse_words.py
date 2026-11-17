"""Slide figure for slide 7.7: the 16-bit synapse word of lif next to that of lif_no_delay.

py-spinnaker2 v0.8.5, neuron_models/lif_neuron.py: lif uses SynapseWordSpec(word_size=16, weight=4, delay=3,
synapse_type=1, target=8); lif_no_delay uses SynapseWordSpec(word_size=16, weight=7, delay=0, synapse_type=1,
target=8). The 1-bit synapse_type (excitatory or inhibitory) acts as the sign. The NIR import maps LIF neurons onto
lif_no_delay. The order of the fields in the word is schematic, not the physical layout.
Run: uv run --with numpy --with matplotlib python b7_make_synapse_words.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ACCENT, GREY, DARK = "#B1063A", "#83888C", "#212427"  # accent: HPI red (slide style); change here for the block colour
LIGHT = "#E8C2CE"  # a light tint of the accent for the sign bit
words = {
    "lif\n(notebooks 01, 02)": [("sign", 1, LIGHT, "±"), ("weight", 4, ACCENT, "−15 to 15"), ("delay", 3, "0.75", "0 to 7 steps"),
                                ("target neuron", 8, "0.9", "up to 256 per PE")],
    "lif_no_delay\n(NIR import,\nnotebooks 03, 04)": [("sign", 1, LIGHT, "±"), ("weight", 7, ACCENT, "−127 to 127"),
                                                     ("target neuron", 8, "0.9", "up to 256 per PE")],
}
for fields in words.values():
    assert sum(bits for _, bits, _, _ in fields) == 16
    weight_bits = dict((n, b) for n, b, _, _ in fields)["weight"]
    assert [f for f in fields if f[0] == "weight"][0][3] == f"−{2 ** weight_bits - 1} to {2 ** weight_bits - 1}"

plt.rcParams.update({"font.size": 18})
fig, ax = plt.subplots(figsize=(13, 5.2))
ax.set(xlim=(-5.2, 16.3), ylim=(-5.0, 1.6), aspect="equal")
ax.axis("off")
for row, (name, fields) in enumerate(words.items()):
    y = -row * 3.6
    ax.text(-0.5, y + 0.5, name, ha="right", va="center", color=DARK, fontsize=17)
    x = 0
    for label, bits, color, meaning in fields:
        for b in range(bits):
            ax.add_patch(Rectangle((x + b, y), 1, 1, fc=color, ec="white", lw=2))
        text_color = "white" if color == ACCENT else DARK
        ax.text(x + bits / 2, y + 0.5, label if bits > 1 else "", ha="center", va="center", color=text_color, fontsize=15)
        ax.text(x + bits / 2, y - 0.3, f"{bits} bit{'s' if bits > 1 else ''}", ha="center", va="top", color=GREY, fontsize=13)
        ax.text(x + bits / 2, y - 1.0, meaning, ha="center", va="top", color=ACCENT if label == "weight" else DARK, fontsize=15)
        x += bits
ax.text(0.5, 1.15, "sign", ha="center", va="bottom", color=GREY, fontsize=13)
fig.text(0.99, 0.01, "py-spinnaker2 v0.8.5, neuron_models/lif_neuron.py; one synapse = one 16-bit word; order of the fields schematic",
         ha="right", va="bottom", fontsize=11, color=GREY)
plt.tight_layout()
out = Path(__file__).with_name("b7_synapse_words.png")
fig.savefig(out, dpi=200)
print("saved", out)
