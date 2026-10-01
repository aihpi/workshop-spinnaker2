"""Run identical micro-networks on the chip and on the Brian2 backend; writes result_chip.json and result_brian2.json.

Usage: python compare_brian2_chip.py chip | brian2   (chip needs a session on cx51). See 01_knowledge_base/03_brian2_fallback.md."""
import sys, json
import numpy as np
from spinnaker2 import snn, hardware, brian2_sim

T = 60

def build():
    net = snn.Network("cmp")
    pops = {}
    def stim(name, spikes):
        p = snn.Population(size=len(spikes), neuron_model="spike_list", params=dict(enumerate(spikes)), name=name)
        net.add(p); return p
    def pop(name, model, params, size=1):
        p = snn.Population(size=size, neuron_model=model, params=params, name=name, record=["spikes", "v"])
        net.add(p); pops[name] = p; return p
    def proj(pre, post, conns):
        net.add(snn.Projection(pre=pre, post=post, connections=conns))

    # A: lif, delay 0, reset by subtraction
    s = stim("sA", [[1, 5, 10]]); A = pop("A_lif_basic", "lif", {"threshold": 1.0, "alpha_decay": 0.9}); proj(s, A, [[0, 0, 2, 0]])
    # B: input lands exactly on threshold (>= vs >)
    s = stim("sB", [[3]]); B = pop("B_lif_equal_thr", "lif", {"threshold": 1.0, "alpha_decay": 0.5}); proj(s, B, [[0, 0, 1, 0]])
    # C: delay 3
    s = stim("sC", [[2]]); C = pop("C_lif_delay3", "lif", {"threshold": 4.0, "alpha_decay": 0.8}); proj(s, C, [[0, 0, 5, 3]])
    # D: constant i_offset 0.3, no leak (float32 vs float64)
    pop("D_lif_ioffset", "lif", {"threshold": 1.0, "alpha_decay": 1.0, "i_offset": 0.3})
    # E: excitatory and inhibitory input
    s = stim("sE", [[2, 3, 4, 5, 6], [3, 4]]); E = pop("E_lif_exc_inh", "lif", {"threshold": 5.0, "alpha_decay": 0.9}); proj(s, E, [[0, 0, 3, 0], [1, 0, -2, 0]])
    # F: lif_curr_exp chain of two layers
    s = stim("sF", [[2]])
    cexp = {"threshold": 5.0, "alpha_decay": 0.8, "exc_decay": 0.5, "inh_decay": 0.5, "t_refract": 0}
    F1 = pop("F1_cexp_layer1", "lif_curr_exp", cexp); F2 = pop("F2_cexp_layer2", "lif_curr_exp", cexp)
    proj(s, F1, [[0, 0, 10, 0]]); proj(F1, F2, [[0, 0, 10, 0]])
    # G: lif_curr_exp with refractory period, constant drive
    pop("G_cexp_refract", "lif_curr_exp", {"threshold": 1.0, "alpha_decay": 0.9, "i_offset": 0.6, "t_refract": 3, "reset": "reset_to_v_reset"})
    # H: alif, constant drive
    pop("H_alif", "alif", {"threshold": 2.0, "alpha_decay": 0.9, "i_offset": 1.5, "threshold_adp_inc": 0.4, "threshold_adp_decay": 0.97, "t_refract": 0, "reset": "reset_to_v_reset"})
    # I: lif -> lif chain (latency per layer)
    I = pop("I_lif_layer2", "lif", {"threshold": 1.0, "alpha_decay": 0.5}); proj(A, I, [[0, 0, 2, 0]])
    return net, pops

def collect(pops):
    out = {}
    for name, p in pops.items():
        v = p.get_voltages() if hasattr(p, "get_voltages") else None
        out[name] = {"spikes": [int(x) for x in p.get_spikes()[0]],
                     "v": [round(float(x), 4) for x in np.asarray(v[0])[:25]] if v else None}
    return out

backend = sys.argv[1]
net, pops = build()
if backend == "chip":
    hardware.SpiNNcloud48NodeBoard().run(net, T)
else:
    brian2_sim.Brian2Backend().run(net, T)
json.dump(collect(pops), open(f"result_{backend}.json", "w"), indent=1)
print("done", backend)
