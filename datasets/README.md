# Datasets

## `nfl_leaders_2020_2024.csv`

The NFL **season leader** in each major statistical category, 2020–2024, in a
tidy one-row-per-record schema. Charted and analyzed by
[`../examples/nfl_leaders.py`](../examples/nfl_leaders.py).

| Column | Meaning |
| --- | --- |
| `year` | NFL season (2020–2024) |
| `category` | Passing, Rushing, Receiving, Defense |
| `stat` | Passing Yards, Passing TDs, Rushing Yards, Rushing TDs, Receiving Yards, Receiving TDs, Sacks |
| `unit` | yards, touchdowns, sacks |
| `player` | player who led the league that season |
| `team` | team abbreviation |
| `value` | the league-leading total |

### ⚠️ Provenance — read this

`pro-football-reference.com` **blocks automated access** (HTTP 403), so this
data could **not** be scraped. The values were **compiled from model knowledge
and have not been verified against the source.** Treat them as a starting point
and confirm against PFR before citing. The marquee leaders (e.g., Henry's 2,027
rushing yards in 2020, Watt's 22.5 sacks in 2021, Kupp's 1,947 receiving yards
in 2021) are well documented; the cells below are lower confidence:

- **2020 Sacks** (T.J. Watt, 15.0) — leader/total is approximate.
- **2022–2023 Rushing TDs** (Williams 17; Mostert 18) — approximate.
- **2022–2023 Receiving TDs** (Adams 14; Evans 13) — approximate.
- **Rushing TDs 2024** is intentionally omitted (couldn't verify the leader).
- **2025** is omitted entirely — it's at the model's knowledge cutoff and
  can't be verified.

### Filling in verified data

Overwrite this file with real numbers (same schema) and re-run
`python examples/nfl_leaders.py`. Because PFR blocks scraping here, get the
data via its *Share & Export → Get table as CSV* on each leaderboard, or save
the page and parse it locally with `pandas.read_html(...)` — keeping the parse
local means the raw HTML never passes through an assistant's context (see the
token note in the top-level README).

### Scope note

This file tracks the **rank-1 leader** per stat per season (not the top 5), so
that every value is one I can reasonably stand behind. That's enough to answer
"who stands out in each category?" and "who leads consistently?" — add more
rows in the same schema if you want full top-N depth.
