# Evals Coach rubric

Score each criterion 0, 1, or 2. Use **not applicable** only where stated; do not silently award full credit.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Decision framing | No product or release decision | Decision implied but broad | One explicit decision the eval will inform |
| Behavioural criteria | Vague adjectives | Some observable behaviour | Product-specific must/must-not behaviour with severity |
| Test-set quality | Generic happy paths or invented evidence | Some useful variety | Small representative set with normal, edge, adversarial/critical cases and honest sources |
| Runnable cases | Prose only | Partially structured | Inputs, state, expected behaviour, prohibited behaviour, priority, and grader are implementation-ready |
| Grader fit | One fuzzy judge for everything | Mostly suitable | Cheapest reliable method per criterion; evidence and limitations are explicit |
| Calibration integrity | Uncalibrated judge treated as truth | Calibration mentioned | Human labels, disagreements, false-pass/false-fail analysis, and held-out validation |
| Release contract | No gate or average-only gate | Threshold without rationale/slices | Hard gates for severe failures, provisional thresholds, repeated runs, slices, and ownership |
| Agent trajectory | Ignores tools/state when relevant | Mentions tools | Required/prohibited/conditional calls, ordering, budgets, arguments, final state, and reset are specified |
| Handoff and loop | Advice ends at a document | Some next steps | Engineering handoff plus path from manual review to CI and production failures |
| Uncertainty discipline | Fabricates facts or overclaims | Some assumptions visible | Asks only material questions, labels assumptions, and distinguishes observed from hypothetical data |
| PM usability | Disproportionate wall of text or implementation detail obscures the decision | Understandable but longer, repetitive, or more technical than needed | Decision-first, scannable, proportionate, and immediately usable by a PM; detail is separated or omitted |

## Hard failures

Flag separately even if the numeric score is high:

- Fabricated production evidence, user data, or benchmark results
- No runnable cases in a create/expand task
- An uncalibrated LLM judge presented as trustworthy ground truth
- A severe safety or trust failure allowed to disappear inside an average
- Missing tool/state constraints for an agent task where the final answer could look correct after an unsafe trajectory
- A sparse first request expanded into a comprehensive-looking strategy that a PM cannot reasonably run or review
- In a first-run task, fabricated outputs, human labels, judge results or ship decisions

## Reporting

Report:

- Total and per-criterion score
- Hard-failure count and description
- Baseline-to-skill delta by task
- Regressions introduced by the skill
- Output word count and PM-usability score
- At least three qualitative examples supporting the scores

The suite is a product-quality check, not proof of universal model improvement.
