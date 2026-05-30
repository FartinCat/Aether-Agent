#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const packageRoot = path.resolve(__dirname, "../../../../");
const defaultTarget = process.argv[2] ? path.resolve(process.argv[2]) : process.cwd();
const force = process.argv.includes("--force");

// The main directories and files we want to dynamically copy recursively from the package root
const itemsToCopy = [
  ".agent",
  ".agents",
  ".claude",
  ".codex",
  "scripts",
  ".mcp.json"
];

// Folders to create empty for standard project taxonomy (delegated to scaffold script now)
const emptyDirectoriesToCreate = [];

const textTemplates = {};

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
      // Allow installation in non-empty directories for aether injection as long as core items don't conflict,
      // but let's warn if forced.
      console.log(`[NOTICE] Target directory is not empty. Overlaying Aether Agent core bundle.`);
    }
  }

  console.log(`Scaffolding Aether Agent to: ${defaultTarget}...`);

  // 1. Create taxonomy directories (delegated)
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

  // 3. Write templates (delegated)
  for (const [destinationRelativePath, content] of Object.entries(textTemplates)) {
    const destinationPath = path.join(defaultTarget, destinationRelativePath);
    ensureDirectory(path.dirname(destinationPath));
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

  console.log(`\n🎉 Aether Agent successfully installed at: ${defaultTarget}`);
  console.log("Next steps:");
  console.log("  1. Open target directory in Cursor/Windsurf/Claude Code");
  console.log("  2. Run '/01-scan' in your chat input to bind session context");
  console.log("  3. Run '/03-scaffold' to safely initialize project folders and stubs without conflicts");
}

try {
  main();
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}