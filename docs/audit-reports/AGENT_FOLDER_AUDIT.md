# .agent/ Folder — Complete Infrastructure Audit

**Date:** 2026-05-29
**Auditor:** Aether Agent OS
**Scope:** Full inventory of `.agent/` — every file, subfolder, purpose, and deletability.

---

## Overview

| Metric | Value |
|--------|-------|
| Total entries | 8 subdirectories + 1 root file |
| Total files | ~166 |
| Total size | ~967 KB |
| CORE items | `rules/`, `skills/`, `workflows/`, `instincts/`, `.agents/`, `install-state.json` |
| TOOL items | `scripts/`, `skills/ui-ux-pro-max/` |
| CONFIG items | `mcps/` |
| ARTIFACT items | `scripts/__pycache__/`, `skills/ui-ux-pro-max/scripts/__pycache__/` |

---

## File Tree

```
.agent/
├── .agents/
│   └── skills/
│       ├── 01-deep-scan/                (3.9 KB SKILL.md)
│       │   └── agents/openai.yaml
│       ├── 02-failure-predictor/        (2.7 KB)
│       │   └── agents/openai.yaml
│       ├── 03-ask/                      (2.4 KB)
│       │   └── agents/openai.yaml
│       ├── 04-planner/                  (2.6 KB)
│       │   └── agents/openai.yaml
│       ├── 05-synthesizer/              (3.1 KB)
│       │   └── agents/openai.yaml
│       ├── 06-tdd-guide/                (3.8 KB)
│       │   └── agents/openai.yaml
│       ├── 07-python-agent/             (3.4 KB)
│       │   └── agents/openai.yaml
│       ├── 08-rust-agent/               (3.9 KB)
│       │   └── agents/openai.yaml
│       ├── 09-jsts-agent/               (3.7 KB)
│       │   └── agents/openai.yaml
│       ├── 10-c-agent/                  (3.6 KB)
│       │   └── agents/openai.yaml
│       ├── 11-go-agent/                 (4.1 KB)
│       │   └── agents/openai.yaml
│       ├── 12-antibug/                  (4.2 KB)
│       │   └── agents/openai.yaml
│       ├── 13-web-aesthetics/           (3.2 KB)
│       │   └── agents/openai.yaml
│       ├── 14-scientific-writing/       (4.6 KB)
│       │   └── agents/openai.yaml
│       ├── 15-latex-bib-manager/        (3.1 KB)
│       │   └── agents/openai.yaml
│       ├── 16-readme-architect/         (4.1 KB)
│       │   └── agents/openai.yaml
│       ├── 17-market-evaluator/         (3.1 KB)
│       │   └── agents/openai.yaml
│       ├── 18-commercial-license/       (2.8 KB)
│       │   └── agents/openai.yaml
│       ├── 19-git-commit-author/        (3.6 KB)
│       │   └── agents/openai.yaml
│       ├── 20-code-reviewer/            (3.2 KB)
│       │   └── agents/openai.yaml
│       ├── 21-security-auditor/         (3.0 KB)
│       │   └── agents/openai.yaml
│       ├── 22-test-engineer/            (2.7 KB)
│       │   └── agents/openai.yaml
│       └── 23-mcp-auditor/              (1.5 KB — MISSING openai.yaml!)
│           └── SKILL.md only
├── aether-agent-install-state.json      (5.7 KB — canonical manifest)
├── instincts/
│   ├── README.md
│   ├── 01-minimal-footprint.md
│   ├── 02-verification-before-confidence.md
│   ├── 03-user-intent-preservation.md
│   ├── 04-graceful-degradation.md
│   ├── 05-commercial-quality-standard.md
│   └── 06-asset-pruning.md
├── mcps/
│   ├── README.md
│   ├── 21st-dev-magic.md
│   ├── figma-remote.md
│   ├── mongodb.md
│   ├── playwright.md
│   ├── StitchMCP.md
│   └── supabase.md
├── rules/
│   ├── 00-workflow-orchestration.md     (2.5 KB)
│   ├── 01-core.md                       (1.8 KB)
│   ├── 02-integrity.md                  (1.7 KB)
│   ├── 03-instincts.md                  (3.3 KB)
│   ├── 04-verification-gates.md         (1.7 KB)
│   ├── 05-context-integrity.md          (1.5 KB)
│   ├── 06-context-memory.md             (2.2 KB)
│   ├── 07-metadata-awareness.md         (1.2 KB)
│   ├── 08-asset-awareness.md            (2.1 KB)
│   ├── 09-archive-management.md         (1.8 KB)
│   ├── 10-semantic-versioning.md        (1.9 KB)
│   ├── 11-git-awareness.md              (1.9 KB)
│   ├── 12-silent-ingest.md              (0.8 KB)
│   ├── 13-self-improvement.md           (2.8 KB)
│   ├── 14-release-packaging.md          (2.1 KB)
│   ├── 15-context-engine.md             (3.2 KB)   ← has YAML frontmatter
│   ├── 16-sdd-lifecycle.md              (1.1 KB)   ← has YAML frontmatter
│   ├── 17-agent-composition.md          (1.1 KB)   ← has YAML frontmatter
│   ├── 18-knowledge-persistence.md      (1.1 KB)   ← has YAML frontmatter
│   ├── 19-test-before-done.md           (1.1 KB)   ← has YAML frontmatter
│   ├── 20-output-organization.md        (1.9 KB)   ← has YAML frontmatter
│   ├── 21-destructive-operation-safety.md (2.7 KB) ← has YAML frontmatter
│   └── 22-continuous-versioning.md      (1.4 KB)   ← has YAML frontmatter
├── scripts/
│   ├── bootstrap.js                     (6.1 KB)
│   ├── deep_scan_engine.py              (7.7 KB)
│   ├── detect_root.py                   (9.3 KB)
│   ├── readme_architect.py              (7.5 KB)
│   ├── sanitize_frontmatter.py          (6.1 KB)
│   ├── sync_registry.py                 (27.8 KB — central engine)
│   ├── upgrade_project.py               (3.4 KB)
│   └── __pycache__/                     (32.7 KB — ARTIFACT)
│       ├── detect_root.cpython-310.pyc
│       ├── readme_architect.cpython-310.pyc
│       └── sync_registry.cpython-310.pyc
├── skills/
│   ├── README.md
│   ├── 01-research-loop.md              (4.9 KB)
│   ├── 02-language-routing.md           (1.8 KB)
│   ├── 03-task-decomposition.md         (2.0 KB)
│   ├── 04-architectural-design.md       (2.8 KB)
│   ├── 05-code-synthesis.md             (3.1 KB)
│   ├── 06-refactor.md                   (2.5 KB)
│   ├── 07-cognitive-load-inspector.md   (1.9 KB)
│   ├── 08-side-effect-tracker.md        (1.5 KB)
│   ├── 09-state-machine-inspector.md    (1.6 KB)
│   ├── 10-confidence-scoring.md         (1.6 KB)
│   ├── 11-memory-evolution.md           (2.2 KB)
│   ├── 12-commit-semantics.md           (2.0 KB)
│   ├── 13-knowledge-capture.md          (2.5 KB)
│   ├── 14-context-engineering.md        (11.5 KB)
│   ├── 15-security-engineering.md       (11.7 KB)
│   ├── 16-api-design.md                 (10.6 KB)
│   ├── 17-spec-compliance.md            (11.1 KB)
│   ├── 18-memory-management.md          (3.9 KB)
│   ├── 19-performance-profiling.md      (11.9 KB)
│   ├── 20-stitch-ui.md                  (3.8 KB)
│   ├── 21-mcp-audit.md                  (3.0 KB)
│   ├── 22-registry-synchronizer.md      (4.2 KB)
│   └── ui-ux-pro-max/                   (570.9 KB — optional design DB)
│       ├── SKILL.md                     (10.7 KB)
│       ├── data/
│       │   ├── charts.csv               (7.7 KB)
│       │   ├── colors.csv               (9.7 KB)
│       │   ├── icons.csv                (13.4 KB)
│       │   ├── landing.csv              (14.4 KB)
│       │   ├── products.csv             (29.8 KB)
│       │   ├── react-performance.csv    (14.8 KB)
│       │   ├── styles.csv               (96.6 KB)
│       │   ├── typography.csv           (31.9 KB)
│       │   ├── ui-reasoning.csv         (31.1 KB)
│       │   ├── ux-guidelines.csv        (18.8 KB)
│       │   ├── web-interface.csv        (7.5 KB)
│       │   └── stacks/
│       │       ├── astro.csv            (11.9 KB)
│       │       ├── flutter.csv          (10.5 KB)
│       │       ├── html-tailwind.csv    (11.4 KB)
│       │       ├── jetpack-compose.csv  (8.2 KB)
│       │       ├── nextjs.csv           (12.5 KB)
│       │       ├── nuxt-ui.csv          (14.0 KB)
│       │       ├── nuxtjs.csv           (16.5 KB)
│       │       ├── react-native.csv     (10.0 KB)
│       │       ├── react.csv            (13.0 KB)
│       │       ├── shadcn.csv           (15.9 KB)
│       │       ├── svelte.csv           (11.1 KB)
│       │       ├── swiftui.csv          (10.9 KB)
│       │       └── vue.csv              (11.1 KB)
│       └── scripts/
│           ├── core.py                  (10.2 KB)
│           ├── design_system.py         (43.6 KB)
│           ├── search.py                (5.5 KB)
│           └── __pycache__/             (81 KB — ARTIFACT)
└── workflows/
    ├── 01-scan.md                       (6.9 KB)
    ├── 02-onboard.md                    (2.3 KB)
    ├── 03-scaffold.md                   (3.1 KB)
    ├── 04-spec.md                       (4.7 KB)
    ├── 05-research.md                   (3.6 KB)
    ├── 06-plan-synthesis.md             (2.2 KB)
    ├── 07-knowledge-capture.md          (2.2 KB)
    ├── 08-build.md                      (5.7 KB)
    ├── 09-feature.md                    (3.8 KB)
    ├── 10-tdd.md                        (3.0 KB)
    ├── 11-debug.md                      (1.7 KB)
    ├── 12-performance.md                (2.5 KB)
    ├── 13-quality-gate.md               (1.4 KB)
    ├── 14-validate.md                   (4.5 KB)
    ├── 15-release.md                    (2.1 KB)
    ├── 16-sync-registry.md              (3.0 KB)
    ├── 17-auto-commit.md                (1.7 KB)
    ├── 18-readme-architect.md           (1.3 KB)
    └── 19-mcp-audit.md                  (1.6 KB)
```

