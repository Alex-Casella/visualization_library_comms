"""simple_eda.core -- the plotting engine.

A thin, opinionated wrapper over matplotlib that turns pandas DataFrames and
Series into clean exploratory charts through a small fluent API:

    import pandas as pd
    from simple_eda import Chart

    df = pd.DataFrame({"month": [...], "sales": [...], "cost": [...]})
    (Chart(df, x="month")
        .line("sales")
        .bar("cost")
        .title("Q1 performance")
        .save("q1.png"))
"""

from __future__ import annotations

from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import pandas as pd

# A calm, colorblind-friendly categorical palette applied series-by-series.
_PALETTE = ["#4C78A8", "#F58518", "#54A24B", "#E45756",
            "#72B7B2", "#B279A2", "#EECA3B", "#9D755D"]


def _as_frame(data: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
    """Accept a Series or DataFrame and always work with a DataFrame."""
    if isinstance(data, pd.Series):
        return data.to_frame()
    if isinstance(data, pd.DataFrame):
        return data
    raise TypeError("simple_eda expects a pandas DataFrame or Series, "
                    f"got {type(data).__name__}")


class Chart:
    """A fluent, layered chart backed by a single matplotlib Axes.

    Each plotting call (``line``, ``bar``, ``scatter``, ``hist``) adds a layer
    and returns ``self`` so calls can be chained. ``x`` defaults to the frame's
    index when not given.
    """

    def __init__(self, data: Union[pd.DataFrame, pd.Series],
                 x: Optional[str] = None, *, figsize=(8, 5)):
        self.df = _as_frame(data)
        self.x = x
        self._color_i = 0
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.grid(True, alpha=0.3, linewidth=0.6)
        self.ax.set_axisbelow(True)
        for spine in ("top", "right"):
            self.ax.spines[spine].set_visible(False)

    # -- internal helpers -------------------------------------------------
    def _next_color(self) -> str:
        c = _PALETTE[self._color_i % len(_PALETTE)]
        self._color_i += 1
        return c

    def _xvals(self):
        return self.df[self.x] if self.x is not None else self.df.index

    def _columns(self, cols: Union[str, Sequence[str], None]) -> list[str]:
        if cols is None:
            cols = [c for c in self.df.columns if c != self.x]
        elif isinstance(cols, str):
            cols = [cols]
        missing = [c for c in cols if c not in self.df.columns]
        if missing:
            raise KeyError(f"column(s) not found in data: {missing}")
        return list(cols)

    # -- layers -----------------------------------------------------------
    def line(self, y: Union[str, Sequence[str], None] = None,
             **kwargs) -> "Chart":
        """Draw one line per column in ``y`` (all non-x columns by default)."""
        x = self._xvals()
        for col in self._columns(y):
            self.ax.plot(x, self.df[col], label=col,
                         color=self._next_color(), linewidth=2, **kwargs)
        return self._finish_categorical()

    def bar(self, y: Union[str, Sequence[str], None] = None,
            **kwargs) -> "Chart":
        """Draw grouped vertical bars, one group of bars per column."""
        cols = self._columns(y)
        x = self._xvals()
        positions = range(len(self.df))
        width = 0.8 / max(len(cols), 1)
        for i, col in enumerate(cols):
            offset = (i - (len(cols) - 1) / 2) * width
            self.ax.bar([p + offset for p in positions], self.df[col],
                        width=width, label=col, color=self._next_color(),
                        **kwargs)
        self.ax.set_xticks(list(positions))
        self.ax.set_xticklabels([str(v) for v in x])
        return self._finish_categorical()

    def scatter(self, y: str, *, size: Optional[str] = None,
                **kwargs) -> "Chart":
        """Scatter ``y`` against ``x``; ``size`` optionally maps a column to area."""
        col = self._columns(y)[0]
        s = self.df[size] if size else None
        self.ax.scatter(self._xvals(), self.df[col], label=col, s=s,
                        color=self._next_color(), alpha=0.75,
                        edgecolor="white", linewidth=0.5, **kwargs)
        return self._finish_categorical()

    def hist(self, y: str, *, bins: int = 20, **kwargs) -> "Chart":
        """Histogram of a single numeric column."""
        col = self._columns(y)[0]
        self.ax.hist(self.df[col].dropna(), bins=bins, label=col,
                     color=self._next_color(), alpha=0.85, **kwargs)
        return self

    # -- styling & output -------------------------------------------------
    def _finish_categorical(self) -> "Chart":
        if len(self.ax.get_legend_handles_labels()[0]) > 1:
            self.ax.legend(frameon=False)
        return self

    def title(self, text: str) -> "Chart":
        self.ax.set_title(text, fontsize=14, fontweight="bold", loc="left")
        return self

    def labels(self, x: Optional[str] = None,
               y: Optional[str] = None) -> "Chart":
        if x is not None:
            self.ax.set_xlabel(x)
        if y is not None:
            self.ax.set_ylabel(y)
        return self

    def save(self, path: str, *, dpi: int = 150) -> "Chart":
        self.fig.tight_layout()
        self.fig.savefig(path, dpi=dpi, bbox_inches="tight")
        return self

    def show(self) -> "Chart":
        self.fig.tight_layout()
        plt.show()
        return self


# -- one-call convenience functions ---------------------------------------
def line(data, x=None, y=None, **kw) -> Chart:
    return Chart(data, x=x).line(y, **kw)


def bar(data, x=None, y=None, **kw) -> Chart:
    return Chart(data, x=x).bar(y, **kw)


def scatter(data, x, y, **kw) -> Chart:
    return Chart(data, x=x).scatter(y, **kw)


def hist(data, y, **kw) -> Chart:
    return Chart(data).hist(y, **kw)
