#!/usr/bin/env python3
"""
task_executor.py - Atomic Task Decomposer & Execution Engine
Zero external dependencies (Python standard library only).

Capabilities:
1. Validates roadmap cognitive load (flags tasks touching >2 files)
2. Tracks task states: PENDING [ ], IN_PROGRESS [-], COMPLETED [x], BLOCKED [!]
3. Validates Definition of Done (DoD) verification criteria per phase
4. Generates execution progress metrics and JSON state reports
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

FILE_EXTENSIONS = {
    '.ts', '.tsx', '.js', '.jsx', '.py', '.rs', '.go', '.c', '.cpp', '.h', '.hpp',
    '.java', '.kt', '.rb', '.php', '.cs', '.swift', '.sql', '.prisma', '.json',
    '.yaml', '.yml', '.toml', '.env', '.html', '.css', '.scss', '.sh', '.bash', '.ps1'
}

def extract_file_paths(text: str) -> list[str]:
    backticked = re.findall(r'`([^`]+)`', text)
    tokens = re.findall(r'[\w\-./\\]+', text)
    candidates = set(backticked + tokens)
    
    files = []
    for c in candidates:
        if re.match(r'^\d+(?:\.\d+)+$', c):
            continue
        ext = Path(c).suffix.lower()
        if ext in FILE_EXTENSIONS:
            files.append(c)
        elif ('/' in c or '\\' in c) and '.' in c and not c.startswith('http'):
            files.append(c)
    return sorted(list(set(files)))

def parse_roadmap(plan_text: str, root_dir: str = ".") -> dict:
    lines = plan_text.splitlines()
    phases = []
    current_phase = None
    issues = []
    
    phase_pattern = re.compile(r'^(?:#{1,4}\s+)?(?:Phase\s+(\d+)[:\s]+)(.+)', re.IGNORECASE)
    task_pattern = re.compile(r'^\s*(?:[-*]\s+\[([\sXx\-\!])\]|\d+\.)\s+(.+)', re.IGNORECASE)
    dod_pattern = re.compile(r'(?:definition\s+of\s+done|verification|exit\s+criteria)', re.IGNORECASE)
    
    for line_idx, line in enumerate(lines, 1):
        p_match = phase_pattern.match(line)
        if p_match:
            phase_num = int(p_match.group(1))
            phase_title = p_match.group(2).strip()
            current_phase = {
                "number": phase_num,
                "title": phase_title,
                "line": line_idx,
                "tasks": [],
                "has_dod": False
            }
            phases.append(current_phase)
            continue
            
        if current_phase:
            if dod_pattern.search(line):
                current_phase["has_dod"] = True
                
            t_match = task_pattern.match(line)
            if t_match:
                state_char = (t_match.group(1) or " ").strip().lower()
                state = "COMPLETED" if state_char == "x" else ("IN_PROGRESS" if state_char == "-" else ("BLOCKED" if state_char == "!" else "PENDING"))
                task_text = t_match.group(2).strip()
                files = extract_file_paths(task_text)
                
                # Check cognitive load: >2 files touched
                if len(files) > 2:
                    issues.append({
                        "severity": "WARNING",
                        "type": "COGNITIVE_LOAD_EXCEEDED",
                        "line": line_idx,
                        "message": f"Task touches {len(files)} files ({', '.join(files)}). Max recommended is 2 files per atomic task."
                    })
                    
                current_phase["tasks"].append({
                    "text": task_text,
                    "state": state,
                    "files": files,
                    "line": line_idx
                })

    if not phases:
        issues.append({
            "severity": "ERROR",
            "type": "NO_PHASES",
            "line": 1,
            "message": "No structured phases found. Expected '### Phase 1: [Title]' format."
        })
        return {
            "status": "FAIL",
            "phases_count": 0,
            "tasks_count": 0,
            "completed_count": 0,
            "progress_percent": 0,
            "issues": issues,
            "phases": []
        }

    total_tasks = sum(len(p["tasks"]) for p in phases)
    completed_tasks = sum(sum(1 for t in p["tasks"] if t["state"] == "COMPLETED") for p in phases)
    progress_pct = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
    
    for p in phases:
        if not p["has_dod"]:
            issues.append({
                "severity": "WARNING",
                "type": "MISSING_DOD",
                "line": p["line"],
                "message": f"Phase {p['number']} ('{p['title']}') is missing an explicit Definition of Done verification gate."
            })
            
    has_errors = any(i["severity"] == "ERROR" for i in issues)
    
    return {
        "status": "FAIL" if has_errors else "PASS",
        "phases_count": len(phases),
        "tasks_count": total_tasks,
        "completed_count": completed_tasks,
        "progress_percent": progress_pct,
        "issues": issues,
        "phases": phases
    }

def main():
    parser = argparse.ArgumentParser(description="Atomic Task Decomposer & Execution Engine.")
    parser.add_argument("plan_file", help="Path to markdown execution roadmap (or '-' for stdin)")
    parser.add_argument("--root", default=".", help="Root repository directory (default: .)")
    parser.add_argument("--json", action="store_true", help="Output execution status as JSON")
    args = parser.parse_args()
    
    if args.plan_file == "-":
        content = sys.stdin.read()
    else:
        if not os.path.exists(args.plan_file):
            sys.stderr.write(f"Error: Roadmap file '{args.plan_file}' not found.\n")
            sys.exit(1)
        with open(args.plan_file, "r", encoding="utf-8") as f:
            content = f.read()
            
    results = parse_roadmap(content, args.root)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n🚀 Execution Roadmap Progress: {results['completed_count']}/{results['tasks_count']} Tasks Completed ({results['progress_percent']}%)")
        print(f"Status: {results['status']} | Phases: {results['phases_count']}")
        
        if results["issues"]:
            print("\nAudit Findings:")
            for i in results["issues"]:
                print(f"  [{i['severity']}] Line {i['line']}: {i['message']}")
        else:
            print("  ✅ All tasks strictly comply with Low Cognitive Load Protocol (<=2 files/task).")
        print()
        
    sys.exit(0 if results["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
