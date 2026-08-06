# Claude Code Skills

A collection of custom skills for [Claude Code](https://claude.ai/code) and
Agent-Skills-compatible harnesses — reusable instructions that extend what an
agent can do in your projects.

## Installing

```bash
git clone https://github.com/matheus-sancha/skills
cd skills
```

**Windows** (recommended — Git Bash's `ln -s` silently copies instead of linking):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\link-skills.ps1 -DryRun   # preview
powershell -ExecutionPolicy Bypass -File scripts\link-skills.ps1           # apply
```

**macOS / Linux:**

```bash
bash scripts/link-skills.sh
```

Either script symlinks every skill into `~/.claude/skills` (Claude Code, and
any subagent that can use skills) and `~/.agents/skills` (other Agent-Skills
harnesses). Because they are symlinks, editing a file in this repo is live
immediately and `git pull` needs no re-installation.

The Windows script needs **Developer Mode** on (Settings → System → For
developers) so it can create symlinks without an elevated shell. Without it,
it falls back to directory junctions, which work the same for local paths.

## Available skills

`slash-only` skills fire only when you type `/<name>`; the rest can also be
invoked by the model when the context matches.

### Engineering

| Skill | Description |
|---|---|
| [codebase-design](./skills/engineering/codebase-design/) | Shared vocabulary for designing deep modules — use when designing or restructuring a module's interface |
| [flutter-desktop-app](./skills/engineering/flutter-desktop-app/) | Blueprint for a local-first Flutter app shipped as a plain Windows zip |
| [lean-code-reviewer](./skills/engineering/lean-code-reviewer/) | Review a codebase for waste, redundancy, and AI slop |
| [prototype](./skills/engineering/prototype/) | Build a throwaway prototype to flesh out a design (logic terminal app or UI variations) |

### Productivity

| Skill | Description |
|---|---|
| [handoff](./skills/productivity/handoff/) | `slash-only` — compact the current conversation into a handoff document for another agent |
| [project-reviewer](./skills/productivity/project-reviewer/) | Interview the user relentlessly about a plan or design to stress-test it |
| [skill-creator](./skills/productivity/skill-creator/) | Reference for writing and editing skills well — vocabulary and principles for predictable skills |
| [teach](./skills/productivity/teach/) | `slash-only` — teach the user a new skill or concept across multiple sessions |

### Vendor

Third-party skills copied in, not authored here. See
[skills/vendor/README.md](./skills/vendor/README.md) for upstreams and licensing.

| Skill | Description | Upstream |
|---|---|---|
| [building-native-ui](./skills/vendor/building-native-ui/) | Guide for building apps with Expo Router | [expo/skills](https://github.com/expo/skills) |
| [find-skills](./skills/vendor/find-skills/) | Discover and install agent skills | [vercel-labs/skills](https://github.com/vercel-labs/skills) |

## Repo structure

Everything under `skills/` is installed as a live skill. Anything that should
*not* be — templates, human-facing docs — lives outside it.

```
skills/
├── skills/
│   ├── engineering/
│   │   ├── codebase-design/
│   │   ├── flutter-desktop-app/
│   │   ├── lean-code-reviewer/
│   │   └── prototype/
│   ├── productivity/
│   │   ├── handoff/
│   │   ├── project-reviewer/
│   │   ├── skill-creator/
│   │   └── teach/
│   └── vendor/               ← third-party, minimally edited
│       ├── building-native-ui/
│       └── find-skills/
├── templates/
│   └── example-skill/        ← copy this to start a new skill; NOT installed
├── scripts/
│   ├── link-skills.ps1       ← Windows installer (use this on Windows)
│   ├── link-skills.sh        ← macOS/Linux installer
│   ├── list-skills.sh        ← list all skills in the repo
│   ├── new-skill.sh          ← scaffold a new skill interactively
│   └── validate.sh           ← validate all SKILL.md files
├── docs/
│   ├── authoring-guide.md
│   └── trigger-writing-tips.md
└── .github/workflows/
    └── validate.yml
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add or improve skills.
