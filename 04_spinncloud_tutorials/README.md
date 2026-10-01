# SpiNNcloud tutorial notebooks

SpiNNcloud's own `deep_dive` tutorials for py-spinnaker2, run against the frame on cx51 so that the stored outputs come from the hardware rather than the simulator. Kept here because the edits would otherwise be lost on the next update of the vendor clone.

**This is reference material, not workshop material.** It serves to learn the API and to record what actually works on our chips. The workshop's own hands-on parts (referred to as "hands-on 1" and "hands-on 2" in `01_knowledge_base/` and `02_workshop_design/brief.md`) are not written yet and will live elsewhere.

Setup and the pinned library version are in [`../03_setup/README.md`](../03_setup/README.md).

| Notebook | Topic |
|---|---|
| `00_welcome.ipynb` | First spiking network, hardware vs. Brian2 backend |
| `01_core_concepts.ipynb` | Populations, neuron models, parameters |
| `02_connectivity.ipynb` | Projections and connection lists |
| `03_lif_conv2d.ipynb` | Convolutional LIF layers |
| `04_hardware_allocation.ipynb` | Choosing a board, placement across cores |
| `05_debugging.ipynb` | Reading the output when a run misbehaves |

`helpers/` and `images/` hold what these six notebooks import and display. Only the referenced assets were copied; the remaining tutorials (`06`–`09`, streaming, NIR, custom neuron models) stay unmodified in the vendor clone at `py-spinnaker2/tutorials/deep_dive/`.

## What differs from upstream

- `USE_HARDWARE = True`, so the stored outputs are real chip results rather than Brian2 simulations.
- Weights and a few parameters adjusted where the upstream defaults produced no spikes on hardware.
- Outputs kept in the notebooks on purpose: they document what the chip actually returned.
- `04_hardware_allocation.ipynb` has the board address in its output replaced by `<board-ip>`.

Rerunning a notebook needs an allocated board and therefore a session on cx51. The Brian2 fallback works everywhere; flipping `USE_HARDWARE` back to `False` is the one-line change.

## Origin and license

Derived from the `tutorials/deep_dive` notebooks of [py-spinnaker2](https://gitlab.com/spinnaker2/py-spinnaker2) (SpiNNcloud / TU Dresden), licensed under the **Apache License 2.0**. The modifications in this folder are published under the same license; the MIT license of the rest of this repository does not apply to them. A copy of the Apache license ships with the vendor clone as `py-spinnaker2/LICENSE`.
