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
├── datasets/
│   ├── nfl_leaders_2020_2024.csv
│   ├── nfl_leader_totals_2020_2024.csv
│   └── nfl_position_top5_2020_2024.csv
├── examples/
│   ├── quickstart.py
│   ├── nfl_leaders.py
│   ├── nfl_totals.py
│   ├── nfl_positions.py
│   ├── nfl_seaborn.py
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
    "player": ["Henry", "Taylor", "Jacobs", "McCaffrey", "Barkley"],
    "yards":  [2027, 1811, 1653, 1459, 2005],
})

(Chart(df, x="player")
    .bar("yards", highlight="Henry", values=True, sort=True)
    .title("Henry's 2,027 tops the rushing leaders, 2020-24")
    .labels(x="Rushing-yards leader", y="Yards")
    .save("rushing.png"))
```

`x` defaults to the DataFrame's index if you don't pass it, and each plotting
call defaults to *all* non-`x` columns, so `Chart(df).line()` plots everything.

## API

Construct a `Chart(data, x=None, figsize=(8, 5))`, then chain layers and styling.
Every method returns the chart, so calls compose:

| Method | What it does |
| --- | --- |
| `.line(y=None, highlight=None, label_lines=False)` | Trend over time; `label_lines` labels each line directly |
| `.bar(y=None, highlight=None, values=False, sort=False)` | Compare groups; `values` labels bars, `sort` orders descending |
| `.dot(y=None, highlight=None, values=False, sort=True)` | Dot / lollipop plot — ink-light comparison across groups |
| `.scatter(y, size=None, highlight=None)` | Relationship between two columns; `size` maps a column to point area |
| `.hist(y, bins=20)` | Distribution of one numeric column |
| `.title(text)` | Descriptive, left-aligned title (aim for 6–12 words) |
| `.subtitle(text)` | Smaller gray subtitle for context/annotation |
| `.labels(x=, y=)` | Axis labels |
| `.save(path, dpi=150)` / `.show()` | Write to a file / open a window |

You can layer multiple calls onto one chart (e.g. `.bar(...).line(...)`); each
series is assigned the next palette color automatically, and a legend appears
when there's more than one series (or use direct labels and drop it).

### Design defaults

`simple_eda` bakes in the guidance from two references so you don't have to
remember it on every chart:

- **[Evergreen Quantitative Chart Chooser](https://stephanieevergreen.com/)** —
  the chart types match its recommendations: `line` for change over time,
  `bar`/`dot` to compare groups, `scatter` for a relationship, `hist` for a
  distribution.
- **[Evergreen/Emery Data Visualization Checklist](https://stephanieevergreen.com/)** —
  the defaults implement its rules:

  | Checklist rule | How `simple_eda` applies it |
  | --- | --- |
  | Descriptive title, left-justified | `.title()` is bold, left-aligned |
  | Subtitle / annotations | `.subtitle()` adds gray context under the title |
  | Data labeled directly, drop the legend | `values=True` on `bar`/`dot`, `label_lines=True` on `line` |
  | Data intentionally ordered | `sort=True` on `bar`/`dot` |
  | Color highlights the key point; rest muted | `highlight=` → one accent color, everything else gray |
  | Limited, colorblind-safe palette | six-color palette |
  | Muted gridlines, no chartjunk | one faint horizontal grid, no tick marks, no top/right spines |
  | Two-dimensional, no decoration | flat 2D marks only |

  ```python
  # Accent the leader, sort bars, label them directly, add a "so what?" subtitle
  (Chart(df, x="player")
      .bar("yards", highlight="Passer A", values=True, sort=True)
      .title("Passer A leads the league in passing yards")
      .subtitle("2025 season, top five"))
  ```

### One-call helpers

For quick plots without chaining:

```python
from simple_eda import line, bar, dot, scatter, hist

bar(df, x="player", y="yards", highlight="Henry", values=True, sort=True).save("bar.png")
dot(df, x="player", y="sacks").show()
line(df, x="month", y="high").save("line.png")
```

## Run the tests

```bash
pip install -e ".[test]"
pytest -q
```

## License

MIT — see [LICENSE](LICENSE).
