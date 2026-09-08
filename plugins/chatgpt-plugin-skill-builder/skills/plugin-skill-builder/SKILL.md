---
name: plugin-skill-builder
description: Use this skill when creating a ChatGPT/Codex plugin skill from a reusable workflow, prompt pattern, agent behavior, checklist, or operating procedure. Typical triggers include making a skills-only plugin, converting a workflow into SKILL.md, preparing a plugin ZIP, validating plugin package shape, or deciding whether MCP is unnecessary.
---

# Plugin Skill Builder

Use this skill to create a ChatGPT-ready skills-only plugin when the user wants reusable behavior without a live MCP server.

## When To Use

Use this skill when the user asks to:

- create a plugin that contains skills;
- turn a workflow, prompt, checklist, or agent behavior into a reusable Skill;
- build a plugin that does not need MCP;
- package a skill for ChatGPT/Codex plugin reuse;
- validate whether a plugin is skills-only, MCP-backed, or hybrid.

Do not assume a URL or tunnel is required unless the plugin needs live tools, external actions, OAuth, server state, or an MCP endpoint.

## Required Plugin Shape

A skills-only plugin should use this shape:

```text
plugin-name/
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   └── skill-name/
│       └── SKILL.md
├── assets/
│   ├── logo-light.svg
│   └── icon.svg
└── README.md
```

Rules:

- `.codex-plugin/plugin.json` must exist.
- Only `plugin.json` belongs inside `.codex-plugin/`.
- Every skill must be an immediate child of `skills/`.
- Every skill folder must contain `SKILL.md`.
- The plugin should not declare MCP or app files unless those components are active.
- Do not claim installation, upload, approval, or publication unless that step actually happened.

## SKILL.md Requirements

Every Skill needs:

- YAML frontmatter with `name` and `description`;
- trigger-oriented description;
- clear use cases;
- steps or workflow;
- expected output;
- quality checks;
- limits or stop conditions when relevant.

Use this starter:

```markdown
---
name: skill-name
description: Use this skill when [specific trigger]. Typical triggers include [scenario 1], [scenario 2], and [scenario 3].
---

# Skill Name

## When To Use

[When this applies.]

## Process

1. [Step one]
2. [Step two]
3. [Step three]

## Output

[Required response or artifact shape.]

## Quality Bar

- [Check one]
- [Check two]
```

## Build Process

1. Name the reusable behavior in plain language.
2. Decide if it is skills-only, MCP-backed, or hybrid.
3. If skills-only, create the plugin scaffold.
4. Write one focused Skill per reusable workflow.
5. Add supporting references only when they reduce repeated explanation.
6. Update `plugin.json` with accurate name, description, capabilities, prompt, logo, and icon.
7. Validate the plugin.
8. Package the ZIP.
9. Keep local validation, upload, submission, approval, and publication as separate statuses.

## Output Format

Return:

```markdown
**Plugin Type**
[skills-only | MCP-backed | hybrid]

**Plugin Name**
[name]

**Skill Created**
[skill name]

**Files**
[important paths]

**Validation**
[checks actually run]

**Next Step**
[install/test/upload/submission step]
```

## Quality Bar

The result is only acceptable if:

- the plugin type is explicit;
- the Skill has a valid `SKILL.md`;
- the package avoids fake MCP dependencies;
- validation status is evidence-based;
- the answer does not confuse local testing with app-wide availability.
