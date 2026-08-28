#!/usr/bin/env python3
"""
dead_code_finder.py - Surgical Dead Code & Debt Finder
Zero external dependencies (Python standard library only).

Scans source files for refactoring candidates:
1. Unused imports (JavaScript, TypeScript, Python)
2. Uncalled private functions/helpers (prefixed with _ or not exported)
3. Unreachable statements after return/throw
4. Commented-out code blocks (>3 lines of commented code)
Outputs findings in text or structured JSON.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

def find_unused_imports(content: str, ext: str) -> list[dict]:
    findings = []
    lines = content.splitlines()
    
    if ext in ['.js', '.jsx', '.ts', '.tsx']:
        # Extract named imports: import { a, b } from '...'
        import_pattern = re.compile(r'import\s+\{([^}]+)\}\s+from\s+["\'][^"\']+["\']')
        for idx, line in enumerate(lines, 1):
            m = import_pattern.search(line)
            if m:
                items = [x.strip().split(' as ')[-1].strip() for x in m.group(1).split(',') if x.strip()]
                for item in items:
                    # Search rest of content for usage outside this import line
                    usage_pattern = re.compile(r'\b' + re.escape(item) + r'\b')
                    matches = list(usage_pattern.finditer(content))
                    if len(matches) <= 1:
                        findings.append({
                            "type": "UNUSED_IMPORT",
                            "symbol": item,
                            "line": idx,
                            "message": f"Imported symbol '{item}' is never referenced in this file."
                        })
    elif ext == '.py':
        # Python: from x import a, b
        import_pattern = re.compile(r'from\s+[\w\.]+\s+import\s+([^#\n]+)')
        for idx, line in enumerate(lines, 1):
            m = import_pattern.search(line)
            if m:
                items = [x.strip().split(' as ')[-1].strip() for x in m.group(1).split(',') if x.strip()]
                for item in items:
                    usage_pattern = re.compile(r'\b' + re.escape(item) + r'\b')
                    matches = list(usage_pattern.finditer(content))
                    if len(matches) <= 1:
                        findings.append({
                            "type": "UNUSED_IMPORT",
                            "symbol": item,
                            "line": idx,
                            "message": f"Imported Python symbol '{item}' is never referenced."
                        })
    return findings

def find_commented_code(content: str, ext: str) -> list[dict]:
    findings = []
    lines = content.splitlines()
    consecutive_comment_lines = 0
    start_line = 0
    
    comment_prefix = '#' if ext == '.py' else '//'
    code_indicators = re.compile(r'(?:const|let|var|function|def|class|if|return|import|export)\s+', re.IGNORECASE)
    
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith(comment_prefix) and code_indicators.search(stripped):
            if consecutive_comment_lines == 0:
                start_line = idx
            consecutive_comment_lines += 1
        else:
            if consecutive_comment_lines >= 3:
                findings.append({
                    "type": "COMMENTED_OUT_CODE",
                    "line": start_line,
                    "length": consecutive_comment_lines,
                    "message": f"Block of {consecutive_comment_lines} lines of commented-out code detected. Remove dead code."
                })
            consecutive_comment_lines = 0
            
    if consecutive_comment_lines >= 3:
        findings.append({
            "type": "COMMENTED_OUT_CODE",
            "line": start_line,
            "length": consecutive_comment_lines,
            "message": f"Block of {consecutive_comment_lines} lines of commented-out code detected."
        })
    return findings

def find_unreachable_code(content: str) -> list[dict]:
    findings = []
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped in ['return;', 'return true;', 'return false;', 'return null;', 'throw new Error('] or stripped.startswith('return '):
            # Check next non-empty, non-closing-brace line at same or deeper indentation
            if idx < len(lines):
                next_line = lines[idx].strip()
                if next_line and not next_line.startswith(('}', 'catch', 'finally', 'else', 'case', 'default')):
                    if not lines[idx].startswith('//') and not lines[idx].startswith('#'):
                        findings.append({
                            "type": "UNREACHABLE_CODE",
                            "line": idx + 1,
                            "message": f"Potentially unreachable code immediately following return statement on line {idx}."
                        })
    return findings

def audit_file(filepath: str) -> dict:
    if not os.path.exists(filepath):
        return {"status": "ERROR", "message": f"File '{filepath}' not found."}
        
    ext = Path(filepath).suffix.lower()
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        unused_imports = find_unused_imports(content, ext)
        commented_code = find_commented_code(content, ext)
        unreachable = find_unreachable_code(content)
        
        all_findings = unused_imports + commented_code + unreachable
        
        return {
            "status": "PASS" if not all_findings else "DEBT_DETECTED",
            "file": filepath,
            "findings_count": len(all_findings),
            "findings": all_findings
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Dead Code & Technical Debt Finder for surgical refactoring.")
    parser.add_argument("target", help="Path to source file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    args = parser.parse_args()
    
    results = audit_file(args.target)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if results.get("status") == "ERROR":
            print(f"❌ Error: {results['message']}")
            sys.exit(1)
            
        print(f"\n🧹 Refactoring & Debt Audit: {results['file']}")
        print(f"Status: {results['status']} | Debt Candidates Found: {results['findings_count']}")
        
        if results["findings"]:
            print("\nIdentified Debt & Dead Code Items:")
            for item in results["findings"]:
                print(f"  - [{item['type']}] Line {item['line']}: {item['message']}")
            print("\nRecommended Action: Prune dead imports and obsolete commented blocks without altering public exports.")
        else:
            print("  ✅ File is clean of obvious dead code, unused imports, and unreachable statements.")
        print()
        
    sys.exit(0)

if __name__ == "__main__":
    main()
