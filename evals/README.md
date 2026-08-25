# Evaluating Evals Coach

This directory evaluates the quality of the **skill**, not the quality of an AI product produced with it.

The suite contains seven PM-shaped tasks covering creation, critique, production-failure expansion, a guided first run, judge calibration, agent tool expectations, and unsafe ambiguity. Each task should be run twice:

- **Baseline:** the model answers without Evals Coach.
- **Skill:** the same model and prompt answer with Evals Coach available and explicitly invoked.

Alternate condition order and blind the scorer to reduce ordering and confirmation bias. Score outputs with [`rubric.md`](rubric.md).

## Run with Codex CLI

Requirements: Node.js 20+ and an authenticated `codex` CLI.

```bash
node evals/run-codex.mjs --dry-run --model gpt-5.6-sol --effort medium --repetitions 2
node evals/run-codex.mjs --condition both --model gpt-5.6-sol --effort medium --repetitions 2
```

Outputs are written to `.eval-runs/`, which is ignored by git. The runner checks for baseline contamination, uses fresh workspaces, alternates run order, records the model, reasoning effort, CLI version and source commit, and prints progress for every run.

For a blind review, zip only the generated `blind-review` directory:

```bash
RUN_DIR=$(ls -td .eval-runs/* | head -1)
zip -r evals-coach-blind-review.zip "$RUN_DIR/blind-review"
```

Keep `condition-map.json` private until the scorer has fixed all scores and hard-failure judgements. Then reveal the map and calculate the baseline-to-skill delta.

## Current status

An initial blinded GPT-5.6 Sol run is published under [`results/`](results/). It found a strong quality improvement and also exposed excessive output length. The current skill and rubric include a concision fix that has not yet been independently replicated. Treat the published run as exploratory evidence, not a universal performance claim.

Suggested first matrix:

- One strong general model and one smaller/faster model
- Two repetitions per task and condition
- A scorer who did not author the outputs
- Per-criterion scores, hard failures, and qualitative regressions—not just a single mean
