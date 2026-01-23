# -*- coding: utf-8 -*-
"""
Style Config Edit Dialog

Provides dialog interface for adding and editing style configs.
"""

from typing import Dict, List, Optional

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFontMetrics
from qgis.PyQt.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QStyledItemDelegate,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..core.i18n import tr

# Button size constants (consistent with main panel)
BUTTON_MIN_WIDTH = 70
BUTTON_HEIGHT = 28
LABEL_WIDTH = 60

# Button styles (consistent with main panel)
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

# Dialog size constraints
MIN_DIALOG_WIDTH = 600
MAX_DIALOG_WIDTH = 1200
MIN_DIALOG_HEIGHT = 400

# Table style
TABLE_STYLE = """
    QTableWidget {
        border: 1px solid #C0C0C0;
        gridline-color: #E0E0E0;
        background-color: white;
    }
    QTableWidget::item {
        padding: 2px 4px;
    }
    QHeaderView::section {
        background-color: #F5F5F5;
        border: none;
        border-bottom: 1px solid #C0C0C0;
        border-right: 1px solid #E0E0E0;
        padding: 4px 8px;
        font-weight: bold;
    }
"""

# Small button style
SMALL_BUTTON_STYLE = """
    QPushButton {
        background-color: #F0F0F0;
        border: 1px solid #C0C0C0;
        border-radius: 3px;
        padding: 2px 8px;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #E5E5E5;
        border: 1px solid #A0A0A0;
    }
    QPushButton:pressed {
        background-color: #D0D0D0;
    }
"""

# Toggle button style
TOGGLE_BUTTON_STYLE = """
    QPushButton {
        background-color: #E8F4FF;
        border: 1px solid #4DA6FF;
        border-radius: 3px;
        padding: 2px 8px;
        font-size: 12px;
        color: #0066CC;
    }
    QPushButton:hover {
        background-color: #D0EBFF;
        border: 1px solid #3399FF;
    }
    QPushButton:pressed {
        background-color: #B8E0FF;
    }
"""

# Edit mode constants
EDIT_MODE_TABLE = 0
EDIT_MODE_TEXT = 1

# Browse button style
BROWSE_BUTTON_STYLE = """
    QPushButton {
        background-color: #F0F0F0;
        border: 1px solid #C0C0C0;
        border-radius: 2px;
        padding: 0px 4px;
        min-width: 24px;
        max-width: 24px;
    }
    QPushButton:hover {
        background-color: #E5E5E5;
        border: 1px solid #A0A0A0;
    }
    QPushButton:pressed {
        background-color: #D0D0D0;
    }
"""


