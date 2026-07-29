"""Quickstart example for simple_eda.

Demonstrates picking the right chart for the job and using a single accent
color to highlight the point worth noticing. Renders to ``examples/images/``.

    pip install -e .
    python examples/quickstart.py
"""

from pathlib import Path

import pandas as pd

from simple_eda import Chart, hist

IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)

sales = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "revenue": [120, 135, 128, 160, 172, 190],
    "cost": [90, 95, 100, 110, 118, 125],
})

# 1. Trend over time -> line. Two series; highlight the one that matters.
(Chart(sales, x="month")
    .line(["revenue", "cost"], highlight="revenue")
    .title("Revenue is pulling away from cost")
    .labels(x="Month", y="USD (thousands)")
    .save(str(IMAGES / "quickstart_line.png")))

# 2. Compare groups -> bar. Accent the standout month, mute the rest.
(Chart(sales, x="month")
    .bar("revenue", highlight="Jun")
    .title("June was the strongest month")
    .labels(x="Month", y="Revenue (thousands)")
    .save(str(IMAGES / "quickstart_bar.png")))

# 3. Relationship between two variables -> scatter.
(Chart(sales, x="cost")
    .scatter("revenue")
    .title("Revenue vs. cost")
    .labels(x="Cost (thousands)", y="Revenue (thousands)")
    .save(str(IMAGES / "quickstart_scatter.png")))

# 4. Distribution -> histogram (one-call helper).
growth = pd.DataFrame({"growth_pct": sales["revenue"].pct_change().fillna(0) * 100})
(hist(growth, "growth_pct", bins=6)
    .title("Month-over-month revenue growth")
    .labels(x="Growth (%)", y="Months")
    .save(str(IMAGES / "quickstart_hist.png")))

print("Wrote charts to", IMAGES)
