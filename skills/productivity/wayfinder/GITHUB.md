# Wayfinder — GitHub operations

Every command below was verified against the live GitHub API. `$R` is
`owner/repo`.

## Three ids, and which one each call wants

This is the trap. An issue has three identifiers, and the relationship
endpoints want the one you are least likely to reach for:

| Id | Looks like | Used by |
|---|---|---|
| number | `4` | everything human-facing, `gh issue *` |
| **database id** | `5085517167` | **sub-issue and dependency endpoints** |
| node id | `I_kwDOTwlKK88AAAABLx7Vbw` | GraphQL only |

`gh issue list --json id` returns the **node** id, not the database id. Fetch
the database id explicitly:

```bash
gh api repos/$R/issues/<number> --jq .id
```

Passing the wrong id fails without a useful error. Fetch it, don't guess it.

## Windows: drop the leading slash

In Git Bash, MSYS rewrites a leading-slash path into a Windows filesystem path,
so `gh api /repos/...` becomes `C:/Program Files/Git/repos/...` and fails. Write
API paths **without** the leading slash — `gh api repos/$R/issues` — which works
on every platform. (`MSYS_NO_PATHCONV=1` also works, but omitting the slash is
one less thing to remember.)

## Charting

```bash
# The map.
gh issue create -R $R -t "<destination-shaped title>" -F map-body.md \
  --label "wayfinder:map"

# A ticket. Create all of them first — wiring needs ids to exist.
gh issue create -R $R -t "<question-shaped title>" -F ticket-body.md \
  --label "wayfinder:grilling"

# Second pass: make each ticket a sub-issue of the map.
TICKET_ID=$(gh api repos/$R/issues/<ticket-number> --jq .id)
gh api -X POST repos/$R/issues/<map-number>/sub_issues -F sub_issue_id=$TICKET_ID

# Second pass: wire blocking. "<blocked> is blocked by <blocker>".
BLOCKER_ID=$(gh api repos/$R/issues/<blocker-number> --jq .id)
gh api -X POST repos/$R/issues/<blocked-number>/dependencies/blocked_by \
  -F issue_id=$BLOCKER_ID
```

Labels must exist before use: `gh label create "wayfinder:map" --force`.

**Cap: 50 issues per relationship type.** A map needing more than 50 sub-issues
is really two maps.

## The frontier — one GraphQL query

Do **not** try to find the frontier with `gh search issues ... is:blocked`. The
REST search API silently returns zero results for `is:blocked` and `is:blocking`
— and silently returns zero for any unknown `is:` value, so a wrong qualifier
looks exactly like an empty frontier. Verified: an issue with a live open
blocker does not match `is:blocked`.

One query returns everything needed to compute the frontier client-side:

```bash
Q='query($owner:String!,$repo:String!,$number:Int!){
  repository(owner:$owner,name:$repo){
    issue(number:$number){
      title
      subIssues(first:50){
        nodes{
          number title state url
          assignees(first:5){nodes{login}}
          blockedBy(first:50){nodes{number state}}
        }
      }
    }
  }
}'

gh api graphql -f owner=<owner> -f repo=<repo> -F number=<map-number> -f query="$Q" \
  --jq '.data.repository.issue.subIssues.nodes[]
        | select(.state=="OPEN")
        | select((.assignees.nodes|length)==0)
        | select([.blockedBy.nodes[]|select(.state=="OPEN")]|length==0)
        | "#\(.number) \(.title)"'
```

The three filters are the three conditions of the frontier: **open**,
**unclaimed**, **unblocked**. Swap the last filter to `length>0` to list the
blocked tickets and what they wait on.

`gh` has `jq` built in via `--jq`; a standalone `jq` binary may not be on PATH.

## Working a ticket

```bash
# Claim, before any work.
gh issue edit -R $R <number> --add-assignee @me

# Resolve: answer as a comment, then close.
gh issue comment -R $R <number> -F answer.md
gh issue close -R $R <number>

# Rule out of scope: close without a resolution comment, then add the
# one-line gist to the map's Out of scope section.
gh issue close -R $R <number> -c "Out of scope: <why>"
```

Closing a ticket unblocks everything it was blocking — verified: the newly
unblocked ticket appears in the next frontier query with no further action.

## Reading the map

```bash
gh issue view -R $R <map-number>                    # the low-res view
gh issue view -R $R <ticket-number> --comments      # zoom into one ticket
```

Load the map body once per session. Zoom into individual tickets only on
demand — that is the whole point of the map being an index.
