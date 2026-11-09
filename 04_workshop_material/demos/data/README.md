# Data of the demos

| File | Content | Source |
|---|---|---|
| `toy5_Q.npy`, `toy8_Q.npy` | QUBO matrices of a 5-node and an 8-node graph for Max-Cut (off-diagonal: edges, diagonal: minus the node degree) | py-spinnaker2 v0.8.2, `tutorials/optimization/max_cut_QUBO/data/maxcut/` |
| `scnn_mnist.nir` | Pretrained convolutional spiking network for NMNIST, as NIR graph | py-spinnaker2 v0.8.2, `examples/nir/` |
| `nmnist/` | NMNIST test set, downloaded by `tonic` on the first run (about 170 MB download, 365 MB on disk); not tracked in git | Orchard et al. 2015, via the `tonic` library |

py-spinnaker2 is by SpiNNcloud, Apache License 2.0, https://gitlab.com/spinnaker2/py-spinnaker2.
