---
name: auto-coder
description: Spec-first coding workflow for the sgcc-report-audit project. Use when implementing, testing, reviewing, or advancing any scheduled task from references/DEV_SPEC.md (A1-K10). Enforces strict DEV_SPEC compliance, task selection from section 6.2, mandatory planning, config-driven implementation, bounded auto-fix test loops, and progress updates in sections 6.2 and 6.3.
---

# Auto Coder

Implement project tasks by treating `references/DEV_SPEC.md` as the single source of truth.

## Core Rules

1. Treat `references/DEV_SPEC.md` as authoritative.
2. Accept user supplements only when they do not conflict with `references/DEV_SPEC.md`.
3. If a conflict exists, stop and ask the user to choose the final requirement.
4. Never skip the planning step.
5. Read only what is needed, then implement fully.

## Toolchain Baseline

Use these project toolchain versions by default:

- Python project manager: `uv 0.8.10`
- Frontend runtime manager: `nvm 0.39.3`
- Node package manager: `npm 11.9.0`
- Node.js runtime: `node v24.14.0`

Execution rule:

1. Use `uv` for Python dependency management and command execution.
2. Use `nvm`-managed Node/NPM for frontend tasks.
3. If local versions differ, report mismatch before proceeding with risky changes.

## References Map

Load these references on demand:

- `references/DEV_SPEC.md`: Canonical full specification document.
- `references/01-overview.md`: Project mission, boundaries, and non-goals.
- `references/02-features.md`: Feature expectations and output behavior.
- `references/03-tech-stack.md`: Required stack and dependency constraints.
- `references/04-testing.md`: Test strategy, directory placement, and mock policy.
- `references/05-architecture.md`: Layering, module boundaries, and file locations.
- `references/06-schedule.md`: Task queue logic and current progress snapshot.

Run `python3 .github/skills/auto-coder/scripts/sync_spec.py --spec .github/skills/auto-coder/references/DEV_SPEC.md --force` to refresh the schedule snapshot.

## Workflow

### 1) Sync Spec and Pick Task

1. Read `references/DEV_SPEC.md` section `6.2`.
2. Resolve target task with this priority:
   1. If user specifies a task ID (for example `E7`), use it directly.
   2. Else pick the first `[~]` task in section order.
   3. If none is `[~]`, pick the first `[ ]` task in section order.
3. Record context:
   - last `[x]` task,
   - selected task ID,
   - selected task acceptance/test notes from `6.4`.

### 2) Read Exact Spec Scope

Read only the sections needed for the selected task in `references/DEV_SPEC.md`:

1. Always read:
   - section `5` (architecture/module boundaries),
   - section `3` (tech stack),
   - section `4` (testing),
   - section `6.4` row for the selected task.
2. Read section `2` when behavior/output semantics are involved.
3. Read section `1` when project context is missing.

### 3) Produce a Mandatory Plan

Before coding, provide a concise plan with:

1. files to modify/create,
2. acceptance criteria from `6.4`,
3. tests to add/update,
4. risks and fallback handling.

Do not start editing before this plan is explicit.

### 4) Implement

1. Follow directory and layering rules from section `5.2`.
2. Keep implementation inside the selected task scope.
3. Prefer configuration from `*settings.yaml`; do not hardcode runtime values.
4. Match existing code style and naming.
5. If required files are missing, create them only if they are present in section `5.2`.

### 5) Add Tests and Self-Review

1. Place tests in the correct tree based on section `5.2` (`unit`, `integration`, `e2e`).
2. Mock external dependencies in unit tests.
3. Self-review before running tests:
   - planned files exist,
   - test imports resolve,
   - config fields are read from config, not hardcoded.

### 6) Test and Auto-Fix Loop

Run this bounded loop:

```text
Round 0..2:
  Run pytest on relevant test file(s)
  If pass -> continue
  If fail -> analyze, patch, rerun

Round 3 still failing:
  STOP and report failure details to user
```

### 7) Persist Progress

After successful implementation and tests:

1. Update selected task row in section `6.2`:
   - status,
   - completion date.
2. Update aggregate counters in section `6.3`.
3. Run re-sync command:

```bash
python3 .github/skills/auto-coder/scripts/sync_spec.py --spec .github/skills/auto-coder/references/DEV_SPEC.md --force
```

4. Return summary and ask for next action using this format:

```text
✅ [<TASK_ID>] <task-name> - done
	Files: <file-1>, <file-2>
	Tests: <passed>/<total> passed
	Commit: feat(scope): [<TASK_ID>] <summary>

	"commit" -> git add + commit
	"skip"   -> end
	"next"   -> commit + start next task
```

5. If user chooses `next`, return to step `1`.

## Output Contract

When reporting work, include:

1. Selected task ID and why it was selected.
2. Files changed.
3. Tests run and result.
4. Whether sections `6.2` and `6.3` were updated.
5. Any remaining risks.
