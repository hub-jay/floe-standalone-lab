# =============================================================================
# run_tilt_check_long_with_eddy.jl -- the 3 m/s wind case of
# run_tilt_check_with_eddy.jl, run for 15 days instead of 5, to see whether the
# floe eventually leaves the anticyclonic eddy with the sea-surface tilt term
# (in 5 days it loops between the centre and ~4 km).
#
# Same set-up as the "wind3" runs there; only the length (15 days) and the
# snapshot interval (6 h, to keep the files ~0.5 GB each) differ.
#
# Output:  output/tiltcheck_wind3_15d_<version>.nc   (3 files)
# Plot:    python plotting/plot_tilt_check_with_eddy.py
#          (makes figures/tiltcheck_wind3_15d.png as well as tiltcheck.png)
#
# Run from the julia> prompt, with D:\Floe as the current folder:
#     include("scripts/run_tilt_check_long_with_eddy.jl")
# =============================================================================
include(joinpath(@__DIR__, "driver.jl"))

B = merge(paper_config(), (
    n_side = 1, rmin = 2000.0, rmax = 2000.0,      # one 2 km floe
    ocean_mode = :eddy, eddy_sense = :anticyclonic,
    eddy_radius = 4000.0, eddy_speed = 0.08,
    thermo = false,                                # motion only
    use_coriolis = true,
    wind_mode = :constant, wind_speed = 3.0, wind_dir_deg = 0.0,
    nx = 384, ny = 384, Lx = 96_000.0, Ly = 96_000.0,
    days = 15.0, out_every_hours = 6.0, dt = 30.0,
))

VERSIONS = [
    ("origdrag",     (model_version = :original, use_tilt = false)),
    ("vecdrag",      (model_version = :extended, use_tilt = false)),
    ("vecdrag_tilt", (model_version = :extended, use_tilt = true)),
]

cases = [merge(B, vs, (name = "tiltcheck_wind3_15d_$(vl)",)) for (vl, vs) in VERSIONS]

println("Running $(length(cases)) long (15-day) tilt / drag check runs")
for (n, c) in enumerate(cases)
    println("\n[$n / $(length(cases))]")
    run_case(c)
end
println("\nLong tilt / drag check finished.")
