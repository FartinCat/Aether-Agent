---
title: "SCAFFOLD ASSETS"
description: "Initialize project structure and taxonomy."
order: 3
category: ops
---
# Workflow: Scaffold Asset Taxonomy



**Objective**: Enforce a standardized resource organization matrix and bootstrap the project metadata state file required by versioning, market-evaluator, and commercial-license agents.



## Execution Sequence

1. **Automated Scaffolding Execution**: Execute the python helper script at the project root:
   ```bash
   python .agent/scripts/scaffold_project.py
   ```

2. **Smart Resolution & Safe Parsing**:
   - The script automatically detects the environment and resolves `ASSETS_ROOT` (uses `src/assets/` if `src/` exists, otherwise `assets/` at root).
   - Generates taxonomy subfolders under `ASSETS_ROOT` (`images/`, `videos/`, `audios/`, `texts/`, `information/`, `icons/`).
   - Standardizes documentation subfolders (`docs/scan-reports/`, `docs/audit-reports/`, `docs/master-plans/`, `docs/research/`, `docs/market-evaluations/`, `docs/maps/`, `docs/opencode-sessions/`).
   - Initializes archive directories and stubs (`archived/archive-registry/DELETION_REGISTRY.md`, etc.).
   - Automatically scans the project root for temporary session dumps (`session-ses_*.md`) and migrates them safely into `docs/opencode-sessions/` to keep the root directory pristine.

3. **Smart Integration & Preservation**:
   - **`AETHER.md`**: If a pre-existing `AETHER.md` is present, the script extracts custom metadata (§14) and timeline logs (§18), reconstructs a fully formatted canonical `AETHER.md` matching the latest Aether governance rules, and cleanly merges the user's data back.
   - **`README.md`**: If a pre-existing `README.md` is present, it preserves all custom headings and paragraphs while cleanly injecting the updated npx-based deployment section.
   - **Stubs**: Verifies `AGENTS.md` and `CLAUDE.md` stubs are present.

4. **Verify Alignment**:
   - Verify that the title of `AETHER.md` matches the actual version number in §14 Project Metadata.
   - Verify that all newly created assets match the required project layout, with zero root pollution.

## Manual Invocation

- Via chat: `/scaffold` (or `/scaffold-assets`)
- Shell command: `python .agent/scripts/scaffold_project.py`
- Automatically triggered as Step 1 of `build-website` and `build-app` workflows.

