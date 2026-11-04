# Figure catalogue

Written automatically by the plotting scripts (plotting/figindex.py).
Each entry: what the figure shows, and the run(s) it was made from with their settings.

## calmeddy_cummelt.png

**Cumulative melt in each grid cell under the floe, shared colour scale (calm)**  
_created 2026-11-04 12:13_

Total melt over the run in each grid cell under the floe (cm), from the exact running sum saved by the driver (melt_cum), divided by the cell's ice cover so that partly covered rim cells show the local thinning. Columns: floe radius 1, 2, 4, 8 km. Rows: constant q, dynamic u*_min = 0.0005, dynamic u*_min = 0.002. ONE colour scale for all panels (colour bar on the right column), so amounts can be compared between panels. Panel titles give the floe-mean melt. Diagnostic only: the model thins each floe uniformly; the map shows where the heat was delivered.

Runs:
- `calmeddy_R1km_qconst.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qconst.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qconst.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qconst.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s

## calmeddy_cummelt_pattern.png

**Pattern of cumulative melt under the floe, deviation from the floe mean in cm (calm)**  
_created 2026-11-04 12:13_

Same data as calmeddy_cummelt.png, shown as each cell's cumulative melt minus that floe's mean melt, in cm over the run (red = more melt than average, blue = less). Panel titles give the floe mean and the range of deviations. Each panel has its own symmetric colour scale, so the pattern inside each floe is visible; amounts are compared in calmeddy_cummelt.png. Constant-q floes are uniform (differences are rounding only). In dynamic runs, rings of high melt mark radii where the rigidly rotating floe and the eddy water move at different speeds; low-melt centre and rings mark where they match.

Runs:
- `calmeddy_R1km_qconst.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qconst.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qconst.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qconst.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s

## calmeddy_du_q.png

**Ice-ocean speed difference and heat transfer coefficient vs time (calm)**  
_created 2026-11-04 12:13_

Top: area-mean ice-ocean speed difference under the floe (incl. floe spin), cm/s. Bottom: area-mean heat transfer coefficient q under the floe. One line per floe radius. Dashed lines: 5.5 cm/s, the speed difference at which the dynamic q equals the paper's constant 100 W/m2/K.

Runs:
- `calmeddy_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s

## calmeddy_melt_ratio.png

**Steady thinning-rate ratio, dynamic / constant heat transfer, vs floe radius (calm, eddy)**  
_created 2026-11-04 12:13_

Mean thinning rate from day 2 to day 5 (after spin-up) with the McPhee (velocity-dependent) heat transfer, divided by that with the paper's constant q_IO = 100 W/m2/K, for floe radii 1-8 km. Circles: u*_min = 0.0005 m/s; squares: 0.002 m/s. Below 1 = slower melt than the paper's formulation. Dotted line: eddy radius.

Runs:
- `calmeddy_R1km_qconst.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qconst.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qconst.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qconst.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s

## calmeddy_meltmaps.png

**Melt-rate maps under the floe on day 4 (calm, dynamic heat transfer)**  
_created 2026-11-04 12:13_

Melt rate (cm/day) in each grid cell under the floe, for floe radii 1, 2, 4 and 8 km, zoomed on the floe (black circle). Includes surface (atmospheric) and basal (ocean) melt; the spatial pattern comes from the ocean part, which depends on the local ice-ocean speed difference. Partly covered edge cells show lower values because only part of the cell is ice.

Runs:
- `calmeddy_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s

## calmeddy_thinning.png

**Thinning rate vs time for each floe radius (calm)**  
_created 2026-11-04 12:13_

Thinning rate of the floe's (single, area-mean) thickness in cm/day against time, one panel per floe radius (1, 2, 4, 8 km). Black: paper's constant q. Blue: dynamic heat transfer, u*_min = 0.0005 m/s. Orange dashed: dynamic, u*_min = 0.002 m/s. The early peak in the dynamic runs is the spin-up period, when the water still slides past the floe at the full eddy speed. Dotted line: day 2.

Runs:
- `calmeddy_R1km_qconst.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qconst.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qconst.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qconst.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s

## eddytest_map.png

