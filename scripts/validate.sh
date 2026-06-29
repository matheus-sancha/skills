#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ERRORS=0
CHECKED=0

# ── Helpers ────────────────────────────────────────────────────────────────────

error() {
  echo "  ERROR: $*" >&2
  ERRORS=$((ERRORS + 1))
}

extract_field() {
  local file="$1" field="$2"
  # Reads the value of a frontmatter field (between the first pair of ---)
  awk -v field="$field" '
    /^---$/ { if (in_fm) exit; in_fm=1; next }
    in_fm && $0 ~ "^" field ": " { sub("^" field ": *", ""); print; exit }
  ' "$file"
}

# ── Scan skills ────────────────────────────────────────────────────────────────

while IFS= read -r skill_file; do
  dir_name="$(basename "$(dirname "$skill_file")")"
  CHECKED=$((CHECKED + 1))
  echo "Checking: $dir_name/SKILL.md"

  # name field
  name_val="$(extract_field "$skill_file" "name")"
  if [[ -z "$name_val" ]]; then
    error "missing or empty 'name:' field"
  elif [[ "$name_val" != "$dir_name" ]]; then
    error "name '$name_val' does not match directory '$dir_name'"
  fi

  # description field
  desc_val="$(extract_field "$skill_file" "description")"
  if [[ -z "$desc_val" ]]; then
    error "missing or empty 'description:' field"
  fi

done < <(find "$REPO_ROOT/skills" -name "SKILL.md" | sort)

# ── Result ─────────────────────────────────────────────────────────────────────

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "All $CHECKED skill(s) valid."
else
  echo "$ERRORS error(s) found across $CHECKED skill(s)." >&2
  exit 1
fi
