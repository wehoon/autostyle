# -*- coding: utf-8 -*-
"""
Style Config Manager

Handles CRUD operations for style configs, stored as JSON files in the styles directory.
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple

from .i18n import tr


class StyleManager:
    """Style config manager."""

    def __init__(self, styles_dir: str):
        """
        Initialize the style manager.

        :param styles_dir: Directory path for storing style configs
        """
        self.styles_dir = styles_dir
        self._ensure_dir_exists()

    def _ensure_dir_exists(self):
        """Ensure the styles directory exists."""
        if not os.path.exists(self.styles_dir):
            os.makedirs(self.styles_dir)

    def _get_config_path(self, name: str) -> str:
        """
        Get the file path for a config.

        :param name: Config name
        :return: Full file path
        """
        safe_name = self._sanitize_filename(name)
        return os.path.join(self.styles_dir, f"{safe_name}.json")

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize filename by removing unsafe characters.

        :param name: Original name
        :return: Safe filename
        """
        return re.sub(r'[<>:"/\\|?*]', '_', name)

    def list_configs(self) -> List[str]:
        """
        List all config names.

        :return: List of config names (derived from filenames)
        """
        configs = []
        if not os.path.exists(self.styles_dir):
            return configs

        for filename in os.listdir(self.styles_dir):
            if filename.endswith('.json'):
                # Use filename without extension as config name
                config_name = filename[:-5]  # Remove '.json'
                configs.append(config_name)
        return sorted(configs)

    def load_config(self, name: str) -> Optional[Dict]:
        """
        Load a specific config.

        :param name: Config name
        :return: Config data dict (with 'name' field added), or None if load failed
        """
        config_path = self._get_config_path(name)
        if not os.path.exists(config_path):
            return None

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Add name field derived from filename
                config['name'] = name
                return config
        except (json.JSONDecodeError, IOError):
            return None

    def save_config(self, name: str, content: str, old_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        Save a config.

        :param name: Config name
        :param content: Config content (format: "<regexp>": "<style_file>" per line)
        :param old_name: Old config name (for renaming, to delete old file)
        :return: (success, error_message)
        """
        if not name or not name.strip():
            return False, tr('config_name_empty')

        name = name.strip()

        # Parse config content
        rules, error = self._parse_content(content)
        if error:
            return False, error

        # If renaming, delete old file first
        if old_name and old_name != name:
            old_path = self._get_config_path(old_name)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except IOError as e:
                    return False, tr('delete_old_config_failed', error=str(e))

        # Build config data (only store rules, name is derived from filename)
        config_data = {
            "rules": rules,
        }

        # Save to file
        config_path = self._get_config_path(name)
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            return True, ""
        except IOError as e:
            return False, tr('save_config_failed', error=str(e))

    def delete_config(self, name: str) -> Tuple[bool, str]:
        """
        Delete a config.

        :param name: Config name
        :return: (success, error_message)
        """
        config_path = self._get_config_path(name)
        if not os.path.exists(config_path):
            return False, tr('config_not_exist')

        try:
            os.remove(config_path)
            return True, ""
        except IOError as e:
            return False, tr('delete_config_failed', error=str(e))

    def _parse_content(self, content: str) -> Tuple[List[Dict], Optional[str]]:
        """
        Parse config content.

        :param content: Config content string
        :return: (rules_list, error_message)
        """
        rules = []
        if not content or not content.strip():
            return rules, None

        # Match format: "pattern": "style_file"
        pattern = re.compile(r'^"(.+)"\s*:\s*"(.+)"$')

        for line_num, line in enumerate(content.strip().split('\n'), 1):
            line = line.strip()
            if not line:
                continue

            match = pattern.match(line)
            if not match:
                return [], tr('format_error_msg', line=line_num, content=line)

            regex_pattern = match.group(1)
            style_file = match.group(2)

            # Validate regex syntax
            try:
                re.compile(regex_pattern)
            except re.error as e:
                return [], tr('regex_syntax_error', row=line_num, error=str(e))

            rules.append({
                "pattern": regex_pattern,
                "style_file": style_file,
            })

        return rules, None

    def get_content_text(self, config: Dict) -> str:
        """
        Convert config data to text format.

        :param config: Config data dict
        :return: Text format content
        """
        lines = []
        for rule in config.get('rules', []):
            pattern = rule.get('pattern', '')
            style_file = rule.get('style_file', '')
            lines.append(f'"{pattern}": "{style_file}"')
        return '\n'.join(lines)

    def export_config(self, name: str, export_path: str) -> Tuple[bool, str]:
        """
        Export a config to a specified path.

        :param name: Config name to export
        :param export_path: Target file path
        :return: (success, error_message)
        """
        config = self.load_config(name)
        if not config:
            return False, tr('config_not_exist')

        # Only export rules, name is derived from filename
        export_data = {"rules": config.get('rules', [])}
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            return True, ""
        except IOError as e:
            return False, str(e)

    def import_config(self, import_path: str, overwrite: bool = False) -> Tuple[bool, str, str]:
        """
        Import a config from a specified path.

        :param import_path: Source file path
        :param overwrite: Whether to overwrite existing config
        :return: (success, error_message, config_name)
        """
        # Get config name from import filename
        import_filename = os.path.basename(import_path)
        if import_filename.endswith('.json'):
            name = import_filename[:-5]  # Remove '.json'
        else:
            name = import_filename

        if not name:
            return False, tr('config_name_empty'), ""

        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            return False, str(e), ""

        # Validate config format
        if not isinstance(config, dict):
            return False, tr('invalid_config_format'), ""

        # Check if config already exists
        existing_path = self._get_config_path(name)
        if os.path.exists(existing_path) and not overwrite:
            return False, "EXISTS", name

        # Validate rules format
        rules = config.get('rules', [])
        if not isinstance(rules, list):
            return False, tr('invalid_config_format'), ""

        for rule in rules:
            if not isinstance(rule, dict):
                return False, tr('invalid_config_format'), ""
            if 'pattern' not in rule or 'style_file' not in rule:
                return False, tr('invalid_config_format'), ""
            # Validate regex syntax
            try:
                re.compile(rule['pattern'])
            except re.error as e:
                return False, tr('regex_syntax_error', row=0, error=str(e)), ""

        # Save config (only store rules, name is derived from filename)
        config_data = {"rules": rules}
        try:
            with open(existing_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            return True, "", name
        except IOError as e:
            return False, str(e), ""

    def config_exists(self, name: str) -> bool:
        """
        Check if a config exists.

        :param name: Config name
        :return: True if exists
        """
        config_path = self._get_config_path(name)
        return os.path.exists(config_path)
