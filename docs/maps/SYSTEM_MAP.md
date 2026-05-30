# 🗺️ Aether Agent System Map

> How this AI Operating System works — every file organized by **what it does**, not where it lives.

## How to Read This

| Icon | Meaning |
|------|---------|
| 📏 | Rule (must-follow law) |
| 🧠 | Skill (thinking technique) |
| ⚡ | Workflow (executable pipeline) |
| 🤖 | Agent (specialist persona) |
| 📄 | Script (automation engine) |
| 🔌 | Command (slash command entry point) |
| 💡 | Instinct (behavioral pattern) |

---

## ⚙️ Step 0: BOOT — The OS Wakes Up

These files load in order every session. They define identity, rules, instincts, and memory.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/03-ask/SKILL.md` | 📄 | Quick, precise answers to doubts with medium context. Works in tandem with de... |
| `.agent/instincts/01-minimal-footprint.md` | 💡 | Instinct: Minimal Footprint |
| `.agent/instincts/02-verification-before-confidence.md` | 💡 | Instinct: Verification Before Confidence |
| `.agent/instincts/03-user-intent-preservation.md` | 💡 | Instinct: User Intent Preservation |
| `.agent/instincts/04-graceful-degradation.md` | 💡 | Instinct: Graceful Degradation |
| `.agent/instincts/05-commercial-quality-standard.md` | 💡 | Instinct: Commercial Quality Standard |
| `.agent/instincts/06-asset-pruning.md` | 💡 | Instinct: Asset Pruning |
| `.agent/rules/00-workflow-orchestration.md` | 📏 | Instinct: System-Wide Orchestration |
| `.agent/rules/01-core.md` | 📏 | Core Architectural Instincts |
| `.agent/rules/02-integrity.md` | 📏 | Universal Integrity Rules (Hard Stops) |
| `.agent/rules/03-instincts.md` | 📏 | Universal Instincts Layer |
| `.agent/rules/04-verification-gates.md` | 📏 | Verification Gate System |
| `.agent/rules/05-context-integrity.md` | 📏 | Context Integrity Rules |
| `.agent/rules/06-context-memory.md` | 📏 | Instinct: Session Context Memory |
| `.agent/rules/07-metadata-awareness.md` | 📏 | Rule: Metadata Awareness |
| `.agent/rules/12-silent-ingest.md` | 📏 | Instinct: Silent Ingest |
| `.agent/rules/13-self-improvement.md` | 📏 | Rule: Self-Improvement & Adaptive Evolution |
| `.agent/rules/15-context-engine.md` | 📏 | Rule 15: Context Engine — "Think in Code" |
| `.agent/rules/17-agent-composition.md` | 📏 | Rule 17: Agent Composition and Orchestration |
| `.agent/rules/18-knowledge-persistence.md` | 📏 | Rule 18: Knowledge Persistence |
| `.agent/rules/21-destructive-operation-safety.md` | 📏 | Rule 21: Destructive Operation Safety — Authorization Gate |
| `.agent/scripts/bootstrap.js` | 📄 | (no description) |
| `.agent/scripts/detect_root.py` | 📄 | (no description) |
| `.agent/skills/02-language-routing.md` | 🧠 | Skill for language-routing |
| `.agent/skills/10-confidence-scoring.md` | 🧠 | Skill for confidence-scoring |
| `.agent/skills/11-memory-evolution.md` | 🧠 | Skill for memory-evolution |
| `.agent/skills/14-context-engineering.md` | 🧠 | Optimizes agent context setup. Use when starting a new session, when agent ou... |
| `.agent/skills/18-memory-management.md` | 🧠 | Use AI DevKit memory via CLI commands. Search before non-trivial work, store ... |
| `.claude/commands/ag-ask.md` | 🔌 | Ask a question about the current project's codebase via the antigravity knowl... |
| `.claude/commands/ag-refresh.md` | 🔌 | Rebuild the antigravity project knowledge base after significant changes. / 在... |

## 🔍 Step 1: SCAN — Understand the Project

When you run /scanner or ask "what's in this project?", these files activate.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/01-deep-scan/SKILL.md` | 📄 | Comprehensive situational awareness agent. Maps the project repository struct... |
| `.agent/scripts/deep_scan_engine.py` | 📄 | (no description) |
| `.agent/skills/01-research-loop.md` | 🧠 | Skill for research-loop |
| `.agent/workflows/01-scan.md` | ⚡ | Build situational awareness and map directories. |
| `.agents/skills/source-command-scanner/SKILL.md` | 🤖 | Map the entire repository before any work begins — project-aware deep scan |
| `.claude/commands/scanner.md` | 🔌 | Map the entire repository before any work begins — project-aware deep scan |

