---
name: A02-ask
description: Surgical codebase inquiry and semantic locator. Delivers pinpoint, noise-free answers to developer doubts by isolating exact code slices without burning context tokens.
category: scan
---

# Skill: A02-ask (Surgical Codebase Inquiry & Semantic Locator)

**Objective**: Answer developer doubts and technical queries about the codebase with surgical accuracy and minimal noise. Locate functions, state transitions, API endpoints, and configuration blocks instantly without dumping large files into context.

---

## 1. Skill Package Structure (Self-Contained)

This skill operates purely through high-precision cognitive search and focused slice reads. It requires zero external scripts:

```
A02-ask/
├── SKILL.md                  # Semantic inquiry protocol & surgical reading rules
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `A02-ask/` directly into any `.agents/skills/` directory to enable instant, low-noise codebase Q&A.

---

## 2. Core Operating Principles

1. **Answer First, Explain Second**: Never start with generic filler ("Sure, let me help you with that"). State the direct answer or location immediately in the first sentence.
2. **Surgical Isolation (Minimal Token Footprint)**:
   - Never read an entire 500-line file to answer a question about one function.
   - Use ripgrep / exact symbol search (`grep_search`) to locate line numbers first, then view only the precise line range (e.g., 20–60 lines).
3. **Tandem with `A01-deep-scan`**:
   - If an architectural map or context anchor from `A01-deep-scan` is available, use it to instantly know which directory houses the subsystem (e.g. `src/auth/` for authentication, `src/db/` for models).
   - If no prior scan exists, locate the symbol via targeted search without re-scanning the entire repo tree.
4. **Clickable References**:
   Always provide clickable markdown file links with line numbers: `[SymbolName](file:///path/to/file#L20-L45)`.

---

## 3. The 4-Step Surgical Inquiry Protocol

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Query Intent Classification                         │
│ (Where is X? / How does X work? / Why is X failing?)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 2: Target Symbol Localization                         │
│ (Execute exact grep search to find definition & line #)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 3: Focused Slice Reading                               │
│ (Read ONLY lines [StartLine, EndLine] around target symbol) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 4: Direct, High-Signal Answer Synthesis                │
│ (Direct answer + Clickable Link + Concise Logic Snippet)    │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Query Intent Classification
Determine what the developer is asking for:
- **Location Query** (*"Where is user authentication handled?"*): Target manifests, route registrations, or middleware.
- **Mechanism Query** (*"How does token refresh work?"*): Target the specific function implementation and its caller.
- **Contract Query** (*"What parameters does `calculate_discount` accept?"*): Target the function signature, type hints, or interface definition.
- **State Query** (*"Where is the cart state stored?"*): Target store declarations (Redux slice, Zustand hook, database schema).

### Step 2: Target Symbol Localization
Search specifically for definitions rather than broad occurrences:
- Search for `def function_name`, `function function_name`, `class ClassName`, `export const symbolName`, or interface keys.
- Do NOT read files during search; use ripgrep/search tools to obtain exact file paths and line numbers.

### Step 3: Focused Slice Reading
- Request a slice containing the function/block plus ~10 lines before and after for context.
- Never exceed 100 lines unless the logic block is exceptionally large.

### Step 4: High-Signal Answer Synthesis
Follow this concise output structure:

```markdown
### 💡 [Direct Answer / Summary in 1-2 Sentences]

**Location**: [`functionName` in path/to/file.ts#L45-L82](file:///d:/path/to/file.ts#L45-L82)

#### How It Works:
- **Input / Trigger**: [What calls this or what inputs it expects]
- **Core Logic**: [1–3 bullet points explaining the mechanism]
- **Output / Side Effect**: [What it returns, mutates, or emits]

```[language]
// Minimal relevant code snippet (highlighting only key lines)
```
```

---

## 4. Invocation & Workflow Integration
- **Manual**: Triggered when the user asks a technical question about the codebase, or invokes `/ask`.
- **In Workflow**: Runs immediately following `A01-deep-scan` when planning a specific feature, helping the planner inspect individual module contracts without context bloat.
