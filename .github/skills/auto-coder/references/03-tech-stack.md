# 03 Tech Stack Checklist

## Use When

- adding/changing dependencies,
- choosing runtime/framework integration patterns.

## Inputs

1. `DEV_SPEC.md` section `3`.
2. Selected task acceptance from `6.4`.

## Checklist

- [ ] Verify candidate change is allowed by section `3`.
- [ ] Verify command/toolchain version baseline before risky changes.
- [ ] Use `uv` for Python dependency and execution commands.
- [ ] Avoid new libraries unless required by selected task.

## Environment Baseline

1. `uv 0.8.10`
2. `nvm 0.39.3`
3. `npm 11.9.0`
4. `node v24.14.0`

## Configuration Staging Rule

1. `A4` builds config loading foundation with minimal key set.
2. `D10` aligns full section `5.6` schema and strict validation.
3. Do not force full `5.6` scope during `A4` unless user asks.

## Output Record

1. Stack compatibility decision.
2. Dependency decision with spec justification.
3. Any version mismatch and risk note.
