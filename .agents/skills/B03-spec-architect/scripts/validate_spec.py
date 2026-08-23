#!/usr/bin/env python3
"""
validate_spec.py - Formal Specification & Contract Validator
Zero external dependencies (Python standard library only).

Audits markdown specifications (SPEC.md) for completeness against 5 core pillars:
1. Acceptance Criteria (Given/When/Then or Verifiable DoD)
2. Data Models & Type Contracts
3. API / Interface Signatures & Status Codes
4. State Transitions / Lifecycle
5. Error Taxonomy & Edge Case Handling
Also enforces the Independence Law: flags any raw absolute file paths.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

REQUIRED_PILLARS = [
    {
        "id": "ACCEPTANCE_CRITERIA",
        "name": "Acceptance Criteria",
        "pattern": re.compile(r'(?:acceptance\s+criteria|given\s+.+when\s+.+then|definition\s+of\s+done)', re.IGNORECASE),
        "weight": 20,
        "advice": "Define explicit Given/When/Then scenarios or verifiable acceptance criteria."
    },
    {
        "id": "DATA_MODELS",
        "name": "Data Models & Schemas",
        "pattern": re.compile(r'(?:interface|type|struct|schema|model|table)\s+[\w\-]+', re.IGNORECASE),
        "weight": 20,
        "advice": "Include typed schemas, field names, and nullability constraints."
    },
    {
        "id": "API_OR_INTERFACE",
        "name": "API & Interface Signatures",
        "pattern": re.compile(r'(?:endpoint|route|function|method|signature|request|response|status\s+code)', re.IGNORECASE),
        "weight": 20,
        "advice": "Specify function signatures, API endpoints, request/response structures, and HTTP status codes."
    },
    {
        "id": "STATE_OR_LIFECYCLE",
        "name": "State Transitions / Lifecycle",
        "pattern": re.compile(r'(?:state\s+transition|lifecycle|status\s*[:=]|enum|workflow)', re.IGNORECASE),
        "weight": 20,
        "advice": "Document valid lifecycle state transitions (e.g. DRAFT -> ACTIVE -> ARCHIVED)."
    },
    {
        "id": "ERROR_TAXONOMY",
        "name": "Error Taxonomy & Recovery",
        "pattern": re.compile(r'(?:error\s+code|exception|unhappy\s+path|failure\s+mode|fallback|timeout)', re.IGNORECASE),
        "weight": 20,
        "advice": "Map explicit error codes, failure scenarios, and graceful user recovery fallbacks."
    }
]

def check_raw_paths(text: str) -> list[str]:
    """Flag any hardcoded local system paths violating portability."""
    path_regex = re.compile(r'(?:[a-zA-Z]:[\\/]|file:\/\/\/[a-zA-Z]:)', re.IGNORECASE)
    matches = path_regex.findall(text)
    return matches

def validate_specification(spec_text: str) -> dict:
    score = 0
    passed_pillars = []
    missing_pillars = []
    
    for pillar in REQUIRED_PILLARS:
        if pillar["pattern"].search(spec_text):
            score += pillar["weight"]
            passed_pillars.append(pillar["name"])
        else:
            missing_pillars.append({
                "pillar": pillar["name"],
                "advice": pillar["advice"]
            })
            
    raw_path_violations = check_raw_paths(spec_text)
    if raw_path_violations:
        score = max(0, score - 25)
        
    status = "APPROVED" if score >= 80 and not raw_path_violations else ("NEEDS_REVISION" if score >= 50 else "REJECTED")
    
    return {
        "status": status,
        "health_score": score,
        "passed_pillars": passed_pillars,
        "missing_pillars": missing_pillars,
        "raw_path_violations": raw_path_violations
    }

def main():
    parser = argparse.ArgumentParser(description="Validate technical specifications for completeness and portability.")
    parser.add_argument("spec_file", help="Path to markdown specification file (or '-' for stdin)")
    parser.add_argument("--json", action="store_true", help="Output validation results as JSON")
    args = parser.parse_args()
    
    if args.spec_file == "-":
        content = sys.stdin.read()
    else:
        if not os.path.exists(args.spec_file):
            sys.stderr.write(f"Error: Specification file '{args.spec_file}' not found.\n")
            sys.exit(1)
        with open(args.spec_file, "r", encoding="utf-8") as f:
            content = f.read()
            
    results = validate_specification(content)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n📋 Specification Health Audit: {results['health_score']}/100 [{results['status']}]")
        print("Passed Pillars:")
        for p in results["passed_pillars"]:
            print(f"  ✅ {p}")
            
        if results["missing_pillars"]:
            print("\nMissing Pillars:")
            for m in results["missing_pillars"]:
                print(f"  ⚠️ {m['pillar']}: {m['advice']}")
                
        if results["raw_path_violations"]:
            print(f"\n❌ Portability Violation: Found {len(results['raw_path_violations'])} hardcoded system paths!")
            
        print()
        
    sys.exit(0 if results["status"] == "APPROVED" else 1)

if __name__ == "__main__":
    main()
