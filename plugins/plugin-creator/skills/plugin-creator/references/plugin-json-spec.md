# Plugin JSON reference

Use `.codex-plugin/plugin.json` at the plugin root.

## Skills-only example

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "url": "https://github.com/author"
  },
  "repository": "https://github.com/author/repository",
  "skills": "./skills/",
  "interface": {
    "displayName": "Plugin Display Name",
    "shortDescription": "Short description",
    "longDescription": "Longer description of the plugin workflow.",
    "developerName": "Author Name",
    "category": "Productivity",
    "capabilities": ["Interactive", "Write"],
    "defaultPrompt": [
      "Use this plugin for its primary workflow."
    ],
    "composerIcon": "./assets/icon.svg",
    "logo": "./assets/logo.svg"
  }
}
```

## Component fields

- `skills`: relative path to bundled skills.
- `hooks`: optional hook configuration path.
- `mcpServers`: optional MCP configuration path or supported inline configuration.
- `apps`: optional app manifest path.

For a skills-only plugin, declare `skills` and omit MCP/app/hook component fields unless those components actually exist.

## Interface fields

- `displayName`: user-facing plugin name.
- `shortDescription`: compact subtitle.
- `longDescription`: fuller workflow description.
- `developerName`: publisher name.
- `category`: plugin category.
- `capabilities`: implementation-derived capabilities.
- `websiteURL`: optional website.
- `privacyPolicyURL`: optional privacy policy.
- `termsOfServiceURL`: optional terms URL.
- `defaultPrompt`: array of at most three starter prompts; keep each prompt under 128 characters.
- `brandColor`: optional brand color.
- `composerIcon`: relative asset path.
- `logo`: relative asset path.
- `screenshots`: optional PNG paths under `./assets/`.

All component and asset paths are relative to the plugin root and should begin with `./`.

# GitHub marketplace JSON reference

For a GitHub-hosted marketplace imported by ChatGPT, place the manifest at:

```text
<repo-root>/.agents/plugins/marketplace.json
```

Example:

```json
{
  "name": "team-plugins",
  "interface": {
    "displayName": "Team Plugins"
  },
  "plugins": [
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
  ]
}
```

## Marketplace rules

- `name`: marketplace identifier.
- `interface.displayName`: optional human-facing marketplace name.
- `plugins`: ordered plugin entries.
- Plugin entry `name` must match the plugin folder and `plugin.json` name.
- Same-repository plugin sources use `source: "local"` and `path: "./plugins/<plugin-name>"`.
- `policy.installation` values: `NOT_AVAILABLE`, `AVAILABLE`, `INSTALLED_BY_DEFAULT`.
- `policy.authentication` values: `ON_INSTALL`, `ON_USE`.
- New entries default to `AVAILABLE` and `ON_INSTALL` unless another policy is explicitly required.
- Omit `policy.products` unless product gating is explicitly required.
- Preserve unrelated existing marketplace entries.

## ChatGPT import boundary

The GitHub repository is the distribution source. ChatGPT workspace admins import the repository from Workspace settings > Plugins > Add > Import marketplace. When `.agents/plugins/marketplace.json` is at repository root, leave the Path field empty.

Creating or pushing repository files does not itself prove that the plugin is installed in ChatGPT. Treat installation as verified only after ChatGPT reports a successful import/install.

## Local Codex-only exception

A home-local marketplace such as `~/.agents/plugins/marketplace.json` is appropriate only when the user explicitly asks for a local Codex plugin. Do not substitute that destination for a GitHub/ChatGPT marketplace request.
