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

Skills in this category turn high-level feature requests and Category A discovery anchors into **unambiguous architectural contracts, locked decisions, multi-variation plans, synthesized roadmaps, and safe atomic task executions** before any code is generated.

### Approved & Operational Skills (6-Skill Pipeline)

#### `B01-grill-me` — Architectural & Requirements Interrogator
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/B01-grill-me/`
* **Aliases**: `grill-me`, `requirements-grill`, `decision-interviewer`, `elia5-interrogator`
* **Role**: Deep pre-planning interrogator. Systematically traverses a 4-Axis Decision Tree (UX/Behavior, Data Model, Edge Cases/Failures, Scope Fences) using interactive multiple-choice options with `(Recommended)` choices. Integrates a **Dual Clarification Safety Hatch**: users can type `/ask` in the write-in box for technical trade-off breakdowns, or `/ask ELIA5` for zero-jargon real-world analogies before deciding.
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
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:DECISION_RECORD -->` block for `B02-planner`.
* **Workflow Connections**: Positioned as the front-gate of Category B, bridging Discovery and Planning. Feeds locked decisions directly into `B02-planner`.

---

#### `B02-planner` — Strategic Architectural Planner with Variations
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/B02-planner/`
* **Aliases**: `planner`, `strategy-planner`, `architectural-planner`, `plan-variants`
* **Role**: Strategic architectural planner. Enforces the **Multi-Variation Mandate**: formulates 2–3 distinct architectural approaches (Variation Alpha: Lean/Minimalist, Variation Beta: Idiomatic/Modular, Variation Gamma: Enterprise/Scalable) and evaluates them using objective trade-off scorecards (Velocity, Maintainability, Risk, Blast Radius).
* **Has Scripts**: **Yes** (`scripts/plan_comparator.py` — zero external dependencies, <20ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/B02-planner/
  ├── SKILL.md                  # Planning protocol & variation comparison standard
  ├── scripts/
  │   └── plan_comparator.py   # Static variation parser & trade-off scorecard generator
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: `DECISION_RECORD` from `B01-grill-me` + discovery anchors.
* **Output Modes**:
  1. *Standalone*: Multi-variant architectural proposal with trade-off comparison matrix.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:PLAN_VARIATIONS -->` block for `B03-spec-architect`.
* **Workflow Connections**: Bridges requirements interrogation into concrete architectural variations. Hands off to `B03-spec-architect`.

---

#### `B03-spec-architect` — Formal Technical Specification & Contract Engine
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/B03-spec-architect/`
* **Aliases**: `spec-architect`, `spec-generator`, `contract-architect`, `specification`
* **Role**: Formal contract engine. Solidifies chosen strategies into binding technical specifications (`SPEC.md`). Enforces the **5 Specification Pillars**: Acceptance Criteria (Given/When/Then), Data Models & Schemas, API & Interface Signatures, State Machine & Lifecycle Transitions, and Error Taxonomy & Recovery.
* **Has Scripts**: **Yes** (`scripts/validate_spec.py` — zero external dependencies, <30ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/B03-spec-architect/
  ├── SKILL.md                  # Specification protocol & 5-pillar contract standard
  ├── scripts/
  │   └── validate_spec.py     # Static specification auditor & portability validator
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Selected variation from `B02-planner` + `DECISION_RECORD` from `B01-grill-me`.
* **Output Modes**:
  1. *Standalone*: Formal `SPEC.md` document with schema definitions, state machines, and error tables.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:SYSTEM_SPEC -->` block for `B04-plan-synthesizer` and `B05-task-executor`.
* **Workflow Connections**: Translates architectural intent into unambiguous technical contracts. Feeds into `B04-plan-synthesizer`.

---

