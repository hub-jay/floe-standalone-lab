"""
plot_tilt_check_with_eddy.py -- figure for scripts/run_tilt_check_with_eddy.jl:
floe tracks over the anticyclonic eddy and distance from the eddy centre, for
original drag / vector drag / vector drag + sea-surface tilt, calm and 3 m/s wind.
Reads only output/tiltcheck_*.nc.

Usage (from the Floe folder, with the .venv active):
    python plotting/plot_tilt_check_with_eddy.py

Saves figures/tiltcheck.png (listed in figures/FIGURES.md).
"""
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
SETUPS = [("calm_off4km", "Calm, floe starting 4 km from the eddy centre"),
          ("wind3", "Wind 3 m/s towards +x, floe starting at the eddy centre")]
VERSIONS = [("origdrag", "original drag, no tilt", "tab:red"),
            ("vecdrag", "vector drag, no tilt", "tab:blue"),
            ("vecdrag_tilt", "vector drag + tilt", "tab:green")]


def attr(ds, key):
    v = ds.attrs[key]
    return float(v.item() if hasattr(v, "item") else v)


def unwrap_track(x, L):
    x = np.asarray(x, float).copy()
    ok = np.isfinite(x)
    if ok.sum() > 1:
        d = np.diff(x[ok]); d -= L * np.round(d / L)
        x[ok] = x[ok][0] + np.concatenate([[0.0], np.cumsum(d)])
    return x


def main(setups=SETUPS, fname="tiltcheck.png", title=None, desc=None):
    fig, axs = plt.subplots(2, len(setups), figsize=(6.5 * len(setups), 11), squeeze=False,
                            gridspec_kw=dict(height_ratios=[1.3, 1]))
    used = {}
    for col, (sl, stitle) in enumerate(setups):
        amap, adist = axs[0, col], axs[1, col]
        ds0, ext = None, []
        for vl, vlab, colr in VERSIONS:
            name = f"tiltcheck_{sl}_{vl}"
            p = OUT / f"{name}.nc"
            if not p.exists():
                print(f"(missing {p.name})"); continue
            ds = xr.open_dataset(p)
            used[name] = ds
            if ds0 is None:
                ds0 = ds
            L = attr(ds, "Lx")
            x = unwrap_track(ds.floe_x.values[:, 0], L)
            y = unwrap_track(ds.floe_y.values[:, 0], L)
            r = ds.floe_r.values[0, 0]
            t = ds.time.values / 86400
            amap.plot(x / 1e3, y / 1e3, color=colr, lw=1.4, label=vlab, zorder=3)
            th = np.linspace(0, 2 * np.pi, 100)
            amap.plot((x[-1] + r * np.cos(th)) / 1e3, (y[-1] + r * np.sin(th)) / 1e3,
                      color=colr, lw=0.8, zorder=3)
            ext += [(np.nanmin(x) - r) / 1e3, (np.nanmax(x) + r) / 1e3,
                    (np.nanmin(y) - r) / 1e3, (np.nanmax(y) + r) / 1e3]   # km
            # distance from the eddy centre (box centre), nearest periodic image
            dx = (x - L / 2 + L / 2) % L - L / 2
            dy = (y - L / 2 + L / 2) % L - L / 2
            adist.plot(t, np.hypot(dx, dy) / 1e3, color=colr, lw=1.5, label=vlab)
        if ds0 is None:
            amap.set_visible(False); adist.set_visible(False); continue
        # eddy vorticity background (with periodic copies)
        f, L = attr(ds0, "f"), attr(ds0, "Lx")
        xg, yg = ds0.x.values, ds0.y.values
        uo, vo = ds0.u_ocean.values, ds0.v_ocean.values
        zeta = (np.gradient(vo, xg[1] - xg[0], axis=1) - np.gradient(uo, xg[1] - xg[0], axis=0)) / f
        zm = np.nanmax(np.abs(zeta))
        for sx in (-L, 0, L):
            for sy in (-L, 0, L):
                im = amap.pcolormesh((xg + sx) / 1e3, (yg + sy) / 1e3, zeta, cmap="RdBu_r",
                                     vmin=-zm, vmax=zm, shading="auto", zorder=0)
        fig.colorbar(im, ax=amap, shrink=0.8, label="eddy vorticity ζ/f")
        c = L / 2e3
        x0, x1 = min(ext[0::4] + [c - 8]), max(ext[1::4] + [c + 8])
        y0, y1 = min(ext[2::4] + [c - 8]), max(ext[3::4] + [c + 8])
        half = 0.5 * max(x1 - x0, y1 - y0) + 2
        cx, cy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
        amap.set(xlim=(cx - half, cx + half), ylim=(cy - half, cy + half), aspect="equal",
                 xlabel="x (km, unwrapped)", ylabel="y (km, unwrapped)",
                 title=f"{stitle}\n(circles: floe at the end, day {ds0.time.values[-1]/86400:.0f})")
        amap.legend(fontsize=8, loc="upper left")
        R = attr(ds0, "eddy_radius") / 1e3
        adist.axhline(R, color="0.6", ls=":", lw=0.8)
        adist.text(0.01, R, " eddy radius (peak speed)", fontsize=7, color="0.4",
                   transform=adist.get_yaxis_transform(), va="bottom")
        adist.set(xlabel="time (days)", ylabel="distance of floe centre\nfrom eddy centre (km)")
        adist.grid(alpha=0.3)
        adist.legend(fontsize=8)
    fig.suptitle("Anticyclonic eddy (R = 4 km, V = 0.08 m/s), 2 km floe, melting off: effect of the "
                 "drag formulation and the sea-surface tilt term on where the floe goes", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    FIG.mkdir(exist_ok=True)
    path = FIG / fname
    fig.savefig(path, dpi=140, bbox_inches="tight")
    register(path, title or "Tilt / drag check: floe tracks and distance from the eddy centre",
             desc or "Anticyclonic eddy (radius 4 km, 0.08 m/s; background: vorticity ζ/f, blue = "
             "anticyclonic), one 2 km floe, melting off, 5 days. Left: calm, floe starting 4 km "
             "from the eddy centre. Right: steady 3 m/s wind towards +x, floe starting at the "
             "centre. Red: original module (component-wise drag), no tilt. Blue: vector drag "
             "(Eq. 2), no tilt. Green: vector drag + sea-surface tilt (gradient-wind balance). Top: "
             "tracks (circles: floe at the end). Bottom: distance of the floe centre from the "
             "eddy centre; decreasing = drawn in (retained), increasing = escaping.", used)
    print("saved", path)


if __name__ == "__main__":
    main()
    # long (15-day) wind runs from scripts/run_tilt_check_long_with_eddy.jl, if they exist
    if any(OUT.glob("tiltcheck_wind3_15d_*.nc")):
        main(setups=[("wind3_15d", "Wind 3 m/s towards +x, floe starting at the eddy centre")],
             fname="tiltcheck_wind3_15d.png",
             title="Tilt / drag check, 3 m/s wind, 15 days",
             desc="As tiltcheck.png (right column), run for 15 days with snapshots every 6 h: "
                  "anticyclonic eddy (radius 4 km, 0.08 m/s), one 2 km floe starting at the "
                  "centre, steady 3 m/s wind towards +x, melting off. Red: original drag, no "
                  "tilt. Blue: vector drag, no tilt. Green: vector drag + sea-surface tilt. Top: "
                  "tracks (circles: floe at the end). Bottom: distance of the floe centre from "
                  "the eddy centre; tests whether the floe eventually leaves the eddy.")
