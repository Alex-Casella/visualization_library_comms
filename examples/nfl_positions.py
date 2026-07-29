"""Compare the top 5 players at each position over 2020-2024.

For each position it renders a bar chart ordered highest-to-lowest on the
defining volume stat, accenting the best player, and prints who tops each one.

    pip install -e .
    python examples/nfl_positions.py

IMPORTANT: these are APPROXIMATE five-season totals compiled from model
knowledge (pro-football-reference.com blocks automated access) and are NOT
verified. Rankings are indicative; treat every figure as "verify vs. PFR."
See datasets/README.md.
"""

from pathlib import Path

import pandas as pd

from simple_eda import Chart

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets" / "nfl_position_top5_2020_2024.csv"
IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)
CAVEAT = "Approximate 2020-24 totals from model knowledge — verify vs. PFR"

POSITIONS = {
    "QB": "passing yards",
    "RB": "rushing yards",
    "WR": "receiving yards",
    "Edge": "sacks",
}

df = pd.read_csv(DATA)
df["last"] = df["player"].str.split().str[-1]

print("Best at each position, 2020-24 (approximate — verify vs. PFR):")
for pos, blurb in POSITIONS.items():
    g = df[df["position"] == pos].sort_values("total", ascending=False)
    best = g.iloc[0]
    print(f"  {pos:5s}: {best['player']} ({best['team']}) "
          f"~{best['total']:g} {best['unit']}")
    # A horizontal dot / lollipop plot reads cleanly for a top-5 ranking.
    (Chart(g, x="last")
        .dot("total", highlight=best["last"], values=True)
        .title(f"Top 5 {pos}s by {blurb}, 2020-24 — {best['last']} leads")
        .subtitle(CAVEAT)
        .labels(x=f"Total {g['unit'].iloc[0]} (approx)")
        .save(str(IMAGES / f"nfl_top5_{pos.lower()}.png")))

print("\nWrote charts to", IMAGES)
