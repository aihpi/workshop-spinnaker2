"""Edge cases of the Brian2 backend (no board needed). See 01_knowledge_base/03_brian2_fallback.md, section 3."""
import traceback, numpy as np
from spinnaker2 import snn, brian2_sim

def case(name, fn):
    try:
        print(f"[{name}] ->", fn())
    except Exception as e:
        print(f"[{name}] -> {type(e).__name__}: {str(e)[:150]}")

def lif_net(w=2.5, rec=("spikes",)):
    snn.Network.clear_names() if hasattr(snn.Network, "clear_names") else None
    net = snn.Network("e")
    s = snn.Population(size=1, neuron_model="spike_list", params={0: [1, 5]}, name="s")
    p = snn.Population(size=1, neuron_model="lif", params={"threshold": 1.0}, name="p", record=list(rec))
    net.add(s, p, snn.Projection(pre=s, post=p, connections=[[0, 0, w, 0]]))
    return net, p

def poisson(tref, rec=("spikes",)):
    net = snn.Network("pp")
    src = snn.Population(size=200, neuron_model="poisson_process", params={"p": 0.2, "Tref": tref, "seed": 1}, name="src", record=list(rec))
    net.add(src)
    brian2_sim.Brian2Backend().run(net, 1000)
    sp = src.get_spikes(); n = sum(len(v) for v in sp.values())
    return f"mean rate per step {n/200/1000:.3f}"

def poisson_relay(tref):
    net = snn.Network("pr")
    src = snn.Population(size=200, neuron_model="poisson_process", params={"p": 0.2, "Tref": tref, "seed": 1}, name="src")
    relay = snn.Population(size=200, neuron_model="lif", params={"threshold": 1.0, "alpha_decay": 0.0}, name="relay", record=["spikes"])
    net.add(src, relay, snn.Projection(pre=src, post=relay, connections=[[i, i, 2, 0] for i in range(200)]))
    brian2_sim.Brian2Backend().run(net, 1000)
    n = sum(len(v) for v in relay.get_spikes().values())
    return f"relayed rate per step {n/200/1000:.3f} (chip expectation p/(1+p*Tref) = {0.2/(1+0.2*tref):.3f})"

def qfalse():
    net, p = lif_net(w=0.6)
    brian2_sim.Brian2Backend().run(net, 10, quantize_weights=False); return p.get_spikes()
def kw():
    net, p = lif_net(); brian2_sim.Brian2Backend().run(net, timesteps=10); return p.get_spikes()
def unsupported():
    net = snn.Network("u"); net.add(snn.Population(size=1, neuron_model="lif_prob", params={}, name="x"))
    brian2_sim.Brian2Backend().run(net, 10)
def rerun():
    net, p = lif_net(); b = brian2_sim.Brian2Backend(); b.run(net, 10); first = dict(p.get_spikes()); b.run(net, 10)
    return f"first {first}, after second run {p.get_spikes()}"
def weight_clip():
    net, p = lif_net(w=40, rec=("spikes","v")); brian2_sim.Brian2Backend().run(net, 4); return p.get_voltages()
def ignored_kwargs():
    net, p = lif_net(); brian2_sim.Brian2Backend().run(net, 10, sys_tick_in_s=5e-3, record_power=True, mapping_only=True); return p.get_spikes()

for n, f in [("poisson record spikes", lambda: poisson(0)), ("poisson Tref0 via relay", lambda: poisson_relay(0)),
             ("poisson Tref3 via relay", lambda: poisson_relay(3)), ("quantize_weights=False", qfalse),
             ("timesteps= keyword", kw), ("unsupported lif_prob", unsupported), ("rerun same net", rerun),
             ("weight 40 on lif (max 15)", weight_clip), ("chip-only kwargs", ignored_kwargs)]:
    case(n, f)
