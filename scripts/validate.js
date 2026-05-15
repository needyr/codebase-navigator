const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const skillsDir = path.join(root, "skills");
const requiredPluginFiles = [
  path.join(root, ".claude-plugin", "plugin.json"),
  path.join(root, ".codex-plugin", "plugin.json"),
];
const requiredHookFiles = [
  path.join(root, "hooks", "hooks.json"),
  path.join(root, "hooks", "run-hook.cmd"),
  path.join(root, "hooks", "session-start"),
];

function fail(message) {
  console.error(message);
  process.exitCode = 1;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!match) {
    return null;
  }

  const data = {};
  for (const line of match[1].split(/\r?\n/)) {
    const index = line.indexOf(":");
    if (index === -1) {
      continue;
    }
    const key = line.slice(0, index).trim();
    const value = line.slice(index + 1).trim();
    data[key] = value;
  }
  return data;
}

if (!fs.existsSync(skillsDir)) {
  fail(`Missing skills directory: ${skillsDir}`);
  process.exit();
}

const seenNames = new Set();
for (const entry of fs.readdirSync(skillsDir, { withFileTypes: true })) {
  if (!entry.isDirectory()) {
    continue;
  }

  const skillName = entry.name;
  const skillPath = path.join(skillsDir, skillName, "SKILL.md");
  if (!fs.existsSync(skillPath)) {
    fail(`Missing SKILL.md for ${skillName}`);
    continue;
  }

  const content = fs.readFileSync(skillPath, "utf8");
  const frontmatter = parseFrontmatter(content);
  if (!frontmatter) {
    fail(`Missing YAML frontmatter in ${skillPath}`);
    continue;
  }

  if (frontmatter.name !== skillName) {
    fail(`Skill name mismatch in ${skillPath}: expected "${skillName}", got "${frontmatter.name || ""}"`);
  }

  if (!frontmatter.description) {
    fail(`Missing description in ${skillPath}`);
  }

  if (seenNames.has(frontmatter.name)) {
    fail(`Duplicate skill name: ${frontmatter.name}`);
  }
  seenNames.add(frontmatter.name);
}

if (!process.exitCode) {
  for (const pluginFile of requiredPluginFiles) {
    if (!fs.existsSync(pluginFile)) {
      fail(`Missing plugin manifest: ${pluginFile}`);
      continue;
    }

    let manifest;
    try {
      manifest = JSON.parse(fs.readFileSync(pluginFile, "utf8"));
    } catch (error) {
      fail(`Invalid JSON in ${pluginFile}: ${error.message}`);
      continue;
    }

    for (const key of ["name", "version", "description"]) {
      if (!manifest[key]) {
        fail(`Missing ${key} in ${pluginFile}`);
      }
    }
  }

  const codexManifestPath = path.join(root, ".codex-plugin", "plugin.json");
  if (fs.existsSync(codexManifestPath)) {
    const codexManifest = JSON.parse(fs.readFileSync(codexManifestPath, "utf8"));
    if (codexManifest.skills !== "./skills/") {
      fail(`Expected .codex-plugin/plugin.json skills to be "./skills/"`);
    }
    if (!codexManifest.interface || !codexManifest.interface.displayName) {
      fail(`Missing interface.displayName in .codex-plugin/plugin.json`);
    }
  }

  for (const hookFile of requiredHookFiles) {
    if (!fs.existsSync(hookFile)) {
      fail(`Missing hook file: ${hookFile}`);
    }
  }

  const hooksJsonPath = path.join(root, "hooks", "hooks.json");
  if (fs.existsSync(hooksJsonPath)) {
    let hooksJson;
    try {
      hooksJson = JSON.parse(fs.readFileSync(hooksJsonPath, "utf8"));
    } catch (error) {
      fail(`Invalid JSON in ${hooksJsonPath}: ${error.message}`);
    }

    if (hooksJson && !hooksJson.hooks?.SessionStart) {
      fail(`hooks/hooks.json must define hooks.SessionStart`);
    }
  }
}

if (!process.exitCode) {
  console.log(`Validated ${seenNames.size} skills, plugin manifests, and hooks`);
}
