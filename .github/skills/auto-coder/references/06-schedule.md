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

Task selection algorithm:

1. if user specifies task ID, use it,
2. else pick first `[~]` task in section order,
3. else pick first `[ ]` task in section order.

## Current Snapshot

Generated at: `2026-03-14 13:54:06`
Overall: `0/118` completed (`0%`)

| Phase | Total | Done | In Progress | Not Started | Progress |
| ----- | ----- | ---- | ----------- | ----------- | -------- |
| A     | 5     | 0    | 0           | 5           | 0%       |
| B     | 7     | 0    | 0           | 7           | 0%       |
| C     | 10    | 0    | 0           | 10          | 0%       |
| D     | 11    | 0    | 0           | 11          | 0%       |
| E     | 16    | 0    | 0           | 16          | 0%       |
| F     | 11    | 0    | 0           | 11          | 0%       |
| G     | 10    | 0    | 0           | 10          | 0%       |
| H     | 13    | 0    | 0           | 13          | 0%       |
| I     | 15    | 0    | 0           | 15          | 0%       |
| J     | 10    | 0    | 0           | 10          | 0%       |
| K     | 10    | 0    | 0           | 10          | 0%       |

## Task Cursor

- Last completed: `none`
- In progress: `none`
- Selected task (auto): `A1 (创建完整目录结构与空文件)`

## Re-sync

```bash
python3 .github/skills/auto-coder/scripts/sync_spec.py --spec .github/skills/auto-coder/references/DEV_SPEC.md --force
```