## 📋 Step 2: PLAN — Decide What to Do

Spec writing, task breakdown, multi-plan synthesis.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/04-planner/SKILL.md` | 📄 | Strategic breakdown of complex requirements into phased, dependency-aware imp... |
| `.agent/.agents/skills/05-synthesizer/SKILL.md` | 📄 | Ensemble Plan Evaluation and Master Synthesis agent. Reads multiple AI plans ... |
| `.agent/rules/16-sdd-lifecycle.md` | 📏 | Rule 16: Spec-Driven Development Lifecycle |
| `.agent/skills/03-task-decomposition.md` | 🧠 | Skill for task-decomposition |
| `.agent/skills/17-spec-compliance.md` | 🧠 | Verifies code implements exactly what documentation specifies for blockchain ... |
| `.agent/workflows/04-spec.md` | ⚡ | Functional and technical spec extraction. |
| `.agent/workflows/05-research.md` | ⚡ | Execute parallel technical research paths. |
| `.agent/workflows/06-plan-synthesis.md` | ⚡ | Merge competing AI strategies into one plan. |
| `.agent/workflows/07-knowledge-capture.md` | ⚡ | Distill project insights into persistent KIs. |
| `.agents/skills/source-command-plan/SKILL.md` | 🤖 | Break work into small verifiable tasks with acceptance criteria and dependenc... |
| `.agents/skills/source-command-planner/SKILL.md` | 🤖 | Create a strategic implementation plan — single-agent version of /plan |
| `.agents/skills/source-command-spec/SKILL.md` | 🤖 | Start spec-driven development — write a structured specification before writi... |
| `.claude/commands/plan.md` | 🔌 | Break work into small verifiable tasks with acceptance criteria and dependenc... |
| `.claude/commands/planner.md` | 🔌 | Create a strategic implementation plan — single-agent version of /plan |
| `.claude/commands/spec.md` | 🔌 | Start spec-driven development — write a structured specification before writi... |

## 🔧 Step 3: BUILD — Write Code

Language specialists, code generation, API design, refactoring.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/07-python-agent/SKILL.md` | 📄 | Python-specific language agent. Encodes Python rules, instincts, and verifica... |
| `.agent/.agents/skills/08-rust-agent/SKILL.md` | 📄 | Rust-specific language agent. Encodes Rust rules, instincts, ownership prefli... |
| `.agent/.agents/skills/09-jsts-agent/SKILL.md` | 📄 | JavaScript/TypeScript-specific language agent. Encodes JS/TS rules, instincts... |
| `.agent/.agents/skills/10-c-agent/SKILL.md` | 📄 | C-specific language agent. Encodes C rules, instincts, and verification workf... |
| `.agent/.agents/skills/11-go-agent/SKILL.md` | 📄 | Go-specific language agent. Encodes Go rules, instincts, and verification wor... |
| `.agent/skills/04-architectural-design.md` | 🧠 | Skill for architectural-design |
| `.agent/skills/05-code-synthesis.md` | 🧠 | Skill for code-synthesis |
| `.agent/skills/06-refactor.md` | 🧠 | Skill for refactor |
| `.agent/skills/16-api-design.md` | 🧠 | Guides stable API and interface design. Use when designing APIs, module bound... |
| `.agent/workflows/08-build.md` | ⚡ | End-to-end production application build pipeline. |
| `.agent/workflows/09-feature.md` | ⚡ | Incremental feature development loop. |
| `.agents/skills/source-command-impl/SKILL.md` | 🤖 | Implement the next task incrementally — build, test, verify, commit |
| `.claude/commands/impl.md` | 🔌 | Implement the next task incrementally — build, test, verify, commit |

## 🧪 Step 4: TEST — Make Sure It Works

