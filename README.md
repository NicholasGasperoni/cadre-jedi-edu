![CADRE logo](notebooks/images/CADRE-Logo-Aspect8-1.jpeg)
# Welcome to CADRE-JEDI-edu!
This repository contains the data assimilation (DA) tutorial, **CADRE-JEDI-edu**.  Built upon the initial JEDI-edu tutorial prototype from JCSDA (Joint Center for Satellite Data Assimilation) and CSU (Colorado State University), the **Consortium for Advanced Data Assimilation Research and Education (CADRE, <https://ucadre.org/>)** has expanded upon JEDI-edu with significant developments. These new developments include the addition of several new DA solvers - in particular **ensemble-based methods** - as well as a cycling tutorial and accompanying Capstone project where users can tune their own cycled DA systems. Additionally, modifications to the python-based plotting scripts have been made to assist in diagnostics and learning of the results, with new scripts added to compute diagnostics (e.g. RMSE, RMSD, ensemble spread) and plot sawtooth diagrams.   

CADRE-JEDI-edu uses the next-generation **Joint Effort for Data assimilation Integration (JEDI)** system (https://www.jcsda.org/jcsda-project-jedi), and is appropriate for upper-level undergraduate and graduate students within the earth science disciplines. In this tutorial, users will explore basic concepts of DA, the science that fuses observations with numerical model outputs to obtain an analysis that best estimates the status of the Earth system as it evolves over time. This will be accomplished through simulated observations and the use of a toy model - the **[Quasigeostrophic (QG) Model](https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest/inside/jedi-components/oops/toy-models/qg.html#equation-eq-toy-model-qg-q)** - an idealized two-layer model which mimics large-scale flow of the atmosphere and can be run efficiently on a personal laptop. 

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


Please see START.md to get started! It has instructions on how to download and install the containerized tutorials on your local Windows or Mac machine.

For questions or comments regarding this tutorial, please contact any of the following developers and testers:

- Nicholas Gasperoni (<ngaspero@ou.edu>)
- Xuguang Wang (<xuguang.wang@ou.edu>)
- Aaron Johnson (<ajohns14@ou.edu>)
- Yongming Wang (<yongming.wang@ou.edu>)
- Xingchao Chen (<xzc55@psu.edu>)
- Jonathan Poterjoy (<poterjoy@umd.edu>)
- Youngmin Choi (<yochoi@umd.edu>)
