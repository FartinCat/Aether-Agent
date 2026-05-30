# MASTER PLAN 10 — Agent Structure Completeness Overhaul

**Feature:** Close 13 structural gaps across agent definitions, commands, validation, lifecycle, and observability

**Priority:** HIGH — infrastructure gaps block maintainability and scale

**Estimated effort:** 5–7 days

**Depends on:**
- MASTER_PLAN_00 (Typed Agent Contracts — schema validation patterns)
- MASTER_PLAN_09 (Telemetry Dashboard — for benchmark storage format)

**Unlocks:** Safe multi-contributor agent development, measurable quality, automated release

---

## Problem Statement

The Aether Agent system has 23 agent personas, 19 workflows, 22 foundational skills, 23 rules, 15 slash commands, and ~180+ files — but the *structure itself* has critical gaps that prevent scaling, maintenance, and quality assurance.

**Current gaps identified:**

| # | Gap | Severity | Category |
|---|---|---|---|
| 1 | Zero validation/schema layer — malformed agent definitions pass silently | Critical | Foundation |
| 2 | Zero testing infrastructure — no test runner, no `tests/` directory | Critical | Foundation |
| 3 | Zero CI/CD pipeline — no `.github/workflows/` for automated checks | Critical | Foundation |
| 4 | No contribution guide — no documented process for extending the system | High | Foundation |
| 5 | 14/23 agent personas lack a slash command — defined but inaccessible | High | Coverage |
| 6 | 10/19 workflows lack a slash command — no direct invocation path | Medium | Coverage |
| 7 | 3 redundant agent definition formats with no sync mechanism | Medium | Coverage |
| 8 | No agent template/scaffold — every new agent requires manual copy-paste | Medium | Maintainability |
| 9 | No agent lifecycle management — no deprecation/retirement policy | Medium | Maintainability |
| 10 | No dependency graph/topology map — relationships documented in prose only | Medium | Maintainability |
| 11 | No inter-agent communication protocol — hardcoded path invocation | Low | Observability |
| 12 | `ui-ux-pro-max` skill on disk but absent from `install-state.json` | Medium | Foundation |
| 13 | No performance benchmarks — no way to measure agent quality/speed | Low | Observability |

Without these foundations, the system cannot:
- Safely accept contributions from multiple developers
- Automatically detect broken agent definitions
- Provide a discoverable interface for all its agents
- Retire or replace agents without manual registry surgery
- Measure whether the system is improving over time

---

## Architecture Overview

```
Phase 1 ──► Foundation
  ├── 1a  .agent/schemas/*.schema.json
  ├── 1b  .agent/tests/*.py
  ├── 1c  .github/workflows/validate.yml
  └── 1d  fix install-state.json (register ui-ux-pro-max)

Phase 2 ──► Coverage
  ├── 2a  .claude/commands/agent.md (unified router)
  ├── 2b  .agents/skills/source-command-agent-router/SKILL.md
  ├── 2c  New workflow commands: /scaffold, /build, /release, /quality-gate
  └── 2d  Cross-ref fields in all SKILL.md frontmatter

Phase 3 ──► Maintainability
  ├── 3a  .agent/templates/new-agent/ + scaffold_agent.py
  ├── 3b  status field in SKILL.md frontmatter schema
  ├── 3c  CONTRIBUTING.md
  └── 3d  Format consolidation docs + validation

Phase 4 ──► Observability
  ├── 4a  graph_agent_deps.py → docs/agent-topology.md
  ├── 4b  benchmarks/ + benchmark_agents.py
  └── 4c  Inter-agent dispatch protocol documented in AETHER.md
```

---

## Phase 1 — Foundation (Days 1–2)

### 1a. Schema Validation Layer

**Problem:** No file validates that SKILL.md frontmatter, workflow YAML, or `install-state.json` follow a defined structure. A missing field, misspelled key, or broken YAML parse goes undetected.

