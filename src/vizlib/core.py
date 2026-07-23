"""The :class:`Chart` object — a thin, chainable wrapper around matplotlib.

Every plotting method returns ``self`` so calls can be chained::

    Chart().line([1, 2, 3], [4, 5, 6]).title("Demo").save("out.png")

The underlying matplotlib :class:`~matplotlib.axes.Axes` and
:class:`~matplotlib.figure.Figure` are always reachable through the ``ax`` and
``fig`` attributes, so nothing matplotlib can do is hidden from you.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from .style import DEFAULT_THEME, use_theme


class Chart:
    """A single plot backed by one matplotlib figure and axes.

    Parameters
    ----------
    figsize:
        Figure size in inches, ``(width, height)``.
    theme:
        Name of a theme to apply, or ``None`` to leave global rcParams alone.
    ax:
        An existing matplotlib axes to draw on. When given, ``figsize`` is
        ignored and the chart will not create its own figure.
    """

    def __init__(self, figsize=(8, 5), theme=DEFAULT_THEME, ax=None):
        if theme is not None:
            use_theme(theme)
        if ax is not None:
            self.ax = ax
            self.fig = ax.figure
        else:
            self.fig, self.ax = plt.subplots(figsize=figsize)
        self._has_labels = False

    # -- plotting -------------------------------------------------------
    def line(self, x, y=None, label=None, **kwargs):
        """Draw a line. If ``y`` is omitted, ``x`` is treated as the y-values."""
        if y is None:
            x, y = range(len(x)), x
        self.ax.plot(x, y, label=label, **kwargs)
        self._track_label(label)
        return self

    def scatter(self, x, y, label=None, **kwargs):
        """Draw a scatter plot."""
        self.ax.scatter(x, y, label=label, **kwargs)
        self._track_label(label)
        return self

    def bar(self, x, height, label=None, **kwargs):
        """Draw a vertical bar chart. ``x`` may be labels or positions."""
        self.ax.bar(x, height, label=label, **kwargs)
        self._track_label(label)
        return self

    def barh(self, y, width, label=None, **kwargs):
        """Draw a horizontal bar chart."""
        self.ax.barh(y, width, label=label, **kwargs)
        self._track_label(label)
        return self

    def hist(self, data, bins=10, label=None, **kwargs):
        """Draw a histogram."""
        self.ax.hist(data, bins=bins, label=label, **kwargs)
        self._track_label(label)
        return self

    def pie(self, values, labels=None, **kwargs):
        """Draw a pie chart and force equal aspect so it stays circular."""
        kwargs.setdefault("autopct", "%1.1f%%")
        self.ax.pie(values, labels=labels, **kwargs)
        self.ax.set_aspect("equal")
        return self

    # -- labelling ------------------------------------------------------
    def title(self, text, **kwargs):
        self.ax.set_title(text, **kwargs)
        return self

    def xlabel(self, text, **kwargs):
        self.ax.set_xlabel(text, **kwargs)
        return self

    def ylabel(self, text, **kwargs):
        self.ax.set_ylabel(text, **kwargs)
        return self

    def labels(self, title=None, xlabel=None, ylabel=None):
        """Set title and axis labels in one call."""
        if title is not None:
            self.title(title)
        if xlabel is not None:
            self.xlabel(xlabel)
        if ylabel is not None:
            self.ylabel(ylabel)
        return self

    def legend(self, **kwargs):
        """Show the legend. Called automatically by :meth:`save`/:meth:`show`
        when any labelled series exist."""
        self.ax.legend(**kwargs)
        return self

    def grid(self, visible=True, **kwargs):
        self.ax.grid(visible, **kwargs)
        return self

    def xlim(self, low=None, high=None):
        self.ax.set_xlim(low, high)
        return self

    def ylim(self, low=None, high=None):
        self.ax.set_ylim(low, high)
        return self

    # -- output ---------------------------------------------------------
    def save(self, path, dpi=150, transparent=False, **kwargs):
        """Save the figure to ``path`` with a tight bounding box."""
        self._auto_legend()
        self.fig.tight_layout()
        self.fig.savefig(
            path, dpi=dpi, bbox_inches="tight", transparent=transparent, **kwargs
        )
        return self

    def show(self):
        """Display the figure in an interactive window."""
        self._auto_legend()
        self.fig.tight_layout()
        plt.show()
        return self

    def close(self):
        """Close the underlying figure to free memory."""
        plt.close(self.fig)
        return self

    # -- internals ------------------------------------------------------
    def _track_label(self, label):
        if label is not None:
            self._has_labels = True

    def _auto_legend(self):
        if self._has_labels and self.ax.get_legend() is None:
            self.ax.legend()
