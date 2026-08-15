#!/usr/bin/env python3
"""
scan_imports.py — Lightweight, zero-dependency import & blast-radius analyzer.
Self-contained helper for the A04-dependency-mapper skill.
Crawls JS/TS, Python, and Rust files to map forward and reverse dependencies.
"""

import os
import sys
import re
import json
from pathlib import Path
from collections import defaultdict

IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "target", "dist", "build", ".next", ".turbo", ".idea", ".vscode"
}

# Regex patterns for various languages
JS_TS_PATTERNS = [
    re.compile(r'''(?:import|export)\s+(?:.*?from\s+)?['"]([^'"]+)['"]'''),
    re.compile(r'''require\s*\(\s*['"]([^'"]+)['"]\s*\)'''),
    re.compile(r'''import\s*\(\s*['"]([^'"]+)['"]\s*\)''')
]

PY_PATTERNS = [
    re.compile(r'''^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)''', re.MULTILINE)
]

FILE_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py",
    ".rs",
    ".go"
}

def resolve_import(source_file, import_str, root):
    """Attempt to resolve a relative import to an actual file on disk."""
    if not (import_str.startswith(".") or import_str.startswith("/")):
        # Package or alias import
        return None

    src_dir = os.path.dirname(source_file)
    candidate_base = os.path.normpath(os.path.join(src_dir, import_str))

    # Direct match (e.g. import './utils.js')
    if os.path.isfile(candidate_base):
        return os.path.relpath(candidate_base, root).replace("\\", "/")

    # Try common extensions
    for ext in [".ts", ".tsx", ".js", ".jsx", ".py"]:
        with_ext = candidate_base + ext
        if os.path.isfile(with_ext):
            return os.path.relpath(with_ext, root).replace("\\", "/")

    # Try index files (barrel imports)
    for ext in [".ts", ".tsx", ".js", ".jsx"]:
        index_file = os.path.join(candidate_base, "index" + ext)
        if os.path.isfile(index_file):
            return os.path.relpath(index_file, root).replace("\\", "/")

    return None

def build_graph(root_dir):
    """Build forward and reverse dependency mappings across the project."""
    root = Path(root_dir).resolve()
    forward_graph = defaultdict(set)
    reverse_graph = defaultdict(set)
    external_deps = defaultdict(set)
    all_files = set()

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in FILE_EXTENSIONS:
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(full_path, root).replace("\\", "/")
                all_files.add(rel_path)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                except Exception:
                    continue

                if ext in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
                    for pat in JS_TS_PATTERNS:
                        for match in pat.findall(content):
                            resolved = resolve_import(full_path, match, root)
                            if resolved:
                                forward_graph[rel_path].add(resolved)
                                reverse_graph[resolved].add(rel_path)
                            else:
                                if not match.startswith("."):
                                    pkg = match.split("/")[0] if not match.startswith("@") else "/".join(match.split("/")[:2])
                                    external_deps[rel_path].add(pkg)

                elif ext == ".py":
                    for pat in PY_PATTERNS:
                        for match in pat.findall(content):
                            # Check if matches local python file
                            parts = match.split(".")
                            cand = os.path.join(dirpath, *parts) + ".py"
                            if os.path.isfile(cand):
                                resolved = os.path.relpath(cand, root).replace("\\", "/")
                                forward_graph[rel_path].add(resolved)
                                reverse_graph[resolved].add(rel_path)
                            else:
                                external_deps[rel_path].add(parts[0])

    return root, forward_graph, reverse_graph, external_deps, all_files

def analyze_target(target_path, root_dir="."):
    root, forward, reverse, external, all_files = build_graph(root_dir)
    target_rel = os.path.normpath(target_path).replace("\\", "/")
    if os.path.isabs(target_rel):
        target_rel = os.path.relpath(target_rel, root).replace("\\", "/")

    # Match target loosely if partial path given
    matched_target = None
    for f in all_files:
        if f == target_rel or f.endswith("/" + target_rel) or f.endswith(target_rel):
            matched_target = f
            break

    if not matched_target:
        return {
            "error": f"File '{target_path}' not found in active project tree.",
            "available_files_count": len(all_files)
        }

    imported_by = sorted(list(reverse.get(matched_target, [])))
    imports = sorted(list(forward.get(matched_target, [])))
    pkgs = sorted(list(external.get(matched_target, [])))

    # Circular import detection (depth 2)
    circular = []
    for dep in imports:
        if matched_target in forward.get(dep, []):
            circular.append({"loop": [matched_target, dep, matched_target]})

    # Blast radius risk assessment
    blast_radius = "LOW"
    consumer_count = len(imported_by)
    if consumer_count >= 6:
        blast_radius = "CRITICAL"
    elif consumer_count >= 3:
        blast_radius = "HIGH"
    elif consumer_count >= 1:
        blast_radius = "MEDIUM"

    return {
        "target_file": matched_target,
        "blast_radius_risk": blast_radius,
        "consumer_count": consumer_count,
        "imported_by": imported_by,
        "internal_dependencies": imports,
        "external_packages": pkgs,
        "circular_dependencies": circular
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"usage": "python scan_imports.py <target_file> [root_dir]"}))
        sys.exit(1)

    target = sys.argv[1]
    root = sys.argv[2] if len(sys.argv) > 2 else "."
    result = analyze_target(target, root)
    print(json.dumps(result, indent=2))
