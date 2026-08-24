## Recommendation

Do **not** automate the release gate yet.

The judge has 85% agreement (34/40), but the headline obscures the important asymmetry:

- 4/40 outputs were unsafe **false passes**: unsupported claims would have cleared the gate.
- 2/40 were **false failures**: supported paraphrases would have been unnecessarily blocked.
- Pass recognition and failure recognition cannot be calculated without the human-labelled pass/fail totals.

Until recalibrated, use the judge for advisory scoring or triage only, with human review making the release decision.

## Next calibration step

1. Have the PM and a second reviewer adjudicate all six disagreements using an operational definition:

   - **Pass:** Every material claim is directly supported by the supplied evidence or is a meaning-preserving paraphrase.
   - **Fail:** Any material claim adds, contradicts, or overstates information not supported by the evidence.
   - **Needs review:** Support depends on genuine ambiguity or missing evidence.

2. Revise the judge prompt using the adjudicated cases:

   - Require claim-by-claim comparison with the supplied evidence.
   - Explicitly prohibit inferring missing facts.
   - Add development examples distinguishing unsupported additions from valid paraphrases.
   - Return `pass`, `fail`, or `needs_review`, with the claim and supporting—or missing—evidence.

3. Validate the revision on a new, untouched, human-labelled held-out set. Include clear passes, clear failures, supported paraphrases, subtle unsupported claims, mixed answers, adversarial wording, and insufficient-evidence cases. Do not reuse prompt-development cases as validation evidence.

## Provisional automation gate

Automate only after the held-out evaluation demonstrates:

- Zero false passes for unsupported material claims, or a PM-approved nonzero tolerance based on consequence.
- An acceptable false-failure rate set by the PM.
- Stable results across important product slices.
- All `needs_review` cases routed to a human.
- Recalibration whenever the judge model, prompt, evidence format, criterion, or traffic distribution changes.

If zero false passes is required, a modest held-out set only provides preliminary evidence—not proof of zero risk. Increase the sample according to the consequence of releasing unsupported claims.

## Engineering handoff

- Record human and judge labels, disagreement type, rationale, and resolution for every calibration case.
- Report false passes and false failures separately; add pass/failure recognition once class totals are available.
- Implement three-way judge output and fail closed to human review on invalid or inconclusive results.
- PM owns the faithfulness definition, acceptable error trade-off, disagreement adjudication, and final release decision.
- Engineering owns reliable judge execution, evidence delivery, logging, and gate integration.

## Next actions

1. Adjudicate the six disagreements and confirm the cost tolerance for false passes.
2. Revise the rubric and prompt, using the 40 existing cases only for development.
3. Run a new held-out calibration set and reconsider automation from the error types and slice results, not overall agreement alone.