---

## Per-Folder Analysis

### 1. `rules/` — Governance Layer (23 files, 42 KB)

**Classification: CORE — NEVER DELETE**

These are the non-negotiable behavioral laws of the system. Each file defines either a hard stop (verification gates, destructive operation safety) or an instinctive behavioral constraint (minimal footprint, context integrity, asset awareness).

**Contents:**
- 00–12: Governance rules with inconsistent `"Instinct:"` prefix in titles. No YAML frontmatter.
- 13–22: Governance rules with `"Rule:"` prefix. Have YAML frontmatter with `rule:` and `priority:` fields.

**What breaks if deleted:** The entire behavioral framework. No verification gates, no context integrity, no destructive-operation safety, no semantic versioning, no test-before-done enforcement. The system becomes unpredictable and dangerous.

**Anomalies:**
- Rules 00–14 lack YAML frontmatter (rules 15–22 have it) — formatting inconsistency.
- Rules 00–12 use `"Instinct:"` title prefix vs `"Rule:"` for 13+ — inconsistent naming.

---

### 2. `skills/` — Cognitive Layer (22 numbered + 1 sub-skill, 672 KB)

**Classification: CORE (numbered 01-22) + TOOL (ui-ux-pro-max/)**

These are the cognitive modules — how the agent reasons, researches, codes, reviews, secures, designs, and maintains itself.

