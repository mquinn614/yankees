# They're Due — New York Yankees

A New York Times–style scrollytelling feature making the data-driven case that
the Yankees are **overdue** for a championship: 27 World Series titles (most in
the sport), but none since 2009 — the longest wait since the late-'90s dynasty.

Built in the same house style as the *ferrari* ("The Long Wait") and *knicks*
scrollytelling repos: a single `index.html` with scroll-driven sections, a
`data/*.json` source of truth, a `scripts/` Python updater, and an `assets/`
folder of duotone-treated photos.

## Narrative arc

1. **Hero** — "They're Due," with the headline drought number.
2. **The 27 Rings** — the dynasty pedigree (titles by decade).
3. **The 2009 Cliff** — the last title, then the line goes flat.
4. **The Drought Years** — a pinned, scroll-driven chart of every season
   2010–present and where each October ended.
5. **The Near-Misses** — 2017, 2019, 2024: within a win / a swing / an inning.
6. **Why Now** — the anchor (Aaron Judge), payroll, and the open window.
7. **Closer** — the case for No. 28.

## Structure

```
index.html              # the whole page: scroll sections, SVG duotone filters, vis JS
data/yankees.json       # real numbers — the single source of truth
scripts/update_data.py  # regenerates data/yankees.json from researched constants
assets/                 # drop raw photos here (see assets/README.md)
```

## Data

All numbers are real (records, postseason results, titles), researched and
held as constants in `scripts/update_data.py`. To regenerate the JSON:

```bash
python3 scripts/update_data.py
```

`index.html` fetches `data/yankees.json` at runtime and also carries an inline
copy as a `file://` fallback, so it renders even when opened directly without a
server. `update_data.py` keeps the two in sync automatically — it rewrites the
inline `<script id="fallback-data">` block in `index.html` every time it runs.

The updater also pulls the **current-season record** live from the free
[MLB Stats API](https://statsapi.mlb.com) (`statsapi.mlb.com`, no key) and writes
it to `meta.current_season`, which the page shows as a "This season" line in the
*Why Now* section. Everything historical (titles, the drought, near-misses) stays
anchored to the researched constants in `update_data.py`; if the API is
unreachable, the build falls back to constants and never fails.

## Hosting & self-update (mqsandbox.com/yankees)

The site is served from the shared web host at **mqsandbox.com/yankees** (not
GitHub Pages), and keeps itself current via three workflows:

| Workflow | Trigger | Does |
|---|---|---|
| `.github/workflows/update-yankees-data.yml` | weekly cron (Mon 06:00 UTC) + manual | regenerates data (live current-season record), commits to `main` if changed |
| `.github/workflows/deploy.yml` | push to `main` + manual | SFTPs `index.html` + `assets/` + `data/` to the host → `mqsandbox.com/yankees` |
| `.github/workflows/keepalive.yml` | monthly cron | tiny commit so GitHub never auto-pauses the scheduled jobs |

The weekly data commit lands on `main`, which triggers the deploy — so the page
re-publishes itself with no manual step.

**Required repo secrets** (same set as the other mqsandbox.com projects):
`SFTP_HOST`, `SFTP_USERNAME`, `SFTP_PASSWORD`, `SFTP_REMOTE_PATH` (point it at the
host's `yankees` folder), and optionally `SFTP_PORT` (defaults to 22).

## Style

- **Palette:** Yankees navy `#0C2340`, white, restrained warm-gold accent
  `#C4A962` (championship/ring connotation).
- **Photos:** consistent navy→white duotone via inline SVG filters, with a
  navy→gold variant for accent images. See `assets/README.md`.
- **Type:** Playfair Display (display serif) · Source Serif 4 (body) ·
  Inter (labels) · IBM Plex Mono (data), with system fallbacks.
- Smooth scroll, sticky/pinned visualizations, `IntersectionObserver`-driven
  reveals, fully mobile-responsive, and `prefers-reduced-motion` aware.

## Running locally

Any static server works (needed for the `fetch` of the JSON; the page also
falls back to its inline copy if opened via `file://`):

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```
