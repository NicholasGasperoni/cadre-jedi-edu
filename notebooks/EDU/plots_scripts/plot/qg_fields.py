#!/usr/bin/env python3
"""
@author: Mayeul Destouches
@author: modified by Benjamin Menetrier for JEDI
@description: plot fields or increments if two paths are specified
"""

import os
import sys
import subprocess
import argparse
import numpy as np
import netCDF4
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import BoundaryNorm

def func(args):
    """! Plot fields"""

    # Geophysical parameters
    req = 6371229.0                      # Earth radius at equator (m)
    domain_zonal = 2 * np.pi * req       # Model domain in zonal direction (m)
    domain_meridional = 0.5 * np.pi *req # Model domain in meridional direction (m)
    plot_width=7 #units in inches
    plot_height=3.5 #units in inches
    vec_len_frac=20 # with --plotwind the longest vector plotted will be (1/vec_len_frac)*plot_width inches in length

    # Variables to plot
    variables = ["x", "q","u","v"]

    # File path
    filepaths = []
    ids = []
    if args.gif is None:
        filepaths.append(args.filepath)
        print(filepaths)
    else:
        check_convert = subprocess.getstatusoutput('convert --help')
        if check_convert[0] != 0:
            print("   Error: convert (imagemagick package) should be available to create an animated gif")
            sys.exit(1)
        if "%id%" in args.filepath:
           for id in args.gif.split(","):
               ids.append(id)
               filepaths.append(args.filepath.replace("%id%", id))
        else:
            print("   Error: filepath should include a %id% pattern for gif generation")
            sys.exit(1)

    # Loop over variables
    for variable in variables:
        # Fields vector
        fields = []
        if args.plotwind:
            fields_u = []
            fields_v = []
        if args.plotstream:
            fields_x = []
        if args.plotObsLocations:
            # Variables to get
            obs_types = ["Stream", "Wind", "WSpeed"]
            # Check file extension
            if not args.plotObsLocations.endswith(".nc"):
                print("   Error: filepath extension should be .nc")
                sys.exit(1)
            # Get data
            res = netCDF4.Dataset(args.plotObsLocations)
            for obs_type in obs_types:
                print(f"Obs_type={obs_type}")
                print(f"res.groups={res.groups}")
                if obs_type in res.groups:
                    locations = res.groups[obs_type].groups["Location"].variables["values"][:,:]
                    break
            obs_lon = locations[:,0]
            obs_lat = locations[:,1]

        if args.plotObsValues:
           # Variables to get
            obs_types = ["Stream", "Wind", "WSpeed"]
            # Check file extension
            if not args.plotObsValues.endswith(".nc"):
                print("   Error: filepath extension should be .nc")
                sys.exit(1)
            # Get data
            res = netCDF4.Dataset(args.plotObsValues)
            for obs_type in obs_types:
                if obs_type in res.groups:
                    locations = res.groups[obs_type].groups["Location"].variables["values"][:,:]
                    obsvalues = res.groups[obs_type].groups["ObsValue"].variables["values"][:,:]
                    hofx = res.groups[obs_type].groups["hofx"].variables["values"][:,:]
                    break
            obs_lon = locations[:,0]
            obs_lat = locations[:,1]
            obind_layer1 = np.where(locations[:,2] < 4000.)
            obind_layer2 = np.where(locations[:,2] >= 4000.)
            obs_lon_layer1 = obs_lon[obind_layer1]
            obs_lat_layer1 = obs_lat[obind_layer1]
            obs_lon_layer2 = obs_lon[obind_layer2]
            obs_lat_layer2 = obs_lat[obind_layer2]
            if args.basefilepath is None:
                obs_values = obsvalues[:,0]
                if args.plothofx: obs_values = hofx[:,0]
            else:
                obs_values = obsvalues[:,0] - hofx[:,0]
            obs_values_layer1 = obs_values[obind_layer1]
            obs_values_layer2 = obs_values[obind_layer2]
            print(f"lon,lat,val of first ob = {obs_lon[0]},{obs_lat[0]},{obs_values[0]}")
        # Loop over filepaths
        for filepath in filepaths:
            # Check file extension
            if not filepath.endswith(".nc"):
                print("   Error: filepath extension should be .nc")
                sys.exit(1)

            # Load fields
            fields.append(netCDF4.Dataset(filepath).variables[variable][:])
            if args.plotwind:
                 fields_u.append(netCDF4.Dataset(filepath).variables["u"][:])
                 fields_v.append(netCDF4.Dataset(filepath).variables["v"][:])
            if args.plotstream:
                 fields_x.append(netCDF4.Dataset(filepath).variables["x"][:])

        # Plotted fields vector
        fields_plot = []
        if args.plotwind:
            fields_u_plot = []
            fields_v_plot = []
        if args.plotstream:
            fields_x_plot = []
        if args.basefilepath is None:
            for field in fields:
               fields_plot.append(field)
            if args.plotwind:
                for field_u in fields_u:
                    fields_u_plot.append(field_u)
                for field_v in fields_v:
                    fields_v_plot.append(field_v)
            if args.plotstream:
                for field_x in fields_x:
                    fields_x_plot.append(field_x)
        else:
            # Check file extension
            if not args.basefilepath.endswith(".nc"):
                print("   Error: basefilepath extension should be .nc")
                sys.exit(1)

            # Load base fields
            field_base = netCDF4.Dataset(args.basefilepath).variables[variable][:]
            if args.plotwind:
                field_u_base = netCDF4.Dataset(args.basefilepath).variables["u"][:]
                field_v_base = netCDF4.Dataset(args.basefilepath).variables["v"][:]
            if args.plotstream:
                field_x_base = netCDF4.Dataset(args.basefilepath).variables["x"][:]
            # Compute increments
            for field in fields:
                fields_plot.append(field-field_base)
                rmsd = np.sqrt(np.mean((field - field_base)**2))
                print(f"Variable {variable}, RMSD = {rmsd}")
            if args.plotwind:
                for field_u in fields_u:
                    fields_u_plot.append(field_u-field_u_base)
                for field_v in fields_v:
                    fields_v_plot.append(field_v-field_v_base)
            if args.plotstream:
                for field_x in fields_x:
                    fields_x_plot.append(field_x_base)
        # Get geometry
        nz, ny, nx = fields_plot[0].shape
        levels = list(range(nz))
        z_coord = netCDF4.Dataset(filepaths[0]).variables["z"][:]
        lon_coord = netCDF4.Dataset(filepaths[0]).variables["lon"][:]
        lat_coord = netCDF4.Dataset(filepaths[0]).variables["lat"][:]

        min_lon = np.min(lon_coord)
        max_lon = np.max(lon_coord)
        min_lat = np.min(lat_coord)
        max_lat = np.max(lat_coord)

        # Get obs locations in other unit
        if args.plotObsLocations or args.plotObsValues:
            indexes = []
            ind1 = []
            ind2 = []
            for ii in range(len(obs_lon)):
                obs_lat[ii] = 90/(max_lat-min_lat) * (obs_lat[ii] - min_lat)
                if (obs_lon[ii] < min_lon) or (obs_lon[ii] > max_lon) or (obs_lat[ii] < min_lat) or (obs_lat[ii] > max_lat):
                    indexes.append(ii)
            obs_lon = np.delete(obs_lon, indexes)
            obs_lat = np.delete(obs_lat, indexes)
        
        if  args.plotObsValues:
            ind1 = []
            ind2 = []
            for ii in range(len(obs_lon_layer1)):
                obs_lat_layer1[ii] = 90/(max_lat-min_lat) * (obs_lat_layer1[ii] - min_lat)
                if (obs_lon_layer1[ii] < min_lon) or (obs_lon_layer1[ii] > max_lon) or (obs_lat_layer1[ii] < min_lat) or (obs_lat_layer1[ii] > max_lat):
                    ind1.append(ii)
            for ii in range(len(obs_lon_layer2)):
                obs_lat_layer2[ii] = 90/(max_lat-min_lat) * (obs_lat_layer2[ii] - min_lat)
                if (obs_lon_layer2[ii] < min_lon) or (obs_lon_layer2[ii] > max_lon) or (obs_lat_layer2[ii] < min_lat) or (obs_lat_layer2[ii] > max_lat):
                    ind2.append(ii)
            obs_lon_layer1 = np.delete(obs_lon_layer1, ind1)
            obs_lat_layer1 = np.delete(obs_lat_layer1, ind1)
            obs_lon_layer2 = np.delete(obs_lon_layer2, ind2)
            obs_lat_layer2 = np.delete(obs_lat_layer2, ind2)
            obs_values = np.delete(obs_values, indexes)
            obs_values_layer1  = np.delete(obs_values_layer1, ind1)
            obs_values_layer2  = np.delete(obs_values_layer2, ind2)


        # Define color levels
        clevels = []
        clevels_obs = []
        norm = []
        norm_obs = []
        if args.fieldmax:
            vmax = float(args.fieldmax)
            if (variable == 'q'): vmax=0.5*vmax*10**-12 #3.5e-4
            if (variable == 'u'): vmax=0.5*vmax*10**-6 #140.0
            if (variable == 'v'): vmax=0.5*vmax*10**-6 #70.0
            vmin = -vmax
            npltlevs=22
        else:
            vmax = 0.0
            tmax=0.0
            tmin=0.0
            if args.basefilepath is None: # Full field
                if (variable == 'x'): vmax=5.0e8 #5.0e8
                if (variable == 'q'): vmax=6.5e-4  #6.5e-4
                if (variable == 'u'): vmax=150.0 #145.0
                if (variable == 'v'): vmax=100.0 #90.0
                npltlevs=22
            else: # Difference field
                if (variable == 'x'): vmax=1.0e8
                if (variable == 'q'): vmax=2.0e-4 #3.5e-4
                if (variable == 'u'): vmax=80. #140.0
                if (variable == 'v'): vmax=40. #70.0
                npltlevs=22
            vmin = -1.0 * vmax
            if args.basefilepath is None and variable == 'x': vmax=1.1e8
            for level in levels:
                for field in fields_plot:
                    tmax = max(tmax, np.max(field[level]))
                    tmin = min(tmin, np.min(field[level]))
            print(f"data range:({tmin},{tmax}), plot range: ({vmin},{vmax}) ")
        for level in levels:
            clevels.append(np.linspace(vmin, vmax, npltlevs))
            clevels_obs.append(np.linspace(-1.0e8, 1.0e8, npltlevs))
            # Create a norm using custom contour levels
            # Useful for dot plot colors being consistent with contour colors
            norm.append(BoundaryNorm(clevels[level], ncolors=256, clip=True))
            norm_obs.append(BoundaryNorm(clevels_obs[level], ncolors=256, clip=True))

        # Define plot
        params = {
            "font.size": 12,
            "text.latex.preamble" : r"\usepackage{amsmath}\usepackage{amsfonts}",
            "ytick.left": False,
            "ytick.labelleft": False,
        }
        plt.rcParams.update(params)
        my_formatter = mticker.FuncFormatter(lambda x, pos:"{:.0f}$\degree$E".format(x).replace("-", "\N{MINUS SIGN}"))
        if args.plotwind:
            # Select scale
            if args.basefilepath is None:
                scale = (vec_len_frac)*np.max(np.sqrt(np.square(fields_u_plot)+np.square(fields_v_plot)),axis=(0,1,2,3))/plot_width
            else:
                scale = (vec_len_frac)*np.max(np.sqrt(np.square(fields_u_plot)+np.square(fields_v_plot)),axis=(0,1,2,3))/plot_width
            dx_quiver = max(nx//20, 1)
            dy_quiver = max(ny//10, 1)

        # Initialize gif command
        if not args.gif is None:
             cmd = "convert -delay 20 -loop 0 "

        for iplot in range(0, len(filepaths)):
            fig, axs = plt.subplots(nrows=2, figsize=(plot_width, plot_height))

            # Loop over levels
            for level, ax in zip(levels, axs[::-1]):
                # Plot variable
                if args.basefilepath is None:
                    im = ax.contourf(lon_coord, lat_coord, fields_plot[iplot][level], cmap="Spectral_r", levels=clevels[level],norm=norm[level])
                else:
                    im = ax.contourf(lon_coord, lat_coord, fields_plot[iplot][level], extend='both',  cmap="RdBu_r", levels=clevels[level],norm=norm[level])

                if args.plotwind:
                    # Plot wind field
                    ax.quiver(lon_coord[::dy_quiver, ::dx_quiver], lat_coord[::dy_quiver, ::dx_quiver],
                                  fields_u_plot[iplot][level, ::dy_quiver, ::dx_quiver], fields_v_plot[iplot][level, ::dy_quiver, ::dx_quiver],
                                  scale=scale, scale_units="inches")

                if args.plotstream:
                    # Plot streamfunction contour lines
                    ax.contour(lon_coord, lat_coord, fields_x_plot[iplot][level], levels=10, colors='black', linewidths=1.0)

                if args.plotObsLocations:
                    ax.scatter(obs_lon, obs_lat, marker='x', c='k', s=8, linewidths=0.5)

                if args.plotObsValues:
                    cmapob="RdBu_r"
                    if args.basefilepath is None: cmapob="Spectral_r"
                    if level == 0:
                        ax.scatter(obs_lon_layer1, obs_lat_layer1, c=obs_values_layer1, cmap=cmapob, norm=norm_obs[level], edgecolor='black', linewidths=0.25, s=12)
                    else:
                        ax.scatter(obs_lon_layer2, obs_lat_layer2, c=obs_values_layer2, cmap=cmapob, norm=norm_obs[level], edgecolor='black', linewidths=0.25, s=12)
                    #marker='x', c='k', s=8, linewidths=0.5)


                # Set plot formatting
                ax.set_aspect("equal")
                cb = fig.colorbar(im, ax=ax, shrink=0.9, extend='both', format=("%.1e" if variable == "q" else None))
                ax.set_ylabel("Altitude {:.0f}$\,$m".format(z_coord[level]))
                ax.xaxis.set_major_formatter(my_formatter)

                # Set title
                varname = dict(x="Streamfunction", q="Potential vorticity",u="Zonal Wind", v="Meridional Wind").get(variable)
                unit = dict(x="m$^2$s$^{-1}$", q="s$^{-1}$", u="m/s",v="m/s").get(variable)
                if not args.title is None:
                    fig.suptitle(args.title + " - " + varname + " in " + unit)
                else:
                    fig.suptitle(varname + " in " + unit)
                fig.subplots_adjust(left=0.04, right=0.98, bottom=0.04, top=0.9, hspace=0.01)

            # Save plot
            if args.output is None:
                plotpath = os.path.splitext(os.path.basename(filepaths[iplot]))[0]
            else:
                plotpath = args.output
                if not args.gif is None:
                    plotpath = plotpath.replace("%id%", ids[iplot])
            if args.basefilepath is None:
                plotpath = plotpath + "_" + str(variable) + ".jpg"
            else:
                plotpath = plotpath + "_" + str(variable) + "_diff.jpg"
            if not args.gif is None:
                cmd = cmd + plotpath + " "
                if iplot == 0:
                    gifpath = plotpath.replace(".jpg", ".gif")
            plt.savefig(plotpath, format="jpg", dpi=150)
            plt.close()
            print(" -> plot produced: " + plotpath)

        if not args.gif is None:
            cmd = cmd + gifpath
            os.system(cmd)
            print(" -> gif produced: " + gifpath)
