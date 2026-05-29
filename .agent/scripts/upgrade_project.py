#!/usr/bin/env python3
"""
Aether Agent OS — Core Project Upgrade Utility
======================================================
Location: .agent/scripts/upgrade_project.py

Upgrades ONLY the core system directories (.agent/ and .claude/) in a target
project directory to the latest development version, preserving target project
metadata, AETHER.md history, and custom files.
"""

import os
import sys
import shutil
import subprocess

# ─── Dynamic Base Path ────────────────────────────────────────────────
try:
    sys.path.append(os.path.dirname(__file__))
    from detect_root import patch_sync_registry
    base = str(patch_sync_registry())
except ImportError:
    base = "."

def copy_recursive(src, dest, exclude=None):
    if not os.path.exists(src):
        return
    exclude = exclude or []
    if os.path.isdir(src):
        if not os.path.exists(dest):
            os.makedirs(dest)
        for item in os.listdir(src):
            if item in exclude:
                continue
            copy_recursive(os.path.join(src, item), os.path.join(dest, item), exclude)
    else:
        # Standard file copy
        shutil.copy2(src, dest)

def main():
    if len(sys.argv) < 2:
        print("ERROR: Missing target directory path.")
        print("Usage: python .agent/scripts/upgrade_project.py [path/to/target/project]")
        sys.exit(1)
        
    target_dir = os.path.abspath(sys.argv[1])
    
    if not os.path.isdir(target_dir):
        print(f"ERROR: Target path is not a valid directory: {target_dir}")
        sys.exit(1)
        
    print(f"Upgrading Aether Agent core in: {target_dir}")
    print(f"Source: {base}")
    
    # Define core items to copy
    core_items = [".agent", ".claude", ".mcp.json"]
    exclude_list = ["__pycache__", "data", "node_modules", ".git", "agent_cache.json"]
    
    for item in core_items:
        src_path = os.path.join(base, item)
        dest_path = os.path.join(target_dir, item)
        
        if not os.path.exists(src_path):
            continue
            
        print(f"-> Overwriting {item}...")
        if os.path.isdir(src_path):
            # Safe overwrite: remove target directory first if it exists to avoid merging conflicts
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            copy_recursive(src_path, dest_path, exclude_list)
        else:
            shutil.copy2(src_path, dest_path)
            
    # Try to execute sync_registry inside the target project to align everything
    print("-> Initiating post-upgrade registry synchronization in target project...")
    target_sync_script = os.path.join(target_dir, ".agent", "scripts", "sync_registry.py")
    if os.path.exists(target_sync_script):
        try:
            # We execute it in the context of the target directory
            subprocess.run([sys.executable, target_sync_script], cwd=target_dir, check=True)
            print("\n[SUCCESS] Core Upgrade & Synchronization SUCCESSFUL!")
        except Exception as e:
            print(f"\n[WARNING] Synchronization encountered an issue: {e}")
            print("Please run /sync-registry manually in your target project.")
    else:
        print("\n[SUCCESS] Core Upgrade complete! Run /sync-registry in your target project to synchronize.")

if __name__ == "__main__":
    main()
