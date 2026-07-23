"""Smoke tests for simple_eda. Uses matplotlib's non-interactive backend."""

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import pytest

from simple_eda import Chart, bar, hist, line, scatter

DF = pd.DataFrame({
    "x": ["a", "b", "c", "d"],
    "y1": [1, 3, 2, 5],
    "y2": [2, 1, 4, 3],
})


def test_line_layers_all_columns_by_default():
    c = Chart(DF, x="x").line()
    assert len(c.ax.get_lines()) == 2  # y1 and y2


def test_chaining_returns_same_chart():
    c = Chart(DF, x="x")
    assert c.line("y1").bar("y2") is c


def test_series_input_is_accepted():
    c = Chart(DF["y1"]).line()
    assert len(c.ax.get_lines()) == 1


def test_missing_column_raises():
    with pytest.raises(KeyError):
        Chart(DF, x="x").line("nope")


def test_bad_type_raises():
    with pytest.raises(TypeError):
        Chart([1, 2, 3])


def test_scatter_and_hist_helpers():
    assert scatter(DF, x="y1", y="y2").ax.collections
    assert hist(DF, "y1", bins=3).ax.patches


def test_save_writes_file(tmp_path):
    out = tmp_path / "out.png"
    bar(DF, x="x", y="y1").save(str(out))
    assert out.exists() and out.stat().st_size > 0


def test_convenience_line_helper():
    assert len(line(DF, x="x", y=["y1", "y2"]).ax.get_lines()) == 2
