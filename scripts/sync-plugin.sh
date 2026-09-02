#!/usr/bin/env sh
# The skill at the repo root is canonical. The plugin ships a copy so that
# `/plugin install` delivers a self-contained skill directory.
# Run this after editing SKILL.md, references/ or scripts/, then commit both.
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
dest="$root/plugin/skills/evals-coach"

mkdir -p "$dest"
rm -rf "$dest/references" "$dest/scripts"
cp "$root/SKILL.md" "$dest/SKILL.md"
cp -R "$root/references" "$dest/references"
mkdir -p "$dest/scripts"
cp "$root/scripts/validate_test_cases.py" "$dest/scripts/validate_test_cases.py"

echo "Synced SKILL.md, references/ and scripts/ into plugin/skills/evals-coach"