#### `B04-plan-synthesizer` — Multi-Plan & User-Idea Synthesis Engine
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/B04-plan-synthesizer/`
* **Aliases**: `plan-synthesizer`, `idea-synthesizer`, `strategy-synthesizer`, `synthesizer`
* **Role**: Multi-input reconciliation engine. Synthesizes competing agent proposals, conflicting architectural strategies, and diverse brainstorming ideas submitted by the user. Identifies baseline consensus, isolates clashes, and reconciles trade-offs into a single, unified, conflict-free Golden Plan.
* **Has Scripts**: **Yes** (`scripts/synthesize_plans.py` — zero external dependencies, <30ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/B04-plan-synthesizer/
  ├── SKILL.md                  # Synthesis protocol & multi-intake reconciliation rules
  ├── scripts/
  │   └── synthesize_plans.py  # Static conflict detector & consensus synthesizer
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Multiple agent plan variations from `B02-planner` AND/OR multiple ideas/wishlists from the user.
* **Output Modes**:
  1. *Standalone*: Synthesis Report detailing Consensus, Clashes, and Unified Golden Strategy.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:SYNTHESIZED_PLAN -->` block for `B05-task-executor`.
* **Workflow Connections**: Merges all divergent ideas into a single coherent plan before task decomposition. Feeds into `B05-task-executor`.

---

#### `B05-task-executor` — Atomic Task Decomposer & Execution Engine
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/B05-task-executor/`
* **Aliases**: `task-executor`, `task-planner`, `decomposer`, `execution-engine`, `roadmap-architect`
* **Role**: Strategic task decomposer and active execution tracker. Converts synthesized golden plans into phased, atomic roadmaps. Enforces the **Low Cognitive Load Protocol** (≤2 files touched per task, <50 lines changed per step) to eliminate AI hallucinations. Tracks dynamic task progress states (`[ ]` ➔ `[-]` ➔ `[x]`) and validates Definitions of Done before advancing phases.
* **Has Scripts**: **Yes** (`scripts/task_executor.py` and `scripts/plan_linter.py` — zero external dependencies, <20ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/B05-task-executor/
  ├── SKILL.md                  # Decomposition protocol & cognitive load rules
  ├── scripts/
  │   ├── task_executor.py     # Execution engine, state tracker & progress calculator
  │   └── plan_linter.py       # Static plan linter & cognitive load validator
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: `SYNTHESIZED_PLAN` from `B04-plan-synthesizer` + `SYSTEM_SPEC` from `B03-spec-architect`.
* **Output Modes**:
  1. *Standalone*: Structured Markdown Execution Roadmap with progressive task check-boxes and verifiable DoD gates.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:TASK_ROADMAP -->` block for `B06-failure-predictor` and Category C.
* **Workflow Connections**: Positioned between plan synthesis and failure prediction. Hands off directly to `B06-failure-predictor`.

---

#### `B06-failure-predictor` — Pre-Flight Risk & Failure Predictor
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/B06-failure-predictor/`
* **Aliases**: `failure-predictor`, `immune-gate`, `risk-assessor`, `predict-failures`
* **Role**: Pre-flight immune system and risk gate. Proactively audits proposed code edits, plans, and file modifications against blast-radius impact (`A04-dependency-mapper`), database schema constraints (`A06-schema-scanner`), and architectural anti-patterns (unhandled network timeouts, unbounded queries, race conditions). Assigns a deterministic 5-level risk score and required verification gate.
* **Has Scripts**: **Yes** (`scripts/scan_risks.py` — zero external dependencies, <30ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/B06-failure-predictor/
  ├── SKILL.md                  # Pre-flight audit protocol & risk gating rules
  ├── scripts/
  │   └── scan_risks.py         # Static risk pattern scanner & blast-radius calculator
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Target file path, proposed code diff, or `TASK_ROADMAP` from `B05-task-executor`.
* **Output Modes**:
  1. *Standalone*: Pre-Flight Failure Prediction Report with Risk Score, identified anti-patterns, and required verification gate.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:FAILURE_PREDICTION -->` block for Category C (Implementation) and Category D (Test Engineer).
* **Workflow Connections**: Positioned directly between `B05-task-executor` and Category C (Implementation). Serves as the pre-execution quality gate preventing regressions and runtime crashes.

---

## 4. Category C: Build & Implementation Skills

