# Datasets

## `nfl_2025_leaders_sample.csv`

NFL statistical leaders in a tidy, one-row-per-record schema, ready to chart
with `simple_eda` (see [`../examples/nfl_leaders.py`](../examples/nfl_leaders.py)).

| Column | Meaning |
| --- | --- |
| `category` | Passing, Rushing, Receiving, Defense |
| `stat` | e.g. Passing Yards, Rushing TDs, Sacks, Interceptions |
| `unit` | yards, touchdowns, sacks, interceptions |
| `rank` | 1 = leader in that stat |
| `player` | player name |
| `team` | team abbreviation (real) |
| `value` | the stat total |

> **⚠️ This is illustrative SAMPLE data, not real results.** Player names are
> placeholders (`Passer A`, `Rusher B`, …) and the values are plausible but
> invented. It exists so the charts run out of the box. Do not cite these
> numbers.

### Loading the real 2025 leaders

The source page — <https://www.pro-football-reference.com/years/2025/leaders.htm>
— blocks automated requests (HTTP 403), so it can't be scraped from this
environment. To populate real data, do one of the following, then re-run
`python examples/nfl_leaders.py`:

1. **CSV export (easiest).** On each PFR leaderboard table, use
   *Share & Export → Get table as CSV*, then reshape the rows into the tidy
   schema above and overwrite this file.
2. **Save the page, parse locally.** Open the URL in a browser, save the HTML,
   and parse it without sending the markup through an assistant:

   ```python
   import pandas as pd
   # PFR wraps many tables in HTML comments; flavor="lxml" + this call
   # usually surfaces them. Inspect tables and map into the tidy schema.
   tables = pd.read_html("saved_leaders.html")
   for i, t in enumerate(tables):
       print(i, t.shape, list(t.columns)[:6])
   ```

Keeping the parse local (a file + pandas) means the raw HTML never has to pass
through the assistant's context — see the token note in the top-level README.
