# Writing Skill Descriptions That Trigger Reliably

The `description:` field in your `SKILL.md` frontmatter is the most important line in the file. Claude Code reads it to decide whether to invoke your skill automatically — and whether to surface it when a user types `/`.

## How Claude uses the description

Claude matches the description against:
- What the user typed (their message or slash command)
- The current context (open files, recent messages, project type)

A vague description means the skill gets missed. A precise description means it fires at the right moment.

## What to include

### 1. Explicit trigger phrases

Name the exact words or patterns that should trigger the skill:

```yaml
description: >
  Scaffold a new React component. Use when the user asks to "create a component",
  "add a component", or mentions a component name that doesn't exist yet.
```

### 2. User intent signals

Describe the problem the user is trying to solve, not just what the skill does:

```yaml
# Too vague
description: Helps with TypeScript errors.

# Better — names the intent
description: >
  Diagnose and fix TypeScript type errors. Use when the user pastes a TS error,
  asks why a type isn't working, or asks to "fix the types".
```

### 3. Anti-triggers (what NOT to use it for)

If your skill overlaps with another, say when to prefer yours:

```yaml
description: >
  Run the full test suite and summarize failures. Use for "run tests" or "check tests".
  For a single test file, use /test-file instead.
```

## What to avoid

- **Don't describe implementation details.** The description is for matching, not documentation.
- **Don't use jargon** the user wouldn't type themselves.
- **Don't be too broad.** A description like "helps with code" matches everything and nothing.
- **Don't list every possible synonym.** 3–5 trigger phrases is enough.

## Length

One or two sentences is ideal. Claude truncates long descriptions — front-load the most important trigger phrase.

## Testing your description

After installing the skill, try:
1. Typing the exact phrases you listed — does Claude invoke the skill?
2. Asking something adjacent that should NOT trigger it — does Claude stay quiet?
3. Typing `/<skill-name>` explicitly — does the skill body match what you described?
