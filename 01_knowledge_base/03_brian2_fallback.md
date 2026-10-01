# Brian2 Fallback

What the Brian2 backend of py-spinnaker2 can and can't do, and how closely it matches the chip. The fallback for workshop participants without cluster access and for the case that the hardware fails on the day. Builds on the primer (`01_primer_snn_basics.md`) for the neuron models and on `02_hardware_energy.md` for what only the chip provides.

Sources: the py-spinnaker2 v0.8.2 code (`src/spinnaker2/brian2_sim.py`) and docs ([Brian2 backend](https://spinnaker2.gitlab.io/py-spinnaker2/user_guide/brian2.html)), and a comparison run on 2026-10-01: the same small networks on a 48-node board of the HPI cluster and on the Brian2 backend (Brian2 2.10.1) on cx51. The scripts are in `03_setup/compare_brian2_chip.py` and `03_setup/brian2_edge_cases.py`.

## Contents

- [1. What the backend is](#1-what-the-backend-is)
- [2. Supported neuron models](#2-supported-neuron-models)
- [3. Differences from the chip](#3-differences-from-the-chip)
- [4. Which examples run on Brian2](#4-which-examples-run-on-brian2)
- [5. Rules for workshop notebooks](#5-rules-for-workshop-notebooks)
- [To check on the cluster](#to-check-on-the-cluster)

## 1. What the backend is

[Brian2](https://briansimulator.org/) is a simulator for spiking neural networks on the CPU. py-spinnaker2 translates a `snn.Network` into Brian2 objects, runs it, and writes spikes and membrane potentials back into the populations, so the same notebook code reads the results on both paths. Only the backend object changes:

```python
from spinnaker2 import snn, hardware, brian2_sim

USE_HARDWARE = False
hw = hardware.SpiNNcloud48NodeBoard() if USE_HARDWARE else brian2_sim.Brian2Backend()
hw.run(net, 50)   # same call on both backends
```

The snippet in the py-spinnaker2 docs has a typo (`brian2sim.Brian2Backend()` instead of `brian2_sim.Brian2Backend()`) and fails as written.

Properties of the backend (py-spinnaker2, `brian2_sim.py`):

- **Fixed timestep of 1 ms** model time. `sys_tick_in_s` and all other chip options (`record_power`, `mapping_only`, `iterative_mapping`, …) are accepted and silently ignored. The only own option is `quantize_weights` (default `True`).
- **Weights and delays are quantised like on the chip:** truncated toward zero and clipped to the model's range (a weight of 40 on `lif` becomes 15, measured). Delays are floored and clipped.
- **Pure Python code generation** (`numpy` target), no compiler needed. Fast enough for workshop sizes: a 784–128–10 network with 100,000 synapses runs 50 or 500 timesteps in under a second on cx51 (measured). Importing the libraries takes longer: the whole comparison script of section 3 needs 18 s.
- **Repeated runs** on the same backend object work.
- **Recording:** spikes and `v`. `v` is recorded after the reset, as on the chip (primer, section 3).

**Workshop:** the switch is shown once in hands-on 1 (1 min); participants without cluster access set `USE_HARDWARE = False`.

## 2. Supported neuron models

Every model not in the left column raises `ValueError: Unsupported neuron model` when the network is built (py-spinnaker2, `brian2_sim.py`).

| Runs on Brian2 | Chip only |
|---|---|
| `lif`, `lif_no_delay`, `lif_32bit`, `lif_conv2d` | `lif_no_delay_1024` |
| `lif_curr_exp`, `lif_curr_exp_no_delay`, `lif_curr_exp_32bit` | `lif_prob` and its variants |
| `alif`, `alif_no_delay`, `alif_no_delay_1024`, `alif_32bit` | `izhikevich`, `izhikevich_32bit` |
| `spike_list` | `qubo_neuron`, `qubo_neuron_32bit` |
| `poisson_process` (with the limits of section 3) | `spikes_from_array_latency_code`, `conv2d_if_neuron_rate_code`, `charge_and_spike` |
| | `relay`, `spike_replicator`, `spike_receiver`, `gather_and_stream` (routing and streaming) |

The docs' list is shorter than the code's: it omits `alif`, `poisson_process` and `lif_conv2d`, which the code supports.

For the primer this means: Figures 7–13 have a Brian2 counterpart, Figure 17 (rate coding) only without the refractory period `Tref` (section 3); `lif_prob` (Figure 15), `izhikevich` (Figure 14), QUBO (Figure 16) and the built-in latency encoder (Figures 17, 19) need the chip. Latency coding still works on Brian2 if the spike times are computed in Python and fed in with `spike_list`, as in the primer's MNIST snippet (section 6).

## 3. Differences from the chip

Measured on 2026-10-01 with the same networks on both backends (`03_setup/compare_brian2_chip.py`, 60 timesteps).

**Identical spike times and membrane potentials** for: `lif` with reset by subtraction, delays (arrival at `delay + 1`), excitatory and inhibitory weights on the same neuron, `alif` with adaptive threshold and reset to `v_reset`, and a `lif` → `lif` chain of two layers. For `lif` and `alif`, Brian2 integrates $dv/dt = -v/\tau + i_\text{offset}/\Delta t$ with the Euler method and $\tau = \Delta t / (1 - \alpha)$, which gives exactly the chip's update $v \leftarrow \alpha v + i_\text{offset}$ (primer, section 3).

**Differences:**

| Case | Chip | Brian2 | Cause (code) |
|---|---|---|---|
| Input lands exactly on the threshold (weight 1, threshold 1) | spikes | no spike | Brian2 tests `v > threshold`, the chip `v >= threshold` |
| Constant `i_offset` = 0.3 without leak, 60 steps | 18 spikes | 17 spikes | float32 on the chip, float64 in Brian2, plus the strict `>`: the sum reaches 1.0 exactly on the chip, just below or at 1.0 in Brian2 |
| `lif_curr_exp`, neuron driven by input spikes | same spikes | same spikes | — |
| `lif_curr_exp`, neuron driven by `i_offset`, `t_refract` = 3 | spikes at 1, 6, 11, … | spikes at 0, 5, 10, … | Brian2 applies the input current one step late and shifts all output spikes one step back to compensate; for `i_offset` that shift is wrong |
| `lif_curr_exp` → `lif_curr_exp`, second layer | first spike at step 4 | first spike at step 5 | the compensation only shifts the recorded spikes, not the spikes passed on, so each further `lif_curr_exp` layer is one step late |
| `poisson_process` with `Tref` = 3, `p` = 0.2 | 0.125 spikes per step, i.e. $p/(1 + p\,T_\text{ref})$ | 0.201 spikes per step | Brian2 uses a plain `PoissonGroup` and ignores `Tref` |
| Same `seed` | reproducible on the chip | reproducible in Brian2 | different random generators, so the spike trains differ between the backends |

**Errors in the backend** (py-spinnaker2 v0.8.2, reproduced with `03_setup/brian2_edge_cases.py`):

- `record=["spikes"]` on a `poisson_process` population fails with `TypeError: Can only add objects of type BrianObject …`. Workaround: relay the Poisson spikes through a `lif` population (`alpha_decay` 0, threshold 1, weight 2) and record that.
- `quantize_weights=False` fails with `NameError: cannot access free variable 'S_inh'` as soon as a projection has excitatory weights.
- `run(net, timesteps=…)` fails with a `TypeError`, as on the chip (primer, section 7).

**What only the chip provides:** power measurement, profiling, deadline misses, the memory check of the mapping (`MemoryError`), and the placement on PEs. `set_max_atoms_per_core` is ignored. A network that runs on Brian2 can therefore still be too large for the chip; `hw.run(net, T, mapping_only=True)` checks this without running, but needs the chip's software stack.

<details>
<summary><b>The <code>lif_curr_exp</code> shift in detail</b></summary>

<br>

On the chip, the synaptic current of a step enters $v$ in the same step: $I[t] = \alpha_\text{exc} I[t-1] + w$, then $v[t] = \alpha v[t-1] + I[t] + i_\text{offset}$. In Brian2 the current enters one step later, $v[t] = \alpha v[t-1] + I[t-1] + i_\text{offset}$ (py-spinnaker2 docs, Brian2 backend). To make the results match, `brian2_sim.py` subtracts one step from every recorded spike time of a `lif_curr_exp` population and drops the first `v` sample. This is exact for a neuron driven only by input spikes from `spike_list` or `lif`, which is the case the docs describe. It is off by one step when `i_offset` drives the neuron (its effect isn't delayed in Brian2, so the shift moves those spikes too early) and when a `lif_curr_exp` population feeds another one (the spikes passed on are not shifted, so the delay adds up per layer).

</details>

<br>

**Workshop:** not taught. The differences matter for whoever writes the notebooks (section 5) and for participants who compare their Brian2 results with a neighbour's chip results.

## 4. Which examples run on Brian2

From the py-spinnaker2 code and examples (fact-check of 2026-09-30), not yet run here:

- **Run on Brian2:** the clustered SNN example (`lif_curr_exp`, `poisson_process`), the NMNIST NIR demo, tutorial 08 (NIR workflow).
- **Need a board:** the QUBO example (`qubo_neuron`), the end-to-end NIR example (48-node board, 795 cores), the streaming examples.
- The clustered SNN example combines both weak spots of section 3: `poisson_process` input (here without `Tref`, so no difference) and `lif_curr_exp` neurons that fire without input, because their rest lies above the threshold (primer, section 7). Such spikes are shifted like the `i_offset`-driven ones in section 3. On Brian2 its raster can differ in detail from the chip; the switching between clusters should look the same *(assumption, to check)*.

**Workshop:** decides which demos have a fallback; see the demo evaluation in `02_workshop_design/`.

## 5. Rules for workshop notebooks

So that every notebook gives the same result on both paths:

- Use `lif` or `alif` where possible. They match the chip exactly.
- Avoid inputs that land exactly on the threshold; use thresholds that the summed weights don't hit exactly (e.g. 1.5 instead of 1 with integer weights).
- With `lif_curr_exp`: drive neurons with input spikes rather than `i_offset`, and expect one step of extra latency per further `lif_curr_exp` layer on Brian2.
- With `poisson_process`: set `Tref` = 0, and don't record the Poisson population itself.
- Keep `quantize_weights` at its default.
- Develop on Brian2, then check the network once with `mapping_only=True` on the cluster, since Brian2 can't detect a network that is too large.
- Compare spike counts and rates between participants, not exact spike times of stochastic networks.

**Workshop:** guidelines for preparing the notebooks, not taught.

## To check on the cluster

- [ ] Run the clustered SNN example, the NMNIST NIR demo and tutorial 08 on both backends and compare (section 4).
- [ ] How participants without cluster access install the Brian2 path on their laptops: `pip install` of py-spinnaker2 builds the chip libraries, which needs the toolchain; alternatives are installing only the Python dependencies and putting `src/` on the `PYTHONPATH` (worked on macOS in September 2026), or the public Docker image that v0.8.2 introduced *(assumption, to check)*. Needs a tested one-page instruction before the workshop.
- [ ] Report the two errors and the `lif_curr_exp` shift to SpiNNcloud.
