"""
plot_floe_track.py -- trajectory of ONE chosen floe in the three free-drift runs
(no Coriolis, Coriolis with the original module, Coriolis with the extended
module), drawn on one set of axes.

Usage (from the Floe folder, with the .venv active):
    python plotting/plot_floe_track.py        # asks which floe number to plot
    python plotting/plot_floe_track.py 5      # plots floe number 5 directly

Saves figures/floe_<n>_trajectory.png
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from figindex import register  # figure catalogue (figures/FIGURES.md)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
FIG = ROOT / "figures"

# The three runs to compare: (file name, label, colour)
RUNS = [
    ("free_drift_no_coriolis.nc",       "no Coriolis",                      "tab:gray"),
    ("free_drift_coriolis_original.nc", "Coriolis, original module",        "tab:red"),
    ("free_drift_coriolis_extended.nc", "Coriolis, extended (vector drag)", "tab:blue"),
]


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


def ask_floe_number(n_max):
    """Floe number from the command line, or ask for it."""
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = input(f"Which floe do you want to plot? Enter a number from 1 to {n_max}: ")
    try:
        n = int(text)
    except ValueError:
        sys.exit(f"'{text}' is not a whole number.")
    if not 1 <= n <= n_max:
        sys.exit(f"Floe number must be between 1 and {n_max} (you entered {n}).")
    return n


def main():
    # Load the runs that exist
    runs = []
    loaded = {}                                # run name -> dataset (for the figure catalogue)
    for fname, label, colour in RUNS:
        path = OUT / fname
        if path.exists():
            runs.append((xr.open_dataset(path), label, colour))
            loaded[Path(fname).stem] = runs[-1][0]
        else:
            print(f"(skipping {fname}: not found in output/)")
    if not runs:
        sys.exit("None of the free-drift files were found. Run scripts/run_free_drift_check.jl first.")

    n_max = runs[0][0].floe_x.values.shape[1]
    n = ask_floe_number(n_max)
    i = n - 1                                  # Python counts from 0

    fig, ax = plt.subplots(figsize=(8, 5.5))
    for ds, label, colour in runs:
        Lx, Ly = float(ds.attrs["Lx"]), float(ds.attrs["Ly"])
        x = unwrap_track(ds.floe_x.values[:, i], Lx) / 1e3     # km
        y = unwrap_track(ds.floe_y.values[:, i], Ly) / 1e3
        u, v = ds.floe_u.values[-1, i], ds.floe_v.values[-1, i]
        wu, wv = ds.wind_u.values[-1], ds.wind_v.values[-1]
        ang = np.degrees(np.arctan2(v, u) - np.arctan2(wv, wu))
        ax.plot(x, y, color=colour, lw=2,
                label=f"{label}: {np.hypot(u, v):.3f} m/s, {ang:+.1f}° from wind")
        ax.plot(x[-1], y[-1], "o", color=colour)
    ax.plot(x[0], y[0], "k*", ms=12, label="start")

    ds0 = runs[0][0]
    r, h = ds0.floe_r.values[0, i], ds0.floe_h.values[0, i]
    days = ds0.time.values[-1] / 86400
    ax.annotate("", xy=(0.22, 0.92), xytext=(0.04, 0.92), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color="k"))
    ax.text(0.04, 0.95, "wind", transform=ax.transAxes, fontsize=9)
    ax.set(xlabel="x (km, unwrapped)", ylabel="y (km, unwrapped)",
           title=f"Floe {n} (radius {r:.0f} m, thickness {h:.2f} m): trajectory over {days:.1f} days")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    FIG.mkdir(exist_ok=True)
    path = FIG / f"floe_{n}_trajectory.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    register(path, f"Floe {n} trajectory in the three free-drift runs",
             f"Track of floe {n} (unwrapped across the box edges) in: no Coriolis (grey), "
             f"Coriolis with the original module's component-wise drag (red), and Coriolis with "
             f"the extended module's vector drag, Eq. 2 (blue). Star = start, dots = end. Legend: "
             f"final speed and angle to the wind.",
             loaded)
    print("saved", path)


if __name__ == "__main__":
    main()
