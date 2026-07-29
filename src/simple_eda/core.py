"""simple_eda.core -- the plotting engine.

A pandas-first wrapper over matplotlib whose defaults follow the Evergreen/Emery
Data Visualization Checklist, with chart types mirroring the Evergreen Chart
Chooser: line (over time), bar/dot (compare groups), scatter (relationship),
hist (distribution). See the top-level README for the full mapping.
"""

from __future__ import annotations

from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import pandas as pd

# A limited (six-color), colorblind-friendly palette applied series-by-series.
_PALETTE = ["#4C78A8", "#F58518", "#54A24B", "#72B7B2", "#B279A2", "#9D755D"]
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


def _fmt(v) -> str:
    """Format a data label with minimal precision (few decimals)."""
    return f"{v:g}"


class Chart:
    """A fluent chart on one Axes. Layer calls chain; ``x`` defaults to the
    index. ``highlight=`` accents series/categories; ``values=True`` labels."""

    def __init__(self, data, x: Optional[str] = None, *, figsize=(8, 5)):
        self.df = _as_frame(data)
        self.x = x
        self._color_i = 0
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.grid(True, axis="y", alpha=0.25, linewidth=0.6)  # muted grid
        self.ax.set_axisbelow(True)
        self.ax.tick_params(length=0, labelsize=10)              # no tick marks
        for spine in ("top", "right"):
            self.ax.spines[spine].set_visible(False)

    def _next_color(self) -> str:
        c = _PALETTE[self._color_i % len(_PALETTE)]
        self._color_i += 1
        return c

    def _xvals(self):
        return self.df[self.x] if self.x is not None else self.df.index

    def _columns(self, cols) -> list:
        if cols is None:
            cols = [c for c in self.df.columns if c != self.x]
        elif isinstance(cols, str):
            cols = [cols]
        missing = [c for c in cols if c not in self.df.columns]
        if missing:
            raise KeyError(f"column(s) not found in data: {missing}")
        return list(cols)

    def _colors(self, xs, hl):
        """Accent for x-values in the highlight set, muted gray otherwise."""
        return [_ACCENT if xv in hl else _MUTED for xv in xs]

    def line(self, y=None, highlight=None, label_lines=False, **kwargs):
        """Trend over time; ``label_lines`` labels each line directly."""
        hl = _as_set(highlight)
        x = self._xvals()
        xv = list(x)
        for col in self._columns(y):
            if hl is None:
                color, lw = self._next_color(), 2.0
            else:
                color, lw = (_ACCENT, 2.5) if col in hl else (_MUTED, 1.3)
            self.ax.plot(x, self.df[col], label=col, color=color,
                         linewidth=lw, **kwargs)
            if label_lines:
                self.ax.text(xv[-1], self.df[col].iloc[-1], f"  {col}",
                             color=color, va="center", fontsize=10)
        return self if label_lines else self._finish_categorical()

    def bar(self, y=None, highlight=None, values=False, sort=False, **kwargs):
        """Compare groups; ``values`` labels bars, ``sort`` orders descending."""
        hl = _as_set(highlight)
        cols = self._columns(y)
        df = self.df.sort_values(cols[0], ascending=False) \
            if sort and len(cols) == 1 else self.df
        x = df[self.x] if self.x is not None else df.index
        positions = range(len(df))
        width = 0.8 / max(len(cols), 1)
        for i, col in enumerate(cols):
            pos = [p + (i - (len(cols) - 1) / 2) * width for p in positions]
            color = self._colors(x, hl) if hl else self._next_color()
            self.ax.bar(pos, df[col], width=width, label=col, color=color, **kwargs)
            if values:
                for p, v in zip(pos, df[col]):
                    self.ax.text(p, v, _fmt(v), ha="center", va="bottom", fontsize=9)
        self.ax.set_xticks(list(positions))
        self.ax.set_xticklabels([str(v) for v in x])
        return self._finish_categorical()

    def dot(self, y=None, highlight=None, values=False, sort=True):
        """Dot / lollipop plot -- an ink-light horizontal group comparison."""
        hl = _as_set(highlight)
        col = self._columns(y)[0]
        df = self.df.sort_values(col) if sort else self.df
        x = df[self.x] if self.x is not None else df.index
        ys = list(range(len(df)))
        colors = self._colors(x, hl) if hl else _PALETTE[0]
        self.ax.hlines(ys, 0, df[col], colors=colors, linewidth=2, alpha=0.6)
        self.ax.scatter(df[col], ys, c=colors, s=60, zorder=3)
        self.ax.set_yticks(ys)
        self.ax.set_yticklabels([str(v) for v in x])
        if values:
            for yy, v in zip(ys, df[col]):
                self.ax.text(v, yy, f" {_fmt(v)}", va="center", fontsize=9)
        return self

    def scatter(self, y, *, size=None, highlight=None, **kwargs):
        """Relationship between two columns. ``highlight`` accents x-value(s)."""
        hl = _as_set(highlight)
        col = self._columns(y)[0]
        s = self.df[size] if size else None
        color = self._colors(self._xvals(), hl) if hl else self._next_color()
        self.ax.scatter(self._xvals(), self.df[col], label=col, s=s, c=color,
                        alpha=0.85, edgecolor="white", linewidth=0.5, **kwargs)
        return self._finish_categorical()

    def hist(self, y, *, bins: int = 20, **kwargs):
        """Distribution of a single numeric column."""
        col = self._columns(y)[0]
        self.ax.hist(self.df[col].dropna(), bins=bins, label=col,
                     color=self._next_color(), alpha=0.85, **kwargs)
        return self

    def _finish_categorical(self):
        if len(self.ax.get_legend_handles_labels()[0]) > 1:
            self.ax.legend(frameon=False, fontsize=10)
        return self

    def title(self, text: str):
        """A descriptive, left-aligned title (aim for 6-12 words)."""
        self.ax.set_title(text, fontsize=14, fontweight="bold", loc="left", pad=24)
        return self

    def subtitle(self, text: str):
        """A smaller gray subtitle under the title for context/annotation."""
        self.ax.text(0, 1.02, text, transform=self.ax.transAxes,
                     fontsize=11, color="#666666", ha="left", va="bottom")
        return self

    def labels(self, x=None, y=None):
        if x is not None:
            self.ax.set_xlabel(x, fontsize=11)
        if y is not None:
            self.ax.set_ylabel(y, fontsize=11)
        return self

    def save(self, path: str, *, dpi: int = 150):
        self.fig.tight_layout()
        self.fig.savefig(path, dpi=dpi, bbox_inches="tight")
        return self

    def show(self):
        self.fig.tight_layout()
        plt.show()
        return self


def line(data, x=None, y=None, **kw):
    return Chart(data, x=x).line(y, **kw)

def bar(data, x=None, y=None, **kw):
    return Chart(data, x=x).bar(y, **kw)

def dot(data, x=None, y=None, **kw):
    return Chart(data, x=x).dot(y, **kw)

def scatter(data, x, y, **kw):
    return Chart(data, x=x).scatter(y, **kw)

def hist(data, y, **kw):
    return Chart(data).hist(y, **kw)
