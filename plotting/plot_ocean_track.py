"""
plot_ocean_track.py -- ocean surface current (arrows) on chosen days, with the
trajectory of one floe up to that day drawn on top.

Usage (from the Floe folder, with the .venv active):
    python plotting/plot_ocean_track.py
        -> file output/paper_4floes_R1km_wind7.nc, floe 1, days 5 and 15
    python plotting/plot_ocean_track.py --days 5 15 25 --floe 1 --file output/<name>.nc

The domain is periodic, so the floe can travel further than the box size. The
trajectory is "unwrapped" (one continuous line), and the ocean-current arrows,
which repeat every box length, are tiled underneath it.

Saves figures/<run name>_ocean_floe<n>.png
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.patches import Circle

from figindex import register  # figure catalogue (figures/FIGURES.md)

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"


def unwrap_track(a, L):
    """Undo periodic wrapping so the path is one continuous line."""
    a = np.asarray(a, float)
    ok = np.isfinite(a)
    out = a.copy()
    if ok.sum() < 2:
        return out
    d = np.diff(a[ok])
    d -= L * np.round(d / L)
    out[ok] = a[ok][0] + np.concatenate([[0.0], np.cumsum(d)])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(ROOT / "output" / "paper_4floes_R1km_wind7.nc"))
    ap.add_argument("--floe", type=int, default=1, help="floe number (1 = first)")
    ap.add_argument("--days", type=float, nargs="+", default=[5, 15])
    args = ap.parse_args()

    ds = xr.open_dataset(args.file)
    name = Path(args.file).stem
    Lx, Ly = float(ds.attrs["Lx"]), float(ds.attrs["Ly"])
    t_days = ds.time.values / 86400
    xg, yg = ds.x.values, ds.y.values                     # grid cell centres [m]
    i = args.floe - 1
    if not 0 <= i < ds.floe_x.values.shape[1]:
        raise SystemExit(f"Floe number must be between 1 and {ds.floe_x.values.shape[1]}.")

    # Unwrapped trajectory of the chosen floe [km]
    xu = unwrap_track(ds.floe_x.values[:, i], Lx) / 1e3
    yu = unwrap_track(ds.floe_y.values[:, i], Ly) / 1e3
    r_km = ds.floe_r.values[:, i] / 1e3

    n = len(args.days)
    fig, axs = plt.subplots(1, n, figsize=(6 * n, 6), squeeze=False)
    for ax, day in zip(axs[0], args.days):
        k = int(np.argmin(np.abs(t_days - day)))         # nearest snapshot
        if not np.isfinite(xu[k]):
            ax.set_title(f"day {t_days[k]:.1f}: floe {args.floe} has melted")
            continue

        # Panel extent: the whole track so far, plus a margin of one floe radius
        x0, x1 = np.nanmin(xu[:k + 1]) - r_km[k] - 2, np.nanmax(xu[:k + 1]) + r_km[k] + 2
        y0, y1 = np.nanmin(yu[:k + 1]) - r_km[k] - 2, np.nanmax(yu[:k + 1]) + r_km[k] + 2
        half = 0.5 * max(x1 - x0, y1 - y0)
        cx, cy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
        x0, x1, y0, y1 = cx - half, cx + half, cy - half, cy + half

        # Ocean current at this snapshot, tiled periodically over the panel
        uo = ds.u_ocean_t.values[k]                      # (y, x)
        vo = ds.v_ocean_t.values[k]
        nq = 18                                          # arrows per side
        qx = np.linspace(x0, x1, nq)
        qy = np.linspace(y0, y1, nq)
        QX, QY = np.meshgrid(qx, qy)
        ix = np.searchsorted(xg, (QX * 1e3) % Lx).clip(0, len(xg) - 1)
        iy = np.searchsorted(yg, (QY * 1e3) % Ly).clip(0, len(yg) - 1)
        U, V = uo[iy, ix], vo[iy, ix]
        speed = float(np.nanmax(np.hypot(uo, vo)))
        if speed > 0:
            ax.quiver(QX, QY, U, V, color="tab:blue", alpha=0.6, width=0.003,
                      scale=speed * nq * 1.2, scale_units="width")

        # Floe trajectory up to this day, and the floe itself
        ax.plot(xu[:k + 1], yu[:k + 1], "k-", lw=1.5, label=f"floe {args.floe} track")
        ax.plot(xu[0], yu[0], "k*", ms=12, label="start")
        ax.add_patch(Circle((xu[k], yu[k]), r_km[k], facecolor="0.85", edgecolor="k",
                            alpha=0.7, label=f"floe on day {t_days[k]:.1f}"))

        # Wind and current at this time
        wu, wv = float(ds.wind_u.values[k]), float(ds.wind_v.values[k])
        cu, cv = float(np.nanmean(uo)), float(np.nanmean(vo))
        fu, fv = float(ds.floe_u.values[k, i]), float(ds.floe_v.values[k, i])
        info = (f"wind  {np.hypot(wu, wv):.1f} m/s towards {np.degrees(np.arctan2(wv, wu)):+.0f}°\n"
                f"ocean {np.hypot(cu, cv):.3f} m/s towards {np.degrees(np.arctan2(cv, cu)):+.0f}°\n"
                f"floe  {np.hypot(fu, fv):.3f} m/s towards {np.degrees(np.arctan2(fv, fu)):+.0f}°\n"
                "(angles from +x, anticlockwise)")
        ax.text(0.02, 0.98, info, transform=ax.transAxes, va="top", fontsize=8,
                family="monospace", bbox=dict(facecolor="white", alpha=0.85, edgecolor="0.7"))

        ax.set(xlim=(x0, x1), ylim=(y0, y1), aspect="equal",
               xlabel="x (km, unwrapped)", ylabel="y (km, unwrapped)",
               title=f"Day {t_days[k]:.1f}: ocean current (arrows) and floe {args.floe}")
        ax.legend(loc="lower right", fontsize=8)

    fig.suptitle(f"{name}", fontsize=10)
    fig.tight_layout()
    FIG.mkdir(exist_ok=True)
    days_txt = ", ".join(f"{d:g}" for d in args.days)
    path = FIG / f"{name}_ocean_floe{args.floe}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    register(path, f"Ocean current and floe {args.floe} track on days {days_txt}: {name}",
             f"One panel per chosen day ({days_txt}). Blue arrows: prescribed ocean surface "
             f"current at that snapshot (tiled, since the domain is periodic). Black line: track "
             f"of floe {args.floe} from the start (star) to that day, unwrapped across the box "
             f"edges. Grey disc: the floe at that day, to scale. Box: wind, ocean current and "
             f"floe velocity at that moment (directions in degrees from +x, anticlockwise).",
             {name: ds})
    print("saved", path)


if __name__ == "__main__":
    main()
