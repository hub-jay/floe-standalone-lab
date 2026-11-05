# floe-standalone-lab: full details

*Short summary: [README.md](README.md).*

Standalone experiments with the discrete-element sea-ice floe model **FloeModule.jl**
of Gupta & Thompson (2022), run with a prescribed (non-evolving) ocean and atmosphere.
The main experiment tests **velocity-dependent ice–ocean heat transfer** for floes
carried by an ocean eddy.

**Author details:** Claude wrote it. Jayasankar T. Pillai kept asking “but why?” until it was right.

*Division of labour:* Jayasankar chose the questions, designed and steered the
experiments, asked the awkward physics questions, spotted the results that didn't add
up, and takes responsibility for everything here. Claude, an AI assistant (Anthropic),
wrote the code, did the arithmetic, talked through the physics at every "but why?",
and was occasionally talked out of a bad idea.

## Credit

`src/FloeModule.jl` is the original, unmodified code by **Mukund Gupta**:

> Gupta, M. (2022). *Sea Ice Circular Floe Code* (v1). Zenodo.
> https://doi.org/10.5281/zenodo.6578706 (CC-BY-4.0)

used in

> Gupta, M., & Thompson, A. F. (2022). Regimes of sea-ice floe melt: Ice-ocean coupling
> at the submesoscales. *Journal of Geophysical Research: Oceans*, 127, e2022JC018894.
> https://doi.org/10.1029/2022JC018894

`src/FloeModuleExt.jl` is an extended copy of it (changes listed below and marked
in the code). Everything else (driver, run scripts, plotting) is new.


## What is added

### Extended model: `src/FloeModuleExt.jl`

Every change is marked in the code as `CHANGE n: BEFORE (original)` (original lines,
commented out) / `CHANGE n: AFTER (modified)`.

| Change | What | Why |
|---|---|---|
| 0 | module renamed `FloeModuleExt` | so the original and the extended copy can be loaded together |
| 1–3 | ice–ocean drag, wind drag on floes and wind stress on open water use the **vector** quadratic law of Eq. 2, τ = ρC\|Δ**u**\|Δ**u** | the published module computes drag component-wise (τx = ρCΔu\|Δu\|, τy = ρCΔv\|Δv\|), which underestimates drag for motion oblique to the grid axes (by up to ~29% at 45°) and makes results depend on grid orientation |
| 4 | collision chord-length fallback uses the floe radii `f.r1`, `f.r2` | the original refers to undefined variables `r1`, `r2`, so a run stops with an error when this branch is reached (when one floe overlaps so far that it lies entirely inside the other, where the chord-length formula has no real solution; in practice only after a numerical blow-up) |
| 5 | in `collideTwoFloes!`, the collision force and torque are **added** to the floe's force and torque (`+=`) | the original assigns them (`=`), overwriting the ocean and wind drag already stored for that floe in the same time step; a colliding floe therefore feels only the collision, and when it touches several floes at once only the last collision counts. Wall collisions in the same module already use `+=` |
| 6 | optional **velocity-dependent ice–ocean heat transfer** (`heat_mode = :dynamic`) | see below; `heat_mode = :constant` keeps the paper's fixed q_IO |

Changes 4 and 5 only matter when floes collide. None of the experiments below involve
floe–floe collisions (single floes, or floes far apart), so their results are not affected;
the fixes are there for runs with packed, interacting floes.

**Velocity-dependent heat transfer (CHANGE 6).** In each grid cell under a floe,

  q = ρ_o c_p c_h u\*,  u\* = max(√C_io |Δ**u**|, u\*_min),  ocean heat flux = q (T_o − T_f)

with ocean density ρ_o, seawater heat capacity c_p = 3990 J kg⁻¹ K⁻¹, heat transfer
(Stanton) coefficient c_h = 0.006 (McPhee), ice–ocean drag coefficient C_io, local
ice–ocean velocity difference |Δ**u**| (including the floe's spin; the same quantity
used for the drag), and a minimum friction velocity u\*_min. The paper's constant
q_IO = 100 W m⁻² K⁻¹ corresponds to |Δ**u**| ≈ 5.5 cm/s. Everything after q (heat
balance, thickness change, single floe thickness) is the original code.

### Driver: `scripts/driver.jl`

