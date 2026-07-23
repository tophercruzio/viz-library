"""Tests for vizlib (headless via the Agg backend, set in conftest)."""

import pytest

import vizlib
from vizlib import Chart


def test_line_is_chainable_and_draws():
    c = Chart().line([1, 2, 3], [4, 5, 6])
    assert isinstance(c, Chart) and len(c.ax.lines) == 1
    c.close()


def test_line_single_arg_uses_index_as_x():
    c = Chart().line([4, 5, 6])
    assert list(c.ax.lines[0].get_xdata()) == [0, 1, 2]
    c.close()


def test_bar_scatter_hist_pie():
    assert len(Chart().bar(["a", "b", "c"], [1, 2, 3]).ax.patches) == 3
    assert len(Chart().scatter([1, 2], [2, 1]).ax.collections) == 1
    assert len(Chart().hist([1, 1, 2, 3, 3, 3], bins=3).ax.patches) == 3
    assert Chart().pie([1, 2, 3]).ax.get_aspect() == 1.0


def test_labels_and_auto_legend(tmp_path):
    c = Chart().line([1, 2], [3, 4], label="s").labels("T", "X", "Y")
    assert (c.ax.get_title(), c.ax.get_xlabel(), c.ax.get_ylabel()) == ("T", "X", "Y")
    assert c.ax.get_legend() is None
    out = tmp_path / "c.png"
    c.save(str(out))
    assert out.stat().st_size > 0 and c.ax.get_legend() is not None
    c.close()


def test_chart_wraps_existing_axes():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    c = Chart(ax=ax)
    assert c.ax is ax and c.fig is fig
    plt.close(fig)


def test_quick_functions_return_chart():
    c = vizlib.bar(["a", "b"], [1, 2], title="Q")
    assert isinstance(c, Chart) and c.ax.get_title() == "Q"
    c.close()


def test_themes():
    assert "clean" in vizlib.available_themes()
    with pytest.raises(ValueError):
        vizlib.use_theme("nope")
