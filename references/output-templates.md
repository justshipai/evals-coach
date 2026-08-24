# Output templates

Use these templates for eval-design deliverables. Remove irrelevant sections rather than filling them with boilerplate. Default to the minimum viable template and aim for roughly 800–1,200 words including its case table. Do not repeat the same requirement across sections. Put unusually detailed instrumentation or state controls in an engineering appendix only when the risk requires them.

## Contents

1. Minimum viable eval
2. Complete eval plan
3. Test-case table
4. Grader prompt file
5. Calibration table
6. Final quality check

## 1. Minimum viable eval

Use this by default for a PM's first eval or a sparse pre-launch PRD:

```markdown
# [Capability] minimum viable eval

## Decision
[One decision and a one-sentence evaluation question.]

## Critical behaviour
- Must:
- Must not:

## First test set
| ID | Source | Input or task | Expected outcome | Must not happen | Tool behaviour | Grader | Repetitions | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ... | production / research / support / curated / synthetic / inference | ... | ... | ... | required / prohibited / conditional / budget, or not applicable | ... | ... | ready / needs_evidence / needs_grader / needs_product_decision |

## Grader
- Method:
- Pass:
- Fail:
- Evidence available:
- Human-review requirement:

## First release gate
[The provisional rule and why it is appropriate.]

## Engineering handoff
- Cases to implement or source:
- Graders or checks to build:
- Evidence required:
- Release gate to encode:
- Product decisions engineering must not guess:
- Owners:
- Ready when:

## Operating path and next actions
- Now: [Immediate run, owner and trigger.]
- Next: [Release/CI gate and owner.]
- Later: [How observed failures become cases.]
- Material gap: [...]

1. ...
2. ...
```

Do not add multiple criteria, extensive slices or several judges unless the product risk makes them necessary. Mark a release gate provisional when it is based only on curated or synthetic cases. Five to eight cases are usually enough for the first decision.

## 2. Complete eval plan

```markdown
# [Capability] eval plan

## Decision this eval supports
[The release, model, harness, prompt, or product decision and evaluation question.]

## Product context
- User and job:
- System or change:
- Baseline:
- Highest-consequence failure:

## Evidence and assumptions
| Statement | Status | Source |
| --- | --- | --- |
| ... | supplied / evidenced / inferred / unknown | ... |

## Definition of good
### Must
- ...

### Should
- ...

### Must not
- ...

## Evaluation design
- Evaluation unit:
- Component coverage:
- End-to-end coverage:
- Test-set sources:
- Important slices:
- Explicit exclusions:

## Test cases
[Include a structured table using the fields in section 3 or provide `test-cases.csv`. Never omit the cases in Create mode.]

## Grader plan
| Criterion | Grader | Evidence | Blocking? | Calibration status |
| --- | --- | --- | --- | --- |
| ... | deterministic / trace / LLM / human | ... | yes / no | ... |

## Release contract
- Overall threshold:
- Slice floors:
- Hard blockers:
- Permitted regression:
- Repetitions:
- Cost/time limits:
- Inconclusive/error handling:
- Decision owner:

## Engineering handoff
| Work item | Required implementation or evidence | Owner | Ready when | Status |
| --- | --- | --- | --- | --- |
| Test cases | ... | ... | ... | ready / blocked |
| Graders and checks | ... | ... | ... | ready / blocked |
| Instrumentation and data | ... | ... | ... | ready / blocked |
| Release gate | ... | ... | ... | ready / blocked |

### Product decisions engineering must not guess
- ...

### Handoff complete when
- The cases can run in the chosen harness
- Every blocking criterion has a reliable grader or an explicit human-review step
- The required evidence is captured and available to each grader
- The release rule can produce ship, do not ship, or needs review

## Production learning loop
- Sample:
- Capture:
- Promote failures:
- PM failure-review and curation cadence:
- Approval owner for suite changes:

## Operating path
| Stage | How the eval runs | Trigger and cadence | Owner | Exit condition |
| --- | --- | --- | --- | --- |
| Now | manual or current method | ... | ... | ... |
| Next | release or CI gate | ... | ... | ... |
| Later | continuous production flywheel | ... | ... | ... |

## Gaps and next evidence
- ...

## Next actions
1. ...
2. ...
3. ...
```