class StyleFileDelegate(QStyledItemDelegate):
    """Custom delegate for style file path column with file browser button."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """Create editor widget."""
        # Create container
        container = QWidget(parent)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Text input
        line_edit = QLineEdit(container)
        line_edit.setFrame(False)
        layout.addWidget(line_edit)

        # Browse button
        browse_btn = QPushButton("...", container)
        browse_btn.setStyleSheet(BROWSE_BUTTON_STYLE)
        browse_btn.setFixedSize(24, 20)
        browse_btn.clicked.connect(lambda: self._on_browse_clicked(line_edit, container))
        layout.addWidget(browse_btn)

        # Save references for later access
        container.line_edit = line_edit
        container.browse_btn = browse_btn

        return container

    def _on_browse_clicked(self, line_edit: QLineEdit, container: QWidget):
        """Browse button click event."""
        current_path = line_edit.text()

        file_path, __ = QFileDialog.getOpenFileName(
            container,
            tr('select_style_file_title'),
            current_path,
            tr('style_file_filter'),
        )

        if file_path:
            line_edit.setText(file_path)

    def setEditorData(self, editor, index):
        """Set editor data."""
        value = index.model().data(index, Qt.EditRole)
        if value is None:
            value = ''
        editor.line_edit.setText(str(value))

    def setModelData(self, editor, model, index):
        """Save editor data to model."""
        value = editor.line_edit.text()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        """Update editor geometry."""
        editor.setGeometry(option.rect)


class EditDialog(QDialog):
    """Style config edit dialog."""

    def __init__(self, style_manager, config: Optional[Dict] = None, parent=None):
        """
        Initialize the edit dialog.

        :param style_manager: StyleManager instance
        :param config: Existing config data (edit mode), None for add mode
        :param parent: Parent widget
        """
        super().__init__(parent)
        self.style_manager = style_manager
        self.config = config
        self.is_edit_mode = config is not None
        self.old_name = config.get('name', '') if config else ''

        self._setup_ui()
        self._load_config()
        self._adjust_dialog_width()

        # Current edit mode
        self.current_edit_mode = EDIT_MODE_TABLE

    def _setup_ui(self):
        """Setup UI layout."""
        title = tr('edit_dialog_title_edit') if self.is_edit_mode else tr('edit_dialog_title_add')
        self.setWindowTitle(title)
        self.setMinimumSize(MIN_DIALOG_WIDTH, MIN_DIALOG_HEIGHT)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Basic info group
        info_group = QGroupBox(tr('basic_info_group'))
        info_layout = QHBoxLayout(info_group)
        info_layout.setContentsMargins(10, 12, 10, 8)
        info_layout.setSpacing(8)

        name_label = QLabel(tr('name_label'))
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        info_layout.addWidget(name_label)

        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText(tr('name_placeholder'))
        self.edit_name.setMinimumHeight(BUTTON_HEIGHT)
        info_layout.addWidget(self.edit_name)

        layout.addWidget(info_group)

        # Style rules group
        rules_group = QGroupBox(tr('rules_group'))
        rules_layout = QVBoxLayout(rules_group)
        rules_layout.setContentsMargins(10, 12, 10, 8)
        rules_layout.setSpacing(6)

        # Toolbar (add/delete buttons + mode toggle)
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(6)

        self.btn_add_row = QPushButton(tr('add_row_button'))
        self.btn_add_row.setStyleSheet(SMALL_BUTTON_STYLE)
        self.btn_add_row.clicked.connect(self._on_add_row)
        toolbar_layout.addWidget(self.btn_add_row)

        self.btn_remove_row = QPushButton(tr('remove_row_button'))
        self.btn_remove_row.setStyleSheet(SMALL_BUTTON_STYLE)
        self.btn_remove_row.clicked.connect(self._on_remove_row)
        toolbar_layout.addWidget(self.btn_remove_row)

        self.btn_move_up = QPushButton(tr('move_up_button'))
        self.btn_move_up.setStyleSheet(SMALL_BUTTON_STYLE)
        self.btn_move_up.clicked.connect(self._on_move_up)
        toolbar_layout.addWidget(self.btn_move_up)

        self.btn_move_down = QPushButton(tr('move_down_button'))
        self.btn_move_down.setStyleSheet(SMALL_BUTTON_STYLE)
        self.btn_move_down.clicked.connect(self._on_move_down)
        toolbar_layout.addWidget(self.btn_move_down)

        self.btn_move_top = QPushButton(tr('move_top_button'))
        self.btn_move_top.setStyleSheet(SMALL_BUTTON_STYLE)
        self.btn_move_top.clicked.connect(self._on_move_top)
        toolbar_layout.addWidget(self.btn_move_top)

        self.btn_move_bottom = QPushButton(tr('move_bottom_button'))
        self.btn_move_bottom.setStyleSheet(SMALL_BUTTON_STYLE)
        self.btn_move_bottom.clicked.connect(self._on_move_bottom)
        toolbar_layout.addWidget(self.btn_move_bottom)

        # Format hint label (shown in text mode, left aligned)
        self.format_hint_label = QLabel(tr('format_hint'))
        self.format_hint_label.setStyleSheet("color: #666666; font-size: 12px;")
        self.format_hint_label.setVisible(False)
        toolbar_layout.addWidget(self.format_hint_label)

        toolbar_layout.addStretch()

        # Mode toggle button
        self.btn_toggle_mode = QPushButton(tr('toggle_text_mode'))
        self.btn_toggle_mode.setStyleSheet(TOGGLE_BUTTON_STYLE)
        self.btn_toggle_mode.clicked.connect(self._on_toggle_mode)
        toolbar_layout.addWidget(self.btn_toggle_mode)

        rules_layout.addLayout(toolbar_layout)

        # Use QStackedWidget to switch between table and text edit
        self.edit_stack = QStackedWidget()
        self.edit_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Rules table (index 0)
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(2)
        self.rules_table.setHorizontalHeaderLabels([
            tr('table_header_pattern'),
            tr('table_header_style_file'),
        ])
        self.rules_table.setStyleSheet(TABLE_STYLE)
        self.rules_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.rules_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.rules_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rules_table.setAlternatingRowColors(True)

        # Set header stretch mode (last column stretches to fill remaining space)
        header = self.rules_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # Set compact row height
        self.rules_table.verticalHeader().setDefaultSectionSize(26)
        self.rules_table.verticalHeader().setVisible(False)

        # Set custom delegate for style file path column (with file browser button)
        self.style_file_delegate = StyleFileDelegate(self.rules_table)
        self.rules_table.setItemDelegateForColumn(1, self.style_file_delegate)

        self.edit_stack.addWidget(self.rules_table)

        # Text edit area (index 1)
        self.edit_content = QPlainTextEdit()
        self.edit_content.setPlaceholderText(tr('text_placeholder'))
        self.edit_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.edit_stack.addWidget(self.edit_content)

        rules_layout.addWidget(self.edit_stack)

        layout.addWidget(rules_group, 1)

        # Button area
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setContentsMargins(0, 4, 0, 0)
        btn_layout.addStretch()

        self.btn_save = QPushButton(tr('save_button'))
        self.btn_save.setMinimumWidth(BUTTON_MIN_WIDTH)
        self.btn_save.setFixedHeight(BUTTON_HEIGHT)
        self.btn_save.setStyleSheet(BUTTON_STYLE_PRIMARY)
        self.btn_save.clicked.connect(self._on_save_clicked)
        btn_layout.addWidget(self.btn_save)

        self.btn_cancel = QPushButton(tr('cancel_button'))
        self.btn_cancel.setMinimumWidth(BUTTON_MIN_WIDTH)
        self.btn_cancel.setFixedHeight(BUTTON_HEIGHT)
        self.btn_cancel.setStyleSheet(BUTTON_STYLE_NORMAL)
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _load_config(self):
        """Load config data to form."""
        if self.config:
            self.edit_name.setText(self.config.get('name', ''))
            rules = self.config.get('rules', [])
            self._load_rules_to_table(rules)
        else:
            # Add mode, add an empty row
            self._add_empty_row()

    def _load_rules_to_table(self, rules: List[Dict]):
        """
        Load rules list to table.

        :param rules: Rules list
        """
        self.rules_table.setRowCount(0)
        for rule in rules:
            row = self.rules_table.rowCount()
            self.rules_table.insertRow(row)

            pattern_item = QTableWidgetItem(rule.get('pattern', ''))
            style_item = QTableWidgetItem(rule.get('style_file', ''))

            self.rules_table.setItem(row, 0, pattern_item)
            self.rules_table.setItem(row, 1, style_item)

        # If no rules, add an empty row
        if not rules:
            self._add_empty_row()

    def _adjust_dialog_width(self):
        """Adjust dialog width and column width based on table content."""
        font_metrics = QFontMetrics(self.rules_table.font())

        # Calculate max width for each column (including header)
        max_pattern_width = font_metrics.horizontalAdvance(tr('table_header_pattern')) + 24
        max_style_width = font_metrics.horizontalAdvance(tr('table_header_style_file')) + 24

        for row in range(self.rules_table.rowCount()):
            pattern_item = self.rules_table.item(row, 0)
            style_item = self.rules_table.item(row, 1)

            if pattern_item and pattern_item.text():
                width = font_metrics.horizontalAdvance(pattern_item.text()) + 24
                max_pattern_width = max(max_pattern_width, width)

            if style_item and style_item.text():
                width = font_metrics.horizontalAdvance(style_item.text()) + 24
                max_style_width = max(max_style_width, width)

        # Set first column width (fit content)
        self.rules_table.setColumnWidth(0, max_pattern_width)

        # Calculate total width: two columns + margins + scrollbar reserve
        # Layout margins(24) + GroupBox margins(20) + table border(4) + scrollbar(20) + extra space(32)
        padding = 24 + 20 + 4 + 20 + 32
        target_width = max_pattern_width + max_style_width + padding

        # Limit between min and max width
        target_width = max(MIN_DIALOG_WIDTH, min(target_width, MAX_DIALOG_WIDTH))

        # Resize dialog
        self.resize(target_width, self.height())

    def _add_empty_row(self):
        """Add an empty row."""
        row = self.rules_table.rowCount()
        self.rules_table.insertRow(row)
        self.rules_table.setItem(row, 0, QTableWidgetItem(''))
        self.rules_table.setItem(row, 1, QTableWidgetItem(''))

    def _on_add_row(self):
        """Add row button clicked callback."""
        self._add_empty_row()
        # Select the newly added row
        new_row = self.rules_table.rowCount() - 1
        self.rules_table.selectRow(new_row)
        self.rules_table.setCurrentCell(new_row, 0)
        self.rules_table.editItem(self.rules_table.item(new_row, 0))

    def _on_remove_row(self):
        """Remove selected rows button clicked callback."""
        selected_rows = set()
        for item in self.rules_table.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            return

        # Delete from end to avoid index shifting
        for row in sorted(selected_rows, reverse=True):
            self.rules_table.removeRow(row)

        # Ensure at least one row remains
        if self.rules_table.rowCount() == 0:
            self._add_empty_row()

    def _on_move_up(self):
        """Move selected row up."""
        current_row = self.rules_table.currentRow()
        if current_row <= 0:
            return

        self._swap_rows(current_row, current_row - 1)
        self.rules_table.selectRow(current_row - 1)

    def _on_move_down(self):
        """Move selected row down."""
        current_row = self.rules_table.currentRow()
        if current_row < 0 or current_row >= self.rules_table.rowCount() - 1:
            return

        self._swap_rows(current_row, current_row + 1)
        self.rules_table.selectRow(current_row + 1)

    def _on_move_top(self):
        """Move selected row to top."""
        current_row = self.rules_table.currentRow()
        if current_row <= 0:
            return

        row_data = self._get_row_data(current_row)
        self.rules_table.removeRow(current_row)
        self.rules_table.insertRow(0)
        self._set_row_data(0, row_data)
        self.rules_table.selectRow(0)

    def _on_move_bottom(self):
        """Move selected row to bottom."""
        current_row = self.rules_table.currentRow()
        last_row = self.rules_table.rowCount() - 1
        if current_row < 0 or current_row >= last_row:
            return

        row_data = self._get_row_data(current_row)
        self.rules_table.removeRow(current_row)
        new_last_row = self.rules_table.rowCount()
        self.rules_table.insertRow(new_last_row)
        self._set_row_data(new_last_row, row_data)
        self.rules_table.selectRow(new_last_row)

    def _get_row_data(self, row: int) -> List[str]:
        """
        Get data from specified row.

        :param row: Row index
        :return: Row data list
        """
        data = []
        for col in range(self.rules_table.columnCount()):
            item = self.rules_table.item(row, col)
            data.append(item.text() if item else '')
        return data

    def _set_row_data(self, row: int, data: List[str]):
        """
        Set data for specified row.

        :param row: Row index
        :param data: Row data list
        """
        for col, text in enumerate(data):
            self.rules_table.setItem(row, col, QTableWidgetItem(text))

    def _swap_rows(self, row1: int, row2: int):
        """
        Swap two rows' data.

        :param row1: First row index
        :param row2: Second row index
        """
        for col in range(self.rules_table.columnCount()):
            item1 = self.rules_table.item(row1, col)
            item2 = self.rules_table.item(row2, col)

            text1 = item1.text() if item1 else ''
            text2 = item2.text() if item2 else ''

            self.rules_table.setItem(row1, col, QTableWidgetItem(text2))
            self.rules_table.setItem(row2, col, QTableWidgetItem(text1))

    def _on_toggle_mode(self):
        """Toggle edit mode."""
        if self.current_edit_mode == EDIT_MODE_TABLE:
            # Switch from table mode to text mode
            rules = self._get_rules_from_table()
            content = self._rules_to_content(rules)
            self.edit_content.setPlainText(content)

            self.edit_stack.setCurrentIndex(EDIT_MODE_TEXT)
            self.current_edit_mode = EDIT_MODE_TEXT
            self.btn_toggle_mode.setText(tr('toggle_table_mode'))

            # Hide table-related buttons
            self.btn_add_row.setVisible(False)
            self.btn_remove_row.setVisible(False)
            self.btn_move_up.setVisible(False)
            self.btn_move_down.setVisible(False)
            self.btn_move_top.setVisible(False)
            self.btn_move_bottom.setVisible(False)
            # Show format hint
            self.format_hint_label.setVisible(True)
        else:
            # Switch from text mode to table mode
            content = self.edit_content.toPlainText()
            rules = self._parse_content_to_rules(content)

            if rules is None:
                # Parse failed, stay in text mode
                return

            self._load_rules_to_table(rules)

            self.edit_stack.setCurrentIndex(EDIT_MODE_TABLE)
            self.current_edit_mode = EDIT_MODE_TABLE
            self.btn_toggle_mode.setText(tr('toggle_text_mode'))

            # Show table-related buttons
            self.btn_add_row.setVisible(True)
            self.btn_remove_row.setVisible(True)
            self.btn_move_up.setVisible(True)
            self.btn_move_down.setVisible(True)
            self.btn_move_top.setVisible(True)
            self.btn_move_bottom.setVisible(True)
            # Hide format hint
            self.format_hint_label.setVisible(False)

    def _parse_content_to_rules(self, content: str) -> Optional[List[Dict]]:
        """
        Parse text content to rules list.

        :param content: Text content
        :return: Rules list, or None if parse failed
        """
        import re

        rules = []
        if not content or not content.strip():
            return rules

        # Match format: "pattern": "style_file"
        pattern = re.compile(r'^"(.+)"\s*:\s*"(.+)"$')

        for line_num, line in enumerate(content.strip().split('\n'), 1):
            line = line.strip()
            if not line:
                continue

            match = pattern.match(line)
            if not match:
                QMessageBox.warning(
                    self,
                    tr('format_error_title'),
                    tr('format_error_msg', line=line_num, content=line),
                )
                return None

            rules.append({
                'pattern': match.group(1),
                'style_file': match.group(2),
            })

        return rules

    def _get_rules_from_table(self) -> List[Dict]:
        """
        Get rules list from table.

        :return: Rules list
        """
        rules = []
        for row in range(self.rules_table.rowCount()):
            pattern_item = self.rules_table.item(row, 0)
            style_item = self.rules_table.item(row, 1)

            pattern = pattern_item.text().strip() if pattern_item else ''
            style_file = style_item.text().strip() if style_item else ''

            # Skip empty rows
            if not pattern and not style_file:
                continue

            rules.append({
                'pattern': pattern,
                'style_file': style_file,
            })
        return rules

    def _rules_to_content(self, rules: List[Dict]) -> str:
        """
        Convert rules list to text format.

        :param rules: Rules list
        :return: Text format content
        """
        lines = []
        for rule in rules:
            pattern = rule.get('pattern', '')
            style_file = rule.get('style_file', '')
            lines.append(f'"{pattern}": "{style_file}"')
        return '\n'.join(lines)

    def _on_save_clicked(self):
        """Save button clicked callback."""
        import re

        name = self.edit_name.text().strip()

        # Get rules based on current mode
        if self.current_edit_mode == EDIT_MODE_TABLE:
            rules = self._get_rules_from_table()
        else:
            content = self.edit_content.toPlainText()
            rules = self._parse_content_to_rules(content)
            if rules is None:
                return

        if not name:
            QMessageBox.warning(self, tr('error_title'), tr('name_required_error'))
            self.edit_name.setFocus()
            return

        # Check for duplicate name (add mode or rename)
        if not self.is_edit_mode or name != self.old_name:
            existing_configs = self.style_manager.list_configs()
            if name in existing_configs:
                QMessageBox.warning(self, tr('error_title'), tr('name_exists_error', name=name))
                self.edit_name.setFocus()
                return

        # Validate rules
        for i, rule in enumerate(rules):
            pattern = rule.get('pattern', '')
            style_file = rule.get('style_file', '')

            if pattern and not style_file:
                QMessageBox.warning(self, tr('error_title'), tr('style_file_required_error', row=i + 1))
                if self.current_edit_mode == EDIT_MODE_TABLE:
                    self.rules_table.selectRow(i)
                return

            if style_file and not pattern:
                QMessageBox.warning(self, tr('error_title'), tr('pattern_required_error', row=i + 1))
                if self.current_edit_mode == EDIT_MODE_TABLE:
                    self.rules_table.selectRow(i)
                return

            # Validate regex syntax
            if pattern:
                try:
                    re.compile(pattern)
                except re.error as e:
                    QMessageBox.warning(
                        self,
                        tr('error_title'),
                        tr('regex_syntax_error', row=i + 1, error=str(e)),
                    )
                    if self.current_edit_mode == EDIT_MODE_TABLE:
                        self.rules_table.selectRow(i)
                    return

        # Convert to text format for compatibility with existing save logic
        content = self._rules_to_content(rules)

        # Save config
        old_name = self.old_name if self.is_edit_mode else None
        success, error = self.style_manager.save_config(name, content, old_name)

        if success:
            self.accept()
        else:
            QMessageBox.warning(self, tr('save_failed_title'), error)

    def get_name(self) -> str:
        """
        Get config name.

        :return: Name string
        """
        return self.edit_name.text().strip()
