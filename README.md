# Evals Coach

**The vendor-neutral eval coach for AI PMs.** Turn product intent into evals your team can implement, run, and improve.

Evals Coach helps product managers move from “the AI should be helpful and accurate” to a small, testable definition of good. It can create an eval plan from a PRD or feature idea, critique an existing eval, expand production failures into regression cases, and help calibrate graders.

It does **not** run your evals or replace an eval platform. It helps you decide whether you are measuring the right behaviour before your team automates it.

> Public alpha: the workflow, example and evaluation harness are usable. An initial blinded run is published transparently below; independent replication is still needed.

## What it produces

- The product decision the eval must support
- Observable must / must-not behaviours
- A minimum viable test set with normal, edge, adversarial, and critical cases
- The right grader for each criterion: deterministic, trace, LLM, or human
- Calibration guidance and explicit release gates
- Agent tool-call, ordering, budget, and state-reset expectations when relevant
- An engineering-ready handoff plus a path from manual review to CI and production feedback

See the complete [AI Meeting Catch-up example](examples/ai-meeting-catch-up/eval-plan.md).

## Install

Clone the repository into a skills directory:

```bash
# Codex / ChatGPT
git clone https://github.com/justshipai/evals-coach.git ~/.agents/skills/evals-coach

# Claude Code
git clone https://github.com/justshipai/evals-coach.git ~/.claude/skills/evals-coach
```

Then ask your assistant to use Evals Coach. In Codex, for example:

```text
$evals-coach Create an eval for this feature idea: ...
```

You do not need repository access or eval expertise. Start with a PRD, feature idea, workflow, examples, traces, feedback, or an existing eval.

## Useful prompts

```text
$evals-coach Turn this PRD into the smallest eval that can inform a ship decision.

$evals-coach Critique this eval. Tell me what could pass while the product still fails users.

$evals-coach Turn these production failures into regression cases. Do not invent missing evidence.

$evals-coach Help me calibrate this LLM judge against human labels.
```

## Why this is different

Many tools generate datasets, scorers, or experiment runs inside a particular platform. Evals Coach works one step upstream: it helps PMs choose the behaviours, cases, evidence, graders, and thresholds that make those components meaningful. The output is deliberately vendor-neutral and importable into the harness your team already uses.

## Early evaluation result

In a six-task blinded comparison using GPT-5.6 Sol at medium reasoning, the tested Evals Coach version beat the no-skill baseline on all six tasks: **100% versus 65%** on the original rubric, with zero critical failures versus two.

The same run exposed a weakness: skill outputs averaged 1,867 words versus 862 for baseline. We have since tightened the default output and added PM usability to the rubric. Because the rubric was developed alongside the skill, there was one run per task and the revised version has not yet been independently replicated, treat this as promising early evidence rather than a universal claim.

Read the [full method, task scores and limitations](evals/results/2026-08-24-gpt-5.6-sol-medium/report.md).

## Repository map

- `SKILL.md` — the workflow used by the assistant
- `references/` — scenario, grader, and output guidance
- `scripts/validate_test_cases.py` — validates the generated CSV schema
- `examples/` — worked PM-to-engineering examples
- `evals/` — cases and rubric for evaluating Evals Coach itself

## Help shape it

The most useful feedback is concrete:

1. Where did the coach make an eval materially better?
2. What important PM or agent workflow did it miss?
3. Which recommendation was impractical for your stack?
4. Can you contribute a sanitised PRD, failure pattern, or before/after eval?

Please [open an issue](https://github.com/justshipai/evals-coach/issues) or send a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT
