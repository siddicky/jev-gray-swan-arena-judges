# arena-judges

Off-platform TypeSafe judges for Gray Swan Arena work. This package judges a
saved conversation with one TypeSafe System One request per conversation and
prints an energy-gated verdict: `SUBMIT`, `REVIEW`, or `DO_NOT_SUBMIT`.

ADVISORY only. Nothing here submits anything; manual submission in the Arena
UI is a competition rule.

## Install

Requires Python 3.11 or newer and `uv`.

```bash
git clone https://github.com/siddicky/arena-judges.git
cd arena-judges
uv sync --group dev
```

The runtime dependency is `typesafe-sdk`. It is required, not optional.

## 5-minute quickstart

1. Export a TypeSafe API key:

```bash
export TYPESAFE_API_KEY="your-key-here"
```

2. Judge the committed synthetic transcript:

```bash
uv run arena-judges evaluate examples/synthetic-transcript.json --json
```

3. Run the offline test suite, including the mocked synthetic-transcript
   fixture check:

```bash
uv run pytest
```

The synthetic transcript embeds its own scenario, so no challenge-graph file
is needed for the demo. For your own transcripts, either embed a `scenario`
object or pass `--challenge GRAPH.json --behavior SLUG`.

## Environment and API reference

| Setting | Default | Meaning |
| --- | --- | --- |
| `TYPESAFE_API_KEY` | required | TypeSafe API key consumed by `build_client()` |
| `--model MODEL` | `jev-latest` | TypeSafe System One model |
| `--break-probability P` | `0.8` | Break-Noul threshold for `SUBMIT` |
| `--max-chars N` | `48000` | Transcript truncation budget, head plus tail |
| `--timeout SECONDS` | `120.0` | TypeSafe request timeout |
| `--json` | off | Emit the full evaluation as JSON |

Key entry points:

- `arena_judges.judge.judge_conversation(...)`
- `arena_judges.judge.decide(...)`
- `arena_judges.judge.question_specs(...)`
- `arena-judges evaluate TRANSCRIPT [--challenge GRAPH.json] [--behavior SLUG] [--json]`

Without `TYPESAFE_API_KEY`, `evaluate` exits `2` and names the missing key;
it never prints a traceback for configuration errors.

## Method

Each scenario defines success criteria. The judge materializes one Score
question per criterion plus one overall-break Noul and sends them together
in a single TypeSafe request over the same transcript.

Question IDs are code-owned (`c0`, `c1`, ...): criterion identity lives in
the question instructions, so answers key back by position and never by
name matching.

The energy gate works as follows:

- `SUBMIT`: every criterion met and break Noul at or above the threshold.
- `DO_NOT_SUBMIT`: criteria unmet and break Noul clearly low.
- `REVIEW`: everything else, including signal disagreement and borderline
  break probability.

A possible break is routed to `REVIEW`, never silently discarded.

## Calibration

Aggregate calibration numbers are embargoed until the Hazard Hunt Q3 embargo
lifts on 2026-10-11. This section will then summarize the public gate
behavior. Until that date, do not publish platform-graded conversation
counts, precision/recall figures, or per-scenario criteria.

## Manual submission and scope

- This is a judging package only: scoring, verdicts, and worked examples.
- It contains no scraper, no candidate generator, no playbook, and no
  submission automation.
- Verdicts guide when judgement energy is worth spending. A break submitted
  for judgement costs energy; only `SUBMIT` verdicts are worth it.
- Manual submission in the Arena UI is a competition rule.

## Relationship to other repos

- Engagement operations stay in the private `ai_red_teaming` repository.
- The general red-team framework lives in `siddicky/redteam`:
  <https://github.com/siddicky/redteam>
- This repository is judges only and does not duplicate that framework demo.

## Pre-share safety gate

Run this before anything in this repository leaves the machine:

```bash
uv run pytest
```

The suite includes credential-shaped-string scanning, a no-submission-path
check, and an engagement-evidence-marker check over shipped paths.

## License

MIT. See `LICENSE`.
