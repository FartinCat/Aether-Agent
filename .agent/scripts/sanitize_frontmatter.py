#!/usr/bin/env python3
"""
Aether Agent OS — Workflow Frontmatter Sanitizer
======================================================
Location: .agent/scripts/sanitize_frontmatter.py

Ensures all workflow files in `.agent/workflows/` have perfectly formatted,
standardized YAML frontmatter headers, matching lifecycle order sequences.
"""

import os
import sys
import re

# ─── Dynamic Base Path ────────────────────────────────────────────────
try:
    sys.path.append(os.path.dirname(__file__))
    from detect_root import patch_sync_registry
    base = str(patch_sync_registry())
except ImportError:
    base = "."

MAPPINGS = {
    "01-scan.md": {
        "title": "SCANNER",
        "description": "Build situational awareness and map directories.",
        "order": 1
    },
    "02-onboard.md": {
        "title": "ONBOARD PROJECT",
        "description": "Analyze legacy code and suggest initial strategy.",
        "order": 2
    },
    "03-scaffold.md": {
        "title": "SCAFFOLD ASSETS",
        "description": "Initialize project structure and taxonomy.",
        "order": 3
    },
    "04-spec.md": {
        "title": "SPEC DISCOVERY",
        "description": "Functional and technical spec extraction.",
        "order": 4
    },
    "05-research.md": {
        "title": "PARALLEL RESEARCH",
        "description": "Execute parallel technical research paths.",
        "order": 5
    },
    "06-plan-synthesis.md": {
        "title": "MULTI PLAN SYNTHESIS",
        "description": "Merge competing AI strategies into one plan.",
        "order": 6
    },
    "07-knowledge-capture.md": {
        "title": "KNOWLEDGE CAPTURE",
        "description": "Distill project insights into persistent KIs.",
        "order": 7
    },
    "08-build.md": {
        "title": "BUILD APP",
        "description": "End-to-end production application build pipeline.",
        "order": 8
    },
    "09-feature.md": {
        "title": "FEATURE DEVELOPMENT",
        "description": "Incremental feature development loop.",
        "order": 9
    },
    "10-tdd.md": {
        "title": "TDD",
        "description": "Disciplined Red-Green-Refactor orchestration.",
        "order": 10
    },
    "11-debug.md": {
        "title": "DEBUG SESSION",
        "description": "Intensive diagnostic and repair protocol.",
        "order": 11
    },
    "12-performance.md": {
        "title": "PERFORMANCE",
        "description": "Profiling and bottleneck elimination.",
        "order": 12
    },
    "13-quality-gate.md": {
        "title": "QUALITY GATE",
        "description": "Compliance check against design/requirements.",
        "order": 13
    },
    "14-validate.md": {
        "title": "CROSS AGENT VALIDATOR",
        "description": "Audit previous steps for hallucinations/errors.",
        "order": 14
    },
    "15-release.md": {
        "title": "RELEASE PROJECT",
        "description": "God Mode: License, README, Packaging.",
        "order": 15
    },
    "16-sync-registry.md": {
        "title": "SYNC REGISTRY",
        "description": "Synchronize all registry files with actual .agent/ state.",
        "order": 16
    },
    "17-auto-commit.md": {
        "title": "AUTO COMMIT",
        "description": "Atomic, semantic commit generation loop.",
        "order": 17
    },
    "18-readme-architect.md": {
        "title": "README ARCHITECT",
        "description": "Dynamically updates README.md with active state.",
        "order": 18
    },
    "19-mcp-audit.md": {
        "title": "MCP AUDIT",
        "description": "Audit & map integrated MCP tool capabilities.",
        "order": 19
    }
}

def main():
    workflows_dir = os.path.join(base, ".agent", "workflows")
    print(f"Sanitizing workflows in {workflows_dir}...")
    
    if not os.path.exists(workflows_dir):
        print(f"ERROR: Workflows directory does not exist at {workflows_dir}")
        sys.exit(1)
        
    for filename in sorted(os.listdir(workflows_dir)):
        if not filename.endswith(".md"):
            continue
            
        path = os.path.join(workflows_dir, filename)
        if filename not in MAPPINGS:
            print(f"Skipping {filename} (not in mappings)")
            continue
            
        mapping = MAPPINGS[filename]
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Strip any existing frontmatter block if it starts with '---'
        if content.startswith("---"):
            fm_end_match = re.search(r"^---\r?\n.*?\r?\n---\r?\n", content, re.DOTALL)
            if fm_end_match:
                content = content[fm_end_match.end():]
                print(f"Stripped existing frontmatter from {filename}")
            else:
                parts = content.split("---")
                if len(parts) >= 3:
                    content = "---".join(parts[2:])
                    print(f"Fallback stripped frontmatter from {filename}")
        
        # Build perfectly formatted new frontmatter with \n line endings
        fm_lines = [
            "---",
            f"title: \"{mapping['title']}\"",
            f"description: \"{mapping['description']}\"",
            f"order: {mapping['order']}",
            "---",
            "" # Trailing empty line after frontmatter
        ]
        frontmatter = "\n".join(fm_lines)
        
        # Normalize the remaining content line endings to LF (\n)
        content_normalized = content.replace("\r\n", "\n").replace("\r", "\n")
        
        # Strip any initial blank lines from the remaining content
        content_normalized = content_normalized.lstrip()
        
        # Write perfectly formatted file
        final_content = frontmatter + content_normalized
        
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(final_content)
            
        print(f"SUCCESS: Sanitized and saved {filename}")

if __name__ == "__main__":
    main()
