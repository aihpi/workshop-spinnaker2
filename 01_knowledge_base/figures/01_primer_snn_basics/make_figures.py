"""Figures for the primer, sections 2 to 6. Run: uv run --with numpy --with matplotlib --with schemdraw make_figures.py"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent
DT = 0.01  # ms, integration step for all ODEs
BLUE, ORANGE, GREEN, GREY = "#1f77b4", "#ff7f0e", "#2ca02c", "0.5"
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10})


def lif(ri, t_end, tau=10.0, v_th=1.0, v_reset=0.0, t_ref=0.0, t_on=0.0, t_off=np.inf):
    """Euler-integrate tau dV/dt = -V + R I(t) (rest at 0), reset to v_reset at threshold. Returns t, v, spike times."""
    t = np.arange(0, t_end, DT)
    v = np.zeros_like(t)
    spikes, last = [], -np.inf
    for k in range(1, len(t)):
        if t[k] - last < t_ref:
            v[k] = v_reset
            continue
        inp = ri if t_on <= t[k] < t_off else 0.0
        v[k] = v[k - 1] + DT / tau * (-v[k - 1] + inp)
        if v[k] >= v_th:
            spikes.append(t[k])
            last = t[k]
            v[k] = v_reset
    return t, v, np.array(spikes)


def rate_analytic(ri, tau=10.0, v_th=1.0, t_ref=0.0):
    """Firing rate in Hz of the LIF neuron for constant input (0 below the critical input)."""
    ri = np.asarray(ri, dtype=float)
    f = np.zeros_like(ri)
    above = ri > v_th
    f[above] = 1000.0 / (t_ref + tau * np.log(ri[above] / (ri[above] - v_th)))
    return f


def fig_circuit():
    """The membrane as an RC circuit (needs schemdraw)."""
    import schemdraw
    import schemdraw.elements as elm

    with schemdraw.Drawing(file=str(OUT / "02_rc_circuit.png"), show=False, dpi=150) as d:
        d.config(fontsize=12, unit=3)
        src = elm.SourceI().up().length(6).label("input\n$I(t)$", loc="bottom")
        elm.Line().right().length(3).label("inside the cell: $V$", loc="top")
        top = elm.Dot()
        cap = elm.Capacitor().down().length(6).label("$C$", loc="bottom")
        elm.CurrentLabel(top=True, length=1.2, ofst=0.6).at(cap).label("$I_C = C\\,dV/dt$")
        bottom = elm.Dot()
        elm.Line().left().to(src.start).label("outside the cell: 0 V (reference)", loc="bottom")
        elm.Line().right().at(top.center).length(4.5)
        res = elm.Resistor().down().label("$R$", loc="bottom")
        elm.CurrentLabel(top=True, length=1.2, ofst=0.6).at(res).label("$I_L = (V - V_{rest})/R$")
        elm.Battery().down().label("$V_{rest}$", loc="bottom")
        elm.Line().left().to(bottom.center)


def fig_rc():
    fig, (ax_i, ax_v) = plt.subplots(2, 1, figsize=(7, 4), sharex=True, gridspec_kw={"height_ratios": [1, 2.5]})
    t_on, t_off = 10, 70
    t = np.arange(0, 110, DT)
    ax_i.plot(t, np.where((t >= t_on) & (t < t_off), 1, 0), color=GREY)
    ax_i.set_ylabel("input I")
    ax_i.set_yticks([0, 1], ["0", "I₀"])
    for tau, color in [(10, BLUE), (25, ORANGE)]:
        _, v, _ = lif(1.0, 110, tau=tau, v_th=np.inf, t_on=t_on, t_off=t_off)
        ax_v.plot(t, v, color=color, label=f"τ = {tau} ms")
    ax_v.axhline(1, color=GREY, ls=":", lw=1)
    ax_v.text(108, 1.02, "steady state R·I₀", ha="right", va="bottom", color=GREY)
    ax_v.axhline(1 - np.exp(-1), color=BLUE, ls=":", lw=0.8)
    ax_v.plot([t_on + 10] * 2, [0, 1 - np.exp(-1)], color=BLUE, ls=":", lw=0.8)
    ax_v.annotate("after one τ: 63 %", (t_on + 10, 1 - np.exp(-1)), (t_on + 18, 0.35), color=BLUE,
                  arrowprops={"arrowstyle": "->", "color": BLUE})
    ax_v.annotate("charging", (48, 0.15), color=GREY)
    ax_v.annotate("leaking back to rest", (78, 0.75), color=GREY)
    ax_v.set_ylabel("V / (R·I₀)")
    ax_v.set_xlabel("time (ms)")
    ax_v.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "02_rc_charging.png")


def fig_spiking():
    inputs = [(0.9, GREY), (1.2, BLUE), (2.0, ORANGE)]
    fig, axes = plt.subplots(len(inputs), 1, figsize=(7, 5), sharex=True, sharey=True)
    for ax, (ri, color) in zip(axes, inputs):
        t, v, spikes = lif(ri, 100)
        ax.plot(t, v, color=color)
        ax.vlines(spikes, 1, 1.5, color=color, lw=1.5)
        ax.axhline(1, color="k", ls=":", lw=0.8)
        ax.axhline(ri, color=color, ls="--", lw=0.8)
        rate = f"{rate_analytic([ri])[0]:.0f} Hz" if ri > 1 else "no spikes"
        ax.set_title(f"R·I = {ri} × threshold → {rate}", loc="left", fontsize=10, color=color)
        ax.set_ylabel("V (units of\nthreshold)")
    axes[0].text(99, 1.03, "threshold", ha="right", va="bottom", fontsize=8)
    axes[-1].text(99, 2.03, "steady state R·I (never reached)", ha="right", va="bottom", fontsize=8, color=ORANGE)
    axes[-1].set_xlabel("time (ms)")
    axes[-1].set_ylim(0, 2.2)
    fig.tight_layout()
    fig.savefig(OUT / "02_lif_spiking.png")


def fig_fi():
    x = np.linspace(0, 4, 800)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.axvspan(0, 1, color="0.93", zorder=0)
    ax.text(0.5, 200, "no spikes:\nV never\nreaches the\nthreshold", ha="center", fontsize=8, color="0.35")
    ax.axvline(1, color="k", ls=":", lw=0.8)
    ax.text(1.03, 300, "critical input\nR·I = threshold", fontsize=8, va="top")
    ax.plot(x, 100 * np.maximum(0, x - 1), color=GREY, ls="--", lw=1, label="ReLU, for comparison of the shape")
    ax.plot(x, rate_analytic(x), color="k", lw=2, label="LIF neuron (τ = 10 ms)")
    for ri, color in [(0.9, GREY), (1.2, BLUE), (2.0, ORANGE)]:  # the three neurons of Figure 5
        f = rate_analytic([ri])[0]
        ax.plot(ri, f, "o", color=color, ms=8, zorder=5)
        ax.annotate(f"{ri}× threshold: {f:.0f} Hz", (ri, f), (ri - 0.08, f + 22), fontsize=8, color=color, ha="right")
    ax.set_xlabel("input strength R·I, in units of the threshold")
    ax.set_ylabel("firing rate f (spikes per second)")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 330)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "02_fi_curve.png")


def hodgkin_huxley(t_end=100, i_amp=10.0, t_on=10):
    """Classic squid axon parameters, V in mV, I in uA/cm^2."""
    def x_inf_tau(a, b):
        return a / (a + b), 1 / (a + b)

    t = np.arange(0, t_end, DT)
    v = np.full_like(t, -65.0)
    n, m, h = 0.3177, 0.0529, 0.5961
    for k in range(1, len(t)):
        u = v[k - 1]
        an, bn = 0.01 * (u + 55) / (1 - np.exp(-(u + 55) / 10)), 0.125 * np.exp(-(u + 65) / 80)
        am, bm = 0.1 * (u + 40) / (1 - np.exp(-(u + 40) / 10)), 4 * np.exp(-(u + 65) / 18)
        ah, bh = 0.07 * np.exp(-(u + 65) / 20), 1 / (1 + np.exp(-(u + 35) / 10))
        n += DT * (an * (1 - n) - bn * n)
        m += DT * (am * (1 - m) - bm * m)
        h += DT * (ah * (1 - h) - bh * h)
        i_ion = 120 * m**3 * h * (u - 50) + 36 * n**4 * (u + 77) + 0.3 * (u + 54.387)
        v[k] = u + DT * ((i_amp if t[k] >= t_on else 0) - i_ion)
    return t, v


def fitzhugh_nagumo(t_end=100, i_amp=0.5, t_on=10, a=0.7, b=0.8, tau_w=12.5, time_scale=2.5):
    """dv/dt = v - v^3/3 - w + I,  tau_w dw/dt = v + a - b w. time_scale maps model time to ms for plotting."""
    t = np.arange(0, t_end, DT)
    v, w = np.empty_like(t), np.empty_like(t)
    v[0], w[0] = -1.1994, -0.6243  # resting fixed point for I = 0
    dt = DT * time_scale
    for k in range(1, len(t)):
        inp = i_amp if t[k] >= t_on else 0.0
        v[k] = v[k - 1] + dt * (v[k - 1] - v[k - 1] ** 3 / 3 - w[k - 1] + inp)
        w[k] = w[k - 1] + dt / tau_w * (v[k - 1] + a - b * w[k - 1])
    return t, v, w


def upstrokes(t, v):
    """Spike times as the moments of steepest rise (where dV/dt crosses half its maximum)."""
    dv = np.gradient(v, t)
    above = dv >= 0.5 * dv.max()
    return t[1:][above[1:] & ~above[:-1]]


def calibrated_models(t_end=100, t_on=10):
    """HH as reference; FHN time scale and LIF parameters fitted to its first-spike latency and period."""
    t, v_hh = hodgkin_huxley(t_end, t_on=t_on)
    ref = upstrokes(t, v_hh)
    latency, period = ref[0] - t_on, np.diff(ref).mean()
    # FHN: stretch model time so its period matches (period at time_scale 1 measured once, long run)
    t_long, v_long, _ = fitzhugh_nagumo(t_end=400, t_on=0, time_scale=1.0)
    scale = np.diff(upstrokes(t_long, v_long))[1:].mean() / period
    _, v_fhn, _ = fitzhugh_nagumo(t_end, t_on=t_on, time_scale=scale)
    # LIF in mV relative to rest (-65 mV): threshold +10 (-55 mV), reset -10 (-75 mV, like HH's undershoot).
    # Input sets the first-spike latency, the refractory period makes up the rest of HH's long interval.
    tau, v_th, v_reset = 10.0, 10.0, -10.0
    ri = v_th / (1 - np.exp(-latency / tau))
    t_ref = period - tau * np.log((ri - v_reset) / (ri - v_th))
    _, v_lif, spikes = lif(ri, t_end, tau=tau, v_th=v_th, v_reset=v_reset, t_ref=t_ref, t_on=t_on)
    return t, v_hh, v_fhn, v_lif - 65, spikes, ref, t_ref, ri


def fig_models():
    t, v_hh, v_fhn, v_lif, spikes, ref, t_ref, ri = calibrated_models()
    fig, (ax_i, *axes) = plt.subplots(4, 1, figsize=(7, 7), sharex=True, gridspec_kw={"height_ratios": [0.6, 1, 1, 1]})
    for ax in [ax_i, *axes]:
        for s in ref:
            ax.axvline(s, color=GREY, lw=0.6, alpha=0.4)
    ax_i.plot(t, np.where(t >= 10, 1, 0), color="k")
    ax_i.set_yticks([0, 1], ["0", "I₀"])
    ax_i.set_ylim(-0.15, 1.3)
    ax_i.set_ylabel("input\ncurrent")
    ax_i.set_title("Constant input current, switched on at 10 ms", loc="left", fontsize=10)
    ax_i.text(99, 0.45, f"HH: I₀ = 10 µA/cm²   FHN: I₀ = 0.5   LIF: R·I₀ = {ri:.0f} mV", ha="right", fontsize=8)
    axes[0].plot(t, v_hh, color=GREY)
    axes[0].axhline(-55, color="k", ls=":", lw=0.8)
    axes[0].text(99, -52, "soft threshold ≈ −55 mV", ha="right", va="bottom", fontsize=8)
    axes[0].set_title("Hodgkin-Huxley: 4 variables, spike shape from ion channels", loc="left", fontsize=10)
    axes[0].set_ylabel("V (mV)")
    axes[1].plot(t, v_fhn, color=GREEN)
    axes[1].axhline(-1, color="k", ls=":", lw=0.8)
    axes[1].text(1, -0.9, "knee v = −1", ha="left", va="bottom", fontsize=8)
    axes[1].set_title("FitzHugh-Nagumo: 2 variables, time scaled to the same rate", loc="left", fontsize=10)
    axes[1].set_ylabel("v (dimensionless)")
    axes[2].plot(t, v_lif, color=BLUE)
    axes[2].vlines(spikes, -55, -35, color=BLUE, lw=1.5)
    axes[2].axhline(-55, color="k", ls=":", lw=0.8)
    axes[2].text(99, -53, "threshold −55 mV", ha="right", va="bottom", fontsize=8)
    axes[2].annotate(f"held at reset for\n{t_ref:.0f} ms refractory", (20, -75), (24, -48), fontsize=8, color=BLUE,
                     arrowprops={"arrowstyle": "->", "color": BLUE})
    axes[2].set_title("LIF: 1 variable, fitted to HH: spike = threshold crossing", loc="left", fontsize=10)
    axes[2].set_ylabel("V (mV)")
    axes[2].set_ylim(-80, -30)
    axes[2].set_xlabel("time (ms). Grey lines: HH spike upstrokes")
    fig.tight_layout()
    fig.savefig(OUT / "02_models_hh_fhn_lif.png")


def fig_fhn_phase():
    a, b, i_amp = 0.7, 0.8, 0.5
    _, v, w = fitzhugh_nagumo(t_end=300, t_on=0)
    vs = np.linspace(-2.5, 2.5, 300)
    fig, ax = plt.subplots(figsize=(7.5, 5.2))

    def flow(v_, w_):
        return v_ - v_**3 / 3 - w_ + i_amp, (v_ + a - b * w_) / 12.5

    # background: direction of the flow (unit arrows; v is fast, so they are mostly horizontal)
    gv, gw = np.meshgrid(np.linspace(-2.3, 2.3, 16), np.linspace(-1.3, 2.4, 12))
    dv, dw = flow(gv, gw)
    norm = np.hypot(dv, dw * 3)  # stretch w so the small vertical component stays visible
    ax.quiver(gv, gw, dv / norm, dw * 3 / norm, color="0.8", angles="xy", scale=28, width=0.003, zorder=0)
    # on the v-nullcline dv/dt = 0: flow is purely vertical, up where dw/dt > 0
    for v0 in [-2.2, -1.6, -0.3, 0.4, 1.5, 2.15]:
        w0 = v0 - v0**3 / 3 + i_amp
        ax.annotate("", (v0, w0 + 0.3 * np.sign(flow(v0, w0)[1])), (v0, w0),
                    arrowprops={"arrowstyle": "-|>", "color": "0.2", "lw": 1.3})
    # on the w-nullcline dw/dt = 0: flow is purely horizontal, right where dv/dt > 0
    for v0 in [-1.75, -1.3, -0.45, 0.25, 1.1]:
        w0 = (v0 + a) / b
        ax.annotate("", (v0 + 0.3 * np.sign(flow(v0, w0)[0]), w0), (v0, w0),
                    arrowprops={"arrowstyle": "-|>", "color": "0.2", "lw": 1.3})
    ax.plot(vs, vs - vs**3 / 3 + i_amp, color=GREY, label="v-nullcline (cubic): dv/dt = 0, flow vertical")
    ax.plot(vs, (vs + a) / b, color=GREY, ls="--", label="w-nullcline (linear): dw/dt = 0, flow horizontal")
    ax.plot(vs, vs - vs**3 / 3, color=GREY, ls=":", lw=1, label="v-nullcline before the input is switched on (I = 0)")
    ax.annotate("", (1.0, 2 / 3 + i_amp), (1.0, 2 / 3), arrowprops={"arrowstyle": "->", "color": GREY})
    ax.text(0.95, 0.75, "input shifts\nthe cubic up", fontsize=7, color=GREY, ha="right")
    # new fixed point: intersection of the shifted cubic with the line, on the middle branch -> unstable
    roots = np.roots([-1 / 3, 0, 1 - 1 / b, i_amp - a / b])
    v_fp = roots[np.isreal(roots)].real[0]
    ax.plot(v_fp, (v_fp + a) / b, "o", mfc="white", mec="k", ms=6, zorder=5)
    ax.annotate("new fixed point:\nunstable, repels", (v_fp, (v_fp + a) / b), (-0.35, -0.75), fontsize=8,
                arrowprops={"arrowstyle": "->"})
    ax.plot(v[:1500], w[:1500], color=GREEN, lw=0.8, alpha=0.5)
    ax.plot(v[-6000:], w[-6000:], color=GREEN, lw=2, label="trajectory (limit cycle = repeated spiking)")
    cyc_v, cyc_w = v[-6000:], w[-6000:]
    for pv, pw in [(-1.75, 0.6), (0.6, -0.13), (1.8, 0.6), (0.9, 1.39)]:
        k = np.argmin(np.hypot(cyc_v - pv, cyc_w - pw))
        ax.annotate("", (cyc_v[k + 5], cyc_w[k + 5]), (cyc_v[k], cyc_w[k]),
                    arrowprops={"arrowstyle": "-|>,head_width=0.4,head_length=0.8", "color": GREEN, "lw": 0})
    ax.plot(v[0], w[0], "o", color=GREEN)
    ax.annotate("start: resting state for I = 0\n(stable fixed point)", (v[0], w[0]), (-2.45, -1.05), fontsize=8,
                arrowprops={"arrowstyle": "->"})
    arrow = {"arrowstyle": "->"}
    ax.annotate("① slow drift down the left branch\n(≈ LIF charging below threshold)", (-1.85, 0.75), (-2.45, 1.9),
                fontsize=8, arrowprops=arrow)
    ax.annotate("② knee = threshold", (-1, -0.17), (-2.45, -0.3), fontsize=8, arrowprops=arrow)
    ax.annotate("③ fast jump right = spike", (0.5, -0.1), (0.2, 0.35), fontsize=8, arrowprops=arrow)
    ax.annotate("④ slow rise of w = recovery\n(LIF: refractory period)", (1.75, 0.46), (0.9, 2.0), fontsize=8,
                arrowprops=arrow)
    ax.annotate("⑤ fast jump back\n(LIF: reset)", (0, 1.36), (-0.4, 2.2), fontsize=8, arrowprops=arrow)
    ax.set_xlabel("v, membrane potential (dimensionless)")
    ax.set_ylabel("w, recovery variable (dimensionless)")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-1.5, 2.6)
    ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "02_fhn_phase_plane.png")


def chip_lif(steps, alpha, threshold, i_offset=0.0, inputs=None, reset="subtract", v_reset=0.0):
    """py-spinnaker2 `lif` update: v[t] = alpha*v[t-1] + I_syn[t] + i_offset, then threshold and reset."""
    inputs = np.zeros(steps) if inputs is None else inputs
    v, trace, spikes = 0.0, np.zeros(steps), []
    for t in range(steps):
        v = alpha * v + inputs[t] + i_offset
        trace[t] = v  # value before reset, so a crossing is visible
        if v >= threshold:
            spikes.append(t)
            v = v - threshold if reset == "subtract" else v_reset
    return trace, np.array(spikes)


def fig_discrete_update():
    steps, alpha, th, w = 30, 0.8, 10, 4
    t_in = [2, 6, 12, 13, 14, 20, 21, 22, 23]
    inputs = np.zeros(steps)
    inputs[t_in] = w
    trace, spikes = chip_lif(steps, alpha, th, inputs=inputs, reset="reset_to_v_reset")
    fig, (ax_s, ax_v) = plt.subplots(2, 1, figsize=(7, 4.2), sharex=True, gridspec_kw={"height_ratios": [1, 3]})
    ax_s.vlines(t_in, 0, 1, color=GREY, lw=2)
    ax_s.set_yticks([])
    ax_s.set_ylabel("input\nspikes")
    ax_s.set_title(f"input spikes, weight {w} each", loc="left", fontsize=10)
    t = np.arange(steps)
    shown = trace.copy()
    shown[spikes] = 0  # draw the reset: the neuron continues from 0
    ax_v.step(t, shown, where="post", color=BLUE, lw=1, alpha=0.4)
    ax_v.plot(t, trace, "o", color=BLUE, ms=4)
    ax_v.axhline(th, color="k", ls=":", lw=0.8)
    ax_v.text(steps - 0.5, th + 0.3, "threshold", ha="right", fontsize=8)
    ax_v.vlines(spikes, th, th + 4, color=ORANGE, lw=2)
    ax_v.annotate("jump by the weight", (2, 4), (3.2, 7.5), fontsize=8, arrowprops={"arrowstyle": "->"})
    ax_v.annotate(f"decay: × {alpha} per step", (4, 4 * alpha**2), (5, 1.0), fontsize=8, arrowprops={"arrowstyle": "->"})
    ax_v.annotate("inputs close together add up:\nthreshold crossed → spike, reset to 0", (14, trace[14]),
                  (15.2, 12.2), fontsize=8, arrowprops={"arrowstyle": "->"})
    ax_v.set_ylabel("v[t] (dimensionless)")
    ax_v.set_xlabel("timestep t")
    ax_v.set_ylim(0, 15)
    fig.tight_layout()
    fig.savefig(OUT / "03_discrete_update.png")


def fig_alpha():
    steps = np.arange(0, 31)
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    for alpha, color in [(0.5, "#9467bd"), (0.8, BLUE), (0.9, GREEN), (0.95, ORANGE), (1.0, "k")]:
        tau = "∞" if alpha == 1 else f"{-1 / np.log(alpha):.1f}"
        ax.plot(steps, alpha**steps, "o-", color=color, ms=3, lw=1, label=f"alpha_decay = {alpha}  (τ = {tau} steps)")
    ax.axhline(np.exp(-1), color=GREY, ls=":", lw=0.8)
    ax.text(30, np.exp(-1) + 0.02, "1/e: one τ has passed", ha="right", fontsize=8, color=GREY)
    ax.set_xlabel("timesteps after a single input spike")
    ax.set_ylabel("v[t] / v[0]")
    ax.set_ylim(0, 1.08)
    ax.legend(frameon=False, fontsize=8, loc="upper right", bbox_to_anchor=(1, 0.93))
    fig.tight_layout()
    fig.savefig(OUT / "03_alpha_decay.png")


def fig_reset_modes():
    th, i_off, steps = 1.0, 0.3, 30
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(9, 3.6), gridspec_kw={"width_ratios": [1.3, 1]})
    for mode, color, label in [("subtract", BLUE, "reset_by_subtraction"), ("reset_to_v_reset", ORANGE, "reset_to_v_reset (0)")]:
        trace, spikes = chip_lif(steps, 1.0, th, i_offset=i_off, reset=mode)
        ax_a.plot(np.arange(steps), trace, "o-", color=color, ms=3, lw=1, label=f"{label}: {len(spikes)} spikes")
    ax_a.axhline(th, color="k", ls=":", lw=0.8)
    ax_a.set_title(f"A: constant input i_offset = {i_off}, no leak", loc="left", fontsize=10)
    ax_a.set_xlabel("timestep t")
    ax_a.set_ylabel("v[t] before reset\n(units of threshold)")
    ax_a.set_ylim(0, 1.6)
    ax_a.legend(frameon=False, fontsize=8, loc="upper left")
    inp = np.linspace(0.01, 1, 400)
    ax_b.plot(inp, inp / th, color=BLUE, label="reset_by_subtraction")
    ax_b.plot(inp, 1 / np.ceil(th / inp), color=ORANGE, label="reset_to_v_reset")
    ax_b.set_title("B: firing rate vs. input, no leak", loc="left", fontsize=10)
    ax_b.set_xlabel("i_offset (in units of the threshold)")
    ax_b.set_ylabel("spikes per timestep")
    ax_b.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "03_reset_modes.png")


def chip_lif_curr_exp(steps, alpha, exc_decay, inh_decay, inputs):
    """py-spinnaker2 `lif_curr_exp` without threshold: separate decaying excitatory and inhibitory currents feed v."""
    i_exc, i_inh, v = 0.0, 0.0, 0.0
    out = np.zeros((3, steps))
    for t in range(steps):
        i_exc = exc_decay * i_exc + max(inputs[t], 0)
        i_inh = inh_decay * i_inh + max(-inputs[t], 0)
        v = alpha * v + i_exc - i_inh
        out[:, t] = i_exc, i_inh, v
    return out


def fig_delay():
    pre_t, delay = 2, 3
    arrive = pre_t + delay + 1  # py-spinnaker2: effective delay = delay + 1
    steps = 14
    inputs = np.zeros(steps)
    inputs[arrive] = 5
    v, _ = chip_lif(steps, 0.8, 100, inputs=inputs)
    fig, (ax_p, ax_v) = plt.subplots(2, 1, figsize=(7, 3.2), sharex=True, gridspec_kw={"height_ratios": [1, 2]})
    ax_p.vlines([pre_t], 0, 1, color=GREY, lw=3)
    ax_p.set_yticks([])
    ax_p.set_ylabel("spike")
    ax_p.set_title("presynaptic neuron fires", loc="left", fontsize=10)
    ax_v.plot(np.arange(steps), v, "o-", color=BLUE, ms=4, lw=1)
    ax_v.set_title("postsynaptic neuron: v[t]", loc="left", fontsize=10)
    ax_v.annotate("", (arrive, 5.4), (pre_t, 5.4), arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 1.5})
    ax_v.text((pre_t + arrive) / 2, 5.8, f"delay = {delay}  →  arrives after {delay} + 1 = {arrive - pre_t} steps",
              ha="center", fontsize=8, color=ORANGE)
    ax_v.axvline(pre_t, color=GREY, ls=":", lw=0.8)
    ax_v.set_ylim(-0.3, 7.5)
    ax_v.set_ylabel("v[t]\n(dimensionless)")
    ax_v.set_xlabel("timestep t")
    ax_v.set_xticks(range(0, steps, 2))
    fig.tight_layout()
    fig.savefig(OUT / "04_delay.png")


def fig_synapse_types():
    steps, alpha, w = 50, 0.9, 4
    inputs = np.zeros(steps)
    inputs[[5, 20, 22]] = w
    inputs[35] = -w
    fig, axes = plt.subplots(3, 1, figsize=(7, 5.5), sharex=True, gridspec_kw={"height_ratios": [0.7, 1.3, 2]})
    exc, inh = np.where(inputs > 0)[0], np.where(inputs < 0)[0]
    axes[0].vlines(exc, 0, 1, color=GREEN, lw=2, label=f"excitatory, weight +{w}")
    axes[0].vlines(inh, 0, 1, color="#d62728", lw=2, label=f"inhibitory, weight −{w}")
    axes[0].set_yticks([])
    axes[0].set_ylabel("input\nspikes")
    axes[0].set_title("input spikes", loc="left", fontsize=10)
    axes[0].legend(frameon=False, fontsize=8, loc="upper right", ncol=2, bbox_to_anchor=(1, 1.45))
    i_exc, i_inh, v_exp = chip_lif_curr_exp(steps, alpha, 0.7, 0.7, inputs)
    t = np.arange(steps)
    axes[1].plot(t, i_exc, "o-", color=GREEN, ms=3, lw=1, label="I_exc (exc_decay = 0.7)")
    axes[1].plot(t, -i_inh, "o-", color="#d62728", ms=3, lw=1, label="−I_inh (inh_decay = 0.7)")
    axes[1].axhline(0, color="k", lw=0.5)
    axes[1].set_title("lif_curr_exp only: synaptic currents", loc="left", fontsize=10)
    axes[1].set_ylabel("synaptic current\n(dimensionless)")
    axes[1].legend(frameon=False, fontsize=8, loc="upper right")
    v_delta, _ = chip_lif(steps, alpha, 1e9, inputs=inputs)
    axes[2].plot(t, v_delta, "o-", color=BLUE, ms=3, lw=1, label="lif (delta synapse): jumps by the weight")
    axes[2].plot(t, v_exp, "o-", color=ORANGE, ms=3, lw=1, label="lif_curr_exp: smooth rise and fall")
    axes[2].axhline(0, color="k", lw=0.5)
    axes[2].set_title("membrane potential v[t], alpha_decay = 0.9", loc="left", fontsize=10)
    axes[2].set_ylabel("v[t]\n(dimensionless)")
    axes[2].set_xlabel("timestep t")
    axes[2].legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "04_synapse_types.png")


def quantize(w, scale, w_max=15):
    """py-spinnaker2 style: scale, round toward zero, clip to [-w_max, w_max]."""
    return np.clip(np.trunc(w * scale), -w_max, w_max)


def fig_quantization():
    rng = np.random.default_rng(0)
    w = rng.normal(0, 0.1, 5000)
    scale = 15 / np.percentile(np.abs(w), 99)  # 1 % of weights get clipped
    q = quantize(w, scale)
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(9, 3.6))
    x = np.linspace(-0.45, 0.45, 2000)
    ax_a.plot(x, x * scale, color=GREY, ls="--", lw=1, label="exact: w · scale")
    ax_a.plot(x, quantize(x, scale), color=BLUE, lw=1.5, label="on the chip: integer in [−15, 15]")
    ax_a.axhspan(-0.99, 0.99, color=ORANGE, alpha=0.15)
    ax_a.annotate("|w · scale| < 1\n→ weight becomes 0", (0.01, 0), (0.12, -8), fontsize=8, color=ORANGE,
                  arrowprops={"arrowstyle": "->", "color": ORANGE})
    ax_a.annotate("clipped", (0.4, 15), (0.22, 19), fontsize=8, arrowprops={"arrowstyle": "->"})
    ax_a.set_title("A: rounding toward zero and clipping", loc="left", fontsize=10)
    ax_a.set_xlabel("trained weight w (float)")
    ax_a.set_ylabel("weight on the chip (integer)")
    ax_a.set_ylim(-22, 22)
    ax_a.legend(frameon=False, fontsize=8, loc="upper left")
    levels = np.arange(-15, 16)
    # both as fraction of weights per unit of "weight x scale", so bar heights and histogram are comparable
    ax_b.hist(w * scale, bins=np.arange(-25, 25.01, 0.5), density=True, color=GREY, alpha=0.6,
              label="trained weights × scale")
    ax_b.bar(levels, [(q == k).mean() for k in levels], width=0.35, color=BLUE, label="5-bit weights on the chip")
    ax_b.set_title(f"B: 5000 weights, {100 * (q == 0).mean():.0f} % become 0", loc="left", fontsize=10)
    ax_b.set_xlabel("weight × scale (dimensionless)")
    ax_b.set_ylabel("fraction of weights")
    ax_b.legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "04_weight_quantization.png")


def chip_alif(steps, alpha, threshold, i_offset, adp_inc, adp_decay):
    """py-spinnaker2 `alif`: threshold rises by adp_inc per spike and decays by adp_decay. Reset to 0 for clarity."""
    v, adp = 0.0, 0.0
    trace, thr, spikes = np.zeros(steps), np.zeros(steps), []
    for t in range(steps):
        v = alpha * v + i_offset
        adp = adp_decay * adp
        trace[t], thr[t] = v, threshold + adp
        if v >= threshold + adp:
            spikes.append(t)
            adp += adp_inc
            v = 0.0
    return trace, thr, np.array(spikes)


def fig_alif():
    steps, alpha, th, i_off, inc = 120, 0.9, 1.0, 0.25, 0.4
    v_lif, sp_lif = chip_lif(steps, alpha, th, i_offset=i_off, reset="reset_to_v_reset")
    v_alif, thr, sp_alif = chip_alif(steps, alpha, th, i_off, adp_inc=inc, adp_decay=0.97)
    t = np.arange(steps)
    fig, (ax_l, ax_a, ax_i) = plt.subplots(3, 1, figsize=(7, 6.5), sharex=True, gridspec_kw={"height_ratios": [2, 2, 1.6]})
    for ax, v, threshold, spikes, color, name in [(ax_l, v_lif, np.full(steps, th), sp_lif, BLUE, "LIF"),
                                                   (ax_a, v_alif, thr, sp_alif, ORANGE, "ALIF")]:
        ax.plot(t, v, color=color, lw=1, label="v[t]")
        ax.plot(t, threshold, color="k", lw=1.5, label="threshold")
        ax.plot(spikes, v[spikes], "o", color=color, mec="k", ms=6, zorder=5, label="spike (threshold reached)")
        ax.set_ylim(0, 2.8)
        ax.set_ylabel("v[t] (units of\nbase threshold)")
    ax_l.set_title(f"LIF: the threshold is constant → regular firing ({len(sp_lif)} spikes)", loc="left", fontsize=10)
    ax_a.set_title(f"ALIF: the threshold moves → firing slows down ({len(sp_alif)} spikes)", loc="left", fontsize=10)
    ax_l.legend(frameon=False, fontsize=8, loc="upper left", ncol=3)
    k = sp_alif[1]
    ax_a.annotate(f"each spike: threshold jumps by {inc}", (k + 0.5, (thr[k] + thr[k + 1]) / 2), (k - 8, 2.5),
                  fontsize=8, arrowprops={"arrowstyle": "->"})
    k2 = (sp_alif[5] + sp_alif[6]) // 2
    ax_a.annotate("between spikes: threshold decays back towards 1", (k2, thr[k2]), (k2 - 4, 2.5), fontsize=8,
                  arrowprops={"arrowstyle": "->"})
    for spikes, color, name in [(sp_lif, BLUE, "LIF"), (sp_alif, ORANGE, "ALIF")]:
        ax_i.plot(spikes[1:], np.diff(spikes), "o-", color=color, ms=4, lw=1, label=name)
    ax_i.set_title("time between consecutive spikes", loc="left", fontsize=10)
    ax_i.set_ylabel("interval\n(timesteps)")
    ax_i.set_ylim(0, 16)
    ax_i.legend(frameon=False, fontsize=8, loc="lower right")
    ax_i.set_xlabel("timestep t (same constant input for both: i_offset = 0.25, alpha_decay = 0.9)")
    fig.tight_layout()
    fig.savefig(OUT / "05_alif_adaptation.png")


def izhikevich(a, b, c, d, i_amp=10.0, t_end=200, t_on=20, dt=0.25):
    """dv/dt = 0.04 v^2 + 5 v + 140 - u + I, du/dt = a (b v - u); at v >= 30 mV: v <- c, u <- u + d. v in mV, t in ms."""
    t = np.arange(0, t_end, dt)
    v, u = np.full_like(t, -70.0), np.zeros_like(t)  # start at rest
    u[0] = b * v[0]
    for k in range(1, len(t)):
        inp = i_amp if t[k] >= t_on else 0.0
        vk = v[k - 1] + dt * (0.04 * v[k - 1] ** 2 + 5 * v[k - 1] + 140 - u[k - 1] + inp)
        uk = u[k - 1] + dt * a * (b * v[k - 1] - u[k - 1])
        if vk >= 30:
            v[k - 1] = 30  # draw the spike peak
            vk, uk = c, uk + d
        v[k], u[k] = vk, uk
    return t, v


def fig_izhikevich():
    patterns = [("regular spiking", (0.02, 0.2, -65, 8), BLUE), ("intrinsically bursting", (0.02, 0.2, -55, 4), GREEN),
                ("chattering (repeated bursts)", (0.02, 0.2, -50, 2), ORANGE), ("fast spiking", (0.1, 0.2, -65, 2), "#9467bd")]
    fig, axes = plt.subplots(len(patterns), 1, figsize=(7, 6), sharex=True, sharey=True)
    for ax, (name, (a, b, c, d), color) in zip(axes, patterns):
        t, v = izhikevich(a, b, c, d)
        ax.plot(t, v, color=color, lw=0.8)
        ax.set_title(f"{name}:  a = {a}, b = {b}, c = {c}, d = {d}", loc="left", fontsize=9)
        ax.set_ylabel("v (mV)")
    axes[-1].set_xlabel("time (ms), constant input I = 10 switched on at 20 ms")
    fig.tight_layout()
    fig.savefig(OUT / "05_izhikevich_patterns.png")


def chip_lif_prob(steps, alpha, threshold, i_offset, p, rng):
    """`lif_prob` as assumed here: above threshold the neuron fires with probability p (then reset to 0),
    otherwise v keeps integrating. What the chip does without a spike is still to be checked."""
    v, trace, spikes = 0.0, np.zeros(steps), []
    for t in range(steps):
        v = alpha * v + i_offset
        trace[t] = v
        if v >= threshold and rng.random() < p:
            spikes.append(t)
            v = 0.0
    return trace, np.array(spikes)


def fig_lif_prob():
    steps, alpha, th, i_off, p, trials = 80, 0.9, 1.0, 0.25, 0.3, 15
    rng = np.random.default_rng(1)
    t = np.arange(steps)
    v_det, sp_det = chip_lif(steps, alpha, th, i_offset=i_off, reset="reset_to_v_reset")
    runs = [chip_lif_prob(steps, alpha, th, i_off, p, rng) for _ in range(trials)]
    v_prob, sp_prob = runs[0]  # the trial shown in panel A is also trial 1 in panel C
    fig, (ax_v, ax_d, ax_p) = plt.subplots(3, 1, figsize=(7, 6.5), sharex=True, gridspec_kw={"height_ratios": [1.8, 1, 1.6]})
    ax_v.plot(t, v_det, color=BLUE, lw=1, label="lif")
    ax_v.plot(sp_det, v_det[sp_det], "o", color=BLUE, mec="k", ms=5, zorder=5)
    ax_v.plot(t, v_prob, color=ORANGE, lw=1, label=f"lif_prob (firing_prob = {p})")
    ax_v.plot(sp_prob, v_prob[sp_prob], "o", color=ORANGE, mec="k", ms=6, zorder=5)
    ax_v.axhline(th, color="k", lw=1.2, label="threshold")
    ax_v.set_title("A: one trial of each, circles = spikes", loc="left", fontsize=10)
    ax_v.set_ylabel("v[t] (units of\nthreshold)")
    ax_v.legend(frameon=False, fontsize=8, loc="upper left", ncol=3)
    ax_v.set_ylim(0, 2.6)
    for k in range(trials):
        row = k  # trial 1 at the bottom
        ax_d.vlines(sp_det, row, row + 0.8, color=BLUE, lw=1.2)
        ax_p.vlines(runs[k][1], row, row + 0.8, color=ORANGE, lw=2.2 if k == 0 else 1.2)
    ax_p.text(steps + 0.5, 0.4, "← trial\n    in A", fontsize=7, va="center")
    ax_d.set_title(f"B: lif, {trials} repetitions: identical every time", loc="left", fontsize=10)
    ax_p.set_title(f"C: lif_prob, {trials} repetitions: new random numbers, different spike times", loc="left", fontsize=10)
    for ax in (ax_d, ax_p):
        ax.set_ylabel("trial\n(repetition)")
        ax.set_yticks([0.4, trials - 0.6], ["1", str(trials)])
    ax_p.set_xlabel("timestep t (same constant input in every trial: i_offset = 0.25, alpha_decay = 0.9)")
    fig.tight_layout()
    fig.savefig(OUT / "05_lif_prob.png")


def maxcut_graph():
    """Small example graph: 8 nodes on a ring plus chords. The chords create triangles, so not every edge can be cut."""
    n = 8
    return n, [(i, (i + 1) % n) for i in range(n)] + [(0, 2), (1, 5), (3, 6), (4, 7), (2, 5)]


def cut_size(x, edges):
    return sum(x[i] != x[j] for i, j in edges)


def qubo_dynamics(n, edges, steps=400, alpha=1.0, seed=3):
    """Principle of the `qubo_neuron`: v[t] = alpha v - 0.1 I_syn - 0.15 v (v^2 - 1) + noise.
    Simplified: I_syn is the sum of the neighbours' v (continuous), the noise is annealed from strong to weak."""
    rng = np.random.default_rng(seed)
    adj = np.zeros((n, n))
    for i, j in edges:
        adj[i, j] = adj[j, i] = 1
    v = rng.normal(0, 0.05, n)
    vs, cuts = np.zeros((steps, n)), np.zeros(steps)
    for t in range(steps):
        sigma = 0.25 * (1 - t / steps) + 0.01
        v = alpha * v - 0.1 * adj @ v - 0.15 * v * (v**2 - 1) + rng.normal(0, sigma, n)
        vs[t], cuts[t] = v, cut_size(v > 0, edges)
    return vs, cuts


