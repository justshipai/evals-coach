# Scenario design

Use this reference to create a representative, decision-useful test set.

## Contents

1. Evaluation unit
2. Post-launch error analysis
3. Failure taxonomy
4. Case sources
5. Slices
6. Case writing
7. Distribution check

## Start with the evaluation unit

Choose the smallest unit that still answers the product question:

| Unit | Use for |
| --- | --- |
| Response | Classification, extraction, writing, or single-turn answers |
| Component decision | Routing, retrieval, memory, tool choice, or hand-off quality |
| Trajectory | Multi-step behaviour, recovery, looping, or policy adherence |
| Completed task | Whether the user job was actually accomplished |
| Resulting state | Files, records, bookings, permissions, or other changed environments |

Use component evals to diagnose and end-to-end evals to support release decisions. Do not assume one replaces the other.

## Ground post-launch evals in error analysis

When real interactions exist, inspect them before deciding what to evaluate. Use a representative sample, supplemented by known failures and high-consequence cases.

For each interaction:

1. Decide whether the user's primary need was met: pass or fail
2. Write a specific critique that cites observable evidence
3. Note the primary failure, even when several weaknesses are present
4. Record useful context such as task type, user intent, tools, latency, or feedback

Group recurring critiques into fewer than ten primary failure modes where possible. Count frequency, assess consequence, and prioritise the modes that could change a product decision. Preserve important one-off failures rather than forcing every example into a common category.

Use a small sample to discover initial patterns, not to claim stable prevalence. Expand towards roughly 50–100 reviewed interactions before treating the taxonomy as representative, subject to traffic and risk.

## Build a failure taxonomy

Derive failures from the product and users rather than copying a standard list. Consider:

- **Capability:** Cannot complete the primary user job
- **Regression:** Breaks behaviour that currently works
- **Edge:** Fails on unusual but legitimate inputs or environments
- **Ambiguity:** Acts confidently when it should clarify, defer, or expose uncertainty
- **Safety:** Violates a policy, permission, privacy, or destructive-action boundary
- **Recovery:** Cannot recognise, repair, or exit from failure
- **Efficiency:** Succeeds only with unacceptable cost, latency, steps, or user effort

Not every eval needs every category. Include a category only when it could change the decision.

## Source cases responsibly

Label each case by source:

- `production`: observed user interaction or trace
- `research`: user interview, usability study, or domain research
- `support`: support ticket, escalation, or complaint
- `curated`: deliberately authored by a domain expert or PM
- `synthetic`: generated to cover a documented gap
- `inference`: plausible but unverified; review before using as a gate

Never allow synthetic volume to create the illusion of representative coverage.

For a minimum viable pre-launch eval, create five to eight varied cases around one critical behaviour. Replace curated and synthetic cases with production evidence as soon as it becomes available.

## Define slices

A slice is a meaningful subgroup that may perform differently. Examples include:

- User expertise or intent
- Task type and difficulty
- Language, locale, or accessibility need
- New versus existing state
- Tool availability or degraded dependency
- Short versus long context
- Clear versus ambiguous request
- Common versus high-consequence workflow

Use slice floors when an overall average could conceal harm or failure for an important group.

## Write each case

Include:

1. A unique ID and plain-language title
2. Category, priority, source, and slices
3. Input or task
4. Relevant context or starting state
5. Expected outcome
6. Required behaviour
7. Prohibited behaviour
8. Tool expectations when relevant: required, prohibited, conditional, and budget
9. Grader and evidence available to it
10. Repetitions for non-deterministic systems
11. Readiness: ready, needs evidence, needs grader, or needs product decision

Avoid prescribing exact wording unless wording itself matters. Avoid prescribing an exact agent path unless the path is required for safety, policy, or user experience.

For stateful agent tasks, make `context_or_starting_state` reproducible. Include relevant data, permissions, tool availability, simulated failures, expected side effects, and reset or cleanup requirements. If an equivalent tool or route is acceptable, say so rather than naming one ideal trajectory.

## Check the distribution

Before finalising, ask:

- Do common cases reflect real frequency?
- Are rare but catastrophic failures represented?
- Are boundary cases present rather than only obvious passes and failures?
- Could the candidate optimise for this set without improving the product?
- Are multiple cases merely paraphrases?
- What real-user behaviour remains absent?
