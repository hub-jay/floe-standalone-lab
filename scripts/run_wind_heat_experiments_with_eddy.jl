# =============================================================================
# run_wind_heat_experiments_with_eddy.jl -- 16 wind runs: velocity-dependent
# ice-ocean heat transfer for ONE floe starting at the centre of ONE eddy,
# with a steady wind that blows it out of the eddy.
#
# Question: with wind-driven slip between floe and water, how does the melt
# with velocity-dependent (McPhee) heat transfer compare with the paper's
# constant q_IO, and how does that depend on wind speed and floe size?
#
# Common set-up (all 16 runs), as in run_calm_heat_experiments_with_eddy.jl except:
#   * steady wind towards +x (east): 3 or 7 m/s
#   * 96 km doubly periodic box, 250 m grid (384 x 384), so the drifting floe
#     stays clear of the box edges for the whole run (at 7 m/s the floe drifts
#     roughly 7 km/day east and 4.5 km/day south)
#   * 5 days (as the calm runs; the floe adjusts to the wind within hours, and
#     5 days shows whether floes held by the eddy at 3 m/s eventually escape),
#     snapshots every 6 h; steady thinning rate measured over days 1-5
#   * no cumulative-melt map (the floe moves across the grid)
# Unchanged: paper values (Table S1), extended model (vector drag), Coriolis on,
#   ocean at -1.0 degC; anticyclonic eddy at the box centre (R = 4 km,
#   V = 0.08 m/s); floe 1.5 m thick, starting at rest at the eddy centre.
#
# Varied:  wind 3, 7 m/s  x  floe radius 1, 2, 4, 8 km  x  heat transfer
#            qdynlow  : dynamic (McPhee), u*_min = 0.0005 m/s
#            qdynhigh : dynamic (McPhee), u*_min = 0.002 m/s
# No constant-q runs: with a constant q and a fixed ocean temperature the melt
# rate does not depend on motion, so it equals the calm constant-q value
# (2.77 cm/day); the plotting script computes it from the same formula.
#
# Output:  output/windeddy_W<wind>_R<radius>km_<heat>.nc   (16 files)
# Plot:    python plotting/plot_wind_heat_experiments_with_eddy.py
#
# Run from the julia> prompt, with D:\Floe as the current folder:
#     include("scripts/run_wind_heat_experiments_with_eddy.jl")
# =============================================================================
include(joinpath(@__DIR__, "driver.jl"))

E = merge(paper_config(), (
    n_side = 1,                                    # one floe at the domain (= eddy) centre
    nx = 384, ny = 384, Lx = 96_000.0, Ly = 96_000.0,   # 96 km box, 250 m grid
    ocean_mode = :eddy, eddy_sense = :anticyclonic,
    eddy_radius = 4000.0, eddy_speed = 0.08,
    wind_mode = :constant, wind_dir_deg = 0.0,     # steady wind towards +x
    days = 5.0, out_every_hours = 6.0,
    save_melt_cum = false,
))

HEAT = [
    ("qdynlow",  (heat_mode = :dynamic, ustar_min = 0.0005)),
    ("qdynhigh", (heat_mode = :dynamic, ustar_min = 0.002)),
]
WINDS = [3, 7]
RADII_KM = [1, 2, 4, 8]

cases = [merge(E, hs, (name = "windeddy_W$(W)_R$(Rkm)km_$(hl)",
                       wind_speed = Float64(W),
                       rmin = 1000.0 * Rkm, rmax = 1000.0 * Rkm))
         for W in WINDS for Rkm in RADII_KM for (hl, hs) in HEAT]

println("Running $(length(cases)) wind heat experiments with an eddy")
for (n, c) in enumerate(cases)
    println("\n[$n / $(length(cases))]")
    run_case(c)
end
println("\nAll wind heat experiments finished.")
