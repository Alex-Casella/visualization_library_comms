"""simple_eda.core -- the plotting engine.

A thin, opinionated wrapper over matplotlib that turns pandas DataFrames and
Series into clean exploratory charts through a small fluent API. It follows a
few visualization best practices by default:

- Pick the right format: ``line`` for trends over time, ``bar`` to compare
  groups, ``scatter`` for relationships, ``hist`` for distributions.
- Keep it simple: no chartjunk -- minimal spines and a single subtle
  horizontal grid instead of a full grid.
- Limit colors: a six-color palette, plus one bright accent reserved for
  highlighting the point you want the audience to notice.

    import pandas as pd
    from simple_eda import Chart

    df = pd.DataFrame({"month": [...], "sales": [...], "cost": [...]})
    (Chart(df, x="month")
        .bar("sales", highlight="Jun")   # accent one bar, mute the rest
        .title("Sales by month")
        .labels(x="Month", y="Units")
        .save("sales.png"))
"""

from __future__ import annotations

from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import pandas as pd

# A limited (six-color), colorblind-friendly palette applied series-by-series.
_PALETTE = ["#4C78A8", "#F58518", "#54A24B",
            "#72B7B2", "#B279A2", "#9D755D"]
_ACCENT = "#E45756"   # one bright color, reserved for highlights
_MUTED = "#BAB0AC"    # everything de-emphasized falls back to this gray


def _as_frame(data: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
    """Accept a Series or DataFrame and always work with a DataFrame."""
    if isinstance(data, pd.Series):
        return data.to_frame()
    if isinstance(data, pd.DataFrame):
        return data
    raise TypeError("simple_eda expects a pandas DataFrame or Series, "
                    f"got {type(data).__name__}")


def _as_set(v):
    """Normalize a scalar / list of highlight keys into a set (or None)."""
    if v is None:
        return None
    return set(v) if isinstance(v, (list, tuple, set)) else {v}


class Chart:
    """A fluent, layered chart backed by a single matplotlib Axes.

    Each plotting call (``line``, ``bar``, ``scatter``, ``hist``) adds a layer
    and returns ``self`` so calls can be chained. ``x`` defaults to the frame's
    index when not given. Pass ``highlight=`` to a layer to draw the chosen
    series (``line``) or x-categories (``bar``/``scatter``) in the accent color
    and mute everything else.
    """

    def __init__(self, data: Union[pd.DataFrame, pd.Series],
                 x: Optional[str] = None, *, figsize=(8, 5)):
        self.df = _as_frame(data)
        self.x = x
        self._color_i = 0
        self.fig, self.ax = plt.subplots(figsize=figsize)
        # Keep it simple: a single subtle horizontal grid, no boxed-in spines.
        self.ax.grid(True, axis="y", alpha=0.25, linewidth=0.6)
        self.ax.set_axisbelow(True)
        self.ax.tick_params(labelsize=10)
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

    def _point_colors(self, hl) -> list[str]:
        """Accent for x-values in the highlight set, muted gray otherwise."""
        return [_ACCENT if xv in hl else _MUTED for xv in self._xvals()]

    # -- layers -----------------------------------------------------------
    def line(self, y: Union[str, Sequence[str], None] = None,
             highlight=None, **kwargs) -> "Chart":
        """Trend over time. ``highlight`` accents the named column(s)."""
        hl = _as_set(highlight)
        x = self._xvals()
        for col in self._columns(y):
            if hl is None:
                color, lw = self._next_color(), 2.0
            else:
                emph = col in hl
                color, lw = (_ACCENT, 2.5) if emph else (_MUTED, 1.3)
            self.ax.plot(x, self.df[col], label=col, color=color,
                         linewidth=lw, **kwargs)
        return self._finish_categorical()

    def bar(self, y: Union[str, Sequence[str], None] = None,
            highlight=None, **kwargs) -> "Chart":
        """Compare groups. ``highlight`` accents bars at the given x-value(s)."""
        hl = _as_set(highlight)
        cols = self._columns(y)
        x = self._xvals()
        positions = range(len(self.df))
        width = 0.8 / max(len(cols), 1)
        for i, col in enumerate(cols):
            offset = (i - (len(cols) - 1) / 2) * width
            color = self._point_colors(hl) if hl else self._next_color()
            self.ax.bar([p + offset for p in positions], self.df[col],
                        width=width, label=col, color=color, **kwargs)
        self.ax.set_xticks(list(positions))
        self.ax.set_xticklabels([str(v) for v in x])
        return self._finish_categorical()

    def scatter(self, y: str, *, size: Optional[str] = None,
                highlight=None, **kwargs) -> "Chart":
        """Relationship between two columns. ``highlight`` accents x-value(s)."""
        hl = _as_set(highlight)
        col = self._columns(y)[0]
        s = self.df[size] if size else None
        color = self._point_colors(hl) if hl else self._next_color()
        self.ax.scatter(self._xvals(), self.df[col], label=col, s=s,
                        c=color, alpha=0.85, edgecolor="white",
                        linewidth=0.5, **kwargs)
        return self._finish_categorical()

    def hist(self, y: str, *, bins: int = 20, **kwargs) -> "Chart":
        """Distribution of a single numeric column."""
        col = self._columns(y)[0]
        self.ax.hist(self.df[col].dropna(), bins=bins, label=col,
                     color=self._next_color(), alpha=0.85, **kwargs)
        return self

    # -- styling & output -------------------------------------------------
    def _finish_categorical(self) -> "Chart":
        if len(self.ax.get_legend_handles_labels()[0]) > 1:
            self.ax.legend(frameon=False, fontsize=10)
        return self

    def title(self, text: str) -> "Chart":
        self.ax.set_title(text, fontsize=14, fontweight="bold", loc="left")
        return self

    def labels(self, x: Optional[str] = None,
               y: Optional[str] = None) -> "Chart":
        if x is not None:
            self.ax.set_xlabel(x, fontsize=11)
        if y is not None:
            self.ax.set_ylabel(y, fontsize=11)
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
