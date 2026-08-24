Do not automate the release gate yet.

The judge has 85% agreement (34/40), but the sample is small—the 95% confidence interval is roughly 71–93%—and four outputs with unsupported claims were incorrectly passed. That is the release gate’s highest-risk failure mode. Class-specific false-pass and false-fail rates also cannot be calculated without the full label distribution.

Next calibration step:

- Refine the rubric with explicit rules and examples for unsupported claims and supported paraphrases.
- Run a blinded, independently human-labelled evaluation of at least 200 new outputs, representative of production traffic and enriched with difficult attribution/paraphrase cases.
- Predefine acceptance criteria, prioritizing unsupported-claim recall—for example: zero critical unsupported claims passed and a false-pass rate below 1%, with confidence bounds acceptable for the release risk.
- Review disagreements by category, revise the prompt/rubric, then validate once more on a fresh untouched set.

Until those criteria are met, run the judge in shadow mode or use it for triage with human review, not as the sole release authority.