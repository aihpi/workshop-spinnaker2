"""Pilot: one almost empty network, 20 s, power recorded. Shows what the power data looks like."""
import shutil
import pandas as pd
from spinnaker2 import snn, hardware
from spinnaker2.tools import diagnostic_folder_utils as dfu

dfu.set_level("persistent")
net = snn.Network("pilot")
net.add(snn.Population(size=1, neuron_model="lif", params={"threshold": 1.0}, name="idle", record=[]))
hardware.SpiNNcloud48NodeBoard().run(net, 20000, record_power=True)
folder = dfu.get_path()
df = pd.read_parquet(folder / "power.parquet")
print("FOLDER", folder)
print("COLUMNS", list(df.columns))
print(df.head(8).to_string())
print(df[df["marker"].notna()].to_string())
print("N samples", df["total"].notna().sum())
shutil.copy(folder / "power.parquet", "data/pilot.parquet")
