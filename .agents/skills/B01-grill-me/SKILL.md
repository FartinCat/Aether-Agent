---
name: B01-grill-me
description: Deep architectural & requirements interrogator. Conducts exhaustive pre-planning interviews across UX, data flow, edge cases, and scope fences with built-in ELIA5 layman translation.
category: plan
aliases: [grill-me, requirements-grill, decision-interviewer, elia5-interrogator]
---

# Skill: B01-grill-me (Architectural & Requirements Interrogator)

**Objective**: Interrogate the user to resolve all ambiguous architectural forks, data models, UX journeys, failure scenarios, and scope fences *before* a plan is drafted. Eliminate misunderstandings, prevent premature coding, and empower non-technical users through the **ELIA5 (Explain Like I'm 5)** layman safety hatch.

---

## 1. Skill Package Structure (Self-Contained)

This skill operates purely through disciplined interactive questioning and cognitive decision-tree synthesis. It requires zero external scripts:

```
B01-grill-me/
├── SKILL.md                  # 4-Axis decision tree & ELIA5 interview protocol
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `B01-grill-me/` directly into any `.agents/skills/` directory to enable deep, guided pre-planning interviews.

---

## 2. Core Operating Principles

1. **The Zero-Redundancy Law**:
   - **Never ask what code already tells you**. Category A ([`A01-deep-scan`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A01-deep-scan), [`A04-dependency-mapper`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A04-dependency-mapper), [`A05-route-scanner`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A05-route-scanner), [`A06-schema-scanner`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A06-schema-scanner)) already reveals the language, framework, database models, and routes.
   - Only interview the user about **human intent, business rules, design choices, error tolerance, and scope boundaries**.

2. **One Branch at a Time**:
   - Never dump a wall of 10 questions at once. Ask questions **one at a time** (or in tight thematic pairs) using interactive multiple-choice options (`ask_question`).

3. **Always Provide a Recommended Option**:
   - Formulate 2–3 concrete, technically distinct options plus a write-in choice.
   - Prefix the strongest option with **`(Recommended)`**, citing existing patterns in the codebase (e.g. *"Recommended because your auth routes in `A05` already use JWT bearer tokens"*).

4. **Dual Clarification Safety Hatch (`/ask` vs `/ask ELIA5`)**:
   - Technical options can sometimes need deeper architectural elaboration, or conversely, be too intimidating for non-computer-science users.
   - If the user uses the write-in box to ask `/ask`, provide a **technical trade-off analysis** (concurrency, memory, query complexity).
   - If the user types `/ask ELIA5`, provide a **zero-jargon physical analogy** (e.g. restaurant, post office) and plain human outcomes.
   - After explaining, re-present the question so the user can make their informed selection.

---

## 3. The 4-Axis Decision Tree

Every interview systematically traverses four mandatory axes to ensure zero blind spots:

```
┌─────────────────────────────────────────────────────────────┐
│ Axis 1: Functional & UX Behavior                            │
│ (Triggers, sync vs async, user flow, visual feedback)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Axis 2: Data & Persistence Model                            │
│ (State lifecycle, storage engine, relations, caching)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Axis 3: Edge Cases & The "Unhappy Path"                     │
│ (Network drops, malformed data, rate limits, rollbacks)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Axis 4: Scope Fence (Anti-Scope)                            │
│ (Explicitly defining what is strictly OUT of scope for v1)  │
└─────────────────────────────────────────────────────────────┘
```

### Axis 1: Functional & UX Behavior
- *Goal*: Clarify how the feature behaves from the user's or caller's perspective.
- *Sample Inquiry*:
  > *"When the user triggers this action, should the UI update optimistically with instant feedback, or wait for the server confirmation spinner?"*

### Axis 2: Data & Persistence Model
- *Goal*: Clarify data lifecycle, schema modifications, and storage location.
- *Sample Inquiry*:
  > *"Should this configuration persist across sessions in the database, remain in localStorage per browser, or reset in memory on page refresh?"*

### Axis 3: Edge Cases & The "Unhappy Path"
- *Goal*: Clarify failure modes and degradation strategies.
- *Sample Inquiry*:
  > *"If the external API returns a 429 Rate Limit error or times out, should we silently retry up to 3 times with exponential backoff, or immediately alert the user with a retry button?"*

### Axis 4: Scope Fence (Anti-Scope)
- *Goal*: Prevent scope creep and lock milestone boundaries.
- *Sample Inquiry*:
  > *"Are we supporting batch operations and CSV exports in this first iteration, or strictly single-item actions?"*

---

## 4. Question Format & Modal Standard

When calling the interactive modal (`ask_question`), format the question with clear options and contextual guidance:

```markdown
Question: [Specific architectural fork or requirement question]
- (Recommended) [Option 1: Idiomatic choice with rationale based on repo state]
- [Option 2: Alternative approach with trade-off]
- [Option 3: Minimalist fallback]
```

### The Option Clarification Prompt
At the bottom of each question or in the introduction, always display:
> 💡 *Need clarification? In the write-in box, type `/ask` for a deeper technical trade-off breakdown, or `/ask ELIA5` for a simple, zero-jargon real-world analogy.*

---

## 5. Dual Clarification Protocol: Technical (`/ask`) vs. Layman (`/ask ELIA5`)

When a user submits a query into the custom write-in box instead of choosing an option, intercept it immediately and route it based on intent:

### Mode A: `/ask` (Technical Trade-Off Breakdown)
* **Trigger**: User types `/ask`, `/ask <question>`, or asks for technical clarification regarding the options.
* **Target Audience**: Engineers and technical leads evaluating performance and architecture.
* **Response Content**:
  - **Option Trade-Offs**: Concurrency, memory footprint, query complexity, latency, and failure tolerance.
  - **Codebase Compatibility**: Cites existing dependencies and patterns found in Category A scans (`A04`, `A05`, `A06`).
  - **Technical Recommendation**: Clear engineering verdict.
* **Post-Action**: Re-present the original question modal with the options so the user can make their informed selection.

### Mode B: `/ask ELIA5` (Layman Real-World Analogy)
* **Trigger**: User types `/ask ELIA5`, `/ask explain simply`, or indicates confusion with technical jargon.
* **Target Audience**: Non-technical stakeholders, product managers, or junior developers wanting simplicity.
* **Response Content**:
  - **The Physical Analogy**: Translates the technical fork into a familiar real-world scenario (e.g., ordering at a diner, mailing letters at a post office, highway toll booths). Max 2 sentences.
  - **Plain-English Consequences**: 1 sentence per option stating what happens in real life (e.g. "Option 1 is faster to build but hard to modify; Option 2 takes more time now but never jams").
  - **Layman Recommendation**: Which choice is simpler and why.
* **Post-Action**: Re-present the simplified question modal for their decision.

---

## 6. Synthesis: The Decision Record

Once all 4 axes are resolved, synthesize the findings into a machine-readable context block and human summary:

```markdown
<!-- CONTEXT_ANCHOR:DECISION_RECORD -->
### 🎯 Architecture & Requirements Decision Record

#### 1. Confirmed Scope & Target
- **Feature/Task**: [Summary of user goal]
- **Primary Beneficiary/Caller**: [Target persona or module]

#### 2. Key Architectural Decisions
- **UX & Behavior**: [Locked decision + rationale]
- **Data & Persistence**: [Storage engine, schema updates, caching policy]

#### 3. Unhappy Path & Resilience Handlers
- **Failure Recovery**: [Timeout / Retry / Error display contract]
- **Validation Fallback**: [Invalid input policy]

#### 4. Scope Fence (Strictly Out of Scope)
- ❌ [Explicit non-goal 1]
- ❌ [Explicit non-goal 2]

---
**Next Step**: Feed directly into `B02-task-planner` for atomic task decomposition.
<!-- END_ANCHOR:DECISION_RECORD -->
```

---

## 7. Invocation & Workflow Integration
- **Manual**: Triggered via `/grill-me`, `/interview`, or when the user provides an ambiguous, multi-faceted feature request.
- **In Workflow**: Runs directly between **Category A (Scan & Discovery)** and **`B02-task-planner`**, guaranteeing that the planner builds on verified human intent rather than AI guesswork.