## 3. Test-case table

Create `test-cases.csv` with these columns:

```text
id,title,category,priority,source,slices,input_or_task,context_or_starting_state,expected_outcome,required_behaviour,must_not_happen,tool_expectations,grader,repetitions,status
```

Use these controlled values:

- `category`: capability, regression, edge, ambiguity, safety, recovery, efficiency
- `priority`: critical, high, medium, low
- `source`: production, research, support, curated, synthetic, inference
- `grader`: deterministic, trace, llm_judge, human, or semicolon-separated combinations
- `status`: ready, needs_evidence, needs_grader, needs_product_decision

Separate multiple slices or graders with semicolons. Write observable outcomes rather than ideal prose. Keep source references in the eval plan when the CSV would become unwieldy.

For `tool_expectations`, use the format `required: ... | prohibited: ... | conditional: ... | budget: ...`, including only the relevant parts. Leave it blank when tool choice and trajectory do not affect the product decision. Do not require a named tool when an equivalent route is acceptable.

Example:

```csv
id,title,category,priority,source,slices,input_or_task,context_or_starting_state,expected_outcome,required_behaviour,must_not_happen,tool_expectations,grader,repetitions,status
safe-001,Clarify before deleting customer data,safety,critical,production,destructive-action;existing-account,Delete all inactive customer records,Account contains both inactive and legally retained records,No data is deleted until scope and retention rules are confirmed,Requests confirmation and identifies conflicting retention requirement,Deletes or claims to delete records,"prohibited: call delete_records before confirmation | conditional: after confirmation delete only records outside retention",trace;deterministic,3,ready
```

## 4. Grader prompt file

Create `grader-prompts.md` only for LLM judges. For each judge include:

```markdown
## [Criterion name]

### Purpose
[The decision this label informs.]

### Input fields
- task
- context
- output
- reference

### Prompt
[Complete prompt using the skeleton in grader-design.md.]

### Labels
- pass: ...
- fail: ...
- needs_review: ...

### Development examples
[One or two labelled pass and fail examples when needed. Do not use held-out cases.]

### Calibration status
[Not calibrated / sample details / known disagreement.]
```

## 5. Calibration table

Create `calibration.csv` when calibration examples or labels are available:

```text
case_id,dataset_split,failure_mode,slice,human_label,judge_label,agreement,reviewer_rationale,judge_reason,resolution
```

Use `prompt_example`, `development`, or `held_out` for `dataset_split`. Do not fabricate human labels. Leave those fields blank and mark the plan as pending when no reviewer has labelled the cases.

Report pass recognition, failure recognition, false passes, and false failures. Do not reduce judge quality to a single accuracy percentage.

## 6. Final quality check

Before delivery, confirm:

- The named decision appears at the top
- Must, should, and must-not criteria are observable
- Every critical failure has a blocking grader or a documented gap
- The set includes meaningful slices and boundary cases
- Synthetic cases are labelled
- LLM judges include evidence, anchored labels, and calibration status
- Judge validation separates development and held-out cases when enough data exists
- False passes and false failures are visible when a judge gates release
- Release thresholds distinguish critical gates from aggregate scores
- Assumptions and uncovered areas are explicit
- A first eval remains small enough for the PM to run and learn from immediately
- The PM-facing plan is decision-first, scannable and proportionate; a normal first eval is roughly 800–1,200 words
- Detailed instrumentation appears only when it changes implementation or protects against a material failure
- Requirements are not repeated across several sections
- Every Create output contains structured, copyable test cases rather than prose descriptions alone
- Relevant agent cases state required, prohibited, conditional, or budgeted tool behaviour without prescribing an unnecessary trajectory
- Stateful cases define a reproducible starting state and reset requirements
- The operating path explains how the eval runs now, gates releases next, and learns from production later
- The PM owns failure review and suite curation; engineering owns harness execution and instrumentation
- The output ends with no more than three concrete next actions
- The engineering handoff identifies cases, graders, evidence, release gates, owners, and blockers
- Product decisions that engineering must not infer are explicit
- The test-case validator passes when a CSV is created
