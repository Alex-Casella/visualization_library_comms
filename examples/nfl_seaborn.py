"""Extra NFL visualizations with seaborn — variety beyond matplotlib bars.

seaborn is an optional dependency:  pip install -e ".[viz]"  (or pip install seaborn)

Renders three non-bar charts from the NFL datasets:
  1. a heatmap of how hot/cold each season's leader ran per stat,
  2. faceted small-multiple line charts (one trend panel per stat),
  3. a drop-off line chart comparing the top-5 curve at each position.

Values are compiled from model knowledge — verify vs. Pro-Football-Reference.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", font_scale=1.0)

leaders = pd.read_csv(ROOT / "datasets" / "nfl_leaders_2020_2024.csv")
pos = pd.read_csv(ROOT / "datasets" / "nfl_position_top5_2020_2024.csv")

# 1. Heatmap: leader value per stat x season, colored by z-score within each
#    stat (so different scales are comparable), annotated with the raw value.
piv = leaders.pivot_table(index="stat", columns="year", values="value")
z = piv.sub(piv.mean(axis=1), axis=0).div(piv.std(axis=1), axis=0)
annot = piv.map(lambda v: "" if pd.isna(v) else f"{v:g}")
plt.figure(figsize=(8, 5))
sns.heatmap(z, annot=annot, fmt="", cmap="vlag", center=0, linewidths=0.5,
            cbar_kws={"label": "Hot / cold vs. that stat's 5-yr average"})
plt.title("Which season ran hot for each stat, 2020-24", fontweight="bold")
plt.xlabel(""); plt.ylabel("")
plt.tight_layout()
plt.savefig(IMAGES / "seaborn_heatmap.png", dpi=150)
plt.close()

# 2. Small multiples: one line panel per stat, each with its own y-scale.
g = sns.relplot(data=leaders, x="year", y="value", col="stat", kind="line",
                marker="o", col_wrap=4, height=2.6, aspect=1.1,
                facet_kws={"sharey": False})
g.set_titles("{col_name}")
g.set_axis_labels("Season", "Leader value")
g.figure.suptitle("Season-leader trend by stat, 2020-24", fontweight="bold")
g.figure.subplots_adjust(top=0.86)
g.savefig(IMAGES / "seaborn_trends.png", dpi=150)
plt.close(g.figure)

# 3. Drop-off curve: each position's top 5 as a % of that position's best,
#    so the steepness of the fall-off is comparable across positions.
pos = pos.copy()
pos["pct_of_best"] = pos.groupby("position")["total"].transform(lambda s: s / s.max() * 100)
plt.figure(figsize=(8, 5))
sns.lineplot(data=pos, x="rank", y="pct_of_best", hue="position",
             marker="o", linewidth=2)
plt.title("How fast the top 5 falls off at each position, 2020-24",
          fontweight="bold")
plt.xlabel("Rank (1 = best)"); plt.ylabel("% of the position's #1")
plt.xticks([1, 2, 3, 4, 5])
plt.tight_layout()
plt.savefig(IMAGES / "seaborn_dropoff.png", dpi=150)
plt.close()

print("Wrote seaborn charts to", IMAGES)
