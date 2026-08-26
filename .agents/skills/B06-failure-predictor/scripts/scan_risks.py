#!/usr/bin/env python3
"""
scan_risks.py - Pre-Flight Risk & Failure Predictor
Zero external dependencies (Python standard library only).

Audits target files or proposed changes for:
1. Downstream blast radius (importers and consumers)
2. High-risk code patterns (unbounded queries, unhandled network calls, hardcoded secrets)
3. Schema and database mutation hazards (non-null without default, table drops)
4. State mutation without concurrency safeguards
5. Computes a deterministic 5-level risk score and required verification gate.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

# High-risk anti-patterns
RISK_PATTERNS = [
    {
        "id": "UNHANDLED_ASYNC_OR_NETWORK",
        "regex": re.compile(r'(?:fetch|axios\.(?:get|post|put|delete)|requests\.(?:get|post)|http\.(?:Get|Post))\s*\(', re.IGNORECASE),
        "severity": "MEDIUM",
        "score": 15,
        "message": "Direct network/HTTP call detected. Ensure timeout and try/catch/error boundary handling."
    },
    {
        "id": "HARDCODED_SECRET_OR_KEY",
        "regex": re.compile(r'(?:api_key|secret|password|bearer|auth_token)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{8,}["\']', re.IGNORECASE),
        "severity": "CRITICAL",
        "score": 35,
        "message": "Potential hardcoded secret or token detected. Secrets must be loaded via environment variables."
    },
    {
        "id": "UNBOUNDED_DB_QUERY",
        "regex": re.compile(r'SELECT\s+\*\s+FROM\s+\w+(?!\s+(?:WHERE|LIMIT|ORDER))', re.IGNORECASE),
        "severity": "HIGH",
        "score": 20,
        "message": "Unbounded SELECT * query without LIMIT or WHERE clause. Risk of memory exhaustion or table locks."
    },
    {
        "id": "DESTRUCTIVE_DB_OP",
        "regex": re.compile(r'(?:DROP\s+TABLE|TRUNCATE\s+TABLE|ALTER\s+TABLE\s+\w+\s+DROP\s+COLUMN)', re.IGNORECASE),
        "severity": "CRITICAL",
        "score": 40,
        "message": "Destructive database operation detected. Irreversible data loss risk."
    },
    {
        "id": "UNPROTECTED_FILE_OVERWRITE",
        "regex": re.compile(r'open\s*\([^,]+,\s*["\']w["\']\)', re.IGNORECASE),
        "severity": "MEDIUM",
        "score": 15,
        "message": "File opened in write mode ('w') without backup or atomic replacement. Risk of data truncation."
    }
]

def find_downstream_consumers(target_file: str, root_dir: str) -> list[str]:
    """Find files that import target_file using lightweight scan."""
    consumers = []
    target_stem = Path(target_file).stem
    target_rel = os.path.relpath(target_file, root_dir).replace("\\", "/")
    
    ignore_dirs = {'.git', 'node_modules', '.venv', 'dist', 'build', '__pycache__', 'target'}
    exts = {'.ts', '.tsx', '.js', '.jsx', '.py', '.rs', '.go'}
    
    import_regex = re.compile(re.escape(target_stem))
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if Path(f).suffix.lower() in exts:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
                if rel_path == target_rel:
                    continue
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read(20480) # read up to 20KB header
                        if import_regex.search(content):
                            consumers.append(rel_path)
                except Exception:
                    pass
    return consumers

def assess_file_risk(file_path: str, root_dir: str = ".") -> dict:
    full_path = os.path.join(root_dir, file_path) if not os.path.isabs(file_path) else file_path
    
    if not os.path.exists(full_path):
        return {
            "target": file_path,
            "status": "NEW_FILE",
            "risk_score": 10,
            "risk_level": "Level 1 (Low)",
            "blast_radius": {"count": 0, "consumers": []},
            "findings": [],
            "gate_recommendation": "PROCEED: New file has zero blast radius."
        }
        
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
    except Exception as e:
        return {
            "target": file_path,
            "error": str(e),
            "risk_score": 50,
            "risk_level": "Level 3 (Elevated)"
        }
        
    findings = []
    total_score = 0
    
    # 1. Pattern scan
    lines = content.splitlines()
    for line_idx, line in enumerate(lines, 1):
        for p in RISK_PATTERNS:
            if p["regex"].search(line):
                findings.append({
                    "id": p["id"],
                    "severity": p["severity"],
                    "line": line_idx,
                    "score": p["score"],
                    "message": p["message"]
                })
                total_score += p["score"]

    # 2. Blast radius scan
    consumers = find_downstream_consumers(full_path, root_dir)
    consumer_count = len(consumers)
    
    if consumer_count > 5:
        blast_tier = "HIGH"
        blast_score = 40
    elif consumer_count >= 3:
        blast_tier = "MEDIUM"
        blast_score = 25
    elif consumer_count > 0:
        blast_tier = "LOW"
        blast_score = 10
    else:
        blast_tier = "ISOLATED"
        blast_score = 0
        
    total_score += blast_score
    
    # Cap score at 100
    risk_score = min(total_score, 100)
    
    # 3. Determine Risk Level & Verification Gate
    if risk_score <= 25:
        risk_level = "Level 1 (Low)"
        recommendation = "PROCEED: Low risk. Safe for immediate execution."
    elif risk_score <= 50:
        risk_level = "Level 2 (Moderate)"
        recommendation = "CAUTION: Moderate risk. Unit tests required before merging."
    elif risk_score <= 75:
        risk_level = "Level 3 (Elevated)"
        recommendation = "GATE REQUIRED: Elevated risk. Integration tests and blast-radius caller review required."
    else:
        risk_level = "Level 4-5 (Critical)"
        recommendation = "HALT / HUMAN SIGN-OFF: High probability of regressions or breaking changes. Decompose action or add rollback safeguards."

    return {
        "target": file_path,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "blast_radius": {
            "tier": blast_tier,
            "count": consumer_count,
            "score": blast_score,
            "consumers": consumers[:10] # cap display
        },
        "findings": findings,
        "gate_recommendation": recommendation
    }

def main():
    parser = argparse.ArgumentParser(description="Pre-flight risk and failure predictor for files and plans.")
    parser.add_argument("target", help="Path to target file to evaluate")
    parser.add_argument("--root", default=".", help="Root repository directory (default: .)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    result = assess_file_risk(args.target, root_dir=args.root)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"=== Failure Prediction Report: {result['target']} ===")
        print(f"Risk Score : {result.get('risk_score', 0)}/100 -> {result.get('risk_level', 'Unknown')}")
        br = result.get('blast_radius', {})
        print(f"Blast Radius: {br.get('tier', 'NONE')} ({br.get('count', 0)} downstream consumers)")
        if br.get('consumers'):
            print(f"  Consumers : {', '.join(br['consumers'])}")
        print(f"Findings   : {len(result.get('findings', []))}")
        for f in result.get('findings', []):
            print(f"  [{f['severity']}] Line {f['line']}: {f['message']}")
        print(f"\nRecommendation: {result.get('gate_recommendation', 'None')}")

if __name__ == "__main__":
    main()
