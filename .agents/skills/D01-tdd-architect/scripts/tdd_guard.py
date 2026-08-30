#!/usr/bin/env python3
"""
tdd_guard.py - Test-Driven Development (TDD) Quality & Assertion Guard
Zero external dependencies (Python standard library only).

Audits test files for TDD integrity:
1. Validates test file existence corresponding to source file
2. Checks assertion density (ensures tests actually verify outcomes)
3. Detects empty / vacuous test blocks without assertions
4. Validates descriptive test naming (e.g., 'should ... when ...' or 'test_...')
Outputs TDD Health Score (0-100) and actionable findings in text or JSON.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

ASSERTION_PATTERNS = re.compile(
    r'\b(?:assert|expect\(|assert_eq!|assert_ne!|assertEqual|assertTrue|assertFalse|assert_called|toHaveLength|toBe|toEqual|toThrow)\b',
    re.IGNORECASE
)

TEST_BLOCK_PATTERNS = {
    "js_ts": re.compile(r'(?:it|test)\s*\(\s*["\']([^"\']+)["\']\s*,\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{', re.MULTILINE),
    "py": re.compile(r'def\s+(test_\w+)\s*\(', re.MULTILINE),
    "go": re.compile(r'func\s+(Test\w+)\s*\(', re.MULTILINE),
    "rs": re.compile(r'#\[test\]\s+(?:async\s+)?fn\s+(\w+)\s*\(', re.MULTILINE)
}

def audit_test_file(filepath: str) -> dict:
    if not os.path.exists(filepath):
        return {"status": "ERROR", "message": f"Test file '{filepath}' not found."}
        
    ext = Path(filepath).suffix.lower()
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        lines = content.splitlines()
        
        # Count assertions
        assertions = list(ASSERTION_PATTERNS.finditer(content))
        assertion_count = len(assertions)
        
        # Identify tests
        test_names = []
        if ext in ['.js', '.jsx', '.ts', '.tsx']:
            test_names = [m.group(1) for m in TEST_BLOCK_PATTERNS["js_ts"].finditer(content)]
        elif ext == '.py':
            test_names = [m.group(1) for m in TEST_BLOCK_PATTERNS["py"].finditer(content)]
        elif ext == '.go':
            test_names = [m.group(1) for m in TEST_BLOCK_PATTERNS["go"].finditer(content)]
        elif ext == '.rs':
            test_names = [m.group(1) for m in TEST_BLOCK_PATTERNS["rs"].finditer(content)]
            
        test_count = len(test_names)
        issues = []
        score = 100
        
        if test_count == 0:
            issues.append("No recognizable test functions or blocks found in file.")
            score -= 50
        else:
            assertions_per_test = assertion_count / test_count if test_count > 0 else 0
            if assertions_per_test < 1.0:
                issues.append(f"Low assertion density: {assertion_count} assertions across {test_count} tests ({assertions_per_test:.1f} per test). Potential vacuous tests.")
                score -= 30
            elif assertions_per_test > 8.0:
                issues.append(f"High assertion density: {assertions_per_test:.1f} assertions per test. Consider breaking into focused unit tests.")
                score -= 10
                
        # Naming conventions
        vague_names = [name for name in test_names if name.lower() in ['test', 'works', 'test1', 'check', 'run']]
        if vague_names:
            issues.append(f"Vague test names detected ({', '.join(vague_names)}). Use descriptive Given/When/Then or 'should ... when ...' phrasing.")
            score -= 15
            
        status = "EXCELLENT" if score >= 90 else ("GOOD" if score >= 70 else "NEEDS_REVISION")
        
        return {
            "status": status,
            "file": filepath,
            "tdd_score": max(0, score),
            "test_count": test_count,
            "assertion_count": assertion_count,
            "assertions_per_test": round(assertion_count / test_count, 1) if test_count > 0 else 0,
            "issues": issues
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def find_test_for_source(source_path: str, root_dir: str = ".") -> str | None:
    """Attempt to locate existing test file for a given source file."""
    src = Path(source_path)
    stem = src.stem
    ext = src.suffix
    
    candidates = [
        src.with_name(f"{stem}.test{ext}"),
        src.with_name(f"{stem}.spec{ext}"),
        src.with_name(f"test_{stem}{ext}"),
        Path(root_dir) / "tests" / f"{stem}.test{ext}",
        Path(root_dir) / "tests" / f"test_{stem}{ext}"
    ]
    
    for c in candidates:
        if c.exists():
            return str(c)
    return None

def main():
    parser = argparse.ArgumentParser(description="TDD Quality & Assertion Guard.")
    parser.add_argument("target", help="Path to test file (or source file with --for-source)")
    parser.add_argument("--for-source", action="store_true", help="Find and audit test corresponding to target source file")
    parser.add_argument("--json", action="store_true", help="Output audit results as JSON")
    args = parser.parse_args()
    
    target_test_file = args.target
    if args.for_source:
        discovered = find_test_for_source(args.target)
        if not discovered:
            res = {
                "status": "MISSING_TEST",
                "source_file": args.target,
                "message": f"No corresponding test file found for '{args.target}'. TDD Red phase requires authoring test first."
            }
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"\n❌ TDD Red Phase Alert: No test file found for '{args.target}'!")
                print("Write a failing test before implementing production code.\n")
            sys.exit(1)
        target_test_file = discovered
        
    results = audit_test_file(target_test_file)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if results.get("status") == "ERROR":
            print(f"❌ Error: {results['message']}")
            sys.exit(1)
            
        print(f"\n🧪 TDD Test Audit: {results['file']}")
        print(f"TDD Health Score: {results['tdd_score']}/100 [{results['status']}]")
        print(f"Tests Defined: {results['test_count']} | Total Assertions: {results['assertion_count']} (~{results['assertions_per_test']} per test)")
        
        if results["issues"]:
            print("\nTDD Improvement Recommendations:")
            for issue in results["issues"]:
                print(f"  ⚠️ {issue}")
        else:
            print("  ✅ Test suite exhibits healthy assertion density and clear naming.")
        print()
        
    sys.exit(0 if results["tdd_score"] >= 70 else 1)

if __name__ == "__main__":
    main()
