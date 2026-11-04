# =============================================================================
# driver.jl -- shared code for standalone runs of FloeModule.jl (Gupta, 2022)
# with a prescribed (non-evolving) ocean and atmosphere. Output -> NetCDF.
#
# Not run directly: experiment scripts do  include("driver.jl")  and then call
# run_case(config) for each case.
#
# Extensions added here (src/FloeModule.jl itself is NOT modified):
#   * Coriolis force on floes, -f k x u_i (Eq. 2 of Gupta & Thompson, 2022),
#     applied as an exact split-step rotation of floe velocity by f*dt.
#   * Prescribed ocean surface currents: at rest, Gaussian eddy, or a uniform
#     wind-driven Ekman surface current following Eq. 4 of the paper.
#   * Constant or periodic (oscillating) winds.
#   * Optional sea-surface tilt force on floes for the prescribed eddy
#     (gradient-wind balance, -g grad(eta) = f k x u_o + (u_o . grad) u_o),
#     applied as a split step like Coriolis.
#   * Diagnostics per floe: mean ice-ocean speed difference |du| and mean
#     heat transfer coefficient q under the floe.
# =============================================================================

using Pkg
Pkg.activate(joinpath(@__DIR__, ".."); io = devnull)   # this project's Julia environment

include(joinpath(@__DIR__, "..", "src", "FloeModule.jl"))      # original (Gupta, 2022), unmodified
include(joinpath(@__DIR__, "..", "src", "FloeModuleExt.jl"))   # our extended copy (changes marked inside)
using StructArrays, NCDatasets, Random, Printf

# -----------------------------------------------------------------------------
# Generic defaults (placeholder values). Experiment scripts override fields.
# -----------------------------------------------------------------------------
function base_config()
    return (
        name = "test",
        model_version = :extended,                 # :extended (src/FloeModuleExt.jl) or :original (src/FloeModule.jl)
        # --- Domain (doubly periodic box) ---
        nx = 50, ny = 50, Lx = 10_000.0, Ly = 10_000.0,
        domain_config = "DoublyPeriodic",          # or "Channel", "4Walls"
        # --- Floes: n_side x n_side regular lattice ---
        n_side = 4,
        start_offset_x = 0.0, start_offset_y = 0.0, # shift all floes from the lattice positions [m]
        rmin = 200.0, rmax = 300.0,                # radius range [m]
        hmin = 1.0,   hmax = 2.0,                  # thickness range [m]
        # --- Physical constants ---
        rho_I = 917.0, rho_O = 1025.0, rho_A = 1.3,
        Cd_IO = 5.5e-3, Cd_IA = 1.2e-3, Cd_AO = 1.2e-3,
        E = 6.0e9, nu = 0.3, er = 0.5,             # collision: Young's modulus [Pa], Poisson, restitution
        frict_fac = 0.3,
        # --- Thermodynamics (Eq. 1 of the paper) ---
        thermo = false,                            # false: thickness never changes
        Q = 200.0, alpha_I = 0.6, alpha_O = 0.1,   # shortwave [W/m2], albedos
        A = 200.0, B = 20.0,                       # longwave A + B*T [W/m2]
        q_IO = 10.0,                               # ice-ocean heat coefficient [W/m2/K] (heat_mode = :constant)
        heat_mode = :constant,                     # :constant (paper) or :dynamic (McPhee; extended model only)
        c_h = 0.006,                               # heat transfer (Stanton) coefficient for :dynamic
        cp_O = 3990.0,                             # seawater heat capacity [J/kg/K]
        ustar_min = 0.0005,                        # minimum friction velocity for :dynamic [m/s]
        Lf = 3.34e5, Tf = -1.8,                    # latent heat [J/kg], freezing T [degC]
        T_ocean = 0.0,                             # uniform ocean surface temperature [degC]
        # --- Atmosphere ---
        wind_mode = :constant,                     # :constant or :periodic
        wind_speed = 10.0,                         # [m/s] (peak speed if periodic)
        wind_dir_deg = 0.0,                        # direction the wind blows TOWARDS, deg from +x
        wind_period_days = 20.0,                   # for :periodic, u_a = U sin(2 pi t / P)
        # --- Ocean currents ---
        ocean_mode = :rest,                        # :rest, :eddy or :ekman
        eddy_sense = :cyclonic,                    # :cyclonic / :anticyclonic (relative to f)
        eddy_speed = 0.2, eddy_radius = 2000.0,    # peak azimuthal speed [m/s], radius of peak [m]
        H_ek = 3.8,                                # Ekman depth for :ekman [m] (paper's fit, Eq. 4)
        use_tilt = false,                          # sea-surface tilt force on floes (eddy only)
        # --- Rotation ---
        use_coriolis = false,
        f = 1.3e-4,                                # [1/s], 70N as in the paper
        # --- Time ---
        dt = 10.0,                                 # [s]
        days = 2.0,
        out_every_hours = 0.5,
        save_melt_cum = false,                     # save the exact cumulative melt map (one 2D map)
        seed = 1,
    )
