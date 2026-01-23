# -*- coding: utf-8 -*-
"""
AutoStyle Main Plugin Class

Manages plugin lifecycle, menu/toolbar integration, and main dialog creation.
"""

import os
import webbrowser

from qgis.core import Qgis
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QTextEdit
from qgis.PyQt.QtWidgets import QVBoxLayout

from .core.i18n import tr
from .core.update_checker import UpdateChecker
from .core.update_checker import UpdateInfo

# Settings keys
SETTINGS_KEY_SKIP_VERSION = "AutoStyle/skip_version"
SETTINGS_KEY_CHECK_UPDATE = "AutoStyle/check_update_on_startup"


class UpdateSignal(QObject):
    """Signal emitter for thread-safe UI updates."""

    update_checked = pyqtSignal(object)


class AutoStyle:
    """AutoStyle plugin main class."""

    def __init__(self, iface):
        """
        Initialize the plugin.

        :param iface: QgisInterface instance
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu_name = "AutoStyle"
        self.toolbar = None
        self.main_dialog = None

        # Update checker
        self.update_checker = UpdateChecker(self.plugin_dir)
        self.update_signal = UpdateSignal()
        self.update_signal.update_checked.connect(self._on_update_checked)

    def initGui(self):
        """Initialize plugin GUI, add menu items and toolbar buttons."""
        icon_path = os.path.join(self.plugin_dir, "icon.svg")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

        # Create main action
        self.action_main = QAction(icon, "AutoStyle", self.iface.mainWindow())
        self.action_main.triggered.connect(self.show_dialog)
        self.actions.append(self.action_main)

        # Create check update action
        self.action_check_update = QAction(
            tr('check_update_menu'),
            self.iface.mainWindow(),
        )
        self.action_check_update.triggered.connect(self._check_update_manual)
        self.actions.append(self.action_check_update)

        # Add to plugin menu
        self.iface.addPluginToMenu(self.menu_name, self.action_main)
        self.iface.addPluginToMenu(self.menu_name, self.action_check_update)

        # Create toolbar
        self.toolbar = self.iface.addToolBar("AutoStyle")
        self.toolbar.setObjectName("AutoStyleToolbar")
        self.toolbar.addAction(self.action_main)

        # Check for updates on startup (async, non-blocking)
        self._check_update_on_startup()

    def unload(self):
        """Unload plugin, remove menu items and toolbar."""
        # Remove menu items
        for action in self.actions:
            self.iface.removePluginMenu(self.menu_name, action)

        # Remove toolbar
        if self.toolbar:
            del self.toolbar

        # Close dialog
        if self.main_dialog:
            self.main_dialog.close()
            self.main_dialog = None

    def show_dialog(self):
        """Show the main dialog."""
        from .ui.panel_widget import MainDialog

        if self.main_dialog is None:
            self.main_dialog = MainDialog(
                self.plugin_dir,
                self.iface,
                parent=self.iface.mainWindow(),
            )

        # Refresh config list
        self.main_dialog._load_configs()
        self.main_dialog.show()
        self.main_dialog.raise_()
        self.main_dialog.activateWindow()

    def _check_update_on_startup(self):
        """Check for updates on plugin startup."""
        settings = QSettings()

        # Check if update check is enabled (default: True)
        check_enabled = settings.value(SETTINGS_KEY_CHECK_UPDATE, True, type=bool)
        if not check_enabled:
            return

        self.update_checker.check_update_async(self._emit_update_result)

    def _check_update_manual(self):
        """Manually check for updates (from menu)."""
        self.iface.messageBar().pushMessage(
            "AutoStyle",
            tr('update_checking'),
            level=Qgis.Info,
            duration=3,
        )
        self.update_checker.check_update_async(
            lambda info: self._emit_update_result(info, manual=True)
        )

    def _emit_update_result(self, update_info: UpdateInfo, manual: bool = False):
        """
        Emit update result signal (thread-safe).

        :param update_info: Update check result
        :param manual: Whether this is a manual check
        """
        # Attach manual flag to info for later use
        update_info._manual_check = manual
        self.update_signal.update_checked.emit(update_info)

    def _on_update_checked(self, update_info: UpdateInfo):
        """
        Handle update check result (runs on main thread).

        :param update_info: Update check result
        """
        manual = getattr(update_info, '_manual_check', False)

        if update_info.error:
            if manual:
                self.iface.messageBar().pushMessage(
                    "AutoStyle",
                    tr('update_check_failed', error=update_info.error),
                    level=Qgis.Warning,
                    duration=5,
                )
            return

        if not update_info.has_update:
            if manual:
                self.iface.messageBar().pushMessage(
                    "AutoStyle",
                    tr('update_no_update', version=update_info.current_version),
                    level=Qgis.Success,
                    duration=5,
                )
            return

        # Check if user chose to skip this version
        settings = QSettings()
        skipped_version = settings.value(SETTINGS_KEY_SKIP_VERSION, "")
        if skipped_version == update_info.latest_version and not manual:
            return

        # Show update dialog
        self._show_update_dialog(update_info)

    def _show_update_dialog(self, update_info: UpdateInfo):
        """
        Show update available dialog.

        :param update_info: Update information
        """
        dialog = QDialog(self.iface.mainWindow())
        dialog.setWindowTitle(tr('update_available_title'))
        dialog.setMinimumSize(450, 300)
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Version info
        msg = tr(
            'update_available_msg',
            current=update_info.current_version,
            latest=update_info.latest_version,
        )
        label = QLabel(msg)
        label.setWordWrap(True)
        layout.addWidget(label)

        # Changelog
        if update_info.changelog:
            changelog_label = QLabel(tr('update_changelog_label'))
            layout.addWidget(changelog_label)

            changelog_text = QTextEdit()
            changelog_text.setPlainText(update_info.changelog)
            changelog_text.setReadOnly(True)
            changelog_text.setMaximumHeight(150)
            layout.addWidget(changelog_text)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        btn_skip = QPushButton(tr('update_skip_version_button'))
        btn_skip.clicked.connect(
            lambda: self._skip_version(update_info.latest_version, dialog)
        )
        btn_layout.addWidget(btn_skip)

        btn_layout.addStretch()

        btn_ignore = QPushButton(tr('update_ignore_button'))
        btn_ignore.clicked.connect(dialog.reject)
        btn_layout.addWidget(btn_ignore)

        btn_download = QPushButton(tr('update_download_button'))
        btn_download.setDefault(True)
        btn_download.clicked.connect(
            lambda: self._open_download(update_info.download_url, dialog)
        )
        btn_layout.addWidget(btn_download)

        layout.addLayout(btn_layout)

        dialog.exec_()

    def _skip_version(self, version: str, dialog: QDialog):
        """
        Skip a specific version.

        :param version: Version to skip
        :param dialog: Dialog to close
        """
        settings = QSettings()
        settings.setValue(SETTINGS_KEY_SKIP_VERSION, version)
        dialog.accept()

    def _open_download(self, url: str, dialog: QDialog):
        """
        Open download URL in browser.

        :param url: Download URL
        :param dialog: Dialog to close
        """
        if url:
            webbrowser.open(url)
        dialog.accept()
