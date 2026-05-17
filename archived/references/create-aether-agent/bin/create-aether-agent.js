#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const packageRoot = path.resolve(__dirname, "../../../../");
const defaultTarget = process.argv[2] ? path.resolve(process.argv[2]) : process.cwd();
const force = process.argv.includes("--force");

// The main directories and files we want to dynamically copy recursively from the package root
const itemsToCopy = [
  ".agent",
  ".claude",
  ".codex",
  "scripts",
  ".mcp.json"
];

// Folders to create empty for standard project taxonomy
const emptyDirectoriesToCreate = [
  "assets",
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

const textTemplates = {
  "README.md": `# Aether Agent\n\nPortable Aether Agent scaffold.\n\n## Quick Start\n\n1. Run /01-scan to bind the session context to this folder.\n2. Run /03-scaffold to ensure docs and archive folders exist.\n3. Run the workflow you need next.\n`,
  "AETHER.md": `# Aether Agent v0.1.0 — [Project Name]\n\n## 14. Project Metadata\n\n**Project Name**: [TO BE FILLED]\n**Version**: 0.1.0\n**Author**: [TO BE FILLED]\n**Created**: [DATE]\n**Status**: In Development\n\n### Description\n[Brief description of the project]\n\n### Tech Stack\n- [e.g., Python 3.11 / React 18 / LaTeX]\n\n### Feature Checklist\n- [ ] Feature 1\n- [ ] Feature 2\n\n## 16. Changelog\n\n### [0.1.0] - [DATE]\n- Project initialized.\n\n## 18. Session Context\n\n# Session Context — [DETECTED PROJECT DIRECTORY NAME]\nInitialized: [DATE]\nProject Directory: [DETECTED PROJECT DIRECTORY NAME]\n`,
  "AGENTS.md": `# Read \`AETHER.md\`\n\nAll system instructions, agent registries, project metadata, deployment protocols,\nchangelogs, and session context are unified in \`AETHER.md\` at the repository root.\n\nThis file is a stub for IDE compatibility (Codex, Cursor, Windsurf, and other tools that auto-load \`AGENTS.md\`). It intentionally contains no operational rules — open \`AETHER.md\` for the full playbook.\n`,
  "CLAUDE.md": `# Read \`AETHER.md\`\n\nAll system instructions, agent registries, project metadata, deployment protocols,\nchangelogs, and session context are unified in \`AETHER.md\` at the repository root.\n\nThis file is a stub for IDE compatibility (Claude Code, Cursor, Windsurf, and other tools that auto-load \`CLAUDE.md\`). It intentionally contains no operational rules — open \`AETHER.md\` for the full playbook.\n`,
  "archived/archive-registry/DELETION_REGISTRY.md": `# Deletion Registry\nThis file logs every item deleted, moved, or archived.\nNever delete this file.\n\n## Registry\n[No entries yet — initialized]\n`
};

function ensureDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function isDirectoryEmpty(dirPath) {
  return fs.existsSync(dirPath) && fs.readdirSync(dirPath).length === 0;
}

// Robust recursive copy that supports modern and legacy Node.js environments
function copyRecursiveSync(src, dest, exclude = []) {
  if (!fs.existsSync(src)) return;
  
  const baseName = path.basename(src);
  if (exclude.includes(baseName) || exclude.includes(src)) {
    return;
  }
  
  const stats = fs.statSync(src);
  if (stats.isDirectory()) {
    ensureDirectory(dest);
    fs.readdirSync(src).forEach((child) => {
      copyRecursiveSync(path.join(src, child), path.join(dest, child), exclude);
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

function main() {
  if (!fs.existsSync(packageRoot)) {
    throw new Error(`Package root not found: ${packageRoot}`);
  }

  ensureDirectory(defaultTarget);

  if (!force && !isDirectoryEmpty(defaultTarget)) {
    const currentEntries = fs.readdirSync(defaultTarget);
    if (currentEntries.length > 0) {
      throw new Error(`Target directory is not empty: ${defaultTarget}. Use --force to overlay the portable bundle.`);
    }
  }

  console.log(`Scaffolding Aether Agent to: ${defaultTarget}...`);

  // 1. Create taxonomy directories
  for (const relativePath of emptyDirectoriesToCreate) {
    ensureDirectory(path.join(defaultTarget, relativePath));
  }

  // 2. Dynamically copy core agent directories and files recursively
  const excludeList = ["data", "node_modules", ".git", "__pycache__", "agent_cache.json"];
  for (const item of itemsToCopy) {
    const sourcePath = path.join(packageRoot, item);
    const destinationPath = path.join(defaultTarget, item);
    copyRecursiveSync(sourcePath, destinationPath, excludeList);
  }

  // 3. Write templates
  for (const [destinationRelativePath, content] of Object.entries(textTemplates)) {
    const destinationPath = path.join(defaultTarget, destinationRelativePath);
    ensureDirectory(path.dirname(destinationPath));
    // Do not overwrite existing files unless forced
    if (force || !fs.existsSync(destinationPath)) {
      fs.writeFileSync(destinationPath, content, "utf8");
    }
  }

  // 4. Reset install state version to 0.1.0 for new project
  const installStateFile = path.join(defaultTarget, ".agent/aether-agent-install-state.json");
  if (fs.existsSync(installStateFile)) {
    try {
      const installState = JSON.parse(fs.readFileSync(installStateFile, "utf8"));
      installState.version = "0.1.0";
      installState.release_date = new Date().toISOString().split("T")[0];
      fs.writeFileSync(installStateFile, JSON.stringify(installState, null, 2), "utf8");
    } catch (e) {
      console.warn("Could not reset install state version, skipping.");
    }
  }

  console.log(`\n🎉 Aether Agent successfully scaffolded at: ${defaultTarget}`);
  console.log("Next steps:");
  console.log("  1. Open target directory in Cursor/Windsurf/Claude Code");
  console.log("  2. Run '/01-scan' in your chat input to bind session context");
  console.log("  3. Run '/03-scaffold' to align full folders and metadata");
}

try {
  main();
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}