Skills in this category execute atomic code implementation, language-specific engineering, and surgical refactoring. They turn roadmaps from `B05-task-executor` and specifications from `B03-spec-architect` into robust, production-ready code with zero regressions.

### Approved & Operational Skills

#### `C01-code-builder` — Atomic Code Implementation Engine
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/C01-code-builder/`
* **Aliases**: `code-builder`, `builder`, `implementer`, `atomic-coder`, `feature-builder`
* **Role**: The core hands-on code implementation engine. Executes atomic tasks from `B05-task-executor` with strict adherence to the **Atomic Edit Protocol** (<=2 files touched, <50 lines per edit). Preserves existing comments, docstrings, and context. Enforces immediate Definition of Done verification commands before advancing roadmap states.
* **Has Scripts**: **Yes** (`scripts/diff_guard.py` — zero external dependencies, <20ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/C01-code-builder/
  ├── SKILL.md                  # Atomic implementation protocol & surgical edit rules
  ├── scripts/
  │   └── diff_guard.py         # Static diff analyzer & cognitive load monitor
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: `TASK_ROADMAP` from `B05-task-executor`, `SYSTEM_SPEC` from `B03-spec-architect`, and `FAILURE_PREDICTION` from `B06-failure-predictor`.
* **Output Modes**:
  1. *Standalone*: Surgical code modifications with bracket balance sanity checks.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:CODE_IMPLEMENTATION -->` block for Category D (Test Engineer) and Category E (Antibug).
* **Workflow Connections**: Positioned directly after `B06-failure-predictor`. Executes code modifications and hands off to Category D for test coverage and Category E for bug hunting.

---

#### `C02-refactor-pro` — Surgical Behavior-Preserving Refactoring Engine
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/C02-refactor-pro/`
* **Aliases**: `refactor-pro`, `refactorer`, `code-cleaner`, `dead-code-remover`, `modernizer`
* **Role**: Surgical behavior-preserving refactoring engine. Eliminates technical debt, unreferenced imports, dead constants, and obsolete comments without breaking public exports, function signatures, or introducing regressions. Enforces the **Green-Before, Green-After** rule (all existing tests must pass before and after the refactoring).
* **Has Scripts**: **Yes** (`scripts/dead_code_finder.py` — zero external dependencies, <30ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/C02-refactor-pro/
  ├── SKILL.md                  # Refactoring protocol & contract invariance rules
  ├── scripts/
  │   └── dead_code_finder.py   # Static unused import & dead code scanner
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Target source file or module to refactor + existing test suite.
* **Output Modes**:
  1. *Standalone*: Cleaned code with reduced cognitive complexity and pruned dead imports.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:REFACTOR_REPORT -->` block detailing debt eliminated and verification status.
* **Workflow Connections**: Runs in Category C during implementation or dedicated debt-cleanup phases. Coordinates with Category D (Test Engineer) to verify zero behavioral regressions.

---

#### `C03-polyglot-engine` — Multi-Language Idiomatic Code Specialist
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/C03-polyglot-engine/`
* **Aliases**: `polyglot-engine`, `language-specialist`, `idiomatic-code`, `code-standards`, `polyglot`
* **Role**: Multi-language idiomatic code specialist and conventions auditor. Enforces ecosystem-native paradigms across TypeScript, Python, Go, Rust, and SQL (strict typing, error wrapping, ownership idioms, parameterized queries). Eliminates non-idiomatic translations and unapproved external dependencies.
* **Has Scripts**: **Yes** (`scripts/idiom_checker.py` — zero external dependencies, <25ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/C03-polyglot-engine/
  ├── SKILL.md                  # Language conventions & idiomatic coding rules
  ├── scripts/
  │   └── idiom_checker.py      # Multi-language static idiom & convention auditor
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Target source file or code snippet in TypeScript, Python, Go, Rust, or SQL.
* **Output Modes**:
  1. *Standalone*: Idiomatic quality score (0–100) and actionable anti-idiom warnings.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:IDIOMATIC_VERIFICATION -->` block for Category D and Category E.
