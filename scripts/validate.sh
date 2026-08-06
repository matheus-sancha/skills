#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ERRORS=0
CHECKED=0
NAMES=()

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

  # description field — required unless the skill is user-invoked only, in
  # which case the model never sees a description and none is needed.
  desc_val="$(extract_field "$skill_file" "description")"
  slash_only="$(extract_field "$skill_file" "disable-model-invocation")"
  if [[ -z "$desc_val" && "$slash_only" != "true" ]]; then
    error "missing or empty 'description:' field (set 'disable-model-invocation: true' if this skill is user-invoked only)"
  fi

  NAMES+=("$dir_name")

done < <(find "$REPO_ROOT/skills" -name "SKILL.md" | sort)

# ── Cross-skill checks ─────────────────────────────────────────────────────────

# Harness skill directories are flat, so two skills in different categories
# that share a name would collide on install — the second link silently wins.
if [[ ${#NAMES[@]} -gt 0 ]]; then
  while IFS= read -r dupe; do
    [[ -z "$dupe" ]] && continue
    echo "Checking: duplicate names"
    error "skill name '$dupe' is used by more than one directory; names must be unique across categories"
  done < <(printf '%s\n' "${NAMES[@]}" | sort | uniq -d)
fi

# ── Result ─────────────────────────────────────────────────────────────────────

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "All $CHECKED skill(s) valid."
else
  echo "$ERRORS error(s) found across $CHECKED skill(s)." >&2
  exit 1
fi
