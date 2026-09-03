---
name: eval-workbench
description: Evals Coach for product managers. Publish a guided, seven-step wizard (a private web page) that walks someone from a plain feature description to a runnable eval (criteria, test cases, graders, judge prompts and a release gate) and hands back an eval plan, test-cases.csv and judge prompts. Use whenever someone wants to build, create, design or improve an eval for an AI feature or agent, asks to use Evals Coach, wants a guided or step-by-step way to evaluate what they are shipping, or would rather fill in a form than write a prompt.
---

# Eval Workbench

Publish the workbench as an Artifact on the user's own account, then tell them what it is
and how it bills. The page is self-contained: do not rewrite it, and do not reimplement it
in the conversation.

## Publish it

1. Copy the page to a working file, so the source in the plugin stays pristine:
   `cp "${CLAUDE_PLUGIN_ROOT}/skills/eval-workbench/assets/eval-workbench.html" ./eval-workbench.html`
2. Publish it with the Artifact tool:
   - `file_path`: the copy
   - `favicon`: 🎚️ (first publish only — never change it on a republish)
   - `capabilities`: `{"sample": {}, "downloads": true}`
   - `description`: one sentence naming what the page does
3. Report the result in one or two sentences. Do not paste the URL — the publish card carries it.

If the Artifact tool is unavailable in this session, deliver the file with SendUserFile
instead and say plainly that drafting will not run from a local copy, because the page
asks Claude through the artifact runtime.

## What to tell them once it is published

Say these three things, briefly, because each one surprises people:

- **Drafting runs on the viewer's own Claude account.** Whoever opens the page consents on
  first use and it spends their usage, not the publisher's.
- **It degrades rather than breaks.** Without drafting the page becomes a worksheet: every
  step keeps its shape, starter suggestions and templates, and the outputs still assemble.
- **Sharing is bounded.** A page that uses Claude or offers downloads cannot take an
  "anyone with the link" URL; it is shared with named people. For a link that can go
  anywhere, publish a copy with no capabilities declared — the page detects their absence
  and presents itself as a worksheet.

## Keeping it in step with the coach

The workbench's drafting prompts encode the same commitments as the
[evals-coach skill](https://github.com/justshipai/evals-coach/blob/main/SKILL.md) at the
repository root: start from the product decision, replace vague quality words with
observable behaviour, prefer a minimum viable eval, never let curated cases pose as
production traffic, and never let an uncalibrated judge gate a release. When that guidance
changes materially, change the prompts in the page to match: they are plain strings in the
`draft*` functions near the end of the file.
