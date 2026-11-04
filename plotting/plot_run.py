"""
plot_run.py -- standard plots for every run in output/ (maps, trajectories,
drift, ice volume). Each figure is listed in figures/FIGURES.md.

Usage (from the Floe folder, with the .venv active):
    python plotting/plot_run.py                 # plots every file in output/
    python plotting/plot_run.py output/paper_4floes_R1km_nowind.nc   # chosen files only

Figures are saved in figures/.
"""
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message="Mean of empty slice")   # after all ice has melted

import matplotlib

matplotlib.use("Agg")  # save to files, no window needed
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

from figindex import register  # figure catalogue (figures/FIGURES.md)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
FIG = ROOT / "figures"


def unwrap_periodic(a, L):
    """Insert NaN where a floe jumps across a periodic boundary (for drawing tracks)."""
    a = a.astype(float).copy()
    jump = np.abs(np.diff(a)) > L / 2
    a[1:][jump] = np.nan
    return a


def floe_map(ds, name):
    """Floes at start (outlines) and end (filled, coloured by thickness), with tracks."""
    Lx, Ly = float(ds.attrs["Lx"]), float(ds.attrs["Ly"])
    x, y = ds.floe_x.values, ds.floe_y.values  # (time, floe)
    r, h = ds.floe_r.values, ds.floe_h.values

    fig, ax = plt.subplots(figsize=(6.5, 6))
    # Ocean currents (if any) as light arrows
    uo, vo = ds.u_ocean.values, ds.v_ocean.values  # (y, x)
    if np.nanmax(np.hypot(uo, vo)) > 0:
        s = max(1, uo.shape[0] // 15)
        ax.quiver(ds.x.values[::s] / 1e3, ds.y.values[::s] / 1e3,
                  uo[::s, ::s], vo[::s, ::s], color="0.75", width=0.003)

    for i in range(x.shape[1]):
        ax.plot(unwrap_periodic(x[:, i], Lx) / 1e3, unwrap_periodic(y[:, i], Ly) / 1e3,
                lw=0.8, color="0.4")

    start = [Circle((x[0, i] / 1e3, y[0, i] / 1e3), r[0, i] / 1e3)
             for i in range(x.shape[1]) if np.isfinite(x[0, i])]
    ax.add_collection(PatchCollection(start, facecolor="none", edgecolor="k",
                                      linestyle="--", linewidth=0.8))

    last = [np.where(np.isfinite(x[:, i]))[0] for i in range(x.shape[1])]
    ends, hs = [], []
    for i, idx in enumerate(last):
        if len(idx):
            k = idx[-1]
            ends.append(Circle((x[k, i] / 1e3, y[k, i] / 1e3), r[k, i] / 1e3))
            hs.append(h[k, i])
    pc = PatchCollection(ends, cmap="viridis", edgecolor="k", linewidth=0.5)
    pc.set_array(np.array(hs))
    ax.add_collection(pc)
    fig.colorbar(pc, ax=ax, label="final floe thickness (m)", shrink=0.8)

    alive = np.where(np.isfinite(x).any(axis=1))[0]
    days = ds.time.values[alive[-1]] / 86400
    ax.set(xlim=(0, Lx / 1e3), ylim=(0, Ly / 1e3), aspect="equal",
           xlabel="x (km)", ylabel="y (km)",
           title=f"{name}\nstart (dashed) and day {days:.1f} (filled, last snapshot with ice)")
    fig.tight_layout()
    path = FIG / f"{name}_map.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    register(path, f"Floe map: {name}",
             "Map of the (periodic) domain. Dashed circles: floes at the start. Filled circles: "
             "floes at the last snapshot that still has ice, coloured by thickness. Grey lines: "
             "each floe's track (broken where it wraps across the box edge). Grey arrows: ocean "
             "current at the end of the run (only if non-zero).", {name: ds})
    print("saved", path)


