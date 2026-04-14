#!/usr/bin/env python3

import argparse
import re
import matplotlib.pyplot as plt
import numpy as np

def parse_file(filename):
    """
    Parses lines like:
    Cyc1 bg Layer 0: RMSE = 1.23

    Returns:
        cycles: ordered list of cycle names (e.g., ["Cyc1", "Cyc2", ...])
        data: dict[layer][type] = list of RMSE values
              type = 'bg' or 'an'
    """
    data = {}
    cycles = []
    seen_cycles = set()

    with open(filename, "r") as f:
        for line in f:
            m = re.search(
                r"(cyc\d+)\s+(bg|an)\s+Layer\s+(\d+):\s+RMSE\s*=\s*([0-9.eE+-]+)",
                line, re.IGNORECASE
            )
            if not m:
                continue
            cyc, typ, layer, val = m.groups()
            layer = int(layer)
            val = float(val)

            if cyc not in seen_cycles:
                cycles.append(cyc)
                seen_cycles.add(cyc)

            if layer not in data:
                data[layer] = {"bg": [], "an": []}

            data[layer][typ].append(val)

    return cycles, data


# --- Parse variance file ---
def parse_var(filename):
    data = {}
    with open(filename, "r") as f:
        for line in f:
            m = re.search(r"(cyc\d+)\s+(bg|an)\s+Layer\s+(\d+): VAR = ([0-9.eE+-]+)", line, re.I)
            if not m: continue
            cyc, typ, layer, val = m.groups()
            layer = int(layer)
            val = float(val)
            if layer not in data:
               data[layer] = {"bg": [], "an": []}
            data[layer][typ].append(val)
    return data

def main():
    parser = argparse.ArgumentParser(
        description="Plot RMSE sawtooth from a single RMSE file"
    )
    parser.add_argument("file", help="RMSE text file")
    parser.add_argument("var_file", help="Ensemble variance text file")
    parser.add_argument("-o", "--omit", default=0, help="Number of cycles from start to omit in computation (default 0)")

    args = parser.parse_args()

    cycles, data = parse_file(args.file)
    var = parse_var(args.var_file)

    #print(cycles)
    #print(data)
    x = list(range(len(cycles)))

    nlayers = len(data)
    print(f"{nlayers=}, ncycles={len(cycles)}") 
    print(f"Omitting {args.omit} cycle(s) from computation\n")

    st = int(args.omit) # Starting index for computation
    bgavg, varavg = 0.0, 0.0
    for layer in sorted(data.keys()):
        bgavg  = bgavg  + np.mean(data[layer]["bg"][st:])
        varavg = varavg + np.mean(var[layer]["bg"][st:])
    bgavg = bgavg /  nlayers
    varavg = np.sqrt(varavg / nlayers)
    print(f"Ens. Mean Background RMSE = {bgavg}")
    print(f"       Total Prior Spread = {varavg}")

if __name__ == "__main__":
    main()