**Solution:** Create `.agent/schemas/` with four JSON Schema files:

```
.agent/schemas/
├── skill.schema.json           # validates SKILL.md frontmatter (all agent personas)
├── workflow.schema.json        # validates workflow markdown frontmatter
├── command.schema.json         # validates .claude/commands/*.md frontmatter
└── install-state.schema.json   # validates aether-agent-install-state.json structure
```

Each schema defines:
- Required fields (name, description, version if applicable)
- Allowed values (status enum: active / beta / deprecated / retired)
- Type constraints (numeric prefix ranges, path existence)
- Cross-reference constraints (referenced agents/workflows must exist)

Create `.agent/scripts/validate_all.py` that:
1. Discovers every SKILL.md across `.agent/.agents/skills/` and `.agents/skills/`
2. Validates frontmatter against `skill.schema.json`
3. Validates every workflow in `.agent/workflows/` against `workflow.schema.json`
4. Validates every command in `.claude/commands/` against `command.schema.json`
5. Validates `install-state.json` against `install-state.schema.json`
6. Checks numeric prefix continuity (no gaps, no duplicates)
7. Checks that all referenced file paths actually exist
8. Reports errors with file:line references
9. Exits with code 1 on any failure

### 1b. Automated Definition Tests

**Problem:** Even with schema validation, there are semantic invariants that schemas cannot express (e.g., "every agent referenced in a workflow must exist", "every numeric prefix must be sequential without gaps").

**Solution:** Create `.agent/tests/` with a test suite:

```
.agent/tests/
├── test_schema_validation.py    # runs validate_all.py and checks output
├── test_prefix_sequence.py      # verifies 01..N are contiguous in each directory
├── test_cross_references.py     # every agent/skill/workflow ref resolves
├── test_registry_sync.py        # filesystem state matches install-state.json
├── test_yaml_parsing.py         # all openai.yaml files parse correctly
├── test_no_orphans.py           # no file on disk unregistered, no reg entry without file
└── test_naming_conventions.py   # kebab-case, no spaces, correct extensions
```

Use Python's `unittest` or `pytest` (align with existing Python scripts in `.agent/scripts/`). Tests must be runnable via a single command: `python -m pytest .agent/tests/`.

### 1c. CI/CD Pipeline

**Problem:** No automated checks run when the agent definitions are modified. Broken definitions can be committed and merged silently.

**Solution:** Create `.github/workflows/validate.yml`:

```yaml
name: Validate Agent Definitions
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pyyaml jsonschema
      - run: python .agent/scripts/validate_all.py
      - run: python -m pytest .agent/tests/
      - run: python .agent/scripts/sync_registry.py --check  # drift detection
```

### 1d. Register `ui-ux-pro-max`

**Problem:** The `ui-ux-pro-max` skill lives at `.agent/skills/ui-ux-pro-max/` but is absent from the `installed_foundational_skills` array in `aether-agent-install-state.json`.

**Solution:** Add the missing entry to `install-state.json`:

```json
{
  "id": "ui-ux-pro-max",
  "path": ".agent/skills/ui-ux-pro-max",
  "version": "1.0.0",
  "description": "Comprehensive UI/UX design skill with style data, color palettes, typography, and design system scripts"
}
```

---

## Phase 2 — Coverage (Days 2–4)

### 2a. Unified Agent-Router Command

**Problem:** 14 of 23 agent personas have no slash command. Creating 14 individual `.claude/commands/` files is maintenance-heavy. Users cannot discover agents they don't know exist.

**Solution:** Create a single `agent.md` command that dispatches to any agent persona by name:

**`.claude/commands/agent.md`**
```markdown
---
name: agent
description: "Invoke any agent persona by name. Usage: /agent <name> [query]"
---
Read `.agent/config/agent-router.json` to find the SKILL.md path for the requested agent name.
Load the SKILL.md. If a query is provided, append it as context. Execute the agent.
```

