#!/usr/bin/env python3
"""
update_data.py - regenerate data/yankees.json

Single source of truth for the "They're Due" scrollytelling page.

All figures below are hand-researched, real numbers (regular-season records,
postseason results, World Series titles, payroll context). When a season's
postseason picture or payroll updates, edit the constants here and re-run:

    python3 scripts/update_data.py

The script writes ../data/yankees.json relative to this file. The page
(index.html) fetches that JSON at runtime and also carries an inline copy as a
file:// fallback, so keep the two in sync (this script prints a reminder).

Sources to verify against when updating:
  - Baseball-Reference (team season pages, postseason results)
  - MLB.com postseason brackets
  - Cot's Contracts / Spotrac (payroll & luxury-tax figures)
"""

import json
import os
import re
import urllib.request
from datetime import date

# ---------------------------------------------------------------------------
# Live data: current-season record from the free MLB Stats API (no key).
# This is what makes the page self-updating on a weekly cron: the Yankees'
# in-season W-L (and the as-of date) refresh automatically. Everything else
# (titles, the historical drought, near-misses) stays anchored to the
# researched constants below. If the API is unreachable the build silently
# falls back to constants and never fails.
# ---------------------------------------------------------------------------

MLB_TEAM_ID = 147        # New York Yankees
AL_LEAGUE_ID = 103       # American League


def _target_season(today):
    """The season to report a live record for. During Jan/Feb there is no
    active season, so fall back to the prior year."""
    return today.year - 1 if today.month <= 2 else today.year