def fig_qubo():
    n, edges = maxcut_graph()
    best = max(cut_size([(k >> i) & 1 for i in range(n)], edges) for k in range(2**n))
    vs, cuts = qubo_dynamics(n, edges)
    fig = plt.figure(figsize=(9.5, 5.5))
    gs = fig.add_gridspec(2, 2)
    ax_w, ax_v, ax_c, ax_g = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])
    x = np.linspace(-1.6, 1.6, 200)
    ax_w.plot(x, 0.15 * (x**4 / 4 - x**2 / 2), color="k")
    ax_w.set_title("A: two stable states per neuron", loc="left", fontsize=10)
    ax_w.set_xlabel("v (dimensionless)")
    ax_w.set_ylabel("U(v), potential of the\nterm −0.15 v (v² − 1)")
    ax_w.text(-1, 0.002, "group 0\n(orange)", ha="center", fontsize=8, color=ORANGE)
    ax_w.text(1, 0.002, "group 1\n(blue)", ha="center", fontsize=8, color=BLUE)
    t = np.arange(len(cuts))
    for i in range(n):
        ax_v.plot(t, vs[:, i], lw=0.8, color=BLUE if vs[-1, i] > 0 else ORANGE)
    ax_v.set_title("B: each neuron settles into one well", loc="left", fontsize=10)
    ax_v.set_xlabel("timestep t (colour = final group)")
    ax_v.set_ylabel("v[t] (dimensionless)")
    ax_c.plot(t, cuts, color="k", lw=1)
    ax_c.axhline(best, color=GREEN, ls="--", lw=1)
    ax_c.text(len(t) - 1, best - 0.4, f"best possible cut: {best} of {len(edges)} edges", ha="right", va="top", fontsize=8,
              color=GREEN)
    ax_c.set_title("C: edges between the two groups (cut edges)", loc="left", fontsize=10)
    ax_c.set_ylabel("number of\ncut edges")
    ax_c.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax_c.set_xlabel("timestep t (noise decreases over time)")
    ax_c.set_ylim(0, len(edges) + 1)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pos = np.c_[np.cos(ang), np.sin(ang)]
    final = vs[-1] > 0
    for i, j in edges:
        cut = final[i] != final[j]
        ax_g.plot(*pos[[i, j]].T, color=GREEN if cut else "0.75", lw=2 if cut else 1, ls="-" if cut else ":")
    ax_g.scatter(*pos.T, s=180, c=[BLUE if f else ORANGE for f in final], edgecolors="k", zorder=3)
    ax_g.set_title("D: final groups, green edges are cut,\ndotted grey edges are not", loc="left", fontsize=10)
    ax_g.set_aspect("equal")
    ax_g.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / "05_qubo_maxcut.png")


