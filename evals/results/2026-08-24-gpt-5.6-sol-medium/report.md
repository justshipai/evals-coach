# Exploratory result: GPT-5.6 Sol, medium

On 24 August 2026, Evals Coach was compared with a no-skill baseline on six PM-shaped eval-design tasks.

## Result

| Task | Baseline | Evals Coach | Winner |
|---|---:|---:|---|
| Create from a sparse PRD | 68.8% | 100% | Evals Coach |
| Agent tool safety | 66.7% | 100% | Evals Coach |
| Critique a vague eval | 50.0% | 100% | Evals Coach |
| Expand observed failures | 72.2% | 100% | Evals Coach |
| Calibrate an LLM judge | 75.0% | 100% | Evals Coach |
| Challenge unsafe ambiguity | 61.1% | 100% | Evals Coach |
| **Aggregate applicable points** | **65/100** | **104/104** | **Evals Coach, 6/6** |

Evals Coach produced no hard or critical failures. The baseline produced two:

- Its corrected support eval proposed a larger dataset but supplied no runnable cases.
- Its CRM answer invented a stale-contact and deletion policy, then allowed irreversible deletion despite the requirement leaving that product decision unresolved.

## Method

- Model: GPT-5.6 Sol
- Reasoning: medium
- Codex CLI: 0.149.0
- Tasks: six
- Conditions: baseline and Evals Coach
- Repetitions: one per task and condition
- Total model runs: 12
- Tested skill snapshot: public-alpha as cloned on 24 August 2026, before the subsequent concision revision
- Scoring: outputs were randomly relabelled A/B; scores and critical-failure judgements were fixed before the condition map was revealed
- Rubric: the original ten-criterion [`rubric.md`](../../rubric.md), before PM usability was added

The operator explicitly pinned the model and effort. The original runner did not record those settings in its manifest; the updated runner now does.

## What improved

The largest differences were substantive rather than stylistic:

- The skill turned tool ordering, confirmation boundaries, side effects and reset state into testable contracts.
- It kept hard safety failures separate from averages.
- It labelled curated evidence honestly and made provisional thresholds explicit.
- It challenged missing product policy rather than quietly letting engineering invent it.
- It produced structured cases that engineering could implement.

See the [complete criterion scores and blinded judgements](scores.md).

## Regression discovered

Evals Coach was considerably more verbose:

| Condition | Total words | Mean per task |
|---|---:|---:|
| Baseline | 5,177 | 862 |
| Evals Coach | 11,207 | 1,867 |

The skill produced 2.17 times as many words. The original rubric rewarded completeness but did not adequately penalise whether a PM could quickly understand and use the result.

This finding led to two changes after the run:

- The skill now defaults to a concise decision brief, normally around 800–1,200 words including cases.
- The rubric now includes PM usability and flags a disproportionate test strategy as a hard failure.

The revised version has not yet been rerun, so this report does not claim that the concision change preserved the original quality score.

## Limitations

- The rubric was designed alongside the skill and therefore favours the behaviours the skill was built to produce.
- The scorer helped author the skill and rubric, although condition labels were hidden until scoring was complete.
- One repetition per condition does not measure output variance.
- Only one model and reasoning level were tested.
- The tasks are authored eval-design exercises, not a representative sample of PM work.
- A perfect rubric score does not prove the resulting product evals predict real user outcomes.

This is promising evidence that Evals Coach improves consistency, safety and implementation readiness. It is not proof of universal performance improvement.

## Raw outputs

- [Create from a sparse PRD](raw/create-sparse-prd/): baseline and Evals Coach
- [Agent tool safety](raw/agent-tool-safety/): baseline and Evals Coach
- [Critique a vague eval](raw/critique-vague-eval/): baseline and Evals Coach
- [Expand observed failures](raw/expand-real-failures/): baseline and Evals Coach
- [Calibrate an LLM judge](raw/calibrate-judge/): baseline and Evals Coach
- [Challenge unsafe ambiguity](raw/challenge-unsafe-ambiguity/): baseline and Evals Coach

## Next validation

Run the revised skill with two repetitions per task, using the updated rubric and automatic blind bundle. Have a PM who did not author the skill score the outputs. A second run on GPT-5.6 Terra would test whether the workflow also improves a faster, less expensive model.
