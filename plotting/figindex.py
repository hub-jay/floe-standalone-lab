"""
figindex.py -- keeps a catalogue of all figures in figures/FIGURES.md.

Every plotting script calls register(...) after saving a figure. The entry
(file name, what it shows, which run files it came from, and those runs'
settings) is stored in figures/figure_index.json, and figures/FIGURES.md is
rewritten from it. Re-plotting a figure updates its entry.
"""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INDEX_JSON = FIG / "figure_index.json"
INDEX_MD = FIG / "FIGURES.md"


def _attr(ds, key, default="?"):
    v = ds.attrs.get(key, default)
    return v.item() if hasattr(v, "item") else v


def settings_summary(ds):
    """One-line description of a run's settings, read from its NetCDF attributes."""
    try:
        n_side = int(_attr(ds, "n_side", 0))
        nfloe = n_side ** 2
        rmin, rmax = float(_attr(ds, "rmin", 0)), float(_attr(ds, "rmax", 0))
        radius = (f"radius {rmin/1e3:g} km" if rmin == rmax
                  else f"radius {rmin/1e3:g}-{rmax/1e3:g} km")
        wind_mode = _attr(ds, "wind_mode")
        ws = float(_attr(ds, "wind_speed", 0))
        if ws == 0:
            wind = "no wind"
        elif wind_mode == "periodic":
            wind = (f"oscillating wind, peak {ws:g} m/s towards {float(_attr(ds, 'wind_dir_deg', 0)):g} deg, "
                    f"period {float(_attr(ds, 'wind_period_days', 0)):g} days")
        else:
            wind = f"constant wind {ws:g} m/s towards {float(_attr(ds, 'wind_dir_deg', 0)):g} deg"
        ocean = {"rest": "ocean at rest", "ekman": "Ekman surface current (paper Eq. 4)",
                 "eddy": f"{_attr(ds, 'eddy_sense')} eddy (R = {float(_attr(ds, 'eddy_radius', 0))/1e3:g} km, "
                         f"V = {float(_attr(ds, 'eddy_speed', 0)):g} m/s)"}.get(_attr(ds, "ocean_mode"), "?")
        cor = "Coriolis on" if int(_attr(ds, "use_coriolis", 0)) else "no Coriolis"
        thermo = (f"melting on (ocean {float(_attr(ds, 'T_ocean', 0)):g} degC)"
                  if int(_attr(ds, "thermo", 0)) else "no melting")
        dom = f"{float(_attr(ds, 'Lx', 0))/1e3:g} km box, {int(_attr(ds, 'nx', 0))}x{int(_attr(ds, 'ny', 0))} grid"
        model = f"model {_attr(ds, 'model_version')}"
        run = f"{float(_attr(ds, 'days', 0)):g} days, dt = {float(_attr(ds, 'dt', 0)):g} s"
        return (f"{nfloe} floe(s), {radius}, h0 = {float(_attr(ds, 'hmin', 0)):g} m; {wind}; {ocean}; "
                f"{cor}; {thermo}; {dom}; {model}; {run}")
    except Exception as err:                       # never let the catalogue break a plot
        return f"(settings unavailable: {err})"


def register(fig_path, title, description, runs):
    """Record a saved figure. runs: dict {run name: xarray Dataset}."""
    FIG.mkdir(exist_ok=True)
    try:
        index = json.loads(INDEX_JSON.read_text(encoding="utf-8")) if INDEX_JSON.exists() else {}
    except Exception:
        index = {}
    index[Path(fig_path).name] = {
        "title": title,
        "description": description,
        "runs": {name: settings_summary(ds) for name, ds in runs.items()},
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    # forget figures that have been deleted from the folder
    index = {k: v for k, v in index.items() if (FIG / k).exists()}
    INDEX_JSON.write_text(json.dumps(index, indent=2), encoding="utf-8")

    lines = ["# Figure catalogue",
             "",
             "Written automatically by the plotting scripts (plotting/figindex.py).",
             "Each entry: what the figure shows, and the run(s) it was made from with their settings.",
             ""]
    for name in sorted(index):
        e = index[name]
        lines += [f"## {name}", "", f"**{e['title']}**  ", f"_created {e['created']}_", "",
                  e["description"], "", "Runs:"]
        lines += [f"- `{run}.nc`: {s}" for run, s in e["runs"].items()]
        lines += [""]
    INDEX_MD.write_text("\n".join(lines), encoding="utf-8")
