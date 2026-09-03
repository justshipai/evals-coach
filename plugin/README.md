# Eval Workbench (Claude plugin)

The **PM Eval Workbench**, packaged as a Claude plugin (Claude app and Claude Code). Ask
for "the eval workbench" and it publishes a seven-step wizard as a private Artifact:
describe your feature, and it drafts the evaluation question, criteria, test cases,
graders, judge prompts and release gate, each editable, ending in an eval plan,
`test-cases.csv` and judge prompts.

## Install

In the Claude app: **Settings → Customize → Plugins → Add → Add marketplace**, enter
`justshipai/evals-coach`, then install **Eval Workbench**.

In Claude Code:

```
/plugin marketplace add justshipai/evals-coach
/plugin install evals-coach@justshipai
```

Then ask for **the eval workbench**.

## Two things to know

- Drafting runs on the Claude account of whoever opens the page. They consent on first use
  and it spends their usage, not the publisher's.
- A page that uses Claude cannot take a public "anyone with the link" URL, so you share it
  with named people. Opened without drafting, it degrades to a worksheet with the same
  structure, starter suggestions and outputs.

## Contents

- `skills/eval-workbench/` — publishes the workbench; the page itself is under `assets/`.

## Already have real outputs? Use the coach directly

The plugin's wizard is best for **pre-launch** work: you describe a feature and it drafts
the whole eval structure for you. For **post-launch** products with real traffic, cases
and criteria should come from what actually happened, not from a description.

The underlying conversational `evals-coach` skill (design, critique, expand, calibrate and
guide a first real scoring run) lives at the
[repository root](https://github.com/justshipai/evals-coach) and installs by cloning into
your assistant's skills directory in either Claude Code or Codex. It's the right tool when
you want to paste in real outputs and do error discovery on them. See the repository README.
