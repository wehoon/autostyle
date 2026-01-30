# -*- coding: utf-8 -*-
"""
AutoStyle Main Dialog

Provides style config selection, add, edit, delete and apply functionality.
"""

import os

from qgis.PyQt.QtCore import QSize, Qt
from qgis.PyQt.QtGui import QIcon, QPixmap
from qgis.PyQt.QtSvg import QSvgRenderer
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
)

from ..core.i18n import tr
from ..core.layer_processor import LayerProcessor
from ..core.style_manager import StyleManager

# Button size constants
BUTTON_MIN_WIDTH = 70
BUTTON_HEIGHT = 28

# Dialog size constants
DIALOG_MIN_WIDTH = 400
DIALOG_MAX_WIDTH = 800
DIALOG_HEIGHT = 110

# Button styles
BUTTON_STYLE_NORMAL = """
    QPushButton {
        background-color: #F0F0F0;
        border: 1px solid #C0C0C0;
        border-radius: 4px;
        padding: 4px 12px;
    }
    QPushButton:hover {
        background-color: #E5E5E5;
        border: 1px solid #A0A0A0;
    }
    QPushButton:pressed {
        background-color: #D0D0D0;
    }
    QPushButton:disabled {
        background-color: #F5F5F5;
        border: 1px solid #D0D0D0;
        color: #A0A0A0;
    }
"""

BUTTON_STYLE_PRIMARY = """
    QPushButton {
        background-color: #4DA6FF;
        border: 1px solid #3399FF;
        border-radius: 4px;
        padding: 4px 12px;
        color: white;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #3399FF;
        border: 1px solid #1A8CFF;
    }
    QPushButton:pressed {
        background-color: #1A8CFF;
    }
    QPushButton:disabled {
        background-color: #B3D9FF;
        border: 1px solid #99CCFF;
        color: #E0E0E0;
    }
"""

# Dropdown arrow SVG icon
SVG_ICON_DROPDOWN = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="none" stroke="#606060" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="2,4 6,8 10,4"/>
</svg>'''


def get_combobox_style(arrow_icon_path: str) -> str:
    """
    Get ComboBox style with dropdown arrow icon.

    :param arrow_icon_path: Arrow icon file path
    :return: Style string
    """
    # Convert backslashes to forward slashes (Windows compatibility)
    arrow_icon_path = arrow_icon_path.replace('\\', '/')
    return f"""
    QComboBox {{
        background-color: #FFFFFF;
        border: 1px solid #D0D0D0;
        border-radius: 4px;
        padding: 4px 8px;
        padding-right: 24px;
    }}
    QComboBox:hover {{
        border: 1px solid #A0A0A0;
    }}
    QComboBox:focus {{
        border: 1px solid #4DA6FF;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: center right;
        width: 24px;
        border: none;
        background: transparent;
    }}
    QComboBox::down-arrow {{
        image: url({arrow_icon_path});
        width: 12px;
        height: 12px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #FFFFFF;
        border: 1px solid #D0D0D0;
        selection-background-color: #E8F4FF;
        selection-color: #333333;
        outline: none;
    }}
    QComboBox QAbstractItemView::item {{
        padding: 6px 8px;
        min-height: 24px;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: #F0F0F0;
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: #E8F4FF;
    }}
    """

# Icon button style
ICON_BUTTON_SIZE = 24
ICON_BUTTON_STYLE = """
    QToolButton {
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 4px;
    }
    QToolButton:hover {
        background-color: #E5E5E5;
        border: 1px solid #C0C0C0;
    }
    QToolButton:pressed {
        background-color: #D0D0D0;
    }
    QToolButton:disabled {
        opacity: 0.5;
    }
"""

# SVG icon definitions (unified style: 2px stroke width, rounded, dark gray #505050)
SVG_ICON_ADD = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#505050" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="12" y1="5" x2="12" y2="19"/>
  <line x1="5" y1="12" x2="19" y2="12"/>
</svg>'''

SVG_ICON_EDIT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#505050" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M17 3a2.85 2.85 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
</svg>'''

SVG_ICON_DELETE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#505050" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="3 6 5 6 21 6"/>
  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
  <line x1="10" y1="11" x2="10" y2="17"/>
  <line x1="14" y1="11" x2="14" y2="17"/>
</svg>'''

