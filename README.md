# Claude Code Skills

A public collection of custom skills for [Claude Code](https://claude.ai/code) and Agent-Skills-compatible harnesses — installable slash commands that extend what Claude can do in your projects.

## Installing

```bash
git clone https://github.com/matheus-sancha/skills
cd skills
bash scripts/link-skills.sh
```

`link-skills.sh` symlinks every skill into `~/.claude/skills` (Claude Code) and `~/.agents/skills` (other Agent-Skills harnesses). To update later, `git pull` in the repo — no re-installation needed.

## Available skills

### Engineering

| Skill | Description |
|---|---|
| [codebase-design](./skills/engineering/codebase-design/) | Shared vocabulary for designing deep modules — use when designing or restructuring a module's interface |
| [prototype](./skills/engineering/prototype/) | Build a throwaway prototype to flesh out a design (logic terminal app or UI variations) |

### Productivity

| Skill | Description |
|---|---|
| [handoff](./skills/productivity/handoff/) | Compact the current conversation into a handoff document for another agent to pick up |
| [project-reviewer](./skills/productivity/project-reviewer/) | Interview the user relentlessly about a plan or design to stress-test it |
| [skill-creator](./skills/productivity/skill-creator/) | Reference for writing and editing skills well — vocabulary and principles for predictable skills |
| [teach](./skills/productivity/teach/) | Teach the user a new skill or concept across multiple sessions, within a workspace |

### Examples

| Skill | Description |
|---|---|
| [example-skill](./skills/example-skill/) | Template demonstrating the skill structure — copy it to build your own |

## Repo structure

```
skills/
├── skills/
│   ├── engineering/
│   │   ├── codebase-design/
│   │   └── prototype/
│   ├── productivity/
│   │   ├── handoff/
│   │   ├── project-reviewer/
│   │   ├── skill-creator/
│   │   └── teach/
│   └── example-skill/
├── scripts/
│   ├── link-skills.sh     ← symlink all skills into harness directories
│   ├── list-skills.sh     ← list all skills in the repo
│   ├── new-skill.sh       ← scaffold a new skill interactively
│   └── validate.sh        ← validate all SKILL.md files
├── docs/
│   ├── authoring-guide.md
│   └── trigger-writing-tips.md
└── .github/workflows/
    └── validate.yml
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add or improve skills.
