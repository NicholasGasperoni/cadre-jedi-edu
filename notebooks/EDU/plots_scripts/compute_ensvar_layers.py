#!/usr/bin/env python3
import argparse
import numpy as np
from netCDF4 import Dataset

def main():
    parser = argparse.ArgumentParser(
        description="Compute 2D-average ensemble variance per layer"
    )
    parser.add_argument("var_file", help="NetCDF file with ensemble variance")
    parser.add_argument("-v", "--variable", required=True, help="Variable name")
    parser.add_argument("-o", "--output", default="ensvar.txt", help="Output text file")
    parser.add_argument("-l", "--label", default="cycle", help="Cycle label, e.g., 'cyc1 bg'")
    args = parser.parse_args()

    # Open file
    ds = Dataset(args.var_file, "r")
    var = ds.variables[args.variable][:]  # assume shape (layer, y, x)
    ds.close()

    nlayer = var.shape[0]
    avg_var = [np.mean(var[k]) for k in range(nlayer)]

    # Append to output file
    with open(args.output, "a") as f:
        for k, v in enumerate(avg_var):
            f.write(f"{args.label} Layer {k}: VAR = {v:.6f}\n")

    print(f"2D-average variance written to {args.output}")

if __name__ == "__main__":
    main()