**`.agent/config/agent-router.json`**
```json
{
  "deep-scan":      ".agent/.agents/skills/01-deep-scan/SKILL.md",
  "failure-predictor": ".agent/.agents/skills/02-failure-predictor/SKILL.md",
  "ask":            ".agent/.agents/skills/03-ask/SKILL.md",
  "planner":        ".agent/.agents/skills/04-planner/SKILL.md",
  "synthesizer":    ".agent/.agents/skills/05-synthesizer/SKILL.md",
  "tdd-guide":      ".agent/.agents/skills/06-tdd-guide/SKILL.md",
  "python-agent":   ".agent/.agents/skills/07-python-agent/SKILL.md",
  "rust-agent":     ".agent/.agents/skills/08-rust-agent/SKILL.md",
  "jsts-agent":     ".agent/.agents/skills/09-jsts-agent/SKILL.md",
  "c-agent":        ".agent/.agents/skills/10-c-agent/SKILL.md",
  "go-agent":       ".agent/.agents/skills/11-go-agent/SKILL.md",
  "antibug":        ".agent/.agents/skills/12-antibug/SKILL.md",
  "web-aesthetics": ".agent/.agents/skills/13-web-aesthetics/SKILL.md",
  "scientific-writing": ".agent/.agents/skills/14-scientific-writing/SKILL.md",
  "latex-bib-manager":  ".agent/.agents/skills/15-latex-bib-manager/SKILL.md",
  "readme-architect":   ".agent/.agents/skills/16-readme-architect/SKILL.md",
  "market-evaluator":   ".agent/.agents/skills/17-market-evaluator/SKILL.md",
  "commercial-license": ".agent/.agents/skills/18-commercial-license/SKILL.md",
  "git-commit-author":  ".agent/.agents/skills/19-git-commit-author/SKILL.md",
  "code-reviewer":      ".agent/.agents/skills/20-code-reviewer/SKILL.md",
  "security-auditor":   ".agent/.agents/skills/21-security-auditor/SKILL.md",
  "test-engineer":      ".agent/.agents/skills/22-test-engineer/SKILL.md",
  "mcp-auditor":        ".agent/.agents/skills/23-mcp-auditor/SKILL.md"
}
```

This makes every agent discoverable and invocable while keeping the command surface minimal.

### 2b. Source-command for Router

**Problem:** The unified router command needs a skill-level implementation that slash commands can invoke.

**Solution:** Create `.agents/skills/source-command-agent-router/SKILL.md`:

```markdown
---
name: source-command-agent-router
description: "Dispatches agent invocation requests to the correct agent persona SKILL.md"
---
Receives an agent name from the `/agent` command.
Looks up .agent/config/agent-router.json for the SKILL.md path.
Validates that the target file exists.
Loads and executes the agent persona with any provided query context.
On invalid agent name, prints available agents list.
```

### 2c. Add Missing Workflow Commands

**Problem:** 10 of 19 workflows have no slash command. While the router covers agent personas, workflows are a separate concept and benefit from dedicated commands.

**Solution:** Create 4 high-value workflow commands (others remain accessible via direct workflow reference or future expansion):

| Command | Workflow | Rationale |
|---|---|---|
| `/scaffold` | `03-scaffold.md` | High-frequency — used when starting new projects |
| `/build` | `08-build.md` | Core development loop — build, compile, assemble |
| `/release` | `15-release.md` | Critical path — packaging and release management |
| `/quality-gate` | `13-quality-gate.md` | Decision point — go/no-go before ship |

Each command file follows the existing `.claude/commands/` pattern with clear frontmatter and invocation logic pointing to the workflow.

The remaining 6 workflows (research, plan-synthesis, knowledge-capture, feature, debug, performance) are accessible via the unified router's eventual workflow extension or remain documented in AETHER.md for direct use.

