---
name: plugin-creator
description: Create and maintain GitHub-hosted plugin marketplaces for ChatGPT and Codex. Use when packaging skills into plugins, creating or updating repository-root .agents/plugins/marketplace.json catalogs, validating plugin manifests, or preparing a GitHub repository for ChatGPT marketplace import.
---

# Plugin Creator

Create plugins as repository-managed packages intended for GitHub marketplace import into ChatGPT and Codex.

## Default target

Unless the user explicitly requests a local Codex-only plugin, treat the current Git repository as the distribution source.

Use this layout:

```text
<repo-root>/
├── .agents/
│   └── plugins/
│       └── marketplace.json
└── plugins/
    └── <plugin-name>/
        ├── .codex-plugin/
        │   └── plugin.json
        ├── skills/          # when the plugin contains skills
        ├── assets/          # when required
        ├── hooks.json       # only when required
        ├── .mcp.json        # only when explicitly required
        └── .app.json        # only when explicitly required
```

`.codex-plugin/plugin.json` is the plugin package manifest. Its name does not mean the finished repository must be installed locally in Codex.

## GitHub marketplace workflow

1. Locate the Git repository root.
2. Create the plugin under `<repo-root>/plugins/<plugin-name>`.
3. Create or update `<repo-root>/.agents/plugins/marketplace.json`.
4. Register the plugin with a repository-relative source:

```json
{
  "name": "plugin-name",
  "source": {
    "source": "local",
    "path": "./plugins/plugin-name"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

5. Validate JSON, referenced paths, skill contents, and required supporting files.
6. Commit and push the repository when the user requested GitHub publication and GitHub write access is available.
7. Treat the pushed GitHub repository as the distribution source. Do not claim that creating local files installed the plugin in ChatGPT.

For ChatGPT workspace import, the repository root contains `.agents/plugins/marketplace.json`. ChatGPT workspace admins import the repository from Workspace settings > Plugins > Add > Import marketplace. If the marketplace manifest is at the repository root, no subdirectory Path is required.

## Skills-only plugins

A plugin may contain only skills. For a skills-only plugin:

- Set `"skills": "./skills/"` in `.codex-plugin/plugin.json`.
- Do not create `.mcp.json`, MCP servers, `.app.json`, apps, widgets, or backend infrastructure unless the user explicitly needs those components.
- Preserve every file required by the packaged skill, including scripts, references, agents metadata, templates, or assets that it actually uses.

## Creating a plugin

Use the scaffold script from this skill when useful:

```bash
python3 <path-to-this-skill>/scripts/create_basic_plugin.py <plugin-name> \
  --path ./plugins \
  --marketplace-path ./.agents/plugins/marketplace.json \
  --with-marketplace \
  --with-skills
```

Plugin names are normalized to lowercase hyphen-case and must be 64 characters or fewer.

If the current repository already contains `.agents/plugins/marketplace.json`, preserve its existing marketplace metadata and unrelated plugin entries.

## Optional components

Create optional components only when required by the requested plugin:

- `skills/`
- `hooks.json`
- `scripts/`
- `assets/`
- `.mcp.json`
- `.app.json`

Do not add MCP or app components to a skills-only plugin merely because the scaffold supports them.

## Marketplace rules

- Repository/team marketplaces use `<repo-root>/.agents/plugins/marketplace.json`.
- Marketplace root metadata supports top-level `name` and optional `interface.displayName`.
- Preserve existing entries and ordering unless the user requests a change.
- Each generated marketplace entry includes `policy.installation`, `policy.authentication`, and `category`.
- Default `policy.installation` to `AVAILABLE`.
- Default `policy.authentication` to `ON_INSTALL`.
- Allowed installation values: `NOT_AVAILABLE`, `AVAILABLE`, `INSTALLED_BY_DEFAULT`.
- Allowed authentication values: `ON_INSTALL`, `ON_USE`.
- Add `policy.products` only when explicitly required.
- Keep same-repository plugin sources relative: `./plugins/<plugin-name>`.
- Use `--force` only when intentionally replacing an existing entry or file.

## Manifest rules

- The plugin folder name and `plugin.json` `name` must use the same normalized plugin name.
- Keep `.codex-plugin/plugin.json` present.
- Include only component fields that the finished plugin actually provides. Do not leave placeholder MCP/app/hook paths in a skills-only plugin.
- Resolve all relative paths from the plugin root and verify each referenced file or directory exists.
- Human-facing metadata should accurately describe the plugin's actual behavior and supported surfaces.

For the manifest schema reference bundled with this skill, use `references/plugin-json-spec.md`.

## Validation gate

Before declaring completion:

1. Parse `.agents/plugins/marketplace.json` as JSON.
2. Parse every referenced `.codex-plugin/plugin.json` as JSON.
3. Verify each marketplace `source.path` resolves to an existing plugin directory.
4. Verify every component path declared by `plugin.json` exists.
5. For every skill, verify `SKILL.md` exists and required supporting files are present.
6. Confirm skills-only plugins do not accidentally declare MCP or app components.
7. If GitHub publication was requested, validate the repository state after push rather than only the local working tree.
8. Do not claim ChatGPT installation unless ChatGPT itself confirms the import/install.

If validation fails, correct the failure and repeat the validation gate.

## Local Codex-only mode

Use `~/plugins/<plugin-name>` and `~/.agents/plugins/marketplace.json` only when the user explicitly requests a personal/local Codex plugin. Do not silently substitute this mode for a GitHub/ChatGPT marketplace request.