- **Coriolis force on floes**, −ρᵢhᵢ f k̂ × **u**ᵢ (Eq. 2 of the paper; not in the
  published module), applied as an exact split-step rotation of the floe velocity.
- **Prescribed ocean currents**: at rest; a Gaussian eddy (cyclonic or anticyclonic);
  or a uniform wind-driven Ekman surface current (Eq. 4 of the paper).
- **Constant or oscillating winds.**
- **Optional sea-surface tilt force** on floes in a prescribed eddy (gradient-wind
  balance, −g∇η = f k̂ × **u**ₒ + (**u**ₒ·∇)**u**ₒ), off by default.
- **Diagnostics**: area-mean ice–ocean speed difference and heat transfer coefficient
  under each floe; optional exact cumulative melt map.
- **Choice of model** per run: `model_version = :extended` (default) or `:original`.
- **NetCDF output** in `output/`; every figure is listed in `figures/FIGURES.md`.

## Layout

```
src/FloeModule.jl                          original model (unmodified)
src/FloeModuleExt.jl                       extended copy (changes marked BEFORE/AFTER)
scripts/driver.jl                          shared run code
scripts/run_free_drift_check.jl            free drift: no Coriolis / Coriolis, original vs extended drag
scripts/run_paper_setup.jl                 paper parameters: melting check, oscillating-wind case
scripts/run_eddy_test.jl                   floe at the centre of an eddy: does it stay there?
scripts/run_calm_heat_experiments_with_eddy.jl   12 runs: heat transfer, calm (5 days)
scripts/run_wind_heat_experiments_with_eddy.jl   16 runs: heat transfer, 3 and 7 m/s wind (5 days)
scripts/run_tilt_check_with_eddy.jl              6 runs: drag formulation and tilt, calm and 3 m/s
scripts/run_tilt_check_long_with_eddy.jl         3 runs: the 3 m/s tilt check over 15 days
plotting/plot_*.py                         one plotting script per experiment set (+ plot_run.py, generic)
plotting/figindex.py                       writes the figure catalogue figures/FIGURES.md
figures/                                   figures and their catalogue
setup.jl, Project.toml, Manifest.toml      Julia environment
LICENSE                                    MIT licence (own code); Gupta's code is CC-BY-4.0
plotting/requirements.txt                  Python packages
```

## How to run

**Julia** (Julia 1.10 or later). First time only, from the `julia>` prompt in this folder:
```julia
include("setup.jl")
```
Then run any experiment set, e.g.
```julia
include("scripts/run_calm_heat_experiments_with_eddy.jl")
```

**Python** (first time only):
```
python -m venv .venv
.venv\Scripts\activate            # Windows; on macOS/Linux: source .venv/bin/activate
pip install -r plotting/requirements.txt
```
Then the matching plotting script, e.g.
```
python plotting/plot_calm_heat_experiments_with_eddy.py
```
Model output (`output/*.nc`) is not stored in the repository; the scripts regenerate it.

## Parameters

Paper set-up (`paper_config()` in `scripts/driver.jl`), from Gupta & Thompson (2022),
Table S1 and Section 2:

| Quantity | Value | | Quantity | Value |
|---|---|---|---|---|
| f | 1.3×10⁻⁴ s⁻¹ (70°N) | | Initial thickness | 1.5 m |
| ρᵢ, ρₒ | 1000, 1027 kg m⁻³ | | Cᵢₒ | 0.0055 |
| Cᵢₐ, Cₐₒ | 0.00125 | | Shortwave S | 300 W m⁻² |
| αᵢ, αₒ | 0.7, 0.4 | | A, B | 90 W m⁻², 15 W m⁻² K⁻¹ |
| qᵢₒ | 100 W m⁻² K⁻¹ | | T_f, Lᵢ | −1.8 °C, 3.34×10⁵ J kg⁻¹ |
| E, ν, e_r | 5×10⁵ Pa, 0.33, 0.5 | | μ_f | 0.3 |

Not specified in the paper's tables: ρₐ = 1.225 kg m⁻³; ocean surface temperature held at
−1.0 °C (initial mixed-layer value, Fig. 2e); of the two restitution values in Table S1,
e_r = 0.5 is used.

## Experiments and results

### 1. Free drift: Coriolis and drag formulation (`run_free_drift_check.jl`)
16 floes, uniform 10 m/s wind, ocean at rest, 2 days.

