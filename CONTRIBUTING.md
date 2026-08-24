# Contributing

Evals Coach is a public alpha. Product feedback, worked examples, rubric improvements, and code contributions are welcome.

## Good contributions

- A sanitised PRD plus the eval you wish you had written
- A real failure pattern converted into a regression case
- A critique showing how an eval could pass while users still fail
- Better guidance for agent trajectories, tool calls, graders, or calibration
- Compatibility fixes for a skill runner or eval harness

Do not include customer data, secrets, private traces, or material you cannot publish.

## Before opening a pull request

1. Keep the skill vendor-neutral and understandable by a non-technical PM.
2. Label assumptions and evidence sources; do not manufacture production evidence.
3. If you edit an example CSV, run:

   ```bash
   python3 scripts/validate_test_cases.py examples/ai-meeting-catch-up/test-cases.csv
   ```

4. If you edit the skill workflow, add or update a case in `evals/cases.json`.
5. Explain the product failure your change prevents.

For early feedback, opening an issue before doing extensive work is encouraged.
