"""vizlib — a small, chainable wrapper around matplotlib.

Quick one-liners::

    import vizlib
    vizlib.line([1, 2, 3], [4, 5, 6], title="Demo").save("demo.png")

Or the chainable Chart, with raw matplotlib always reachable via .fig / .ax::

    from vizlib import Chart
    Chart().line(x, y, label="a").labels("Demo", "x", "y").save("demo.png")
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

__version__ = "0.1.0"
__all__ = ["Chart", "line", "scatter", "bar", "barh", "hist", "pie",
           "use_theme", "available_themes", "PALETTE", "__version__"]

# Colorblind-friendly categorical palette (Okabe-Ito derived), cycled per series.
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
           "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]

_BASE = {"axes.grid": True, "axes.axisbelow": True, "axes.spines.top": False,
         "axes.spines.right": False, "axes.titlesize": 14,
         "axes.titleweight": "bold", "axes.labelsize": 11, "grid.linewidth": 0.6,
         "legend.frameon": False, "figure.dpi": 100}
_THEMES = {
    "clean": {**_BASE, "figure.facecolor": "white", "axes.facecolor": "white",
              "grid.color": "#DDDDDD"},
    "dark": {**_BASE, "figure.facecolor": "#1e1e1e", "axes.facecolor": "#1e1e1e",
             "grid.color": "#3a3a3a", "text.color": "#e0e0e0",
             "axes.labelcolor": "#e0e0e0", "axes.edgecolor": "#cccccc",
             "xtick.color": "#cccccc", "ytick.color": "#cccccc"},
    "minimal": {**_BASE, "axes.grid": False},
}


def available_themes():
    """List the theme names that use_theme accepts."""
    return sorted(_THEMES)


def use_theme(name="clean", palette=None):
    """Apply a named theme globally and set the color cycle."""
    if name not in _THEMES:
        raise ValueError(f"Unknown theme {name!r}; choose from {available_themes()}")
    mpl.rcParams.update(_THEMES[name])
    mpl.rcParams["axes.prop_cycle"] = cycler(color=palette or PALETTE)


class Chart:
    """One plot backed by a single matplotlib figure and axes.

    Every plotting/labelling method returns self so calls chain. Pass an
    existing ``ax`` to draw onto it (e.g. one cell of a subplot grid).
    """

    def __init__(self, figsize=(8, 5), theme="clean", ax=None):
        if theme:
            use_theme(theme)
        if ax is not None:
            self.ax, self.fig = ax, ax.figure
        else:
            self.fig, self.ax = plt.subplots(figsize=figsize)
        self._labelled = False

    def _draw(self, kind, *args, label=None, **kw):
        getattr(self.ax, kind)(*args, label=label, **kw)
        self._labelled = self._labelled or label is not None
        return self

    def line(self, x, y=None, label=None, **kw):
        """Line plot; omit y to use the index as x."""
        if y is None:
            x, y = range(len(x)), x
        return self._draw("plot", x, y, label=label, **kw)

    def scatter(self, x, y, label=None, **kw):
        return self._draw("scatter", x, y, label=label, **kw)

    def bar(self, x, height, label=None, **kw):
        return self._draw("bar", x, height, label=label, **kw)

    def barh(self, y, width, label=None, **kw):
        return self._draw("barh", y, width, label=label, **kw)

    def hist(self, data, bins=10, label=None, **kw):
        return self._draw("hist", data, label=label, bins=bins, **kw)

    def pie(self, values, labels=None, **kw):
        kw.setdefault("autopct", "%1.1f%%")
        self.ax.pie(values, labels=labels, **kw)
        self.ax.set_aspect("equal")
        return self

    def labels(self, title=None, xlabel=None, ylabel=None):
        """Set title and axis labels in one call (each optional)."""
        if title is not None:
            self.ax.set_title(title)
        if xlabel is not None:
            self.ax.set_xlabel(xlabel)
        if ylabel is not None:
            self.ax.set_ylabel(ylabel)
        return self

    def legend(self, **kw):
        self.ax.legend(**kw)
        return self

    def grid(self, visible=True, **kw):
        self.ax.grid(visible, **kw)
        return self

    def xlim(self, low=None, high=None):
        self.ax.set_xlim(low, high)
        return self

    def ylim(self, low=None, high=None):
        self.ax.set_ylim(low, high)
        return self

    def _finish(self):
        if self._labelled and self.ax.get_legend() is None:
            self.ax.legend()
        self.fig.tight_layout()

    def save(self, path, dpi=150, **kw):
        """Save with an auto legend and a tight bounding box."""
        self._finish()
        self.fig.savefig(path, dpi=dpi, bbox_inches="tight", **kw)
        return self

    def show(self):
        self._finish()
        plt.show()
        return self

    def close(self):
        plt.close(self.fig)
        return self


def _quick(kind):
    def fn(*args, title=None, xlabel=None, ylabel=None, figsize=(8, 5), **kw):
        chart = getattr(Chart(figsize=figsize), kind)(*args, **kw)
        return chart.labels(title, xlabel, ylabel)
    fn.__name__ = fn.__qualname__ = kind
    fn.__doc__ = f"Quick single-series {kind} chart; returns the Chart."
    return fn


line, scatter, bar, barh, hist, pie = map(
    _quick, ["line", "scatter", "bar", "barh", "hist", "pie"])