TDD enforcement, test engineering, quality gates, performance profiling.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/06-tdd-guide/SKILL.md` | 📄 | Strict Test-Driven Development agent. Enforces the Red-Green-Refactor cycle f... |
| `.agent/.agents/skills/22-test-engineer/SKILL.md` | 📄 | QA engineer specialized in test strategy, test writing, and coverage analysis... |
| `.agent/rules/19-test-before-done.md` | 📏 | Rule 19: Test Before Done |
| `.agent/skills/19-performance-profiling.md` | 🧠 | Optimizes application performance. Use when performance requirements exist, w... |
| `.agent/workflows/10-tdd.md` | ⚡ | Disciplined Red-Green-Refactor orchestration. |
| `.agent/workflows/13-quality-gate.md` | ⚡ | Compliance check against design/requirements. |
| `.agents/skills/source-command-tdd-guide/SKILL.md` | 🤖 | Enforce strict TDD Red-Green-Refactor cycle |
| `.claude/commands/tdd-guide.md` | 🔌 | Enforce strict TDD Red-Green-Refactor cycle |

## 👁️ Step 5: REVIEW — Check Quality

Code review, bug detection, cognitive/side-effect/state-machine inspection.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/12-antibug/SKILL.md` | 📄 | Advanced bug detection agent. Works in tandem with deep-scan to identify logi... |
| `.agent/.agents/skills/20-code-reviewer/SKILL.md` | 📄 | Senior code reviewer that evaluates changes across five dimensions — correctn... |
| `.agent/skills/07-cognitive-load-inspector.md` | 🧠 | Skill for cognitive-load-inspector |
| `.agent/skills/08-side-effect-tracker.md` | 🧠 | Skill for side-effect-tracker |
| `.agent/skills/09-state-machine-inspector.md` | 🧠 | Skill for state-machine-inspector |
| `.agent/workflows/11-debug.md` | ⚡ | Intensive diagnostic and repair protocol. |
| `.agent/workflows/14-validate.md` | ⚡ | Audit previous steps for hallucinations/errors. |
| `.agents/skills/source-command-antibug/SKILL.md` | 🤖 | Deep logical audit and root-cause bug fixing |
| `.agents/skills/source-command-review/SKILL.md` | 🤖 | Run a five-axis code review on current changes |
| `.claude/commands/antibug.md` | 🔌 | Deep logical audit and root-cause bug fixing |
| `.claude/commands/review.md` | 🔌 | Run a five-axis code review on current changes |

## 🔒 Step 6: SECURE — Harden the System

