#!/usr/bin/env python3
"""Scaffold a repository-managed ChatGPT plugin and optionally update marketplace.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


MAX_PLUGIN_NAME_LENGTH = 64
DEFAULT_PLUGIN_PARENT = Path.cwd() / "plugins"
DEFAULT_MARKETPLACE_PATH = Path.cwd() / ".agents" / "plugins" / "marketplace.json"
DEFAULT_INSTALL_POLICY = "AVAILABLE"
DEFAULT_AUTH_POLICY = "ON_INSTALL"
DEFAULT_CATEGORY = "Productivity"
DEFAULT_MARKETPLACE_DISPLAY_NAME = "[TODO: Marketplace Display Name]"
VALID_INSTALL_POLICIES = {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}
VALID_AUTH_POLICIES = {"ON_INSTALL", "ON_USE"}


def normalize_plugin_name(plugin_name: str) -> str:
    """Normalize a plugin name to lowercase hyphen-case."""
    normalized = plugin_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def validate_plugin_name(plugin_name: str) -> None:
    if not plugin_name:
        raise ValueError("Plugin name must include at least one letter or digit.")
    if len(plugin_name) > MAX_PLUGIN_NAME_LENGTH:
        raise ValueError(
            f"Plugin name '{plugin_name}' is too long ({len(plugin_name)} characters). "
            f"Maximum is {MAX_PLUGIN_NAME_LENGTH} characters."
        )


def build_plugin_json(plugin_name: str) -> dict:
    display_name = plugin_name.replace("-", " ").title()
    return {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": plugin_name,
        "version": "1.0.0",
        "description": f"Reusable workflows provided by the {display_name} plugin.",
        "author": {"name": "Plugin Author"},
        "extensions": {
            "com.openai": {
                "interface": {
                    "displayName": display_name,
                    "shortDescription": f"Use {display_name} workflows",
                    "longDescription": f"Reusable workflows packaged by {display_name}.",
                    "developerName": "Plugin Author",
                    "category": "Productivity",
                    "capabilities": ["Reusable skill workflow"],
                    "defaultPrompt": [
                        f"Use {display_name} for its primary workflow."
                    ],
                }
            }
        },
    }


def build_marketplace_entry(
    plugin_name: str,
    install_policy: str,
    auth_policy: str,
    category: str,
) -> dict[str, Any]:
    return {
        "name": plugin_name,
        "source": {
            "source": "local",
            "path": f"./plugins/{plugin_name}",
        },
        "policy": {
            "installation": install_policy,
            "authentication": auth_policy,
        },
        "category": category,
    }


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def build_default_marketplace() -> dict[str, Any]:
    return {
        "name": "[TODO: marketplace-name]",
        "interface": {
            "displayName": DEFAULT_MARKETPLACE_DISPLAY_NAME,
        },
        "plugins": [],
    }


def validate_marketplace_interface(payload: dict[str, Any]) -> None:
    interface = payload.get("interface")
    if interface is not None and not isinstance(interface, dict):
        raise ValueError("marketplace.json field 'interface' must be an object.")


def update_marketplace_json(
    marketplace_path: Path,
    plugin_name: str,
    install_policy: str,
    auth_policy: str,
    category: str,
    force: bool,
) -> None:
    if marketplace_path.exists():
        payload = load_json(marketplace_path)
    else:
        payload = build_default_marketplace()

    if not isinstance(payload, dict):
        raise ValueError(f"{marketplace_path} must contain a JSON object.")

    validate_marketplace_interface(payload)

    plugins = payload.setdefault("plugins", [])
    if not isinstance(plugins, list):
        raise ValueError(f"{marketplace_path} field 'plugins' must be an array.")

    new_entry = build_marketplace_entry(plugin_name, install_policy, auth_policy, category)

    for index, entry in enumerate(plugins):
        if isinstance(entry, dict) and entry.get("name") == plugin_name:
            if not force:
                raise FileExistsError(
                    f"Marketplace entry '{plugin_name}' already exists in {marketplace_path}. "
                    "Use --force to overwrite that entry."
                )
            plugins[index] = new_entry
            break
    else:
        plugins.append(new_entry)

    write_json(marketplace_path, payload, force=True)


def write_json(path: Path, data: dict, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def create_stub_file(path: Path, payload: dict, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a repository-managed ChatGPT plugin skeleton with plugin.json."
    )
    parser.add_argument("plugin_name")
    parser.add_argument(
        "--path",
        default=str(DEFAULT_PLUGIN_PARENT),
        help="Parent directory for plugin creation (defaults to ./plugins from the current repository root).",
    )
    parser.add_argument("--with-skills", action="store_true", help="Create skills/ directory")
    parser.add_argument("--with-hooks", action="store_true", help="Create hooks/ directory")
    parser.add_argument("--with-scripts", action="store_true", help="Create scripts/ directory")
    parser.add_argument("--with-assets", action="store_true", help="Create assets/ directory")
    parser.add_argument("--with-mcp", action="store_true", help="Create .mcp.json placeholder")
    parser.add_argument("--with-apps", action="store_true", help="Create .app.json placeholder")
    parser.add_argument(
        "--with-marketplace",
        action="store_true",
        help="Create or update ./.agents/plugins/marketplace.json by default.",
    )
    parser.add_argument(
        "--marketplace-path",
        default=str(DEFAULT_MARKETPLACE_PATH),
        help="Path to marketplace.json (defaults to ./.agents/plugins/marketplace.json).",
    )
    parser.add_argument(
        "--install-policy",
        default=DEFAULT_INSTALL_POLICY,
        choices=sorted(VALID_INSTALL_POLICIES),
        help="Marketplace policy.installation value",
    )
    parser.add_argument(
        "--auth-policy",
        default=DEFAULT_AUTH_POLICY,
        choices=sorted(VALID_AUTH_POLICIES),
        help="Marketplace policy.authentication value",
    )
    parser.add_argument(
        "--category",
        default=DEFAULT_CATEGORY,
        help="Marketplace category value",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_plugin_name = args.plugin_name
    plugin_name = normalize_plugin_name(raw_plugin_name)
    if plugin_name != raw_plugin_name:
        print(f"Note: Normalized plugin name from '{raw_plugin_name}' to '{plugin_name}'.")
    validate_plugin_name(plugin_name)

    plugin_root = Path(args.path).expanduser().resolve() / plugin_name
    plugin_root.mkdir(parents=True, exist_ok=True)

    manifest_path = plugin_root / "plugin.json"
    write_json(manifest_path, build_plugin_json(plugin_name), args.force)

    optional_directories = {
        "skills": args.with_skills,
        "scripts": args.with_scripts,
        "assets": args.with_assets,
    }
    for folder, enabled in optional_directories.items():
        if enabled:
            (plugin_root / folder).mkdir(parents=True, exist_ok=True)

    if args.with_hooks:
        create_stub_file(plugin_root / "hooks.json", {"hooks": {}}, args.force)

    if args.with_mcp:
        create_stub_file(plugin_root / ".mcp.json", {"mcpServers": {}}, args.force)

    if args.with_apps:
        create_stub_file(plugin_root / ".app.json", {"apps": {}}, args.force)

    if args.with_marketplace:
        marketplace_path = Path(args.marketplace_path).expanduser().resolve()
        update_marketplace_json(
            marketplace_path,
            plugin_name,
            args.install_policy,
            args.auth_policy,
            args.category,
            args.force,
        )

    print(f"Created repository plugin scaffold: {plugin_root}")
    print(f"plugin manifest: {manifest_path}")
    if args.with_marketplace:
        print(f"marketplace manifest: {marketplace_path}")


if __name__ == "__main__":
    main()
