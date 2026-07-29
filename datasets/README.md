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

---

## `nfl_leader_totals_2020_2024.csv`

A season-agnostic **aggregation** of the file above, built by
[`../examples/nfl_totals.py`](../examples/nfl_totals.py): one row per
`(player, stat)`, summing across the seasons that player led the league.

| Column | Meaning |
| --- | --- |
| `player`, `category`, `stat`, `unit` | as above |
| `total` | sum of the player's values across their league-leading seasons |
| `seasons_led` | how many seasons that total covers |
| `years` | the specific seasons (e.g., `2020;2021;2023`) |
| `teams` | team(s) over those seasons |

### ⚠️ What `total` is — and isn't

`total` is the sum across the seasons a player **led the league**, **not** their
full 2020–2024 output. Because the source has only each season's leader, a
player who led once has a `total` equal to that single season (see `years`/
`seasons_led` to tell them apart). The aggregation only adds signal where a
player led more than once:

- **T.J. Watt — 56.5 sacks** across three leading seasons (2020, 2021, 2023).
- **Davante Adams — 32 receiving TDs** across two (2020 GB, 2022 LV).

To get true multi-year career totals, you'd need every player's per-season
stats (blocked here) — drop them into `nfl_leaders_2020_2024.csv` and re-run
`python examples/nfl_totals.py` to rebuild this file.

---

## `nfl_position_top5_2020_2024.csv`

The **top 5 players at each position** over 2020–2024, by the defining volume
stat: QB (passing yards), RB (rushing yards), WR (receiving yards), Edge
(sacks). Charted by [`../examples/nfl_positions.py`](../examples/nfl_positions.py).

| Column | Meaning |
| --- | --- |
| `position` | QB, RB, WR, Edge |
| `stat`, `unit` | the ranking stat and its unit |
| `rank` | 1 = best at that position over the span |
| `player`, `team` | player and primary team |
| `total` | **approximate** five-season total in that stat |

### ⚠️ These are approximate, unverified estimates

Because PFR can't be scraped here, these five-season totals were **estimated
from model knowledge and rounded** (to signal they aren't exact). The
**ordering** is broadly defensible, but the **numbers are approximate** and some
races are close — verify against PFR before relying on them:

- **RB (Derrick Henry) and Edge (T.J. Watt)** — fairly clear #1s.
- **QB (Mahomes vs. Josh Allen)** and **WR (Jefferson vs. Tyreek Hill)** — close
  at the top; the #1 could flip once verified.
- Totals are also affected by games missed to injury (e.g., Chubb, Diggs), which
  these round-number estimates only roughly capture.
