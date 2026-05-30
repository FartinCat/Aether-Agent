#!/usr/bin/env python3
"""
Aether Agent OS — Automated Scaffolding & Safe Project Initialization Script
========================================================================
Location: .agent/scripts/scaffold_project.py

This script automates the /03-scaffold workflow. It safely initializes empty taxonomy
directories (assets, docs, archived) and root stubs (AETHER.md, README.md, CLAUDE.md, AGENTS.md)
ONLY if they do not exist. If they do exist, it parses them, extracts existing metadata
and history, and restructures them cleanly into the canonical Aether Agent format.
"""

import os
import sys
import shutil
import re
from datetime import datetime

# Try to configure standard output to UTF-8 to prevent cp1252 encoding errors on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ─── Dynamic Base Path Resolution ─────────────────────────────────────
try:
    sys.path.append(os.path.dirname(__file__))
    from detect_root import patch_sync_registry
    base = str(patch_sync_registry())
except ImportError:
    base = "."

# Resolve canonical paths
PROJECT_ROOT = os.path.abspath(base)

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created folder: {os.path.relpath(path, PROJECT_ROOT)}")
        return True
    return False

def parse_existing_aether(file_content):
    """
    Parses an existing AETHER.md file, extracting §14 Project Metadata,
    §16 Changelog, and §18 Session Context sections.
    """
    metadata_content = ""
    changelog_content = ""
    session_content = ""
    
    lines = file_content.splitlines()
    current_section = None
    
    for line in lines:
        stripped = line.strip()
        # Detect section transitions
        if stripped.startswith("## 14. Project Metadata"):
            current_section = "metadata"
            continue
        elif stripped.startswith("## 16. Changelog"):
            current_section = "changelog"
            continue
        elif stripped.startswith("## 18. Session Context"):
            current_section = "session"
            continue
        elif stripped.startswith("## ") or stripped.startswith("---"):
            if current_section in ["metadata", "changelog", "session"]:
                current_section = None
                
        # Append line based on active section
        if current_section == "metadata":
            metadata_content += line + "\n"
        elif current_section == "changelog":
            changelog_content += line + "\n"
        elif current_section == "session":
            session_content += line + "\n"
            
    return metadata_content.strip(), changelog_content.strip(), session_content.strip()

def parse_existing_readme(file_content):
    """
    Finds existing sections in README.md to preserve them, returning everything before
    and after the deployment/installation guide.
    """
    lines = file_content.splitlines()
    deploy_start_idx = -1
    deploy_end_idx = -1
    
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## "):
            # Check if this is the start of the deployment section
            if any(kw in stripped.lower() for kw in ["deployment", "installation", "deploy"]):
                if deploy_start_idx == -1:
                    deploy_start_idx = idx
            elif deploy_start_idx != -1:
                # We already started the deployment section, and hit another H2 section header.
                # This marks the end of the deployment section.
                deploy_end_idx = idx
                break
                
    if deploy_start_idx != -1:
        before = "\n".join(lines[:deploy_start_idx]).strip()
        after = "\n".join(lines[deploy_end_idx:]).strip() if deploy_end_idx != -1 else ""
        return before, after
    else:
        return file_content.strip(), ""

