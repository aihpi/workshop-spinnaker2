# Participant access to the SpiNNaker2 boards

- **Decision** (meeting with the cluster admins, 2026-11-04):
    - HPI participants run their code on cx51 (option A); they get access to the `pot-hpi-early-access` partition for the duration of the workshop
    - outside participants get no access to cx51; they use the Brian2 simulator (option B)

## How access works today

```
laptop ──VPN──> login node ──ssh / srun──> cx51 ──private network──> 6 boards
```

- **Only cx51 reaches the boards**, over two paths (`03_setup/README.md`):
    - power and boot commands: cx51 → frame controller → boards
    - application data (program, simulation, results): cx51 → board directly
- **The board locks only work on cx51.**
    - A run reserves a board via a lock file in `/mnt/spinnaker/locks`, on cx51's local disk.
    - A run from another machine doesn't see these locks: it could take a busy board and, at its end, switch that board off during someone else's run (py-spinnaker2 powers boards off after each run).
    - Talking to the frame controller (`STM_<address>.lock`) is exclusive too: runs take turns for it, about 27 s per run (probably power-up, boot and power-off).
    - Lock = Linux `flock`, held during the run (checked with `lslocks`, 1–8 simultaneous runs, 2026-11-04).

## Options

| Option | Participants need | Admin effort | Assessment |
|---|---|---|---|
| **A. Log in to cx51** (ssh, VS Code, Jupyter) | account, VPN, partition access | accounts, permissions | **recommended** for HPI participants |
| **B. Brian2 on the laptop**, chip runs by the instructor | Python | none | **recommended** for outside participants; also saves chip time |
| **C. JupyterHub on cx51** | browser (+ VPN?) | higher, one-time | most convenient, if feasible in two weeks |
| **D. Laptops connect to the boards via VPN** | route into the board network, full install incl. chip toolchain | high | **ruled out:** board locks only work on cx51 |

## Capacity

- **Boards:** 6, one run per board at a time, even if the network uses one core. Six simultaneous runs got all six boards within 28 s.
- **No sharing of a board:** py-spinnaker2 v0.8 allocates whole boards only (docs, hardware allocation). The vendor's announced plans concern runs across several boards, not several users on one board.
- **Frame controller is the bottleneck:** every run needs 26–29 s of exclusive controller time, in several turns. Six simultaneous runs kept it busy without a break: **about 2 runs per minute** for all participants together.
- **Duration per run** (tiny network): about 60 s alone and 75–77 s with two at once (20 s of simulation each); 166–169 s with six at once (1 s of simulation). The six runs all finished at about the same time, so nobody finishes early.
- **All boards busy:** the run waits for a free board (tested with 8 simultaneous runs) and meanwhile prints a harmless `All machines are busy … Retrying` message.
- **cx51:** 40 CPU cores, 125 GB RAM, enough for the Python side of many sessions.
- **Consequence:**
    - about 90 chip runs per 45-minute hands-on, shared by all participants
    - measured until all results were back: 1 run ≈ 1 min, 2 at once ≈ 1.3 min, 6 at once ≈ 2.8 min, 8 at once ≈ 4.1 min
