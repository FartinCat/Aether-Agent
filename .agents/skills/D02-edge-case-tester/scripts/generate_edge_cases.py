#!/usr/bin/env python3
"""
generate_edge_cases.py - Adversarial Boundary & Edge-Case Payload Generator
Zero external dependencies (Python standard library only).

Generates boundary-value test matrices across 5 core dimensions:
1. Null, Undefined & Empty states
2. Numeric boundary extremes (0, negative, MAX_SAFE_INTEGER, NaN)
3. String & Payload extremes (10k chars, multi-byte emojis, SQL/XSS probes)
4. Temporal & Race condition states (simultaneous submissions, clock skew)
5. Network failure modes (429 rate limit, 504 timeout, corrupted JSON)
Outputs test matrices in Markdown or structured JSON.
"""

import sys
import os
import re
import json
import argparse

BOUNDARY_MATRICES = {
    "strings": [
        {"name": "Empty String", "value": "", "scenario": "Field submitted as empty string"},
        {"name": "Whitespace Only", "value": "   \t\n   ", "scenario": "Field contains only un-trimmed whitespace"},
        {"name": "Multi-byte Unicode / Emoji", "value": "🚀 👨‍👩‍👦 𝓤𝓷𝓲𝓬𝓸𝓭𝓮", "scenario": "4-byte UTF-8 characters exceeding single-byte buffers"},
        {"name": "Buffer Overflow (10KB)", "value": "A" * 10240, "scenario": "Oversized payload to verify memory bounds"},
        {"name": "SQL Injection Probe", "value": "' OR '1'='1' --", "scenario": "Sanitization and parameterization check"},
        {"name": "XSS Script Probe", "value": "<script>alert('xss')</script>", "scenario": "HTML entity escaping check"}
    ],
    "numbers": [
        {"name": "Zero Value", "value": 0, "scenario": "Falsy numerical zero check"},
        {"name": "Negative Integer", "value": -1, "scenario": "Unsigned expectation violation"},
        {"name": "Max Safe Integer", "value": 9007199254740991, "scenario": "Integer overflow boundary (JS MAX_SAFE_INTEGER)"},
        {"name": "Floating Point Precision", "value": 0.1 + 0.2, "scenario": "Floating point precision loss (0.30000000000000004)"},
        {"name": "NaN / Non-numeric", "value": "NaN", "scenario": "Unparseable numeric conversion check"}
    ],
    "collections": [
        {"name": "Null Reference", "value": None, "scenario": "Null input check"},
        {"name": "Empty Array / List", "value": [], "scenario": "Collection with 0 items"},
        {"name": "Massive Array (5000 items)", "value": "[5000 items]", "scenario": "Batch operation memory stress"},
        {"name": "Duplicate Elements", "value": ["id_1", "id_1"], "scenario": "Idempotency and deduplication check"}
    ],
    "network_failures": [
        {"name": "HTTP 429 Rate Limited", "status": 429, "scenario": "Verify retry-after header handling and user notification"},
        {"name": "HTTP 504 Gateway Timeout", "status": 504, "scenario": "Verify client timeout threshold and exponential retry"},
        {"name": "Malformed JSON Response", "body": "<html>502 Bad Gateway</html>", "scenario": "Non-JSON response crash prevention"}
    ]
}

def generate_matrix(entity_name: str, field_types: dict = None) -> dict:
    return {
        "target_entity": entity_name,
        "boundary_checks": BOUNDARY_MATRICES
    }

def format_markdown(data: dict) -> str:
    lines = [
        f"### 🛡️ Adversarial Edge-Case Matrix: `{data['target_entity']}`",
        "\n#### 1. String & Payload Boundary Tests:",
        "| Test Case | Payload Description | Expected Behavior |",
        "| :--- | :--- | :--- |"
    ]
    for item in data["boundary_checks"]["strings"]:
        lines.append(f"| **{item['name']}** | {item['scenario']} | Reject with 400 Bad Request or sanitize safely |")
        
    lines.append("\n#### 2. Numeric Extreme Tests:")
    lines.append("| Test Case | Payload Description | Expected Behavior |")
    lines.append("| :--- | :--- | :--- |")
    for item in data["boundary_checks"]["numbers"]:
        lines.append(f"| **{item['name']}** | {item['scenario']} | Handle gracefully without NaN propagation |")
        
    lines.append("\n#### 3. Collection & Nullability Tests:")
    lines.append("| Test Case | Payload Description | Expected Behavior |")
    lines.append("| :--- | :--- | :--- |")
    for item in data["boundary_checks"]["collections"]:
        lines.append(f"| **{item['name']}** | {item['scenario']} | Return empty result set or explicit validation error |")
        
    lines.append("\n#### 4. Network & Degradation Scenarios:")
    lines.append("| Failure Mode | Trigger | Expected Degradation |")
    lines.append("| :--- | :--- | :--- |")
    for item in data["boundary_checks"]["network_failures"]:
        lines.append(f"| **{item['name']}** | {item['scenario']} | Exponential backoff retry up to 3x, fallback UI alert |")
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Adversarial Edge-Case & Boundary Payload Generator.")
    parser.add_argument("target", help="Name of target function, route, or entity (e.g., 'UserRegistration' or 'createOrder')")
    parser.add_argument("--json", action="store_true", help="Output matrix as JSON")
    args = parser.parse_args()
    
    matrix = generate_matrix(args.target)
    
    if args.json:
        print(json.dumps(matrix, indent=2))
    else:
        print(format_markdown(matrix))

if __name__ == "__main__":
    main()