**Eddy test: floe trajectory over the eddy**  
_created 2026-11-03 17:27_

One panel per run. Colours: vorticity of the prescribed eddy (ζ/f; red = cyclonic, blue = anticyclonic). Arrows: eddy current. Dots and black line: floe-centre track, coloured by time. Dashed circle: floe at the start; gold circle: floe at the end. Box: maximum and final distance of the floe centre from the eddy centre, and the floe's spin rate relative to the rotation rate of the eddy core (+1 = turning with the water).

Runs:
- `eddytest_anticyclonic_R2km.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; no melting; 32 km box, 128x128 grid; model extended; 20 days, dt = 30 s
- `eddytest_cyclonic_R2km.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; cyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; no melting; 32 km box, 128x128 grid; model extended; 20 days, dt = 30 s

## floe_1_trajectory.png

**Floe 1 trajectory in the three free-drift runs**  
_created 2026-11-03 13:18_

Track of floe 1 (unwrapped across the box edges) in: no Coriolis (grey), Coriolis with the original module's component-wise drag (red), and Coriolis with the extended module's vector drag, Eq. 2 (blue). Star = start, dots = end. Legend: final speed and angle to the wind.

Runs:
- `free_drift_no_coriolis.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; no Coriolis; no melting; 10 km box, 50x50 grid; model extended; 2 days, dt = 10 s
- `free_drift_coriolis_original.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; Coriolis on; no melting; 10 km box, 50x50 grid; model original; 2 days, dt = 10 s
- `free_drift_coriolis_extended.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; Coriolis on; no melting; 10 km box, 50x50 grid; model extended; 2 days, dt = 10 s

## free_drift.png

**Drift speed and direction: 'free' runs with wind**  
_created 2026-11-03 13:18_

Top: mean floe drift speed (m/s) against time. Bottom: drift direction relative to the wind direction (degrees; negative = to the right of the wind). Directions are hidden when the wind is weaker than 0.5 m/s or the floes are nearly still.

Runs:
- `free_drift_coriolis_extended.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; Coriolis on; no melting; 10 km box, 50x50 grid; model extended; 2 days, dt = 10 s
- `free_drift_coriolis_original.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; Coriolis on; no melting; 10 km box, 50x50 grid; model original; 2 days, dt = 10 s
- `free_drift_no_coriolis.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; no Coriolis; no melting; 10 km box, 50x50 grid; model extended; 2 days, dt = 10 s

## free_drift_coriolis_extended_map.png

**Floe map: free_drift_coriolis_extended**  
_created 2026-11-03 13:18_

Map of the (periodic) domain. Dashed circles: floes at the start. Filled circles: floes at the last snapshot that still has ice, coloured by thickness. Grey lines: each floe's track (broken where it wraps across the box edge). Grey arrows: ocean current at the end of the run (only if non-zero).

Runs:
- `free_drift_coriolis_extended.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; Coriolis on; no melting; 10 km box, 50x50 grid; model extended; 2 days, dt = 10 s

## free_drift_coriolis_original_map.png

**Floe map: free_drift_coriolis_original**  
_created 2026-11-03 13:18_

Map of the (periodic) domain. Dashed circles: floes at the start. Filled circles: floes at the last snapshot that still has ice, coloured by thickness. Grey lines: each floe's track (broken where it wraps across the box edge). Grey arrows: ocean current at the end of the run (only if non-zero).

Runs:
- `free_drift_coriolis_original.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; Coriolis on; no melting; 10 km box, 50x50 grid; model original; 2 days, dt = 10 s

## free_drift_no_coriolis_map.png

**Floe map: free_drift_no_coriolis**  
_created 2026-11-03 13:18_

Map of the (periodic) domain. Dashed circles: floes at the start. Filled circles: floes at the last snapshot that still has ice, coloured by thickness. Grey lines: each floe's track (broken where it wraps across the box edge). Grey arrows: ocean current at the end of the run (only if non-zero).

