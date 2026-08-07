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
| [diagnosing-bugs](./skills/engineering/diagnosing-bugs/) | Diagnosis discipline for hard bugs — build a tight, red-capable feedback loop before hypothesising |
| [flutter-desktop-app](./skills/engineering/flutter-desktop-app/) | Blueprint for a local-first Flutter app shipped as a plain Windows zip |
| [lean-code-reviewer](./skills/engineering/lean-code-reviewer/) | Review a codebase for waste, redundancy, and AI slop |
| [prototype](./skills/engineering/prototype/) | Build a throwaway prototype to flesh out a design (logic terminal app or UI variations) |
| [review-changes](./skills/engineering/review-changes/) | Review a diff on two axes — repo standards, and fidelity to the originating spec |

### Productivity

| Skill | Description |
|---|---|
| [handoff](./skills/productivity/handoff/) | `slash-only` — compact the current conversation into a handoff document for another agent |
| [project-reviewer](./skills/productivity/project-reviewer/) | Interview the user relentlessly about a plan or design to stress-test it |
| [research](./skills/productivity/research/) | Investigate a question against primary sources, captured as a cited Markdown file |
| [skill-creator](./skills/productivity/skill-creator/) | Reference for writing and editing skills well — vocabulary and principles for predictable skills |
| [teach](./skills/productivity/teach/) | `slash-only` — teach the user a new skill or concept across multiple sessions |
| [wayfinder](./skills/productivity/wayfinder/) | `slash-only` — plan work too big for one session as a map of tickets on GitHub Issues |

Three review skills exist and the boundary between them is **scope**:
`review-changes` reviews a diff, `lean-code-reviewer` reviews a whole codebase,
and the built-in `/code-review` hunts bugs.

`diagnosing-bugs`, `research`, `review-changes`, and `wayfinder` are adapted
from [Matt Pocock's skills](https://github.com/mattpocock), rewritten to depend
only on skills in this repo and to target GitHub Issues directly.

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
│   │   ├── diagnosing-bugs/
│   │   ├── flutter-desktop-app/
│   │   ├── lean-code-reviewer/
│   │   ├── prototype/
│   │   └── review-changes/
│   ├── productivity/
│   │   ├── handoff/
│   │   ├── project-reviewer/
│   │   ├── research/
│   │   ├── skill-creator/
│   │   ├── teach/
│   │   └── wayfinder/
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
