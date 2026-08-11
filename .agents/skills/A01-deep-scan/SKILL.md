---
name: A01-deep-scan
description: Comprehensive situational awareness and architectural mapping. Dynamically detects repository type, traces core execution flows and entrypoints, and generates human briefs or machine context anchors.
category: scan
---

# Skill: Deep Scan

**Objective**: Build rapid, accurate, and comprehensive situational awareness of any codebase before taking action. Dynamically adapt inspection to the repository's actual paradigm rather than enforcing rigid, pre-installed templates.

---

## 1. Skill Package Structure (100% Self-Contained)

This skill is designed to be completely portable and independent. It carries all of its own instructions, metadata, and utilities within its own directory:

```
deep-scan/
├── SKILL.md                  # Core cognitive protocol & operating guidelines
├── scripts/
│   └── repo_fingerprint.py   # Zero-dependency, pure standard library analyzer (<50ms)
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI & invocation metadata
```

Anyone can copy the `deep-scan/` folder into any Antigravity or AI IDE setup (`.agents/skills/deep-scan`), and it will execute reliably without depending on external project scripts or frameworks.

---

## 2. Core Operating Principles

1. **Cognitive Over Static**: Do not merely list files or print directory trees. Understand what the software does, how data flows through it, and what state the architecture is in.
2. **Repository-Adaptive**: Automatically classify the project type (Fullstack, Systems, AI/ML, Monorepo, Library, CLI, Agentic) and ask questions relevant to that specific paradigm.
3. **Context Efficiency**:
   - For **small/medium repositories (< 50 files)**: Perform direct cognitive inspection using standard read/list tools. No scripts needed.
   - For **large codebases or monorepos (> 50 files)**: Run the skill's self-contained helper script `scripts/repo_fingerprint.py` to extract scale, manifests, and file distributions in milliseconds without flooding the LLM context window.
4. **Strict Infrastructure Exclusion**:
   Never treat agent infrastructure (e.g., `.agent/`, `.agents/`, `.git/`, `.vscode/`, `.idea/`, `node_modules/`, `target/`, `.venv/`, `dist/`, `build/`) as project source code or structural anomalies. They are operational tooling or build artifacts.

---

## 3. The 4-Stage Execution Protocol

```
┌─────────────────────────────────────────────────────────────┐
│ Stage 1: Rapid Orientation & Repository Typing             │
│ (Inspect root manifests, detect languages & frameworks)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 2: Scale-Aware Inspection                             │
│ (<50 files: direct reads | >50 files: run repo_fingerprint)│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 3: Architecture & Data Flow Tracing                   │
│ (Trace entrypoints, state management, API/DB boundaries)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 4: Codebase Health & Dual-Mode Output Generation      │
│ (Standalone Developer Brief OR Ensemble Context Anchor)     │
└─────────────────────────────────────────────────────────────┘
```

### Stage 1: Rapid Orientation & Repository Typing
Inspect root directory configuration files to classify the project:

| Detected Artifact | Inferred Repository Type | Primary Scanning Focus |
| :--- | :--- | :--- |
| `package.json` with `next`, `react`, `vue`, `svelte` | **Fullstack / Web App** | App/pages routing, state stores, client/server boundaries, styling system |
| `Cargo.toml` | **Rust Systems / Tooling** | Crate structure, binary vs library targets, ownership boundaries, FFI |
| `pyproject.toml`, `requirements.txt` | **Python / AI / Data** | Package management, entry CLI/API, data pipelines, model weights, env configs |
| `go.mod` | **Go Service / CLI** | Package main, internal vs pkg layout, concurrency patterns, interfaces |
| `CMakeLists.txt`, `Makefile` | **C / C++ Native** | Source vs include separation, compiler flags, third-party libraries |
| `pnpm-workspace.yaml`, `lerna.json`, `turbo.json` | **Monorepo** | Workspace dependency graph, shared packages, build pipelines |
| Pure Markdown, `.agents`, skills | **Agentic / Meta Repo** | Governance rules, skill contracts, prompt architectures, workflows |

