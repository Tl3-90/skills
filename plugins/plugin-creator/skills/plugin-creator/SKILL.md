---
name: plugin-creator
description: Create or update GitHub-hosted skills-only plugins for ChatGPT and Codex, including plugins intended for ChatGPT mobile. Use for portable plugin packaging, repository marketplace metadata, validation, and distribution preparation.
---

# Plugin Creator

Create portable, skills-only plugins that work across ChatGPT and Codex. Treat ChatGPT mobile compatibility as a cloud distribution requirement: the core workflow must not depend on a local shell, local filesystem, or desktop-only hook.

## Choose the execution path

### ChatGPT web or mobile

Use an available GitHub connector to inspect and update the target repository. If GitHub tools are unavailable, ask the user to connect GitHub or return a complete package for upload. Do not pretend that a repository was changed.

1. Resolve the exact repository and default branch.
2. Inspect existing marketplace and plugin files before writing.
3. Preserve unrelated files and marketplace entries.
4. Create or update the portable package described below.
5. Validate the complete repository state.
6. Commit to GitHub when the user asked to publish or update the repository.

### Codex desktop or CLI

Use the same portable layout. Local scripts may help scaffold or validate it, but they are optional implementation aids and must not be required for the finished plugin to work in ChatGPT.

## Required portable layout

```text
<repo-root>/
├── .agents/
│   └── plugins/
│       └── marketplace.json
└── plugins/
    └── <plugin-name>/
        ├── plugin.json
        ├── skills/
        │   └── <skill-name>/
        │       ├── SKILL.md
        │       ├── agents/openai.yaml   # optional
        │       ├── references/          # optional
        │       ├── scripts/             # optional
        │       └── assets/              # optional
        ├── assets/                      # optional plugin artwork
        └── .codex-plugin/
            └── plugin.json              # optional compatibility fallback
```

The root `plugin.json` is canonical. Portable plugins automatically discover skills under `skills/`; do not add a `skills` field to the root manifest. Keep `.codex-plugin/plugin.json` only as a compatibility fallback when useful.

## Root plugin manifest

Use the Agent Plugins schema:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What this plugin does",
  "extensions": {
    "com.openai": {
      "interface": {
        "displayName": "Plugin Name",
        "shortDescription": "Short description",
        "longDescription": "Longer description",
        "developerName": "Publisher",
        "category": "Productivity",
        "capabilities": ["Primary capability"],
        "defaultPrompt": ["Use this plugin for its primary workflow."]
      }
    }
  }
}
```

Use lowercase hyphen-case identifiers and strict semantic versions. Keep paths relative to the plugin root. Include only components that actually exist.

## Repository marketplace

Register each same-repository plugin in `.agents/plugins/marketplace.json`:

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

Preserve existing marketplace identity, entry order, and unrelated entries unless the user requests a change.

## Mobile compatibility rules

- Put the complete reusable workflow in `SKILL.md`.
- Never require a bundled local script for the core workflow.
- Use connected tools for GitHub or other external systems.
- Treat scripts as optional desktop/CLI helpers.
- Do not require lifecycle hooks; ChatGPT does not run plugin hooks.
- Avoid instructions that depend on machine-local paths.
- Do not claim that pushing a repository installed the plugin.
- After installation, start a new ChatGPT chat so bundled skills are loaded.

## Distribution

For a private workspace marketplace, a workspace admin imports the GitHub repository from **Admin > Plugins > Add > Import marketplace**. After the plugin is installed and available to the account, it can be used in ChatGPT mobile Chat or Work.

For broader or personal-account availability, prepare a skills-only submission through the OpenAI plugin submission portal. Submission begins review; it does not publish immediately.

## Validation gate

Before completion:

1. Parse the repository marketplace and every plugin manifest as JSON.
2. Verify marketplace names and source paths match real plugin directories.
3. Verify root `plugin.json` uses the Agent Plugins schema.
4. Verify each `skills/<name>/SKILL.md` has valid `name` and `description` frontmatter.
5. Verify all declared assets exist inside the plugin.
6. Confirm the core skill workflow works without local scripts or hooks.
7. Confirm no placeholder values or credentials are committed.
8. Re-read the committed GitHub state after publishing.
