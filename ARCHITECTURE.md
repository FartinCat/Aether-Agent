# Antigravity Agent Architecture & Skill Registry

> Master architectural ledger for approved, self-contained skills in `.agents/skills/`.
> Only skills that have been audited, sanitized, made 100% self-contained, and verified are registered here.

---

## 1. Category Taxonomy

Skills are organized into functional execution categories using alphabetical prefixes. This ensures a clean, deterministic alphabetical sort order in the Antigravity IDE and Cursor skills menus:

| Prefix | Domain | Primary Purpose |
| :--- | :--- | :--- |
| **A** | **Scan & Discovery** | Situational awareness, repo typing, semantic inquiry, and dependency mapping. |
| **B** | **Plan & Specification** | Requirements breakdown, failure prediction, spec extraction, and synthesis. |
| **C** | **Build & Implementation** | Language specialists (Python, Rust, TS, Go, C), refactoring, and code generation. |
| **D** | **Test & Quality** | TDD enforcement, test writing, coverage audits, and edge-case testing. |
| **E** | **Review & Security** | Bug hunting (antibug), security auditing, and 5-axis code reviews. |
| **F** | **UI/UX & Aesthetics** | Modern design systems, palettes, typography, and micro-interactions (`ui-ux-pro-max`). |
| **G** | **Docs & Release** | Architecture docs, README generation, commit authoring, and licensing. |

---

## 2. Category A: Scan & Discovery Skills

Skills in this category are responsible for building **zero-trust situational awareness**. They never guess; they inspect, classify, extract evidence, and hand structured context anchors to downstream skills.

### Approved & Operational Skills

