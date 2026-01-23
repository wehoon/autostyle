# -*- coding: utf-8 -*-
"""
Layer Processor

Traverses project layers, matches layer names with regex rules, and applies QML styles.
"""

import os
import re
from typing import Dict, List

from qgis.core import Qgis, QgsMapLayer, QgsMessageLog, QgsProject

from .i18n import tr


class LayerProcessor:
    """Layer processor."""

    LOG_TAG = "AutoStyle"

    def __init__(self, iface):
        """
        Initialize the layer processor.

        :param iface: QgisInterface instance
        """
        self.iface = iface

    def apply_styles(self, rules: List[Dict]) -> Dict:
        """
        Apply styles to matching layers.

        :param rules: List of style rules, each containing pattern and style_file
        :return: Result dict with success, failed, unmatched counts and details list
        """
        result = {
            "success": 0,
            "failed": 0,
            "unmatched": 0,
            "details": [],
        }

        # Get all layers from current project
        project = QgsProject.instance()
        layers = project.mapLayers().values()

        if not layers:
            result["details"].append(tr('no_layers'))
            return result

        # Pre-compile regex patterns
        compiled_rules = []
        for rule in rules:
            pattern = rule.get("pattern", "")
            style_file = rule.get("style_file", "")
            try:
                regex = re.compile(pattern)
                compiled_rules.append({
                    "regex": regex,
                    "pattern": pattern,
                    "style_file": style_file,
                })
            except re.error as e:
                msg = tr('regex_compile_failed', pattern=pattern, error=str(e))
                QgsMessageLog.logMessage(msg, self.LOG_TAG, Qgis.Warning)
                result["details"].append(msg)

        if not compiled_rules:
            result["details"].append(tr('no_valid_rules'))
            return result

        # Traverse layers and apply styles
        for layer in layers:
            layer_name = layer.name()
            matched = False

            for rule in compiled_rules:
                if rule["regex"].search(layer_name):
                    matched = True
                    style_file = rule["style_file"]

                    # Check if style file exists
                    if not os.path.exists(style_file):
                        msg = tr('style_file_not_exist', layer=layer_name, file=style_file)
                        QgsMessageLog.logMessage(msg, self.LOG_TAG, Qgis.Warning)
                        result["details"].append(msg)
                        result["failed"] += 1
                        break

                    # Apply style
                    success = self._apply_style_to_layer(layer, style_file)
                    if success:
                        msg = tr('style_apply_success', layer=layer_name, pattern=rule['pattern'])
                        QgsMessageLog.logMessage(msg, self.LOG_TAG, Qgis.Info)
                        result["details"].append(msg)
                        result["success"] += 1
                    else:
                        msg = tr('style_apply_failed', layer=layer_name, file=style_file)
                        QgsMessageLog.logMessage(msg, self.LOG_TAG, Qgis.Warning)
                        result["details"].append(msg)
                        result["failed"] += 1
                    break

            if not matched:
                msg = tr('layer_unmatched', layer=layer_name)
                QgsMessageLog.logMessage(msg, self.LOG_TAG, Qgis.Info)
                result["details"].append(msg)
                result["unmatched"] += 1

        return result

    def _apply_style_to_layer(self, layer: QgsMapLayer, style_file: str) -> bool:
        """
        Apply style file to a layer.

        :param layer: Target layer
        :param style_file: QML style file path
        :return: Success status
        """
        try:
            # Load style
            result = layer.loadNamedStyle(style_file)

            # loadNamedStyle returns tuple (message, success)
            if isinstance(result, tuple):
                message, success = result
                if not success:
                    QgsMessageLog.logMessage(
                        tr('load_style_failed', message=message),
                        self.LOG_TAG,
                        Qgis.Warning,
                    )
                    return False
            elif isinstance(result, str) and result:
                # Older QGIS versions may return error message string only
                QgsMessageLog.logMessage(
                    tr('load_style_failed', message=result),
                    self.LOG_TAG,
                    Qgis.Warning,
                )
                return False

            # Refresh layer display
            layer.triggerRepaint()

            # Refresh legend in layer panel
            if self.iface:
                self.iface.layerTreeView().refreshLayerSymbology(layer.id())

            return True

        except Exception as e:
            QgsMessageLog.logMessage(
                tr('apply_style_exception', error=str(e)),
                self.LOG_TAG,
                Qgis.Critical,
            )
            return False
