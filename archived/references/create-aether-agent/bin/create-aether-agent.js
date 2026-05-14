#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const packageRoot = path.resolve(__dirname, "../../../../");
const defaultTarget = process.argv[2] ? path.resolve(process.argv[2]) : process.cwd();
const force = process.argv.includes("--force");

const directoryPaths = [
  ".agent/scripts",
  ".agent/rules",
  ".agent/skills",
  ".agent/workflows",
  ".agent/instincts",
  ".agent/.agents/skills",
  ".claude/commands",
  ".claude/agents",
  ".codex",
  "assets",
  "scripts",
  "docs/scan-reports",
  "docs/audit-reports",
  "docs/master-plans",
  "docs/research",
  "docs/market-evaluations",
  "archived/archive-registry",
  "archived/current-version",
  "archived/old-versions",
  "archived/references"
];

const fileCopies = [
  [".agent/aether-agent-install-state.json", ".agent/aether-agent-install-state.json"],
  [".agent/scripts/bootstrap.js", ".agent/scripts/bootstrap.js"],
  [".agent/scripts/detect_root.py", ".agent/scripts/detect_root.py"],
  [".agent/scripts/readme_architect.py", ".agent/scripts/readme_architect.py"],
  [".agent/scripts/sync_registry.py", ".agent/scripts/sync_registry.py"],
  [".agent/workflows/01-scan.md", ".agent/workflows/01-scan.md"],
  [".agent/workflows/02-onboard.md", ".agent/workflows/02-onboard.md"],
  [".agent/workflows/03-scaffold.md", ".agent/workflows/03-scaffold.md"],
  [".agent/workflows/04-spec.md", ".agent/workflows/04-spec.md"],
  [".agent/workflows/05-research.md", ".agent/workflows/05-research.md"],
  [".agent/workflows/06-plan-synthesis.md", ".agent/workflows/06-plan-synthesis.md"],
  [".agent/workflows/07-knowledge-capture.md", ".agent/workflows/07-knowledge-capture.md"],
  [".agent/workflows/08-build.md", ".agent/workflows/08-build.md"],
  [".agent/workflows/09-feature.md", ".agent/workflows/09-feature.md"],
  [".agent/workflows/10-tdd.md", ".agent/workflows/10-tdd.md"],
  [".agent/workflows/11-debug.md", ".agent/workflows/11-debug.md"],
  [".agent/workflows/12-performance.md", ".agent/workflows/12-performance.md"],
  [".agent/workflows/13-quality-gate.md", ".agent/workflows/13-quality-gate.md"],
  [".agent/workflows/14-validate.md", ".agent/workflows/14-validate.md"],
  [".agent/workflows/15-release.md", ".agent/workflows/15-release.md"],
  [".agent/workflows/16-sync-registry.md", ".agent/workflows/16-sync-registry.md"],
  [".agent/workflows/17-auto-commit.md", ".agent/workflows/17-auto-commit.md"],
  [".agent/workflows/18-readme-architect.md", ".agent/workflows/18-readme-architect.md"],
  [".agent/workflows/19-mcp-audit.md", ".agent/workflows/19-mcp-audit.md"],
  [".agent/rules/00-workflow-orchestration.md", ".agent/rules/00-workflow-orchestration.md"],
  [".agent/rules/01-core.md", ".agent/rules/01-core.md"],
  [".agent/rules/02-integrity.md", ".agent/rules/02-integrity.md"],
  [".agent/rules/03-instincts.md", ".agent/rules/03-instincts.md"],
  [".agent/rules/04-verification-gates.md", ".agent/rules/04-verification-gates.md"],
  [".agent/rules/05-context-integrity.md", ".agent/rules/05-context-integrity.md"],
  [".agent/rules/06-context-memory.md", ".agent/rules/06-context-memory.md"],
  [".agent/rules/07-metadata-awareness.md", ".agent/rules/07-metadata-awareness.md"],
  [".agent/rules/08-asset-awareness.md", ".agent/rules/08-asset-awareness.md"],
  [".agent/rules/09-archive-management.md", ".agent/rules/09-archive-management.md"],
  [".agent/rules/10-semantic-versioning.md", ".agent/rules/10-semantic-versioning.md"],
  [".agent/rules/11-git-awareness.md", ".agent/rules/11-git-awareness.md"],
  [".agent/rules/12-silent-ingest.md", ".agent/rules/12-silent-ingest.md"],
  [".agent/rules/13-self-improvement.md", ".agent/rules/13-self-improvement.md"],
  [".agent/rules/14-release-packaging.md", ".agent/rules/14-release-packaging.md"],
  [".agent/rules/15-context-engine.md", ".agent/rules/15-context-engine.md"],
  [".agent/rules/16-sdd-lifecycle.md", ".agent/rules/16-sdd-lifecycle.md"],
  [".agent/rules/17-agent-composition.md", ".agent/rules/17-agent-composition.md"],
  [".agent/rules/18-knowledge-persistence.md", ".agent/rules/18-knowledge-persistence.md"],
  [".agent/rules/19-test-before-done.md", ".agent/rules/19-test-before-done.md"],
  [".agent/rules/20-output-organization.md", ".agent/rules/20-output-organization.md"],
  [".agent/rules/21-destructive-operation-safety.md", ".agent/rules/21-destructive-operation-safety.md"],
  [".agent/rules/22-continuous-versioning.md", ".agent/rules/22-continuous-versioning.md"],
  [".agent/skills/01-research-loop.md", ".agent/skills/01-research-loop.md"],
  [".agent/skills/02-language-routing.md", ".agent/skills/02-language-routing.md"],
  [".agent/skills/03-task-decomposition.md", ".agent/skills/03-task-decomposition.md"],
  [".agent/skills/04-architectural-design.md", ".agent/skills/04-architectural-design.md"],
  [".agent/skills/05-code-synthesis.md", ".agent/skills/05-code-synthesis.md"],
  [".agent/skills/06-refactor.md", ".agent/skills/06-refactor.md"],
  [".agent/skills/07-cognitive-load-inspector.md", ".agent/skills/07-cognitive-load-inspector.md"],
  [".agent/skills/08-side-effect-tracker.md", ".agent/skills/08-side-effect-tracker.md"],
  [".agent/skills/09-state-machine-inspector.md", ".agent/skills/09-state-machine-inspector.md"],
  [".agent/skills/10-confidence-scoring.md", ".agent/skills/10-confidence-scoring.md"],
  [".agent/skills/11-memory-evolution.md", ".agent/skills/11-memory-evolution.md"],
  [".agent/skills/12-commit-semantics.md", ".agent/skills/12-commit-semantics.md"],
  [".agent/skills/13-knowledge-capture.md", ".agent/skills/13-knowledge-capture.md"],
  [".agent/skills/14-context-engineering.md", ".agent/skills/14-context-engineering.md"],
  [".agent/skills/15-security-engineering.md", ".agent/skills/15-security-engineering.md"],
  [".agent/skills/16-api-design.md", ".agent/skills/16-api-design.md"],
  [".agent/skills/17-spec-compliance.md", ".agent/skills/17-spec-compliance.md"],
  [".agent/skills/18-memory-management.md", ".agent/skills/18-memory-management.md"],
  [".agent/skills/19-performance-profiling.md", ".agent/skills/19-performance-profiling.md"],
  [".agent/skills/20-stitch-ui.md", ".agent/skills/20-stitch-ui.md"],
  [".agent/skills/21-mcp-audit.md", ".agent/skills/21-mcp-audit.md"],
  [".agent/skills/22-registry-synchronizer.md", ".agent/skills/22-registry-synchronizer.md"],
  [".agent/.agents/skills/01-deep-scan/SKILL.md", ".agent/.agents/skills/01-deep-scan/SKILL.md"],
  [".agent/.agents/skills/02-failure-predictor/SKILL.md", ".agent/.agents/skills/02-failure-predictor/SKILL.md"],
  [".agent/.agents/skills/03-ask/SKILL.md", ".agent/.agents/skills/03-ask/SKILL.md"],
  [".agent/.agents/skills/04-planner/SKILL.md", ".agent/.agents/skills/04-planner/SKILL.md"],
  [".agent/.agents/skills/05-synthesizer/SKILL.md", ".agent/.agents/skills/05-synthesizer/SKILL.md"],
  [".agent/.agents/skills/06-tdd-guide/SKILL.md", ".agent/.agents/skills/06-tdd-guide/SKILL.md"],
  [".agent/.agents/skills/07-python-agent/SKILL.md", ".agent/.agents/skills/07-python-agent/SKILL.md"],
  [".agent/.agents/skills/08-rust-agent/SKILL.md", ".agent/.agents/skills/08-rust-agent/SKILL.md"],
  [".agent/.agents/skills/09-jsts-agent/SKILL.md", ".agent/.agents/skills/09-jsts-agent/SKILL.md"],
  [".agent/.agents/skills/10-c-agent/SKILL.md", ".agent/.agents/skills/10-c-agent/SKILL.md"],
  [".agent/.agents/skills/11-go-agent/SKILL.md", ".agent/.agents/skills/11-go-agent/SKILL.md"],
  [".agent/.agents/skills/12-antibug/SKILL.md", ".agent/.agents/skills/12-antibug/SKILL.md"],
  [".agent/.agents/skills/13-web-aesthetics/SKILL.md", ".agent/.agents/skills/13-web-aesthetics/SKILL.md"],
  [".agent/.agents/skills/14-scientific-writing/SKILL.md", ".agent/.agents/skills/14-scientific-writing/SKILL.md"],
  [".agent/.agents/skills/15-latex-bib-manager/SKILL.md", ".agent/.agents/skills/15-latex-bib-manager/SKILL.md"],
  [".agent/.agents/skills/16-readme-architect/SKILL.md", ".agent/.agents/skills/16-readme-architect/SKILL.md"],
  [".agent/.agents/skills/17-market-evaluator/SKILL.md", ".agent/.agents/skills/17-market-evaluator/SKILL.md"],
  [".agent/.agents/skills/18-commercial-license/SKILL.md", ".agent/.agents/skills/18-commercial-license/SKILL.md"],
  [".agent/.agents/skills/19-git-commit-author/SKILL.md", ".agent/.agents/skills/19-git-commit-author/SKILL.md"],
  [".agent/.agents/skills/20-code-reviewer/SKILL.md", ".agent/.agents/skills/20-code-reviewer/SKILL.md"],
  [".agent/.agents/skills/21-security-auditor/SKILL.md", ".agent/.agents/skills/21-security-auditor/SKILL.md"],
  [".agent/.agents/skills/22-test-engineer/SKILL.md", ".agent/.agents/skills/22-test-engineer/SKILL.md"],
  [".agent/.agents/skills/23-mcp-auditor/SKILL.md", ".agent/.agents/skills/23-mcp-auditor/SKILL.md"],
  [".claude/commands/ag-ask.md", ".claude/commands/ag-ask.md"],
  [".claude/commands/ag-refresh.md", ".claude/commands/ag-refresh.md"],
  [".claude/commands/antibug.md", ".claude/commands/antibug.md"],
  [".claude/commands/auto-commit.md", ".claude/commands/auto-commit.md"],
  [".claude/commands/impl.md", ".claude/commands/impl.md"],
  [".claude/commands/onboard.md", ".claude/commands/onboard.md"],
  [".claude/commands/plan.md", ".claude/commands/plan.md"],
  [".claude/commands/planner.md", ".claude/commands/planner.md"],
  [".claude/commands/review.md", ".claude/commands/review.md"],
  [".claude/commands/scanner.md", ".claude/commands/scanner.md"],
  [".claude/commands/ship.md", ".claude/commands/ship.md"],
  [".claude/commands/spec.md", ".claude/commands/spec.md"],
  [".claude/commands/sync-registry.md", ".claude/commands/sync-registry.md"],
  [".claude/commands/tdd-guide.md", ".claude/commands/tdd-guide.md"],
  [".claude/commands/web-aesthetics.md", ".claude/commands/web-aesthetics.md"],
  [".claude/agents/code-reviewer.md", ".claude/agents/code-reviewer.md"],
  [".claude/agents/security-auditor.md", ".claude/agents/security-auditor.md"],
  [".claude/agents/test-engineer.md", ".claude/agents/test-engineer.md"],
  [".mcp.json", ".mcp.json"],
  ["scripts/entrypoint.sh", "scripts/entrypoint.sh"],
  ["scripts/install-mcps.sh", "scripts/install-mcps.sh"],
  ["LICENSE.md", "LICENSE.md"]
];

