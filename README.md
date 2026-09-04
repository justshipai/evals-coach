# Evals Coach

**The evals copilot for AI product managers.** Turn product intent, or real outputs from a live feature, into evals your team can implement, run and improve.

Evals Coach helps product managers move from “the AI should be helpful and accurate” to a small, testable definition of good. It can create an eval plan from a PRD or feature idea, guide a team through its first real scoring cycle, critique an existing eval, expand production failures into regression cases, and help calibrate graders.

It does **not** replace an eval platform or execute your product suite. It helps you decide whether you are measuring the right behaviour, then guides the first manual run before your team automates it.

> Public alpha: the workflow, example and evaluation harness are usable. An initial blinded run is published transparently below; independent replication is still needed.

## What it produces

- The product decision the eval must support
- Observable must / must-not behaviours
- A minimum viable test set with normal, edge, adversarial, and critical cases
- The right grader for each criterion: deterministic, trace, LLM, or human
- Calibration guidance and explicit release gates
- A guided first run using actual outputs, independent human scoring and rubric reconciliation
- Agent tool-call, ordering, budget, and state-reset expectations when relevant
- An engineering-ready handoff plus a path from manual review to CI and production feedback

## Examples

- [AI Meeting Catch-up](examples/ai-meeting-catch-up/eval-plan.md), a complete in-repo eval plan and test set
- [SmartDesk AI Triage & Auto-Resolve](examples/smartdesk-ai-triage/README.md), a public Claude example showing Evals Coach applied to a higher-risk support agent

## Install

Two ways in. Most PMs want the first.

### Easiest: the Evals Coach plugin (Claude)

A guided seven-step wizard. In the Claude app: **Settings → Customize → Plugins → Add → Add marketplace**, enter `justshipai/evals-coach`, then install **Evals Coach**. In Claude Code:

```text
/plugin marketplace add justshipai/evals-coach
/plugin install evals-coach@justshipai
```

Then ask **Evals Coach** to build you an eval, in your own words. It publishes a private web page that walks you from a feature description, or real outputs from a live feature, to a runnable eval, and hands back an eval plan, `test-cases.csv`, judge prompts and a calibration guide. It runs on Claude: drafting spends the account of whoever opens the page, and the page is shared with named people rather than a public link. See [website](https://evalscoach.com).

### For Codex, Claude Code, or any assistant: the skill

The conversational `evals-coach` skill (create, critique, expand, calibrate, run) installs by cloning into a skills directory:

```bash
# Codex / ChatGPT
git clone https://github.com/justshipai/evals-coach.git ~/.agents/skills/evals-coach

# Claude Code
git clone https://github.com/justshipai/evals-coach.git ~/.claude/skills/evals-coach
```

Then, for example: `$evals-coach Create an eval for this feature idea: ...`

You do not need repository access or eval expertise. Start with a PRD, feature idea, workflow, examples, traces, feedback, or an existing eval.

## Useful prompts

```text
$evals-coach Turn this PRD into the smallest eval that can inform a ship decision.

$evals-coach Critique this eval. Tell me what could pass while the product still fails users.

$evals-coach Turn these production failures into regression cases. Do not invent missing evidence.

$evals-coach Help me calibrate this LLM judge against human labels.

$evals-coach Run our first eval using these product outputs and this draft rubric.
```

## Common questions

### How is this different from eval platforms or other eval skills?

Many tools generate datasets, scorers or experiment runs inside a particular platform. Evals Coach works one step upstream: it helps PMs decide what good looks like, which failures matter and what evidence should determine whether a feature ships. The output is vendor-neutral and can be implemented in the eval harness your team already uses.

### Does it work with Codex, Claude Code, Cursor, Lovable or Bolt?

Yes, although installation differs. Codex, [Claude Code](https://docs.anthropic.com/en/docs/claude-code/skills) and [Cursor](https://cursor.com/docs/skills) can load `SKILL.md` as an agent skill. [Lovable supports reusable skills](https://docs.lovable.dev/features/skills). Bolt can upload skills directly from files or GitHub.

On any other AI tool, attach or copy `SKILL.md` and its referenced files into the conversation or project context, then ask the agent to follow Evals Coach.

### What is `SKILL.md`?

A portable instruction file that teaches an AI agent a repeatable workflow. It contains the core Evals Coach method and points the agent to supporting guidance, templates and validation scripts only when needed.

### Do I need a code repository or technical eval experience?

No. Start with whatever you have: a PRD, feature idea, workflow, sample outputs, production failures, user feedback or an existing eval. Repository access is optional evidence, not a requirement.

### Does Evals Coach run the evals?

It can guide your team through its first manual scoring cycle using actual system outputs: prepare the session, capture independent human labels, reconcile disagreements, trial an LLM judge and produce the engineering handoff. It does not call your product system or execute an automated suite. Your team can implement that in Braintrust, LangSmith, Promptfoo, an internal harness or another eval platform.

### Should every agent eval prescribe tool calls?

No. Specify required, prohibited or conditional tool behaviour only when it affects correctness, safety, permissions, recovery, user experience, cost or latency. If several routes can produce the right outcome safely, do not force one ideal trajectory.

## Early evaluation result

In a six-task blinded comparison using GPT-5.6 Sol at medium reasoning, the tested Evals Coach version beat the no-skill baseline on all six tasks: **100% versus 65%** on the original rubric, with zero critical failures versus two.

The same run exposed a weakness: skill outputs averaged 1,867 words versus 862 for baseline. We have since tightened the default output and added PM usability to the rubric. The rubric was developed alongside the skill, there was one run per task and the revised version has not yet been independently replicated. Treat this as promising early evidence rather than a universal claim.

Read the [full method, task scores and limitations](evals/results/2026-08-24-gpt-5.6-sol-medium/report.md).

## Repository map

- `SKILL.md`: the workflow used by the assistant
- `references/`: scenario, grader, and output guidance
- `scripts/validate_test_cases.py`: validates the generated CSV schema
- `scripts/test_workbench_csv.py`: checks the wizard's export still satisfies that schema
- `examples/`: worked PM-to-engineering examples
- `plugin/`: the Claude plugin (the Evals Coach wizard)
- `.claude-plugin/marketplace.json`: lets this repository be added as a plugin marketplace
- `evals/`: cases and rubric for evaluating Evals Coach itself
- `site/`: source of evalscoach.com

## Help shape it

The most useful feedback is concrete:

1. Where did the coach make an eval materially better?
2. What important PM or agent workflow did it miss?
3. Which recommendation was impractical for your stack?
4. Can you contribute a sanitised PRD, failure pattern, or before/after eval?

Please [open an issue](https://github.com/justshipai/evals-coach/issues) or send a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT
