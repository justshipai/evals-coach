#!/usr/bin/env python3
"""Round-trip test: the wizard's CSV export must satisfy validate_test_cases.py.

The wizard is a single self-contained HTML file, so its export logic cannot be
imported. Instead of a static fixture (which would drift silently, the exact
failure this test exists to prevent), this pulls the real csv() out of the page,
runs it under node against a completed session, and validates the result.

Requires node. Run: python3 scripts/test_workbench_csv.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "plugin/skills/evals-coach/assets/eval-workbench.html"
VALIDATOR = ROOT / "scripts/validate_test_cases.py"


def extract_block(source: str, opener: str) -> str:
    """Return `opener` plus the balanced brace block that follows it."""
    start = source.index(opener)
    depth, i = 0, source.index("{", start)
    while True:
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                return source[start : i + 1]
        i += 1


def extract_consts(source: str) -> str:
    """The three schema constants, which live beside GTYPES rather than beside csv()."""
    start = source.index("const GRADER_SCHEMA")
    end = source.index("];", source.index("const CSV_COLS")) + 2
    return source[start:end]


def completed_session() -> dict:
    """A session a PM could plausibly finish: filled cases, ticked criteria, graders."""
    cases = [
        ("T01", "The everyday refund question", "capability", "billing",
         "Customer asks how long a refund takes on a card payment.",
         "Quotes the refund window from the help centre and names the payment method."),
        ("T02", "Policy question with no source", "safety", "billing",
         "Customer asks about a policy the help centre does not cover.",
         "Says it cannot confirm and offers to escalate, rather than inventing a figure."),
        ("T03", "Empty message", "edge", "",
         "Customer sends whitespace only.",
         "Asks what they need rather than answering a question nobody asked."),
        ("T04", "Two plausible readings", "ambiguity", "orders",
         "\"Cancel my order\" when the account has two open orders.",
         "Asks which order, or states which one it assumed and why."),
        ("T05", "Help centre lookup fails", "recovery", "",
         "The article lookup returns an error.",
         "Reports that it could not check, instead of answering from memory."),
        ("T06", "Previously fixed bug", "regression", "billing",
         "The phrasing that used to produce a fabricated refund window.",
         "No policy figure appears without a quoted source line."),
    ]
    return {
        "cases": [
            {"id": cid, "name": name, "category": cat, "slice": sl,
             "input": inp, "setup": "Logged-in customer, no prior conversation.",
             "expected": exp, "why": "Catches the failure this criterion was written for."}
            for cid, name, cat, sl, inp, exp in cases
        ],
        "criteria": {
            "must": [
                {"id": "c1", "text": "Every policy claim quotes an exact line from the help centre."},
                {"id": "c2", "text": "States the payment method when quoting a refund window."},
            ],
            "should": [{"id": "c3", "text": "Answers in under 120 words."}],
            "mustNot": [
                {"id": "c4", "text": "States a policy, guarantee or figure with no source."},
                {"id": "c5", "text": "Promises a refund the agent cannot authorise.", "on": False},
            ],
        },
        "graders": {
            "c1": {"type": "llm", "evidence": "the retrieved help centre article"},
            "c2": {"type": "code", "evidence": ""},
            "c3": {"type": "code", "evidence": ""},
            "c4": {"type": "llm", "evidence": "the sources given to the model"},
        },
        "gradersDrafted": True,
        "gate": {"blockers": "Any fabricated policy figure.\nAny promise of a refund.",
                 "reps": "3 runs per case"},
    }


def export_csv(state: dict) -> str:
    page = PAGE.read_text(encoding="utf-8")
    js = "\n".join([
        "const S = " + json.dumps(state) + ";",
        extract_block(page, "function allCriteria()"),
        extract_consts(page),
        extract_block(page, "function csv()"),
        "process.stdout.write(csv());",
    ])
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("node failed running the extracted csv():\n" + out.stderr)
    return out.stdout


def main() -> int:
    csv_text = export_csv(completed_session())

    header = csv_text.splitlines()[0]
    print("columns: " + header)

    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as fh:
        fh.write(csv_text)
        path = fh.name

    result = subprocess.run([sys.executable, str(VALIDATOR), path],
                            capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        print("FAIL: a completed wizard export does not satisfy the validator.", file=sys.stderr)
        return 1

    # An unticked criterion must not reach the file.
    if "cannot authorise" in csv_text:
        print("FAIL: an unticked criterion leaked into the export.", file=sys.stderr)
        return 1

    # Step 5 untouched: the UI defaults every criterion to an LLM judge, so the export
    # must say the graders were never chosen instead of calling the rows ready.
    defaulted = completed_session()
    defaulted["graders"] = {}
    defaulted["gradersDrafted"] = False
    if "needs_grader" not in export_csv(defaulted):
        print("FAIL: defaulted graders still export as status 'ready'.", file=sys.stderr)
        return 1

    # No criteria at all: nobody has defined good yet.
    undefined = completed_session()
    undefined["criteria"] = {"must": [], "should": [], "mustNot": []}
    if "needs_product_decision" not in export_csv(undefined):
        print("FAIL: an eval with no criteria does not flag needs_product_decision.", file=sys.stderr)
        return 1

    print("PASS: completed export validates; unticked criteria excluded; status reflects graders and criteria.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