#### `A01-deep-scan` — Architectural Macro-Scanner
* **Status**: ✅ Approved & Tested
* **Location**: `.agents/skills/A01-deep-scan/`
* **Role**: Rapid, scale-aware repository landscape and architecture mapping.
* **Has Scripts**: **Yes** (`scripts/repo_fingerprint.py` — zero external dependencies, <50ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/A01-deep-scan/
  ├── SKILL.md                  # Adaptive 4-stage cognitive protocol
  ├── scripts/
  │   └── repo_fingerprint.py   # Pure standard library repository fingerprinter
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Any repository root path.
* **Output Modes**:
  1. *Standalone*: Human-readable Developer Architectural Brief.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:DEEP_SCAN -->` block.
* **Workflow Connections**: Feeds into `B` (Planner), `D` (Test Engineer), and `E` (Antibug).

---

#### `A02-ask` — Surgical Codebase Inquiry & Semantic Locator
* **Status**: ✅ Approved & Tested (Updated with ELIA5 Layman Mode)
* **Location**: `.agents/skills/A02-ask/`
* **Role**: Answers developer technical doubts with surgical accuracy and minimal noise. Locates functions, states, and endpoints without dumping large files into context. Includes the **ELIA5 (Explain Like I'm 5)** mode to translate technical concepts into simple real-world analogies.
* **Has Scripts**: **No** (Direct cognitive tool calls: exact grep search + focused slice reading).
* **Self-Contained File Structure**:
  ```
  .agents/skills/A02-ask/
  ├── SKILL.md                  # Semantic inquiry protocol, surgical reading rules & ELIA5 translation
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Specific technical question, symbol query, or `/ask ELIA5 <topic>`.
* **Output Modes**:
  1. *Standalone Technical*: Direct answer, clickable `[SymbolName](file:///path#Lxx-Lyy)` markdown link, and minimal code snippet.
  2. *Standalone ELIA5*: Jargon-free real-world analogy and practical trade-off breakdown.
  3. *Ensemble*: Targeted slice extraction for `B` (Planner) or `E` (Antibug).
* **Workflow Connections**: Consumes `A01-deep-scan` context anchors to target relevant subdirectories immediately; serves as the layman translation engine for `B01-grill-me`.

#### `A03-validator` — Evidence & Contradiction Validator
* **Status**: ✅ Approved & Tested
* **Location**: `.agents/skills/A03-validator/`
* **Aliases**: `evidence-validator`, `research-loop`
* **Role**: Pre-execution evidence grounding and contradiction validator. Audits user requests, specs, and proposed plans against active code and dependency manifests to eliminate hallucinations before work begins.
* **Has Scripts**: **No** (Direct cognitive tool calls: manifest checking, symbol verification, config parsing).
* **Self-Contained File Structure**:
  ```
  .agents/skills/A03-validator/
  ├── SKILL.md                  # Evidence validation protocol & contradiction audit
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: User prompt, proposed change, or architectural specification.
* **Output Modes**:
  1. *Standalone*: Structured Evidence Validation Report (Confirmed Facts, Contradictions, Gaps, Confidence Score).
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:VALIDATOR -->` block for `B` (Planner).
* **Workflow Connections**: Sits directly between `A01-deep-scan` and `Category B (Planner)` to guarantee bulletproof plan feasibility.

#### `A04-dependency-mapper` — Blast-Radius & Import Graph Scanner
* **Status**: ✅ Approved & Tested
* **Location**: `.agents/skills/A04-dependency-mapper/`
* **Aliases**: `blast-radius-scanner`, `import-graph`
* **Role**: AST-based import/export graph and blast-radius analyzer. Traces upstream consumers and downstream dependencies of any target file to prevent silent regressions during refactors.
* **Has Scripts**: **Yes** (`scripts/scan_imports.py` — zero external dependencies, <100ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/A04-dependency-mapper/
  ├── SKILL.md                  # Blast-radius protocol & refactoring guidelines
  ├── scripts/
  │   └── scan_imports.py       # Pure standard-library import & reverse-dependency crawler
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Target file path about to be modified or refactored.
* **Output Modes**:
  1. *Standalone*: Blast-Radius Report (Risk Tier, Consumer Files That Will Break, Downstream Dependencies, Circular Loops).
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:DEPENDENCY_MAP -->` block for `B` (Planner) and `E` (Antibug).
* **Workflow Connections**: Ingested by `Category B (Planner)` to scope multi-file atomic edits, and `Category E (Antibug)` to prevent regressions.

#### `A05-route-scanner` — URL, Page & Endpoint Scanner
* **Status**: ✅ Approved & Tested
* **Location**: `.agents/skills/A05-route-scanner/`
* **Aliases**: `endpoint-scanner`, `url-mapper`, `page-finder`
* **Role**: Automated web page and API route discovery scanner. Maps all frontend UI pages, Next.js app/pages routes, and backend API endpoints into a unified URL directory sheet.
* **Has Scripts**: **Yes** (`scripts/scan_routes.py` — zero external dependencies, <100ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/A05-route-scanner/
  ├── SKILL.md                  # Route scanning protocol & categorization guidelines
  ├── scripts/
  │   └── scan_routes.py        # Pure standard-library route & endpoint crawler
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Root project path or sub-application directory.
* **Output Modes**:
  1. *Standalone*: URL & Route Directory Sheet (UI Pages vs API Endpoints, HTTP methods, file:line links).
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:ROUTES -->` block for `B` (Planner) and `D` (Test Engineer).
* **Workflow Connections**: Ingested by `Category B (Planner)` to prevent route duplication, and `Category D (Test Engineer)` to write end-to-end and API integration tests.

#### `A06-schema-scanner` — Data Model & Database Schema Finder
* **Status**: ✅ Approved & Tested
* **Location**: `.agents/skills/A06-schema-scanner/`
* **Aliases**: `data-model-finder`, `model-scanner`, `schema-mapper`
* **Role**: Automated database schema and data model extractor. Discovers database tables, ORM models, field names, and data types across Prisma, SQL, Pydantic, SQLAlchemy, and Drizzle to eliminate hallucinated field names.
* **Has Scripts**: **Yes** (`scripts/scan_schemas.py` — zero external dependencies, <100ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/A06-schema-scanner/
  ├── SKILL.md                  # Schema discovery protocol & query safety guidelines
  ├── scripts/
  │   └── scan_schemas.py       # Pure standard-library schema & model extractor
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Root project path or sub-application directory.
* **Output Modes**:
  1. *Standalone*: Entity Blueprint Sheet (Models, Fields, Types, Relations, Casing Conventions).
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:SCHEMAS -->` block for `B` (Planner) and `C` (Implementer).
* **Workflow Connections**: Ingested by `Category B (Planner)` when designing database-backed features, and `Category C (Language Specialists)` to guarantee 100% field name accuracy without database crashes.

---

### Category A Suite Status: COMPLETE (6/6 Skills Approved)
All core Scan & Discovery capabilities are now fully operational, tested, and 100% self-contained.

*(Note: The **Pattern Hunter** concept for technical debt and secret leaks is reserved for **Category E: Review & Security** as a pre-commit quality audit tool).*

---

## 3. Category B: Plan & Specification Skills

Skills in this category turn high-level feature requests and Category A discovery anchors into **unambiguous architectural contracts, locked decisions, and safe atomic task breakdowns** before any code is generated.

### Approved & Operational Skills

#### `B01-grill-me` — Architectural & Requirements Interrogator
* **Status**: ✅ Approved & Tested
* **Location**: `.agents/skills/B01-grill-me/`
* **Aliases**: `grill-me`, `requirements-grill`, `decision-interviewer`, `elia5-interrogator`
* **Role**: Deep pre-planning interrogator. Systematically walks down a 4-Axis Decision Tree (UX/Behavior, Data Model, Edge Cases/Failures, Scope Fences) using interactive multiple-choice options with `(Recommended)` answers based on codebase findings. Integrates a **Dual Clarification Safety Hatch**: users can type `/ask` in the write-in box for deep technical trade-off breakdowns, or `/ask ELIA5` for simple, zero-jargon real-world analogies before making decisions.
* **Has Scripts**: **No** (Direct cognitive tool calls: interactive multiple choice + decision synthesis).
* **Self-Contained File Structure**:
  ```
  .agents/skills/B01-grill-me/
  ├── SKILL.md                  # 4-Axis decision tree & ELIA5 interview protocol
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: User feature prompt + Category A discovery anchors (`A01`–`A06`).
* **Output Modes**:
  1. *Interactive*: Progressive multiple-choice queries with ELIA5 layman explanations on demand.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:DECISION_RECORD -->` block for `B02-task-planner`.
* **Workflow Connections**: Positioned as the front-gate of Category B, bridging Discovery and Planning. Feeds locked decisions directly into `B02-task-planner`.

---

#### `B02-task-planner` — Strategic Task Decomposer & Roadmap Architect
* **Status**: ✅ Approved & Tested
* **Location**: `.agents/skills/B02-task-planner/`
* **Aliases**: `task-planner`, `decomposer`, `roadmap-architect`, `planner`
* **Role**: Strategic task decomposer. Converts high-level requirements and `B01-grill-me` decision records into phased, atomic roadmaps. Enforces the **Low Cognitive Load Protocol** (≤2 files touched per task, <50 lines changed per step) to eliminate AI hallucinations and context exhaustion. Includes a self-contained static plan linter.
* **Has Scripts**: **Yes** (`scripts/plan_linter.py` — zero external dependencies, <20ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/B02-task-planner/
  ├── SKILL.md                  # Decomposition protocol & cognitive load rules
  ├── scripts/
  │   └── plan_linter.py        # Static plan linter & cognitive load validator
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: `DECISION_RECORD` from `B01-grill-me` + discovery anchors (`A01`–`A06`).
* **Output Modes**:
  1. *Standalone*: Structured Markdown Implementation Plan (`PLAN.md`) with explicit phases, tasks, and Definitions of Done.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:TASK_PLAN -->` block for `B03-failure-predictor` and Category C.
* **Workflow Connections**: Sits directly between `B01-grill-me` and `B03-failure-predictor`. Ingests blast-radius data from `A04-dependency-mapper` to guarantee dependency-ordered updates.

---

## 4. Self-Contained Skill Packaging Standard

Every skill in `.agents/skills/` must strictly adhere to the **Independence Law**:
1. **No External Scripts**: A skill must never import or run scripts located outside its own folder (e.g. no calling `.agent/scripts/`).
2. **Self-Contained Assets**: Any helper scripts must live inside `<skill_name>/scripts/`. Any templates or assets must live inside `<skill_name>/resources/` or `<skill_name>/data/`.
3. **No Flawed Concatenation**: Zero escaped `\n` literals, zero broken frontmatter, and zero references to deleted legacy files.
4. **Portability**: A developer should be able to copy any single skill folder directly into another project's `.agents/skills/` directory, and it must work immediately.
