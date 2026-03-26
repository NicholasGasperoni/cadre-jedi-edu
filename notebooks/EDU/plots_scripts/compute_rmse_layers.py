#!/usr/bin/env python3

import argparse
import numpy as np
#import xarray as xr
from netCDF4 import Dataset

def compute_rmse(a, b):
    """Compute RMSE between two arrays."""
    return np.sqrt(np.mean((a - b) ** 2))

def main():
    parser = argparse.ArgumentParser(
        description="Compute RMSE between model and truth for each layer"
    )
    parser.add_argument("model_file", help="Path to model (background/analysis) file")
    parser.add_argument("truth_file", help="Path to truth file")
    parser.add_argument("-v", "--variable", required=True,
                        help="Variable name to compare")
    parser.add_argument("-o", "--output", default="rmse.txt",
                        help="Output text file")
    parser.add_argument("-l", "--label", default="Cyc", 
                        help="Label for text file (e.g. cycle number, bg, etc.")

    args = parser.parse_args()

    # Open NetCDF files
    ds_model = Dataset(args.model_file, "r")
    ds_truth = Dataset(args.truth_file, "r")

    # Extract variables
    var_model = ds_model.variables[args.variable][:]
    var_truth = ds_truth.variables[args.variable][:]

    # Check dimensions
    if var_model.shape != var_truth.shape:
        raise ValueError("Model and truth variable shapes do not match")

    # Assume first dimension is "layer" (size = 2)
    nlayer = var_model.shape[0]

    rmse_values = []

    for k in range(nlayer):
        rmse = compute_rmse(var_model[k], var_truth[k])
        rmse_values.append(rmse)

    # Write output
    with open(args.output, "a") as f:
        for k, rmse in enumerate(rmse_values):
            f.write(f"{args.label} Layer {k}: RMSE = {rmse:.6f}\n")

    print(f"RMSE written to {args.output}")

    # Close files
    ds_model.close()
    ds_truth.close()

if __name__ == "__main__":
    main()
