#!/usr/bin/env python3
import argparse
import re
import matplotlib.pyplot as plt
import numpy as np

def parse_file(filename):
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

def parse_var(filename):
    data = {}
    with open(filename, "r") as f:
        for line in f:
            m = re.search(r"(cyc\d+)\s+(bg|an)\s+Layer\s+(\d+): VAR = ([0-9.eE+-]+)", line, re.I)
            if not m:
                continue
            cyc, typ, layer, val = m.groups()
            layer = int(layer)
            val = float(val)
            if layer not in data:
                data[layer] = {"bg": [], "an": []}
            data[layer][typ].append(val)
    return data


def plot_panel(ax, cycles_slice, data_slice, var_slice, ymax):
    """Plot one panel of the sawtooth onto a given Axes object."""
    n = len(cycles_slice)
    for layer in sorted(data_slice.keys()):
        bg      = data_slice[layer]["bg"]
        an      = data_slice[layer]["an"]
        varbg   = var_slice[layer]["bg"]
        varan   = var_slice[layer]["an"]

        combined     = []
        combined_var = []
        for i in range(n):
            combined.append(bg[i])
            combined.append(an[i])
            combined_var.append(np.sqrt(varbg[i]))
            combined_var.append(np.sqrt(varan[i]))

        x = [(v // 2) * 2 for v in range(len(combined))]
        ax.plot(x, combined,     marker='o', label=f"Layer {layer} RMSE")
        ax.plot(x, combined_var, marker='+', label=f"Layer {layer} Spread")

    xticks  = [2 * i for i in range(n)]
    xlabels = cycles_slice
    ax.set_xlabel("Cycle")
    ax.set_ylabel("RMSE")
    ax.set_title("RMSE Sawtooth Plot")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, rotation=45)
    ax.legend()
    ax.grid()
    ax.set_ylim(0, ymax)


def slice_data(data, var, start, end):
    """Slice data and var dicts to cycles [start, end) (0-indexed)."""
    data_slice = {}
    var_slice  = {}
    for layer in data:
        data_slice[layer] = {
            "bg": data[layer]["bg"][start:end],
            "an": data[layer]["an"][start:end],
        }
        var_slice[layer] = {
            "bg": var[layer]["bg"][start:end],
            "an": var[layer]["an"][start:end],
        }
    return data_slice, var_slice


def main():
    parser = argparse.ArgumentParser(
        description="Plot RMSE sawtooth from a single RMSE file"
    )
    parser.add_argument("file",     help="RMSE text file")
    parser.add_argument("var_file", help="Ensemble variance text file")
    parser.add_argument("-o", "--output", default="rmse_sawtooth.png")
    parser.add_argument("-m", "--max",    default=8e7,
                        help="Maximum value for RMSE plot")
    parser.add_argument("--split", type=int, default=100,
                        help="Split into two panels above this many cycles (default 100)")
    args = parser.parse_args()

    cycles, data = parse_file(args.file)
    var          = parse_var(args.var_file)
    ymax         = float(args.max)
    ncycles      = len(cycles)

    if ncycles > args.split:
        # Two-panel figure
        mid = args.split
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

        data1, var1 = slice_data(data, var, 0,   mid)
        data2, var2 = slice_data(data, var, mid, ncycles)

        plot_panel(ax1, cycles[0:mid],      data1, var1, ymax)
        plot_panel(ax2, cycles[mid:ncycles], data2, var2, ymax)

        ax1.set_title(f"RMSE Sawtooth Plot — Cycles 1–{mid}")
        ax2.set_title(f"RMSE Sawtooth Plot — Cycles {mid+1}–{ncycles}")

    else:
        # Single-panel figure
        figwidth = 12 if ncycles > 20 else 6
        fig, ax  = plt.subplots(figsize=(figwidth, 4))
        plot_panel(ax, cycles, data, var, ymax)

    plt.tight_layout()
    plt.savefig(args.output, dpi=150)
    print(f"Saved plot to {args.output}")

    
    # Collect per-layer stats for averaging across layers
    bg_means, bg_stds = [], []
    var_means, var_stds = [], []
    ssr_vals = []  # per-cycle spread-skill ratios, pooled across layers
    st=0
    
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
    print(f"  Avg. Total Prior Spread = {varavg:.6f}  (std dev = {varstd:.6f})")
    print(f"  Avg. Spread-Skill Ratio = {ssr_mean:.6f}  (std dev = {ssr_std:.6f})  → {calibration}")

if __name__ == "__main__":
    main()
