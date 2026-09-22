"""Pre-share safety gate: credentials, submission automation, evidence markers.

Run with ``uv run pytest`` before anything in this repo leaves the machine.
Every scan below skips this file by name: the forbidden patterns appear here
as the very literals being searched for, which is the standard self-match
exception.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).name

# Secret *values*, not environment variable names: reading
# TYPESAFE_API_KEY via os.environ is the documented configuration path.
CREDENTIAL_PATTERNS = (
    re.compile(r"""(?i)\b(api[_-]?key|secret|token)\b\s*[:=]\s*['"][^'"]{4,}['"]"""),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-(live|test)-[0-9A-Za-z]{8,}\b"),
    re.compile(r"xox[baprs]-[0-9A-Za-z-]{8,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"""(?i)\b(password|passwd|pwd)\b\s*[:=]\s*['"][^'"]+['"]"""),
)

# Nothing in this repo automates Arena interaction.
SUBMISSION_PATTERNS = (
    re.compile(r"(?i)submit.{0,20}judgement.{0,20}(post|request|fetch|axios|curl)"),
    re.compile(r"(?i)(post|request|fetch).{0,20}submit.{0,20}judgement"),
    re.compile(r"(?i)arena.{0,20}login|login.{0,20}arena"),
    re.compile(r"grayswan-scraper|gs-submissions|arena-scrape"),
)

# Engagement-evidence markers: real scrape output, scoreboards, challenge
# internals. Plain-English policy discussion in DECISIONS.md/README.md may
# name these categories; shipped code, fixtures, and tests must not carry
# the markers themselves.
EVIDENCE_PATTERNS = (
    re.compile(r"gs-scrape"),
    re.compile(r"panels-API|panels_api"),
    re.compile(r"HAZARD_HUNT"),
    re.compile(r"scoreboard"),
    re.compile(r"calibration-set|calibration_set"),
)
EVIDENCE_SCOPES = ("arena_judges", "examples", "tests")


def _repo_files():
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file() or path.name == SELF:
            continue
        parts = set(path.relative_to(REPO_ROOT).parts)
        if parts & {".git", ".venv", "__pycache__", ".egg-info"}:
            continue
        if path.suffix == ".lock":
            continue
        if path.name.endswith(".egg-info"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        yield path, text


def _scoped_files(scope: str):
    scope_root = REPO_ROOT / scope
    for path in sorted(scope_root.rglob("*")):
        if not path.is_file() or path.name == SELF:
            continue
        if "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        yield path, text


def test_no_credential_shaped_strings():
    hits = []
    for path, text in _repo_files():
        for pattern in CREDENTIAL_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                # os.environ reads name the variable without holding a value.
                if "os.environ" in text.splitlines()[line - 1]:
                    continue
                hits.append(f"{path.relative_to(REPO_ROOT)}:{line}")
    assert hits == [], f"credential-shaped strings found: {hits}"


def test_no_automated_submission_paths():
    hits = []
    for path, text in _repo_files():
        if path.suffix == ".lock":
            continue
        for pattern in SUBMISSION_PATTERNS:
            if pattern.search(text):
                hits.append(f"{path.relative_to(REPO_ROOT)}:{pattern.pattern}")
    assert hits == [], f"submission-automation markers found: {hits}"


def test_no_engagement_evidence_markers_in_shipped_paths():
    hits = []
    for scope in EVIDENCE_SCOPES:
        for path, text in _scoped_files(scope):
            for pattern in EVIDENCE_PATTERNS:
                if pattern.search(text):
                    hits.append(f"{path.relative_to(REPO_ROOT)}:{pattern.pattern}")
    assert hits == [], f"engagement-evidence markers found: {hits}"
