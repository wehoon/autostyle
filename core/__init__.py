# -*- coding: utf-8 -*-
"""
AutoStyle Core Module

Contains style manager, layer processor, i18n module, and path utilities.
"""

from .i18n import get_current_language, tr
from .paths import get_autostyle_data_dir, get_styles_dir

__all__ = ['get_autostyle_data_dir', 'get_current_language', 'get_styles_dir', 'tr']
