"""Render sample charts with pandaviz to verify the library end to end."""

import pandas as pd

from pandaviz import Chart, hist

sales = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "revenue": [120, 135, 128, 160, 172, 190],
    "cost": [90, 95, 100, 110, 118, 125],
})

# Chained, layered chart: bars for cost, a line for revenue.
(Chart(sales, x="month")
    .bar("cost")
    .line("revenue")
    .title("First-half performance")
    .labels(x="Month", y="USD (thousands)")
    .save("chart_combo.png"))

# Scatter with a fluent call.
(Chart(sales, x="cost")
    .scatter("revenue")
    .title("Revenue vs. cost")
    .labels(x="Cost", y="Revenue")
    .save("chart_scatter.png"))

# One-call convenience helper for a distribution.
returns = pd.DataFrame({"daily_return": (sales["revenue"].pct_change()
                                         .fillna(0) * 100)})
hist(returns, "daily_return", bins=6).title("Return distribution") \
    .save("chart_hist.png")

print("Wrote chart_combo.png, chart_scatter.png, chart_hist.png")