end

# -----------------------------------------------------------------------------
# Values from Gupta & Thompson (2022), Table S1 and Section 2, for standalone use.
# Notes:
#  - rho_A is not given in the paper -> 1.225 kg/m3 (standard air density).
#  - Table S1 lists two restitution values (0.6 unlabelled, er = 0.5); er = 0.5 used.
#  - mu_f = 0.3 (dynamic friction) is used for frict_fac.
#  - Initial mixed-layer temperature -1.0 degC read from Fig. 2e (day 0).
#  - In the paper the ocean evolves (Oceananigans); here it is held fixed.
# -----------------------------------------------------------------------------
function paper_config()
    return merge(base_config(), (
        nx = 128, ny = 128, Lx = 32_000.0, Ly = 32_000.0,   # 32 km, 250 m grid
        hmin = 1.5, hmax = 1.5,                             # initial thickness
        rho_I = 1000.0, rho_O = 1027.0, rho_A = 1.225,
        Cd_IO = 5.5e-3, Cd_IA = 1.25e-3, Cd_AO = 1.25e-3,
        E = 5.0e5, nu = 0.33, er = 0.5, frict_fac = 0.3,
        thermo = true,
        Q = 300.0, alpha_I = 0.7, alpha_O = 0.4,
        A = 90.0, B = 15.0, q_IO = 100.0,
        Lf = 3.34e5, Tf = -1.8,
        T_ocean = -1.0,
        wind_speed = 0.0,          # no wind unless a case sets it (paper Sec. 3.1 runs are wind-free)
        use_coriolis = true, f = 1.3e-4,
        # dt = 30 s: explicit ice-ocean drag becomes unstable for thin, moving floes
        # when dt > rho_I*h / (rho_O*Cd_IO*|du|), i.e. dt = 120 s fails below h ~ 10 cm.
        # With dt = 30 s the scheme stays stable down to the 5 cm deletion threshold.
        dt = 30.0, days = 80.0, out_every_hours = 12.0,
    ))
end

"Which model module a case uses."
model_module(c) = c.model_version == :original ? FloeModule : FloeModuleExt

"Floe radius giving sea-ice concentration `conc` with n_side^2 equal floes."
floe_radius(conc, n_side, Lx, Ly) = sqrt(conc * Lx * Ly / (n_side^2 * π))

# -----------------------------------------------------------------------------
function make_constants(c)
    Ec, Gc, βc = model_module(c).prepareCollisionFactors(c.E, c.nu, c.er)
    th = c.thermo
    return (rho_I = c.rho_I, rho_O = c.rho_O, rho_A = c.rho_A,
            Ec = Ec, Gc = Gc, βc = βc, frict_fac = c.frict_fac,
            Cd_IO = c.Cd_IO, Cd_IA = c.Cd_IA, Cd_AO = c.Cd_AO,
            Lf = c.Lf, alpha_I = c.alpha_I, alpha_O = c.alpha_O,
            Q = th ? c.Q : 0.0, A = th ? c.A : 0.0, B = th ? c.B : 0.0,
            Tf = c.Tf, q_IO = th ? c.q_IO : 0.0,
            heat_mode = th ? c.heat_mode : :constant,
            c_h = c.c_h, cp_O = c.cp_O, ustar_min = c.ustar_min,
            domain_config = c.domain_config)
end

