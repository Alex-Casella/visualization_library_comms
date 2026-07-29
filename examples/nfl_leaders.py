"""Visualize NFL statistical leaders with simple_eda.

Loads the tidy leaders dataset and renders a bar chart per category, using the
highlight feature to accent the league leader. Run from the repo root:

    pip install -e .
    python examples/nfl_leaders.py

By default it reads the clearly-labeled SAMPLE dataset. To chart the real
2025 numbers, replace that file with real data in the same tidy schema
(category, stat, unit, rank, player, team, value) -- see datasets/README.md.
"""

from pathlib import Path

import pandas as pd

from simple_eda import Chart

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets" / "nfl_2025_leaders_sample.csv"
IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)

leaders = pd.read_csv(DATA)

# One bar chart per stat, with the rank-1 leader accented.
charts = [
    ("Passing Yards", "Passing yards leaders", "Yards"),
    ("Rushing Yards", "Rushing yards leaders", "Yards"),
    ("Receiving Yards", "Receiving yards leaders", "Yards"),
    ("Sacks", "Sack leaders", "Sacks"),
]

for stat, title, ylabel in charts:
    top = leaders[leaders["stat"] == stat].sort_values("value", ascending=False)
    leader = top.iloc[0]["player"]
    slug = stat.lower().replace(" ", "_")
    (Chart(top, x="player")
        .bar("value", highlight=leader)
        .title(f"{title} (2025, sample data)")
        .labels(x="Player", y=ylabel)
        .save(str(IMAGES / f"nfl_{slug}.png")))

print("Wrote NFL leader charts to", IMAGES)
