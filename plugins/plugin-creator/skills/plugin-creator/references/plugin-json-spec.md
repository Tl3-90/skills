# Portable plugin reference

The current portable package format uses a root `plugin.json`.

## Minimal skills-only plugin

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Reusable workflow",
  "author": {
    "name": "Publisher",
    "url": "https://github.com/publisher"
  },
  "repository": "https://github.com/publisher/repository",
  "extensions": {
    "com.openai": {
      "interface": {
        "displayName": "Plugin Name",
        "shortDescription": "Short description",
        "longDescription": "Long description",
        "developerName": "Publisher",
        "category": "Productivity",
        "capabilities": ["Primary capability"],
        "defaultPrompt": ["Use this plugin for its primary workflow."]
      }
    }
  }
}
```

Skills are discovered from `skills/<skill-name>/SKILL.md`. Do not declare `skills` in the portable root manifest.

A legacy `.codex-plugin/plugin.json` may remain as a compatibility fallback. In that fallback only, `"skills": "./skills/"` is accepted.

## Repository marketplace

Place the catalog at `.agents/plugins/marketplace.json` in the repository root. Same-repository entries use a relative local source:

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

The marketplace file is a distribution catalog, not proof of installation. Workspace admins can import a GitHub marketplace. Installed plugin skills are then available in new ChatGPT chats on supported web, desktop, and mobile surfaces.

## Mobile checklist

- Core behavior lives in `SKILL.md`.
- No required shell, local path, hook, or local-only service.
- External actions use connected tools.
- All references and assets are bundled.
- Root portable manifest is present.
- Marketplace entry resolves inside the repository.