const textTemplates = {
  "README.md": `# Aether Agent\n\nPortable Aether Agent scaffold.\n\n## Quick Start\n\n1. Run /01-scan to bind the session context to this folder.\n2. Run /03-scaffold to ensure docs and archive folders exist.\n3. Run the workflow you need next.\n`,
  "AETHER.md": `# Aether Agent v0.1.0 — [Project Name]\n\n## 14. Project Metadata\n\n**Project Name**: [TO BE FILLED]\n**Version**: 0.1.0\n**Author**: [TO BE FILLED]\n**Created**: [DATE]\n**Status**: In Development\n\n### Description\n[Brief description of the project]\n\n### Tech Stack\n- [e.g., Python 3.11 / React 18 / LaTeX]\n\n### Feature Checklist\n- [ ] Feature 1\n- [ ] Feature 2\n\n## 16. Changelog\n\n### [0.1.0] - [DATE]\n- Project initialized.\n\n## 18. Session Context\n\n# Session Context — [DETECTED PROJECT DIRECTORY NAME]\nInitialized: [DATE]\nProject Directory: [DETECTED PROJECT DIRECTORY NAME]\n`,
  "AGENTS.md": `# Read \`AETHER.md\`\n\nAll system instructions, agent registries, project metadata, deployment protocols,\nchangelogs, and session context are unified in \`AETHER.md\` at the repository root.\n\nThis file is a stub for IDE compatibility (Codex, Cursor, Windsurf, and other tools that auto-load \`AGENTS.md\`). It intentionally contains no operational rules — open \`AETHER.md\` for the full playbook.\n`,
  "CLAUDE.md": `# Read \`AETHER.md\`\n\nAll system instructions, agent registries, project metadata, deployment protocols,\nchangelogs, and session context are unified in \`AETHER.md\` at the repository root.\n\nThis file is a stub for IDE compatibility (Claude Code, Cursor, Windsurf, and other tools that auto-load \`CLAUDE.md\`). It intentionally contains no operational rules — open \`AETHER.md\` for the full playbook.\n`,
  "archived/archive-registry/DELETION_REGISTRY.md": `# Deletion Registry\nThis file logs every item deleted, moved, or archived.\nNever delete this file.\n\n## Registry\n[No entries yet — initialized]\n`
};

