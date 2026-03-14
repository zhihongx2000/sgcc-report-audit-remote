# 05 Architecture

When to read:

- creating new modules,
- changing cross-layer behavior,
- deciding file placement.

Source anchors in `references/DEV_SPEC.md`:

- `## 5.` for system architecture and module design,
- `### 5.2` for full directory structure,
- `### 5.4` and `### 5.5` for layered responsibilities and data flow.

Enforcement checklist:

1. map each code change to the correct layer,
2. avoid bypassing layer boundaries,
3. place files exactly where section `5.2` defines,
4. keep contracts explicit between modules.

If requested work violates the architecture contract, surface the conflict and ask for confirmation before proceeding.
