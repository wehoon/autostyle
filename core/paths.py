# -*- coding: utf-8 -*-
"""
AutoStyle Paths Module

Provides cross-platform path utilities for storing plugin data.
"""

import os
import sys


def get_autostyle_data_dir() -> str:
    """
    Get the AutoStyle data directory in the user's QGIS configuration directory.

    This function returns a cross-platform path for storing AutoStyle
    configuration files in the user's QGIS directory, independent of
    plugin installation to prevent data loss during plugin updates.

    Platform-specific paths:
    - Windows: %APPDATA%/QGIS/QGIS3/AutoStyle
    - macOS: ~/Library/Application Support/QGIS/QGIS3/AutoStyle
    - Linux: ~/.local/share/QGIS/QGIS3/AutoStyle

    :return: Path to the AutoStyle data directory
    """
    if sys.platform == 'win32':
        # Windows: %APPDATA%/QGIS/QGIS3/AutoStyle
        appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
        base_dir = os.path.join(appdata, 'QGIS', 'QGIS3', 'AutoStyle')
    elif sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/QGIS/QGIS3/AutoStyle
        base_dir = os.path.join(
            os.path.expanduser('~'),
            'Library',
            'Application Support',
            'QGIS',
            'QGIS3',
            'AutoStyle',
        )
    else:
        # Linux and other Unix-like systems: ~/.local/share/QGIS/QGIS3/AutoStyle
        xdg_data_home = os.environ.get(
            'XDG_DATA_HOME',
            os.path.join(os.path.expanduser('~'), '.local', 'share'),
        )
        base_dir = os.path.join(xdg_data_home, 'QGIS', 'QGIS3', 'AutoStyle')

    return base_dir


def get_styles_dir() -> str:
    """
    Get the styles configuration directory.

    :return: Path to the styles directory
    """
    return os.path.join(get_autostyle_data_dir(), 'styles')


def ensure_dir_exists(dir_path: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.

    :param dir_path: Path to the directory
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
