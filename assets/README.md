# assets/

Drop raw photos here. The page applies a consistent **navy → white duotone**
(SVG `feColorMatrix`/`feComponentTransfer`, defined inline at the top of
`index.html`) so anything you add matches the editorial house style. A
**navy → gold** variant (`.photo.gold`) is used on accent images.

Until a file exists, the page shows a navy gradient placeholder with the
expected filename — so the layout never breaks. As soon as you commit a file
with the matching name, it swaps in automatically (handled by `loadPhotos()`).

## Expected filenames

| File              | Where it appears        | Treatment        | Suggested shot |
|-------------------|-------------------------|------------------|----------------|
| `yanks.webp`    | Full-screen hero        | navy duotone     | Wide Yankee Stadium / crowd / championship celebration. Landscape, ≥2000px wide. |
| `2009.jpg`        | "The 2009 Cliff"        | navy→gold duotone| 2009 World Series celebration / trophy. Portrait (4:5) works best. |
| `judge.jpg`       | "Why Now" anchor card   | navy→gold duotone| Aaron Judge batting / portrait. Landscape (5:4). |
| `closer.jpg`      | Closing section         | navy duotone (darkened) | Stadium at night / empty diamond / iconic façade. Landscape. |

JPGs or PNGs both fine; keep them reasonably optimized. The duotone is applied
in-browser, so commit normal full-color photos — do **not** pre-filter them.

## Changing the treatment

- The two filters live in the hidden `<svg>` near the top of `index.html`
  (`#duotone-navy`, `#duotone-gold`). Edit the `tableValues` to retarget the
  shadow/highlight colors.
- To force a plain grayscale look on a specific image, add the `flat` class to
  its `.photo` container.