| Case | Drift speed | Direction from wind |
|---|---|---|
| no Coriolis | 0.164 m/s | 0.0° |
| Coriolis, original (component-wise) drag | 0.172 m/s | −25.0° |
| Coriolis, extended (vector) drag | 0.162 m/s | −11.7° |

With the vector drag of Eq. 2 the deflection matches the analytical free-drift balance
(≈12°); the component-wise drag of the published code roughly doubles it.
Figures: `free_trajectories.png`, `floe_1_trajectory.png`, `free_drift.png`.

### 2. Paper set-up (`run_paper_setup.jl`)
Melting check (4 floes, no wind): uniform thinning of ≈2.8 cm/day, as expected from the
heat balance (90 − 63 + 80 = 107 W m⁻²); all ice gone around day 53. Oscillating-wind
case: floes follow the wind and the prescribed Ekman current.
Figures: `paper_ice.png`, `paper_4floes_R1km_wind7_ocean_floe1.png`, `paper_trajectories.png`.

### 3. Eddy test (`run_eddy_test.jl`)
A 2 km floe at the centre of a cyclonic and an anticyclonic eddy (no wind, 20 days)
stays at the centre in both, i.e. the floe–grid force calculation leaves no spurious
net force. Figure: `eddytest_map.png`.

### 4. Velocity-dependent heat transfer for a floe in an eddy
One floe (radius 1, 2, 4, 8 km) starting at rest at the centre of an anticyclonic eddy
(radius 4 km ≈ the paper's deformation radius; peak speed 0.08 m/s; ζ/f ≈ 0.5). Ocean
temperature fixed at −1.0 °C. Steady thinning rate with the dynamic heat transfer,
relative to the paper's constant q (2.77 cm/day):

| Condition | u\*_min = 0.0005 m/s | u\*_min = 0.002 m/s | Floe behaviour |
|---|---|---|---|
| calm (days 2–5) | 0.34 (R ≤ 2 km) – 0.62 (8 km) | 0.62 (R ≤ 4 km) – 0.70 (8 km) | spins up with the eddy within ~0.5 day |
| wind 3 m/s (days 1–5) | 0.93 (R ≤ 2 km) – 0.83 (8 km) | 0.93 (R ≤ 2 km) – 0.85 (8 km) | floes ≤ 4 km stay in the eddy (slip ≈ 5 cm/s); the 8 km floe escapes |
| wind 7 m/s (days 1–5) | ≈1.77 | ≈1.77 | all floes leave the eddy; slip ≈ 11 cm/s, q ≈ 200 W m⁻² K⁻¹ |

- A floe carried by an eddy in calm conditions melts **30–65% more slowly** than with
  the constant q. For floes up to the eddy size the slip falls below the threshold set
  by u\*_min, so **the melt rate is set by the assumed minimum turbulence**, which
  differs by a factor of ~1.8 between the two plausible values used.
- Larger floes cannot follow the eddy's sheared flow as a rigid body; the heat delivery
  is then concentrated in **rings** where floe and water move at different speeds
  (`calmeddy_cummelt_pattern.png`). The differential melt is negligible for floes
  smaller than the eddy (±0.1 cm over 5 days for R ≤ 2 km) but large for floes at or
  above the eddy size: for R = 8 km (u\*_min = 0.0005 m/s) the cumulative melt ranges
  from −3.9 to +3.5 cm around a floe mean of 8.7 cm (≈ ±45%); for R = 4 km from −0.6 to
  +1.2 cm around 5.3 cm.
- With wind, the slip is set by the wind (≈ Nansen number × wind speed); the result no
  longer depends on u\*_min, and melt changes from slightly slower (3 m/s, 7–17% below
  the constant-q rate) to ~1.8× faster (7 m/s) than with the constant q.
- At 3 m/s the eddy (peak speed 0.08 m/s) holds floes up to its own size against the
  wind (wind-driven drift ≈ 0.05 m/s); the floe twice the eddy's size escapes. This
  retention is obtained without the sea-surface tilt term; experiment 5 shows that it
  persists with tilt and that the melt changes by only ~6%.

Figures: `windeddy_melt_ratio.png` (summary: calm, 3 and 7 m/s), `calmeddy_thinning.png`,
`calmeddy_cummelt.png`, `calmeddy_cummelt_pattern.png`, `calmeddy_du_q.png`,
`windeddy_thinning.png`, `windeddy_du_q.png`, `windeddy_tracks.png`.
Calm runs: 32 km box, 5 days. Wind runs: steady wind towards +x, 96 km box, 5 days.

### 5. Drag formulation and sea-surface tilt: does the floe stay in the eddy?
(`run_tilt_check_with_eddy.jl`, `run_tilt_check_long_with_eddy.jl`)

Without a sea-surface tilt term (as in the paper and the experiments above), Coriolis on a
floe circling an anticyclone is not balanced and pushes it inwards. The tilt term adds the
pressure-gradient force of the eddy's sloping surface, −g∇η = f k̂ × **u**ₒ + (**u**ₒ·∇)**u**ₒ
(gradient-wind balance; g gravity, η sea-surface height, **u**ₒ ocean velocity), so a floe
moving with the water feels the same force balance as the water. One 2 km floe in the
anticyclonic eddy, melting off, three versions: original module (component-wise drag),
vector drag, vector drag + tilt.

| Set-up | No tilt (either drag) | With tilt |
|---|---|---|
| calm, floe starting 4 km from the centre (5 days) | spirals into the centre within ~2 days | circles the eddy at ≈4.2 km (its starting radius) |
| 3 m/s wind, floe starting at the centre (15 days) | parks ≈1.9 km from the centre, where the eddy current (≈5.6 cm/s) opposes the wind-driven drift (≈5 cm/s) | orbits that same point on a loop between ≈0.3 and ≈4.2 km from the centre (period ≈3.7 days); still in the eddy after 15 days, peak distance growing slowly (3.95 → 4.17 km) |
| 3 m/s wind: mean slip, days 2–15 | 4.97 (original drag), 4.94 cm/s (vector drag) | 4.55 cm/s |

- The **drag formulation hardly matters** for retention: original and vector drag give
  nearly identical tracks.
- In **calm** conditions the inward drift of a floe in an anticyclone is an **artefact of
  the missing tilt term**: with tilt, the floe stays at whatever radius it starts.
  (Floes starting at the eddy centre, as in the calm heat experiments, are unaffected.)
- At **3 m/s** the floe remains in the eddy with tilt, but orbits instead of parking. The
  slip is ~8% lower, which lowers the dynamic heat transfer by the same fraction and the
  melt ratio from ≈0.93 to ≈0.87 (u\*_min not reached). The heat-transfer conclusions of
  experiment 4 are therefore robust to the tilt term at the ~6% level.

Figures: `tiltcheck.png` (5 days, calm and 3 m/s), `tiltcheck_wind3_15d.png` (3 m/s, 15 days).

## Limitations

- **Prescribed ocean.** Ocean temperature and currents are fixed: no cooling or
  freshening under the ice, no meltwater feedback, no eddy evolution, and the floe
  does not act back on the ocean. Results show directions and relative sizes, not
  realistic melt rates.
- **Single thickness per floe.** Per-cell melt is summed into one floe thickness, so
  ring-shaped heat delivery cannot produce thinner rims.
- **Constant freezing temperature** (−1.8 °C); salinity is not used.
- **No sea-surface tilt** in the heat experiments (as in the paper). Without it, Coriolis
  on a floe circling an eddy is unbalanced and draws floes into anticyclones. Experiment 5
  shows this matters for off-centre floes in calm conditions, but changes the 3 m/s melt
  by only ~6%. Tilt was tested for one floe size and an anticyclone only.
- **Periodic boundaries.** The module keeps one periodic copy per floe, so a floe
  overlapping a box corner is only partly represented. Floes here are kept away from
  the corners.

## Next steps

- Sea-surface tilt in the heat experiments themselves (all floe sizes, cyclonic eddies,
  longer runs to see whether the orbiting floe eventually escapes).
- Floes with radially varying thickness, to test whether rim-concentrated heat
  delivery thins floe edges.
- Coupling to an evolving ocean (Oceananigans.jl) to include meltwater stratification
  under the floe, which sets the minimum turbulence that controls the calm-case melt.

## License

`src/FloeModule.jl` and the derived `src/FloeModuleExt.jl`: CC-BY-4.0, © Mukund Gupta
(see Credit). All other code: MIT License, © 2026 Jayasankar T. Pillai (see `LICENSE`).
