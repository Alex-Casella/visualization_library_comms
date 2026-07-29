"""Analyze and visualize NFL statistical leaders, 2020-2024.

Answers two questions directly from the data:
  1. Who is the statistical outlier in each category? (highest |z-score| among
     the yearly leaders in that stat)
  2. Who performs consistently? (players who led a category in 2+ seasons)

Renders a chart per category (outlier accented) plus a consistency chart.

    pip install -e .
    python examples/nfl_leaders.py

NOTE: pro-football-reference.com blocks automated access, so these values were
compiled from model knowledge and should be verified against PFR. See
datasets/README.md for per-cell confidence notes.
"""

from pathlib import Path

import pandas as pd

from simple_eda import Chart

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets" / "nfl_leaders_2020_2024.csv"
IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)
CAVEAT = "Compiled from model knowledge — verify vs. Pro-Football-Reference"

df = pd.read_csv(DATA)
df["last"] = df["player"].str.split().str[-1]
df["label"] = df["year"].astype(str).str[2:] + " " + df["last"]  # e.g. "20 Henry"

# 1. Standout (high-water-mark) season per category, with its z-score for
#    context — how far above the other yearly leaders that peak sits.
print("Standout season per category (peak value; z = SDs above the mean):")
for stat, g in df.groupby("stat", sort=False):
    g = g.sort_values("year")
    mean, std = g["value"].mean(), g["value"].std(ddof=0)
    g = g.assign(z=(g["value"] - mean) / std)
    out = g.loc[g["value"].idxmax()]
    print(f"  {stat:15s}: {out['player']} ({out['year']}) "
          f"{out['value']:g} {out['unit']}  z={out['z']:+.2f}")
    slug = stat.lower().replace(" ", "_")
    (Chart(g, x="label")
        .bar("value", highlight=out["label"], values=True)
        .title(f"{stat} leaders 2020-24 — {out['last']} ({out['year']}) stands out")
        .subtitle(CAVEAT)
        .labels(x="Season / leader", y=g["unit"].iloc[0])
        .save(str(IMAGES / f"nfl_{slug}.png")))

# 2. Consistency: who led a category in the most seasons?
counts = (df["player"].value_counts()
          .rename_axis("player").reset_index(name="seasons"))
repeat = counts[counts["seasons"] >= 2].copy()
repeat["last"] = repeat["player"].str.split().str[-1]
top = repeat[repeat["seasons"] == repeat["seasons"].max()]["last"].tolist()
print("\nConsistent leaders (led a category in 2+ seasons):")
for _, r in repeat.iterrows():
    print(f"  {r['player']}: {r['seasons']}")

(Chart(repeat, x="last")
    .bar("seasons", highlight=top, values=True, sort=True)
    .title(f"{' & '.join(top)} led most often, 2020-24")
    .subtitle("Category-seasons each player led | " + CAVEAT)
    .labels(x="Player", y="Category-seasons led")
    .save(str(IMAGES / "nfl_consistency.png")))

print("\nWrote charts to", IMAGES)
