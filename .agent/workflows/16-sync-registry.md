---
title: "SYNC REGISTRY"
description: "Synchronize all registry files with actual .agent/ state."
order: 16
category: ops
---
# Workflow: Sync Registry

**Objective:** Keep **`AETHER.md`** (§13 registry, §14 metadata, §16 changelog, §18 session),
**`.agent/aether-agent-install-state.json`** (plus **`.agent/antigravity-agent-install-state.json`** mirror when sync writes state), `README.md`, `LICENSE.md`, and `archived/archive-registry/DELETION_REGISTRY.md` synchronized with the actual `.agent/`
filesystem. Enforced by the executable engine at `.agent/scripts/sync_registry.py`.

## Trigger Conditions
- Automatically as LAST STEP of any workflow that creates new .agent/ files
- Manually via /sync-registry
- Automatically when scanner detects drift
- Automatically before /release-project packaging step

## Execution Sequence

### Step 1 — Run the Sync Engine
Execute the Python script:
```bash
python .agent/scripts/sync_registry.py
```
The script performs ALL of the following steps autonomously:

### Step 2 — Drift Detection
Compares filesystem vs **`.agent/aether-agent-install-state.json`** for:
- Rules, Skills, Workflows, Agents, Instincts, Commands (file counts + names)
- Version field (**`AETHER.md` §1 / §14** vs install-state.json)
- **`AETHER.md` §16** (changelog entry for current version)
- **`AETHER.md` §18** (session sync marker for current version when applicable)

### Step 3 — Collision & Integrity Detection
- Scans `.agent/skills/` and `.agent/.agents/skills/` for duplicate numeric prefixes
- Detects gaps in numbering sequences
- Strips BOM corruption (`\x07` bell characters) from registry outputs

### Step 4 — Synchronization (only if drift detected)
1. **`.agent/aether-agent-install-state.json`**: Updates component lists, counts, version, changelog map, timestamp (and mirrors to **`.agent/antigravity-agent-install-state.json`** for legacy tooling)
2. **`AETHER.md` §13**: Full regeneration of agents + workflows registry from filesystem
3. **`AETHER.md` §16 / §18**: Inserts changelog + session entries when the engine bumps or reconciles version
4. **`archived/archive-registry/DELETION_REGISTRY.md`**: Reconciles deletion/archival entries created by move-first operations
5. **README.md**: Updates version badges
6. **LICENSE.md**: Updates applies-to-version field

### Step 5 — Verification & Report
Re-validates all components and prints file write status.

### Step 6 — Semantic & Reference Diagnostics
Runs deep diagnostic audits:
- **Version Synchronization**: Scans all active code and markdown files in the workspace to verify there are no out-of-sync or outdated version references.
- **File Path Audit**: Scans rules, workflows, commands, and skills to ensure all referenced system paths exist on disk.
- **Model Synchronization**: Audits consistent referencing and tracking of LLM models across active operating files.

Outputs final health metrics:
- **HEALTH: GREEN** — No collisions, no gaps, no BOM corruption, and all references nominal.
- **HEALTH: YELLOW** — Non-critical anomalies like version mismatches or broken file path references detected.

## Primary Script
- `.agent/scripts/sync_registry.py`

## Related Skill
- `.agent/skills/22-registry-synchronizer.md`
