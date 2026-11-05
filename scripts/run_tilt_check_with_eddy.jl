# =============================================================================
# run_tilt_check_with_eddy.jl -- does a floe stay in an anticyclonic eddy because
# of eddy physics, or because of how the model treats drag and Coriolis?
#
# Two numerical choices in the published formulation could both favour the
# retention of floes in anticyclones:
#   * component-wise quadratic drag (published module), which is too weak for
#     motion oblique to the grid axes, i.e. for most of a floe's circular path,
#     so it resists the floe's inward drift less;
#   * no sea-surface tilt term (paper's Eq. 2), so Coriolis on a floe circling
#     an anticyclone is unbalanced and pushes it inwards. With the tilt term,
#     Coriolis effectively acts on the floe's velocity RELATIVE to the water.
#
# Three versions, compared in two set-ups (6 runs):
#   origdrag      original module (component-wise drag), no tilt
#   vecdrag       extended module (vector drag, Eq. 2), no tilt
#   vecdrag_tilt  extended module (vector drag) + sea-surface tilt
#                 (gradient-wind balance, see driver.jl: tilt_field)
#
#   calm_off4km : no wind; floe starts at rest 4 km east of the eddy centre
#                 (at the eddy's peak speed); 32 km box
#   wind3       : steady 3 m/s wind towards +x; floe starts at rest at the eddy
#                 centre; 96 km box (as the wind heat experiments)
#
# Common: anticyclonic eddy at the box centre (R = 4 km, V = 0.08 m/s), one floe
# of radius 2 km and thickness 1.5 m, paper values, Coriolis on, MELTING OFF
# (motion only; also keeps the floes' mass identical in all versions),
# 5 days, snapshots every 3 h.
#
# Output:  output/tiltcheck_<setup>_<version>.nc   (6 files)
# Plot:    python plotting/plot_tilt_check_with_eddy.py
#
# Run from the julia> prompt, with D:\Floe as the current folder:
#     include("scripts/run_tilt_check_with_eddy.jl")
# =============================================================================
include(joinpath(@__DIR__, "driver.jl"))

B = merge(paper_config(), (
    n_side = 1, rmin = 2000.0, rmax = 2000.0,      # one 2 km floe
    ocean_mode = :eddy, eddy_sense = :anticyclonic,
    eddy_radius = 4000.0, eddy_speed = 0.08,
    thermo = false,                                # motion only
    use_coriolis = true,
    days = 5.0, out_every_hours = 3.0, dt = 30.0,
))

SETUPS = [
    ("calm_off4km", (wind_speed = 0.0, start_offset_x = 4000.0)),
    ("wind3",       (wind_mode = :constant, wind_speed = 3.0, wind_dir_deg = 0.0,
                     nx = 384, ny = 384, Lx = 96_000.0, Ly = 96_000.0)),
]
VERSIONS = [
    ("origdrag",     (model_version = :original, use_tilt = false)),
    ("vecdrag",      (model_version = :extended, use_tilt = false)),
    ("vecdrag_tilt", (model_version = :extended, use_tilt = true)),
]

cases = [merge(B, ss, vs, (name = "tiltcheck_$(sl)_$(vl)",))
         for (sl, ss) in SETUPS for (vl, vs) in VERSIONS]

println("Running $(length(cases)) tilt / drag check runs")
for (n, c) in enumerate(cases)
    println("\n[$n / $(length(cases))]")
    run_case(c)
end
println("\nTilt / drag check finished.")
