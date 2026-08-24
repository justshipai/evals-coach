## Critique

This eval can pass while users still fail because it measures an underspecified average rather than successful support outcomes.

- **The sample may be unrepresentative.** Thirty hand-picked questions can omit rare, high-impact, ambiguous, multilingual, adversarial, and multi-turn cases.
- **“Helpfulness” is undefined.** A response can sound clear and empathetic while being incorrect, unsafe, outdated, or impossible to act on.
- **A single LLM judge is unreliable.** It may favor polished wording, share the assistant’s factual errors, or score inconsistently without a rubric and reference evidence.
- **The average hides serious failures.** Twenty-four perfect scores and six completely failed cases average exactly 4.0. Those failures could include account lockouts, billing errors, privacy breaches, or harmful instructions.
- **No task completion is measured.** Users may still need to contact support, repeat themselves, or abandon the task despite receiving a “helpful” answer.
- **No abstention or escalation criteria exist.** The assistant may confidently invent an answer instead of asking for missing information or handing off.
- **No regressions or uncertainty are reported.** A 4.0 observed on 30 cases is noisy, and repeated tuning against the same set invites overfitting.

## Corrected minimum viable eval

### 1. Build a small, stratified test set

Use at least 60 anonymized questions sampled from real support traffic:

- Cover the major intents in proportion to traffic.
- Include at least five cases for every critical workflow.
- Include straightforward, ambiguous, multi-turn, unsupported, and escalation-required cases.
- Tag each case by intent, severity, language, and expected behavior.
- Keep a separate hidden regression set; do not tune prompts against it.

For each case, define:

- The user’s goal.
- Relevant approved documentation or system facts.
- Required answer elements.
- Disallowed claims or actions.
- Whether clarification, refusal, or human escalation is expected.

### 2. Score concrete dimensions

Have a human support expert score every case; an LLM judge may assist but must use the same rubric and cite evidence.

Score each response independently on:

- **Correctness:** factually consistent with approved sources.
- **Goal completion:** enables the user to complete the task, or takes the correct next step.
- **Safety and policy compliance:** avoids prohibited disclosure, action, or advice.
- **Escalation behavior:** asks for necessary information and escalates when required.
- **Clarity:** concise, understandable, and actionable.

Use binary pass/fail for the first four dimensions and a 1–5 score for clarity. Resolve human–judge disagreements on critical cases manually.

### 3. Add outcome-oriented checks

Where feasible, run executable or simulated workflow tests—for example, whether the recommended steps actually reach the correct setting, policy, or resolution. Track:

- Task-success rate.
- Unsupported-claim rate.
- Correct escalation rate.
- Critical-failure count.
- Results by intent and severity, not only overall.

### 4. Apply hard release gates

Ship only if the hidden set meets all of these:

- **Zero critical safety, privacy, or irreversible-action failures.**
- **At least 90% overall task success.**
- **At least 85% task success for every major intent.**
- **At least 95% correct handling of escalation-required cases.**
- **No more than 2% unsupported factual claims.**
- **Average clarity of at least 4/5.**
- **No statistically credible regression against the current production baseline.**

Any failed critical case blocks release regardless of the average. Report confidence intervals and inspect every failure before shipping.

### 5. Validate after launch

Release to a small monitored cohort and compare against the existing assistant using resolution rate, repeat-contact rate, escalation rate, user satisfaction, and safety incidents. Roll back if critical incidents appear or user outcomes materially regress.