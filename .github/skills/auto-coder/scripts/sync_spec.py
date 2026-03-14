#!/usr/bin/env python3
"""Sync auto-coder schedule reference from references/DEV_SPEC.md.

This script parses section 6.2 task rows and regenerates:
  .github/skills/auto-coder/references/06-schedule.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PHASE_RE = re.compile(r"^####\s+阶段\s+([A-Z])")
TASK_RE = re.compile(
    r"^\|\s*([A-Z]\d+)\s*\|\s*([^|]+?)\s*\|\s*(\[(?: |~|x)\])\s*\|\s*([^|]*?)\s*\|"
)


@dataclass(frozen=True)
class Task:
    phase: str
    task_id: str
    name: str
    status: str
    completed_date: str


@dataclass(frozen=True)
class PhaseStats:
    phase: str
    total: int
    done: int
    in_progress: int
    todo: int

    @property
    def progress_pct(self) -> int:
        if self.total == 0:
            return 0
        return round((self.done / self.total) * 100)


def extract_slice(lines: list[str], start_prefix: str, end_prefix: str) -> list[str]:
    start_idx = None
    end_idx = None

    for idx, line in enumerate(lines):
        if line.startswith(start_prefix):
            start_idx = idx
            break

    if start_idx is None:
        raise ValueError(f"Cannot find section starting with: {start_prefix}")

    for idx in range(start_idx + 1, len(lines)):
        if lines[idx].startswith(end_prefix):
            end_idx = idx
            break

    if end_idx is None:
        end_idx = len(lines)

    return lines[start_idx:end_idx]


def parse_tasks(section_62_lines: list[str]) -> list[Task]:
    tasks: list[Task] = []
    current_phase = "?"

    for raw in section_62_lines:
        phase_match = PHASE_RE.match(raw)
        if phase_match:
            current_phase = phase_match.group(1)
            continue

        task_match = TASK_RE.match(raw)
        if not task_match:
            continue

        task_id, name, status, completed_date = task_match.groups()
        tasks.append(
            Task(
                phase=current_phase,
                task_id=task_id.strip(),
                name=name.strip(),
                status=status.strip(),
                completed_date=completed_date.strip() or "-",
            )
        )

    if not tasks:
        raise ValueError("No tasks found in section 6.2")

    return tasks


def compute_phase_stats(tasks: list[Task]) -> list[PhaseStats]:
    order: list[str] = []
    grouped: dict[str, list[Task]] = {}

    for task in tasks:
        if task.phase not in grouped:
            grouped[task.phase] = []
            order.append(task.phase)
        grouped[task.phase].append(task)

    stats: list[PhaseStats] = []
    for phase in order:
        phase_tasks = grouped[phase]
        done = sum(1 for t in phase_tasks if t.status == "[x]")
        in_progress = sum(1 for t in phase_tasks if t.status == "[~]")
        todo = sum(1 for t in phase_tasks if t.status == "[ ]")
        stats.append(
            PhaseStats(
                phase=phase,
                total=len(phase_tasks),
                done=done,
                in_progress=in_progress,
                todo=todo,
            )
        )

    return stats


def choose_task(tasks: list[Task], requested_task: str | None) -> tuple[Task | None, Task | None, Task | None]:
    requested = requested_task.strip().upper() if requested_task else None

    if requested:
        selected = next((t for t in tasks if t.task_id.upper() == requested), None)
        if selected is None:
            known_ids = ", ".join(t.task_id for t in tasks)
            raise ValueError(f"Task '{requested}' not found. Known task IDs: {known_ids}")
    else:
        selected = next((t for t in tasks if t.status == "[~]"), None)
        if selected is None:
            selected = next((t for t in tasks if t.status == "[ ]"), None)

    last_completed = None
    for task in tasks:
        if task.status == "[x]":
            last_completed = task

    in_progress = next((t for t in tasks if t.status == "[~]"), None)
    return last_completed, in_progress, selected


def build_markdown(
    tasks: list[Task],
    phase_stats: list[PhaseStats],
    last_completed: Task | None,
    in_progress: Task | None,
    selected: Task | None,
    requested_task: str | None,
) -> str:
    total_tasks = len(tasks)
    total_done = sum(1 for t in tasks if t.status == "[x]")
    total_pct = round((total_done / total_tasks) * 100) if total_tasks else 0
    generated_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    selected_rule = "user-specified" if requested_task else "auto"
    selected_text = "none"
    if selected is not None:
        selected_text = f"{selected.task_id} ({selected.name})"

    lines: list[str] = []
    lines.append("# 06 Schedule")
    lines.append("")
    lines.append("When to read:")
    lines.append("- at the start of every implementation cycle,")
    lines.append("- after each completed task before reporting.")
    lines.append("")
    lines.append("Source anchors in `references/DEV_SPEC.md`:")
    lines.append("- `### 6.2` progress tracking table,")
    lines.append("- `### 6.3` overall progress table,")
    lines.append("- `### 6.4` task-level implementation details.")
    lines.append("")
    lines.append("Status legend:")
    lines.append("- `[ ]` not started")
    lines.append("- `[~]` in progress")
    lines.append("- `[x]` completed")
    lines.append("")
    lines.append("Task selection algorithm:")
    lines.append("1. if user specifies task ID, use it,")
    lines.append("2. else pick first `[~]` task in section order,")
    lines.append("3. else pick first `[ ]` task in section order.")
    lines.append("")
    lines.append("## Current Snapshot")
    lines.append("")
    lines.append(f"Generated at: `{generated_at}`")
    lines.append(f"Overall: `{total_done}/{total_tasks}` completed (`{total_pct}%`)\n")
    lines.append("| Phase | Total | Done | In Progress | Not Started | Progress |")
    lines.append("| ----- | ----- | ---- | ----------- | ----------- | -------- |")
    for stat in phase_stats:
        lines.append(
            f"| {stat.phase} | {stat.total} | {stat.done} | {stat.in_progress} | {stat.todo} | {stat.progress_pct}% |"
        )
    lines.append("")

    lines.append("## Task Cursor")
    lines.append("")
    if last_completed is None:
        lines.append("- Last completed: `none`")
    else:
        lines.append(f"- Last completed: `{last_completed.task_id}` {last_completed.name}")

    if in_progress is None:
        lines.append("- In progress: `none`")
    else:
        lines.append(f"- In progress: `{in_progress.task_id}` {in_progress.name}")

    lines.append(f"- Selected task ({selected_rule}): `{selected_text}`")
    lines.append("")

    lines.append("## Re-sync")
    lines.append("")
    lines.append("```bash")
    lines.append(
        "python3 .github/skills/auto-coder/scripts/sync_spec.py --spec .github/skills/auto-coder/references/DEV_SPEC.md --force"
    )
    lines.append("```")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync auto-coder schedule reference from references/DEV_SPEC.md")
    parser.add_argument(
        "--spec",
        default=".github/skills/auto-coder/references/DEV_SPEC.md",
        help="Path to DEV_SPEC markdown file",
    )
    parser.add_argument(
        "--out",
        default=".github/skills/auto-coder/references/06-schedule.md",
        help="Output path for generated schedule reference",
    )
    parser.add_argument("--task", default=None, help="Optional task ID override, for example E7")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    spec_path = Path(args.spec)
    out_path = Path(args.out)

    if not spec_path.exists():
        print(f"ERROR: spec file not found: {spec_path}", file=sys.stderr)
        return 1

    if out_path.exists() and not args.force:
        print(f"ERROR: output file exists: {out_path} (use --force to overwrite)", file=sys.stderr)
        return 1

    lines = spec_path.read_text(encoding="utf-8").splitlines()

    try:
        section_62 = extract_slice(lines, "### 6.2", "### 6.3")
        tasks = parse_tasks(section_62)
        phase_stats = compute_phase_stats(tasks)
        last_completed, in_progress, selected = choose_task(tasks, args.task)
        output = build_markdown(
            tasks=tasks,
            phase_stats=phase_stats,
            last_completed=last_completed,
            in_progress=in_progress,
            selected=selected,
            requested_task=args.task,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")

    selected_id = selected.task_id if selected else "none"
    print(f"Wrote {out_path}")
    print(f"Selected task: {selected_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())