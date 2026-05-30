"""
generate_system_map.py

Generates:
1. docs/maps/SYSTEM_MAP.md — Human-readable domain view ("5-Year-Old" guide)
2. AETHER.md Section 19 — Category registry table
3. Syncs `category:` frontmatter to all markdown files

Usage:
    python .agent/scripts/generate_system_map.py              # Generate docs only
    python .agent/scripts/generate_system_map.py --sync       # Also add/update frontmatter
    python .agent/scripts/generate_system_map.py --check      # Dry-run: report missing categories only
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent

CATEGORY_LABELS = {
    'core': 'Core Infrastructure',
    'scan': 'Scanning & Discovery',
    'plan': 'Planning & Spec',
    'build': 'Implementation',
    'test': 'Testing & Quality',
    'review': 'Review & Bug Detection',
    'security': 'Security',
    'ui': 'UI/UX & Design',
    'docs': 'Documentation',
    'ops': 'Operations',
}

CATEGORY_ORDER = ['core', 'scan', 'plan', 'build', 'test', 'review', 'security', 'ui', 'docs', 'ops']

CATEGORY_ICONS = {
    'core': '⚙️',
    'scan': '🔍',
    'plan': '📋',
    'build': '🔧',
    'test': '🧪',
    'review': '👁️',
    'security': '🔒',
    'ui': '🎨',
    'docs': '📝',
    'ops': '🔄',
}

CATEGORY_MAP = {
    # ── Core Infrastructure ──────────────────────────────────
    '.agent/rules/00-workflow-orchestration.md': 'core',
    '.agent/rules/01-core.md': 'core',
    '.agent/rules/02-integrity.md': 'core',
    '.agent/rules/03-instincts.md': 'core',
    '.agent/rules/04-verification-gates.md': 'core',
    '.agent/rules/05-context-integrity.md': 'core',
    '.agent/rules/06-context-memory.md': 'core',
    '.agent/rules/07-metadata-awareness.md': 'core',
    '.agent/rules/12-silent-ingest.md': 'core',
    '.agent/rules/13-self-improvement.md': 'core',
    '.agent/rules/15-context-engine.md': 'core',
    '.agent/rules/17-agent-composition.md': 'core',
    '.agent/rules/18-knowledge-persistence.md': 'core',
    '.agent/rules/21-destructive-operation-safety.md': 'core',
    '.agent/skills/02-language-routing.md': 'core',
    '.agent/skills/10-confidence-scoring.md': 'core',
    '.agent/skills/11-memory-evolution.md': 'core',
    '.agent/skills/14-context-engineering.md': 'core',
    '.agent/skills/18-memory-management.md': 'core',
    '.agent/instincts/01-minimal-footprint.md': 'core',
    '.agent/instincts/02-verification-before-confidence.md': 'core',
    '.agent/instincts/03-user-intent-preservation.md': 'core',
    '.agent/instincts/04-graceful-degradation.md': 'core',
    '.agent/instincts/05-commercial-quality-standard.md': 'core',
    '.agent/instincts/06-asset-pruning.md': 'core',
    '.agent/.agents/skills/03-ask/SKILL.md': 'core',
    '.agent/scripts/bootstrap.js': 'core',
    '.agent/scripts/detect_root.py': 'core',
    '.claude/commands/ag-ask.md': 'core',
    '.claude/commands/ag-refresh.md': 'core',
    # ── Scanning & Discovery ──────────────────────────────────
    '.agent/workflows/01-scan.md': 'scan',
    '.agent/.agents/skills/01-deep-scan/SKILL.md': 'scan',
    '.agent/skills/01-research-loop.md': 'scan',
    '.agent/scripts/deep_scan_engine.py': 'scan',
    '.claude/commands/scanner.md': 'scan',
    '.agents/skills/source-command-scanner/SKILL.md': 'scan',
    # ── Planning & Spec ───────────────────────────────────────
    '.agent/workflows/04-spec.md': 'plan',
    '.agent/workflows/05-research.md': 'plan',
    '.agent/workflows/06-plan-synthesis.md': 'plan',
    '.agent/workflows/07-knowledge-capture.md': 'plan',
    '.agent/.agents/skills/04-planner/SKILL.md': 'plan',
    '.agent/.agents/skills/05-synthesizer/SKILL.md': 'plan',
    '.agent/skills/03-task-decomposition.md': 'plan',
    '.agent/skills/17-spec-compliance.md': 'plan',
    '.agent/rules/16-sdd-lifecycle.md': 'plan',
    '.claude/commands/spec.md': 'plan',
    '.claude/commands/plan.md': 'plan',
    '.claude/commands/planner.md': 'plan',
    '.agents/skills/source-command-spec/SKILL.md': 'plan',
    '.agents/skills/source-command-plan/SKILL.md': 'plan',
    '.agents/skills/source-command-planner/SKILL.md': 'plan',
    # ── Implementation ────────────────────────────────────────
    '.agent/workflows/08-build.md': 'build',
    '.agent/workflows/09-feature.md': 'build',
    '.agent/.agents/skills/07-python-agent/SKILL.md': 'build',
    '.agent/.agents/skills/08-rust-agent/SKILL.md': 'build',
    '.agent/.agents/skills/09-jsts-agent/SKILL.md': 'build',
    '.agent/.agents/skills/10-c-agent/SKILL.md': 'build',
    '.agent/.agents/skills/11-go-agent/SKILL.md': 'build',
    '.agent/skills/04-architectural-design.md': 'build',
    '.agent/skills/05-code-synthesis.md': 'build',
    '.agent/skills/06-refactor.md': 'build',
    '.agent/skills/16-api-design.md': 'build',
    '.claude/commands/impl.md': 'build',
    '.agents/skills/source-command-impl/SKILL.md': 'build',
    # ── Testing & Quality ─────────────────────────────────────
    '.agent/workflows/10-tdd.md': 'test',
    '.agent/workflows/13-quality-gate.md': 'test',
    '.agent/.agents/skills/06-tdd-guide/SKILL.md': 'test',
    '.agent/.agents/skills/22-test-engineer/SKILL.md': 'test',
    '.agent/skills/19-performance-profiling.md': 'test',
    '.agent/rules/19-test-before-done.md': 'test',
    '.claude/commands/tdd-guide.md': 'test',
    '.agents/skills/source-command-tdd-guide/SKILL.md': 'test',
    # ── Review & Bug Detection ────────────────────────────────
    '.agent/workflows/11-debug.md': 'review',
    '.agent/workflows/14-validate.md': 'review',
    '.agent/.agents/skills/12-antibug/SKILL.md': 'review',
    '.agent/.agents/skills/20-code-reviewer/SKILL.md': 'review',
    '.agent/skills/07-cognitive-load-inspector.md': 'review',
    '.agent/skills/08-side-effect-tracker.md': 'review',
    '.agent/skills/09-state-machine-inspector.md': 'review',
    '.claude/commands/antibug.md': 'review',
    '.claude/commands/review.md': 'review',
    '.agents/skills/source-command-antibug/SKILL.md': 'review',
    '.agents/skills/source-command-review/SKILL.md': 'review',
    # ── Security ──────────────────────────────────────────────
    '.agent/.agents/skills/21-security-auditor/SKILL.md': 'security',
    '.agent/skills/15-security-engineering.md': 'security',
    '.claude/agents/security-auditor.md': 'security',
    # ── UI/UX & Design ────────────────────────────────────────
    '.agent/.agents/skills/13-web-aesthetics/SKILL.md': 'ui',
    '.agent/skills/20-stitch-ui.md': 'ui',
    '.agent/skills/ui-ux-pro-max/SKILL.md': 'ui',
    '.claude/commands/web-aesthetics.md': 'ui',
    '.agents/skills/source-command-web-aesthetics/SKILL.md': 'ui',
    # ── Documentation ─────────────────────────────────────────
    '.agent/workflows/18-readme-architect.md': 'docs',
    '.agent/.agents/skills/14-scientific-writing/SKILL.md': 'docs',
    '.agent/.agents/skills/15-latex-bib-manager/SKILL.md': 'docs',
    '.agent/.agents/skills/16-readme-architect/SKILL.md': 'docs',
    '.agent/skills/13-knowledge-capture.md': 'docs',
    # ── Operations ────────────────────────────────────────────
    '.agent/workflows/02-onboard.md': 'ops',
    '.agent/workflows/03-scaffold.md': 'ops',
    '.agent/workflows/12-performance.md': 'ops',
    '.agent/workflows/15-release.md': 'ops',
    '.agent/workflows/16-sync-registry.md': 'ops',
    '.agent/workflows/17-auto-commit.md': 'ops',
    '.agent/workflows/19-mcp-audit.md': 'ops',
    '.agent/.agents/skills/02-failure-predictor/SKILL.md': 'ops',
    '.agent/.agents/skills/17-market-evaluator/SKILL.md': 'ops',
    '.agent/.agents/skills/18-commercial-license/SKILL.md': 'ops',
    '.agent/.agents/skills/19-git-commit-author/SKILL.md': 'ops',
    '.agent/.agents/skills/23-mcp-auditor/SKILL.md': 'ops',
    '.agent/skills/12-commit-semantics.md': 'ops',
    '.agent/skills/21-mcp-audit.md': 'ops',
    '.agent/skills/22-registry-synchronizer.md': 'ops',
    '.agent/rules/08-asset-awareness.md': 'ops',
    '.agent/rules/09-archive-management.md': 'ops',
    '.agent/rules/10-semantic-versioning.md': 'ops',
    '.agent/rules/11-git-awareness.md': 'ops',
    '.agent/rules/14-release-packaging.md': 'ops',
    '.agent/rules/20-output-organization.md': 'ops',
    '.agent/rules/22-continuous-versioning.md': 'ops',
    '.agent/scripts/sync_registry.py': 'ops',
    '.agent/scripts/readme_architect.py': 'ops',
    '.agent/scripts/sanitize_frontmatter.py': 'ops',
    '.agent/scripts/upgrade_project.py': 'ops',
    '.claude/commands/sync-registry.md': 'ops',
    '.claude/commands/auto-commit.md': 'ops',
    '.claude/commands/onboard.md': 'ops',
    '.claude/commands/ship.md': 'ops',
    '.claude/agents/code-reviewer.md': 'ops',
    '.claude/agents/test-engineer.md': 'ops',
    '.agents/skills/source-command-sync-registry/SKILL.md': 'ops',
    '.agents/skills/source-command-onboard/SKILL.md': 'ops',
    '.agents/skills/source-command-auto-commit/SKILL.md': 'ops',
    '.agents/skills/source-command-ship/SKILL.md': 'ops',
}

ICON_MAP = {
    'core': '⚙️', 'scan': '🔍', 'plan': '📋', 'build': '🔧',
    'test': '🧪', 'review': '👁️', 'security': '🔒', 'ui': '🎨',
    'docs': '📝', 'ops': '🔄',
}

TYPE_ICONS = {
    'rules': '📏', 'skills': '🧠', 'workflows': '⚡',
    'instincts': '💡', 'scripts': '📄', 'commands': '🔌',
    'agents': '🤖',
}

def file_type_icon(rel_path):
    for prefix, icon in TYPE_ICONS.items():
        if rel_path.startswith('.agent/' + prefix) or rel_path.startswith('.' + prefix):
            return icon
    if rel_path.startswith('.claude/commands'):
        return '🔌'
    if rel_path.startswith('.claude/agents'):
        return '🤖'
    if rel_path.startswith('.agents/'):
        return '🤖'
    return '📄'

def short_name(rel_path):
    """Extract a concise display name from a path."""
    name = Path(rel_path).stem
    if name == 'SKILL':
        parent = Path(rel_path).parent.name
        return parent
    return name

def read_frontmatter(content):
    """Parse existing YAML frontmatter from markdown content. Returns (fm_lines, body_start)."""
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        return [], 0
    end = 1
    while end < len(lines) and lines[end].strip() != '---':
        end += 1
    if end >= len(lines):
        return [], 0
    return lines[1:end], end + 1

def has_category_field(fm_lines):
    """Check if frontmatter already has a category: field."""
    for line in fm_lines:
        if line.strip().startswith('category:'):
            return True
    return False

def add_category_to_content(content, category):
    """Add or update category: in frontmatter. Returns new content."""
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        new_fm = ['---', f'category: {category}', '---']
        return '\n'.join(new_fm) + ('\n' if content else '') + content
    end = 1
    while end < len(lines) and lines[end].strip() != '---':
        end += 1
    if end >= len(lines):
        return content
    fm_lines = lines[1:end]
    for i, line in enumerate(fm_lines):
        if line.strip().startswith('category:'):
            fm_lines[i] = f'category: {category}'
            break
    else:
        fm_lines.append(f'category: {category}')
    new_lines = ['---'] + fm_lines + ['---'] + lines[end+1:]
    return '\n'.join(new_lines)

def collect_files(root):
    """Walk all relevant directories and return list of (rel_path, full_path)."""
    results = []
    scan_dirs = [
        '.agent/rules',
        '.agent/skills',
        '.agent/workflows',
        '.agent/instincts',
        '.agent/.agents/skills',
        '.agent/scripts',
        '.agents/skills',
        '.claude/commands',
        '.claude/agents',
    ]
    for rel_dir in scan_dirs:
        full_dir = root / rel_dir
        if not full_dir.exists():
            continue
        for entry in sorted(full_dir.rglob('*')):
            if entry.is_file() and entry.suffix in ('.md', '.py', '.js'):
                rel = entry.relative_to(root).as_posix()
                results.append((rel, entry))
    return results

def get_category(rel_path):
    """Get category for a file path from the master map."""
    return CATEGORY_MAP.get(rel_path)

def get_description(rel_path, content):
    """Extract a one-line description from frontmatter or first heading."""
    lines = content.split('\n')
    fm_lines, body_start = read_frontmatter(content)
    for line in fm_lines:
        stripped = line.strip()
        if stripped.startswith('description:'):
            desc = stripped[len('description:'):].strip().strip('"').strip("'")
            if len(desc) > 80:
                desc = desc[:77] + '...'
            return desc
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# ') and len(stripped) > 2:
            return stripped[2:].strip()
    return '(no description)'

def sync_frontmatter(root):
    """Add category: frontmatter to all mapped files that need it."""
    modified = []
    skipped_no_map = []
    for rel_path, full_path in collect_files(root):
        if full_path.suffix not in ('.md',):
            continue
        category = get_category(rel_path)
        if category is None:
            skipped_no_map.append(rel_path)
            continue
        content = full_path.read_text(encoding='utf-8')
        new_content = add_category_to_content(content, category)
        if new_content != content:
            full_path.write_text(new_content, encoding='utf-8')
            modified.append(rel_path)
    return modified, skipped_no_map

def check_frontmatter(root):
    """Dry-run: report which files are missing categories."""
    missing = []
    for rel_path, full_path in collect_files(root):
        if full_path.suffix not in ('.md',):
            continue
        category = get_category(rel_path)
        if category is None:
            continue
        content = full_path.read_text(encoding='utf-8')
        fm_lines, _ = read_frontmatter(content)
        if not has_category_field(fm_lines):
            missing.append(rel_path)
    return missing

def build_sections(root):
    """Group files by category."""
    sections = defaultdict(list)
    for rel_path, full_path in collect_files(root):
        category = get_category(rel_path)
        if category is None:
            continue
        content = full_path.read_text(encoding='utf-8') if full_path.suffix == '.md' else ''
        desc = get_description(rel_path, content)
        sections[category].append((rel_path, desc, full_path.suffix))
    for cat in sections:
        sections[cat].sort(key=lambda x: x[0])
    return sections

def generate_system_map(root, sections):
    """Generate docs/maps/SYSTEM_MAP.md."""
    lines = []
    lines.append('# 🗺️ Aether Agent System Map')
    lines.append('')
    lines.append('> How this AI Operating System works — every file organized by **what it does**, not where it lives.')
    lines.append('')
    lines.append('## How to Read This')
    lines.append('')
    lines.append('| Icon | Meaning |')
    lines.append('|------|---------|')
    lines.append('| 📏 | Rule (must-follow law) |')
    lines.append('| 🧠 | Skill (thinking technique) |')
    lines.append('| ⚡ | Workflow (executable pipeline) |')
    lines.append('| 🤖 | Agent (specialist persona) |')
    lines.append('| 📄 | Script (automation engine) |')
    lines.append('| 🔌 | Command (slash command entry point) |')
    lines.append('| 💡 | Instinct (behavioral pattern) |')
    lines.append('')
    lines.append('---')
    lines.append('')

    algorithm_steps = [
        ('core', '⚙️ Step 0: BOOT — The OS Wakes Up', 'These files load in order every session. They define identity, rules, instincts, and memory.'),
        ('scan', '🔍 Step 1: SCAN — Understand the Project', 'When you run /scanner or ask "what\'s in this project?", these files activate.'),
        ('plan', '📋 Step 2: PLAN — Decide What to Do', 'Spec writing, task breakdown, multi-plan synthesis.'),
        ('build', '🔧 Step 3: BUILD — Write Code', 'Language specialists, code generation, API design, refactoring.'),
        ('test', '🧪 Step 4: TEST — Make Sure It Works', 'TDD enforcement, test engineering, quality gates, performance profiling.'),
        ('review', '👁️ Step 5: REVIEW — Check Quality', 'Code review, bug detection, cognitive/side-effect/state-machine inspection.'),
        ('security', '🔒 Step 6: SECURE — Harden the System', 'Security auditing, vulnerability detection, secure coding practices.'),
        ('ui', '🎨 Step 7: DESIGN — Polish the UI', 'Web aesthetics, design systems, stitch UI integration.'),
        ('docs', '📝 Step 8: DOCUMENT — Explain Everything', 'Scientific writing, LaTeX, README generation, knowledge capture.'),
        ('ops', '🔄 Step 9: OPERATE — Maintain & Ship', 'Registry sync, commits, release, MCP audit, licensing, scaffolding.'),
    ]

    for cat, heading, intro in algorithm_steps:
        items = sections.get(cat, [])
        if not items:
            continue
        lines.append(f'## {heading}')
        lines.append('')
        lines.append(intro)
        lines.append('')
        lines.append('| File | Type | What It Does |')
        lines.append('|------|------|--------------|')
        for rel_path, desc, suffix in items:
            icon = file_type_icon(rel_path)
            name = short_name(rel_path)
            lines.append(f'| `{rel_path}` | {icon} | {desc} |')
        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('*Auto-generated by `.agent/scripts/generate_system_map.py`. Last updated: _auto_*')
    lines.append('')

    return '\n'.join(lines)

def generate_aether_section19(root, sections):
    """Generate content for AETHER.md §19."""
    lines = []
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 19. Domain Category Registry')
    lines.append('')
    lines.append('Every file in the system organized by **domain category** — not by file type.')
    lines.append('This is the human\'s view. The physical layout remains type-based for boot sequence compatibility.')
    lines.append('')
    lines.append('| Category | Files | What It Covers |')
    lines.append('|----------|-------|----------------|')

    for cat in CATEGORY_ORDER:
        items = sections.get(cat, [])
        icon = CATEGORY_ICONS.get(cat, '')
        label = CATEGORY_LABELS.get(cat, cat)
        count = len(items)
        descriptions = {
            'core': 'Boot sequence, governance rules, instincts, context memory, language routing',
            'scan': 'Project mapping, file tree, dependency detection, anomaly detection',
            'plan': 'Spec writing, task decomposition, plan synthesis, research',
            'build': 'Code synthesis, 5 language agents, API design, refactoring',
            'test': 'TDD, test engineering, performance profiling, quality gates',
            'review': 'Code review, antibug, cognitive/side-effect/state-machine inspectors',
            'security': 'Security auditing, vulnerability detection, hardening',
            'ui': 'Web aesthetics, stitch UI, ui-ux-pro-max design system',
            'docs': 'Scientific writing, LaTeX, README architect, knowledge capture',
            'ops': 'Registry sync, auto-commit, release, MCP audit, versioning, licensing',
        }
        desc = descriptions.get(cat, '')
        lines.append(f'| {icon} **{label}** | `{cat}` | {count} files | {desc} |')

    lines.append('')
    lines.append('### File Index by Category')
    lines.append('')

    for cat in CATEGORY_ORDER:
        items = sections.get(cat, [])
        if not items:
            continue
        icon = CATEGORY_ICONS.get(cat, '')
        label = CATEGORY_LABELS.get(cat, cat)
        lines.append(f'#### {icon} {label} ({len(items)} files)')
        lines.append('')
        lines.append('| Path | Type | Description |')
        lines.append('|------|------|-------------|')
        for rel_path, desc, suffix in items:
            ticon = file_type_icon(rel_path)
            lines.append(f'| `{rel_path}` | {ticon} | {desc} |')
        lines.append('')

    lines.append('')
    lines.append('*Auto-generated by `.agent/scripts/generate_system_map.py`. Run `--sync` to refresh.*')
    lines.append('')

    return '\n'.join(lines)


def main():
    args = set(sys.argv[1:])

    root = ROOT

    if '--check' in args:
        missing = check_frontmatter(root)
        if missing:
            print(f"Files missing category frontmatter ({len(missing)}):")
            for f in missing:
                print(f"  {f}")
        else:
            print("All files have category frontmatter. OK")
        return

    if '--sync' in args:
        modified, skipped = sync_frontmatter(root)
        if modified:
            print(f"Added/updated category frontmatter to {len(modified)} files:")
            for f in modified:
                print(f"  {f}")
        else:
            print("No frontmatter changes needed. ✓")
        if skipped:
            print(f"Files without category mapping (skipped): {len(skipped)}")

    sections = build_sections(root)

    # Generate SYSTEM_MAP.md
    system_map = generate_system_map(root, sections)
    map_path = root / 'docs' / 'maps' / 'SYSTEM_MAP.md'
    map_path.parent.mkdir(parents=True, exist_ok=True)
    # Replace auto-timestamp
    from datetime import datetime
    system_map = system_map.replace('_auto_', datetime.now().strftime('%Y-%m-%d %H:%M'))
    map_path.write_text(system_map, encoding='utf-8')
    print(f"Generated: {map_path.relative_to(root)} ({len(system_map)} chars)")

    # Generate AETHER §19
    section19 = generate_aether_section19(root, sections)
    aether_path = root / 'AETHER.md'
    if aether_path.exists():
        content = aether_path.read_text(encoding='utf-8')
        # Check if §19 already exists
        section19_marker = '## 19. Domain Category Registry'
        if section19_marker in content:
            old_content = content.split(section19_marker)[0]
            new_content = old_content + section19.strip()
            aether_path.write_text(new_content, encoding='utf-8')
            print(f"Updated existing §19 in AETHER.md")
        else:
            content = content.rstrip() + '\n\n' + section19.strip() + '\n'
            aether_path.write_text(content, encoding='utf-8')
            print(f"Appended §19 to AETHER.md")

    print("\nDone.")

if __name__ == '__main__':
    main()
