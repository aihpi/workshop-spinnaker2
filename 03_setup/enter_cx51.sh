#!/bin/bash
# Reserve the SpiNNaker2 node cx51 and open a shell on it. Keep this shell open while you work on cx51.
# Usage: bash enter_cx51.sh <your Slurm account>
# Find the account: sacctmgr -n show assoc user=$USER format=account,qos (the one whose QOS list contains early-access)
ACCOUNT="${1:?Usage: bash enter_cx51.sh <your Slurm account>. Find it with: sacctmgr -n show assoc user=\$USER format=account,qos}"
srun -A "$ACCOUNT" --partition=pot-hpi-early-access --qos=early-access --time=06:00:00 --mem=8G --nodelist=cx51 --pty bash
