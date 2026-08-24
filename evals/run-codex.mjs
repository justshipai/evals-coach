#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "..");
const cases = JSON.parse(readFileSync(join(here, "cases.json"), "utf8"));
const args = new Set(process.argv.slice(2));
const dryRun = args.has("--dry-run");
const conditionArg = process.argv[process.argv.indexOf("--condition") + 1];
const conditions = !args.has("--condition") || conditionArg === "both"
  ? ["baseline", "skill"]
  : [conditionArg];

if (args.has("--condition") && !["baseline", "skill", "both"].includes(conditionArg)) {
  throw new Error("--condition must be baseline, skill, or both");
}

const codex = spawnSync("codex", ["--version"], { encoding: "utf8" });
if (!dryRun && codex.status !== 0) {
  throw new Error("codex CLI is required and must be authenticated");
}

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
  conditions,
  case_ids: cases.map(item => item.id),
  note: "Score final.md files blind with evals/rubric.md"
};
writeFileSync(join(outputRoot, "manifest.json"), JSON.stringify(manifest, null, 2));

for (let index = 0; index < cases.length; index += 1) {
  const item = cases[index];
  const ordered = index % 2 === 0 ? conditions : [...conditions].reverse();

  for (const condition of ordered) {
    const runDir = join(outputRoot, item.id, condition);
    mkdirSync(runDir, { recursive: true });
    const workspace = mkdtempSync(join(tmpdir(), `evals-coach-${item.id}-`));

    try {
      if (condition === "skill") {
        const destination = join(workspace, ".agents", "skills", "evals-coach");
        mkdirSync(destination, { recursive: true });
        for (const path of ["SKILL.md", "references", "scripts"]) {
          cpSync(join(root, path), join(destination, path), { recursive: true });
        }
      }

      const invocation = condition === "skill"
        ? "Use the $evals-coach skill. "
        : "";
      const prompt = `${invocation}${item.prompt}\n\nReturn only the finished deliverable, not your internal reasoning.`;
      writeFileSync(join(runDir, "prompt.txt"), prompt);

      if (dryRun) {
        writeFileSync(join(runDir, "DRY_RUN"), "No model call made.\n");
        continue;
      }

      const result = spawnSync("codex", [
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--skip-git-repo-check",
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
        throw new Error(`${item.id}/${condition} failed; inspect ${runDir}`);
      }
    } finally {
      rmSync(workspace, { recursive: true, force: true });
    }
  }
}

console.log(dryRun
  ? `Dry-run layout written to ${outputRoot}`
  : `Evaluation outputs written to ${outputRoot}`);
