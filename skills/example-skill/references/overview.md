# Example Skill — Overview

This reference file is an example of how to use the `references/` subdirectory.

## When to use references/

Place supporting Markdown docs here when your skill's instructions are too long to fit cleanly in `SKILL.md`, or when parts of the content are reference material rather than instructions (API tables, configuration schemas, troubleshooting guides, etc.).

Claude Code can read reference files when the skill is invoked, so keep them focused and well-named.

## Naming reference files

Use descriptive kebab-case names that make the content obvious at a glance:

- `api-reference.md`
- `configuration-options.md`
- `troubleshooting.md`
- `setup-guide.md`

## This file

This file exists purely as a demonstration. When you copy `example-skill/` to build your own skill, replace this file with reference material relevant to your skill, or delete the `references/` directory entirely if you don't need it.
