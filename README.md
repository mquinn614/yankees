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
server. After editing the data, re-run the script **and** keep that inline
`<script id="fallback-data">` block in `index.html` in sync (the script prints
a reminder; the inline block is just a verbatim copy of the JSON).

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
