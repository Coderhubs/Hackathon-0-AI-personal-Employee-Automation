#!/usr/bin/env python3
"""
Plugin Manager
Discovers and manages watcher plugins dynamically
"""

import json
import os
import sys
from pathlib import Path
import importlib.util
import subprocess

class PluginManager:
    """
    Manages watcher plugins and MCP servers.

    Features:
    - Auto-discovery of watcher plugins
    - Dynamic loading from configuration
    - Plugin validation
    - Centralized plugin management
    """

    def __init__(self, base_dir="Gold_Tier"):
        self.base_dir = Path(base_dir)
        self.config_file = self.base_dir / "Config" / "watchers_config.json"
        self.mcp_config_file = self.base_dir / "Config" / "mcp_config.json"
        self.config = self.load_config()
        self.mcp_config = self.load_mcp_config()

    def load_config(self):
        """Load watchers configuration"""
        if not self.config_file.exists():
            return {"watchers": [], "plugin_discovery": {"enabled": False}}

        with open(self.config_file, 'r') as f:
            return json.load(f)

    def load_mcp_config(self):
        """Load MCP configuration"""
        if not self.mcp_config_file.exists():
            return {"mcpServers": {}}

        with open(self.mcp_config_file, 'r') as f:
            return json.load(f)

    def discover_watchers(self):
        """
        Auto-discover watcher plugins.

        Looks for files matching pattern (default: *_watcher.py)
        Excludes base classes and templates
        """
        discovered = []

        if not self.config.get("plugin_discovery", {}).get("enabled", False):
            return discovered

        pattern = self.config.get("plugin_discovery", {}).get("pattern", "*_watcher.py")
        exclude = self.config.get("plugin_discovery", {}).get("exclude", [])

        for watcher_file in self.base_dir.glob(pattern):
            if watcher_file.name not in exclude:
                # Check if already in config
                if not any(w["script"] == watcher_file.name for w in self.config.get("watchers", [])):
                    discovered.append({
                        "name": watcher_file.stem.replace("_", " ").title(),
                        "script": watcher_file.name,
                        "enabled": True,
                        "description": f"Auto-discovered watcher: {watcher_file.name}",
                        "interval_seconds": 60
                    })

        return discovered

    def get_enabled_watchers(self):
        """Get list of enabled watchers (configured + discovered)"""
        watchers = [w for w in self.config.get("watchers", []) if w.get("enabled", True)]

        # Add auto-discovered watchers
        if self.config.get("plugin_discovery", {}).get("enabled", False):
            watchers.extend(self.discover_watchers())

        return watchers

    def get_enabled_mcp_servers(self):
        """Get list of enabled MCP servers"""
        return self.mcp_config.get("mcpServers", {})

    def validate_watcher(self, watcher_script):
        """
        Validate that watcher script exists and is executable.

        Args:
            watcher_script: Filename of watcher script

        Returns:
            True if valid, False otherwise
        """
        watcher_path = self.base_dir / watcher_script
        return watcher_path.exists() and watcher_path.suffix == ".py"

    def start_watcher(self, watcher_config):
        """
        Start a watcher plugin.

        Args:
            watcher_config: Watcher configuration dict

        Returns:
            subprocess.Popen object or None
        """
        script = watcher_config.get("script")
        name = watcher_config.get("name", script)

        if not self.validate_watcher(script):
            print(f"Error: Invalid watcher script: {script}")
            return None

        script_path = self.base_dir / script

        try:
            # Start watcher in new window
            if sys.platform == "win32":
                process = subprocess.Popen(
                    ["start", name, "python", str(script_path)],
                    shell=True,
                    cwd=str(self.base_dir)
                )
            else:
                process = subprocess.Popen(
                    ["python3", str(script_path)],
                    cwd=str(self.base_dir)
                )

            print(f"Started: {name}")
            return process

        except Exception as e:
            print(f"Error starting {name}: {e}")
            return None

    def start_all_watchers(self):
        """Start all enabled watchers"""
        watchers = self.get_enabled_watchers()
        processes = []

        print(f"Starting {len(watchers)} watchers...")

        for watcher in watchers:
            process = self.start_watcher(watcher)
            if process:
                processes.append(process)

        return processes

    def list_watchers(self):
        """List all available watchers"""
        print("\n=== Configured Watchers ===")
        for watcher in self.config.get("watchers", []):
            status = "✓ Enabled" if watcher.get("enabled", True) else "✗ Disabled"
            print(f"{status} - {watcher['name']}: {watcher['script']}")

        print("\n=== Auto-Discovered Watchers ===")
        discovered = self.discover_watchers()
        if discovered:
            for watcher in discovered:
                print(f"✓ New - {watcher['name']}: {watcher['script']}")
        else:
            print("None")

        print("\n=== MCP Servers ===")
        for name, config in self.mcp_config.get("mcpServers", {}).items():
            print(f"✓ {name}: {config.get('description', 'No description')}")

    def add_watcher(self, name, script, description="", interval_seconds=60, enabled=True):
        """
        Add new watcher to configuration.

        Args:
            name: Watcher display name
            script: Script filename
            description: Watcher description
            interval_seconds: Check interval (None for event-driven)
            enabled: Whether to enable by default
        """
        new_watcher = {
            "name": name,
            "script": script,
            "enabled": enabled,
            "description": description,
            "interval_seconds": interval_seconds
        }

        self.config.setdefault("watchers", []).append(new_watcher)

        # Save updated config
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

        print(f"Added watcher: {name}")

    def add_mcp_server(self, name, command, args, description="", env=None):
        """
        Add new MCP server to configuration.

        Args:
            name: Server name
            command: Command to run
            args: Command arguments (list)
            description: Server description
            env: Environment variables (dict)
        """
        new_server = {
            "command": command,
            "args": args,
            "description": description
        }

        if env:
            new_server["env"] = env

        self.mcp_config.setdefault("mcpServers", {})[name] = new_server

        # Save updated config
        with open(self.mcp_config_file, 'w') as f:
            json.dump(self.mcp_config, f, indent=2)

        print(f"Added MCP server: {name}")

def main():
    """CLI for plugin management"""
    import argparse

    parser = argparse.ArgumentParser(description="Gold Tier Plugin Manager")
    parser.add_argument("command", choices=["list", "start", "add-watcher", "add-mcp"],
                       help="Command to execute")
    parser.add_argument("--name", help="Plugin name")
    parser.add_argument("--script", help="Script filename")
    parser.add_argument("--description", help="Plugin description")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds")

    args = parser.parse_args()

    manager = PluginManager()

    if args.command == "list":
        manager.list_watchers()

    elif args.command == "start":
        manager.start_all_watchers()

    elif args.command == "add-watcher":
        if not args.name or not args.script:
            print("Error: --name and --script required")
            return
        manager.add_watcher(args.name, args.script, args.description or "", args.interval)

    elif args.command == "add-mcp":
        print("Use add_mcp_server() method directly or edit Config/mcp_config.json")

if __name__ == "__main__":
    main()