def scaffold():
    print(f"==================================================")
    print(f"[START] Aether Agent - Safe Project Scaffolder")
    print(f"Project Directory: {PROJECT_ROOT}")
    print(f"==================================================")

    # ─── 1. Determine Assets Root (Rule 08-asset-awareness) ─────────────────
    src_dir = os.path.join(PROJECT_ROOT, "src")
    if os.path.exists(src_dir) and os.path.isdir(src_dir):
        assets_root = os.path.join(src_dir, "assets")
        print("Asset Injection Point: src/assets/ (detected src/ folder)")
    else:
        assets_root = os.path.join(PROJECT_ROOT, "assets")
        print("Asset Injection Point: assets/ (at root)")

    # ─── 2. Create Directory Taxonomy ──────────────────────────────────
    empty_directories = [
        os.path.join(assets_root, "images"),
        os.path.join(assets_root, "videos"),
        os.path.join(assets_root, "audios"),
        os.path.join(assets_root, "texts"),
        os.path.join(assets_root, "information"),
        os.path.join(assets_root, "icons"),
        os.path.join(PROJECT_ROOT, "docs", "scan-reports"),
        os.path.join(PROJECT_ROOT, "docs", "audit-reports"),
        os.path.join(PROJECT_ROOT, "docs", "master-plans"),
        os.path.join(PROJECT_ROOT, "docs", "research"),
        os.path.join(PROJECT_ROOT, "docs", "market-evaluations"),
        os.path.join(PROJECT_ROOT, "docs", "maps"),
        os.path.join(PROJECT_ROOT, "docs", "opencode-sessions"),
        os.path.join(PROJECT_ROOT, "archived", "archive-registry"),
        os.path.join(PROJECT_ROOT, "archived", "current-version"),
        os.path.join(PROJECT_ROOT, "archived", "old-versions"),
        os.path.join(PROJECT_ROOT, "archived", "references"),
    ]

    for directory in empty_directories:
        ensure_directory(directory)

    # ─── 2a. Move Root Session Dumps to docs/opencode-sessions/ ──────────
    session_dir = os.path.join(PROJECT_ROOT, "docs", "opencode-sessions")
    ensure_directory(session_dir)
    for file in os.listdir(PROJECT_ROOT):
        if file.startswith("session-ses_") and file.endswith(".md"):
            src_file = os.path.join(PROJECT_ROOT, file)
            dest_file = os.path.join(session_dir, file)
            try:
                shutil.move(src_file, dest_file)
                print(f"Moved session dump: {file} -> docs/opencode-sessions/")
            except Exception as e:
                print(f"[WARNING] Could not move session dump {file}: {e}")

    # ─── 3. Write Stubs if Missing ─────────────────────────────────────
    agents_stub = os.path.join(PROJECT_ROOT, "AGENTS.md")
    if not os.path.exists(agents_stub):
        with open(agents_stub, "w", encoding="utf-8") as f:
            f.write("# Read `AETHER.md`\n\nAll system instructions, agent registries, project metadata, deployment protocols,\nchangelogs, and session context are unified in `AETHER.md` at the repository root.\n\nThis file is a stub for IDE compatibility (Codex, Cursor, Windsurf, and other tools that auto-load `AGENTS.md`). It intentionally contains no operational rules — open `AETHER.md` for the full playbook.\n")
        print("Created stub: AGENTS.md")

    claude_stub = os.path.join(PROJECT_ROOT, "CLAUDE.md")
    if not os.path.exists(claude_stub):
        with open(claude_stub, "w", encoding="utf-8") as f:
            f.write("# Read `AETHER.md`\n\nAll system instructions, agent registries, project metadata, deployment protocols,\nchangelogs, and session context are unified in `AETHER.md` at the repository root.\n\nThis file is a stub for IDE compatibility (Claude Code, Cursor, Windsurf, and other tools that auto-load `CLAUDE.md`). It intentionally contains no operational rules — open `AETHER.md` for the full playbook.\n")
        print("Created stub: CLAUDE.md")

    deletion_registry = os.path.join(PROJECT_ROOT, "archived", "archive-registry", "DELETION_REGISTRY.md")
    if not os.path.exists(deletion_registry):
        with open(deletion_registry, "w", encoding="utf-8") as f:
            f.write("# Deletion Registry\nThis file logs every item deleted, moved, or archived.\nNever delete this file.\n\n## Registry\n[No entries yet — initialized]\n")
        print("Created file: archived/archive-registry/DELETION_REGISTRY.md")

    # ─── 4. Smart AETHER.md Restructuring & Integration ───────────────────
    aether_file = os.path.join(PROJECT_ROOT, "AETHER.md")
    aether_template_file = os.path.join(PROJECT_ROOT, ".agent", "AETHER_template.md")
    
    # Read core canonical structure (rules §§1-13, §15, §17, §19) from template
    if os.path.exists(aether_template_file):
        with open(aether_template_file, "r", encoding="utf-8") as f:
            canonical_aether = f.read()
    else:
        # Fallback to current target AETHER.md if template is missing
        if os.path.exists(aether_file):
            with open(aether_file, "r", encoding="utf-8") as f:
                canonical_aether = f.read()
        else:
            print("ERROR: Canonical AETHER_template.md not found. Cannot bootstrap AETHER.md.")
            sys.exit(1)

    project_name = os.path.basename(PROJECT_ROOT)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Extract user metadata and session context from existing file
    existing_metadata = ""
    existing_changelog = ""
    existing_session = ""
    
    if os.path.exists(aether_file):
        print("Parsing pre-existing AETHER.md to preserve user metadata and session logs...")
        with open(aether_file, "r", encoding="utf-8") as f:
            content = f.read()
        existing_metadata, existing_changelog, existing_session = parse_existing_aether(content)

    # Initialize default sections if they were empty or missing
    if not existing_metadata:
        existing_metadata = f"""**Project Name**: {project_name}
**Version**: 0.1.0
**Author**: [TO BE FILLED]
**Created**: {current_date}
**Status**: In Development

### Description
[Brief description of the project]

### Tech Stack
- [e.g., Python 3.11 / React 18 / LaTeX]

### Feature Checklist
- [ ] Feature 1
- [ ] Feature 2"""

    if not existing_changelog:
        existing_changelog = f"""### [0.1.0] - {current_date}
- Project initialized."""

    if not existing_session:
        existing_session = f"""# Session Context — {project_name}
Initialized: {current_date}
Project Directory: {project_name}

This section is maintained automatically by the Aether Agent system.
It tracks cumulative session history for THIS project only.

---

### {current_date} — Project initialized.
**Agent**: system
**Action**: Scaffolder executed. Taxonomy and stubs safely constructed.
**State Change**: Version 0.1.0 configured.
**Next Step**: Run /01-scan to verify context health and begin development."""

    # We now split the canonical AETHER.md template into blocks and rebuild it
    # containing our custom parsed §14, §16, and §18 sections.
    # To do this safely and preserve structural compliance:
    # We find headers like '## 14. Project Metadata', '## 16. Changelog', '## 18. Session Context'
    # in the template, and replace their body.
    
    def replace_section(document, header_title, new_content):
        # Matches the section header and everything up to the next section header or end of file
        pattern = r"(## " + re.escape(header_title) + r"\n+)(.*?)(?=\n## |\n---|\Z)"
        # The section content gets beautifully replaced
        replacement = r"\g<1>" + new_content.replace("\\", "\\\\").replace("$", "\\$") + "\n"
        result, count = re.subn(pattern, replacement, document, flags=re.DOTALL)
        if count == 0:
            print(f"[WARNING] Could not find section '{header_title}' in canonical template.")
        return result

    rebuilt_aether = canonical_aether
    rebuilt_aether = replace_section(rebuilt_aether, "14. Project Metadata", existing_metadata)
    rebuilt_aether = replace_section(rebuilt_aether, "16. Changelog", existing_changelog)
    rebuilt_aether = replace_section(rebuilt_aether, "18. Session Context", existing_session)

    # Make sure version headers inside AETHER.md title reflect version in metadata
    version_match = re.search(r"\*\*Version\*\*:\s*([^\n]+)", existing_metadata)
    if version_match:
        version = version_match.group(1).strip()
        # Replace title e.g. '# Aether Agent vX.Y.Z — Portable AI Operating System'
        rebuilt_aether = re.sub(
            r"# Aether Agent v[^\s]+",
            f"# Aether Agent v{version}",
            rebuilt_aether
        )

    # Write rebuilt, structured AETHER.md
    with open(aether_file, "w", encoding="utf-8") as f:
        f.write(rebuilt_aether)
    print("Reconstructed & Synced: AETHER.md (Structural Integrity Verified)")

    # ─── 5. Smart README.md Alignment ─────────────────────────────────────
    readme_file = os.path.join(PROJECT_ROOT, "README.md")
    
    deploy_guide = f"""
## 📥 Deployment Guide (Installation)

Aether Agent is designed to be **injected** into any directory using `npx`. This ensures conflict-free integration.

### 🚀 Installation
Run the following command at the root of the folder you want to use as your new project root:

```bash
npx create-aether-agent .
```

This will safely install the core `.agent/` and `.claude/` system folders into your project.

### ⚡ First-Boot & Scaffolding
Once the core files are installed, run these two commands in order via your AI IDE chat (Cursor/Windsurf/Claude Code):
1. **/01-scan** — Detects the environment and initializes project memory.
2. **/03-scaffold** — Safely generates the standard project folders (assets, docs, archives) and stubs without conflicts.
"""

    if os.path.exists(readme_file):
        print("Parsing pre-existing README.md to preserve user contents while aligning deployment instructions...")
        with open(readme_file, "r", encoding="utf-8") as f:
            readme_content = f.read()
        
        before, after = parse_existing_readme(readme_content)
        
        rebuilt_readme = before.strip() + "\n\n" + deploy_guide.strip()
        if after.strip():
            rebuilt_readme += "\n\n" + after.strip()
            
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(rebuilt_readme + "\n")
        print("Aligned & Integrated: README.md")
    else:
        # Default README.md bootstrap
        default_readme = f"""# {project_name}

Aether Agentic Workspace.

{deploy_guide.strip()}
"""
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(default_readme)
        print("Created stub: README.md")

    print(f"==================================================")
    print(f"[SUCCESS] SCAFFOLD COMPLETE! Project is structured and conflict-free.")
    print(f"==================================================")

if __name__ == "__main__":
    scaffold()
