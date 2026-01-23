# AutoStyle

[English](README_EN.md)

QGIS 样式管理与批量应用插件，支持正则匹配图层名称自动应用 QML 样式。

## 功能特性

- **样式配置管理**：创建、编辑、删除样式配置表
- **正则匹配**：通过正则表达式匹配图层名称
- **批量应用**：一键为匹配的图层应用 QML 样式文件
- **国际化**：根据 QGIS 语言设置自动切换中英文界面

## 系统要求

- QGIS >= 3.22

## 安装

1. 下载插件 ZIP 文件
2. 打开 QGIS，进入 `插件` -> `管理和安装插件` -> `从ZIP安装`
3. 选择下载的 ZIP 文件并安装

## 使用方法

### 1. 打开插件

点击工具栏上的 AutoStyle 图标，或通过菜单 `插件` -> `AutoStyle` -> `AutoStyle` 打开。

### 2. 创建样式配置

点击 `新建` 按钮，输入配置名称和样式规则。

### 3. 配置格式

每行一条规则，格式为：

```
"<正则表达式>": "<QML样式文件路径>"
```

示例：

```
"^道路.*": "/path/to/road.qml"
"^建筑": "/path/to/building.qml"
".*河流.*": "/path/to/river.qml"
```

### 4. 应用样式

选择配置后，点击 `应用` 按钮，插件将：

1. 遍历当前项目中的所有图层
2. 使用正则表达式匹配图层名称
3. 为匹配的图层应用对应的 QML 样式

## 项目结构

```
AutoStyle/
├── __init__.py          # 插件入口
├── auto_style.py        # 插件主类
├── metadata.txt         # 插件元数据
├── icon.svg             # 插件图标
├── core/
│   ├── __init__.py
│   ├── i18n.py          # 国际化模块
│   ├── style_manager.py # 样式配置增删改查
│   └── layer_processor.py # 图层遍历与样式应用
├── ui/
│   └── panel_widget.py  # 主对话框界面
└── styles/              # 样式配置存储目录 (JSON)
```

## 开发

### 打包

```bash
./scripts/package.sh
```

打包后的 ZIP 文件将生成在 `dist/` 目录。
