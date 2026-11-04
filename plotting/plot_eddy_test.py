"""
plot_eddy_test.py -- map of the eddy with the floe's trajectory on top, for the
eddy test runs (scripts/run_eddy_test.jl). Reads ONLY the run files named.

Usage (from the Floe folder, with the .venv active):
    python plotting/plot_eddy_test.py
        -> eddytest_anticyclonic_R2km and eddytest_cyclonic_R2km
    python plotting/plot_eddy_test.py <run name 1> <run name 2> ...   (names without .nc)

Saves figures/eddytest_map.png (listed in figures/FIGURES.md).
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from figindex import register

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
FIG = ROOT / "figures"
DEFAULT = ["eddytest_anticyclonic_R2km", "eddytest_cyclonic_R2km"]


def main():
    names = sys.argv[1:] or DEFAULT
    runs = {}
    for n in names:
        p = OUT / f"{n}.nc"
        if not p.exists():
            sys.exit(f"File not found: {p}  (run scripts/run_eddy_test.jl first)")
        runs[n] = xr.open_dataset(p)

    fig, axs = plt.subplots(1, len(runs), figsize=(6.0 * len(runs), 7.0), squeeze=False)
    for ax, (name, ds) in zip(axs[0], runs.items()):
        L = float(ds.attrs["Lx"])
        f = float(ds.attrs["f"])
        R_eddy = float(ds.attrs["eddy_radius"])
        V = float(ds.attrs["eddy_speed"])
        x, y = ds.x.values, ds.y.values                       # cell centres [m]
        uo, vo = ds.u_ocean.values, ds.v_ocean.values         # (y, x)
        dxg = x[1] - x[0]

        # Relative vorticity of the prescribed eddy, zeta = dv/dx - du/dy, in units of f
        zeta = (np.gradient(vo, dxg, axis=1) - np.gradient(uo, dxg, axis=0)) / f
        zmax = np.nanmax(np.abs(zeta))
        X, Y = x / 1e3, y / 1e3
        im = ax.pcolormesh(X, Y, zeta, cmap="RdBu_r", vmin=-zmax, vmax=zmax, shading="auto")
        fig.colorbar(im, ax=ax, orientation="horizontal", shrink=0.8, pad=0.1,
                     label="eddy vorticity  ζ/f  (red = cyclonic, blue = anticyclonic)")
        s = 4                                                 # every 4th cell for arrows
        ax.quiver(X[::s], Y[::s], uo[::s, ::s], vo[::s, ::s], color="0.25", width=0.0025)

        # Floe trajectory (it should stay near the centre; drawn as is, not unwrapped)
        fx, fy = ds.floe_x.values[:, 0], ds.floe_y.values[:, 0]
        r = ds.floe_r.values[0, 0]
        t = ds.time.values / 86400
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot((fx[0] + r * np.cos(th)) / 1e3, (fy[0] + r * np.sin(th)) / 1e3, "k--", lw=1,
                label="floe at start")
        k = np.where(np.isfinite(fx))[0][-1]
        ax.plot((fx[k] + r * np.cos(th)) / 1e3, (fy[k] + r * np.sin(th)) / 1e3, "-", color="gold",
                lw=1.5, label=f"floe on day {t[k]:.0f}")
        sc = ax.scatter(fx / 1e3, fy / 1e3, c=t, s=6, cmap="viridis", zorder=5)
        ax.plot(fx / 1e3, fy / 1e3, "k-", lw=0.6, zorder=4)
        fig.colorbar(sc, ax=ax, shrink=0.7, label="floe track: time (days)")

        # How far did it move, and how fast does it spin compared with the eddy core?
        cx, cy = L / 2, L / 2
        dxc = (fx - cx + L / 2) % L - L / 2
        dyc = (fy - cy + L / 2) % L - L / 2
        dist = np.hypot(dxc, dyc)
        omega_core = V * np.exp(0.5) / R_eddy                 # water's angular velocity at the core
        sense = 1.0 if ds.attrs["eddy_sense"] == "cyclonic" else -1.0
        omega_core *= sense * np.sign(f)                      # signed: same sign as the eddy's rotation
        spin = ds.floe_zeta.values[k, 0]
        info = (f"max distance from eddy centre: {np.nanmax(dist):.1f} m\n"
                f"distance on day {t[k]:.0f}: {dist[k]:.1f} m\n"
                f"floe spin / eddy-core rotation: {spin / omega_core:.2f}\n"
                f"(1 = turning with the water)")
        ax.text(0.02, 0.98, info, transform=ax.transAxes, va="top", fontsize=8, family="monospace",
                bbox=dict(facecolor="white", alpha=0.85, edgecolor="0.7"))

        pad = 2.5 * R_eddy / 1e3
        ax.set(xlim=(cx / 1e3 - pad, cx / 1e3 + pad), ylim=(cy / 1e3 - pad, cy / 1e3 + pad),
               aspect="equal", xlabel="x (km)", ylabel="y (km)",
               title=f"{name}\n{ds.attrs['eddy_sense']} eddy: R = {R_eddy/1e3:g} km, V = {V:g} m/s\n"
                     f"floe radius {r/1e3:g} km")
        ax.legend(loc="lower right", fontsize=8)

    fig.tight_layout()
    FIG.mkdir(exist_ok=True)
    path = FIG / "eddytest_map.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    register(path, "Eddy test: floe trajectory over the eddy",
             "One panel per run. Colours: vorticity of the prescribed eddy (ζ/f; red = cyclonic, "
             "blue = anticyclonic). Arrows: eddy current. Dots and black line: floe-centre track, "
             "coloured by time. Dashed circle: floe at the start; gold circle: floe at the end. Box: "
             "maximum and final distance of the floe centre from the eddy centre, and the floe's "
             "spin rate relative to the rotation rate of the eddy core (+1 = turning with the water).",
             runs)
    print("saved", path)


if __name__ == "__main__":
    main()
