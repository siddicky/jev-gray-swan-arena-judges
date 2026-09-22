# Release decisions

Recorded 2026-09-22. These lock the v1 public-release scope; change by
editing this file with a new dated entry.

## 1. Package name

- Repo: `siddicky/jev-gray-swan-arena-judges`
- PyPI: `jev-gray-swan-arena-judges`
- Import: `jev_gray_swan_arena_judges`
- CLI: `jev-gray-swan-arena-judges`

## 2. Public / private boundary (never ships)

The following stay in the private engagement repo and must never be
committed here: real Arena conversation transcripts or breaks, credited or
not; per-scenario criteria text from the challenge graph; playbook content;
scraper code or scrape output; scoreboards; calibration-set rows.

## 3. Calibration numbers embargo ruling

No aggregate calibration figures may be published until the Hazard Hunt
Q3 embargo lifts on 2026-10-11: no platform-graded conversation counts and
no precision or recall figures. Until that date the README carries an
explicit placeholder with the date instead of a summary. The gate defaults
shipped in code (0.8 submit threshold, 0.5 review boundary) are method, not
calibration results, and stay published. This ruling itself names no
embargoed figures.

## 4. Rename (2026-09-22)

Renamed from `arena-judges` to `jev-gray-swan-arena-judges` across the
GitHub repo slug, the PyPI project name, the import package
(`jev_gray_swan_arena_judges`), and the CLI (`jev-gray-swan-arena-judges`).
Earlier entries above originally read `arena-judges` where they now read
the new name.
