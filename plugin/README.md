# Evals Coach (Claude plugin)

**Evals Coach** as a Claude plugin: a guided seven-step wizard that turns a feature
description (or real outputs from a live feature) into a runnable eval and hands back an
eval plan, `test-cases.csv`, judge prompts and a calibration guide.

## Install

In the Claude app: **Settings → Customize → Plugins → Add → Add marketplace**, enter
`justshipai/evals-coach`, then install **Evals Coach**.

In Claude Code:

```
/plugin marketplace add justshipai/evals-coach
/plugin install evals-coach@justshipai
```

Then ask Evals Coach to build you an eval, in your own words.

## Two flows in one wizard

- **Pre-launch**, you describe the feature; drafting works from your description at every
  step. Cases are curated (labelled as such in the handoff).
- **Post-launch**, you paste real outputs, optional notes on what's off, and optional
  human-edited "gold" versions. Criteria and cases are then grounded in what actually
  happened, and where gold versions exist the drafting derives them from the delta between
  what happened and what should have happened.

## Two things to know

- Drafting runs on the Claude account of whoever opens the page. They consent on first
  use and it spends their usage, not the publisher's.
- A page that uses Claude cannot take a public "anyone with the link" URL, so you share it
  with named people. Opened without drafting, it degrades to a worksheet with the same
  structure, starter suggestions and outputs.

## Contents

- `skills/evals-coach/`: publishes the wizard; the page itself is under `assets/`.

## Prefer to chat, or working in Codex?

The underlying conversational `evals-coach` skill (create, critique, expand, calibrate
and run) lives at the [repository root](https://github.com/justshipai/evals-coach) and
installs by cloning into a skills directory in either Claude Code or Codex. Same
philosophy, chat interface instead of a wizard. See the repository README.
