# OpenTofu Module Modification Policy

## General Rule

- **Do Not Modify Modules**: The `modules/` directory contains reusable infrastructure components. You should **never** modify files within the `modules/` directory unless explicitly instructed to do so by the user.
- **Consumption Only**: Focus on consuming these modules in the root compositions (e.g., `prod/`, `staging/`) rather than altering the modules themselves.

## Exceptions

- **Explicit Request**: If the user specifically asks to update, refactor, or fix a module, you may proceed with the modification.
- **New Features**: If a task requires functionality not present in the existing modules, prefer creating a new module or asking the user for permission to extend an existing one before making changes.