def drift_comparison(datasets, tag):
    """Mean drift speed, and drift direction relative to the wind, for runs with wind."""
    runs = {n: d for n, d in datasets.items() if np.nanmax(np.abs(d.wind_u.values)) +
            np.nanmax(np.abs(d.wind_v.values)) > 0}
    if not runs:
        return
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    for name, ds in runs.items():
        t = ds.time.values / 86400
        u = np.nanmean(ds.floe_u.values, axis=1)
        v = np.nanmean(ds.floe_v.values, axis=1)
        wu, wv = ds.wind_u.values, ds.wind_v.values
        ang = np.degrees(np.arctan2(v, u) - np.arctan2(wv, wu))
        ang = (ang + 180) % 360 - 180
        ang[(np.hypot(u, v) < 1e-4) | (np.hypot(wu, wv) < 0.5)] = np.nan
        a1.plot(t, np.hypot(u, v), label=name)
        a2.plot(t, ang, label=name)
    a1.set_ylabel("mean drift speed (m/s)")
    a2.set_ylabel("drift direction\nrelative to wind (deg)")
    a2.axhline(0, color="0.6", lw=0.8)
    a2.set_xlabel("time (days)")
    a1.legend(fontsize=8)
    a2.text(0.01, 0.92, "negative = to the right of the wind", transform=a2.transAxes,
            fontsize=8, color="0.4")
    fig.tight_layout()
    path = FIG / f"{tag}_drift.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    register(path, f"Drift speed and direction: '{tag}' runs with wind",
             "Top: mean floe drift speed (m/s) against time. Bottom: drift direction relative "
             "to the wind direction (degrees; negative = to the right of the wind). Directions "
             "are hidden when the wind is weaker than 0.5 m/s or the floes are nearly still.",
             runs)
    print("saved", path)


def ice_comparison(datasets, tag):
    """Ice volume, mean thickness of remaining ice, and basal+surface melt rate."""
    fig, axs = plt.subplots(3, 1, figsize=(7, 8), sharex=True)
    for name, ds in datasets.items():
        t = ds.time.values / 86400
        r = np.nan_to_num(ds.floe_r.values)
        h = np.nan_to_num(ds.floe_h.values)
        area = np.pi * r**2
        vol = (area * h).sum(axis=1)
        a_tot = area.sum(axis=1)
        hbar = np.where(a_tot > 0, vol / np.where(a_tot > 0, a_tot, 1), np.nan)
        rate = -np.gradient(hbar, t) * 100          # cm/day, ice-area-weighted
        gone = a_tot == 0
        rate[gone | np.roll(gone, -1) | np.roll(gone, 1)] = np.nan   # skip melt-out jumps
        axs[0].plot(t, vol / vol[0], label=name)
        axs[1].plot(t, hbar, label=name)
        axs[2].plot(t, rate, label=name)
    axs[0].set_ylabel("ice volume\n(fraction of initial)")
    axs[1].set_ylabel("mean thickness of\nremaining ice (m)")
    axs[2].set_ylabel("thinning rate (cm/day)")
    axs[2].set_xlabel("time (days)")
    axs[0].legend(fontsize=8)
    fig.tight_layout()
    path = FIG / f"{tag}_ice.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    register(path, f"Ice volume, thickness and thinning rate: '{tag}' runs",
             "Top: total ice volume as a fraction of the initial volume. Middle: mean thickness "
             "of the ice that remains (area-weighted). Bottom: thinning rate of that mean "
             "thickness (cm/day). All against time (days).", datasets)
    print("saved", path)


def unwrap_track(a, L):
    """Undo periodic wrapping: a floe leaving at x = L and re-entering at x = 0
    is continued at x > L, so the whole path is one continuous line."""
    a = np.asarray(a, float)
    out = a.copy()
    ok = np.isfinite(a)
    if ok.sum() < 2:
        return out
    v = a[ok]
    d = np.diff(v)
    d -= L * np.round(d / L)          # remove jumps of +-L across the boundary
    out[ok] = v[0] + np.concatenate([[0.0], np.cumsum(d)])
    return out


