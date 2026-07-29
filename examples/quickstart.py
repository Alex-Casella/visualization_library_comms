"""Quickstart example for simple_eda.

A short tour of the chart types on the real NFL season-leaders dataset
(2020-2024). Renders to ``examples/images/``.

    pip install -e .
    python examples/quickstart.py

Values are compiled from model knowledge — verify vs. Pro-Football-Reference
(see datasets/README.md).
"""

from pathlib import Path

import pandas as pd

from simple_eda import Chart, hist

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets" / "nfl_leaders_2020_2024.csv"
IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df["season"] = df["year"].astype(str)                          # categorical x-axis
df["last"] = df["player"].str.split().str[-1]
df["label"] = df["year"].astype(str).str[2:] + " " + df["last"]  # e.g. "20 Henry"


def stat(name):
    return df[df["stat"] == name].sort_values("year")


# 1. Trend over time -> line: the passing-yards crown, season by season.
(Chart(stat("Passing Yards"), x="season")
    .line("value")
    .title("The passing-yards crown by season, 2020-24")
    .labels(x="Season", y="Yards")
    .save(str(IMAGES / "quickstart_line.png")))

# 2. Compare groups -> bar: rushing-yards leaders, sorted, standout accented.
ry = stat("Rushing Yards")
(Chart(ry, x="label")
    .bar("value", highlight=ry.loc[ry["value"].idxmax(), "label"],
         values=True, sort=True)
    .title("Henry's 2,027 tops the rushing leaders, 2020-24")
    .labels(x="Season / leader", y="Yards")
    .save(str(IMAGES / "quickstart_bar.png")))

# 3. Compare groups, ink-light -> dot / lollipop: receiving-yards leaders.
rec = stat("Receiving Yards")
(Chart(rec, x="label")
    .dot("value", highlight=rec.loc[rec["value"].idxmax(), "label"], values=True)
    .title("Receiving-yards leaders, 2020-24")
    .labels(x="Yards")
    .save(str(IMAGES / "quickstart_dot.png")))

# 4. Distribution -> histogram: skill-position (rush + rec) yardage leaders.
skill = df[df["stat"].isin(["Rushing Yards", "Receiving Yards"])]
(hist(skill, "value", bins=6)
    .title("Yardage leaders mostly land between 1,450 and 2,050")
    .labels(x="Yards", y="Seasons")
    .save(str(IMAGES / "quickstart_hist.png")))

print("Wrote charts to", IMAGES)
