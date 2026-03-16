# 04 Testing Checklist

## Use When

- adding/updating tests,
- deciding unit vs integration vs e2e scope.

## Inputs

1. `DEV_SPEC.md` section `4`.
2. Selected task row in `6.4`.
3. Directory placement rules from section `5.2`.

## Checklist

- [ ] Place tests under correct tree (`unit`/`integration`/`e2e`).
- [ ] Ensure assertions directly map to selected task acceptance criteria.
- [ ] Mock external dependencies in unit tests.
- [ ] Run targeted pytest first, then broaden only if needed.
- [ ] Follow bounded auto-fix loop (round 0..2).

## Pre-Run Gate

1. Test imports resolve.
2. Fixtures/path assumptions match repository layout.
3. Assertions and expected errors are deterministic.

## Output Record

1. Test files added/updated.
2. Command list and pass/fail counts.
3. Remaining testing risk.