**Numbered skills (01–22):**
- 01–13: Core reasoning skills (research, routing, decomposition, architecture, coding, refactoring, cognitive load, side-effects, state machines, confidence, memory, commits, knowledge capture)
- 14–17: Large imported reference skills (context engineering 11.5 KB, security 11.7 KB, API design 10.6 KB, spec compliance 11.1 KB) — sourced from community
- 18–22: Specialized skills (memory CLI, performance, Stitch UI, MCP audit, registry sync)

**`ui-ux-pro-max/` (570.9 KB):**
- Massive design reference database with 11 CSV datasets + 13 stack-specific CSVs
- Python search engine (BM25) and design system generator
- 3 scripts (core.py, design_system.py, search.py) + `__pycache__/`

**What breaks if deleted:**
- Without numbered skills: The agent loses all reasoning ability — cannot research, route, decompose, design, code, refactor, inspect, track, score, evolve memory, write commits, capture knowledge, engineer context, harden security, design APIs, check specs, manage memory, profile performance, use Stitch, audit MCPs, or sync registries.
- Without `ui-ux-pro-max/`: UI/UX workflow degrades. Otherwise, system runs fine.

**Anomalies:**
- Skills 14–17 are significantly larger (289–363 lines) vs 01–13 (34–86 lines). Community-sourced.
- `ui-ux-pro-max/` is NOT registered in `install-state.json` `installed_foundational_skills` array — missing registry entry.

