# Changelog

Notable changes to Evals Coach. Dates are release dates.

Updating the plugin does not refresh a wizard page you have already published.
An Evals Coach page is a snapshot taken when it was published, so to pick up the
changes below, update the plugin and then ask Evals Coach for a new page.

```
/plugin update evals-coach@justshipai
```

## 0.2.0 (2026-09-04)

The wizard gained a way to build an eval up from real outputs, rather than only
down from a description. The handoff files also changed shape.

### Added

- **Review real outputs and distil them into criteria.** If you paste outputs
  from a live feature, step 3 now lets you read them one at a time and note what
  is off. Those notes become named failure modes, and the criteria derived from
  them carry a reference back to the outputs they came from.
- **The failure taxonomy is its own artifact**, so the failure modes you found
  travel with the eval instead of disappearing into the criteria list.
- **Prevalence with an honest confidence range.** A failure seen in 5 of 12
  outputs is reported as 42% with the range a sample that size actually supports,
  rather than as a number that sounds more certain than it is.
- **A saturation signal**, showing how many outputs you have reviewed since the
  last new failure mode appeared.
- **A grader decision procedure.** Choosing a grader was previously guided by
  "pick the cheapest that works", which told a PM nothing. It is now four
  questions about what the grader has to see and decide.
- **Guidance and worked examples on the release gate**, which was previously a
  set of empty boxes with no indication of what belonged in them.

### Changed

- **`test-cases.csv` now matches the schema in `scripts/validate_test_cases.py`.**
  The export previously shared only three column names with the repo's own
  validator, so a finished eval could not be checked against it. If you have
  tooling that reads the old columns, it will need updating. Fields the wizard
  does not collect are derived rather than invented: `priority` comes from the
  case category, `source` is always `curated` because these cases are chosen
  rather than sampled from traffic, and `status` reports `needs_grader` when
  step 5 was never confirmed.
- **Graders are named the same way everywhere.** Exports now say `deterministic`,
  `trace`, `llm_judge` and `human`, matching the skill and the validator. The
  wizard's own labels stay in plain English.
- **Test set size is 5 to 8 cases**, matching `SKILL.md`. The drafting prompt
  previously asked for 8 while the guidance said 5 to 10.
- Branded as Evals Coach throughout, and the "workbench" jargon is gone from
  anything a user reads.

### Fixed

- Step 1 no longer claims it is the only writing you do, and step 7 describes
  what you leave with rather than a handoff.

## 0.1.0 (2026-09-02)

First public alpha. Seven-step wizard published as a private page, with an eval
plan, `test-cases.csv`, judge prompts and a calibration guide as its output.
