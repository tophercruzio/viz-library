"""simple-eda-christophersnook — a small, chainable matplotlib wrapper with a
luxe aesthetic.

Quick one-liners (the long import name is usually aliased)::

    import simple_eda_christophersnook as seda
    seda.line([1, 2, 3], [4, 5, 6], title="Demo").save("demo.png")

Or the chainable Chart, with raw matplotlib always reachable via .fig / .ax::

    from simple_eda_christophersnook import Chart
    Chart().line(x, y, label="a").labels("Demo", "x", "y").save("demo.png")

Two luxury themes ship in: "obsidian" (dark, the default) and "ivory" (light),
both built on warm neutrals, champagne-gold accents, and a muted jewel-tone
palette (gold, teal, garnet, sapphire, emerald, amethyst). The palette order is
colorblind-safe and validated against the data-viz colour checks.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

__version__ = "0.1.0"
__all__ = ["Chart", "line", "scatter", "bar", "barh", "hist", "pie",
           "use_theme", "available_themes", "PALETTE", "__version__"]

# Muted jewel tones + champagne gold, ordered so no two adjacent series collide
# under colourblind simulation. Each theme carries the steps tuned for its
# surface (validated: CVD ΔE >= 8, normal-vision ΔE >= 15, contrast >= 3:1).
_PALETTES = {  # gold, teal, garnet, sapphire, emerald, amethyst
    "obsidian": ["#a28626", "#0f9aa4", "#ac354a", "#4759b7", "#00834e", "#8e4aa7"],
    "ivory": ["#8d7100", "#007a9e", "#b02f43", "#2d51ab", "#00794a", "#82418f"],
}
PALETTE = _PALETTES["obsidian"]  # default palette (the dark theme)

# Shared chrome: thin lines, an editorial serif, a recessive y-only grid, and a
# surface-coloured hairline around fills so bars/wedges read as separated.
_SHARED = {
    "figure.dpi": 100, "font.family": "serif",
    "axes.axisbelow": True, "axes.grid": True, "axes.grid.axis": "y",
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8,
    "axes.titlesize": 15, "axes.titleweight": "normal", "axes.titlepad": 14,
    "axes.labelsize": 11, "axes.labelpad": 8, "grid.linewidth": 0.6,
    "lines.linewidth": 2.0, "lines.markersize": 7, "lines.solid_capstyle": "round",
    "patch.force_edgecolor": True, "patch.linewidth": 1.2,
    "legend.frameon": False, "xtick.labelsize": 9, "ytick.labelsize": 9,
}
_THEMES = {
    "obsidian": {  # dark luxury: warm obsidian surface, champagne-gold ink
        "figure.facecolor": "#0D0B08", "axes.facecolor": "#14120E",
        "savefig.facecolor": "#0D0B08", "text.color": "#EAE3D2",
        "axes.labelcolor": "#C9BFA8", "axes.titlecolor": "#C6A867",
        "axes.edgecolor": "#3A352B", "xtick.color": "#9A9078",
        "ytick.color": "#9A9078", "grid.color": "#26221B",
        "patch.edgecolor": "#14120E",
    },
    "ivory": {  # light luxury: warm ivory surface, antique-gold ink
        "figure.facecolor": "#F2ECDE", "axes.facecolor": "#F5F0E6",
        "savefig.facecolor": "#F2ECDE", "text.color": "#2A251C",
        "axes.labelcolor": "#4A4335", "axes.titlecolor": "#7A5C1E",
        "axes.edgecolor": "#D8CFBB", "xtick.color": "#6E6552",
        "ytick.color": "#6E6552", "grid.color": "#E4DCCB",
        "patch.edgecolor": "#F5F0E6",
    },
}
DEFAULT_THEME = "obsidian"


def available_themes():
    """List the theme names that use_theme accepts."""
    return sorted(_THEMES)


def use_theme(name=DEFAULT_THEME, palette=None):
    """Apply a named theme globally and set the matching color cycle."""
    if name not in _THEMES:
        raise ValueError(f"Unknown theme {name!r}; choose from {available_themes()}")
    mpl.rcParams.update(_SHARED)
    mpl.rcParams.update(_THEMES[name])
    mpl.rcParams["axes.prop_cycle"] = cycler(color=palette or _PALETTES[name])


class Chart:
    """One plot backed by a single matplotlib figure and axes.

    Every plotting/labelling method returns self so calls chain. Pass an
    existing ``ax`` to draw onto it (e.g. one cell of a subplot grid).
    """

    def __init__(self, figsize=(8, 5), theme=DEFAULT_THEME, ax=None):
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
