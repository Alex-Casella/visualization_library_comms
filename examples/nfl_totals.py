"""Aggregate NFL leaders across seasons and surface the accumulation outliers.

Builds a separate dataset that is NOT split by season: for each player + stat
it sums the values across the seasons that player LED the league, 2020-2024.

IMPORTANT: the source only contains each season's leader, so a player's total
here covers the seasons they *led* -- it is NOT their full multi-year output.
The aggregation therefore only changes the picture for players who led a stat
more than once (T.J. Watt in sacks, Davante Adams in receiving TDs).

    pip install -e .
    python examples/nfl_totals.py
"""

from pathlib import Path

import pandas as pd

from simple_eda import Chart

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "datasets" / "nfl_leaders_2020_2024.csv"
OUT = ROOT / "datasets" / "nfl_leader_totals_2020_2024.csv"
IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)
CAVEAT = "Totals across league-leading seasons only — verify vs. PFR"

df = pd.read_csv(SRC)

# Aggregate across seasons: one row per (player, stat), no year column.
totals = (df.groupby(["player", "category", "stat", "unit"], sort=False)
          .agg(total=("value", "sum"),
               seasons_led=("year", "count"),
               years=("year", lambda s: ";".join(map(str, sorted(s)))),
               teams=("team", lambda s: ";".join(sorted(set(s)))))
          .reset_index()
          .sort_values(["stat", "total"], ascending=[True, False]))
totals.to_csv(OUT, index=False)
print("Wrote", OUT.relative_to(ROOT), f"({len(totals)} rows)\n")

# Statistical outlier per stat: the highest accumulated total (z vs the field).
print("Outlier per stat (highest accumulated total; z = SDs above the mean):")
for stat, g in totals.groupby("stat", sort=False):
    mean, std = g["total"].mean(), g["total"].std(ddof=0)
    top = g.loc[g["total"].idxmax()]
    z = (top["total"] - mean) / std if std else 0.0
    flag = "  <-- stands out" if top["seasons_led"] > 1 else ""
    print(f"  {stat:15s}: {top['player']:18s} {top['total']:>6g} {top['unit']:<11s}"
          f" ({top['seasons_led']} season(s) led) z={z:+.2f}{flag}")

# Visualize the two stats where multi-season accumulation creates a real
# outlier: sacks (Watt) and receiving TDs (Adams).
for stat in ["Sacks", "Receiving TDs"]:
    g = totals[totals["stat"] == stat].copy()
    g["last"] = g["player"].str.split().str[-1]
    leader = g.loc[g["total"].idxmax(), "last"]
    (Chart(g, x="last")
        .bar("total", highlight=leader, values=True, sort=True)
        .title(f"{stat} 2020-24 — {leader} towers over the field")
        .subtitle(CAVEAT)
        .labels(x="Player", y=f"Total {g['unit'].iloc[0]} while leading")
        .save(str(IMAGES / f"nfl_total_{stat.lower().replace(' ', '_')}.png")))

print("\nWrote charts to", IMAGES)
