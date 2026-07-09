![CADRE logo](notebooks/images/CADRE-Logo-Aspect8-1.jpeg)
# Welcome to CADRE-JEDI-edu!
## How to use the CADRE-JEDI-edu tutorials
**These tutorials are provided as an educational tool for the purpose of learning data assimilation (DA). They are best used together with other materials (e.g., lecture notes from a DA class or training, theory/derivation of DA formularameworks), rather than as a standalone comprehensive guide to DA.**
## Overview and Contents
This repository contains the data assimilation (DA) tutorial, ****CADRE-JEDI-edu****.  Built upon the initial JEDI-edu’s 3DVar and 4DVar  tutorial prototype from JCSDA (Joint Center for Satellite Data Assimilation) and CSU (Colorado State University), the ****Consortium for Advanced Data Assimilation Research and Education (CADRE, <https://ucadre.org/>)**** has expanded upon JEDI-edu with significant developments. These new developments include the addition of several new DA solvers - in particular ****ensemble-based methods**** (LETKF, EnVar, LPF) - as well as a cycling tutorial and accompanying Capstone project where users can tune their own cycled DA systems. Additionally, various modifications to the python-based plotting scripts have been developed made to assist in diagnostics and learning of the essence of the various solvers (see details below)results. Collectively, this tutorial tool is called CADRE-JEDI-edu., with new scripts added to compute diagnostics (e.g. RMSE, RMSD, ensemble spread) and plot sawtooth diagrams.

CADRE-JEDI-edu uses the next-generation ****Joint Effort for Data assimilation Integration (JEDI)**** system (https://www.jcsda.org/jcsda-project-jedi), and is appropriate for upper-level undergraduate and graduate students within the earth science disciplines. In this tutorial, users will explore basic concepts of DA, the science that fuses observations with numerical model outputs to obtain an analysis that best estimates the state of the Earth system as it evolves over time. This will be accomplished through simulated observations and the use of a toy model - the ****[Quasigeostrophic (QG) Model](https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest/inside/jedi-components/oops/toy-models/qg.html#equation-eq-toy-model-qg-q)**** - an idealized two-layer model which mimics large-scale flow of the atmosphere and can be run efficiently on a personal laptop.
  
The tutorial covers several topics, including:

- Basic overview of DA concepts using:
  - Single-observation DA experiments
  - Multi-observation (100 observations) DA experiments
- How to design idealized experiments for DA
- Variational solvers (3DVar and 4DVar)
- Ensemble Kalman filters (via LETKF) and benefits of ensemble-based methods
- Hybrid ensemble-variational data assimilation (3DEnVar, 4DEnVar)
- Local Particle Filter (LPF) for nonlinear, non-Gaussian DA
- Examination of spatial and time-based flow dependence, and their effects on analyses
- Basic qualitative and quantitative diagnostics/visualizations (i.e. RMSE, RMSD, spread, sawtooth diagrams)
- DA cycling of analyses and forecasts
- Capstone project, where users must tune a cycled LETKF system for best results across 200 cycles

## Installation and Important Technical Information
Please see START.md to get started! It has instructions on how to download and install the containerized tutorials on your local Windows or Mac machine.

Note that two versions of the JEDI's Object-Oriented Prediction System (OOPS) are provided inside the container to run all of the tutorials  in the "shared" directory.  All tutorials except for the LPF tutorial use an earlier version of OOPS, while the LPF tutorial (*7.qg_lpf_tutorial.ipynb*) was later added to a newer version of OOPS (within folders labeled "-v2" in the container). In a subsequent update, all tutorials will be merged within the newer version of OOPS, please check back for future releases!

## Software License and Support 
This software is licensed under the terms of the Apache License Version 2.0 which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
This code is released **as-is**. While we hope you find it useful, we're unable to provide individual support and troubleshooting. For questions or concerns, we ask that you submit them through our [main development repository](https://github.com/NicholasGasperoni/cadre-jedi-edu/discussions). Though we cannot guarantee a prompt response, your feedback will be considered while developing future versions.