def trajectories(datasets, tag):
    """Unwrapped trajectory of every floe, one panel per run, same axes."""
    order = lambda nm: (0 if "no_coriolis" in nm else 1 if "original" in nm else 2, nm)
    names = sorted(datasets, key=order)       # no Coriolis, then original, then extended
    n = len(names)
    fig, axs = plt.subplots(1, n, figsize=(4.2 * n, 5.2), sharex=True, sharey=True,
                            squeeze=False)
    axs = axs[0]
    xr_, yr_ = [0.0, 0.0], [0.0, 0.0]          # common axis range over all runs
    for ax, name in zip(axs, names):
        ds = datasets[name]
        Lx, Ly = float(ds.attrs["Lx"]), float(ds.attrs["Ly"])
        x, y = ds.floe_x.values, ds.floe_y.values          # (time, floe)
        for i in range(x.shape[1]):
            xu = unwrap_track(x[:, i], Lx) / 1e3
            yu = unwrap_track(y[:, i], Ly) / 1e3
            ax.plot(xu - xu[0], yu - yu[0], lw=0.9, alpha=0.8)      # displacement from start
            xr_ = [min(xr_[0], np.nanmin(xu - xu[0])), max(xr_[1], np.nanmax(xu - xu[0]))]
            yr_ = [min(yr_[0], np.nanmin(yu - yu[0])), max(yr_[1], np.nanmax(yu - yu[0]))]
            k = np.where(np.isfinite(xu))[0]
            if len(k):
                ax.plot(xu[k[-1]] - xu[0], yu[k[-1]] - yu[0], "k.", ms=3)
        # last snapshot that still has ice (after melt-out everything is NaN)
        alive = np.where(np.isfinite(ds.floe_u.values).any(axis=1))[0]
        kl = alive[-1] if len(alive) else -1
        # wind direction arrow (at that snapshot)
        wu, wv = ds.wind_u.values[kl], ds.wind_v.values[kl]
        if np.hypot(wu, wv) > 0.5:
            # arrow in the actual wind direction at that snapshot
            th = np.arctan2(wv, wu)
            x0a, y0a = 0.15, 0.82
            ax.annotate("", xy=(x0a + 0.1 * np.cos(th), y0a + 0.1 * np.sin(th)),
                        xytext=(x0a, y0a), xycoords="axes fraction",
                        arrowprops=dict(arrowstyle="->", color="tab:blue"))
            ax.text(0.03, 0.95, f"wind on day {ds.time.values[kl] / 86400:.0f}",
                    transform=ax.transAxes, color="tab:blue", fontsize=8)
        # mean drift angle
        u = np.nanmean(ds.floe_u.values[kl]); v = np.nanmean(ds.floe_v.values[kl])
        tday = ds.time.values[kl] / 86400
        if np.hypot(wu, wv) > 0.5:
            drift = f"drift {np.hypot(u, v):.3f} m/s, " \
                    f"{(np.degrees(np.arctan2(v, u) - np.arctan2(wv, wu)) + 180) % 360 - 180:+.1f}° from wind"
        else:
            drift = f"drift {np.hypot(u, v):.3f} m/s (wind ~0)"
        ax.set_title(f"{name}\nday {tday:.1f}: {drift}", fontsize=9)
        ax.axhline(0, color="0.85", lw=0.8, zorder=0)
        ax.axvline(0, color="0.85", lw=0.8, zorder=0)
        ax.set_xlabel("x displacement (km)")
    # same scale in x and y, same limits in every panel
    half = 0.55 * max(xr_[1] - xr_[0], yr_[1] - yr_[0], 1e-3)
    cx, cy = np.mean(xr_), np.mean(yr_)
    for ax in axs:
        ax.set_xlim(cx - half, cx + half)
        ax.set_ylim(cy - half, cy + half)
        ax.set_aspect("equal", adjustable="box")
    axs[0].set_ylabel("y displacement (km)")
    days = datasets[names[0]].time.values[-1] / 86400
    fig.suptitle(f"Floe trajectories over {days:.1f} days (unwrapped across periodic boundaries; "
                 "dot = end position)", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    path = FIG / f"{tag}_trajectories.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    register(path, f"Floe trajectories: '{tag}' runs",
             "Every floe's path as displacement from its starting point (km), unwrapped across "
             "the periodic boundaries so each path is one continuous line. One panel per run, "
             "same scale. Dot = last position with ice. Panel title: drift speed and angle to "
             "the wind at the last snapshot with ice.", {n: datasets[n] for n in names})
    print("saved", path)


def main():
    FIG.mkdir(exist_ok=True)
    files = [Path(a) for a in sys.argv[1:]] or sorted(OUT.glob("*.nc"))
    if not files:
        sys.exit("No .nc files found in output/. Run one of the scripts/run_*.jl scripts first.")
    datasets = {}
    for f in files:
        ds = xr.open_dataset(f)
        name = f.stem
        datasets[name] = ds
        floe_map(ds, name)
    # Group runs by name prefix (e.g. "free_drift", "paper") for comparison plots
    groups = {}
    for name, ds in datasets.items():
        groups.setdefault(name.split("_")[0], {})[name] = ds
    for tag, group in groups.items():
        trajectories(group, tag)
        drift_comparison(group, tag)
        thermo = any(int(d.attrs.get("thermo", 0)) for d in group.values())
        if thermo:  # thickness only changes when thermodynamics is on
            ice_comparison(group, tag)


if __name__ == "__main__":
    main()
