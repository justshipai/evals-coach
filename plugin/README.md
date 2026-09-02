# Evals Coach (plugin)

The [Evals Coach](https://github.com/justshipai/evals-coach) skill, packaged for Claude
Code and Cowork, plus a guided workbench for PMs.

## Install

```
/plugin marketplace add justshipai/evals-coach
/plugin install evals-coach@justship
```

## What you get

**`evals-coach`** — the skill. Ask for an eval in your own words:

```
Turn this PRD into the smallest eval that can inform a ship decision.
Critique this eval. Tell me what could pass while the product still fails users.
Turn these production failures into regression cases.
Help me calibrate this LLM judge against human labels.
```

**`eval-workbench`** — for people who would rather fill in a form. Ask for "the eval
workbench" and it publishes you a seven-step wizard as a private Artifact: describe your
feature, and it drafts the evaluation question, criteria, test cases, graders, judge
prompts and release gate, each editable, ending in an eval plan, `test-cases.csv` and
judge prompts.

Two things to know about the workbench: drafting runs on the Claude account of whoever
opens the page, and a page that uses Claude cannot take a public "anyone with the link"
URL — you share it with named people. Opened without drafting it becomes a worksheet, with
the same structure, starter suggestions and outputs.

## Contents

- `skills/evals-coach/` — a copy of the canonical skill at the repository root, synced by
  `scripts/sync-plugin.sh`. Edit the root, not this copy.
- `skills/eval-workbench/` — publishes the workbench, and the page itself under `assets/`.
