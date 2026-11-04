"""
plot_wind_heat_experiments_with_eddy.py -- figures for
scripts/run_wind_heat_experiments_with_eddy.jl (16 wind runs: one floe starting
at the centre of an anticyclonic eddy, steady wind 3 or 7 m/s for 5 days, velocity-dependent
heat transfer, floe radius 1, 2, 4, 8 km). Reads only output/windeddy_*.nc
(and, if present, output/calmeddy_*.nc for comparison).

Usage (from the Floe folder, with the .venv active):
    python plotting/plot_wind_heat_experiments_with_eddy.py

Figures (all listed in figures/FIGURES.md):
    windeddy_melt_ratio.png   steady thinning rate / constant-q rate vs floe radius (calm, 3, 7 m/s)
    windeddy_thinning.png     thinning rate vs time for each floe radius
    windeddy_du_q.png         ice-ocean speed difference and heat transfer coefficient vs time
    windeddy_tracks.png       floe tracks over the eddy, for each wind speed
"""
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import xarray as xr

from figindex import register

warnings.filterwarnings("ignore", message="Mean of empty slice")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
FIG = ROOT / "figures"
PREFIX = "windeddy"
WINDS = [3, 7]
RADII = [1, 2, 4, 8]
HEAT = [("qdynlow", "u*min = 0.0005 m/s"), ("qdynhigh", "u*min = 0.002 m/s")]
RCOL = dict(zip(RADII, ["tab:blue", "tab:orange", "tab:green", "tab:red"]))


def load(name):
    p = OUT / f"{name}.nc"
    return xr.open_dataset(p) if p.exists() else None


def a(ds, key):
    v = ds.attrs[key]
    return float(v.item() if hasattr(v, "item") else v)


def constant_q_rate(ds):
    """Thinning rate [cm/day] the paper's constant q would give with this run's settings:
    (S(1-alpha_i) - (A + B T_f) + q_IO (T_o - T_f)) / (rho_i L_f)."""
    heat = (a(ds, "Q") * (1 - a(ds, "alpha_I")) - (a(ds, "A") + a(ds, "B") * a(ds, "Tf"))
            + a(ds, "q_IO") * (a(ds, "T_ocean") - a(ds, "Tf")))
    return heat / (a(ds, "rho_I") * a(ds, "Lf")) * 86400 * 100


def thinning_rate_series(ds):
    t = ds.time.values / 86400
    h = ds.floe_h.values[:, 0]
    return 0.5 * (t[1:] + t[:-1]), -np.diff(h) / np.diff(t) * 100


def steady_rate(ds, t_from):
    t = ds.time.values / 86400
    h = ds.floe_h.values[:, 0]
    ok = np.where(np.isfinite(h) & (t >= t_from))[0]
    return (h[ok[0]] - h[ok[-1]]) / (t[ok[-1]] - t[ok[0]]) * 100


def unwrap_track(x, L):
    x = np.asarray(x, float).copy()
    ok = np.isfinite(x)
    if ok.sum() > 1:
        d = np.diff(x[ok]); d -= L * np.round(d / L)
        x[ok] = x[ok][0] + np.concatenate([[0.0], np.cumsum(d)])
    return x


