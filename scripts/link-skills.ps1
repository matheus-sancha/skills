<#
.SYNOPSIS
    Symlinks every skill in this repository into the local skill directories
    used by each agent harness.

.DESCRIPTION
    Destinations:
      ~/.claude/skills  - Claude Code (and its subagents)
      ~/.agents/skills  - pi and other Agent-Skills-standard harnesses

    Each entry becomes a directory symlink into this repo, so editing a file
    here is live immediately and `git pull` needs no re-installation.

    Requires either Windows Developer Mode (Settings > System > For developers)
    or an elevated shell. Developer Mode is the better option - it lets this
    run unelevated.

    Links are created via `cmd /c mklink /D`, not New-Item -ItemType
    SymbolicLink: Windows PowerShell 5.1 does not pass the
    SYMBOLIC_LINK_FLAG_ALLOW_UNPRIVILEGED_CREATE flag, so New-Item demands
    elevation even when Developer Mode is on. mklink passes it. If a symlink
    still cannot be made, the script falls back to a directory junction, which
    never needs privileges and resolves identically for local paths.

    Note: the Git Bash equivalent (link-skills.sh) silently COPIES instead of
    linking on Windows unless MSYS=winsymlinks:nativestrict is set, which is
    why this script exists. Prefer this one on Windows.

.PARAMETER DryRun
    Print what would change without touching the filesystem.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\link-skills.ps1 -DryRun
    powershell -ExecutionPolicy Bypass -File scripts\link-skills.ps1
#>
[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$RepoRoot   = Split-Path -Parent $PSScriptRoot
$SkillsRoot = Join-Path $RepoRoot 'skills'
$Dests      = @(
    (Join-Path $HOME '.claude\skills'),
    (Join-Path $HOME '.agents\skills')
)

# ── Helpers ───────────────────────────────────────────────────────────────────

function Test-ReparsePoint {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $false }
    $item = Get-Item -LiteralPath $Path -Force
    return [bool]($item.Attributes -band [IO.FileAttributes]::ReparsePoint)
}

function Get-LinkTarget {
    param([string]$Path)
    $item = Get-Item -LiteralPath $Path -Force
    if ($item.PSObject.Properties.Name -contains 'Target' -and $item.Target) {
        return @($item.Target)[0]
    }
    return $null
}

function Remove-Entry {
    param([string]$Path)
    # A directory symlink must be unlinked, NOT recursed into. Remove-Item
    # -Recurse on a reparse point can delete the TARGET's contents in
    # Windows PowerShell 5.1 - use the .NET call, which only drops the link.
    if (Test-ReparsePoint $Path) {
        [IO.Directory]::Delete($Path, $false)
    }
    else {
        Remove-Item -LiteralPath $Path -Recurse -Force -Confirm:$false
    }
}

function New-DirLink {
    param([string]$Link, [string]$Target)
    # /D = directory symbolic link. Honours Developer Mode unelevated.
    $out = cmd /c mklink /D "`"$Link`"" "`"$Target`"" 2>&1
    if (Test-Path -LiteralPath $Link) { return 'symlink' }
    # /J = junction. Needs no privileges at all; local paths only, which is all
    # we ever link. Last resort so the install still works without Dev Mode.
    $out2 = cmd /c mklink /J "`"$Link`"" "`"$Target`"" 2>&1
    if (Test-Path -LiteralPath $Link) { return 'junction' }
    throw "Could not link $Link -> $Target`n  mklink /D: $out`n  mklink /J: $out2"
}

function Write-Action {
    param([string]$Verb, [string]$Message, [string]$Color = 'Gray')
    Write-Host ("  {0,-9} {1}" -f $Verb, $Message) -ForegroundColor $Color
}

# ── Collect skills ────────────────────────────────────────────────────────────

if (-not (Test-Path -LiteralPath $SkillsRoot)) {
    throw "No skills directory at $SkillsRoot"
}

$skills = Get-ChildItem -LiteralPath $SkillsRoot -Recurse -Filter 'SKILL.md' -File |
    ForEach-Object {
        [pscustomobject]@{
            Name = $_.Directory.Name
            Path = $_.Directory.FullName
        }
    } | Sort-Object Name

if (-not $skills) { throw "Found no SKILL.md files under $SkillsRoot" }

# A duplicate name would mean the second link silently wins - catch it here
# rather than wondering later why a skill loads the wrong body.
$dupes = $skills | Group-Object Name | Where-Object Count -gt 1
if ($dupes) {
    throw "Duplicate skill name(s): $($dupes.Name -join ', '). Skill names must be unique across categories."
}

Write-Host "Repo:   $RepoRoot"
Write-Host "Skills: $($skills.Count)"
if ($DryRun) { Write-Host "MODE:   dry run - nothing will be written" -ForegroundColor Yellow }

# ── Link into each destination ────────────────────────────────────────────────

foreach ($dest in $Dests) {
    Write-Host ""
    Write-Host $dest -ForegroundColor Cyan

    # If $dest is itself a link into this repo, the per-skill links below would
    # be written back into the repo's own tree. Bail rather than pollute it.
    if (Test-ReparsePoint $dest) {
        $resolved = Get-LinkTarget $dest
        if ($resolved -and $resolved.StartsWith($RepoRoot, [StringComparison]::OrdinalIgnoreCase)) {
            throw "$dest is a link into this repo ($resolved). Remove it and re-run."
        }
    }

    if (-not (Test-Path -LiteralPath $dest)) {
        if (-not $DryRun) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
        Write-Action 'mkdir' $dest 'Green'
    }

    foreach ($skill in $skills) {
        $target = Join-Path $dest $skill.Name

        if (Test-Path -LiteralPath $target) {
            if (Test-ReparsePoint $target) {
                $current = Get-LinkTarget $target
                if ($current -and $current.TrimEnd('\') -ieq $skill.Path.TrimEnd('\')) {
                    Write-Action 'ok' $skill.Name
                    continue
                }
                Write-Action 'relink' "$($skill.Name)  (was -> $current)" 'Yellow'
            }
            else {
                Write-Action 'replace' "$($skill.Name)  (real directory -> symlink)" 'Yellow'
            }
            if (-not $DryRun) { Remove-Entry $target }
        }
        else {
            Write-Action 'link' $skill.Name 'Green'
        }

        if (-not $DryRun) {
            $kind = New-DirLink -Link $target -Target $skill.Path
            if ($kind -eq 'junction') {
                Write-Action '' "  (fell back to junction)" 'DarkYellow'
            }
        }
    }

    # Prune links that point into this repo but whose target is gone - a skill
    # that was renamed, recategorised, or moved out of skills/. Real
    # directories are never auto-deleted: they may be skills this repo does
    # not own, and guessing wrong is unrecoverable.
    Get-ChildItem -LiteralPath $dest -Directory -Force | ForEach-Object {
        if (-not (Test-ReparsePoint $_.FullName)) { return }
        $t = Get-LinkTarget $_.FullName
        if (-not $t) { return }
        if (-not $t.StartsWith($RepoRoot, [StringComparison]::OrdinalIgnoreCase)) { return }
        if (Test-Path -LiteralPath $t) { return }
        Write-Action 'prune' "$($_.Name)  (dangling -> $t)" 'Red'
        if (-not $DryRun) { Remove-Entry $_.FullName }
    }
}

Write-Host ""
if ($DryRun) {
    Write-Host "Dry run complete. Re-run without -DryRun to apply." -ForegroundColor Yellow
}
else {
    Write-Host "Done. Restart Claude Code to pick up changes." -ForegroundColor Green
}
