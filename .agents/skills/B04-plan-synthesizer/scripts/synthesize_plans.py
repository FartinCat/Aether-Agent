#!/usr/bin/env python3
"""
synthesize_plans.py - Multi-Plan & User-Idea Synthesis Engine
Zero external dependencies (Python standard library only).

Reconciles multiple proposals, agent strategies, or user brainstorming ideas:
1. Extracts target files and components across inputs
2. Identifies Consensus (shared elements) and Clashes (overlapping files or conflicting architectures)
3. Outputs a Unified Synthesis Report in Markdown or JSON
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

def extract_ideas(text: str) -> list[dict]:
    """Parse discrete proposals or user ideas from markdown."""
    pattern = re.compile(
        r'^(?:#{2,4}\s+)?(?:Plan|Proposal|Idea|Option|Strategy)\s+([A-Za-z0-9_\-]+)[:\s\-]+([^\n]+)',
        re.IGNORECASE | re.MULTILINE
    )
    
    matches = list(pattern.finditer(text))
    if not matches:
        # Fallback: Treat bullet points or numbered lists as ideas if short text
        return []
        
    proposals = []
    for i, m in enumerate(matches):
        p_id = m.group(1).strip()
        p_title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        
        # Files mentioned
        files = set(re.findall(r'`([^`]+\.[a-zA-Z0-9]{1,6})`', body))
        
        # Keywords
        is_async = bool(re.search(r'\b(?:async|queue|worker|background|event|stream)\b', body, re.IGNORECASE))
        is_sync = bool(re.search(r'\b(?:sync|direct|inline|blocking)\b', body, re.IGNORECASE))
        
        proposals.append({
            "id": p_id,
            "title": p_title,
            "files": sorted(list(files)),
            "is_async": is_async,
            "is_sync": is_sync,
            "body": body[:300].strip()
        })
        
    return proposals

def synthesize(proposals: list[dict]) -> dict:
    if not proposals:
        return {
            "status": "EMPTY",
            "message": "No structured plans or ideas found. Use `### Plan A: [Title]` or `### Idea 1: [Title]` headers."
        }
        
    all_files = set()
    file_map = {}
    for p in proposals:
        for f in p["files"]:
            all_files.add(f)
            file_map.setdefault(f, []).append(p["id"])
            
    # Consensus: Files or goals agreed across all proposals
    consensus_files = [f for f, p_ids in file_map.items() if len(p_ids) > 1]
    
    # Clashes: Overlapping files with potentially conflicting approaches
    clashes = []
    async_count = sum(1 for p in proposals if p["is_async"])
    sync_count = sum(1 for p in proposals if p["is_sync"])
    if async_count > 0 and sync_count > 0:
        clashes.append({
            "topic": "Execution Model",
            "conflict": "Conflict between Synchronous vs. Asynchronous/Event-Driven processing",
            "resolution": "Adopt Asynchronous background processing for heavy operations; retain synchronous response for instant validation."
        })
        
    for f, p_ids in file_map.items():
        if len(p_ids) > 1:
            clashes.append({
                "topic": f"Shared File: {f}",
                "conflict": f"Modified by multiple proposals ({', '.join(p_ids)})",
                "resolution": "Consolidate changes into a single phased task to avoid race conditions and file collisions."
            })
            
    return {
        "status": "SYNTHESIZED",
        "proposal_count": len(proposals),
        "total_files_affected": len(all_files),
        "consensus_files": consensus_files,
        "clashes": clashes,
        "proposals": proposals
    }

def format_markdown_synthesis(results: dict) -> str:
    if results.get("status") == "EMPTY":
        return results["message"]
        
    lines = [
        "### 🧩 Multi-Plan & Idea Synthesis Report",
        f"- **Input Sources Analyzed**: {results['proposal_count']} proposals / user ideas",
        f"- **Total Target Files**: {results['total_files_affected']} files",
        "\n#### 1. Consensus Elements (Agreed Baseline):"
    ]
    
    if results["consensus_files"]:
        for f in results["consensus_files"]:
            lines.append(f"  - ✅ Shared module: `{f}`")
    else:
        lines.append("  - All proposals touch distinct files with minimal baseline overlap.")
        
    lines.append("\n#### 2. Conflicts & Trade-Off Resolutions:")
    if results["clashes"]:
        for c in results["clashes"]:
            lines.append(f"  - ⚡ **{c['topic']}**: {c['conflict']}")
            lines.append(f"    - *Resolution*: {c['resolution']}")
    else:
        lines.append("  - Zero architectural conflicts detected. Proposals can be merged cleanly.")
        
    lines.append("\n#### 3. Golden Plan Recommendation:")
    lines.append("  - Merge consensus elements first, then apply resolved conflict decisions sequentially.")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Synthesize multiple plans, agent proposals, or user ideas into a unified roadmap.")
    parser.add_argument("input_file", help="Path to markdown file containing multiple plans or ideas (or '-' for stdin)")
    parser.add_argument("--json", action="store_true", help="Output synthesis as JSON")
    args = parser.parse_args()
    
    if args.input_file == "-":
        content = sys.stdin.read()
    else:
        if not os.path.exists(args.input_file):
            sys.stderr.write(f"Error: File '{args.input_file}' not found.\n")
            sys.exit(1)
        with open(args.input_file, "r", encoding="utf-8") as f:
            content = f.read()
            
    proposals = extract_ideas(content)
    results = synthesize(proposals)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_markdown_synthesis(results))

if __name__ == "__main__":
    main()
