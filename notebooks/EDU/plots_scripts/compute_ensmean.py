#!/usr/bin/env python3

import argparse
import glob
import numpy as np
from netCDF4 import Dataset

def main():
    parser = argparse.ArgumentParser(
        description="Compute ensemble mean from NetCDF ensemble members"
    )
    parser.add_argument(
        "-p", "--pattern",
        required=True,
        help="Input file pattern, e.g. bkgd.ens.*.2009-12-30T00:00:00Z.P1D.nc"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output ensemble mean file"
    )
    args = parser.parse_args()

    files = sorted(glob.glob(args.pattern))

    if len(files) == 0:
        raise RuntimeError("No files found matching pattern")

    print(f"Found {len(files)} ensemble members")

    # --- Open first file as template ---
    ds0 = Dataset(files[0], "r")

    # Identify variables to average (exclude coordinates)
    varnames = []
    for v in ds0.variables:
        if v in ds0.dimensions:
            continue  # skip coordinate variables like time, lat, lon
        varnames.append(v)

    print(f"Variables to average: {varnames}")

    # --- Initialize accumulators ---
    sums = {}
    for v in varnames:
        sums[v] = np.zeros_like(ds0.variables[v][:], dtype=np.float64)

    # --- Loop over ensemble members ---
    for f in files:
        print(f"Reading {f}")
        ds = Dataset(f, "r")

        for v in varnames:
            sums[v] += ds.variables[v][:]

        ds.close()

    # --- Compute mean ---
    nmem = len(files)
    means = {v: sums[v] / nmem for v in varnames}

    # --- Write output file ---
    out = Dataset(args.output, "w")

    # Copy dimensions
    for dim_name, dim in ds0.dimensions.items():
        out.createDimension(dim_name, len(dim) if not dim.isunlimited() else None)

    # Copy variables
    for name, var in ds0.variables.items():
        out_var = out.createVariable(name, var.datatype, var.dimensions)

        # Copy attributes
        out_var.setncatts({k: var.getncattr(k) for k in var.ncattrs()})

        if name in varnames:
            out_var[:] = means[name]
        else:
            # Copy coordinate variables unchanged
            out_var[:] = var[:]

    # Global attributes
    out.setncatts({k: ds0.getncattr(k) for k in ds0.ncattrs()})
    out.history = "Ensemble mean computed from {} members".format(nmem)

    ds0.close()
    out.close()

    print(f"Ensemble mean written to {args.output}")
    exit(0)


if __name__ == "__main__":
    main()