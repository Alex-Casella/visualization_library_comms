"""Quickstart example for simple_eda.

Runs the full fluent API against a small sales dataset and writes rendered
charts to ``examples/images/``. Run it from the repo root:

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

# 1. Layered chart: cost as bars, revenue as a line, on one axes.
(Chart(sales, x="month")
    .bar("cost")
    .line("revenue")
    .title("First-half performance")
    .labels(x="Month", y="USD (thousands)")
    .save(str(IMAGES / "quickstart_combo.png")))

# 2. Scatter to eyeball the cost/revenue relationship.
(Chart(sales, x="cost")
    .scatter("revenue")
    .title("Revenue vs. cost")
    .labels(x="Cost", y="Revenue")
    .save(str(IMAGES / "quickstart_scatter.png")))

# 3. One-call helper for a distribution of month-over-month growth.
growth = pd.DataFrame({"growth_pct": sales["revenue"].pct_change().fillna(0) * 100})
(hist(growth, "growth_pct", bins=6)
    .title("Month-over-month revenue growth")
    .labels(x="Growth (%)", y="Months")
    .save(str(IMAGES / "quickstart_hist.png")))

print("Wrote charts to", IMAGES)
