# Evaluating Evals Coach

This directory evaluates the quality of the **skill**, not the quality of an AI product produced with it.

The suite contains six PM-shaped tasks covering creation, critique, production-failure expansion, judge calibration, agent tool expectations, and unsafe ambiguity. Each task should be run twice:

- **Baseline:** the model answers without Evals Coach.
- **Skill:** the same model and prompt answer with Evals Coach available and explicitly invoked.

Alternate condition order and blind the scorer to reduce ordering and confirmation bias. Score outputs with [`rubric.md`](rubric.md).

## Run with Codex CLI

Requirements: Node.js 20+ and an authenticated `codex` CLI.

```bash
node evals/run-codex.mjs --dry-run
node evals/run-codex.mjs --condition both
```

Outputs are written to `.eval-runs/`, which is ignored by git. The runner checks for baseline contamination, uses fresh workspaces, alternates run order, and records final answers and traces.

## Current status

The cases and rubric have been reviewed for coverage, but no cross-model scores are published yet. Do not cite a performance improvement until blinded runs have been completed and inspected. Publishing a weak or null result is preferable to turning an eval into marketing theatre.

Suggested first matrix:

- One strong general model and one smaller/faster model
- Two repetitions per task and condition
- A scorer who did not author the outputs
- Per-criterion scores, hard failures, and qualitative regressions—not just a single mean