---

### 3. `workflows/` — Pipeline Layer (19 files, 56 KB)

**Classification: CORE — NEVER DELETE**

These are the executable multi-step pipelines: scan → onboard → scaffold → spec → research → plan → capture → build → feature → TDD → debug → performance → quality gate → validate → release → sync → commit → readme → MCP audit.

**Contents:**
| # | File | Pipeline Name |
|---|------|---------------|
| 01 | `01-scan.md` | SCANNER — situational awareness |
| 02 | `02-onboard.md` | ONBOARD PROJECT — legacy analysis |
| 03 | `03-scaffold.md` | SCAFFOLD ASSETS — project init |
| 04 | `04-spec.md` | SPEC DISCOVERY |
| 05 | `05-research.md` | PARALLEL RESEARCH |
| 06 | `06-plan-synthesis.md` | MULTI PLAN SYNTHESIS |
| 07 | `07-knowledge-capture.md` | KNOWLEDGE CAPTURE |
| 08 | `08-build.md` | BUILD APP |
| 09 | `09-feature.md` | FEATURE DEVELOPMENT |
| 10 | `10-tdd.md` | TDD — Red-Green-Refactor |
| 11 | `11-debug.md` | DEBUG SESSION |
| 12 | `12-performance.md` | PERFORMANCE |
| 13 | `13-quality-gate.md` | QUALITY GATE |
| 14 | `14-validate.md` | CROSS AGENT VALIDATOR |
| 15 | `15-release.md` | RELEASE PROJECT |
| 16 | `16-sync-registry.md` | SYNC REGISTRY |
| 17 | `17-auto-commit.md` | AUTO COMMIT |
| 18 | `18-readme-architect.md` | README ARCHITECT |
| 19 | `19-mcp-audit.md` | MCP AUDIT |

**What breaks if deleted:** The entire pipeline orchestration. No scanning, building, testing, releasing, or maintenance.

---

### 4. `instincts/` — Soft Patterns (6 files + README, 6 KB)

**Classification: CORE — avoid deleting**

