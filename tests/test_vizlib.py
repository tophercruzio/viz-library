"""Tests for vizlib. These run headless via the Agg backend (set in conftest)."""

import os

import pytest

import vizlib
from vizlib import Chart


def test_chart_creates_figure_and_axes():
    c = Chart()
    assert c.fig is not None
    assert c.ax is not None
    c.close()


def test_line_is_chainable_and_draws():
    c = Chart().line([1, 2, 3], [4, 5, 6])
    assert isinstance(c, Chart)
    assert len(c.ax.lines) == 1
    c.close()


def test_line_with_single_arg_uses_index_as_x():
    c = Chart().line([4, 5, 6])
    line = c.ax.lines[0]
    assert list(line.get_xdata()) == [0, 1, 2]
    c.close()


def test_multiple_series_and_labels():
    c = Chart().line([1, 2], [3, 4], label="a").line([1, 2], [5, 6], label="b")
    assert len(c.ax.lines) == 2
    assert c._has_labels is True
    c.close()


def test_bar_and_scatter_and_hist():
    c = Chart()
    c.bar(["a", "b", "c"], [1, 2, 3])
    assert len(c.ax.patches) == 3
    c.close()

    c = Chart().scatter([1, 2, 3], [3, 2, 1])
    assert len(c.ax.collections) == 1
    c.close()

    c = Chart().hist([1, 1, 2, 3, 3, 3], bins=3)
    assert len(c.ax.patches) == 3
    c.close()


def test_pie_is_equal_aspect():
    c = Chart().pie([1, 2, 3], labels=["a", "b", "c"])
    assert c.ax.get_aspect() == 1.0
    c.close()


def test_labels_sets_title_and_axes():
    c = Chart().labels("T", "X", "Y")
    assert c.ax.get_title() == "T"
    assert c.ax.get_xlabel() == "X"
    assert c.ax.get_ylabel() == "Y"
    c.close()


def test_save_writes_file(tmp_path):
    out = tmp_path / "chart.png"
    Chart().line([1, 2, 3], [4, 5, 6], label="x").save(str(out)).close()
    assert out.exists()
    assert out.stat().st_size > 0


def test_auto_legend_added_on_save(tmp_path):
    out = tmp_path / "chart.png"
    c = Chart().line([1, 2], [3, 4], label="series")
    assert c.ax.get_legend() is None
    c.save(str(out))
    assert c.ax.get_legend() is not None
    c.close()


def test_quick_functions_return_chart(tmp_path):
    c = vizlib.line([1, 2, 3], [4, 5, 6], title="Q")
    assert isinstance(c, Chart)
    assert c.ax.get_title() == "Q"
    c.close()


def test_chart_accepts_existing_axes():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    c = Chart(ax=ax)
    assert c.ax is ax
    assert c.fig is fig
    plt.close(fig)


def test_use_theme_rejects_unknown():
    with pytest.raises(ValueError):
        vizlib.use_theme("does-not-exist")


def test_available_themes_nonempty():
    themes = vizlib.available_themes()
    assert "clean" in themes
    assert len(themes) >= 1
