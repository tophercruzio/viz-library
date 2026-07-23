# vizlib

A small, functional wrapper around [matplotlib](https://matplotlib.org/) for
quick, good-looking charts. It gives you sensible defaults and a chainable API,
without hiding matplotlib when you need it.

## Install

```bash
pip install -e .
```

Requires Python 3.8+ and `matplotlib>=3.5`.

## Quick start

One-liners for the common case:

```python
import vizlib

vizlib.line([1, 2, 3], [4, 5, 6], title="Sales", xlabel="week", ylabel="$").save("sales.png")
vizlib.bar(["a", "b", "c"], [3, 7, 2], title="Counts").show()
vizlib.hist([1, 1, 2, 3, 3, 3], bins=3, title="Distribution").save("dist.png")
```

The chainable `Chart` for full control:

```python
from vizlib import Chart

(Chart(figsize=(8, 5), theme="obsidian")
    .line(range(10), [x * x for x in range(10)], label="squared")
    .line(range(10), [x * 3 for x in range(10)], label="linear")
    .labels("Growth", "step", "value")
    .save("growth.png"))
```

Labelled series get a legend automatically when you `save()` or `show()`.

## What you get

- **Chart types**: `line`, `scatter`, `bar`, `barh`, `hist`, `pie` — as both
  chainable `Chart` methods and quick module-level functions.
- **Luxury themes**: `obsidian` (dark, default) and `ivory` (light) — warm
  neutral surfaces, an editorial serif, champagne-gold titles, and a recessive
  grid. Apply with a `theme=` argument or globally via `vizlib.use_theme(...)`.
- **A validated jewel-tone palette** — gold, teal, garnet, sapphire, emerald,
  amethyst (`vizlib.PALETTE`), cycled across series. The order is
  colorblind-safe: it passes CVD ΔE ≥ 8, normal-vision ΔE ≥ 15, and ≥ 3:1
  surface contrast on both themes.
- **Sensible output**: `save()` uses a tight bounding box and 150 dpi by
  default.

## Dropping down to matplotlib

Nothing is hidden. Every `Chart` exposes the raw figure and axes:

```python
c = Chart().line([1, 2, 3], [4, 5, 6])
c.ax.axhline(5, linestyle="--")   # any matplotlib Axes method
c.fig.suptitle("Custom")           # any matplotlib Figure method
c.save("out.png")
```

You can also wrap an existing axes, e.g. one cell of a subplot grid:

```python
import matplotlib.pyplot as plt
from vizlib import Chart

fig, axes = plt.subplots(1, 2)
Chart(ax=axes[0]).line([1, 2, 3], [3, 2, 1])
Chart(ax=axes[1]).bar(["x", "y"], [4, 8])
```

## API reference

| Function / method | Description |
|---|---|
| `Chart(figsize, theme, ax)` | Create a chart (or wrap an existing axes). |
| `.line(x, y=None, label=None, **kw)` | Line plot; omit `y` to use the index as x. |
| `.scatter(x, y, label=None, **kw)` | Scatter plot. |
| `.bar(x, height, ...)` / `.barh(y, width, ...)` | Vertical / horizontal bars. |
| `.hist(data, bins=10, ...)` | Histogram. |
| `.pie(values, labels=None, ...)` | Pie chart (kept circular). |
| `.title/.xlabel/.ylabel/.labels(...)` | Text labelling. |
| `.legend/.grid/.xlim/.ylim(...)` | Common axes tweaks. |
| `.save(path, dpi=150, ...)` | Save to a file. |
| `.show()` / `.close()` | Display / free the figure. |
| `vizlib.line/scatter/bar/barh/hist/pie(...)` | Quick single-series charts. |
| `vizlib.use_theme(name, palette=None)` | Apply a theme globally. |
| `vizlib.available_themes()` | List theme names. |

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