function make_floes(c)
    rng = MersenneTwister(c.seed)
    M = model_module(c)
    v = M.Floe[]
    dx, dy = c.Lx / c.n_side, c.Ly / c.n_side
    id = 0
    for j in 1:c.n_side, i in 1:c.n_side
        id += 1
        push!(v, M.Floe(x = dx * (i - 0.5) + c.start_offset_x, y = dy * (j - 0.5) + c.start_offset_y,
                                 r = c.rmin + (c.rmax - c.rmin) * rand(rng),
                                 h = c.hmin + (c.hmax - c.hmin) * rand(rng),
                                 ID = id))
    end
    return StructArray(v)
end

# -----------------------------------------------------------------------------
# Wind at time t [s]
# -----------------------------------------------------------------------------
function wind_at(c, t)
    U = c.wind_mode == :periodic ? c.wind_speed * sin(2π * t / (c.wind_period_days * 86400)) :
                                   c.wind_speed
    d = deg2rad(c.wind_dir_deg)
    return U * cos(d), U * sin(d)
end

# -----------------------------------------------------------------------------
# Ocean surface currents
#   :eddy  Gaussian eddy  v_theta = V (r/R) exp((1 - r^2/R^2)/2) at domain centre
#   :ekman uniform surface current |u_o| = rho_a C_ao |u_a|^2 / (rho_o f H_ek)
#          (Eq. 4 of the paper), 45 deg to the right of the wind if f > 0
# -----------------------------------------------------------------------------
function set_eddy!(m, c)
    s = sign(c.f) * (c.eddy_sense == :cyclonic ? 1.0 : -1.0)
    x0, y0 = c.Lx / 2, c.Ly / 2
    R, V = c.eddy_radius, c.eddy_speed
    for j in eachindex(m.grid.yc), i in eachindex(m.grid.xc)
        dx, dy = m.grid.xc[i] - x0, m.grid.yc[j] - y0
        r = hypot(dx, dy)
        r == 0 && continue
        vθ = V * (r / R) * exp(0.5 * (1 - r^2 / R^2))
        m.u_O[i, j] = -s * vθ * dy / r
        m.v_O[i, j] =  s * vθ * dx / r
    end
end

function set_ekman!(m, c, ua, va)
    U = hypot(ua, va)
    if U == 0
        m.u_O .= 0.0; m.v_O .= 0.0; return
    end
    uo = c.rho_A * c.Cd_AO * U^2 / (c.rho_O * abs(c.f) * c.H_ek)
    φ = atan(va, ua) - sign(c.f) * π / 4
    m.u_O .= uo * cos(φ)
    m.v_O .= uo * sin(φ)
end

# -----------------------------------------------------------------------------
# Coriolis split step: exact solution of du/dt = f v, dv/dt = -f u over dt
# -----------------------------------------------------------------------------
function apply_coriolis!(floes, f, dt)
    cθ, sθ = cos(f * dt), sin(f * dt)
    @inbounds for i in eachindex(floes.u)
        u, v = floes.u[i], floes.v[i]
        floes.u[i] =  u * cθ + v * sθ
        floes.v[i] = -u * sθ + v * cθ
    end
end

# -----------------------------------------------------------------------------
# Sea-surface tilt for a steady, balanced prescribed eddy (gradient-wind balance)
#   tilt acceleration  a = -g grad(eta) = f k x u_o + (u_o . grad) u_o
#     a_x = -f v_o + u_o du_o/dx + v_o du_o/dy
#     a_y =  f u_o + u_o dv_o/dx + v_o dv_o/dy
# computed once on the grid (centred differences, periodic), then averaged over
# the area under each floe and added to its velocity every step (split step).
# Together with the Coriolis step this makes Coriolis act on the floe's velocity
# RELATIVE to the water.
# -----------------------------------------------------------------------------
function tilt_field(m, c)
    u, v = m.u_O, m.v_O
    Δ = c.Lx / c.nx
    ddx(a) = (circshift(a, (-1, 0)) .- circshift(a, (1, 0))) ./ (2Δ)
    ddy(a) = (circshift(a, (0, -1)) .- circshift(a, (0, 1))) ./ (2Δ)
    ax = .-c.f .* v .+ u .* ddx(u) .+ v .* ddy(u)
    ay =   c.f .* u .+ u .* ddx(v) .+ v .* ddy(v)
    return ax, ay
end