### 2d. Agent-Persona Cross-References

**Problem:** Agent definitions exist in isolation. There is no machine-readable way to know that "antibug works with deep-scan" or "code-reviewer feeds into ship".

**Solution:** Add three optional fields to the SKILL.md YAML frontmatter schema:

```yaml
related_agents: ["01-deep-scan", "12-antibug"]
related_workflows: ["10-tdd", "11-debug"]
related_skills: ["03-task-decomposition", "14-context-engineering"]
```

Then create `.agent/scripts/generate_cross_refs.py` that:
1. Reads all SKILL.md files
2. Extracts cross-reference fields
3. Builds `.agent/data/agent-cross-references.json` — a bidirectional adjacency list
4. Validates that all references resolve to existing entities

This file becomes the machine-readable source for the topology graph (Phase 4a).

---

## Phase 3 — Maintainability (Days 4–5)

### 3a. Agent Template + Scaffold

**Problem:** Creating a new agent requires manually copying an existing directory, editing frontmatter, updating numeric prefixes, and registering in `install-state.json`. Error-prone and inconsistent.

**Solution:** Create `.agent/templates/new-agent/`:

```
.agent/templates/new-agent/
├── SKILL.md           # template with {{placeholder}} variables
└── agents/
    └── openai.yaml    # template with matching placeholders
```

**`SKILL.md` template:**
```markdown
---
name: "{{agent_name}}"
description: "{{agent_description}}"
status: beta
related_agents: []
related_workflows: []
related_skills: []
---
{{agent_instructions}}
```

Create `.agent/scripts/scaffold_agent.py`:

```
python .agent/scripts/scaffold_agent.py --name "my-agent" --description "Does X"
```

This script:
1. Determines the next numeric prefix (e.g., `24` if current max is `23`)
2. Creates `.agent/.agents/skills/24-my-agent/SKILL.md` from template
3. Creates `.agent/.agents/skills/24-my-agent/agents/openai.yaml` from template
4. Adds the entry to `agent-router.json`
5. Adds the entry to `install-state.json` via the registry script
6. Reports the new agent path

### 3b. Lifecycle Status Field

**Problem:** No way to mark an agent as deprecated, beta, or retired. Old agents linger without warning. New agents cannot signal instability.

**Solution:** Define a `status` enum in `skill.schema.json`:

| Value | Meaning | Validate behavior |
|---|---|---|
| `active` | Fully supported, production-ready | Normal validation |
| `beta` | New, may change | Passes validation, prints warning |
| `deprecated` | Will be removed in future version | Passes validation, prints warning on every invocation |
| `retired` | Removed, kept for reference only | Validation warns; router refuses invocation |

Add optional fields:
```yaml
status: active
deprecated_by: "24-replacement-agent"   # only for deprecated
retired_date: "2026-12-01"              # only for retired
replaced_by: "24-replacement-agent"     # for any status change
```

The router command (2a) checks `status` before dispatching and warns/informs accordingly.

### 3c. Contribution Guide

**Problem:** No documentation tells a new developer how to add an agent, modify a workflow, or understand the system architecture.

**Solution:** Create `CONTRIBUTING.md` at repository root with sections:

1. **Architecture overview** — How the five layers interact (rules → skills → workflows → agents → commands)
2. **Adding a new agent** — Step-by-step using the scaffold tool
3. **Adding a new workflow** — Template and registration process
4. **Adding a new skill** — When to create a foundational skill vs agent persona
5. **Modifying an existing agent** — Updating SKILL.md, openai.yaml, and cross-refs
6. **Definition checklist** — Required fields, naming conventions, prefix rules
7. **Testing your changes** — Running validate_all.py and pytest
8. **Registry synchronization** — When and how to run sync_registry.py
9. **Deprecating/retiring an agent** — Lifecycle management steps

### 3d. Definition Format Consolidation

