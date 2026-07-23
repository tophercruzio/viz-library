"""vizlib — a small, functional wrapper around matplotlib.

Two ways to use it:

1. Quick one-liners for the common case::

       import vizlib
       vizlib.line([1, 2, 3], [4, 5, 6], title="Demo").save("demo.png")

2. The chainable :class:`Chart` for full control::

       from vizlib import Chart
       (Chart()
           .line([1, 2, 3], [4, 5, 6], label="a")
           .line([1, 2, 3], [6, 5, 4], label="b")
           .labels("Demo", "x", "y")
           .save("demo.png"))

The raw matplotlib figure and axes are always available as ``chart.fig`` and
``chart.ax`` when you need to drop down to matplotlib directly.
"""

from __future__ import annotations

from .core import Chart
from .quick import bar, barh, hist, line, pie, scatter
from .style import PALETTE, available_themes, use_theme

__version__ = "0.1.0"

__all__ = [
    "Chart",
    "line",
    "scatter",
    "bar",
    "barh",
    "hist",
    "pie",
    "use_theme",
    "available_themes",
    "PALETTE",
    "__version__",
]
