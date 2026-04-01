# 05 Architecture Checklist

## Use When

- creating/moving modules,
- changing cross-layer behavior,
- deciding file placement.

## Inputs

1. `DEV_SPEC.md` section `5.2` (directory contract).
2. `DEV_SPEC.md` sections `5.4` and `5.5` (layer and data-flow boundaries).
3. `DEV_SPEC.md` section `5.6` for config-driven boundaries.

## Checklist

- [ ] Map each change to one layer and one responsibility.
- [ ] Keep dependencies flowing top-down through defined interfaces.
- [ ] Place/modify files exactly under paths defined by `5.2`.
- [ ] Do not bypass factory/config boundaries when spec requires them.

## Task-Boundary Note

1. Configuration work in `A4` can use minimal fields for loader precedence.
2. Full section `5.6` coverage is expected in `D10`.

## Conflict Rule

If requested work violates architecture boundaries, stop and ask user to confirm deviation.

## Output Record

1. Layer mapping for each changed file.
2. Boundary checks passed/failed.
3. Approved deviations (if any).
