# =============================================================================
# run_free_drift_check.jl -- quick check: free drift under a uniform 10 m/s wind.
#   1. no Coriolis                         (extended model)
#   2. Coriolis, ORIGINAL module           (component-wise drag -> ~25 deg)
#   3. Coriolis, EXTENDED module           (vector drag, Eq. 2  -> ~12 deg)
#
# Run from the julia> prompt, with D:\Floe as the current folder:
#     include("scripts/run_free_drift_check.jl")
# =============================================================================
include(joinpath(@__DIR__, "driver.jl"))

cases = [
    merge(base_config(), (name = "free_drift_no_coriolis",         use_coriolis = false)),
    merge(base_config(), (name = "free_drift_coriolis_original",   use_coriolis = true, model_version = :original)),
    merge(base_config(), (name = "free_drift_coriolis_extended",   use_coriolis = true, model_version = :extended)),
]

for c in cases
    run_case(c)
end
println("\nAll runs finished.")
