#!/usr/bin/env python3
"""
plan_linter.py - Static Linter & Cognitive Load Validator for Agent Plans
Zero external dependencies (Python standard library only).

Validates:
1. Phased sequencing (Phase 1, Phase 2, ...)
2. Atomic task scope (<2 files touched per task)
3. File path existence (flags non-existent files unless tagged [NEW])
4. Definition of Done (DoD) verification criteria per phase
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
    # Extract backticked paths first
    backticked = re.findall(r'`([^`]+)`', text)
    tokens = re.findall(r'[\w\-./\\]+', text)
    candidates = set(backticked + tokens)
    
    files = []
    for c in candidates:
        # Ignore pure numbers or versions like 2.1, 1.0.0
        if re.match(r'^\d+(?:\.\d+)+$', c):
            continue
        ext = Path(c).suffix.lower()
        if ext in FILE_EXTENSIONS:
            files.append(c)
        elif ('/' in c or '\\' in c) and '.' in c and not c.startswith('http'):
            files.append(c)
    return sorted(list(set(files)))

def lint_plan(plan_text: str, root_dir: str = ".") -> dict:
    lines = plan_text.splitlines()
    phases = []
    current_phase = None
    issues = []
    
    # 1. Parse phases and tasks
    phase_pattern = re.compile(r'^(?:#{1,4}\s+)?(?:Phase\s+(\d+)[:\s]+)(.+)', re.IGNORECASE)
    task_pattern = re.compile(r'^\s*(?:[-*]\s+\[[\sXx]\]|\d+\.)\s+(.+)', re.IGNORECASE)
    dod_pattern = re.compile(r'(?:definition\s+of\s+done|verification|exit\s+criteria)', re.IGNORECASE)
    
    for line_idx, line in enumerate(lines, 1):
        p_match = phase_pattern.match(line)
        if p_match:
            phase_num = p_match.group(1)
            phase_title = p_match.group(2).strip()
            current_phase = {
                "number": int(phase_num),
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
                task_text = t_match.group(1).strip()
                current_phase["tasks"].append({
                    "text": task_text,
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
            "issues": issues
        }

    total_tasks = sum(len(p["tasks"]) for p in phases)
    
    # 2. Check each phase for Definition of Done
    for p in phases:
        if not p["has_dod"]:
            issues.append({
                "severity": "WARN",
                "type": "MISSING_DOD",
                "line": p["line"],
                "message": f"Phase {p['number']} ('{p['title']}') lacks an explicit 'Definition of Done' or 'Verification' gate."
            })
            
        if not p["tasks"]:
            issues.append({
                "severity": "WARN",
                "type": "EMPTY_PHASE",
                "line": p["line"],
                "message": f"Phase {p['number']} ('{p['title']}') has no executable checklist tasks."
            })

    # 3. Check atomic scope and file references per task
    for p in phases:
        for t in p["tasks"]:
            target_files = extract_file_paths(t["text"])
            
            # Cognitive load rule: Max 2 source files per task
            if len(target_files) > 2:
                issues.append({
                    "severity": "WARN",
                    "type": "COGNITIVE_LOAD_VIOLATION",
                    "line": t["line"],
                    "message": f"Task touches {len(target_files)} files ({', '.join(target_files)}). Violates Low Cognitive Load rule (>2 files). Decompose into sub-tasks."
                })
                
            # Verify existence or [NEW] tag
            is_new = any(kw in t["text"].lower() for kw in ["[new]", "(new)", "create", "initialize"])
            for f in target_files:
                if not is_new:
                    # check if path exists relative to root_dir
                    full_path = os.path.join(root_dir, f)
                    if not os.path.exists(full_path):
                        # also check if basename exists in repo
                        issues.append({
                            "severity": "INFO",
                            "type": "FILE_NOT_FOUND",
                            "line": t["line"],
                            "message": f"File '{f}' does not exist on disk. If this is a new file, mark with [NEW]."
                        })

    status = "FAIL" if any(i["severity"] == "ERROR" for i in issues) else ("WARN" if any(i["severity"] == "WARN" for i in issues) else "PASS")
    
    return {
        "status": status,
        "phases_count": len(phases),
        "tasks_count": total_tasks,
        "issues": issues
    }

def main():
    parser = argparse.ArgumentParser(description="Lint and validate task plans for atomic cognitive load compliance.")
    parser.add_argument("plan_file", help="Path to markdown plan file (or '-' to read from stdin)")
    parser.add_argument("--root", default=".", help="Root repository directory for path checks (default: .)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    if args.plan_file == "-":
        plan_text = sys.stdin.read()
    else:
        if not os.path.isfile(args.plan_file):
            print(f"Error: File '{args.plan_file}' not found.", file=sys.stderr)
            sys.exit(1)
        with open(args.plan_file, "r", encoding="utf-8", errors="replace") as f:
            plan_text = f.read()

    result = lint_plan(plan_text, root_dir=args.root)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"=== Plan Linter Results: {result['status']} ===")
        print(f"Phases: {result['phases_count']} | Total Tasks: {result['tasks_count']}")
        print(f"Issues: {len(result['issues'])}")
        for iss in result["issues"]:
            prefix = f"[{iss['severity']}] (Line {iss['line']})"
            print(f"  {prefix:22} {iss['type']}: {iss['message']}")
            
    if result["status"] == "FAIL":
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
