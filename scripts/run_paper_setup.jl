# =============================================================================
# run_paper_setup.jl -- standalone versions of the Gupta & Thompson (2022)
# experiments, using the parameter values of their Table S1 (see paper_config()
# in driver.jl). 32 km doubly periodic box, 250 m grid, f = 1.3e-4 s-1,
# 20% ice concentration, initial thickness 1.5 m, ocean surface at -1.0 degC.
#
# IMPORTANT: the ocean here is PRESCRIBED (fixed temperature and currents).
# In the paper it evolves in Oceananigans. These runs are therefore the
# "no ocean dynamics" reference: any difference from the paper's melt rates
# is due to the ocean eddies and the ocean cooling/warming the paper resolves.
#
# Run from the julia> prompt, with D:\Floe as the current folder:
#     include("scripts/run_paper_setup.jl")
# Output: output/paper_*.nc   (each case takes a few minutes)
# =============================================================================
include(joinpath(@__DIR__, "driver.jl"))

P = paper_config()
# Floe radii as stated in the paper (Rf = 8, 2, 1 km). This gives an ice
# concentration of 19.6%, i.e. the paper's "20%" (exactly 20% would need
# R = 8.07, 2.02, 1.01 km; use floe_radius(0.2, n_side, P.Lx, P.Ly) for that).

cases = [
    # Both cases: 4 floes (2 x 2 layout, 16 km apart), radius 1 km (2 km diameter, the
    # paper's smallest floes), initial thickness 1.5 m. Ice concentration is only ~1%
    # (the paper uses ~20%); that does not matter here, because the ocean is prescribed
    # and the floes are far apart, so each floe behaves independently. Small floes also
    # keep the periodic-boundary "corner" limitation of the module negligible (a floe is
    # only partly counted when it overlaps two box edges at once).

    # 1. No wind, ocean at rest: melting check.
    #    Expected: floes stay put, uniform thinning ~2.8 cm/day, all ice gone ~day 53.
    #    (nothing moves, so the larger dt = 120 s is safe and 4x faster)
    merge(P, (name = "paper_4floes_R1km_nowind", n_side = 2, rmin = 1000.0, rmax = 1000.0,
              dt = 120.0)),

    # 2. Wind (paper Section 3.3): oscillating along the NE-SW axis, 20-day period, peak
    #    7 m/s (as in Movie S7); ocean surface current from the paper's Ekman scaling
    #    (Eq. 4, H_ek = 3.8 m), 45 deg to the right of the wind. dt = 30 s (paper_config).
    merge(P, (name = "paper_4floes_R1km_wind7", n_side = 2, rmin = 1000.0, rmax = 1000.0,
              wind_mode = :periodic, wind_speed = 7.0, wind_dir_deg = 45.0,
              wind_period_days = 20.0, ocean_mode = :ekman)),
]

for c in cases
    run_case(c)
end
println("\nAll paper-setup runs finished.")
