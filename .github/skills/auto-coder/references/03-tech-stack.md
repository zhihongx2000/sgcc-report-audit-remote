# 03 Tech Stack

When to read:

- before adding dependencies,
- before choosing frameworks, runtimes, or integration patterns.

Source anchors in `references/DEV_SPEC.md`:

- `## 3.` for approved stack and implementation boundaries.

Extract these facts:

1. allowed runtime and framework choices,
2. required integration approach,
3. dependency restrictions.

Environment baseline:

1. Python project management: `uv 0.8.10`.
2. Frontend environment management: `nvm 0.39.3`.
3. Frontend package manager: `npm 11.9.0`.
4. Node runtime: `node v24.14.0`.

Implementation rule:

- prefer existing stack conventions,
- avoid introducing libraries not justified by section `3`.
- run Python commands with `uv`, and run frontend commands under the configured `nvm` Node runtime.