Runs:
- `free_drift_no_coriolis.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; no Coriolis; no melting; 10 km box, 50x50 grid; model extended; 2 days, dt = 10 s

## free_trajectories.png

**Floe trajectories: 'free' runs**  
_created 2026-11-03 13:18_

Every floe's path as displacement from its starting point (km), unwrapped across the periodic boundaries so each path is one continuous line. One panel per run, same scale. Dot = last position with ice. Panel title: drift speed and angle to the wind at the last snapshot with ice.

Runs:
- `free_drift_no_coriolis.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; no Coriolis; no melting; 10 km box, 50x50 grid; model extended; 2 days, dt = 10 s
- `free_drift_coriolis_original.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; Coriolis on; no melting; 10 km box, 50x50 grid; model original; 2 days, dt = 10 s
- `free_drift_coriolis_extended.nc`: 16 floe(s), radius 0.2-0.3 km, h0 = 1 m; constant wind 10 m/s towards 0 deg; ocean at rest; Coriolis on; no melting; 10 km box, 50x50 grid; model extended; 2 days, dt = 10 s

## paper_4floes_R1km_nowind_map.png

**Floe map: paper_4floes_R1km_nowind**  
_created 2026-11-03 13:18_

Map of the (periodic) domain. Dashed circles: floes at the start. Filled circles: floes at the last snapshot that still has ice, coloured by thickness. Grey lines: each floe's track (broken where it wraps across the box edge). Grey arrows: ocean current at the end of the run (only if non-zero).

Runs:
- `paper_4floes_R1km_nowind.nc`: 4 floe(s), radius 1 km, h0 = 1.5 m; no wind; ocean at rest; Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 80 days, dt = 120 s

## paper_4floes_R1km_wind7_map.png

**Floe map: paper_4floes_R1km_wind7**  
_created 2026-11-03 13:18_

Map of the (periodic) domain. Dashed circles: floes at the start. Filled circles: floes at the last snapshot that still has ice, coloured by thickness. Grey lines: each floe's track (broken where it wraps across the box edge). Grey arrows: ocean current at the end of the run (only if non-zero).

Runs:
- `paper_4floes_R1km_wind7.nc`: 4 floe(s), radius 1 km, h0 = 1.5 m; oscillating wind, peak 7 m/s towards 45 deg, period 20 days; Ekman surface current (paper Eq. 4); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 80 days, dt = 30 s

## paper_4floes_R1km_wind7_ocean_floe1.png

**Ocean current and floe 1 track on days 5, 15: paper_4floes_R1km_wind7**  
_created 2026-11-03 13:18_

One panel per chosen day (5, 15). Blue arrows: prescribed ocean surface current at that snapshot (tiled, since the domain is periodic). Black line: track of floe 1 from the start (star) to that day, unwrapped across the box edges. Grey disc: the floe at that day, to scale. Box: wind, ocean current and floe velocity at that moment (directions in degrees from +x, anticlockwise).

Runs:
- `paper_4floes_R1km_wind7.nc`: 4 floe(s), radius 1 km, h0 = 1.5 m; oscillating wind, peak 7 m/s towards 45 deg, period 20 days; Ekman surface current (paper Eq. 4); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 80 days, dt = 30 s

## paper_drift.png

**Drift speed and direction: 'paper' runs with wind**  
_created 2026-11-03 13:18_

Top: mean floe drift speed (m/s) against time. Bottom: drift direction relative to the wind direction (degrees; negative = to the right of the wind). Directions are hidden when the wind is weaker than 0.5 m/s or the floes are nearly still.

Runs:
- `paper_4floes_R1km_wind7.nc`: 4 floe(s), radius 1 km, h0 = 1.5 m; oscillating wind, peak 7 m/s towards 45 deg, period 20 days; Ekman surface current (paper Eq. 4); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 80 days, dt = 30 s

## paper_ice.png

**Ice volume, thickness and thinning rate: 'paper' runs**  
_created 2026-11-03 13:18_

Top: total ice volume as a fraction of the initial volume. Middle: mean thickness of the ice that remains (area-weighted). Bottom: thinning rate of that mean thickness (cm/day). All against time (days).

Runs:
- `paper_4floes_R1km_nowind.nc`: 4 floe(s), radius 1 km, h0 = 1.5 m; no wind; ocean at rest; Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 80 days, dt = 120 s
- `paper_4floes_R1km_wind7.nc`: 4 floe(s), radius 1 km, h0 = 1.5 m; oscillating wind, peak 7 m/s towards 45 deg, period 20 days; Ekman surface current (paper Eq. 4); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 80 days, dt = 30 s

## paper_trajectories.png

**Floe trajectories: 'paper' runs**  
_created 2026-11-03 13:18_

Every floe's path as displacement from its starting point (km), unwrapped across the periodic boundaries so each path is one continuous line. One panel per run, same scale. Dot = last position with ice. Panel title: drift speed and angle to the wind at the last snapshot with ice.

Runs:
- `paper_4floes_R1km_nowind.nc`: 4 floe(s), radius 1 km, h0 = 1.5 m; no wind; ocean at rest; Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 80 days, dt = 120 s
- `paper_4floes_R1km_wind7.nc`: 4 floe(s), radius 1 km, h0 = 1.5 m; oscillating wind, peak 7 m/s towards 45 deg, period 20 days; Ekman surface current (paper Eq. 4); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 80 days, dt = 30 s

## windeddy_du_q.png

**Ice-ocean speed difference and heat transfer coefficient vs time (wind runs)**  
_created 2026-11-04 12:20_

Top: area-mean ice-ocean speed difference under the floe (incl. spin), cm/s. Bottom: area-mean heat transfer coefficient q. Columns: wind 3 and 7 m/s; one line per floe radius; u*_min = 0.0005 m/s. Dashed: 5.5 cm/s and q = 100 W/m2/K, where the dynamic formula equals the paper's constant.

Runs:
- `windeddy_W3_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s

