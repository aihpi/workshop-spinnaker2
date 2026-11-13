# Troubleshooting SpiNNaker2 runs on the cluster

Failure modes seen between May and August 2026 while bringing the frame up, and what they turned out to mean. Setup instructions are in [README.md](README.md).

## Contents

- [1. Normal behaviour that looks like a fault](#1-normal-behaviour-that-looks-like-a-fault)
- [2. Allocation failures](#2-allocation-failures)
- [3. Import and library errors](#3-import-and-library-errors)
- [4. Mapping limits](#4-mapping-limits)
- [5. Diagnostic techniques on cx51](#5-diagnostic-techniques-on-cx51)

## 1. Normal behaviour that looks like a fault

**Boards do not answer pings.** The boards are powered off whenever no job runs. Only the frame controller is always on. An unreachable board between runs says nothing about its health.

**No SCAMP process anywhere.** SCAMP is the monitor firmware of the chips and is not persistent. The chips come up blank after power-on, and the host uploads and starts SCAMP at the beginning of a session (`SpinnmanSession(load_scamp=True)`, the default); it disappears when the board powers down. It never appears as a process on the host either. The only observable trace during a session is that the board answers SCP requests.

**148 instead of 152 cores per chip.** SCAMP occupies one quad of cores, and the whole quad is excluded from the application cores. A 48-chip board therefore reports 7104 usable cores, which is where a line such as `Used 2 out of 7104` comes from.

**Only one or two boards power up during a run.** Boards are tried in order and the search stops at the first success. All six powering up means every attempt failed.

## 2. Allocation failures

### `Eth chip init failed during allocation`

The historical headline failure, seen on every run from May to July 2026. It resolves to a simple reachability check: the host pings the board and the board does not answer.

Root cause, found 2026-07-07 and fixed 2026-07-16: **the Ethernet cables of the boards were physically missing.** The boards booted, reported a healthy network interface, and were nevertheless absent from the network.

The decisive measurement was an ARP watcher. While each board was powered and booted, the network was asked once per second who holds the board's address. The frame controller answered throughout, proving the measurement worked; no board answered once, across three runs. Answering ARP is a reflex of any connected port and does not depend on addresses, routes or gateways, which also explains why an earlier gateway correction changed nothing.

The lesson generalises: when a board claims a healthy interface but is unreachable, the question is whether its port is connected at all, and that can only be answered from the switch or the cable, not from the host configuration.

### Intermittent allocation, boards ready just after the timeout

After the cabling fix, allocation succeeded only sometimes. The boards became reachable one to three seconds after the library had already given up waiting. Fixed upstream in SpiNNMan2 (vendor ticket COMP-588), released in SpiNNMan2 v0.2.4, which py-spinnaker2 v0.8.0 pins. The pinned commit in [README.md](README.md) contains the fix; older environments do not.

## 3. Import and library errors

**`ImportError` on `from spinnaker2 import snn`.** A circular import in v0.8.0 when `snn` is the first import of a session. Reported to the vendor and fixed in v0.8.1. On an affected version, importing `spinnaker2.hardware` first is the workaround. This hits the first cell of the vendor tutorial notebooks.

**Build fails on a fresh clone.** Two causes: `cmake` missing (cx51 has it system-wide since at least November 2026), or a clone without `--recursive`, which leaves the `snn-core` submodule empty. The submodule was private until August 2026 and is now public.

**`SpinnmanInvalidParameterException: … s2app.mem … doesn't exist`.** The chip program for this network isn't in the user's cache (`~/.cache/py-spinnaker2/apps/`), and rebuilding is switched off with `backend_settings.set_rebuild_apps(False)`. py-spinnaker2 compiles a separate variant, e.g. for networks spread over several chips ("Using multi-chip settings requires a re-build of the application binaries"), so a new kind of network can need a program that was never built. Fix: leave rebuilding on (the default). Switching it off only avoids the collision of two runs started at the same time by the same user, which compile into the same build folder (seen on 2026-11-09).

## 4. Mapping limits

- Up to v0.8.0, a `Hardware` object runs **once**: a second `run()` on the same object fails, and network names must be unique within a session (`snn.Network.clear_names()` as workaround). Fixed in v0.8.1; the pinned v0.8.2 allows both. The tutorial copies in `_local/04_spinncloud_tutorials/` still contain the old workarounds, which are harmless.
- In the synfire chain of tutorial 00 (`lif_curr_exp`, 60 inputs per neuron, `v` and spikes recorded) at most **100** neurons fit on one core, not the 125 that the memory budget suggests. The limit depends on connectivity and recording; it is not a general cap for the model (documented cap: 256).
- `mapping_only=True` performs placement and routing without touching the hardware, which makes network sizes testable without an allocated board.

## 5. Diagnostic techniques on cx51

- Unprivileged `tcpdump` is blocked; `arping` works without privileges.
- The ARP table via `ip neigh` was the decisive diagnostic: an `lladdr` entry means the device answered, `INCOMPLETE` or `FAILED` means it stayed silent.
- The frame controller is a useful positive control. It is always on, so it must appear in the ARP table; if it does not, the measurement itself is broken.
- Figures must be written with `fig.savefig(...)`; `plt.show()` produces no visible output.
