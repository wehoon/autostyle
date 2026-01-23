# AutoStyle

[中文文档](README.md)

Style management and batch apply plugin for QGIS with regex layer name matching.

## Features

- **Style Config Management**: Create, edit, and delete style configurations
- **Regex Matching**: Match layer names using regular expressions
- **Batch Apply**: One-click apply QML style files to matched layers
- **i18n Support**: Auto-switch Chinese/English interface based on QGIS language settings

## Requirements

- QGIS >= 3.22

## Installation

1. Download the plugin ZIP file
2. Open QGIS, go to `Plugins` -> `Manage and Install Plugins` -> `Install from ZIP`
3. Select the downloaded ZIP file and install

## Usage

### 1. Open Plugin

Click the AutoStyle icon on the toolbar, or open via menu `Plugins` -> `AutoStyle` -> `AutoStyle`.

### 2. Create Style Config

Click `New` button, enter config name and style rules.

### 3. Config Format

One rule per line, format:

```
"<regex_pattern>": "<qml_style_file_path>"
```

Example:

```
"^road.*": "/path/to/road.qml"
"^building": "/path/to/building.qml"
".*river.*": "/path/to/river.qml"
```

### 4. Apply Styles

Select a config and click `Apply` button, the plugin will:

1. Traverse all layers in the current project
2. Match layer names using regex patterns
3. Apply corresponding QML styles to matched layers

## Project Structure

```
AutoStyle/
├── __init__.py          # Plugin entry point
├── auto_style.py        # Main plugin class
├── metadata.txt         # Plugin metadata
├── icon.svg             # Plugin icon
├── core/
│   ├── __init__.py
│   ├── i18n.py          # Internationalization module
│   ├── style_manager.py # Style config CRUD operations
│   └── layer_processor.py # Layer traversal and style application
├── ui/
│   └── panel_widget.py  # Main dialog UI
└── styles/              # Style configs storage (JSON)
```

## Development

### Package

```bash
./scripts/package.sh
```

The packaged ZIP file will be generated in the `dist/` directory.