* **Workflow Connections**: Works within Category C alongside `C01-code-builder` and `C02-refactor-pro` to ensure generated or refactored code meets ecosystem-native standards before hand-off to testing.

---

## 5. Category D: Test & Quality Skills

Skills in this category enforce test-driven development, edge-case generation, regression prevention, and test suite health. They guarantee that production code is backed by verifiable, automated tests.

### Approved & Operational Skills

#### `D01-tdd-architect` — Disciplined Red-Green-Refactor Orchestrator
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/D01-tdd-architect/`
* **Aliases**: `tdd-architect`, `tdd-guard`, `test-driven-dev`, `test-engineer`, `red-green-refactor`
* **Role**: Disciplined TDD orchestrator. Enforces the strict **Red-Green-Refactor Cycle**: authors focused, isolated unit tests first, confirms expected failure (Red), oversees minimal implementation until green (Green), and safeguards test suite stability during refactoring.
* **Has Scripts**: **Yes** (`scripts/tdd_guard.py` — zero external dependencies, <25ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/D01-tdd-architect/
  ├── SKILL.md                  # TDD protocol & Red-Green-Refactor standards
  ├── scripts/
  │   └── tdd_guard.py          # Static assertion density & test health auditor
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Requirements from `B03-spec-architect` + target feature/module.
* **Output Modes**:
  1. *Standalone*: Isolated unit/integration test files with healthy assertion density.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:TDD_CYCLE -->` block verifying Red, Green, and Refactor milestones.
* **Workflow Connections**: Positioned at the entrypoint of Category D. Drives `C01-code-builder` and pairs with `C02-refactor-pro` to maintain green test suites.

---

#### `D02-edge-case-tester` — Adversarial Boundary & Edge-Case Prober
* **Status**: ✅ Approved & Operational
* **Location**: `.agents/skills/D02-edge-case-tester/`
* **Aliases**: `edge-case-tester`, `boundary-prober`, `fuzz-tester`, `unhappy-path-tester`, `stress-tester`
* **Role**: Adversarial boundary prober. Systematically stress-tests modules, models, and routes against the **5-Axis Boundary Matrix**: null/empty states, numeric extremes (overflows, precision loss), string/buffer extremes (10KB payloads, emojis, injection probes), concurrency races, and network degradation (429, 504, corrupted JSON).
* **Has Scripts**: **Yes** (`scripts/generate_edge_cases.py` — zero external dependencies, <25ms execution).
* **Self-Contained File Structure**:
  ```
  .agents/skills/D02-edge-case-tester/
  ├── SKILL.md                  # Boundary testing protocol & 5-axis fuzzing standard
  ├── scripts/
  │   └── generate_edge_cases.py # Static boundary matrix & payload generator
  └── agents/
      └── openai.yaml           # Antigravity/OpenAI UI display metadata
  ```
* **Input**: Target function signature, API route, or data model + risk limits from `B06-failure-predictor`.
* **Output Modes**:
  1. *Standalone*: Adversarial test cases and boundary-value test matrices.
  2. *Ensemble*: Machine-readable `<!-- CONTEXT_ANCHOR:EDGE_CASE_MATRIX -->` block for Category E (Review & Security).
* **Workflow Connections**: Follows `D01-tdd-architect` and `B06-failure-predictor`. Generates unhappy-path suites that prevent runtime crashes and unhandled exceptions.

---

## 6. Self-Contained Skill Packaging Standard

Every skill in `.agents/skills/` must strictly adhere to the **Independence Law**:
1. **No External Scripts**: A skill must never import or run scripts located outside its own folder (e.g. no calling `.agent/scripts/`).
2. **Self-Contained Assets**: Any helper scripts must live inside `<skill_name>/scripts/`. Any templates or assets must live inside `<skill_name>/resources/` or `<skill_name>/data/`.
3. **No Flawed Concatenation**: Zero escaped `\n` literals, zero broken frontmatter, and zero references to deleted legacy files.
4. **Portability**: A developer should be able to copy any single skill folder directly into another project's `.agents/skills/` directory, and it must work immediately.
