# Contributing

Thanks for contributing a skill! Here's everything you need to know.

## Skill location

Skills live under `skills/<category>/<skill-name>/`:

```
skills/
└── engineering/
│   └── my-skill/
│       ├── SKILL.md           # Required
│       └── references/        # Optional: supporting docs Claude can read
│           └── some-guide.md
└── productivity/
    └── my-other-skill/
        └── SKILL.md
```

Current categories: `engineering`, `productivity`. Add a new category directory if your skill doesn't fit either.

## Skill format

### `SKILL.md` frontmatter

```yaml
---
name: my-skill                  # Required — kebab-case, must match directory name
description: ...                # Required for model-invoked skills (omit if user-invoked)
version: 1.0.0                  # Recommended
license: MIT                    # Recommended for public skills
disable-model-invocation: true  # Optional — set to prevent Claude from auto-invoking
argument-hint: "..."            # Optional — shown when the user types the skill name
---
```

The body is plain Markdown written as instructions to Claude — imperative, specific, and focused on one task. See [docs/authoring-guide.md](./docs/authoring-guide.md) for writing guidance and [docs/trigger-writing-tips.md](./docs/trigger-writing-tips.md) for description best practices.

### Model-invoked vs user-invoked

- **Model-invoked** (default): include a `description:` — Claude can fire the skill automatically based on context, and other skills can reach it by name. The description adds to context load every turn, so keep it tight.
- **User-invoked**: set `disable-model-invocation: true` — only fires when the user types `/<skill-name>`. Zero context load, but the user must remember it exists.

See [skills/productivity/skill-creator/SKILL.md](./skills/productivity/skill-creator/SKILL.md) for the full reference on this decision.

## Naming conventions

- Directory name and `name:` field must be identical
- Use kebab-case (`my-skill`, not `mySkill` or `my_skill`)
- Keep names short and descriptive (2–4 words max)

## Scaffold a new skill

```bash
bash scripts/new-skill.sh
```

Prompts for a category, name, and description, then creates the directory and `SKILL.md`.

## Scripts reference

| Script | Purpose |
|---|---|
| `scripts/link-skills.sh` | Symlink all skills into `~/.claude/skills` and `~/.agents/skills` |
| `scripts/list-skills.sh` | List all `SKILL.md` paths in the repo |
| `scripts/new-skill.sh` | Scaffold a new skill interactively |
| `scripts/validate.sh` | Validate all `SKILL.md` files for required fields |

## Validate before opening a PR

```bash
bash scripts/validate.sh
```

Checks that every `SKILL.md` has the required fields and that directory names match the `name:` field. CI runs this automatically on all PRs.

## PR checklist

- [ ] Skill is in the right category under `skills/<category>/<skill-name>/`
- [ ] Directory name matches `name:` in frontmatter
- [ ] `description:` is present (or `disable-model-invocation: true` is set intentionally)
- [ ] `bash scripts/validate.sh` passes locally
- [ ] `README.md` skills table updated with the new entry
