# Examples

Runnable examples for `simple_eda`. Every example script renders its charts to
`examples/images/` so you can see the output without running anything.

**Convention:** every new `.py` example ships with at least one rendered
visualization committed under `images/`.

| Script | Renders |
| --- | --- |
| [`quickstart.py`](quickstart.py) | Picking the right chart per question, with a single accent color used to highlight the key point |
| [`nfl_leaders.py`](nfl_leaders.py) | Analyzes NFL season leaders 2020–24: the standout season per category and the most consistent leaders |

Run any example from the repo root:

```bash
pip install -e .
python examples/quickstart.py
```

## quickstart.py

A line for the trend (revenue accented), a bar chart comparing months (the
standout accented), a scatter for the cost/revenue relationship, and a
histogram for the growth distribution.

![line](images/quickstart_line.png)
![bar](images/quickstart_bar.png)
![scatter](images/quickstart_scatter.png)
![hist](images/quickstart_hist.png)

## nfl_leaders.py

Analyzes the NFL season leaders in
[`../datasets/nfl_leaders_2020_2024.csv`](../datasets/nfl_leaders_2020_2024.csv)
(compiled from model knowledge — verify vs. PFR). For each category it accents
the **standout (highest) season**, and a final chart ranks the **most
consistent** leaders (most category-seasons led). Findings: peaks like Henry's
2,027 rushing yards (2020), Brady's 5,316 passing yards (2021), Kupp's 1,947
receiving yards (2021), and Watt's 22.5 sacks (2021) — with **T.J. Watt** the
most consistent, leading a category in three of the five seasons.

![passing-yards](images/nfl_passing_yards.png)
![passing-tds](images/nfl_passing_tds.png)
![rushing-yards](images/nfl_rushing_yards.png)
![rushing-tds](images/nfl_rushing_tds.png)
![receiving-yards](images/nfl_receiving_yards.png)
![receiving-tds](images/nfl_receiving_tds.png)
![sacks](images/nfl_sacks.png)
![consistency](images/nfl_consistency.png)