def poisson_spikes(p, steps, rng, t_ref=3):
    """`poisson_process`: spike with probability p per step, then silent for t_ref steps (default Tref = 3)."""
    spikes, last = [], -np.inf
    for t in range(steps):
        if t - last > t_ref and rng.random() < p:
            spikes.append(t)
            last = t
    return np.array(spikes)


def latency_spike(x, x_max, t_max):
    """`spikes_from_array_latency_code`: t = t_max (x_max - x) / x_max, one spike per input.
    Rounded down to a whole timestep (how the chip rounds is still to be checked)."""
    return int(t_max * (x_max - x) / x_max)


def fig_coding():
    values = np.array([1.0, 0.75, 0.5, 0.25, 0.1])
    steps, p_max, t_max, t_ref = 60, 0.25, 50, 3
    rng = np.random.default_rng(2)
    rows = np.arange(len(values))[::-1]
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 5.6), gridspec_kw={"width_ratios": [0.8, 2.2, 0.9]})
    spikes = {"rate": [poisson_spikes(p_max * x, steps, rng, t_ref=t_ref) for x in values],
              "latency": [np.array([latency_spike(x, 1.0, t_max)]) for x in values]}
    # decoding: invert the encoders
    r = np.array([len(sp) / steps for sp in spikes["rate"]])  # measured rate per step
    decoded = {"rate": r / (1 - t_ref * r) / p_max,  # rate with refractory period: r = p / (1 + t_ref p)
               "latency": np.array([1 - sp[0] / t_max for sp in spikes["latency"]])}
    for row_axes, name, color, how, rule in [
            (axes[0], "rate", BLUE, f"spike with probability p = {p_max} · x per step", "count spikes"),
            (axes[1], "latency", ORANGE, f"one spike at t = t_max (1 − x), t_max = {t_max}", "x = 1 − t / t_max")]:
        ax_in, ax_sp, ax_out = row_axes
        ax_in.barh(rows, values, color=GREY, height=0.6)
        ax_in.set_yticks(rows, [f"neuron {k + 1}" for k in range(len(values))])
        ax_in.set_xlim(0, 1.25)
        ax_in.set_xlabel("input value x\n(dimensionless)")
        for sp, row in zip(spikes[name], rows):
            ax_sp.vlines(sp, row - 0.3, row + 0.3, color=color, lw=1.8)
        n = sum(len(sp) for sp in spikes[name])
        ax_sp.set_yticks(rows, [])
        ax_sp.set_ylim(rows.min() - 0.6, rows.max() + 0.6)
        ax_sp.set_xlim(-1, steps)
        ax_sp.set_xlabel(f"timestep t ({how})")
        ax_sp.set_title(f"{name} coding: {n} spikes in total", loc="left", fontsize=10, color=color)
        ax_out.barh(rows, decoded[name], color=color, height=0.6, alpha=0.8, label="decoded")
        ax_out.plot(values, rows, "|", color="k", ms=16, mew=2, label="true input")
        ax_out.set_yticks(rows, [])
        ax_out.set_xlim(0, 1.25)
        ax_out.set_xlabel(f"decoded value (dimensionless)\n{rule}")
        ax_out.legend(frameon=False, fontsize=7, loc="lower right")
    for ax, title in zip(axes[0], ["① input", "② encoded as spikes", "③ read back from the spikes"]):
        ax.annotate(title, (0, 1.22), xycoords="axes fraction", fontsize=11, fontweight="bold")
    fig.tight_layout(h_pad=2.5)
    for row in (0, 1):  # arrows between the columns
        for a, b in [(0, 1), (1, 2)]:
            x0 = axes[row][a].get_position().x1
            x1 = axes[row][b].get_position().x0
            y = axes[row][a].get_position().y0 + axes[row][a].get_position().height / 2
            fig.patches.append(plt.matplotlib.patches.FancyArrowPatch((x0 + 0.005, y), (x1 - 0.005, y),
                               transform=fig.transFigure, arrowstyle="-|>", mutation_scale=15, color="0.4"))
    fig.savefig(OUT / "06_rate_vs_latency.png")