Probabilistic behavioral nudges that fire at boot. Not hard halts (like rules) but warnings/guidance.

| # | File | Pattern |
|---|------|---------|
| 01 | `01-minimal-footprint.md` | Smallest change that solves the problem |
| 02 | `02-verification-before-confidence.md` | Never assert without verifying |
| 03 | `03-user-intent-preservation.md` | Serve what user MEANS, not just says |
| 04 | `04-graceful-degradation.md` | Keep working when part fails |
| 05 | `05-commercial-quality-standard.md` | Production-ready output |
| 06 | `06-asset-pruning.md` | Propose deletion of unused assets |

**What breaks if deleted:** System loses its "second brain" of learned patterns. Would still function but makes more mistakes. This is the "softest" layer.

---

### 5. `mcps/` — MCP Documentation (6 server docs + README, 2 KB)

**Classification: CONFIG — SAFE TO DELETE**

Documentation-only files describing MCP server integrations. The actual server configurations live in `.mcp.json` at the project root.

| File | Server | Size |
|------|--------|------|
| `21st-dev-magic.md` | UI component generator (21st.dev) | 265 B |
| `figma-remote.md` | Figma design interface | 212 B |
| `mongodb.md` | MongoDB database queries | 182 B |
| `playwright.md` | Browser automation/testing | 190 B |
| `StitchMCP.md` | UI design system generator | 168 B |
| `supabase.md` | Supabase project interface | 206 B |

**What breaks if deleted:** MCP server documentation is lost. The servers themselves continue working (configured in `.mcp.json`). Workflow `19-mcp-audit` and skill `21-mcp-audit` lose their documentation source.

**Regenerable?** Yes — from `.mcp.json` + running MCP audit workflow.

---

### 6. `scripts/` — Automation Engines (7 files + `__pycache__/`, 98 KB)

**Classification: TOOL — scripts are essential, `__pycache__/` is ARTIFACT**

| File | Language | Purpose | Lines | Size |
|------|----------|---------|-------|------|
| `sync_registry.py` | Python | **Central engine** — drift detection, version bump, §13 regen, README/License sync | 644 | 27.8 KB |
| `detect_root.py` | Python | Root detection (walk up from cwd) — imported by all other Python scripts | 241 | 9.3 KB |
| `deep_scan_engine.py` | Python | Deep project scanning — drift detection, root pollution, version consistency | 196 | 7.7 KB |
| `readme_architect.py` | Python | Auto-generate README.md from .agent/ structure | 199 | 7.5 KB |
| `sanitize_frontmatter.py` | Python | Fix YAML frontmatter in all 19 workflow files | 181 | 6.1 KB |
| `bootstrap.js` | JavaScript | Dynamic root detection for Node.js environments | 176 | 6.1 KB |
| `upgrade_project.py` | Python | Copy .agent/ and .claude/ to a target project | 90 | 3.4 KB |

**Import graph:**
```
sync_registry.py ──imports──► detect_root.py
readme_architect.py ──imports──► detect_root.py
sanitize_frontmatter.py ──imports──► detect_root.py
upgrade_project.py ──imports──► detect_root.py
deep_scan_engine.py ──optionally imports──► detect_root.py
```

**What breaks if deleted:**
- Without `sync_registry.py`: No drift detection, no version bumps, no changelog updates, no README/License sync.
- Without `detect_root.py`: All other Python scripts fail (they import it).
- Without `bootstrap.js`: Node.js environments lose root detection.
- Without `readme_architect.py`: Workflow 18 fails.
- Without `deep_scan_engine.py`: Scanner workflow (01) loses its introspection engine.

**`__pycache__/` (32.7 KB):** ARTIFACT — auto-regenerated on next Python run. Safe to delete.

---

### 7. `.agents/skills/` — Agent Personas (23 agents, 85 KB)

**Classification: CORE — individual agents removable if capability unneeded**

