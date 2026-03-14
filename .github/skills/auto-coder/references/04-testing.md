# 04 Testing

When to read:

- before writing or modifying tests,
- before defining test scope for a task.

Source anchors in `references/DEV_SPEC.md`:

- `## 4.` for testing conventions,
- `### 6.4` selected task row for acceptance and test method.

Testing rules:

1. place tests in the tree defined by section `5.2`.
2. mock external dependencies in unit tests.
3. keep integration/e2e for cross-component behavior.
4. run targeted tests first, then broader scope when needed.

Minimum pre-run self-check:

1. all new test files import cleanly,
2. fixtures and paths match project layout,
3. assertions map to `6.4` acceptance criteria.
