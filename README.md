# simple-eda

A minimal, pandas-first visualization library for exploratory data analysis.
`simple_eda` is a thin, opinionated wrapper over
[matplotlib](https://matplotlib.org/) that turns pandas `DataFrame`s and
`Series` into clean charts through a small fluent API — sensible defaults, a
colorblind-friendly palette, and no boilerplate.

The entire library is a single ~120-line module (`simple_eda/core.py`).

## Layout

```
simple-eda-project/
├── src/
│   └── simple_eda/
│       ├── __init__.py
│       └── core.py
├── examples/
│   ├── quickstart.py
│   └── images/
├── tests/
│   └── test_core.py
├── README.md
├── pyproject.toml
└── LICENSE
```

## Install

```bash
pip install -e .          # installs simple_eda plus pandas + matplotlib
```

## Quick start

```python
import pandas as pd
from simple_eda import Chart

df = pd.DataFrame({
    "month":   ["Jan", "Feb", "Mar", "Apr"],
    "revenue": [120, 135, 128, 160],
    "cost":    [90, 95, 100, 110],
})

(Chart(df, x="month")
    .bar("cost")
    .line("revenue")
    .title("Q1 performance")
    .labels(x="Month", y="USD (thousands)")
    .save("q1.png"))
```

`x` defaults to the DataFrame's index if you don't pass it, and each plotting
call defaults to *all* non-`x` columns, so `Chart(df).line()` plots everything.

## API

Construct a `Chart(data, x=None, figsize=(8, 5))`, then chain layers and styling.
Every method returns the chart, so calls compose:

| Method | What it does |
| --- | --- |
| `.line(y=None, highlight=None)` | Trend over time — one line per column in `y` (all non-x by default) |
| `.bar(y=None, highlight=None)` | Compare groups — grouped vertical bars |
| `.scatter(y, size=None, highlight=None)` | Relationship between two columns; `size` maps a column to point area |
| `.hist(y, bins=20)` | Distribution of one numeric column |
| `.title(text)` | Left-aligned bold title |
| `.labels(x=, y=)` | Axis labels |
| `.save(path, dpi=150)` | Write to a file |
| `.show()` | Open an interactive window |

You can layer multiple calls onto one chart (e.g. `.bar(...).line(...)`); each
series is assigned the next palette color automatically, and a legend appears
when there's more than one series.

### Design defaults

`simple_eda` bakes in a few visualization best practices so you don't have to:

- **Right format for the job** — `line` for trends over time, `bar` to compare
  groups, `scatter` for relationships, `hist` for distributions.
- **Minimal chartjunk** — no boxed-in spines, and a single subtle horizontal
  grid instead of a full grid.
- **A limited palette** — six calm, colorblind-friendly colors.
- **Highlighting** — pass `highlight=` to draw the series (`line`) or
  x-categories (`bar`/`scatter`) you want noticed in a bright accent color,
  muting everything else to gray:

  ```python
  Chart(df, x="month").bar("revenue", highlight="Jun")   # accent June, mute the rest
  Chart(df, x="month").line(["revenue", "cost"], highlight="revenue")
  ```

### One-call helpers

For quick plots without chaining:

```python
from simple_eda import line, bar, scatter, hist

line(df, x="month", y="revenue").save("line.png")
scatter(df, x="cost", y="revenue").show()
hist(df, "revenue", bins=10).save("dist.png")
```

## Run the tests

```bash
pip install -e ".[test]"
pytest -q
```

## License

MIT — see [LICENSE](LICENSE).
