#!/usr/bin/env python3
"""Validate Evals Coach test-case CSV files using only the standard library."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


REQUIRED_COLUMNS = {
    "id",
    "title",
    "category",
    "priority",
    "source",
    "slices",
    "input_or_task",
    "context_or_starting_state",
    "expected_outcome",
    "required_behaviour",
    "must_not_happen",
    "tool_expectations",
    "grader",
    "repetitions",
    "status",
}

ALLOWED = {
    "category": {"capability", "regression", "edge", "ambiguity", "safety", "recovery", "efficiency"},
    "priority": {"critical", "high", "medium", "low"},
    "source": {"production", "research", "support", "curated", "synthetic", "inference"},
    "grader": {"deterministic", "trace", "llm_judge", "human"},
    "status": {"ready", "needs_evidence", "needs_grader", "needs_product_decision"},
}


def split_values(value: str) -> set[str]:
    return {item.strip() for item in value.split(";") if item.strip()}


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        handle = path.open(newline="", encoding="utf-8-sig")
    except OSError as exc:
        return [f"Cannot read {path}: {exc}"], warnings

    with handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            return [f"Missing required columns: {', '.join(missing)}"], warnings
        rows = list(reader)

    if not rows:
        return ["The CSV contains no test cases."], warnings

    seen_ids: set[str] = set()
    category_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    critical_count = 0

    for number, row in enumerate(rows, start=2):
        prefix = f"Row {number}"
        case_id = row["id"].strip()
        if not case_id:
            errors.append(f"{prefix}: id is empty.")
        elif case_id in seen_ids:
            errors.append(f"{prefix}: duplicate id '{case_id}'.")
        else:
            seen_ids.add(case_id)

        for field in ("title", "input_or_task", "expected_outcome", "required_behaviour"):
            if not row[field].strip():
                errors.append(f"{prefix}: {field} is empty.")

        for field in ("category", "priority", "source", "status"):
            value = row[field].strip()
            if value not in ALLOWED[field]:
                errors.append(f"{prefix}: invalid {field} '{value}'.")

        graders = split_values(row["grader"])
        unknown_graders = graders - ALLOWED["grader"]
        if unknown_graders:
            errors.append(f"{prefix}: invalid grader(s): {', '.join(sorted(unknown_graders))}.")
        if row["status"].strip() == "ready" and not graders:
            errors.append(f"{prefix}: a ready case must name at least one grader.")

        try:
            repetitions = int(row["repetitions"].strip())
            if repetitions < 1:
                raise ValueError
        except ValueError:
            errors.append(f"{prefix}: repetitions must be a positive integer.")

        priority = row["priority"].strip()
        if priority == "critical":
            critical_count += 1
            if not row["must_not_happen"].strip():
                warnings.append(f"{prefix}: critical case has no prohibited behaviour.")

        category_counts[row["category"].strip()] += 1
        source_counts[row["source"].strip()] += 1

    if len(category_counts) < 2:
        warnings.append("The set contains fewer than two scenario categories; check coverage.")
    if critical_count == 0:
        warnings.append("No critical cases are present; confirm that this is intentional.")
    if source_counts and set(source_counts) <= {"synthetic", "inference"}:
        warnings.append("Every case is synthetic or inferred; do not treat this set as representative without review.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Evals Coach test-cases.csv file.")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    errors, warnings = validate(args.csv_path)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Validation passed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