SVG_ICON_HELP = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#1A73E8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
  <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>'''

SVG_ICON_EXPORT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#505050" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="7 10 12 15 17 10"/>
  <line x1="12" y1="15" x2="12" y2="3"/>
</svg>'''

SVG_ICON_IMPORT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#505050" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="17 8 12 3 7 8"/>
  <line x1="12" y1="3" x2="12" y2="15"/>
</svg>'''


def create_svg_icon(svg_content: str, size: int = 16) -> QIcon:
    """
    Create QIcon from SVG string.

    :param svg_content: SVG content string
    :param size: Icon size
    :return: QIcon object
    """
    from qgis.PyQt.QtCore import QByteArray
    from qgis.PyQt.QtGui import QPainter

    renderer = QSvgRenderer(QByteArray(svg_content.encode('utf-8')))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


class MainDialog(QDialog):
    """Main dialog."""

    def __init__(self, plugin_dir: str, iface, parent=None):
        """
        Initialize the dialog.

        :param plugin_dir: Plugin directory path
        :param iface: QgisInterface instance
        :param parent: Parent widget
        """
        super().__init__(parent)
        self.plugin_dir = plugin_dir
        self.iface = iface

        # Use user's QGIS config directory for storing styles
        from ..core.paths import get_styles_dir
        self.styles_dir = get_styles_dir()
        self.style_manager = StyleManager(self.styles_dir)
        self.layer_processor = LayerProcessor(iface)

        # Create dropdown arrow icon file
        self._dropdown_icon_path = self._create_dropdown_icon()

        self.setWindowTitle("AutoStyle")
        self.setMinimumWidth(DIALOG_MIN_WIDTH)
        self.setMaximumWidth(DIALOG_MAX_WIDTH)
        self.setFixedHeight(DIALOG_HEIGHT)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._setup_ui()
        self._load_configs()
        self._adjust_width()

    def _create_dropdown_icon(self) -> str:
        """
        Create dropdown arrow icon file.

        :return: Icon file path
        """
        import tempfile
        icon_path = os.path.join(tempfile.gettempdir(), 'autostyle_dropdown.svg')
        with open(icon_path, 'w', encoding='utf-8') as f:
            f.write(SVG_ICON_DROPDOWN)
        return icon_path

    def _setup_ui(self):
        """Setup UI layout."""
        # Main layout uses vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # Group box
        config_group = QGroupBox()
        config_layout = QVBoxLayout(config_group)
        config_layout.setContentsMargins(12, 12, 12, 12)
        config_layout.setSpacing(10)

        # Selection area: label + dropdown + icon buttons
        select_layout = QHBoxLayout()
        select_layout.setSpacing(8)
        select_layout.setAlignment(Qt.AlignVCenter)

        label = QLabel(tr('select_config'))
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label.setFixedHeight(BUTTON_HEIGHT)
        select_layout.addWidget(label)

        self.combo_configs = QComboBox()
        self.combo_configs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo_configs.setFixedHeight(BUTTON_HEIGHT)
        self.combo_configs.setStyleSheet(get_combobox_style(self._dropdown_icon_path))
        self.combo_configs.currentIndexChanged.connect(self._on_config_changed)
        select_layout.addWidget(self.combo_configs)

        # Icon button container (compact layout)
        icon_btn_layout = QHBoxLayout()
        icon_btn_layout.setSpacing(2)
        icon_btn_layout.setContentsMargins(0, 0, 0, 0)
        icon_btn_layout.setAlignment(Qt.AlignVCenter)

        # Add button (+)
        self.btn_add = QToolButton()
        self.btn_add.setIcon(create_svg_icon(SVG_ICON_ADD, 16))
        self.btn_add.setIconSize(QSize(16, 16))
        self.btn_add.setFixedSize(QSize(BUTTON_HEIGHT, BUTTON_HEIGHT))
        self.btn_add.setStyleSheet(ICON_BUTTON_STYLE)
        self.btn_add.setToolTip(tr('add_config_tooltip'))
        self.btn_add.clicked.connect(self._on_add_clicked)
        icon_btn_layout.addWidget(self.btn_add)

        # Edit button (pencil)
        self.btn_edit = QToolButton()
        self.btn_edit.setIcon(create_svg_icon(SVG_ICON_EDIT, 16))
        self.btn_edit.setIconSize(QSize(16, 16))
        self.btn_edit.setFixedSize(QSize(BUTTON_HEIGHT, BUTTON_HEIGHT))
        self.btn_edit.setStyleSheet(ICON_BUTTON_STYLE)
        self.btn_edit.setToolTip(tr('edit_config_tooltip'))
        self.btn_edit.clicked.connect(self._on_edit_clicked)
        icon_btn_layout.addWidget(self.btn_edit)

        # Delete button (trash)
        self.btn_delete = QToolButton()
        self.btn_delete.setIcon(create_svg_icon(SVG_ICON_DELETE, 16))
        self.btn_delete.setIconSize(QSize(16, 16))
        self.btn_delete.setFixedSize(QSize(BUTTON_HEIGHT, BUTTON_HEIGHT))
        self.btn_delete.setStyleSheet(ICON_BUTTON_STYLE)
        self.btn_delete.setToolTip(tr('delete_config_tooltip'))
        self.btn_delete.clicked.connect(self._on_delete_clicked)
        icon_btn_layout.addWidget(self.btn_delete)

        # Export button
        self.btn_export = QToolButton()
        self.btn_export.setIcon(create_svg_icon(SVG_ICON_EXPORT, 16))
        self.btn_export.setIconSize(QSize(16, 16))
        self.btn_export.setFixedSize(QSize(BUTTON_HEIGHT, BUTTON_HEIGHT))
        self.btn_export.setStyleSheet(ICON_BUTTON_STYLE)
        self.btn_export.setToolTip(tr('export_config_tooltip'))
        self.btn_export.clicked.connect(self._on_export_clicked)
        icon_btn_layout.addWidget(self.btn_export)

        # Import button
        self.btn_import = QToolButton()
        self.btn_import.setIcon(create_svg_icon(SVG_ICON_IMPORT, 16))
        self.btn_import.setIconSize(QSize(16, 16))
        self.btn_import.setFixedSize(QSize(BUTTON_HEIGHT, BUTTON_HEIGHT))
        self.btn_import.setStyleSheet(ICON_BUTTON_STYLE)
        self.btn_import.setToolTip(tr('import_config_tooltip'))
        self.btn_import.clicked.connect(self._on_import_clicked)
        icon_btn_layout.addWidget(self.btn_import)

        select_layout.addLayout(icon_btn_layout)

        config_layout.addLayout(select_layout)

        # Action button area
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        btn_layout.setAlignment(Qt.AlignVCenter)

        # Help icon
        self.lbl_help_icon = QLabel()
        self.lbl_help_icon.setPixmap(create_svg_icon(SVG_ICON_HELP, 16).pixmap(16, 16))
        self.lbl_help_icon.setFixedSize(16, BUTTON_HEIGHT)
        self.lbl_help_icon.setAlignment(Qt.AlignCenter)
        self.lbl_help_icon.setCursor(Qt.PointingHandCursor)
        self.lbl_help_icon.mousePressEvent = lambda e: self._on_help_clicked()
        btn_layout.addWidget(self.lbl_help_icon)

        # Help text
        help_text = tr('help_link')
        self.lbl_help = QLabel(f'<a href="#" style="color: #1A73E8; text-decoration: none;">{help_text}</a>')
        self.lbl_help.setFixedHeight(BUTTON_HEIGHT)
        self.lbl_help.setAlignment(Qt.AlignVCenter)
        self.lbl_help.setCursor(Qt.PointingHandCursor)
        self.lbl_help.linkActivated.connect(self._on_help_clicked)
        btn_layout.addWidget(self.lbl_help)

        btn_layout.addStretch()

        # Apply and close buttons (right aligned)
        self.btn_apply = QPushButton(tr('apply_button'))
        self.btn_apply.setFixedHeight(BUTTON_HEIGHT)
        self.btn_apply.setMinimumWidth(80)
        self.btn_apply.setStyleSheet(BUTTON_STYLE_PRIMARY)
        self.btn_apply.clicked.connect(self._on_apply_clicked)
        btn_layout.addWidget(self.btn_apply)

        self.btn_close = QPushButton(tr('close_button'))
        self.btn_close.setFixedHeight(BUTTON_HEIGHT)
        self.btn_close.setMinimumWidth(BUTTON_MIN_WIDTH)
        self.btn_close.setStyleSheet(BUTTON_STYLE_NORMAL)
        self.btn_close.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_close)

        config_layout.addLayout(btn_layout)

        main_layout.addWidget(config_group)

    def _load_configs(self):
        """Load config list."""
        current_text = self.combo_configs.currentText()
        self.combo_configs.clear()

        configs = self.style_manager.list_configs()
        self.combo_configs.addItems(configs)

        # Restore previously selected config
        if current_text:
            index = self.combo_configs.findText(current_text)
            if index >= 0:
                self.combo_configs.setCurrentIndex(index)

        self._update_button_states()
        self._adjust_width()

    def _adjust_width(self):
        """Adjust dialog width based on config names."""
        from qgis.PyQt.QtGui import QFontMetrics

        if self.combo_configs.count() == 0:
            self.resize(DIALOG_MIN_WIDTH, DIALOG_HEIGHT)
            return

        # Calculate max text width
        font_metrics = QFontMetrics(self.combo_configs.font())
        max_text_width = 0
        for i in range(self.combo_configs.count()):
            text = self.combo_configs.itemText(i)
            text_width = font_metrics.horizontalAdvance(text)
            max_text_width = max(max_text_width, text_width)

        # Add padding for combobox (dropdown arrow, padding, border)
        combobox_extra = 60
        # Add space for label and buttons
        # Label (~80px) + buttons (6 buttons * 30px) + spacing
        other_elements = 80 + 6 * 30 + 50
        # Add margins
        margins = 12 * 2 + 12 * 2  # main layout + group box margins

        total_width = max_text_width + combobox_extra + other_elements + margins
        # Clamp to min/max
        total_width = max(DIALOG_MIN_WIDTH, min(DIALOG_MAX_WIDTH, total_width))

        self.resize(total_width, DIALOG_HEIGHT)

    def _update_button_states(self):
        """Update button states."""
        has_config = self.combo_configs.count() > 0
        self.btn_edit.setEnabled(has_config)
        self.btn_delete.setEnabled(has_config)
        self.btn_export.setEnabled(has_config)
        self.btn_apply.setEnabled(has_config)

    def _on_config_changed(self, index):
        """Config selection changed callback."""
        self._update_button_states()

    def _on_add_clicked(self):
        """Add button clicked callback."""
        from .edit_dialog import EditDialog

        dialog = EditDialog(self.style_manager, parent=self)
        if dialog.exec_():
            self._load_configs()
            # Select the newly added config
            new_name = dialog.get_name()
            index = self.combo_configs.findText(new_name)
            if index >= 0:
                self.combo_configs.setCurrentIndex(index)

    def _on_edit_clicked(self):
        """Edit button clicked callback."""
        from .edit_dialog import EditDialog

        current_name = self.combo_configs.currentText()
        if not current_name:
            return

        config = self.style_manager.load_config(current_name)
        if not config:
            QMessageBox.warning(self, tr('error_title'), tr('load_config_error', name=current_name))
            return

        dialog = EditDialog(self.style_manager, config=config, parent=self)
        if dialog.exec_():
            self._load_configs()
            # Select the edited config
            new_name = dialog.get_name()
            index = self.combo_configs.findText(new_name)
            if index >= 0:
                self.combo_configs.setCurrentIndex(index)

    def _on_delete_clicked(self):
        """Delete button clicked callback."""
        current_name = self.combo_configs.currentText()
        if not current_name:
            return

        reply = QMessageBox.question(
            self,
            tr('confirm_delete_title'),
            tr('confirm_delete_msg', name=current_name),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            success, error = self.style_manager.delete_config(current_name)
            if success:
                self._load_configs()
            else:
                QMessageBox.warning(self, tr('delete_failed_title'), error)

    def _on_export_clicked(self):
        """Export button clicked callback."""
        current_name = self.combo_configs.currentText()
        if not current_name:
            QMessageBox.warning(self, tr('hint_title'), tr('no_config_selected'))
            return

        # Open file save dialog
        default_filename = f"{current_name}.json"
        file_path, __ = QFileDialog.getSaveFileName(
            self,
            tr('export_config_title'),
            default_filename,
            tr('json_file_filter'),
            options=QFileDialog.DontUseNativeDialog,
        )

        if not file_path:
            return

        # Export config
        success, error = self.style_manager.export_config(current_name, file_path)
        if success:
            QMessageBox.information(
                self,
                tr('export_config_title'),
                tr('export_success', path=file_path),
            )
        else:
            QMessageBox.warning(
                self,
                tr('error_title'),
                tr('export_failed', error=error),
            )

    def _on_import_clicked(self):
        """Import button clicked callback."""
        # Open file dialog
        file_path, __ = QFileDialog.getOpenFileName(
            self,
            tr('import_config_title'),
            "",
            tr('json_file_filter'),
            options=QFileDialog.DontUseNativeDialog,
        )

        if not file_path:
            return

        # Try to import config
        success, error, config_name = self.style_manager.import_config(file_path, overwrite=False)

        if not success:
            if error == "EXISTS":
                # Config already exists, ask for confirmation
                reply = QMessageBox.question(
                    self,
                    tr('confirm_overwrite_title'),
                    tr('import_config_exists', name=config_name),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if reply == QMessageBox.Yes:
                    success, error, config_name = self.style_manager.import_config(
                        file_path,
                        overwrite=True,
                    )
                else:
                    return

        if success:
            self._load_configs()
            # Select the imported config
            index = self.combo_configs.findText(config_name)
            if index >= 0:
                self.combo_configs.setCurrentIndex(index)
            QMessageBox.information(
                self,
                tr('import_config_title'),
                tr('import_success', name=config_name),
            )
        else:
            QMessageBox.warning(
                self,
                tr('error_title'),
                tr('import_failed', error=error),
            )

    def _on_apply_clicked(self):
        """Apply button clicked callback."""
        current_name = self.combo_configs.currentText()
        if not current_name:
            return

        config = self.style_manager.load_config(current_name)
        if not config:
            QMessageBox.warning(self, tr('error_title'), tr('load_config_error', name=current_name))
            return

        rules = config.get('rules', [])
        if not rules:
            QMessageBox.information(self, tr('hint_title'), tr('no_rules_hint'))
            return

        # Apply styles
        result = self.layer_processor.apply_styles(rules)

        # Display result
        success_count = result.get('success', 0)
        failed_count = result.get('failed', 0)
        unmatched_count = result.get('unmatched', 0)
        details = result.get('details', [])

        message = f"{tr('apply_result_complete')}\n\n"
        message += f"{tr('apply_result_success', count=success_count)}\n"
        message += f"{tr('apply_result_failed', count=failed_count)}\n"
        message += f"{tr('apply_result_unmatched', count=unmatched_count)}"

        if details:
            message += f"\n\n{tr('apply_result_details')}\n" + "\n".join(details)

        self._show_result_dialog(tr('apply_result_title'), message)

    def _on_help_clicked(self, link=None):
        """Help link clicked callback."""
        self._show_help_dialog(tr('help_title'), tr('help_content'))

    def _show_help_dialog(self, title: str, content: str):
        """
        Show help dialog.

        :param title: Dialog title
        :param content: HTML format content
        """
        from qgis.PyQt.QtWidgets import QTextBrowser

        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(520, 480)
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        text_browser = QTextBrowser()
        text_browser.setHtml(content)
        text_browser.setOpenExternalLinks(True)
        text_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        layout.addWidget(text_browser)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_ok = QPushButton(tr('ok_button'))
        btn_ok.setMinimumWidth(BUTTON_MIN_WIDTH)
        btn_ok.setFixedHeight(BUTTON_HEIGHT)
        btn_ok.setStyleSheet(BUTTON_STYLE_PRIMARY)
        btn_ok.clicked.connect(dialog.accept)
        btn_layout.addWidget(btn_ok)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        dialog.exec_()

    def _show_result_dialog(self, title: str, message: str):
        """
        Show result dialog.

        :param title: Dialog title
        :param message: Display content
        """
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(450, 350)
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        text_edit = QTextEdit()
        text_edit.setPlainText(message)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_ok = QPushButton(tr('ok_button'))
        btn_ok.setMinimumWidth(BUTTON_MIN_WIDTH)
        btn_ok.setFixedHeight(BUTTON_HEIGHT)
        btn_ok.setStyleSheet(BUTTON_STYLE_PRIMARY)
        btn_ok.clicked.connect(dialog.accept)
        btn_layout.addWidget(btn_ok)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        dialog.exec_()