def fig_rate_precision():
    rng = np.random.default_rng(4)
    windows = np.array([10, 20, 50, 100, 200, 500, 1000, 2000])
    p_true, reps = 0.1, 300
    errs = []
    for n in windows:
        counts = np.array([len(poisson_spikes(p_true, n, rng, t_ref=0)) for _ in range(reps)])
        errs.append(100 * counts.std() / counts.mean())
    fig, ax = plt.subplots(figsize=(6.8, 4))
    n_fine = np.logspace(1, np.log10(2000), 200)
    ax.plot(n_fine, 100 * np.sqrt((1 - p_true) / (p_true * n_fine)), color=GREY, ls="--", lw=1,
            label="theory: √((1 − p) / (p · N))")
    ax.plot(windows, errs, "o", color=BLUE, ms=6, label=f"simulation ({reps} repetitions per N)")
    for n, dy in [(100, 1.15), (1000, 1.15)]:
        e = 100 * np.sqrt((1 - p_true) / (p_true * n))
        ax.plot([n, n], [3, e], color=ORANGE, lw=0.8, ls=":")
        ax.plot([8, n], [e, e], color=ORANGE, lw=0.8, ls=":")
        ax.text(n * 1.08, e * dy, f"N = {n}: ≈ {e:.0f} % error", fontsize=8, color=ORANGE)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ticks = [5, 10, 20, 50, 100]
    ax.set_yticks(ticks, [f"{t} %" for t in ticks])
    ax.set_xticks([10, 100, 1000], ["10", "100", "1000"])
    ax.set_xlim(8, 2500)
    ax.set_ylim(3, 130)
    ax.set_xlabel("counting window N (timesteps)")
    ax.set_ylabel("relative error of the value\nread from the spike count")
    ax.set_title(f"How precisely can a rate-coded value be read? (spike probability p = {p_true} per step)",
                 loc="left", fontsize=9)
    top = ax.secondary_xaxis("top", functions=(lambda n: p_true * n, lambda k: k / p_true))
    top.set_xlabel("expected number of spikes (p · N)", fontsize=8)
    top.set_xticks([1, 10, 100], ["1", "10", "100"])
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "06_rate_precision.png")