**Problem:** There are three parallel agent definition formats:
- `SKILL.md` (primary, all 23 agents)
- `agents/openai.yaml` (22 of 23 agents — secondary/legacy)
- `.claude/agents/*.md` (3 specialist personas — third format)

**Solution:** Document and enforce a single canonical flow:

```
Canonical definition: SKILL.md (in .agent/.agents/skills/<N>-<name>/)
├── Primary format — all agents MUST have this
├── Contains full instructions, schema, and metadata
│
├── agents/openai.yaml (RECOMMENDED — secondary)
│   └── OpenAI-compatible format, auto-generated from SKILL.md if possible
│
└── .claude/agents/*.md (DEPRECATED — do not add new ones)
    └── Existing 3 files kept for backward compatibility
    └── validate_all.py flags any new additions to this directory
```

Update `validate_all.py` to:
- Warn if an agent lacks `agents/openai.yaml` (non-fatal)
- Error if a new `.claude/agents/*.md` file is added

---

## Phase 4 — Observability (Days 5–7)

### 4a. Agent Dependency Graph

**Problem:** There is no visual or machine-readable topology showing how agents, skills, workflows, and commands relate. New contributors cannot trace "what calls what."

**Solution:** Create `.agent/scripts/graph_agent_deps.py` that:

1. Reads all SKILL.md frontmatter for `related_agents`, `related_workflows`, `related_skills` fields
2. Reads all workflow markdown frontmatter for `primary_agent`, `dependent_skills`, `trigger_commands`
3. Reads all command markdown frontmatter for `invokes_agent`, `invokes_workflow`
4. Generates `docs/agent-topology.md` containing:

**Mermaid graph:**
```mermaid
graph TD
  subgraph Agents
    A1[01-deep-scan]
    A12[12-antibug]
    A20[20-code-reviewer]
  end
  subgraph Workflows
    W1[01-scan]
    W13[13-quality-gate]
  end
  subgraph Commands
    C1[/scanner]
    C13[/quality-gate]
  end
  C1 --> W1 --> A1
  A1 -.-> A12
  C13 --> W13 --> A20
```

**Dependency tables:**
| Agent | Invoked By | Invokes | Related Skills |
|---|---|---|---|
| 01-deep-scan | `/scanner`, `/agent deep-scan` | — | 03-task-decomposition |
| 12-antibug | `/antibug`, `/agent antibug` | 01-deep-scan | 07-cognitive-load-inspector |

The graph should be auto-generated and re-generated on each run of `validate_all.py` to stay in sync.

### 4b. Performance Benchmarks

**Problem:** No way to measure whether agents are getting faster, more accurate, or more cost-effective over time.

**Solution:** Create an agent benchmarking framework:

```
benchmarks/
├── prompts/
│   ├── deep-scan.txt              # standard prompt for deep-scan
│   ├── code-reviewer.txt          # standard prompt for code-review
│   └── ...                        # one per active agent persona
└── results/
    └── (auto-generated JSONL files)
```

Create `.agent/scripts/benchmark_agents.py` that:

1. Reads a benchmark prompt for a given agent
2. Invokes the agent via the router
3. Measures: time-to-first-token, total completion time, output length (tokens/characters)
4. Records: date, agent version, model used, latency, output size
5. Appends to `benchmarks/results/<agent-name>.jsonl`

This produces a time-series dataset that MASTER_PLAN_09's telemetry dashboard can consume.

### 4c. Inter-Agent Dispatch Protocol

**Problem:** Agents invoke each other via hardcoded file paths in slash commands and SKILL.md files. There is no standardized invocation envelope.

**Solution:** Define a lightweight dispatch convention documented in `AETHER.md` §Agent Communication:

