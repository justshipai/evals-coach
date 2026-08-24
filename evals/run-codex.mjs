#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { randomInt } from "node:crypto";
import {
  copyFileSync,
  cpSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync
} from "node:fs";
import { homedir, tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "..");
const cases = JSON.parse(readFileSync(join(here, "cases.json"), "utf8"));
const argv = process.argv.slice(2);

function hasFlag(name) {
  return argv.includes(name);
}

function option(name, fallback) {
  const index = argv.indexOf(name);
  if (index === -1) return fallback;
  const value = argv[index + 1];
  if (!value || value.startsWith("--")) throw new Error(`${name} requires a value`);
  return value;
}

const dryRun = hasFlag("--dry-run");
const conditionArg = option("--condition", "both");
const model = option("--model", "gpt-5.6-sol");
const effort = option("--effort", "medium");
const repetitions = Number.parseInt(option("--repetitions", "1"), 10);
const conditions = conditionArg === "both" ? ["baseline", "skill"] : [conditionArg];

if (!["baseline", "skill", "both"].includes(conditionArg)) {
  throw new Error("--condition must be baseline, skill, or both");
}
if (!Number.isInteger(repetitions) || repetitions < 1) {
  throw new Error("--repetitions must be a positive integer");
}

const codex = spawnSync("codex", ["--version"], { encoding: "utf8" });
if (!dryRun && codex.status !== 0) {
  throw new Error("codex CLI is required and must be authenticated");
}

const git = spawnSync("git", ["rev-parse", "HEAD"], { cwd: root, encoding: "utf8" });
const runId = new Date().toISOString().replaceAll(":", "-");
const outputRoot = join(root, ".eval-runs", runId);
mkdirSync(outputRoot, { recursive: true });

function contaminationPaths() {
  return [
    join(homedir(), ".agents", "skills", "evals-coach"),
    join(homedir(), ".codex", "skills", "evals-coach")
  ].filter(existsSync);
}

const contaminated = contaminationPaths();
if (conditions.includes("baseline") && contaminated.length) {
  throw new Error(`Baseline contaminated by installed skill: ${contaminated.join(", ")}`);
}

const manifest = {
  run_id: runId,
  created_at: new Date().toISOString(),
  source_commit: git.status === 0 ? git.stdout.trim() : null,
  codex_cli: codex.status === 0 ? codex.stdout.trim() : "not checked in dry run",
  node: process.version,
  model,
  reasoning_effort: effort,
  repetitions,
  conditions,
  case_ids: cases.map(item => item.id),
  note: "Share blind-review without condition-map.json; reveal the map only after scores are fixed."
};
writeFileSync(join(outputRoot, "manifest.json"), JSON.stringify(manifest, null, 2));

const totalRuns = cases.length * conditions.length * repetitions;
let completedRuns = 0;
console.log(`${dryRun ? "Planning" : "Running"} ${totalRuns} evaluations with ${model} at ${effort} reasoning.`);

for (let caseIndex = 0; caseIndex < cases.length; caseIndex += 1) {
  const item = cases[caseIndex];

  for (let repetition = 1; repetition <= repetitions; repetition += 1) {
    const ordered = (caseIndex + repetition) % 2 === 0
      ? conditions
      : [...conditions].reverse();

    for (const condition of ordered) {
      const runName = `run-${String(repetition).padStart(2, "0")}`;
      const runDir = join(outputRoot, item.id, condition, runName);
      mkdirSync(runDir, { recursive: true });
      const workspace = mkdtempSync(join(tmpdir(), `evals-coach-${item.id}-`));
      const nextRun = completedRuns + 1;
      console.log(`[${nextRun}/${totalRuns}] ${item.id} · ${condition} · ${runName}`);

      try {
        if (condition === "skill") {
          const destination = join(workspace, ".agents", "skills", "evals-coach");
          mkdirSync(destination, { recursive: true });
          for (const path of ["SKILL.md", "references", "scripts"]) {
            cpSync(join(root, path), join(destination, path), { recursive: true });
          }
        }

        const invocation = condition === "skill" ? "Use the $evals-coach skill. " : "";
        const prompt = `${invocation}${item.prompt}\n\nReturn only the finished deliverable, not your internal reasoning.`;
        writeFileSync(join(runDir, "prompt.txt"), prompt);

        if (dryRun) {
          writeFileSync(join(runDir, "DRY_RUN"), "No model call made.\n");
          completedRuns += 1;
          continue;
        }

        const result = spawnSync("codex", [
          "exec",
          "--ephemeral",
          "--ignore-user-config",
          "--ignore-rules",
          "--skip-git-repo-check",
          "--model",
          model,
          "--config",
          `model_reasoning_effort=\"${effort}\"`,
          "--json",
          "--output-last-message",
          join(runDir, "final.md"),
          "-C",
          workspace,
          prompt
        ], { encoding: "utf8", maxBuffer: 20 * 1024 * 1024 });

        writeFileSync(join(runDir, "trace.jsonl"), result.stdout ?? "");
        writeFileSync(join(runDir, "stderr.txt"), result.stderr ?? "");
        writeFileSync(join(runDir, "exit-code.txt"), `${result.status}\n`);
        if (result.status !== 0) {
          throw new Error(`${item.id}/${condition}/${runName} failed; inspect ${runDir}`);
        }
        completedRuns += 1;
      } finally {
        rmSync(workspace, { recursive: true, force: true });
      }
    }
  }
}

if (!dryRun && conditions.length === 2) {
  const blindRoot = join(outputRoot, "blind-review");
  const mapping = {};
  mkdirSync(blindRoot, { recursive: true });
  copyFileSync(join(here, "rubric.md"), join(blindRoot, "rubric.md"));

  for (const item of cases) {
    mapping[item.id] = {};
    const caseRoot = join(blindRoot, item.id);
    mkdirSync(caseRoot, { recursive: true });
    writeFileSync(join(caseRoot, "task.md"), `${item.prompt}\n`);

    for (let repetition = 1; repetition <= repetitions; repetition += 1) {
      const runName = `run-${String(repetition).padStart(2, "0")}`;
      const labels = randomInt(2) === 0
        ? { A: "baseline", B: "skill" }
        : { A: "skill", B: "baseline" };
      mapping[item.id][runName] = labels;

      for (const [label, condition] of Object.entries(labels)) {
        copyFileSync(
          join(outputRoot, item.id, condition, runName, "final.md"),
          join(caseRoot, `${runName}-${label}.md`)
        );
      }
    }
  }

  writeFileSync(join(outputRoot, "condition-map.json"), JSON.stringify(mapping, null, 2));
  writeFileSync(join(blindRoot, "README.md"), [
    "# Blind review bundle",
    "",
    "Score every A/B output with `rubric.md` before requesting `condition-map.json`.",
    "The condition mapping is deliberately outside this directory.",
    ""
  ].join("\n"));
}

console.log(dryRun
  ? `Dry-run layout written to ${outputRoot}`
  : `Evaluation outputs written to ${outputRoot}`);
if (!dryRun && conditions.length === 2) {
  console.log(`Share only ${join(outputRoot, "blind-review")} with the scorer.`);
  console.log(`Keep ${join(outputRoot, "condition-map.json")} private until scoring is fixed.`);
}
