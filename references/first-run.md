# First eval run

Use this reference in **Run** mode to move a PM from a written eval to a completed first scoring cycle. Keep the process lightweight enough to repeat.

## Contents

1. Entry conditions
2. Select the batch
3. Prepare human scoring
4. Reconcile the rubric
5. Trial an automated judge
6. Report and hand off
7. Output templates

## 1. Entry conditions

Confirm:

- The product decision and critical behaviour are explicit
- A rubric or pass/fail criterion exists
- Actual system outputs can be paired with their inputs and relevant evidence
- The candidate or system version is recorded
- Sensitive production data is removed or handled in an approved environment

If the eval itself is weak, repair it before facilitating the run. If outputs are missing, produce a collection plan and blank scorecard rather than inventing them.

## 2. Select the batch

Start with 10–20 actual outputs. A smaller batch is acceptable when evidence is scarce, but label the confidence limit.

Include:

- Common user tasks
- Known or suspected failures
- Boundary and ambiguous examples
- High-consequence cases
- Relevant slices such as task difficulty, user type, context length, tool availability, or locale

Do not use only conspicuous failures. Do not claim the batch represents production traffic unless the sampling method supports that claim. Blind reviewers to candidate identity when comparing systems and practical.

## 3. Prepare human scoring

Give reviewers the input, output, rubric, evidence they are allowed to use, and anchored labels. Do not show another reviewer's score or rationale before independent scoring.

Use at least two reviewers on an overlapping calibration subset where practical. A solo PM can run the first pass, but record that inter-rater agreement was not tested.

For each criterion, capture:

- Label or score
- Observable evidence
- Confidence
- Ambiguity or missing evidence
- Reviewer

Critical failures remain visible and cannot be averaged away.

## 4. Reconcile the rubric

Review disagreements before calculating a headline result. Treat disagreement as a possible rubric or evidence problem, not automatically as reviewer error.

For each disagreement:

1. Identify the exact phrase or evidence that drove each judgement
2. Decide whether the criterion, labels, evidence, or example is ambiguous
3. Revise the rubric only when the intended product behaviour becomes clearer
4. Record the resolution without rewriting the original human labels
5. Re-score affected examples when the rubric materially changes

Separate legitimate subjective variation from product decisions the PM still needs to make.

## 5. Trial an automated judge

Only trial an LLM judge after human labels exist for the same observable criterion.

- Give the judge the rubric and permitted evidence, not the human answer
- Keep prompt-development examples separate from held-out comparisons when the batch allows
- Compare judge labels with adjudicated human labels
- Report false passes and false failures separately
- Inspect whether disagreements cluster by slice or failure type
- Route ambiguous or high-consequence cases to human review

A judge is not better because it is stricter. Recommend automation only when its errors are acceptable for the decision it will gate.

## 6. Report and hand off

Produce:

- Baseline performance by criterion and important slice
- Every critical failure
- Human disagreement rate and unresolved product questions
- Judge agreement, false passes, and false failures when tested
- New regression cases discovered during review
- A provisional ship, do-not-ship, or needs-review decision
- The smallest engineering step needed to repeat the run

The handoff should name the cases and scorecard to import, evidence to capture, checks to automate, human-review path, release rule, owners, and readiness condition.

## 7. Output templates

When creating files, use `first-run-scorecard.csv`:

```text
item_id,case_id,source,slice,input_reference,output_reference,system_version,criterion,human_label,human_evidence,human_confidence,reviewer,judge_label,judge_reason,agreement,adjudicated_label,resolution,status
```

Leave human and judge fields blank until those judgements actually exist. Use `ready_to_score`, `scored`, `needs_adjudication`, or `complete` for `status`.

Use this compact report:

```markdown
# [Capability] first eval run

## Decision and batch
- Decision:
- System version:
- Outputs reviewed:
- Sampling and limitations:

## Result
- Overall:
- Critical failures:
- Important slices:
- Decision: ship / do not ship / needs review

## Human calibration
- Reviewers and overlap:
- Disagreements:
- Rubric changes:
- Unresolved product decisions:

## Judge trial
- Status: not run / development / held out
- Agreement:
- False passes:
- False failures:
- Human-review route:

## Regression cases and engineering handoff
- Cases to add:
- Evidence and checks to implement:
- Release rule:
- Owners:
- Ready when:

## Next actions
1. ...
2. ...
3. ...
```
