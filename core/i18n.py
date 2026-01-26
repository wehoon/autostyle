# -*- coding: utf-8 -*-
"""
Internationalization Module

Automatically selects Chinese or English interface based on QGIS language settings.
Simplified Chinese and Traditional Chinese use Chinese, other languages use English.
"""

from qgis.core import QgsSettings


def get_current_language() -> str:
    """
    Get current language code.

    :return: 'zh' for Chinese, 'en' for English
    """
    settings = QgsSettings()
    locale = settings.value('locale/userLocale', '')

    if not locale:
        # Try to get from system locale
        from qgis.PyQt.QtCore import QLocale
        locale = QLocale.system().name()

    # Simplified Chinese and Traditional Chinese use Chinese
    if locale.startswith('zh'):
        return 'zh'

    return 'en'


# Translation dictionary
_TRANSLATIONS = {
    # ===== Main Panel (panel_widget.py) =====
    'select_config': {
        'zh': '选择配置表:',
        'en': 'Select Config:',
    },
    'add_config_tooltip': {
        'zh': '新增配置表',
        'en': 'Add Config',
    },
    'edit_config_tooltip': {
        'zh': '编辑配置表',
        'en': 'Edit Config',
    },
    'delete_config_tooltip': {
        'zh': '删除配置表',
        'en': 'Delete Config',
    },
    'help_link': {
        'zh': '使用说明',
        'en': 'Help',
    },
    'apply_button': {
        'zh': '一键应用',
        'en': 'Apply',
    },
    'close_button': {
        'zh': '关闭',
        'en': 'Close',
    },
    'confirm_delete_title': {
        'zh': '确认删除',
        'en': 'Confirm Delete',
    },
    'confirm_delete_msg': {
        'zh': '确定要删除样式表 "{name}" 吗？',
        'en': 'Are you sure you want to delete config "{name}"?',
    },
    'delete_failed_title': {
        'zh': '删除失败',
        'en': 'Delete Failed',
    },
    'error_title': {
        'zh': '错误',
        'en': 'Error',
    },
    'load_config_error': {
        'zh': '无法加载配置表: {name}',
        'en': 'Failed to load config: {name}',
    },
    'hint_title': {
        'zh': '提示',
        'en': 'Info',
    },
    'no_rules_hint': {
        'zh': '配置表中没有样式规则',
        'en': 'No style rules in the config',
    },
    'apply_result_title': {
        'zh': '应用结果',
        'en': 'Apply Result',
    },
    'apply_result_complete': {
        'zh': '样式应用完成:',
        'en': 'Style application completed:',
    },
    'apply_result_success': {
        'zh': '成功: {count} 个图层',
        'en': 'Success: {count} layer(s)',
    },
    'apply_result_failed': {
        'zh': '失败: {count} 个图层',
        'en': 'Failed: {count} layer(s)',
    },
    'apply_result_unmatched': {
        'zh': '未匹配: {count} 个图层',
        'en': 'Unmatched: {count} layer(s)',
    },
    'apply_result_details': {
        'zh': '详情:',
        'en': 'Details:',
    },
    'ok_button': {
        'zh': '确定',
        'en': 'OK',
    },
    'help_title': {
        'zh': '使用说明',
        'en': 'Help',
    },

    # ===== Edit Dialog (edit_dialog.py) =====
    'edit_dialog_title_edit': {
        'zh': '编辑样式表',
        'en': 'Edit Style Config',
    },
    'edit_dialog_title_add': {
        'zh': '新增样式表',
        'en': 'Add Style Config',
    },
    'basic_info_group': {
        'zh': '基本信息',
        'en': 'Basic Info',
    },
    'name_label': {
        'zh': '名称:',
        'en': 'Name:',
    },
    'name_placeholder': {
        'zh': '请输入配置表名称',
        'en': 'Enter config name',
    },
    'rules_group': {
        'zh': '样式规则',
        'en': 'Style Rules',
    },
    'add_row_button': {
        'zh': '+ 添加',
        'en': '+ Add',
    },
    'remove_row_button': {
        'zh': '- 删除',
        'en': '- Remove',
    },
    'move_up_button': {
        'zh': '↑ 上移',
        'en': '↑ Up',
    },
    'move_down_button': {
        'zh': '↓ 下移',
        'en': '↓ Down',
    },
    'move_top_button': {
        'zh': '⤒ 置顶',
        'en': '⤒ Top',
    },
    'move_bottom_button': {
        'zh': '⤓ 置底',
        'en': '⤓ Bottom',
    },
    'toggle_text_mode': {
        'zh': '切换文本模式',
        'en': 'Text Mode',
    },
    'toggle_table_mode': {
        'zh': '切换表格模式',
        'en': 'Table Mode',
    },
    'format_hint': {
        'zh': '格式: "正则表达式": "样式文件路径"，每行一条规则',
        'en': 'Format: "pattern": "style_file_path", one rule per line',
    },
    'table_header_pattern': {
        'zh': '正则表达式',
        'en': 'Pattern',
    },
    'table_header_style_file': {
        'zh': '样式文件路径',
        'en': 'Style File Path',
    },
    'text_placeholder': {
        'zh': '示例:\n"^road_.*": "/path/to/road_style.qml"\n"^building_.*": "/path/to/building_style.qml"',
        'en': 'Example:\n"^road_.*": "/path/to/road_style.qml"\n"^building_.*": "/path/to/building_style.qml"',
    },
    'save_button': {
        'zh': '保存',
        'en': 'Save',
    },
    'cancel_button': {
        'zh': '取消',
        'en': 'Cancel',
    },
    'format_error_title': {
        'zh': '格式错误',
        'en': 'Format Error',
    },
    'format_error_msg': {
        'zh': '第 {line} 行格式错误: {content}\n期望格式: "<正则表达式>": "<样式文件路径>"',
        'en': 'Format error at line {line}: {content}\nExpected format: "<pattern>": "<style_file_path>"',
    },
    'name_required_error': {
        'zh': '请输入配置表名称',
        'en': 'Please enter config name',
    },
    'name_exists_error': {
        'zh': '配置表 "{name}" 已存在',
        'en': 'Config "{name}" already exists',
    },
    'style_file_required_error': {
        'zh': '第 {row} 行：请填写样式文件路径',
        'en': 'Row {row}: Please enter style file path',
    },
    'pattern_required_error': {
        'zh': '第 {row} 行：请填写正则表达式',
        'en': 'Row {row}: Please enter pattern',
    },
    'regex_syntax_error': {
        'zh': '第 {row} 行正则表达式语法错误: {error}',
        'en': 'Row {row} regex syntax error: {error}',
    },
    'save_failed_title': {
        'zh': '保存失败',
        'en': 'Save Failed',
    },
    'select_style_file_title': {
        'zh': '选择样式文件',
        'en': 'Select Style File',
    },
    'style_file_filter': {
        'zh': 'QGIS样式文件 (*.qml);;所有文件 (*.*)',
        'en': 'QGIS Style Files (*.qml);;All Files (*.*)',
    },

    # ===== Layer Processor (layer_processor.py) =====
    'no_layers': {
        'zh': '当前项目没有图层',
        'en': 'No layers in current project',
    },
    'no_valid_rules': {
        'zh': '没有有效的样式规则',
        'en': 'No valid style rules',
    },
    'regex_compile_failed': {
        'zh': '正则表达式编译失败: {pattern} - {error}',
        'en': 'Regex compile failed: {pattern} - {error}',
    },
    'style_file_not_exist': {
        'zh': '图层 [{layer}]: 样式文件不存在 - {file}',
        'en': 'Layer [{layer}]: Style file not found - {file}',
    },
    'style_apply_success': {
        'zh': '图层 [{layer}]: 样式应用成功 - {pattern}',
        'en': 'Layer [{layer}]: Style applied - {pattern}',
    },
    'style_apply_failed': {
        'zh': '图层 [{layer}]: 样式应用失败 - {file}',
        'en': 'Layer [{layer}]: Style apply failed - {file}',
    },
    'layer_unmatched': {
        'zh': '图层 [{layer}]: 未匹配任何规则',
        'en': 'Layer [{layer}]: No matching rule',
    },
    'load_style_failed': {
        'zh': '加载样式失败: {message}',
        'en': 'Load style failed: {message}',
    },
    'apply_style_exception': {
        'zh': '应用样式时发生异常: {error}',
        'en': 'Exception while applying style: {error}',
    },

    # ===== Export/Import =====
    'export_config_tooltip': {
        'zh': '导出配置表',
        'en': 'Export Config',
    },
    'import_config_tooltip': {
        'zh': '导入配置表',
        'en': 'Import Config',
    },
    'export_config_title': {
        'zh': '导出配置表',
        'en': 'Export Config',
    },
    'import_config_title': {
        'zh': '导入配置表',
        'en': 'Import Config',
    },
    'export_success': {
        'zh': '配置表已成功导出到:\n{path}',
        'en': 'Config exported successfully to:\n{path}',
    },
    'export_failed': {
        'zh': '导出失败: {error}',
        'en': 'Export failed: {error}',
    },
    'import_success': {
        'zh': '配置表 "{name}" 导入成功',
        'en': 'Config "{name}" imported successfully',
    },
    'import_failed': {
        'zh': '导入失败: {error}',
        'en': 'Import failed: {error}',
    },
    'json_file_filter': {
        'zh': 'JSON文件 (*.json);;所有文件 (*.*)',
        'en': 'JSON Files (*.json);;All Files (*.*)',
    },
    'no_config_selected': {
        'zh': '请先选择一个配置表',
        'en': 'Please select a config first',
    },
    'import_config_exists': {
        'zh': '配置表 "{name}" 已存在，是否覆盖？',
        'en': 'Config "{name}" already exists. Overwrite?',
    },
    'confirm_overwrite_title': {
        'zh': '确认覆盖',
        'en': 'Confirm Overwrite',
    },
    'invalid_config_format': {
        'zh': '无效的配置文件格式',
        'en': 'Invalid config file format',
    },

    # ===== Style Manager Error Messages =====
    'config_name_empty': {
        'zh': '配置表名称不能为空',
        'en': 'Config name cannot be empty',
    },
    'config_not_exist': {
        'zh': '配置表不存在',
        'en': 'Config does not exist',
    },
    'delete_old_config_failed': {
        'zh': '删除旧配置文件失败: {error}',
        'en': 'Failed to delete old config: {error}',
    },
    'save_config_failed': {
        'zh': '保存配置文件失败: {error}',
        'en': 'Failed to save config: {error}',
    },
    'delete_config_failed': {
        'zh': '删除配置文件失败: {error}',
        'en': 'Failed to delete config: {error}',
    },

    # ===== Update Checker =====
    'update_available_title': {
        'zh': '发现新版本',
        'en': 'Update Available',
    },
    'update_available_msg': {
        'zh': '发现 AutoStyle 新版本！\n\n当前版本: {current}\n最新版本: {latest}',
        'en': 'A new version of AutoStyle is available!\n\nCurrent: {current}\nLatest: {latest}',
    },
    'update_changelog_label': {
        'zh': '更新内容:',
        'en': 'Changelog:',
    },
    'update_download_button': {
        'zh': '下载更新',
        'en': 'Download',
    },
    'update_ignore_button': {
        'zh': '暂不更新',
        'en': 'Ignore',
    },
    'update_skip_version_button': {
        'zh': '跳过此版本',
        'en': 'Skip Version',
    },
    'update_check_failed': {
        'zh': '检查更新失败: {error}',
        'en': 'Update check failed: {error}',
    },
    'update_no_update': {
        'zh': '当前已是最新版本 ({version})',
        'en': 'You are using the latest version ({version})',
    },
    'update_checking': {
        'zh': '正在检查更新...',
        'en': 'Checking for updates...',
    },
    'check_update_menu': {
        'zh': '检查更新',
        'en': 'Check for Updates',
    },

    # ===== Help Content =====
    'help_content': {
        'zh': """
<h2>AutoStyle 使用说明</h2>

<h3>功能概述</h3>
<p>AutoStyle 是一款 QGIS 样式管理插件，支持通过正则表达式匹配图层名称，自动批量应用 QML 样式文件。适用于需要频繁对多个图层应用统一样式的场景，如地图制图、数据可视化等。</p>

<h3>主界面操作</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
<tr><th style="width: 120px;">按钮</th><th>功能说明</th></tr>
<tr><td><b>添加</b></td><td>创建新的样式配置表，打开编辑对话框</td></tr>
<tr><td><b>编辑</b></td><td>编辑当前选中的配置表，修改名称或样式规则</td></tr>
<tr><td><b>删除</b></td><td>删除当前选中的配置表，删除前会弹出确认对话框</td></tr>
<tr><td><b>一键应用</b></td><td>遍历当前项目的所有图层，根据配置表中的规则自动匹配并应用样式</td></tr>
</table>

<h3>配置表编辑</h3>
<p>编辑对话框支持两种编辑模式，可通过右上角按钮切换：</p>

<p><b>表格模式（默认）</b></p>
<ul>
<li><b>+ 添加</b>：在表格末尾添加新规则行</li>
<li><b>- 删除</b>：删除选中的规则行（支持多选）</li>
<li><b>↑ 上移 / ↓ 下移</b>：调整规则的优先级顺序</li>
<li><b>⤒ 置顶 / ⤓ 置底</b>：将选中规则移至最前或最后</li>
<li>样式文件路径列支持点击 <b>...</b> 按钮浏览选择 QML 文件</li>
</ul>

<p><b>文本模式</b></p>
<ul>
<li>以纯文本方式编辑规则，适合批量复制粘贴</li>
<li>格式：<code>"正则表达式": "样式文件路径"</code>，每行一条规则</li>
<li>切换回表格模式时会自动验证格式</li>
</ul>

<h3>样式规则说明</h3>
<p>每条规则包含两个部分：</p>
<ul>
<li><b>正则表达式</b>：用于匹配图层名称的模式（使用 Python re 模块语法）</li>
<li><b>样式文件路径</b>：匹配成功后应用的 QML 样式文件的绝对路径</li>
</ul>

<h3>正则表达式示例</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
<tr><th>模式</th><th>说明</th><th>匹配示例</th></tr>
<tr><td><code>^道路.*</code></td><td>匹配以"道路"开头的图层</td><td>道路_主干道、道路边界</td></tr>
<tr><td><code>.*水系$</code></td><td>匹配以"水系"结尾的图层</td><td>河流水系、湖泊水系</td></tr>
<tr><td><code>.*建筑.*</code></td><td>匹配包含"建筑"的图层</td><td>住宅建筑、建筑轮廓</td></tr>
<tr><td><code>^(植被|绿地).*</code></td><td>匹配以"植被"或"绿地"开头</td><td>植被覆盖、绿地公园</td></tr>
<tr><td><code>(?i)road</code></td><td>不区分大小写匹配包含"road"</td><td>Road_Main、road_01</td></tr>
<tr><td><code>layer_\\d+</code></td><td>匹配"layer_"后跟数字</td><td>layer_01、layer_123</td></tr>
</table>

<h3>应用结果说明</h3>
<p>点击"一键应用"后，插件会遍历当前项目的所有图层并显示结果：</p>
<ul>
<li><b>成功</b>：成功匹配规则并应用样式的图层数量</li>
<li><b>失败</b>：匹配到规则但样式应用失败的图层数量（如样式文件不存在）</li>
<li><b>未匹配</b>：未匹配到任何规则的图层数量</li>
</ul>
<p>详细的处理日志可在 QGIS 消息日志面板（标签：AutoStyle）中查看。</p>

<h3>注意事项</h3>
<ul>
<li>规则按顺序从上到下匹配，<b>先匹配到的规则优先应用</b>，后续规则不再处理该图层</li>
<li>正则表达式默认区分大小写，如需忽略大小写可使用 <code>(?i)</code> 前缀</li>
<li>样式文件路径建议使用绝对路径，确保文件存在且可访问</li>
<li>保存配置表时会自动验证正则表达式语法</li>
<li>配置表数据以 JSON 格式存储在插件目录的 styles 文件夹中</li>
</ul>
""",
        'en': """
<h2>AutoStyle User Guide</h2>

<h3>Overview</h3>
<p>AutoStyle is a QGIS style management plugin that supports batch applying QML style files to layers by matching layer names with regular expressions. It is suitable for scenarios where you need to frequently apply unified styles to multiple layers, such as cartography and data visualization.</p>

<h3>Main Interface</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
<tr><th style="width: 120px;">Button</th><th>Description</th></tr>
<tr><td><b>Add</b></td><td>Create a new style config, opens the edit dialog</td></tr>
<tr><td><b>Edit</b></td><td>Edit the selected config, modify name or style rules</td></tr>
<tr><td><b>Delete</b></td><td>Delete the selected config (confirmation required)</td></tr>
<tr><td><b>Apply</b></td><td>Traverse all layers in the current project and apply styles based on matching rules</td></tr>
</table>

<h3>Config Editor</h3>
<p>The edit dialog supports two editing modes, switchable via the button in the top right:</p>

<p><b>Table Mode (Default)</b></p>
<ul>
<li><b>+ Add</b>: Add a new rule row at the end of the table</li>
<li><b>- Remove</b>: Remove selected rule rows (multi-select supported)</li>
<li><b>↑ Up / ↓ Down</b>: Adjust the priority order of rules</li>
<li><b>⤒ Top / ⤓ Bottom</b>: Move selected rule to the first or last position</li>
<li>Click the <b>...</b> button in the style file path column to browse and select QML files</li>
</ul>

<p><b>Text Mode</b></p>
<ul>
<li>Edit rules as plain text, suitable for batch copy-paste</li>
<li>Format: <code>"pattern": "style_file_path"</code>, one rule per line</li>
<li>Format validation is performed when switching back to table mode</li>
</ul>

<h3>Style Rules</h3>
<p>Each rule contains two parts:</p>
<ul>
<li><b>Pattern</b>: Regular expression to match layer names (Python re module syntax)</li>
<li><b>Style File Path</b>: Absolute path to the QML style file to apply on match</li>
</ul>

<h3>Regex Examples</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
<tr><th>Pattern</th><th>Description</th><th>Match Examples</th></tr>
<tr><td><code>^road.*</code></td><td>Match layers starting with "road"</td><td>road_main, road_boundary</td></tr>
<tr><td><code>.*river$</code></td><td>Match layers ending with "river"</td><td>main_river, small_river</td></tr>
<tr><td><code>.*building.*</code></td><td>Match layers containing "building"</td><td>residential_building, building_outline</td></tr>
<tr><td><code>^(forest|park).*</code></td><td>Match layers starting with "forest" or "park"</td><td>forest_cover, park_area</td></tr>
<tr><td><code>(?i)road</code></td><td>Case-insensitive match for "road"</td><td>Road_Main, road_01</td></tr>
<tr><td><code>layer_\\d+</code></td><td>Match "layer_" followed by digits</td><td>layer_01, layer_123</td></tr>
</table>

<h3>Apply Results</h3>
<p>After clicking "Apply", the plugin traverses all layers and displays results:</p>
<ul>
<li><b>Success</b>: Number of layers that matched rules and had styles applied successfully</li>
<li><b>Failed</b>: Number of layers that matched rules but style application failed (e.g., style file not found)</li>
<li><b>Unmatched</b>: Number of layers that didn't match any rules</li>
</ul>
<p>Detailed processing logs can be viewed in the QGIS Message Log panel (tab: AutoStyle).</p>

<h3>Notes</h3>
<ul>
<li>Rules are matched from top to bottom, <b>first match wins</b>, subsequent rules are not processed for that layer</li>
<li>Regular expressions are case-sensitive by default, use <code>(?i)</code> prefix for case-insensitive matching</li>
<li>It is recommended to use absolute paths for style files to ensure they exist and are accessible</li>
<li>Regex syntax is automatically validated when saving configs</li>
<li>Config data is stored in JSON format in the styles folder of the plugin directory</li>
</ul>
""",
    },
}


def tr(key: str, **kwargs) -> str:
    """
    Get translated text.

    :param key: Translation key
    :param kwargs: Format parameters
    :return: Translated text
    """
    lang = get_current_language()
    translation = _TRANSLATIONS.get(key, {})

    text = translation.get(lang, translation.get('en', key))

    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text
