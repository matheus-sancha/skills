---
name: example-skill
description: A template skill demonstrating the structure of a Claude Code skill. Use this as a starting point when creating your own skill — copy the directory, rename it, and replace the contents of this file.
version: 1.0.0
license: MIT
---

# Example Skill

This is the body of a skill file. Write your skill instructions here in plain Markdown.

## How this works

When Claude Code loads this skill, it reads the `description:` frontmatter field to decide when to invoke the skill automatically. The body (this section) contains the actual instructions Claude follows when the skill runs.

## Writing skill instructions

- Use imperative voice: "Search for X", "Run Y", "Output Z"
- Be specific about what to do and what to output
- Reference supporting docs in `references/` when the skill is complex

See [references/overview.md](./references/overview.md) for more details on this example, and see [docs/authoring-guide.md](../../docs/authoring-guide.md) for general authoring guidance.

## Getting started

To build your own skill based on this template:

1. Copy this directory: `cp -r example-skill my-skill`
2. Rename the directory to your skill's name (kebab-case)
3. Update the `name:` and `description:` frontmatter fields to match
4. Replace this body with your skill's instructions
5. Run `bash scripts/validate.sh` to confirm everything is valid