def fetch_current_record(year):
    """Return (wins, losses) for the Yankees in `year`, or None on any failure."""
    url = (
        "https://statsapi.mlb.com/api/v1/standings"
        f"?leagueId={AL_LEAGUE_ID}&season={year}&standingsTypes=regularSeason"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "yankees-scrolly/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.load(resp)
        for record in payload.get("records", []):
            for tr in record.get("teamRecords", []):
                if tr.get("team", {}).get("id") == MLB_TEAM_ID:
                    return int(tr["wins"]), int(tr["losses"])
        print(f"  (live fetch: Yankees not found in {year} standings; using constants)")
    except Exception as exc:  # network error, JSON error, schema drift, etc.
        print(f"  (live fetch failed: {exc}; using constants)")
    return None

# ---------------------------------------------------------------------------
# Core franchise numbers
# ---------------------------------------------------------------------------

LAST_TITLE_YEAR = 2009          # 27th World Series
TOTAL_TITLES = 27               # most in MLB
AL_PENNANTS = 40                # most in MLB
CHASING_NUMBER = 28             # the title they're chasing
THROUGH_SEASON = 2025           # last completed season reflected here

# Every Yankees World Series championship (27).
TITLES = [
    1923, 1927, 1928, 1932, 1936, 1937, 1938, 1939, 1941, 1943,
    1947, 1949, 1950, 1951, 1952, 1953, 1956, 1958, 1961, 1962,
    1977, 1978, 1996, 1998, 1999, 2000, 2009,
]

# Titles grouped by decade - for the "dynasty pedigree" bar chart.
TITLES_BY_DECADE = [
    {"decade": "1920s", "count": 3},
    {"decade": "1930s", "count": 5},
    {"decade": "1940s", "count": 4},
    {"decade": "1950s", "count": 6},
    {"decade": "1960s", "count": 2},
    {"decade": "1970s", "count": 2},
    {"decade": "1980s", "count": 0},
    {"decade": "1990s", "count": 3},
    {"decade": "2000s", "count": 2},
    {"decade": "2010s", "count": 0},
    {"decade": "2020s", "count": 0},
]

# Gaps between titles across franchise history. The current wait is the
# longest since the late-'90s Torre dynasty began.
HISTORICAL_DROUGHTS = [
    {"span": "1962–1977", "years": 15, "ongoing": False},
    {"span": "1978–1996", "years": 18, "ongoing": False},
    {"span": "2000–2009", "years": 9, "ongoing": False},
    {"span": "2009–present", "years": THROUGH_SEASON - LAST_TITLE_YEAR, "ongoing": True},
]

# ---------------------------------------------------------------------------
# The drought, season by season (2010 → present). "where it ended each year."
# round: WS | ALCS | ALDS | WCS (Wild Card Series/Game) | DNQ (missed playoffs)
# ---------------------------------------------------------------------------

DROUGHT_YEARS = [
    {"year": 2010, "wins": 95, "losses": 67, "playoffs": True,
     "round": "ALCS", "exit": "Lost ALCS", "opponent": "Texas Rangers", "series": "2–4",
     "note": "Cliff Lee and a young Rangers club end the title defense one round from the pennant."},
    {"year": 2011, "wins": 97, "losses": 65, "playoffs": True,
     "round": "ALDS", "exit": "Lost ALDS", "opponent": "Detroit Tigers", "series": "2–3",
     "note": "Best record in the AL, out in five. Game 5 lost at home."},
    {"year": 2012, "wins": 95, "losses": 67, "playoffs": True,
     "round": "ALCS", "exit": "Lost ALCS", "opponent": "Detroit Tigers", "series": "0–4",
     "note": "Swept. The lineup goes cold; Jeter breaks his ankle in Game 1."},
    {"year": 2013, "wins": 85, "losses": 77, "playoffs": False,
     "round": "DNQ", "exit": "Missed playoffs", "opponent": None, "series": None,
     "note": "Jeter's farewell-year injuries; first October at home since 2008."},
    {"year": 2014, "wins": 84, "losses": 78, "playoffs": False,
     "round": "DNQ", "exit": "Missed playoffs", "opponent": None, "series": None,
     "note": "Jeter's actual farewell. Back-to-back misses for the first time in two decades."},
    {"year": 2015, "wins": 87, "losses": 75, "playoffs": True,
     "round": "WCS", "exit": "Lost Wild Card Game", "opponent": "Houston Astros", "series": "0–1",
     "note": "Shut out by Dallas Keuchel. One game, one night, done."},
    {"year": 2016, "wins": 84, "losses": 78, "playoffs": False,
     "round": "DNQ", "exit": "Missed playoffs", "opponent": None, "series": None,
     "note": "Deadline sell-off. The Judge/Sánchez core debuts in the wreckage."},
    {"year": 2017, "wins": 91, "losses": 71, "playoffs": True,
     "round": "ALCS", "exit": "Lost ALCS", "opponent": "Houston Astros", "series": "3–4",
     "note": "Up 3–2, one win from the pennant, then shut out twice in Houston. The Astros were later found to have stolen signs."},
    {"year": 2018, "wins": 100, "losses": 62, "playoffs": True,
     "round": "ALDS", "exit": "Lost ALDS", "opponent": "Boston Red Sox", "series": "1–3",
     "note": "100 wins, but the 108-win Red Sox roll them and win it all."},
    {"year": 2019, "wins": 103, "losses": 59, "playoffs": True,
     "round": "ALCS", "exit": "Lost ALCS", "opponent": "Houston Astros", "series": "2–4",
     "note": "103 wins. José Altuve's walk-off homer off Chapman ends Game 6, and the season."},
    {"year": 2020, "wins": 33, "losses": 27, "playoffs": True,
     "round": "ALDS", "exit": "Lost ALDS", "opponent": "Tampa Bay Rays", "series": "2–3",
     "note": "The 60-game year. Five-game ALDS lost in the bubble to the division-rival Rays."},
    {"year": 2021, "wins": 92, "losses": 70, "playoffs": True,
     "round": "WCS", "exit": "Lost Wild Card Game", "opponent": "Boston Red Sox", "series": "0–1",
     "note": "One-game playoff at Fenway. Out before the series rounds even begin."},
    {"year": 2022, "wins": 99, "losses": 63, "playoffs": True,
     "round": "ALCS", "exit": "Lost ALCS", "opponent": "Houston Astros", "series": "0–4",
     "note": "Aaron Judge's 62-homer season ends in a four-game sweep by Houston."},
    {"year": 2023, "wins": 82, "losses": 80, "playoffs": False,
     "round": "DNQ", "exit": "Missed playoffs", "opponent": None, "series": None,
     "note": "First losing-adjacent season since 1992: 82–80, no October at all."},
    {"year": 2024, "wins": 94, "losses": 68, "playoffs": True,
     "round": "WS", "exit": "Lost World Series", "opponent": "Los Angeles Dodgers", "series": "1–4",
     "note": "First pennant since 2009, then a Game 5 unraveling hands the Dodgers the title."},
    {"year": 2025, "wins": 94, "losses": 68, "playoffs": True,
     "round": "ALDS", "exit": "Lost ALDS", "opponent": "Toronto Blue Jays", "series": "1–3",
     "note": "Back to October, past Boston in the Wild Card round, then out in the division series."},
]

# ---------------------------------------------------------------------------
# Near-misses - the deepest, most painful runs that ended short.
# ---------------------------------------------------------------------------

NEAR_MISSES = [
    {"year": 2017, "stage": "ALCS Game 7", "opponent": "Houston Astros",
     "how_close": "1 win from the pennant",
     "detail": "Led the series 3–2, then was shut out in Games 6 and 7 in Houston. The Astros later admitted to an illegal sign-stealing scheme that season."},
    {"year": 2019, "stage": "ALCS Game 6", "opponent": "Houston Astros",
     "how_close": "1 swing from Game 7",
     "detail": "José Altuve's two-run walk-off homer off Aroldis Chapman ended the pennant on the spot."},
    {"year": 2024, "stage": "World Series Game 5", "opponent": "Los Angeles Dodgers",
     "how_close": "1 inning from forcing Game 6",
     "detail": "Led 5–0 in the clincher; a five-run fifth, fueled by defensive misplays, turned the title over to Los Angeles."},
]

# Summary counts across the drought (2010–2025), derived from DROUGHT_YEARS.
def _summary(years):
    playoff_years = [y for y in years if y["playoffs"]]
    alcs_or_better = [y for y in years if y["round"] in ("ALCS", "WS")]
    pennants = [y for y in years if y["round"] == "WS"]
    missed = [y for y in years if not y["playoffs"]]
    hundred_win = [y for y in years if y["wins"] >= 100]
    return {
        "seasons": len(years),
        "playoff_appearances": len(playoff_years),
        "missed_playoffs": len(missed),
        "alcs_or_deeper": len(alcs_or_better),
        "pennants": len(pennants),
        "titles": 0,
        "hundred_win_seasons": len(hundred_win),
        "total_regular_season_wins": sum(y["wins"] for y in years),
    }

# ---------------------------------------------------------------------------
# Why now - the contention case (current-era context).
# Keep payroll qualitative + approximate; exact figures shift each winter.
# ---------------------------------------------------------------------------

WHY_NOW = {
    "anchor": {
        "name": "Aaron Judge",
        "role": "Captain · CF/RF",
        "mvps": "2× AL MVP (2022, 2024)",
        "calling_card": "62 HR in 2022, the AL single-season record",
    },
    "payroll": {
        "approx_usd_millions": 300,
        "rank_note": "Among the top of MLB in payroll and luxury-tax spending every year of the drought",
    },
    "window": [
        "A generational hitter in his prime anchoring the lineup as captain.",
        "A top-of-market payroll and a front office that spends to win now.",
        "Twelve playoff trips in sixteen years, and the door has never really closed.",
        "A 2024 pennant proved the roster can reach the final stage; the last step is all that's left.",
    ],
}

# "Due" case - the statistical argument.
DUE_CASE = {
    "avg_years_between_titles_1923_2009": 3.3,   # 27 titles across the 1923–2009 span
    "playoff_rate_drought": None,                # filled below from summary
    "longest_modern_drought_context": "the longest the Yankees have gone without a title since their late-1990s dynasty began",
}


def build():
    summary = _summary(DROUGHT_YEARS)
    DUE_CASE["playoff_rate_drought"] = round(
        summary["playoff_appearances"] / summary["seasons"], 2
    )
    drought_seasons = THROUGH_SEASON - LAST_TITLE_YEAR

    today = date.today()
    season = _target_season(today)
    current_season = None
    live = fetch_current_record(season)
    if live:
        wins, losses = live
        current_season = {
            "year": season,
            "wins": wins,
            "losses": losses,
            "as_of": today.isoformat(),
        }

    return {
        "meta": {
            "team": "New York Yankees",
            "headline": "They're Due",
            "updated": today.isoformat(),
            "through_season": THROUGH_SEASON,
            "last_title_year": LAST_TITLE_YEAR,
            "drought_seasons": drought_seasons,
            "total_titles": TOTAL_TITLES,
            "al_pennants": AL_PENNANTS,
            "chasing_number": CHASING_NUMBER,
            "current_season": current_season,
            "source_note": "Records and postseason results from Baseball-Reference / MLB.com; "
                           "payroll context from public luxury-tax reporting. Current-season "
                           "record is pulled live from the MLB Stats API. Regenerate via "
                           "scripts/update_data.py.",
        },
        "titles": TITLES,
        "titles_by_decade": TITLES_BY_DECADE,
        "historical_droughts": HISTORICAL_DROUGHTS,
        "drought_years": DROUGHT_YEARS,
        "drought_summary": summary,
        "near_misses": NEAR_MISSES,
        "why_now": WHY_NOW,
        "due_case": DUE_CASE,
    }


FALLBACK_OPEN = '<script id="fallback-data" type="application/json">'
FALLBACK_CLOSE = "</script>"


def sync_inline_fallback(index_path, json_text):
    """Rewrite the inline file:// fallback block in index.html so it always
    matches data/yankees.json (keeps the two in sync automatically)."""
    if not os.path.exists(index_path):
        return False
    html = open(index_path, encoding="utf-8").read()
    start = html.find(FALLBACK_OPEN)
    if start == -1:
        return False
    inner = start + len(FALLBACK_OPEN)
    end = html.find(FALLBACK_CLOSE, inner)
    if end == -1:
        return False
    new_html = html[:inner] + "\n" + json_text + "\n" + html[end:]
    if new_html != html:
        open(index_path, "w", encoding="utf-8").write(new_html)
        return True
    return False


def main():
    data = build()
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.normpath(os.path.join(here, "..", "data", "yankees.json"))
    index_path = os.path.normpath(os.path.join(here, "..", "index.html"))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    json_text = json.dumps(data, indent=2, ensure_ascii=False)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(json_text + "\n")
    synced = sync_inline_fallback(index_path, json_text)

    cur = data["meta"]["current_season"]
    print(f"Wrote {out_path}")
    print(f"  {data['meta']['total_titles']} titles · "
          f"{data['meta']['drought_seasons']}-season drought · "
          f"chasing #{data['meta']['chasing_number']}")
    if cur:
        print(f"  live {cur['year']} record: {cur['wins']}-{cur['losses']} "
              f"(as of {cur['as_of']})")
    print(f"  inline fallback in index.html: {'updated' if synced else 'unchanged'}")


if __name__ == "__main__":
    main()
