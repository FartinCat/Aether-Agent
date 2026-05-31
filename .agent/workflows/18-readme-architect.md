---
title: "README ARCHITECT"
description: "Dynamically updates README.md with active state."
order: 18
category: docs
---
# Workflow: README Architect

**Objective**: Ensure the main `README.md` file is an accurate, perfectly synced reflection of the `.agent/` architecture. 

## Execution Sequence

**This workflow is fully autonomous.** The agent must simply execute the python engine:

1. **Run Engine**: Execute `python .agent/scripts/readme_architect.py`
2. **Verification**: Run `git diff README.md` to verify the tables and flowchart updated successfully.

The Python engine handles:
- **Architecture Scan**: Parses `.agent/` and `.claude/` directories to identify all active rules, skills, workflows, commands, and instincts.
- **Deep Extraction**: Extracts actual YAML `description` and `trigger` attributes from `SKILL.md`, `instincts/*.md` (e.g. `## The Pattern`), and frontmatter.
- **Flowchart Generation**: Rebuilds the Mermaid flowchart dynamically based on workflow numbers.
- **README Injection**: Injects updated Specialist Tables, Workflows, Foundational Skills, and Behavioral Instincts into `README.md`.
- **Privacy Sanitization**: Scans the final output for personal filesystem paths (home dirs, usernames, workspace roots) and replaces them with generic examples before writing. Enforces Instinct 07.

## Execution Trigger
- Triggered automatically during `/15-release` OR manually via `/18-readme-architect`.
- **Must execute BEFORE** `/16-sync-registry` so that the updated README correctly receives the finalized version badge during the sync.

## Primary Agent
- `16-readme-architect`

