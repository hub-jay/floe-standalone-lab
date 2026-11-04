# =============================================================================
# run_eddy_test.jl -- does a floe placed at the centre of an eddy stay there?
#
# Purpose: check that the grid-cell force calculation leaves no net residual
# push on a floe at the eddy centre. In a cyclonic eddy (without the tilt term)
# the centre is an unstable position under Coriolis, so any small residual push
# would be amplified and show up as the floe drifting outwards.
#
# Two runs, identical except for the eddy's sense of rotation:
#   eddytest_anticyclonic_R2km
#   eddytest_cyclonic_R2km
#
# Set-up: paper values (32 km box, 250 m grid), extended model, ONE floe of
# radius 2 km and thickness 1.5 m starting at rest at the exact centre of an
# eddy (radius 4 km, peak speed 0.08 m/s) at the domain centre.
#   ON : ocean drag from the eddy, Coriolis (as in the heat experiments)
#   OFF: wind, melting (thickness stays 1.5 m), tilt term; one floe, so no collisions
# 20 days, snapshots every 3 hours.
#
# Run from the julia> prompt, with D:\Floe as the current folder:
#     include("scripts/run_eddy_test.jl")
# Then plot with:
#     python plotting/plot_eddy_test.py
# =============================================================================
include(joinpath(@__DIR__, "driver.jl"))

T = merge(paper_config(), (
    n_side = 1, rmin = 2000.0, rmax = 2000.0,      # one 2 km floe at the domain centre
    ocean_mode = :eddy, eddy_radius = 4000.0, eddy_speed = 0.08,
    wind_speed = 0.0,                              # no wind
    thermo = false,                                # no melting
    use_tilt = false,
    use_coriolis = true,
    days = 20.0, out_every_hours = 3.0, dt = 30.0,
))

cases = [
    merge(T, (name = "eddytest_anticyclonic_R2km", eddy_sense = :anticyclonic)),
    merge(T, (name = "eddytest_cyclonic_R2km",     eddy_sense = :cyclonic)),
]

for c in cases
    run_case(c)
end
println("\nEddy test finished.")
