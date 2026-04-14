----bg---
The bg directory contains reduced resolution (20 x 10 x 2) background ensemble files that can be used as initial conditions for the Capstone pproject. 

There are 200 ensemble member provided, but you only need to use a subset in your cycling experiments. 

Please see the capstone noteboook (qg_cycling_capstone) for more information


----obs----
The obs directory contains observations files produced from the full resolution truth (40 x 20 x 2).

Each file contains 100 observations at the same locations for each time.

Note cycle 1 were produced from the P16D forecast of the truth simulation


----truth----
The truth directory contains truth model simulation, but already reduced in resolution  from 40 x 20 x 2 to 20 x 10 x 2

The original truth similation out to 115 days (not provided) was run at the full 40 x 20 x 2 resolution. 

Output from each day in the forecast was then converted to the reduced resolution, to ensure verification is done on the same grid as the experiment resolution of 20 x 10 x 2. But these files still represent a truth simulation produced from a higher resolution forecast.
