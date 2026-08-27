#!/usr/bin/env python3
"""
diff_guard.py - Atomic Edit Guard & Cognitive Load Monitor
Zero external dependencies (Python standard library only).

Monitors proposed code edits to prevent runaway blast radius:
1. Validates diff size (warns if lines changed > 80 lines for a single atomic task)
2. Validates file touch limits (warns if > 2 files are modified in a single task)
3. Basic syntax & bracket balance sanity check
4. Outputs pass/warning verdict in text or JSON
"""

import sys
import os
import re
import json
import argparse
import subprocess

def check_bracket_balance(content: str) -> bool:
    """Basic balance check for braces and brackets to catch truncated writes."""
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    
    # Strip string literals and comments to avoid false positives
    cleaned = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', content)
    cleaned = re.sub(r'//.*$|/\*[\s\S]*?\*/|#.*$', '', cleaned, flags=re.MULTILINE)
    
    for char in cleaned:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0

def analyze_git_diff(root_dir: str = ".") -> dict:
    """Analyze current unstaged or cached git diff."""
    try:
        proc = subprocess.run(
            ["git", "diff", "--numstat"],
            cwd=root_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        lines = proc.stdout.strip().splitlines()
        
        files_modified = []
        total_added = 0
        total_deleted = 0
        
        for line in lines:
            parts = line.split('\t')
            if len(parts) >= 3:
                added = int(parts[0]) if parts[0] != '-' else 0
                deleted = int(parts[1]) if parts[1] != '-' else 0
                filepath = parts[2]
                total_added += added
                total_deleted += deleted
                files_modified.append({
                    "file": filepath,
                    "added": added,
                    "deleted": deleted
                })
                
        total_delta = total_added + total_deleted
        issues = []
        
        if len(files_modified) > 2:
            issues.append(f"Cognitive load warning: {len(files_modified)} files touched (exceeds atomic limit of 2 files).")
            
        if total_delta > 80:
            issues.append(f"Diff size warning: {total_delta} lines modified (exceeds recommended atomic threshold of 80 lines).")
            
        status = "PASS" if not issues else "WARN"
        
        return {
            "status": status,
            "files_count": len(files_modified),
            "lines_added": total_added,
            "lines_deleted": total_deleted,
            "total_delta": total_delta,
            "files": files_modified,
            "issues": issues
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to execute git diff: {str(e)}"
        }

def analyze_file(filepath: str) -> dict:
    """Analyze a single target file for basic syntax sanity."""
    if not os.path.exists(filepath):
        return {"status": "ERROR", "message": f"File '{filepath}' not found."}
        
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        balanced = check_bracket_balance(content)
        lines_count = len(content.splitlines())
        
        return {
            "status": "PASS" if balanced else "WARN",
            "file": filepath,
            "lines_count": lines_count,
            "syntax_balance": "OK" if balanced else "UNBALANCED_BRACKETS",
            "issues": [] if balanced else ["Unbalanced brackets or truncated syntax detected."]
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Diff Guard - Atomic Edit & Cognitive Load Monitor.")
    parser.add_argument("--file", help="Path to single file to verify syntax balance")
    parser.add_argument("--root", default=".", help="Root repository directory (default: .)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()
    
    if args.file:
        results = analyze_file(args.file)
    else:
        results = analyze_git_diff(args.root)
        
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if "message" in results and results["status"] == "ERROR":
            print(f"❌ Error: {results['message']}")
            sys.exit(1)
            
        print(f"\n🛡️ Diff Guard Status: {results['status']}")
        if "files_count" in results:
            print(f"Files Modified: {results['files_count']} | Lines Delta: {results['total_delta']} (+{results['lines_added']} / -{results['lines_deleted']})")
        if results.get("issues"):
            print("Audit Warnings:")
            for issue in results["issues"]:
                print(f"  ⚠️ {issue}")
        else:
            print("  ✅ Edits strictly comply with atomic modification protocol.")
        print()
        
    sys.exit(0 if results.get("status") == "PASS" else 0)

if __name__ == "__main__":
    main()