function apply_tilt!(m, ax, ay, dt, M)
    fl = m.floes
    acc = Dict{Int, Tuple{Float64, Float64}}()
    for i in eachindex(fl.ID)                      # area-mean tilt under each ORIGINAL floe
        fl.ID[i] > 0 || continue
        _, _, idx, w = M.FloeAreaRatio(fl.x[i], fl.y[i], fl.r[i], m.grid.xg, m.grid.yg)
        sw = sum(w)
        sw > 0 || continue
        acc[fl.ID[i]] = (sum(ax[idx] .* w) / sw, sum(ay[idx] .* w) / sw)
    end
    for i in eachindex(fl.ID)                      # same push for the floe and its periodic copy
        a = get(acc, abs(fl.ID[i]), nothing)
        a === nothing && continue
        fl.u[i] += a[1] * dt
        fl.v[i] += a[2] * dt
    end
end

# -----------------------------------------------------------------------------
# Diagnostics: area-mean |du| (ice-ocean speed difference, incl. spin) and heat
# transfer coefficient q under each original floe, same formulas as the model.
# -----------------------------------------------------------------------------
function floe_diag!(S, k, m, M)
    fl, mc = m.floes, m.mc
    for i in eachindex(fl.ID)
        id = fl.ID[i]
        (1 <= id <= size(S.x, 1)) || continue
        xidx, yidx, idx, w = M.FloeAreaRatio(fl.x[i], fl.y[i], fl.r[i], m.grid.xg, m.grid.yg)
        sw = sum(w)
        sw > 0 || continue
        lx = m.grid.xc[xidx] .- fl.x[i]
        ly = m.grid.yc[yidx] .- fl.y[i]
        du = (fl.u[i] .- ly .* fl.ζ[i]) .- m.u_O[idx]
        dv = (fl.v[i] .+ lx .* fl.ζ[i]) .- m.v_O[idx]
        sp = sqrt.(du .^ 2 .+ dv .^ 2)
        q = get(mc, :heat_mode, :constant) == :dynamic ?
            mc.rho_O * mc.cp_O * mc.c_h .* max.(sqrt(mc.Cd_IO) .* sp, mc.ustar_min) :
            fill(mc.q_IO, length(sp))
        S.du[id, k] = sum(sp .* w) / sw
        S.q[id, k]  = sum(q .* w) / sw
    end
end

# -----------------------------------------------------------------------------
# Snapshot of original floes (periodic copies have negative IDs) and fields
# -----------------------------------------------------------------------------
function snapshot!(S, k, m, M)
    fl = m.floes
    for i in eachindex(fl.ID)
        id = fl.ID[i]
        (1 <= id <= size(S.x, 1)) || continue
        S.x[id, k] = fl.x[i];  S.y[id, k] = fl.y[i]
        S.u[id, k] = fl.u[i];  S.v[id, k] = fl.v[i]
        S.ζ[id, k] = fl.ζ[i];  S.θ[id, k] = fl.θ[i]
        S.r[id, k] = fl.r[i];  S.h[id, k] = fl.h[i]
        S.col[id, k] = fl.collision[i] ? 1.0 : 0.0
    end
    S.sic[:, :, k]  .= m.SIfract
    S.taux[:, :, k] .= m.taux
    S.tauy[:, :, k] .= m.tauy
    S.hflx[:, :, k] .= m.hflx
    S.melt[:, :, k] .= m.melt_rate .* (m.SIfract .> 0)   # only where there is ice now
    S.uO[:, :, k]   .= m.u_O
    S.vO[:, :, k]   .= m.v_O
    S.ua[k] = m.u_A[1, 1];  S.va[k] = m.v_A[1, 1]
    S.uo[k] = sum(m.u_O) / length(m.u_O);  S.vo[k] = sum(m.v_O) / length(m.v_O)
    floe_diag!(S, k, m, M)
end