### Stage 2: Scale-Aware Inspection
- Check the approximate file count of source files.
- **If < 50 files**: Use `list_dir` on key source directories and directly read package manifests.
- **If > 50 files**: Run the skill's self-contained script:
  ```bash
  python "<path_to_skill>/scripts/repo_fingerprint.py" .
  ```
  *(Or execute inline via Python standard library)*. This returns a compact JSON summary of the file distribution and detected manifests in <50ms without burning context tokens.

### Stage 3: Architecture & Data Flow Tracing
Trace the execution life-cycle by answering these 4 fundamental questions:
1. **Bootstrap / Entrypoint**: Where does execution begin? (`main()`, `index.tsx`, `app.py`, `layout.tsx`)
2. **State & Data Boundary**: Where does state live? (Database, memory, Redux/Zustand store, filesystem, URL params)
3. **Interface & Communication**: How do components talk to each other? (REST, GraphQL, gRPC, CLI flags, event buses)
4. **Configuration & Environment**: Where are secrets and operational settings loaded? (`.env.example`, `config.yaml`, environment variables)

### Stage 4: Codebase Health Diagnosis
Evaluate tangible engineering health indicators:
- **Build & Test Infrastructure**: Are tests present? Is there a test runner configured (`pytest`, `vitest`, `cargo test`, `jest`)?
- **Type Safety & Linting**: Are type definitions enforced (`tsconfig.json`, `mypy.ini`, strict mode)?
- **Documentation**: Does a clear `README` or architecture spec exist for onboarding?
- **Hygiene**: Are build artifacts, `.env` files, or temporary dumps mistakenly committed?

---

## 4. Dual Output Modes

### Mode A: Standalone Developer Brief
*Use this when invoked directly by the user or via `/deep-scan`.*

```markdown
## 🔍 Deep Scan Report: [Project Name]

### 1. Repository Identification
- **Type**: [e.g. Next.js Fullstack Web Application / Python CLI / Rust Crate]
- **Core Languages**: [e.g. TypeScript (80%), Python (15%), CSS (5%)]
- **Scale**: [e.g. Small (~15 source files) / Medium (~60 files) / Large Monorepo]
- **Primary Frameworks**: [e.g. React 19, FastAPI, TailwindCSS, Prisma]

### 2. Architecture & Data Flow
- **Entry Point**: `path/to/entry` (bootstraps server/UI)
- **Data & State Flow**: [How data enters the system, gets processed, and persists]
- **Key Modules**:
  - `path/to/module-a/`: [Responsibility]
  - `path/to/module-b/`: [Responsibility]

### 3. Engineering Health & Observations
- **Tests**: [Configured / Missing / Failing]
- **Types & Quality**: [Strict / Partial / None]
- **Key Observations**: [Specific strengths, architectural bottlenecks, or technical debt]

### 4. Recommended Next Steps
- [Immediate high-value action item, e.g. "Run `/planner` to design the auth module" or "Run `/antibug` to inspect async error handling"]
```

### Mode B: Ensemble Machine Context Anchor
*Use this when `deep-scan` runs as Step 1 of a multi-agent workflow (e.g. before `/planner`, `/antibug`, or `/ship`).*

Emit a compact block that subsequent agents can parse without re-reading the filesystem:

```markdown
<!-- CONTEXT_ANCHOR:DEEP_SCAN -->
{
  "repo_type": "type_identifier",
  "languages": ["primary", "secondary"],
  "entrypoints": ["path/to/main"],
  "key_directories": {
    "src": "path",
    "tests": "path",
    "docs": "path"
  },
  "package_manifest": "path/to/manifest",
  "test_runner": "runner_name_or_null",
  "health_summary": "one_sentence_state"
}
<!-- /CONTEXT_ANCHOR -->
```

---

## 5. Invocation
- Explicitly: run when starting a new session or onboarding to an unfamiliar repository (`/deep-scan`).
- Pipeline: automatically runs as Stage 1 of scan-plan-build-test workflows.
