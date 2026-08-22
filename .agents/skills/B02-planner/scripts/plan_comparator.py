#!/usr/bin/env python3
"""
plan_comparator.py - Architectural Plan & Variation Comparator
Zero external dependencies (Python standard library only).

Parses plan variations from markdown and generates an objective trade-off scorecard:
- Analyzes proposed files touched, new dependencies, and architectural complexity
- Evaluates Velocity, Maintainability, and Blast-Radius Risk
- Produces markdown scorecard or structured JSON
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

def parse_variations(text: str) -> list[dict]:
    """Extract distinct architectural variations from a plan text."""
    variation_pattern = re.compile(
        r'^(?:#{2,4}\s+)?(?:Variation|Option|Approach)\s+([A-Za-z0-9]+)[:\s\-]+([^\n]+)',
        re.IGNORECASE | re.MULTILINE
    )
    
    matches = list(variation_pattern.finditer(text))
    if not matches:
        return []
        
    variations = []
    for i, m in enumerate(matches):
        v_id = m.group(1).strip()
        v_name = m.group(2).strip()
        start_pos = m.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        v_body = text[start_pos:end_pos].strip()
        
        # Extract files mentioned
        file_tokens = re.findall(r'`([^`]+\.[a-zA-Z0-9]{1,6})`', v_body)
        files = sorted(list(set(file_tokens)))
        new_files = [f for f in files if '[NEW]' in v_body or 'new' in f.lower()]
        
        # Detect dependency additions
        dep_match = re.findall(r'(?:npm\s+i(?:nstall)?|pip\s+install|cargo\s+add)\s+([\w\-@/]+)', v_body, re.IGNORECASE)
        deps = sorted(list(set(dep_match)))
        
        # Calculate heuristic scores
        file_count = len(files)
        dep_count = len(deps)
        
        # Velocity score (higher = faster to ship, less files touched)
        velocity = max(1, min(10, 10 - (file_count * 1) - (dep_count * 2)))
        
        # Maintainability score (higher = better modularity, clean separation)
        is_modular = bool(re.search(r'(?:interface|adapter|service|decoupled|repository|modular)', v_body, re.IGNORECASE))
        maintainability = 6 if not is_modular else 9
        if file_count == 1:
            maintainability -= 2 # Potentially monolithic
            
        # Risk score (1 = lowest risk, 10 = highest risk)
        risk = min(10, max(1, 2 + (file_count * 1) + (dep_count * 3)))
        
        variations.append({
            "id": v_id,
            "title": v_name,
            "files_touched": file_count,
            "files": files,
            "dependencies_added": deps,
            "scores": {
                "velocity": velocity,
                "maintainability": maintainability,
                "risk_score": risk
            },
            "summary_snippet": v_body[:240].replace('\n', ' ').strip() + "..."
        })
        
    return variations

def format_markdown_table(variations: list[dict]) -> str:
    if not variations:
        return "No distinct variations found in input. Ensure headers follow `### Variation A: [Name]`."
        
    lines = [
        "| Variation | Focus / Strategy | Files Touched | New Deps | Velocity (1-10) | Maintainability (1-10) | Risk (1-10) |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: |"
    ]
    
    for v in variations:
        lines.append(
            f"| **Variation {v['id']}** | {v['title']} | {v['files_touched']} | {len(v['dependencies_added'])} | {v['scores']['velocity']}/10 | {v['scores']['maintainability']}/10 | {v['scores']['risk_score']}/10 |"
        )
        
    lines.append("\n#### Trade-Off Verdict:")
    recommended = max(variations, key=lambda x: (x["scores"]["maintainability"] * 1.5 + x["scores"]["velocity"] - x["scores"]["risk_score"]))
    lines.append(f"- **Recommended Choice**: **Variation {recommended['id']} ({recommended['title']})** provides the optimal balance between velocity and long-term architectural stability.")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Compare architectural plan variations and generate trade-off matrices.")
    parser.add_argument("input_file", help="Path to markdown plan containing variations (or '-' for stdin)")
    parser.add_argument("--json", action="store_true", help="Output comparison results as JSON")
    args = parser.parse_args()
    
    if args.input_file == "-":
        content = sys.stdin.read()
    else:
        if not os.path.exists(args.input_file):
            sys.stderr.write(f"Error: Input file '{args.input_file}' not found.\n")
            sys.exit(1)
        with open(args.input_file, "r", encoding="utf-8") as f:
            content = f.read()
            
    variations = parse_variations(content)
    
    if args.json:
        print(json.dumps({"variations": variations, "count": len(variations)}, indent=2))
    else:
        print(format_markdown_table(variations))

if __name__ == "__main__":
    main()
