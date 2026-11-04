# =============================================================================
# run_calm_heat_experiments_with_eddy.jl -- 12 calm runs: velocity-dependent vs
# constant ice-ocean heat transfer for ONE floe at the centre of ONE eddy.
#
# Question: if ice-ocean heat transfer depends on the floe's motion relative to
# the water (McPhee bulk formula), how does the melt of a floe carried by an
# eddy differ from the paper's constant q_IO, and how does that depend on the
# floe's size relative to the eddy?
#
# Common set-up (all 12 runs):
#   * Gupta & Thompson (2022) Table S1 values (paper_config), extended model
#     (vector drag), Coriolis on, NO wind, ocean temperature fixed at -1.0 degC
#   * 32 km doubly periodic box, 250 m grid
#   * ONE floe (1.5 m thick), starting at rest at the centre of ONE eddy at the
#     domain centre
#   * eddy: anticyclonic (where the paper finds coupled floes reside), radius
#     R = 4 km (~ mixed-layer deformation radius R_d = 3.8 km in the paper), peak
#     speed V = 0.08 m/s, i.e. core vorticity zeta = 3.3 V / R ~ 6.6e-5 1/s,
#     zeta/f ~ 0.5 (strong end of the paper's Fig. 2c)
#   * 5 days (floes spin up within ~1 day; the melt rate is then steady),
#     snapshots every 6 hours, exact cumulative melt map saved (melt_cum)
#
# Varied:  floe radius 1, 2, 4, 8 km  x  heat transfer
#            qconst   : constant q_IO = 100 W/m2/K (paper)
#            qdynlow  : dynamic (McPhee), u*_min = 0.0005 m/s
#            qdynhigh : dynamic (McPhee), u*_min = 0.002 m/s
#
# Output:  output/calmeddy_R<radius>km_<heat>.nc   (12 files)
# Plot:    python plotting/plot_calm_heat_experiments_with_eddy.py
#
# Run from the julia> prompt, with D:\Floe as the current folder:
#     include("scripts/run_calm_heat_experiments_with_eddy.jl")
# =============================================================================
include(joinpath(@__DIR__, "driver.jl"))

E = merge(paper_config(), (
    n_side = 1,                                    # one floe at the domain (= eddy) centre
    ocean_mode = :eddy, eddy_sense = :anticyclonic,
    eddy_radius = 4000.0, eddy_speed = 0.08,
    wind_speed = 0.0,                              # calm
    days = 5.0, out_every_hours = 6.0,
    save_melt_cum = true,                          # exact cumulative melt map in each cell
))

HEAT = [
    ("qconst",   (heat_mode = :constant,)),
    ("qdynlow",  (heat_mode = :dynamic, ustar_min = 0.0005)),
    ("qdynhigh", (heat_mode = :dynamic, ustar_min = 0.002)),
]
RADII_KM = [1, 2, 4, 8]

cases = [merge(E, hs, (name = "calmeddy_R$(Rkm)km_$(hl)",
                       rmin = 1000.0 * Rkm, rmax = 1000.0 * Rkm))
         for Rkm in RADII_KM for (hl, hs) in HEAT]

println("Running $(length(cases)) calm heat experiments with an eddy")
for (n, c) in enumerate(cases)
    println("\n[$n / $(length(cases))]")
    run_case(c)
end
println("\nAll calm heat experiments finished.")
