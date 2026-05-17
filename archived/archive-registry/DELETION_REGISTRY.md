# Deletion Registry — Aether Agent
This file logs every item deleted, moved, or archived.
Never delete this file.

## Registry

### 2026-05-14
- **DELETED**: `.agent/antigravity-agent-install-state.json` (v4.9.0 — stale, superseded by aether-agent-install-state.json)
- **REASON**: Consolidated to single install state file; new projects now initialize with v0.1.0 instead of inheriting Aether Agent version
- **IMPACT**: npm CLI updated to remove antigravity reference and reset install state version on scaffold
