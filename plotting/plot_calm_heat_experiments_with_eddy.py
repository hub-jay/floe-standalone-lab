"""
plot_calm_heat_experiments_with_eddy.py -- figures for
scripts/run_calm_heat_experiments_with_eddy.jl (12 calm runs: one floe at the
centre of an anticyclonic eddy; constant vs velocity-dependent heat transfer;
floe radius 1, 2, 4, 8 km). Reads only output/calmeddy_*.nc.

Usage (from the Floe folder, with the .venv active):
    python plotting/plot_calm_heat_experiments_with_eddy.py

Figures (all listed in figures/FIGURES.md):
    calmeddy_melt_ratio.png   steady thinning rate, dynamic / constant, vs floe radius
    calmeddy_thinning.png     thinning rate vs time for each floe radius, 3 heat versions
    calmeddy_cummelt.png      cumulative melt in each grid cell, ONE shared colour scale (amounts)
    calmeddy_cummelt_pattern.png  same, as deviation from each floe's mean in cm (where it melts)
    calmeddy_du_q.png         ice-ocean speed difference and heat transfer coefficient vs time
    calmeddy_meltmaps.png     melt rate under each floe on day 4 (dynamic, low u*_min)
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
PREFIX = "calmeddy"            # run and figure name prefix
RADII = [1, 2, 4, 8]
HEAT = [("qconst", "constant q (paper)"),
        ("qdynlow", "dynamic, u*min = 0.0005 m/s"),
        ("qdynhigh", "dynamic, u*min = 0.002 m/s")]


def load(name):
    p = OUT / f"{name}.nc"
    return xr.open_dataset(p) if p.exists() else None


def thinning_rate_series(ds):
    """Thinning rate of the (single) floe between snapshots [cm/day], at mid-interval times [days]."""
    t = ds.time.values / 86400
    h = ds.floe_h.values[:, 0]
    rate = -np.diff(h) / np.diff(t) * 100
    return 0.5 * (t[1:] + t[:-1]), rate


def steady_rate(ds, t_from):
    """Mean thinning rate [cm/day] from day t_from to the last snapshot with ice
    (i.e. after the floe has spun up / adjusted)."""
    t = ds.time.values / 86400
    h = ds.floe_h.values[:, 0]
    ok = np.where(np.isfinite(h) & (t >= t_from))[0]
    return (h[ok[0]] - h[ok[-1]]) / (t[ok[-1]] - t[ok[0]]) * 100


def fig_melt_ratio(t_from=2.0):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    used = {}
    for hl, hlab, style in [("qdynlow", HEAT[1][1], "o-"), ("qdynhigh", HEAT[2][1], "s--")]:
        ratio = []
        for R in RADII:
            c, d = load(f"{PREFIX}_R{R}km_qconst"), load(f"{PREFIX}_R{R}km_{hl}")
            if c is None or d is None:
                ratio.append(np.nan); continue
            used[f"{PREFIX}_R{R}km_qconst"] = c; used[f"{PREFIX}_R{R}km_{hl}"] = d
            ratio.append(steady_rate(d, t_from) / steady_rate(c, t_from))
        ax.plot(RADII, ratio, style, label=hlab)
    ax.axhline(1, color="0.6", lw=0.8)
    ax.axvline(4, color="0.8", lw=0.8, ls=":")
    ax.text(4.1, 0.02, "eddy radius", transform=ax.get_xaxis_transform(), fontsize=7, color="0.5")
    ax.set(xscale="log", xticks=RADII, xticklabels=[str(r) for r in RADII],
           xlabel="floe radius (km)", ylabel="steady thinning rate:\ndynamic / constant",
           title=f"Calm, anticyclonic eddy: thinning rate (days {t_from:g}-5)\n"
                 "relative to the paper's constant q (1 = same)")
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.legend(fontsize=8)
    fig.tight_layout()
    path = FIG / f"{PREFIX}_melt_ratio.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    register(path, "Steady thinning-rate ratio, dynamic / constant heat transfer, vs floe radius (calm, eddy)",
             f"Mean thinning rate from day {t_from:g} to day 5 (after spin-up) with the McPhee "
             "(velocity-dependent) heat transfer, divided by that with the paper's constant "
             "q_IO = 100 W/m2/K, for floe radii 1-8 km. Circles: u*_min = 0.0005 m/s; squares: "
             "0.002 m/s. Below 1 = slower melt than the paper's formulation. Dotted line: eddy radius.",
             used)
    print("saved", path)


def fig_calm_thinning():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4), sharey=True)
    used = {}
    styles = {"qconst": ("k", "-"), "qdynlow": ("tab:blue", "-"), "qdynhigh": ("tab:orange", "--")}
    for ax, R in zip(axs, RADII):
        for hl, hlab in HEAT:
            ds = load(f"{PREFIX}_R{R}km_{hl}")
            if ds is None:
                continue
            used[f"{PREFIX}_R{R}km_{hl}"] = ds
            t, rate = thinning_rate_series(ds)
            col, ls = styles[hl]
            ax.plot(t, rate, color=col, ls=ls, label=hlab)
        ax.axvline(2, color="0.8", lw=0.8, ls=":")
        ax.set(title=f"floe radius {R} km", xlabel="time (days)")
        ax.grid(alpha=0.3)
    axs[0].set_ylabel("thinning rate (cm/day)")
    axs[0].legend(fontsize=8)
    fig.suptitle("Calm, anticyclonic eddy: floe thinning rate over time (dotted: day 2, start of the "
                 "steady-rate window)", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    path = FIG / f"{PREFIX}_thinning.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    register(path, "Thinning rate vs time for each floe radius (calm)",
             "Thinning rate of the floe's (single, area-mean) thickness in cm/day against time, one "
             "panel per floe radius (1, 2, 4, 8 km). Black: paper's constant q. Blue: dynamic heat "
             "transfer, u*_min = 0.0005 m/s. Orange dashed: dynamic, u*_min = 0.002 m/s. The early "
             "peak in the dynamic runs is the spin-up period, when the water still slides past the "
             "floe at the full eddy speed. Dotted line: day 2.", used)
    print("saved", path)


def _local_cum_melt(ds):
    """Cumulative melt per cell [cm], divided by the cell's ice cover (local thinning);
    NaN outside the floe."""
    cum = ds.melt_cum.values                         # (y, x) [m], cell-area weighted
    sic = ds.sic.values[-1]                          # ice cover in each cell at the end
    return np.where(sic > 0.05, cum / np.where(sic > 0, sic, 1), np.nan) * 100


def _cummelt_grid(kind):
    """kind = 'absolute' (one shared colour scale) or 'pattern' (cm from the floe's own mean)."""
    data, used = {}, {}
    for R in RADII:
        for hl, _ in HEAT:
            ds = load(f"{PREFIX}_R{R}km_{hl}")
            if ds is None or not hasattr(ds, "melt_cum"):
                continue
            used[f"{PREFIX}_R{R}km_{hl}"] = ds
            data[(R, hl)] = (ds, _local_cum_melt(ds))
    if not data:
        return None, used
    if kind == "absolute":
        vmax = max(np.nanmax(v) for _, v in data.values())
        norm = dict(vmin=0.0, vmax=vmax, cmap="magma_r")
    fig, axs = plt.subplots(3, 4, figsize=(16, 12))
    for col, R in enumerate(RADII):
        for row, (hl, hlab) in enumerate(HEAT):
            ax = axs[row, col]
            if (R, hl) not in data:
                ax.set_visible(False); continue
            ds, local = data[(R, hl)]
            mean = np.nanmean(local)
            if kind == "pattern":
                field = local - mean                            # cm, deviation from the floe's mean
                lim = max(np.nanmax(np.abs(field)), 1e-9)
                if lim < 0.01:                                  # numerically uniform (constant q)
                    lim = 0.01
                kw = dict(vmin=-lim, vmax=lim, cmap="RdBu_r")
                label = "deviation from floe mean (cm)"
            else:
                field, kw, label = local, norm, "melt over the run (cm)"
            x, y = ds.x.values / 1e3, ds.y.values / 1e3
            xc, yc = ds.floe_x.values[-1, 0] / 1e3, ds.floe_y.values[-1, 0] / 1e3
            im = ax.pcolormesh(x, y, field, shading="auto", **kw)
            th = np.linspace(0, 2 * np.pi, 200)
            ax.plot(xc + R * np.cos(th), yc + R * np.sin(th), "k-", lw=0.8)
            pad = 1.25 * R
            ax.set(xlim=(xc - pad, xc + pad), ylim=(yc - pad, yc + pad), aspect="equal",
                   xlabel="x (km)" if row == 2 else None, ylabel="y (km)" if col == 0 else None)
            if kind == "pattern":
                ax.set_title(f"R = {R} km, {hlab}\nmean {mean:.2f} cm, range "
                             f"{np.nanmin(field):+.2f} to {np.nanmax(field):+.2f} cm", fontsize=8)
            else:
                ax.set_title(f"R = {R} km, {hlab}\nfloe mean {mean:.2f} cm", fontsize=8)
            if kind == "pattern" or col == 3:
                cb = fig.colorbar(im, ax=ax, shrink=0.8, label=label)
                cb.formatter.set_useOffset(False); cb.update_ticks()
    days = next(iter(data.values()))[0].time.values[-1] / 86400
    return (fig, days), used


def fig_calm_cummelt():
    out, used = _cummelt_grid("absolute")
    if out is None:
        return
    fig, days = out
    fig.suptitle(f"Calm, anticyclonic eddy: cumulative melt over {days:.0f} days in each grid cell under "
                 "the floe (local thinning). ONE colour scale for all panels: compare amounts.", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    path = FIG / f"{PREFIX}_cummelt.png"
    fig.savefig(path, dpi=130, bbox_inches="tight"); plt.close(fig)
    register(path, "Cumulative melt in each grid cell under the floe, shared colour scale (calm)",
             "Total melt over the run in each grid cell under the floe (cm), from the exact running "
             "sum saved by the driver (melt_cum), divided by the cell's ice cover so that partly "
             "covered rim cells show the local thinning. Columns: floe radius 1, 2, 4, 8 km. Rows: "
             "constant q, dynamic u*_min = 0.0005, dynamic u*_min = 0.002. ONE colour scale for all "
             "panels (colour bar on the right column), so amounts can be compared between panels. "
             "Panel titles give the floe-mean melt. Diagnostic only: the model thins each floe "
             "uniformly; the map shows where the heat was delivered.", used)
    print("saved", path)


def fig_calm_cummelt_pattern():
    out, used = _cummelt_grid("pattern")
    if out is None:
        return
    fig, days = out
    fig.suptitle(f"Calm, anticyclonic eddy: WHERE each floe melts more or less than its own average "
                 f"(cumulative melt over {days:.0f} days minus the floe mean, in cm; each panel its own "
                 "scale)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    path = FIG / f"{PREFIX}_cummelt_pattern.png"
    fig.savefig(path, dpi=130, bbox_inches="tight"); plt.close(fig)
    register(path, "Pattern of cumulative melt under the floe, deviation from the floe mean in cm (calm)",
             "Same data as calmeddy_cummelt.png, shown as each cell's cumulative melt minus that "
             "floe's mean melt, in cm over the run (red = more melt than average, blue = less). Panel "
             "titles give the floe mean and the range of deviations. Each panel has its own symmetric "
             "colour scale, so the pattern inside each floe is visible; amounts are compared in "
             "calmeddy_cummelt.png. Constant-q floes are uniform (differences "
             "are rounding only). In dynamic runs, rings of high melt mark radii where the rigidly "
             "rotating floe and the eddy water move at different speeds; low-melt centre and rings "
             "mark where they match.", used)
    print("saved", path)


def fig_calm_du_q():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 6.5), sharex=True)
    used = {}
    colours = dict(zip(RADII, ["tab:blue", "tab:orange", "tab:green", "tab:red"]))
    for R in RADII:
        ds = load(f"{PREFIX}_R{R}km_qdynlow")
        if ds is None:
            continue
        used[f"{PREFIX}_R{R}km_qdynlow"] = ds
        t = ds.time.values / 86400
        a1.plot(t, ds.floe_du.values[:, 0] * 100, color=colours[R], label=f"R = {R} km")
        a2.plot(t, ds.floe_q.values[:, 0], color=colours[R])
    a1.axhline(5.5, color="0.5", ls="--", lw=0.8)
    a1.text(0.99, 5.7, "5.5 cm/s: |du| at which dynamic q = paper's 100", ha="right", fontsize=7,
            color="0.4", transform=a1.get_yaxis_transform())
    a2.axhline(100, color="0.5", ls="--", lw=0.8)
    a2.text(0.99, 102, "paper's constant q = 100", ha="right", fontsize=7, color="0.4",
            transform=a2.get_yaxis_transform())
    a1.set_ylabel("mean |u_ice - u_ocean|\nunder floe (cm/s)")
    a2.set_ylabel("mean heat transfer\ncoefficient q (W m$^{-2}$ K$^{-1}$)")
    a2.set_xlabel("time (days)")
    a1.legend(fontsize=8)
    a1.set_title("Calm, anticyclonic eddy, dynamic heat transfer (u*min = 0.0005 m/s)", fontsize=10)
    fig.tight_layout()
    path = FIG / f"{PREFIX}_du_q.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    register(path, "Ice-ocean speed difference and heat transfer coefficient vs time (calm)",
             "Top: area-mean ice-ocean speed difference under the floe (incl. floe spin), cm/s. "
             "Bottom: area-mean heat transfer coefficient q under the floe. One line per floe radius. "
             "Dashed lines: 5.5 cm/s, the speed difference at which the dynamic q equals the paper's "
             "constant 100 W/m2/K.", used)
    print("saved", path)


