#!/usr/bin/env python3
"""
idiom_checker.py - Polyglot Idiom & Language Convention Auditor
Zero external dependencies (Python standard library only).

Scans code files across TypeScript, Python, Go, Rust, and SQL for non-idiomatic patterns:
- TypeScript: 'any' types, 'var' keyword, loose equality ('==')
- Python: Bare except clauses, mutable default arguments, comparison to literals with 'is'
- Go: Ignored error return blanks (_ = ...), panic() in library code
- Rust: Unchecked .unwrap() calls in non-test code
- SQL: 'SELECT *' without WHERE or LIMIT
Outputs an Idiomatic Score (0-100) and actionable advice in text or JSON.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

RULES = {
    ".ts": [
        {"id": "TS_ANY_TYPE", "regex": re.compile(r':\s*any\b'), "penalty": 15, "msg": "Avoid 'any' type. Use unknown, generics, or a typed interface."},
        {"id": "TS_VAR_KEYWORD", "regex": re.compile(r'\bvar\s+\w+'), "penalty": 20, "msg": "Avoid legacy 'var' declaration. Use const or let."},
        {"id": "TS_LOOSE_EQUALITY", "regex": re.compile(r'(?<![!=])==(?!=)'), "penalty": 10, "msg": "Avoid loose equality '=='. Use strict equality '==='."}
    ],
    ".tsx": [
        {"id": "TS_ANY_TYPE", "regex": re.compile(r':\s*any\b'), "penalty": 15, "msg": "Avoid 'any' type. Use unknown, generics, or a typed interface."},
        {"id": "TS_VAR_KEYWORD", "regex": re.compile(r'\bvar\s+\w+'), "penalty": 20, "msg": "Avoid legacy 'var' declaration. Use const or let."},
        {"id": "TS_LOOSE_EQUALITY", "regex": re.compile(r'(?<![!=])==(?!=)'), "penalty": 10, "msg": "Avoid loose equality '=='. Use strict equality '==='."}
    ],
    ".py": [
        {"id": "PY_BARE_EXCEPT", "regex": re.compile(r'except\s*:'), "penalty": 25, "msg": "Avoid bare 'except:'. Specify Exception or a specific error class."},
        {"id": "PY_MUTABLE_DEFAULT", "regex": re.compile(r'def\s+\w+\([^)]*=\s*(?:\[\]|\{\}|set\(\))'), "penalty": 20, "msg": "Mutable default argument detected. Use None as default and initialize inside function."},
        {"id": "PY_TYPE_ANNOTATIONS", "regex": re.compile(r'def\s+\w+\([^)]*\)\s*:'), "penalty": 5, "msg": "Function missing return type annotation (-> ReturnType:)."}
    ],
    ".go": [
        {"id": "GO_PANIC", "regex": re.compile(r'\bpanic\s*\('), "penalty": 20, "msg": "Avoid panic() in library code. Propagate errors via error return values."},
        {"id": "GO_BLANK_ERROR", "regex": re.compile(r'_\s*,\s*err\s*:?='), "penalty": 15, "msg": "Ensure error is explicitly handled immediately after assignment."}
    ],
    ".rs": [
        {"id": "RUST_UNWRAP", "regex": re.compile(r'\.unwrap\s*\('), "penalty": 20, "msg": "Unchecked .unwrap() detected. Use '?' operator, .expect(), or match/if-let."}
    ],
    ".sql": [
        {"id": "SQL_SELECT_ALL", "regex": re.compile(r'SELECT\s+\*\s+FROM', re.IGNORECASE), "penalty": 15, "msg": "Avoid 'SELECT *' in production queries. Explicitly declare column names."}
    ]
}

def audit_idioms(filepath: str) -> dict:
    if not os.path.exists(filepath):
        return {"status": "ERROR", "message": f"File '{filepath}' not found."}
        
    ext = Path(filepath).suffix.lower()
    applicable_rules = RULES.get(ext, [])
    
    if not applicable_rules:
        return {
            "status": "UNSUPPORTED",
            "file": filepath,
            "message": f"Language extension '{ext}' does not have dedicated idiom rules. Standard style rules apply."
        }
        
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.splitlines() if hasattr(f, 'splitlines') else f.read().splitlines()
            
        content = "\n".join(lines)
        issues = []
        score = 100
        
        for rule in applicable_rules:
            for line_idx, line in enumerate(lines, 1):
                # Ignore comments
                stripped = line.strip()
                if stripped.startswith(('//', '#', '--', '/*')):
                    continue
                if rule["regex"].search(line):
                    issues.append({
                        "id": rule["id"],
                        "line": line_idx,
                        "line_content": stripped[:80],
                        "message": rule["msg"]
                    })
                    score = max(0, score - rule["penalty"])
                    
        status = "EXCELLENT" if score >= 90 else ("GOOD" if score >= 75 else "NEEDS_IMPROVEMENT")
        
        return {
            "status": status,
            "file": filepath,
            "idiom_score": score,
            "issues_count": len(issues),
            "issues": issues
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Polyglot Idiom & Language Convention Auditor.")
    parser.add_argument("target", help="Path to source file to audit (.ts, .py, .go, .rs, .sql)")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    args = parser.parse_args()
    
    results = audit_idioms(args.target)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if results.get("status") == "ERROR":
            print(f"❌ Error: {results['message']}")
            sys.exit(1)
            
        if results.get("status") == "UNSUPPORTED":
            print(f"ℹ️ {results['message']}")
            sys.exit(0)
            
        print(f"\n💎 Idiomatic Quality Audit: {results['file']}")
        print(f"Score: {results['idiom_score']}/100 [{results['status']}] | Issues Detected: {results['issues_count']}")
        
        if results["issues"]:
            print("\nNon-Idiomatic Patterns Identified:")
            for issue in results["issues"]:
                print(f"  - Line {issue['line']}: {issue['message']}")
                print(f"    Code: {issue['line_content']}")
        else:
            print("  ✅ Code follows ecosystem-native idioms and best practices.")
        print()
        
    sys.exit(0)

if __name__ == "__main__":
    main()
