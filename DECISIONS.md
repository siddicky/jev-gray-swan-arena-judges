# Release decisions

Recorded 2026-09-22. These lock the v1 public-release scope; change by
editing this file with a new dated entry.

## 1. Package name

- Repo: `siddicky/arena-judges`
- PyPI: `arena-judges`
- Import: `arena_judges`
- CLI: `arena-judges`

## 2. Public / private boundary (never ships)

The following stay in the private engagement repo and must never be
committed here: real Arena conversation transcripts or breaks, credited or
not; per-scenario criteria text from the challenge graph; playbook content;
scraper code or scrape output; scoreboards; calibration-set rows. Only the
aggregate calibration summary (story 3) may be published.

## 3. Calibration numbers embargo ruling

The aggregate calibration summary (aggregate figures withheld until the embargo lifts) is embargoed until the Hazard
Hunt Q3 embargo lifts on 2026-10-11. Until then the README carries an
explicit placeholder with that date instead of the numbers.
