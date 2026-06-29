#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_ROOT="$REPO_ROOT/skills"

# ── Prompt helpers ─────────────────────────────────────────────────────────────

prompt() {
  local var_name="$1" prompt_text="$2"
  read -r -p "$prompt_text" "$var_name"
}

# ── Validate kebab-case ────────────────────────────────────────────────────────

is_kebab_case() {
  [[ "$1" =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]]
}

# ── Main ───────────────────────────────────────────────────────────────────────

echo "Claude Code Skill Scaffolder"
echo "────────────────────────────"

# List existing categories
existing_categories=()
while IFS= read -r -d '' d; do
  existing_categories+=("$(basename "$d")")
done < <(find "$SKILLS_ROOT" -maxdepth 1 -mindepth 1 -type d -not -name 'example-skill' -print0 2>/dev/null | sort -z)

if [[ ${#existing_categories[@]} -gt 0 ]]; then
  echo "Existing categories: ${existing_categories[*]}"
fi

# Category
while true; do
  prompt CATEGORY "Category (kebab-case, e.g. engineering): "
  if [[ -z "$CATEGORY" ]]; then
    echo "Error: category cannot be empty." >&2
  elif ! is_kebab_case "$CATEGORY"; then
    echo "Error: category must be kebab-case." >&2
  else
    break
  fi
done

# Skill name
while true; do
  prompt SKILL_NAME "Skill name (kebab-case, e.g. my-skill): "
  if [[ -z "$SKILL_NAME" ]]; then
    echo "Error: name cannot be empty." >&2
  elif ! is_kebab_case "$SKILL_NAME"; then
    echo "Error: name must be kebab-case (lowercase letters, numbers, hyphens — no spaces or capitals)." >&2
  elif [[ -d "$SKILLS_ROOT/$CATEGORY/$SKILL_NAME" ]]; then
    echo "Error: 'skills/$CATEGORY/$SKILL_NAME' already exists." >&2
  else
    break
  fi
done

# Description
while true; do
  prompt SKILL_DESC "Description (one or two sentences, or leave blank for user-invoked): "
  break
done

# User-invoked?
DISABLE_MODEL=""
if [[ -z "$SKILL_DESC" ]]; then
  DISABLE_MODEL="disable-model-invocation: true"$'\n'
fi

# References directory
prompt ADD_REFS "Create a references/ subdirectory? [y/N] "
ADD_REFS="${ADD_REFS,,}"  # lowercase

# ── Create files ───────────────────────────────────────────────────────────────

SKILL_DIR="$SKILLS_ROOT/$CATEGORY/$SKILL_NAME"
mkdir -p "$SKILL_DIR"

TITLE="$(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2); print}')"

DESC_LINE=""
if [[ -n "$SKILL_DESC" ]]; then
  DESC_LINE="description: $SKILL_DESC"$'\n'
fi

cat > "$SKILL_DIR/SKILL.md" <<EOF
---
name: $SKILL_NAME
${DESC_LINE}${DISABLE_MODEL}version: 1.0.0
---

# $TITLE

TODO: Write your skill instructions here.
EOF

if [[ "$ADD_REFS" == "y" ]]; then
  mkdir -p "$SKILL_DIR/references"
  cat > "$SKILL_DIR/references/README.md" <<EOF
# $SKILL_NAME — References

Add supporting Markdown documents here.
EOF
  echo "Created: skills/$CATEGORY/$SKILL_NAME/references/README.md"
fi

echo ""
echo "Created: skills/$CATEGORY/$SKILL_NAME/SKILL.md"
echo ""
echo "Next steps:"
echo "  1. Edit skills/$CATEGORY/$SKILL_NAME/SKILL.md — fill in your skill instructions"
echo "  2. Run: bash scripts/validate.sh"
echo "  3. Add an entry to the README.md skills table under '$CATEGORY'"
