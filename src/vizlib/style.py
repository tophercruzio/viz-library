"""Themes and a clean default color palette for vizlib.

The goal is that a chart looks good with zero configuration. Applying a theme
tweaks matplotlib's rcParams; the palette is a set of colorblind-friendly hues
used to cycle through series.
"""

from __future__ import annotations

from cycler import cycler

import matplotlib as mpl

# A brand-neutral, colorblind-friendly categorical palette (Okabe-Ito derived).
PALETTE = [
    "#4C72B0",  # blue
    "#DD8452",  # orange
    "#55A868",  # green
    "#C44E52",  # red
    "#8172B3",  # purple
    "#937860",  # brown
    "#DA8BC3",  # pink
    "#8C8C8C",  # gray
    "#CCB974",  # gold
    "#64B5CD",  # cyan
]

# Named themes map to a dict of rcParams overrides.
_THEMES = {
    "clean": {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.labelcolor": "#333333",
        "grid.color": "#DDDDDD",
        "grid.linewidth": 0.6,
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "text.color": "#222222",
        "font.size": 10,
        "legend.frameon": False,
        "figure.dpi": 100,
    },
    "dark": {
        "figure.facecolor": "#1e1e1e",
        "axes.facecolor": "#1e1e1e",
        "axes.edgecolor": "#cccccc",
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.labelcolor": "#e0e0e0",
        "grid.color": "#3a3a3a",
        "grid.linewidth": 0.6,
        "xtick.color": "#cccccc",
        "ytick.color": "#cccccc",
        "text.color": "#e0e0e0",
        "font.size": 10,
        "legend.frameon": False,
        "figure.dpi": 100,
    },
    "minimal": {
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "legend.frameon": False,
        "figure.dpi": 100,
    },
}

DEFAULT_THEME = "clean"


def available_themes():
    """Return the list of theme names that :func:`use_theme` accepts."""
    return sorted(_THEMES)


def use_theme(name=DEFAULT_THEME, palette=None):
    """Apply a named theme globally via matplotlib rcParams.

    Parameters
    ----------
    name:
        One of :func:`available_themes`.
    palette:
        Optional list of colors to override the default cycle.
    """
    if name not in _THEMES:
        raise ValueError(
            f"Unknown theme {name!r}. Choose from {available_themes()}."
        )
    mpl.rcParams.update(_THEMES[name])
    colors = palette if palette is not None else PALETTE
    mpl.rcParams["axes.prop_cycle"] = cycler(color=colors)