def mnist_digit():
    """First image of the MNIST test set (a 7), 28 x 28 pixels with values 0-255.
    MNIST: Y. LeCun, C. Cortes, C. J. C. Burges, http://yann.lecun.com/exdb/mnist/ (CC BY-SA 3.0)."""
    return np.load(OUT / "06_mnist_test0_digit7.npy")


def mnist_to_spike_list(img, t_max=50):
    """Latency coding on the host: one spike per non-zero pixel, brighter = earlier. Neuron index = 28 * row + column."""
    return {i: [latency_spike(v, 255, t_max)] for i, v in enumerate(img.flatten().astype(float)) if v > 0}


def fig_mnist():
    img = mnist_digit()
    t_max, steps, p_max = 50, 50, 0.25
    lat = mnist_to_spike_list(img, t_max)
    rng = np.random.default_rng(5)
    rate = {i: poisson_spikes(p_max * v / 255, steps, rng) for i, v in enumerate(img.flatten().astype(float)) if v > 0}
    # example pixel: the active pixel whose spike time is closest to the middle of the window
    ex = min(lat, key=lambda i: abs(lat[i][0] - t_max / 2))
    ex_r, ex_c = divmod(ex, 28)
    RED = "#d62728"
    fig = plt.figure(figsize=(10.5, 7.5))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15])
    ax_img, ax_t, ax_l, ax_r = (fig.add_subplot(gs[k]) for k in [(0, 0), (0, 1), (1, 0), (1, 1)])
    im = ax_img.imshow(img, cmap="gray", vmin=0, vmax=255)  # MNIST convention: 0 = black background, 255 = white stroke
    ax_img.set_title("A: MNIST digit, 28 × 28 pixels", loc="left", fontsize=10)
    fig.colorbar(im, ax=ax_img, label="pixel value (0–255)", shrink=0.85)
    t_map = np.full(img.shape, np.nan)
    for i, (t,) in lat.items():
        t_map.flat[i] = t
    ax_t.set_facecolor("0.8")  # pixels without a spike
    im2 = ax_t.imshow(t_map, cmap="viridis", vmin=0, vmax=t_max)
    ax_t.set_title("B: latency coding, spike time of each pixel", loc="left", fontsize=10)
    fig.colorbar(im2, ax=ax_t, label="spike time (timestep)\ngrey = no spike (pixel value 0)", shrink=0.85)
    for ax in (ax_img, ax_t):
        ax.add_patch(plt.Rectangle((ex_c - 0.5, ex_r - 0.5), 1, 1, fill=False, ec=RED, lw=2))
        ax.set_xlabel("pixel column")
        ax.set_ylabel("pixel row")
    box = {"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.9}
    ax_img.annotate(f"example pixel\nrow {ex_r}, column {ex_c}\nvalue {img[ex_r, ex_c]}", (ex_c + 0.6, ex_r),
                    (17.5, 24), fontsize=8, color=RED, bbox=box, arrowprops={"arrowstyle": "->", "color": RED})
    ax_l.plot([t for (t,) in lat.values()], list(lat.keys()), "|", color=ORANGE, ms=6, mew=1.5)
    ax_l.plot(lat[ex], [ex], "o", mfc="none", mec=RED, ms=10, mew=2)
    ax_l.annotate(f"neuron 28 · {ex_r} + {ex_c} = {ex}\nspikes at t = {lat[ex][0]}", (lat[ex][0], ex), (lat[ex][0] + 4, ex + 190),
                  fontsize=8, color=RED, bbox=box, arrowprops={"arrowstyle": "->", "color": RED})
    ax_l.set_title(f"C: latency coding, {len(lat)} spikes", loc="left", fontsize=10)
    # zoom on the image row of the example pixel: all 28 neurons of that row, most of them silent
    lo, hi = 28 * ex_r, 28 * ex_r + 27
    ins = ax_l.inset_axes([0.46, 0.77, 0.51, 0.12])  # fits into the silent region (neurons 0-190)
    for i in range(lo, hi + 1):
        ins.axhline(i, color="0.9", lw=0.6, zorder=0)
    row_sp = {i: t for i, t in lat.items() if lo <= i <= hi}
    ins.plot([t for (t,) in row_sp.values()], list(row_sp.keys()), "|", color=ORANGE, ms=7, mew=2)
    ins.plot(lat[ex], [ex], "o", mfc="none", mec=RED, ms=8, mew=1.5)
    ins.set_xlim(-1, steps + 1)
    ins.set_ylim(hi + 0.5, lo - 0.5)
    ins.set_yticks([lo, ex, hi], [f"{lo} (col 0)", f"{ex} (col {ex_c})", f"{hi} (col 27)"], fontsize=6)
    ins.tick_params(axis="x", labelsize=6, top=True, labeltop=True, bottom=False, labelbottom=False)
    ins.set_xlabel(f"zoom on image row {ex_r}: timestep t, only {len(row_sp)} of its 28 neurons fire", fontsize=6.5)
    ins.xaxis.set_label_position("top")
    ins.set_ylabel("neuron", fontsize=6)
    ax_l.indicate_inset_zoom(ins, edgecolor="0.3")
    n_rate = 0
    for i, sp in rate.items():
        ax_r.plot(sp, np.full(len(sp), i), "|", color=BLUE, ms=6, mew=1.2)
        n_rate += len(sp)
    ax_r.plot(rate[ex], np.full(len(rate[ex]), ex), "|", color=RED, ms=9, mew=2.5, zorder=5)
    ax_r.set_title(f"D: rate coding (p = {p_max} · x / 255), {n_rate} spikes", loc="left", fontsize=10)
    ax_r.annotate(f"neuron {ex}: {len(rate[ex])} spikes", (rate[ex][-1], ex), (rate[ex][-1] - 22, ex + 190), fontsize=8,
                  color=RED, bbox=box, arrowprops={"arrowstyle": "->", "color": RED})
    for ax in (ax_l, ax_r):
        ax.set_xlim(-1, steps + 1)
        ax.set_ylim(783, 0)  # neuron 0 = top-left pixel at the top, like the image
        ax.set_xlabel("timestep t")
        ax.set_ylabel("input neuron i\n(i = 28 · row + column)")
        rows = ax.secondary_yaxis("right", functions=(lambda i: i / 28, lambda r: r * 28))
        rows.set_ylabel("pixel row")
        rows.set_yticks([0, 5, 10, 15, 20, 25])
    fig.tight_layout()
    fig.savefig(OUT / "06_mnist_encoding.png")


def check():
    """Simulated LIF rates match the analytic formula used in the primer."""
    for ri in [1.2, 2.0, 3.0]:
        _, _, spikes = lif(ri, 1000)
        sim = 1000.0 / np.diff(spikes).mean()
        assert abs(sim - rate_analytic([ri])[0]) / sim < 0.01, (ri, sim)
    _, _, spikes = lif(0.9, 1000)
    assert len(spikes) == 0
    # calibrated LIF fires within 0.3 ms of every HH spike
    *_, spikes, ref, _, _ = calibrated_models()
    assert len(spikes) == len(ref) and np.abs(spikes - ref).max() < 0.3, (spikes, ref)
    # chip update without leak: subtraction gives rate = input / threshold, reset to 0 gives 1 / ceil(threshold / input)
    for i_off in [0.3, 0.45, 0.7]:
        _, sp = chip_lif(10_000, 1.0, 1.0, i_offset=i_off, reset="subtract")
        assert abs(len(sp) / 10_000 - i_off) < 1e-3, i_off
        _, sp = chip_lif(10_000, 1.0, 1.0, i_offset=i_off, reset="reset_to_v_reset")
        assert abs(len(sp) / 10_000 - 1 / np.ceil(1 / i_off)) < 1e-3, i_off
    # quantisation: round toward zero, then clip
    # ALIF: adaptation makes inter-spike intervals grow
    _, _, sp = chip_alif(120, 0.9, 1.0, 0.25, 0.4, 0.97)
    assert np.diff(sp)[-1] > np.diff(sp)[0]
    # QUBO illustration reaches the optimal cut of the example graph
    n, edges = maxcut_graph()
    best = max(cut_size([(k >> i) & 1 for i in range(n)], edges) for k in range(2**n))
    assert qubo_dynamics(n, edges)[1][-1] == best
    # Poisson source without refractory period fires with rate p, latency code maps x_max to t = 0
    rng = np.random.default_rng(0)
    assert abs(len(poisson_spikes(0.2, 50_000, rng, t_ref=0)) / 50_000 - 0.2) < 0.01
    assert latency_spike(1.0, 1.0, 50) == 0 and latency_spike(0.5, 1.0, 50) == 25
    # MNIST example: one latency spike per non-zero pixel, brightest pixels at t = 0
    lat = mnist_to_spike_list(mnist_digit())
    assert len(lat) == (mnist_digit() > 0).sum() == 116 and min(t for (t,) in lat.values()) == 0
    assert list(quantize(np.array([0.9, -0.9, 1.7, -1.7, 20, -20]), 1.0)) == [0, 0, 1, -1, 15, -15]


if __name__ == "__main__":
    check()
    fig_circuit()
    fig_rc()
    fig_spiking()
    fig_fi()
    fig_models()
    fig_fhn_phase()
    fig_discrete_update()
    fig_alpha()
    fig_reset_modes()
    fig_delay()
    fig_synapse_types()
    fig_quantization()
    fig_alif()
    fig_izhikevich()
    fig_lif_prob()
    fig_qubo()
    fig_coding()
    fig_rate_precision()
    fig_mnist()