## windeddy_melt_ratio.png

**Thinning-rate ratio (dynamic / constant q) vs floe radius: calm, 3 m/s, 7 m/s**  
_created 2026-11-04 12:19_

Steady thinning rate with velocity-dependent (McPhee) heat transfer divided by the rate the paper's constant q_IO = 100 W/m2/K gives (2.77 cm/day here; computed from the heat balance, since with a fixed ocean temperature it does not depend on motion). Grey: calm runs (days 2-5, if calmeddy files exist); blue: wind 3 m/s; red: wind 7 m/s (days 1-5). Circles/solid: u*_min = 0.0005 m/s; squares/dashed: 0.002 m/s.

Runs:
- `calmeddy_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `calmeddy_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; no wind; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 32 km box, 128x128 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s

## windeddy_thinning.png

**Thinning rate vs time for each floe radius (wind runs)**  
_created 2026-11-04 12:19_

Thinning rate of the floe (cm/day) against time, one panel per floe radius. Blue: wind 3 m/s; red: 7 m/s. Solid: u*_min = 0.0005 m/s; dashed: 0.002 m/s. Black line: the rate with the paper's constant q.

Runs:
- `windeddy_W3_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R1km_qdynhigh.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R2km_qdynhigh.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R4km_qdynhigh.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R8km_qdynhigh.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s

## windeddy_tracks.png

**Floe tracks over the eddy (wind runs)**  
_created 2026-11-04 12:20_

Track of the floe centre over the run for each floe radius (colours), starting at the centre of the anticyclonic eddy (background: eddy vorticity ζ/f, blue = anticyclonic). Circles: floe outlines at the end. Left: wind 3 m/s; right: 7 m/s, both towards +x. Runs with u*_min = 0.0005 m/s (the heat transfer does not affect the motion).

Runs:
- `windeddy_W3_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W3_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 3 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R1km_qdynlow.nc`: 1 floe(s), radius 1 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R2km_qdynlow.nc`: 1 floe(s), radius 2 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R4km_qdynlow.nc`: 1 floe(s), radius 4 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
- `windeddy_W7_R8km_qdynlow.nc`: 1 floe(s), radius 8 km, h0 = 1.5 m; constant wind 7 m/s towards 0 deg; anticyclonic eddy (R = 4 km, V = 0.08 m/s); Coriolis on; melting on (ocean -1 degC); 96 km box, 384x384 grid; model extended; 5 days, dt = 30 s