def fig_calm_meltmaps(day=4):
    fig, axs = plt.subplots(1, 4, figsize=(15, 4.2))
    used = {}
    for ax, R in zip(axs, RADII):
        ds = load(f"{PREFIX}_R{R}km_qdynlow")
        if ds is None:
            ax.set_visible(False); continue
        used[f"{PREFIX}_R{R}km_qdynlow"] = ds
        k = int(np.argmin(np.abs(ds.time.values / 86400 - day)))
        melt = ds.melt_rate.values[k] * 86400 * 100          # (y, x), cm/day
        melt = np.where(melt > 0, melt, np.nan)
        x, y = ds.x.values / 1e3, ds.y.values / 1e3
        xc, yc = ds.floe_x.values[k, 0] / 1e3, ds.floe_y.values[k, 0] / 1e3
        pad = 1.3 * R
        im = ax.pcolormesh(x, y, melt, shading="auto", cmap="magma_r")
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(xc + R * np.cos(th), yc + R * np.sin(th), "k-", lw=0.8)
        ax.set(xlim=(xc - pad, xc + pad), ylim=(yc - pad, yc + pad), aspect="equal",
               title=f"R = {R} km (day {ds.time.values[k] / 86400:.0f})", xlabel="x (km)")
        fig.colorbar(im, ax=ax, shrink=0.8, label="melt rate (cm/day)")
    axs[0].set_ylabel("y (km)")
    fig.suptitle("Melt rate under the floe, calm, anticyclonic eddy (R = 4 km), dynamic heat transfer "
                 "(u*min = 0.0005 m/s): where does the floe melt fastest?", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    path = FIG / f"{PREFIX}_meltmaps.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    register(path, f"Melt-rate maps under the floe on day {day} (calm, dynamic heat transfer)",
             "Melt rate (cm/day) in each grid cell under the floe, for floe radii 1, 2, 4 and 8 km, "
             "zoomed on the floe (black circle). Includes surface (atmospheric) and basal (ocean) "
             "melt; the spatial pattern comes from the ocean part, which depends on the local "
             "ice-ocean speed difference. Partly covered edge cells show lower values because only "
             "part of the cell is ice.", used)
    print("saved", path)


def main():
    FIG.mkdir(exist_ok=True)
    fig_melt_ratio()
    fig_calm_thinning()
    fig_calm_cummelt()
    fig_calm_cummelt_pattern()
    fig_calm_du_q()
    fig_calm_meltmaps()


if __name__ == "__main__":
    main()