Security auditing, vulnerability detection, secure coding practices.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/21-security-auditor/SKILL.md` | 📄 | Security engineer focused on vulnerability detection, threat modeling, and se... |
| `.agent/skills/15-security-engineering.md` | 🧠 | Hardens code against vulnerabilities. Use when handling user input, authentic... |
| `.claude/agents/security-auditor.md` | 🤖 | Persona: Security Auditor |

## 🎨 Step 7: DESIGN — Polish the UI

Web aesthetics, design systems, stitch UI integration.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/13-web-aesthetics/SKILL.md` | 📄 | Ensures any generated vanilla CSS/JS web app features a premium, modern desig... |
| `.agent/skills/20-stitch-ui.md` | 🧠 | Unified entry point for Stitch design work. Handles prompt enhancement (UI/UX... |
| `.agent/skills/ui-ux-pro-max/SKILL.md` | 🧠 | UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 chart... |
| `.agents/skills/source-command-web-aesthetics/SKILL.md` | 🤖 | Audit and upgrade UI/UX to premium standards, powered by UI/UX Pro Max intell... |
| `.claude/commands/web-aesthetics.md` | 🔌 | Audit and upgrade UI/UX to premium standards, powered by UI/UX Pro Max. |

## 📝 Step 8: DOCUMENT — Explain Everything

Scientific writing, LaTeX, README generation, knowledge capture.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/14-scientific-writing/SKILL.md` | 📄 | Specialized rules for writing physics dissertations, academic reports, and La... |
| `.agent/.agents/skills/15-latex-bib-manager/SKILL.md` | 📄 | Automatically manages LaTeX bibliographies, enforces strictly sequential cita... |
| `.agent/.agents/skills/16-readme-architect/SKILL.md` | 📄 | Generates a highly structured, comprehensive, and engaging README.md for the ... |
| `.agent/skills/13-knowledge-capture.md` | 🧠 | Capture structured knowledge about a code entry point and save it to the know... |
| `.agent/workflows/18-readme-architect.md` | ⚡ | Dynamically updates README.md with active state. |

## 🔄 Step 9: OPERATE — Maintain & Ship

Registry sync, commits, release, MCP audit, licensing, scaffolding.

| File | Type | What It Does |
|------|------|--------------|
| `.agent/.agents/skills/02-failure-predictor/SKILL.md` | 📄 | Pre-execution failure prediction agent. Runs before any code execution to pre... |
| `.agent/.agents/skills/17-market-evaluator/SKILL.md` | 📄 | Evaluates the codebase and features against user requirements to estimate fut... |
| `.agent/.agents/skills/18-commercial-license/SKILL.md` | 📄 | Generates a custom LICENSE.md enforcing commercial fees and validation-based ... |
| `.agent/.agents/skills/19-git-commit-author/SKILL.md` | 📄 | Analyzes git diff output and generates atomic, Conventional Commit commands f... |
| `.agent/.agents/skills/23-mcp-auditor/SKILL.md` | 📄 | Agent 23: MCP Auditor |
| `.agent/rules/08-asset-awareness.md` | 📏 | Instinct: Asset Architecture Awareness |
| `.agent/rules/09-archive-management.md` | 📏 | Rule: Archive Management |
| `.agent/rules/10-semantic-versioning.md` | 📏 | Instinct: Semantic Versioning Control |
| `.agent/rules/11-git-awareness.md` | 📏 | Instinct: Git Awareness |
| `.agent/rules/14-release-packaging.md` | 📏 | Instinct: Release Packaging |
| `.agent/rules/20-output-organization.md` | 📏 | Rule 20: Output Organization — No Root Pollution |
| `.agent/rules/22-continuous-versioning.md` | 📏 | Governance rule mandating a semantic version bump before every finalized comm... |
| `.agent/scripts/readme_architect.py` | 📄 | (no description) |
| `.agent/scripts/sanitize_frontmatter.py` | 📄 | (no description) |
| `.agent/scripts/sync_registry.py` | 📄 | (no description) |
| `.agent/scripts/upgrade_project.py` | 📄 | (no description) |
| `.agent/skills/12-commit-semantics.md` | 🧠 | Skill for commit-semantics |
| `.agent/skills/21-mcp-audit.md` | 🧠 | MCP Capability Audit Protocol |
| `.agent/skills/22-registry-synchronizer.md` | 🧠 | Skill: Registry Synchronizer |
| `.agent/workflows/02-onboard.md` | ⚡ | Analyze legacy code and suggest initial strategy. |
| `.agent/workflows/03-scaffold.md` | ⚡ | Initialize project structure and taxonomy. |
| `.agent/workflows/12-performance.md` | ⚡ | Profiling and bottleneck elimination. |
| `.agent/workflows/15-release.md` | ⚡ | God Mode: License, README, Packaging. |
| `.agent/workflows/16-sync-registry.md` | ⚡ | Synchronize all registry files with actual .agent/ state. |
| `.agent/workflows/17-auto-commit.md` | ⚡ | Atomic, semantic commit generation loop. |
| `.agent/workflows/19-mcp-audit.md` | ⚡ | Audit & map integrated MCP tool capabilities. |
| `.agents/skills/source-command-auto-commit/SKILL.md` | 🤖 | Analyze all staged changes and create atomic Conventional Commits |
| `.agents/skills/source-command-onboard/SKILL.md` | 🤖 | First-contact project analysis — run this on any new project |
| `.agents/skills/source-command-ship/SKILL.md` | 🤖 | Run parallel fan-out to code-reviewer, security-auditor, and test-engineer, t... |
| `.agents/skills/source-command-sync-registry/SKILL.md` | 🤖 | Synchronize install-state.json and AETHER.md §13 with actual .agent/ filesyst... |
| `.claude/agents/code-reviewer.md` | 🤖 | Persona: Code Reviewer |
| `.claude/agents/test-engineer.md` | 🤖 | Persona: Test Engineer |
| `.claude/commands/auto-commit.md` | 🔌 | Analyze all staged changes and create atomic Conventional Commits |
| `.claude/commands/onboard.md` | 🔌 | First-contact project analysis — run this on any new project |
| `.claude/commands/ship.md` | 🔌 | Run parallel fan-out to code-reviewer, security-auditor, and test-engineer, t... |
| `.claude/commands/sync-registry.md` | 🔌 | Synchronize install-state.json and AETHER.md §13 with actual .agent/ filesyst... |

---

*Auto-generated by `.agent/scripts/generate_system_map.py`. Last updated: 2026-05-30 12:10*
