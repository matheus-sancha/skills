# Skill Authoring Guide

This guide covers how to write Claude Code skills that are clear, focused, and reliably invoked.

## Frontmatter reference

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Kebab-case; must match the directory name exactly |
| `description` | Yes | One or two sentences; Claude reads this to decide when to invoke the skill |
| `version` | Recommended | Semantic version (e.g. `1.0.0`) |
| `license` | Recommended | `MIT` for public skills |

## Writing the skill body

The body is instructions to Claude. Write in imperative, second-person voice:

**Do:**
> Search the current directory for all `.test.ts` files. For each file, check that it imports from `@testing-library/react`. Report any that don't.

**Avoid:**
> This skill helps with testing files. It can look at TypeScript files and check imports.

### Structural tips

- **One skill, one job.** If a skill does two unrelated things, split it.
- **Be specific about output.** Tell Claude exactly what to produce — a list, a summary, a code block, etc.
- **Reference supporting docs** in `references/` for large tables, config schemas, or anything that would clutter the main instructions.
- **Use headers** to break multi-step instructions into named stages. Claude follows them in order.

## When to use `references/`

Add a `references/` subdirectory when your skill needs lookup material that isn't instructions — for example:

- An API reference table the skill needs to consult
- A configuration schema with many fields
- A troubleshooting guide the skill should surface conditionally

Keep each reference file focused on one topic. Name them descriptively (`api-reference.md`, `config-options.md`).

## Testing your skill

1. Run `bash scripts/validate.sh` — catches missing frontmatter.
2. Install the skill locally and invoke it manually to verify behavior.
3. Test the edge cases mentioned in the description.