def fig_melt_ratio():
    fig, ax = plt.subplots(figsize=(7, 5))
    used = {}
    rows = [("calm", "calmeddy_R{R}km_{h}", 2.0, "0.4"),
            ("wind 3 m/s", "windeddy_W3_R{R}km_{h}", 1.0, "tab:blue"),
            ("wind 7 m/s", "windeddy_W7_R{R}km_{h}", 1.0, "tab:red")]
    for label, pattern, t_from, col in rows:
        for hl, hlab, mk, ls in [("qdynlow", HEAT[0][1], "o", "-"), ("qdynhigh", HEAT[1][1], "s", "--")]:
            ratio = []
            for R in RADII:
                name = pattern.format(R=R, h=hl)
                ds = load(name)
                if ds is None:
                    ratio.append(np.nan); continue
                used[name] = ds
                ratio.append(steady_rate(ds, t_from) / constant_q_rate(ds))
            if np.all(np.isnan(ratio)):
                continue
            ax.plot(RADII, ratio, marker=mk, ls=ls, color=col, label=f"{label}, {hlab}")
    ax.axhline(1, color="k", lw=0.8)
    ax.text(1.0, 1.02, "paper's constant q", fontsize=7, color="0.3")
    ax.axvline(4, color="0.8", lw=0.8, ls=":")
    ax.text(4.1, 0.02, "eddy radius", transform=ax.get_xaxis_transform(), fontsize=7, color="0.5")
    ax.set(xscale="log", xticks=RADII, xticklabels=[str(r) for r in RADII],
           xlabel="floe radius (km)", ylabel="steady thinning rate / constant-q rate",
           title="Velocity-dependent heat transfer relative to the paper's constant q\n"
                 "(floe starting at the centre of an anticyclonic eddy; >1 = faster melt)")
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.legend(fontsize=7, ncol=1)
    fig.tight_layout()
    path = FIG / f"{PREFIX}_melt_ratio.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    register(path, "Thinning-rate ratio (dynamic / constant q) vs floe radius: calm, 3 m/s, 7 m/s",
             "Steady thinning rate with velocity-dependent (McPhee) heat transfer divided by the rate "
             "the paper's constant q_IO = 100 W/m2/K gives (2.77 cm/day here; computed from the heat "
             "balance, since with a fixed ocean temperature it does not depend on motion). Grey: calm "
             "runs (days 2-5, if calmeddy files exist); blue: wind 3 m/s; red: wind 7 m/s (days "
             "1-5). Circles/solid: u*_min = 0.0005 m/s; squares/dashed: 0.002 m/s.", used)
    print("saved", path)


def fig_thinning():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4), sharey=True)
    used = {}
    ref = None
    for ax, R in zip(axs, RADII):
        for W, col in [(3, "tab:blue"), (7, "tab:red")]:
            for hl, hlab in HEAT:
                name = f"{PREFIX}_W{W}_R{R}km_{hl}"
                ds = load(name)
                if ds is None:
                    continue
                used[name] = ds
                ref = constant_q_rate(ds)
                t, rate = thinning_rate_series(ds)
                ax.plot(t, rate, color=col, ls="-" if hl == "qdynlow" else "--",
                        label=f"{W} m/s, {hlab}")
        if ref is not None:
            ax.axhline(ref, color="k", lw=1, label="paper's constant q")
        ax.set(title=f"floe radius {R} km", xlabel="time (days)")
        ax.grid(alpha=0.3)
    axs[0].set_ylabel("thinning rate (cm/day)")
    axs[0].legend(fontsize=7)
    fig.suptitle("Wind runs: floe thinning rate over time (floe starts at rest at the eddy centre "
                 "and is blown out of the eddy)", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    path = FIG / f"{PREFIX}_thinning.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    register(path, "Thinning rate vs time for each floe radius (wind runs)",
             "Thinning rate of the floe (cm/day) against time, one panel per floe radius. Blue: wind "
             "3 m/s; red: 7 m/s. Solid: u*_min = 0.0005 m/s; dashed: 0.002 m/s. Black line: the rate "
             "with the paper's constant q.", used)
    print("saved", path)


def fig_du_q():
    fig, axs = plt.subplots(2, 2, figsize=(11, 7), sharex=True)
    used = {}
    for col, W in enumerate(WINDS):
        for R in RADII:
            name = f"{PREFIX}_W{W}_R{R}km_qdynlow"
            ds = load(name)
            if ds is None:
                continue
            used[name] = ds
            t = ds.time.values / 86400
            axs[0, col].plot(t, ds.floe_du.values[:, 0] * 100, color=RCOL[R], label=f"R = {R} km")
            axs[1, col].plot(t, ds.floe_q.values[:, 0], color=RCOL[R])
        axs[0, col].axhline(5.5, color="0.5", ls="--", lw=0.8)
        axs[1, col].axhline(100, color="0.5", ls="--", lw=0.8)
        axs[0, col].set_title(f"wind {W} m/s (u*min = 0.0005 m/s)")
        axs[1, col].set_xlabel("time (days)")
    axs[0, 0].set_ylabel("mean |u_ice - u_ocean|\nunder floe (cm/s)")
    axs[1, 0].set_ylabel("mean heat transfer\ncoefficient q (W m$^{-2}$ K$^{-1}$)")
    axs[0, 0].legend(fontsize=8)
    fig.suptitle("Wind runs: ice-ocean speed difference and heat transfer coefficient under the floe "
                 "(dashed: 5.5 cm/s and q = 100, the paper's equivalent)", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = FIG / f"{PREFIX}_du_q.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    register(path, "Ice-ocean speed difference and heat transfer coefficient vs time (wind runs)",
             "Top: area-mean ice-ocean speed difference under the floe (incl. spin), cm/s. Bottom: "
             "area-mean heat transfer coefficient q. Columns: wind 3 and 7 m/s; one line per floe "
             "radius; u*_min = 0.0005 m/s. Dashed: 5.5 cm/s and q = 100 W/m2/K, where the dynamic "
             "formula equals the paper's constant.", used)
    print("saved", path)


