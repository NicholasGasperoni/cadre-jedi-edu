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
    parser.add_argument("-f", "--outfile", default="./ssr_timeseries.png", help="Name of output file (png)")
    args = parser.parse_args()

    cycles, data = parse_file(args.file)
    var = parse_var(args.var_file)

    x = list(range(len(cycles)))
    nlayers = len(data)
    print(f"{nlayers=}, ncycles={len(cycles)}")
    print(f"Omitting {args.omit} cycle(s) from computation\n")
    st = int(args.omit)  # Starting index for computation

    # Collect per-layer stats for averaging across layers
    bg_means, bg_stds = [], []
    var_means, var_stds = [], []
    ssr_vals = []  # per-cycle spread-skill ratios, pooled across layers

    for layer in sorted(data.keys()):
        bg_vals  = np.array(data[layer]["bg"][st:])
        var_vals = np.array(var[layer]["bg"][st:])

        bg_means.append(np.mean(bg_vals))
        bg_stds.append(np.std(bg_vals, ddof=1))

        var_means.append(np.mean(var_vals))
        var_stds.append(np.std(var_vals, ddof=1))

        # Per-cycle spread-skill ratio for this layer: spread / RMSE
        spread_vals = np.sqrt(var_vals)
        ssr_vals.append(spread_vals / bg_vals)

    # Average mean and spread across layers (matching original logic)
    bgavg  = np.mean(bg_means)
    varavg = np.sqrt(np.mean(var_means))

    # Layer-averaged std dev:
    #   For RMSE: average the per-layer std devs
    #   For spread: propagate through the sqrt(mean(var)) formula using
    #               d/d(var_mean) sqrt(mean(var)) = 1 / (2*sqrt(mean(var)))
    bgstd  = np.mean(bg_stds)
    varstd = np.mean(var_stds) / (2.0 * varavg) if varavg > 0 else 0.0

    # Spread-skill ratio: mean and std dev over all cycles and layers
    # Computed per-cycle (not ratio-of-means) to capture cycle-to-cycle variability
    ssr_all = np.concatenate(ssr_vals)
    ssr_mean = np.mean(ssr_all)
    ssr_std  = np.std(ssr_all, ddof=1)

    if   ssr_mean < 0.9:  calibration = "underdispersed (overconfident)"
    elif ssr_mean > 1.1:  calibration = "overdispersed"
    else:                 calibration = "well-calibrated"

    print(f"Ens. Mean Background RMSE = {bgavg:.6f}  (std dev = {bgstd:.6f})")
    print(f"       Total Prior Spread = {varavg:.6f}  (std dev = {varstd:.6f})")
    print(f"      Spread-Skill Ratio  = {ssr_mean:.6f}  (std dev = {ssr_std:.6f})  → {calibration}")

    # --- Spread-skill ratio time series plot ---
    # ssr_vals is a list of per-layer arrays (each length ncycles - st).
    # Average across layers at each cycle to get a single time series.
    ssr_by_cycle = np.mean(np.stack(ssr_vals, axis=0), axis=0)  # shape: (ncycles - st,)
    cycle_nums   = np.arange(st, len(cycles))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(cycle_nums, ssr_by_cycle, color="steelblue", linewidth=1.2, label="SSR (layer avg)")
    ax.axhline(1.0,      color="black",  linewidth=1.0, linestyle="--", label="Perfect calibration (1.0)")
    ax.axhline(ssr_mean, color="tomato", linewidth=1.0, linestyle=":",  label=f"Mean SSR = {ssr_mean:.3f}")
    ax.fill_between(cycle_nums, 0.9, 1.1, color="green", alpha=0.08, label="Well-calibrated band (0.9–1.1)")
    ax.set_xlabel("Cycle")
    ax.set_ylabel("Spread-Skill Ratio")
    ax.set_title("Prior Spread-Skill Ratio over Time")
    ax.legend(fontsize=8)
    ax.set_xlim(cycle_nums[0], cycle_nums[-1])
    ax.set_ylim(bottom=0)
    plt.tight_layout()
    plt.savefig(args.outfile, dpi=150)
    print("\nSpread-skill ratio plot saved to ssr_timeseries.png")
    plt.show()

if __name__ == "__main__":
    main()
