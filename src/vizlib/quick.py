"""One-liner helpers for the most common charts.

Each function builds a :class:`~vizlib.core.Chart`, draws a single series, and
returns the chart so you can keep customizing or call ``.save()`` / ``.show()``::

    vizlib.line([1, 2, 3], [4, 5, 6], title="Sales").save("sales.png")
"""

from __future__ import annotations

from .core import Chart


def _apply(chart, title, xlabel, ylabel):
    chart.labels(title=title, xlabel=xlabel, ylabel=ylabel)
    return chart


def line(x, y=None, title=None, xlabel=None, ylabel=None, figsize=(8, 5), **kwargs):
    """Quick line chart."""
    chart = Chart(figsize=figsize).line(x, y, **kwargs)
    return _apply(chart, title, xlabel, ylabel)


def scatter(x, y, title=None, xlabel=None, ylabel=None, figsize=(8, 5), **kwargs):
    """Quick scatter plot."""
    chart = Chart(figsize=figsize).scatter(x, y, **kwargs)
    return _apply(chart, title, xlabel, ylabel)


def bar(x, height, title=None, xlabel=None, ylabel=None, figsize=(8, 5), **kwargs):
    """Quick vertical bar chart."""
    chart = Chart(figsize=figsize).bar(x, height, **kwargs)
    return _apply(chart, title, xlabel, ylabel)


def barh(y, width, title=None, xlabel=None, ylabel=None, figsize=(8, 5), **kwargs):
    """Quick horizontal bar chart."""
    chart = Chart(figsize=figsize).barh(y, width, **kwargs)
    return _apply(chart, title, xlabel, ylabel)


def hist(data, bins=10, title=None, xlabel=None, ylabel=None, figsize=(8, 5), **kwargs):
    """Quick histogram."""
    chart = Chart(figsize=figsize).hist(data, bins=bins, **kwargs)
    return _apply(chart, title, xlabel, ylabel)


def pie(values, labels=None, title=None, figsize=(6, 6), **kwargs):
    """Quick pie chart."""
    chart = Chart(figsize=figsize).pie(values, labels=labels, **kwargs)
    if title is not None:
        chart.title(title)
    return chart
