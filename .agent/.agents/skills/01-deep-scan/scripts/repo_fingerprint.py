#!/usr/bin/env python3
"""
Lightweight, zero-dependency repository fingerprinting utility.
Self-contained helper for the deep-scan skill.
Fast, token-efficient summary of codebase scale, languages, and manifests.
"""

import os
import sys
import json
from collections import Counter
from pathlib import Path

IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "target", "dist", "build", ".next", ".turbo", ".idea", ".vscode"
}

MANIFEST_MAP = {
    "package.json": "JavaScript / Node / Web",
    "Cargo.toml": "Rust Systems",
    "pyproject.toml": "Python (Modern)",
    "requirements.txt": "Python",
    "go.mod": "Go Service / CLI",
    "CMakeLists.txt": "C / C++ (CMake)",
    "Makefile": "Make-based Native / C",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java / Kotlin (Gradle)"
}

def fingerprint(target_dir="."):
    try:
        root = Path(target_dir).resolve()
    except Exception as e:
        print(json.dumps({"error": f"Invalid path {target_dir}: {e}"}))
        return

    if not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {target_dir}"}))
        return

    ext_counts = Counter()
    detected_manifests = []
    top_level_dirs = []
    total_files = 0

    # Top-level scan
    try:
        for entry in os.scandir(root):
            try:
                if entry.is_dir() and entry.name not in IGNORED_DIRS:
                    top_level_dirs.append(entry.name)
                elif entry.is_file() and entry.name in MANIFEST_MAP:
                    detected_manifests.append(entry.name)
            except (PermissionError, OSError):
                continue
    except (PermissionError, OSError) as e:
        print(json.dumps({"error": f"Cannot scan {root}: {e}"}))
        return

    # File extensions walk
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for f in filenames:
            total_files += 1
            ext = os.path.splitext(f)[1].lower()
            if ext:
                ext_counts[ext] += 1
            else:
                ext_counts["[no_ext]"] += 1

    top_exts = dict(ext_counts.most_common(8))

    # Dynamic repo classification
    inferred_type = "Generic / Mixed"
    if any(d in [".agent", ".agents"] for d in top_level_dirs) and ext_counts[".md"] > 20:
        inferred_type = "Agentic Framework / AI Customizations"
    elif "package.json" in detected_manifests:
        inferred_type = "Web / Fullstack / Node"
    elif "Cargo.toml" in detected_manifests:
        inferred_type = "Rust Systems"
    elif "pyproject.toml" in detected_manifests or "requirements.txt" in detected_manifests:
        inferred_type = "Python / AI / Data"
    elif "go.mod" in detected_manifests:
        inferred_type = "Go Service / CLI"
    elif "CMakeLists.txt" in detected_manifests or "Makefile" in detected_manifests:
        inferred_type = "C / C++ Native Project"

    result = {
        "root": str(root.name),
        "inferred_type": inferred_type,
        "total_source_files": total_files,
        "manifests": detected_manifests,
        "top_level_dirs": sorted(top_level_dirs)[:12],
        "top_extensions": top_exts
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    fingerprint(target)