Each agent directory contains `SKILL.md` (primary definition) and `agents/openai.yaml` (OpenAI-compatible persona definition). These are the named identities that the system invokes for specific tasks.

| # | Agent | Purpose |
|---|-------|---------|
| 01 | deep-scan | Full project mapping and situational awareness |
| 02 | failure-predictor | Pre-execution bug prediction |
| 03 | ask | Quick, precise answers |
| 04 | planner | Strategic breakdown into phased roadmaps |
| 05 | synthesizer | Multi-plan reconciliation into single strategy |
| 06 | tdd-guide | Red-Green-Refactor enforcement |
| 07 | python-agent | Python development specialization |
| 08 | rust-agent | Rust development specialization |
| 09 | jsts-agent | JS/TS development specialization |
| 10 | c-agent | C development specialization |
| 11 | go-agent | Go development specialization |
| 12 | antibug | Advanced bug detection |
| 13 | web-aesthetics | Premium UI/UX design |
| 14 | scientific-writing | Physics dissertations, academic writing |
| 15 | latex-bib-manager | LaTeX bibliography management |
| 16 | readme-architect | README.md generation |
| 17 | market-evaluator | Market value estimation |
| 18 | commercial-license | License generation |
| 19 | git-commit-author | Atomic commit generation |
| 20 | code-reviewer | Five-axis code review |
| 21 | security-auditor | Vulnerability detection |
| 22 | test-engineer | Test strategy and writing |
| 23 | mcp-auditor | MCP capability mapping |

**Anomaly: `23-mcp-auditor` is missing `agents/openai.yaml`** — the only agent without it. Cannot be invoked as an OpenAI-compatible persona. Likely a partially set up agent.

---

### 8. `aether-agent-install-state.json` (5.7 KB)

**Classification: CORE — NEVER DELETE**

The canonical manifest. A JSON file listing every installed component: 23 rules, 22 foundational skills, 19 workflows, 23 agent personas, 6 instincts, 15 commands, 3 specialist personas, 6 MCP servers. Tracks version, release date, changelog, and last-updated timestamp.

**What breaks if deleted:** `sync_registry.py` immediately reports "MISSING install-state.json" and refuses to synchronize. Workflow 16, skill 22, and rule 14 all depend on this file as the source of truth.

**Regenerable?** Yes, via `sync_registry.py --regen-section13`, but version history and changelog would need to be preserved from AETHER.md.

---

## Safe-to-Delete Summary

| Item | Size | Type | Reason |
|------|------|------|--------|
| `scripts/__pycache__/` | 32.7 KB | ARTIFACT | Python bytecode cache — auto-regenerated |
| `skills/ui-ux-pro-max/scripts/__pycache__/` | 81 KB | ARTIFACT | Python bytecode cache — auto-regenerated |
| `mcps/*.md` (all 7 files) | 2.2 KB | CONFIG | Docs only — real config in root `.mcp.json` |
| `skills/ui-ux-pro-max/` (entire directory) | 570.9 KB | TOOL | Optional UI design reference DB — not core |

**Total reclaimable:** ~687 KB

---

## Issues Found

| # | Issue | Location | Severity |
|---|-------|----------|----------|
| 1 | `23-mcp-auditor` missing `agents/openai.yaml` | `.agent/.agents/skills/23-mcp-auditor/` | **MEDIUM** — agent is "headless" |
| 2 | Rules 00–14 have no YAML frontmatter (rules 15–22 do) | `rules/` | LOW — cosmetic inconsistency |
| 3 | Rules 00–12 use `"Instinct:"` title prefix vs `"Rule:"` for 13+ | `rules/` | LOW — confusing naming |
| 4 | `ui-ux-pro-max/` not registered in `install-state.json` | `skills/ui-ux-pro-max/` | MEDIUM — registry drift |
| 5 | `antigravity-agent-install-state.json` referenced but absent | Referenced in rules/scripts | LOW — legacy mirror |
