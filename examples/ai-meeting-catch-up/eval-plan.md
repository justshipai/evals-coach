# Worked example: AI Meeting Catch-up

This is what Evals Coach might produce from [`input-prd.md`](input-prd.md). It is intentionally small enough to run before the team invests in a full eval programme.

## 1. Product decision

**Decision:** Can we ship the first version without users being misled about what the meeting actually decided or assigned?

This first eval does not try to prove that every summary is delightful. It protects the trust-critical behaviour first.

## 2. Definition of good

The output must:

- Separate confirmed decisions, proposed ideas, action items, and unresolved questions.
- Ground every reported decision and action in the transcript.
- Preserve uncertainty: missing owners and deadlines stay missing.
- Make the supporting transcript passage available for verification.

The output must not:

- Turn a suggestion, preference, or unresolved debate into a decision.
- Invent an action, owner, deadline, number, or rationale.
- Silently resolve conflicting statements.

## 3. Minimum viable test set

The runnable cases are in [`test-cases.csv`](test-cases.csv). The set covers:

- A normal meeting with an explicit decision and assignment
- A suggestion that is never accepted
- A debate that ends without a decision
- An action with no owner or deadline
- A long transcript with distracting detail
- A follow-up question whose answer is not present

Each case is critical because a false confirmed claim can directly mislead a user. Run each case three times to expose non-deterministic failures.

## 4. Grading plan

### First release: human-grounded rubric

For every claimed decision and action, a reviewer marks:

1. **Supported:** the cited passage entails the claim.
2. **Correct status:** decision, proposal, action, or unresolved question is labelled correctly.
3. **No invented detail:** actor, deadline, number, and rationale are present in the source or explicitly unknown.

Any unsupported confirmed decision or action is a critical failure. A formatting or brevity issue is not allowed to average it away.

### Automation path

- Deterministically check that each decision/action contains a valid reference to the supplied transcript.
- After collecting human labels, calibrate an entailment/status LLM judge on disagreements and a held-out set.
- Keep ambiguous cases in human review until the judge meets the agreed false-pass tolerance.

The first release should not treat an uncalibrated LLM judge as ground truth.

## 5. Release contract

Provisional gate for the curated set, across three runs per case:

- **Hard gate:** zero unsupported confirmed decisions or actions.
- **Hard gate:** zero proposals or unresolved debates reported as confirmed decisions.
- **Hard gate:** zero invented owners, deadlines, or numerical commitments.
- **Coverage gate:** all explicit decisions and actions in the reference notes are represented.

These thresholds are provisional. Revisit them after at least 50 reviewed production interactions and report results by failure category, not only as one average score.

## 6. Engineering handoff

Engineering receives:

- The CSV cases, source transcripts, and reference notes
- A versioned output schema containing `type`, `claim`, `status`, and `source_reference`
- The human rubric above
- A requirement to run each case three times and retain outputs for review
- A report split by unsupported claim, wrong status, invented detail, and omission

The PM owns the behavioural criteria and adjudicates disputed examples. Engineering owns the runner and deterministic checks. PM and engineering jointly calibrate any learned judge.

## 7. Improvement loop

**Now:** Run the six curated cases manually before release.

**Next:** Add failures from dogfood and support feedback as regression cases; calibrate the judge against human labels.

**Later:** Run the suite in CI, sample production traces by slice, and maintain a fast path from a real failure to a new case. Track task success and user trust alongside eval scores to avoid optimising only for the metric.

## Assumptions to confirm

- The product can expose transcript references in its output or UI.
- The transcript is the authoritative source for the first release.
- Precision on confirmed claims matters more than producing a complete but speculative summary.