# -----------------------------------------------------------------------------
# Run one case and write output/<name>.nc
# -----------------------------------------------------------------------------
function run_case(c)
    Random.seed!(c.seed)
    mc    = make_constants(c)
    M     = model_module(c)
    grid  = M.FloeGrid(size = (c.nx, c.ny), extent = (c.Lx, c.Ly))
    floes = make_floes(c)
    m     = M.FloeModel(floes = floes, mc = mc, grid = grid, Δt = c.dt)
    m.T_O .= c.T_ocean

    ua, va = wind_at(c, 0.0)
    m.u_A .= ua; m.v_A .= va
    c.ocean_mode == :eddy  && set_eddy!(m, c)
    c.ocean_mode == :ekman && set_ekman!(m, c, ua, va)
    tilt = (c.use_tilt && c.ocean_mode == :eddy) ? tilt_field(m, c) : nothing

    N      = c.n_side^2
    nsteps = round(Int, c.days * 86400 / c.dt)
    every  = max(1, round(Int, c.out_every_hours * 3600 / c.dt))
    nsnap  = nsteps ÷ every + 1
    nanF() = fill(NaN, N, nsnap)
    nanG() = fill(NaN, c.nx, c.ny, nsnap)
    S = (x = nanF(), y = nanF(), u = nanF(), v = nanF(), ζ = nanF(), θ = nanF(),
         r = nanF(), h = nanF(), col = nanF(), du = nanF(), q = nanF(),
         sic = nanG(), taux = nanG(), tauy = nanG(), hflx = nanG(), melt = nanG(),
         uO = nanG(), vO = nanG(),
         ua = fill(NaN, nsnap), va = fill(NaN, nsnap), uo = fill(NaN, nsnap), vo = fill(NaN, nsnap))
    tsec = collect(0:nsnap-1) .* (every * c.dt)    # snapshot times [s] (filled even if all ice melts early)
    melt_cum = zeros(c.nx, c.ny)                   # exact cumulative melt in each cell [m], summed every step

    println("\n=== Case: $(c.name) ===")
    println("  Model version: ", c.model_version, c.model_version == :original ? " (src/FloeModule.jl)" : " (src/FloeModuleExt.jl)")
    @printf("  %d floe(s), radius %.0f-%.0f m, %.0f days, dt = %.0f s, Coriolis = %s, wind = %s %.1f m/s, ocean = %s, thermo = %s\n",
            N, c.rmin, c.rmax, c.days, c.dt, c.use_coriolis, c.wind_mode, c.wind_speed, c.ocean_mode, c.thermo)
    c.ocean_mode == :eddy && @printf("  eddy: %s, R = %.0f m, V = %.3f m/s, tilt = %s\n",
                                     c.eddy_sense, c.eddy_radius, c.eddy_speed, tilt !== nothing)
    if c.thermo
        if c.heat_mode == :dynamic && c.model_version != :original
            println("  heat transfer: dynamic (c_h = $(c.c_h), ustar_min = $(c.ustar_min) m/s)")
        else
            println("  heat transfer: constant (q_IO = $(c.q_IO) W/m2/K)")
        end
    end

    snapshot!(S, 1, m, M)
    k = 1
    t0 = time()
    for step in 1:nsteps
        t = step * c.dt
        if c.wind_mode == :periodic
            ua, va = wind_at(c, t)
            m.u_A .= ua; m.v_A .= va
            c.ocean_mode == :ekman && set_ekman!(m, c, ua, va)
        end
        M.timestepAtm!(m)
        M.timestepFloes!(m)
        c.use_coriolis && apply_coriolis!(m.floes, c.f, c.dt)
        tilt === nothing || apply_tilt!(m, tilt[1], tilt[2], c.dt, M)
        c.save_melt_cum && (melt_cum .+= m.melt_rate .* (m.SIfract .> 0) .* c.dt)   # only cells with ice this step

        if step % every == 0
            k += 1
            tsec[k] = t
            snapshot!(S, k, m, M)
        end
        if step % max(1, nsteps ÷ 10) == 0
            @printf("  %3d%% done (model day %.1f, %.0f s elapsed, %d floes left)\n",
                    round(Int, 100 * step / nsteps), t / 86400, time() - t0, count(>(0), m.floes.ID))
        end
        count(>(0), m.floes.ID) == 0 && (println("  All floes melted at day ", round(t/86400, digits=1)); break)
    end

    orig = m.floes.ID .> 0
    if count(orig) > 0
        ub, vb = sum(m.floes.u[orig]) / count(orig), sum(m.floes.v[orig]) / count(orig)
        uaE, vaE = wind_at(c, nsteps * c.dt)
        ang = hypot(uaE, vaE) > 0 ? rad2deg(atan(vb, ub) - atan(vaE, uaE)) : NaN
        ang = mod(ang + 180, 360) - 180
        @printf("  End: %d of %d floes left, mean thickness %.2f m, mean drift %.3f m/s, %+.1f deg from wind (negative = right)\n",
                count(orig), N, sum(m.floes.h[orig]) / count(orig), hypot(ub, vb), ang)
    end
    write_netcdf(c, m, S, tsec, melt_cum)
