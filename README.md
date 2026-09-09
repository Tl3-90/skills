# Thomas Skills

GitHub-hosted portable skill plugins for ChatGPT.

## Plugin Creator

`plugins/plugin-creator` packages reusable workflows as skills-only plugins for ChatGPT. Its core instructions are designed to work in ChatGPT on web, desktop, and mobile when the plugin and required connected tools are available to the account.

## Install for ChatGPT mobile

A GitHub repository does not install itself into the mobile app.

### Workspace marketplace

A ChatGPT workspace admin can import this repository from **Admin > Plugins > Add > Import marketplace**:

- Source: `Tl3-90/skills`
- Path: leave empty
- Branch: `main`

Install **Plugin Creator** from the workspace Plugins directory. Then start a new ChatGPT mobile chat and invoke `@plugin-creator`.

### Public directory

For accounts without workspace marketplace import, submit `plugins/plugin-creator` as a **Skills only** plugin through the OpenAI plugin submission portal. After review and publication, install it from the Plugins directory and use it in a new mobile chat.

## Package layout

- `.agents/plugins/marketplace.json`: repository marketplace
- `plugins/plugin-creator/plugin.json`: canonical portable manifest
- `plugins/plugin-creator/skills/plugin-creator/SKILL.md`: reusable workflow