**Environment variables passed to every agent invocation:**
| Variable | Description |
|---|---|
| `AGENT_NAME` | Canonical name (e.g., `antibug`) |
| `AGENT_PATH` | Filesystem path to the agent's SKILL.md |
| `REQUEST_ID` | UUID for tracing the full invocation chain |
| `INPUT_FORMAT` | Format of the input context (`text`, `markdown`, `json`) |
| `OUTPUT_SCHEMA` | Path to the expected output schema (if any, from MASTER_PLAN_00) |
| `PARENT_REQUEST_ID` | The REQUEST_ID of the calling agent (for nesting) |

**Agent output envelope (recommended):**
```json
{
  "request_id": "uuid-123",
  "agent": "antibug",
  "status": "success",
  "output": "...",
  "metadata": {
    "tokens_in": 1500,
    "tokens_out": 200,
    "duration_ms": 4500
  }
}
```

Agents conforming to this protocol are "dispatch-compliant." The router command routes to non-compliant agents with a compatibility wrapper.

---

## Dependency Graph

```
Phase 1                               Phase 2                              Phase 3                              Phase 4
────────                               ────────                             ────────                             ────────

1a schema.json ─────┐                 2a router command ────┐              3a template ─────────┐             4a deps graph
                    │                                         │                                   │
1b tests ───────────┤                2b source-command ──────┤              3b lifecycle ────────┤             4b benchmarks
                    │                                         │                                   │
1c CI/CD ──────────┤                2c workflow commands ────┤              3c CONTRIBUTING.md ──┤             4c dispatch proto
                    │                                         │                                   │
1d register fix ───┘                2d cross-refs ───────────┘              3d format consolidation ┘

  ▲
  └─── All phases depend on Foundation (Phase 1) being correct first

Phase 4 can start in parallel with Phase 3 once Phase 2 is complete
```

---

## Acceptance Criteria

- [ ] `python .agent/scripts/validate_all.py` passes with zero errors on current codebase
- [ ] `python -m pytest .agent/tests/` — all tests pass
- [ ] GitHub Actions workflow runs on every push and PR, blocking merge on failure
- [ ] `install-state.json` passes its own schema and includes `ui-ux-pro-max`
- [ ] `/agent python-agent -- "write a Flask route"` invokes the Python agent persona
- [ ] `/agent failure-predictor -- "check this code"` invokes the failure predictor
- [ ] `/agent invalid-name` prints the list of available agents
- [ ] `/scaffold`, `/build`, `/release`, `/quality-gate` commands work
- [ ] `CONTRIBUTING.md` guides a new developer through adding an agent in under 10 minutes
- [ ] `docs/agent-topology.md` renders a complete, accurate dependency graph
- [ ] `scaffold_agent.py` creates a new agent with correct prefix, paths, and registry entry
- [ ] Deprecated agents print warnings on invocation; retired agents are blocked by router
- [ ] `benchmark_agents.py` produces valid JSONL output

---

## Risks and Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Adding schemas breaks existing definitions | Medium | Run `validate_all.py` first in dry-run mode; fix any existing violations before enforcing in CI |
| Router command conflicts with existing agent commands | Low | Router dispatches by name; existing commands (`/scanner`, `/antibug`, etc.) take priority and remain unchanged |
| Contributors ignore lifecycle fields | Medium | Schema validation enforces `status` as required; default is `active` |
| Benchmark tests consume real API costs | High | Benchmarks require explicit `--run` flag; dry-run mode validates setup without invocation |
| Migration of 23 SKILL.md files for cross-refs is tedious | High | Use a script to bulk-add empty `related_*: []` fields; authors fill them in over time |

---

## Out of Scope

- Creating individual slash commands for all 23 agents (router solves this more efficiently)
- Migrating `ui-ux-pro-max` out of `.agent/skills/` (only registration is missing, not relocation)
- Rewriting the existing 15 slash commands (they work; router is additive)
- Full event-bus implementation (dispatch protocol is lightweight convention, not infrastructure)
- Converting all agents to a single definition format (SKILL.md is canonical; others are secondary/deprecated)