end

function write_netcdf(c, m, S, tsec, melt_cum)
    outdir = joinpath(@__DIR__, "..", "output")
    mkpath(outdir)
    path = joinpath(outdir, c.name * ".nc")
    isfile(path) && rm(path)
    NCDataset(path, "c") do ds
        for (k, v) in pairs(c)
            ds.attrib[string(k)] = v isa Bool ? Int(v) : v isa Symbol ? string(v) : v
        end
        ds.attrib["source"] = (c.model_version == :original ? "FloeModule.jl" : "FloeModuleExt.jl (extended copy of FloeModule.jl)") *
                              " (Gupta, 2022; doi:10.5281/zenodo.6578706) driven by scripts/driver.jl"
        defVar(ds, "time", tsec, ("time",), attrib = Dict("units" => "s"))
        defVar(ds, "x", collect(m.grid.xc), ("x",), attrib = Dict("units" => "m"))
        defVar(ds, "y", collect(m.grid.yc), ("y",), attrib = Dict("units" => "m"))
        defVar(ds, "floe", collect(1:size(S.x, 1)), ("floe",), attrib = Dict("long_name" => "floe ID"))
        fv = [("floe_x", S.x, "m", "floe centre x"), ("floe_y", S.y, "m", "floe centre y"),
              ("floe_u", S.u, "m s-1", "floe velocity x"), ("floe_v", S.v, "m s-1", "floe velocity y"),
              ("floe_zeta", S.ζ, "s-1", "floe rotation rate"), ("floe_theta", S.θ, "rad", "floe angle"),
              ("floe_r", S.r, "m", "floe radius"), ("floe_h", S.h, "m", "floe thickness"),
              ("floe_collision", S.col, "1", "1 if floe in collision"),
              ("floe_du", S.du, "m s-1", "area-mean ice-ocean speed difference under floe (incl. spin)"),
              ("floe_q", S.q, "W m-2 K-1", "area-mean ice-ocean heat transfer coefficient under floe")]
        for (name, data, units, ln) in fv
            defVar(ds, name, data, ("floe", "time"), attrib = Dict("units" => units, "long_name" => ln))
        end
        gv = [("sic", S.sic, "1", "sea-ice fraction"),
              ("taux", S.taux, "N m-2", "net x-stress on ocean"),
              ("tauy", S.tauy, "N m-2", "net y-stress on ocean"),
              ("hflx", S.hflx, "W m-2", "net surface heat flux into ocean"),
              ("melt_rate", S.melt, "m s-1", "ice melt rate"),
              ("u_ocean_t", S.uO, "m s-1", "ocean surface current x (prescribed)"),
              ("v_ocean_t", S.vO, "m s-1", "ocean surface current y (prescribed)")]
        for (name, data, units, ln) in gv
            defVar(ds, name, data, ("x", "y", "time"), attrib = Dict("units" => units, "long_name" => ln))
        end
        tv = [("wind_u", S.ua, "m s-1"), ("wind_v", S.va, "m s-1"),
              ("ocean_u_mean", S.uo, "m s-1"), ("ocean_v_mean", S.vo, "m s-1")]
        for (name, data, units) in tv
            defVar(ds, name, data, ("time",), attrib = Dict("units" => units))
        end
        c.save_melt_cum && defVar(ds, "melt_cum", melt_cum, ("x", "y"),
               attrib = Dict("units" => "m", "long_name" =>
                   "cumulative melt in each cell over the run (cell-area weighted: divide by ice cover for local thinning)"))
        defVar(ds, "u_ocean", m.u_O, ("x", "y"), attrib = Dict("units" => "m s-1", "long_name" => "ocean u at end"))
        defVar(ds, "v_ocean", m.v_O, ("x", "y"), attrib = Dict("units" => "m s-1", "long_name" => "ocean v at end"))
    end
    println("  Saved: ", normpath(path))
end