function ensureDirectory(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function isDirectoryEmpty(dirPath) {
  return fs.existsSync(dirPath) && fs.readdirSync(dirPath).length === 0;
}

function main() {
  if (!fs.existsSync(packageRoot)) {
    throw new Error(`Package root not found: ${packageRoot}`);
  }

  ensureDirectory(defaultTarget);

  if (!force && !isDirectoryEmpty(defaultTarget)) {
    const currentEntries = fs.readdirSync(defaultTarget);
    const allowedCleanTarget = currentEntries.length === 0;
    if (!allowedCleanTarget) {
      throw new Error(`Target directory is not empty: ${defaultTarget}. Use --force to overlay the portable bundle.`);
    }
  }

  for (const relativePath of directoryPaths) {
    ensureDirectory(path.join(defaultTarget, relativePath));
  }

  for (const [sourceRelativePath, destinationRelativePath] of fileCopies) {
    const sourcePath = path.join(packageRoot, sourceRelativePath);
    if (!fs.existsSync(sourcePath)) {
      continue;
    }
    const destinationPath = path.join(defaultTarget, destinationRelativePath);
    ensureDirectory(path.dirname(destinationPath));
    fs.copyFileSync(sourcePath, destinationPath);
  }

  for (const [destinationRelativePath, content] of Object.entries(textTemplates)) {
    const destinationPath = path.join(defaultTarget, destinationRelativePath);
    ensureDirectory(path.dirname(destinationPath));
    fs.writeFileSync(destinationPath, content, "utf8");
  }

  // Reset install state version to 0.1.0 for new project
  const installStateFile = path.join(defaultTarget, ".agent/aether-agent-install-state.json");
  if (fs.existsSync(installStateFile)) {
    const installState = JSON.parse(fs.readFileSync(installStateFile, "utf8"));
    installState.version = "0.1.0";
    installState.release_date = new Date().toISOString().split("T")[0];
    fs.writeFileSync(installStateFile, JSON.stringify(installState, null, 2), "utf8");
  }

  console.log(`Aether Agent scaffolded at: ${defaultTarget}`);
  console.log("Next: run /01-scan in the target project to rebind session context.");
}

try {
  main();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}