def fig_tracks():
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
    used = {}
    for ax, W in zip(axs, WINDS):
        ds0, ext = None, []
        for R in RADII:
            name = f"{PREFIX}_W{W}_R{R}km_qdynlow"
            ds = load(name)
            if ds is None:
                continue
            used[name] = ds
            if ds0 is None:
                ds0 = ds
            L = a(ds, "Lx")
            x = unwrap_track(ds.floe_x.values[:, 0], L) / 1e3
            y = unwrap_track(ds.floe_y.values[:, 0], L) / 1e3
            ax.plot(x, y, color=RCOL[R], lw=1.5, label=f"R = {R} km", zorder=3)
            th = np.linspace(0, 2 * np.pi, 100)
            k = np.where(np.isfinite(x))[0][-1]
            ax.plot(x[k] + R * np.cos(th), y[k] + R * np.sin(th), color=RCOL[R], lw=0.8, zorder=3)
            ext += [np.nanmin(x) - R, np.nanmax(x) + R, np.nanmin(y) - R, np.nanmax(y) + R]
        if ds0 is None:
            ax.set_visible(False); continue
        f = a(ds0, "f")
        L = a(ds0, "Lx")
        xg, yg = ds0.x.values, ds0.y.values
        uo, vo = ds0.u_ocean.values, ds0.v_ocean.values
        zeta = (np.gradient(vo, xg[1] - xg[0], axis=1) - np.gradient(uo, xg[1] - xg[0], axis=0)) / f
        zm = np.nanmax(np.abs(zeta))
        # the domain is periodic: draw the eddy and its neighbouring copies
        for sx in (-L, 0, L):
            for sy in (-L, 0, L):
                im = ax.pcolormesh((xg + sx) / 1e3, (yg + sy) / 1e3, zeta, cmap="RdBu_r",
                                   vmin=-zm, vmax=zm, shading="auto", zorder=0)
        fig.colorbar(im, ax=ax, shrink=0.8, label="eddy vorticity ζ/f")
        c = L / 2e3
        x0, x1 = min(ext[0::4] + [c - 10]), max(ext[1::4] + [c + 10])
        y0, y1 = min(ext[2::4] + [c - 10]), max(ext[3::4] + [c + 10])
        half = 0.5 * max(x1 - x0, y1 - y0) + 3
        cx, cy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
        days = ds0.time.values[-1] / 86400
        ax.set(xlim=(cx - half, cx + half), ylim=(cy - half, cy + half), aspect="equal",
               xlabel="x (km, unwrapped)", ylabel="y (km, unwrapped)",
               title=f"Wind {W} m/s towards +x: floe tracks over {days:.0f} days\n"
                     "(circles: floes at the end; eddy copies shown where the box repeats)")
        ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    path = FIG / f"{PREFIX}_tracks.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    register(path, "Floe tracks over the eddy (wind runs)",
             "Track of the floe centre over the run for each floe radius (colours), starting at the "
             "centre of the anticyclonic eddy (background: eddy vorticity ζ/f, blue = anticyclonic). "
             "Circles: floe outlines at the end. Left: wind 3 m/s; right: 7 m/s, both towards +x. "
             "Runs with u*_min = 0.0005 m/s (the heat transfer does not affect the motion).", used)
    print("saved", path)


def main():
    FIG.mkdir(exist_ok=True)
    fig_melt_ratio()
    fig_thinning()
    fig_du_q()
    fig_tracks()


if __name__ == "__main__":
    main()
