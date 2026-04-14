#!/usr/bin/env python3

import argparse
import re
import matplotlib.pyplot as plt

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


def main():
    parser = argparse.ArgumentParser(
        description="Plot RMSE sawtooth from a single RMSE file"
    )
    parser.add_argument("file", help="RMSE text file")
    parser.add_argument("-o", "--output", default="rmse_sawtooth.png")

    args = parser.parse_args()

    cycles, data = parse_file(args.file)

    print(cycles)
    print(data)
    x = list(range(len(cycles)))

    plt.figure()

    #for layer in sorted(data.keys()):
    #    bg = data[layer]["bg"]
    #    an = data[layer]["an"]
    #
    #    # Safety check
    #    if len(bg) != len(an):
    #        raise ValueError(f"Mismatch in bg/an lengths for layer {layer}")

     #   plt.plot(x, bg, marker='o', label=f"Layer {layer} (bg)")
     #   plt.plot(x, an, marker='s', linestyle='--', label=f"Layer {layer} (an)")
 
    for layer in sorted(data.keys()):
        bg = data[layer]["bg"]
        an = data[layer]["an"]

        # Ensure matching lengths (skip incomplete last cycle if needed)
        n = min(len(bg), len(an))

        combined = []
        for i in range(n):
            combined.append(bg[i])
            combined.append(an[i])

        #x = list(range(len(combined)))
        x=[0, 0, 2, 2, 4, 4, 6, 6, 8, 8, 10, 10]
        plt.plot(x, combined, marker='o', label=f"Layer {layer}")

    xticks = [2*i for i in range(n)]
    xlabels = [cycles[i] for i in range(n)]

    plt.xlabel("Cycle")
    plt.ylabel("RMSE")
    plt.title("RMSE Sawtooth Plot")
    plt.xticks(xticks, xlabels, rotation=45)
    plt.ylim(0,4.5e7)
    plt.legend()
    plt.grid()

    
    plt.tight_layout()
    plt.savefig(args.output, dpi=150)

    print(f"Saved plot to {args.output}")


if __name__ == "__main__":
    main()
