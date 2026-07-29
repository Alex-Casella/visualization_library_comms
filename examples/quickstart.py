"""Quickstart example for simple_eda.

Demonstrates picking the right chart for the job and using a single accent
color to highlight the point worth noticing, on a small illustrative weather
dataset. Renders to ``examples/images/``.

    pip install -e .
    python examples/quickstart.py
"""

from pathlib import Path

import pandas as pd

from simple_eda import Chart, hist

IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)

weather = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "high": [45, 50, 58, 67, 75, 84],
    "low": [30, 33, 40, 48, 56, 64],
    "rainfall": [3.1, 2.8, 3.5, 3.0, 4.2, 3.8],
})

# 1. Trend over time -> line. Two series; highlight the one that matters.
(Chart(weather, x="month")
    .line(["high", "low"], highlight="high")
    .title("Daytime highs climb into summer")
    .labels(x="Month", y="Degrees (F)")
    .save(str(IMAGES / "quickstart_line.png")))

# 2. Compare groups -> bar. Accent the standout month, mute the rest.
(Chart(weather, x="month")
    .bar("rainfall", highlight="May", values=True, sort=True)
    .title("May was the wettest month")
    .labels(x="Month", y="Rainfall (inches)")
    .save(str(IMAGES / "quickstart_bar.png")))

# 3. Relationship between two variables -> scatter.
(Chart(weather, x="low")
    .scatter("high")
    .title("Daily highs track the lows")
    .labels(x="Low (F)", y="High (F)")
    .save(str(IMAGES / "quickstart_scatter.png")))

# 4. Distribution -> histogram (one-call helper).
swing = pd.DataFrame({"month_over_month": weather["high"].diff().fillna(0)})
(hist(swing, "month_over_month", bins=6)
    .title("Month-over-month change in high temp")
    .labels(x="Change (F)", y="Months")
    .save(str(IMAGES / "quickstart_hist.png")))

print("Wrote charts to", IMAGES)
