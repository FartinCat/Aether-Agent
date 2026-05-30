---
description: Safely initialize project folders and stubs without conflicts (merges existing data)
category: ops
---
Run workflow `03-scaffold.md` (or execute `python .agent/scripts/scaffold_project.py`).

Determines taxonomy requirements:
- Creates standard `docs/`, `archived/`, and `assets/` subfolders if they do not exist.
- Bootstraps root metadata stubs (`CLAUDE.md`, `AGENTS.md`, `DELETION_REGISTRY.md`) if missing.
- **Smart Merger**: If `AETHER.md` or `README.md` already exist, it parses their metadata, timeline logs, and custom sections, merging them cleanly into Aether's canonical structures without overwriting your custom information.

Run when initializing a new project or updating system configurations.
