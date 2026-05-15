## A note about directory structures in this tutorial:

The directory tree at left allows you to navigate to any experiment results, plots, or yaml files to view them

In the top level directory there are seven subdirectories:

1. **build** - The directory of pre-built oops-bundle files, using older JEDI version
2. **oops-bundle** - The source code corresponding to the prebuilt **build** files
3. **build-v2** - A newer version of JEDI oops (oops-bundle-v2), needed to run Local particle Filter (LPF)
4. **oops-bundle-v2** - Source code of newer version of oops
5. **libs_new** - Pre-built libraries needed to run newer **build-v2** oops
6. **shared** - Main directory where all python notebooks, yamls, experiment output, and plotting scripts/output are enclosed
7. **shared-v2** - Can be safely ignored, as LPF tutorial has been merged into the main **shared** directory.

Note you should only need to stay within the **shared** directory to run the tutorial


## **shared** directory structure

1. **EDU** - Contains all tutorial experiment subdirectories as well as **plots_scripts** - containing plotting/diagnostic python scripts
2. **images** - Contains images that are displayed by default in all tutorial notebooks. Do not modify these images!


## Tutorial Experiment directories' structure

For a given TUTORIAL directory (e.g. qgstart, qg3Dvar, qgLETKF, etc...), the structure of the directory is common

1. **output**/ - with individual experiment subdirectories (e.g. **exp_default, exp_mult_obs,** etc.)
	- Each experiment subdirectory contains further subdirectories **bg, obs, da,** and **plots**. Note some experiments will not have bg and obs directories, as they will default to the subdirectories contained in TUTORIAL directory **qgstart**. Also note the **truth** simulation is contained in **qgstart** after generation
	- Resulting analysis and output JEDI files after assimilation are contained in **da** subdirectories directories.

2. **yamls**/ - All yaml files for all JEDI programs executed for each tutorial are located here





