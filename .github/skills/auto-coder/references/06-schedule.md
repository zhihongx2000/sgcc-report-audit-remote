# 06 Schedule

When to read:
- at the start of every implementation cycle,
- after each completed task before reporting.

Source anchors in `references/DEV_SPEC.md`:
- `### 6.2` progress tracking table,
- `### 6.3` overall progress table,
- `### 6.4` task-level implementation details.

Status legend:
- `[ ]` not started
- `[~]` in progress
- `[x]` completed
- completion date format for completed tasks: `YY-MM-DD HH:mm:ss`

Task selection algorithm:
1. if user specifies task ID, use it,
2. else pick first `[~]` task in section order,
3. else pick first `[ ]` task in section order.

## Next Cycle Checklist

- [ ] Read references in mandatory order (`00` -> `06`) before coding.
- [ ] Confirm selected task acceptance in `DEV_SPEC.md` section `6.4`.
- [ ] Keep implementation inside selected task scope only.
- [ ] Run bounded test loop (`round 0..2`) and stop/escalate on round 3.
- [ ] Update `6.2` and `6.3` after success, then re-sync this file.

## Scope Guardrails

- `DEV_SPEC.md` is authoritative over reference summaries.
- Do not pull future-stage tasks into the current task unless user requests it.
- Config staging: `A4` is baseline loading; full `5.6` semantics are aligned in `D10`.

## Current Snapshot

Generated at: `2026-03-26 21:46:23`
Overall: `28/118` completed (`24%`)

| Phase | Total | Done | In Progress | Not Started | Progress |
| ----- | ----- | ---- | ----------- | ----------- | -------- |
| A | 5 | 5 | 0 | 0 | 100% |
| B | 7 | 7 | 0 | 0 | 100% |
| C | 10 | 10 | 0 | 0 | 100% |
| D | 11 | 6 | 0 | 5 | 55% |
| E | 16 | 0 | 0 | 16 | 0% |
| F | 11 | 0 | 0 | 11 | 0% |
| G | 10 | 0 | 0 | 10 | 0% |
| H | 13 | 0 | 0 | 13 | 0% |
| I | 15 | 0 | 0 | 15 | 0% |
| J | 10 | 0 | 0 | 10 | 0% |
| K | 10 | 0 | 0 | 10 | 0% |

## Task Cursor

- Last completed: `D6` VectorStore 抽象与 PgVector 实现
- In progress: `none`
- Selected task (auto): `D7 (Reranker 抽象与实现)`
- Selection reason: `first [ ] task in section order`

## Re-sync

```bash
python3 .github/skills/auto-coder/scripts/sync_spec.py --spec .github/skills/auto-coder/references/DEV_SPEC.md --force
```

Fallback (when workspace `python3` is broken):

```bash
./rag-server/.venv/bin/python .github/skills/auto-coder/scripts/sync_spec.py --spec .github/skills/auto-coder/references/DEV_SPEC.md --force
```
