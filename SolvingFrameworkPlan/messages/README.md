# Messages between teams

**Messages only.** Plans, reports, reviews and notes are documents, and they go in `../docs/`. A message is a short, addressed handoff that points to documents by path.

## File name

```
messages/YYYY-MM-DD/YYYY-MM-DD_HHMM_<from>_to_<to>[+<to>...]_<subject>.md
```

- **Date folder:** one folder per day.
- **Time:** `HHMM` is the sender's local time (MDT, UTC−6), 24-hour. Older messages renamed on 5 October carry their first-commit time, or `0000` where it is unknown.
- **From and to:** use the team tokens below. Join several recipients with `+`.
- **Subject:** lower-case words joined by hyphens, and short.

Example: `2026-10-05/2026-10-05_1432_longtable_to_math+navigator_wp19-followup.md`

| Token | Team | Also called |
|---|---|---|
| `longtable` | Long Table | Creative Intel |
| `math` | Math solutions and scale-up team | Math superintel |
| `navigator` | Proof Navigator | ledger; web frontend `docs/navigator/` |
| `audit` | Independent audit | audit chat; Teams A and B |
| `swarm` | Night swarm | gremlins; exploratory only |
| `user` | The user | |

## Required header

Every message starts with this block:

```
# <Subject in words>

- **From:** <team> — <agent or sub-team name, e.g. "Long Table (main session)", "Audit Team A">
- **To:** <team>; <team>
- **Sent:** YYYY-MM-DD HH:MM MDT
- **Replies to:** <path of the message answered, or "none">
- **Asks for:** <decision, review, data, or "information only">
```

## Rules

- A message assigns nothing. Acceptance is an explicit reply, never silence.
- Reply in a new file. Never edit someone else's message.
- Cite evidence by repository path. If you cite an old path, look it up in `../PATHMAP.md`.
- Status words belong to the Proof Navigator.
- A go-ahead for an experiment must name the declaration's SHA-256, the package commit and the phases, and must say "released".
