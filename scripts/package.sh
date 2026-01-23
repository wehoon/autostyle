#!/bin/bash
# -*- coding: utf-8 -*-
#
# AutoStyle Plugin Packaging Script
# Generates an installable QGIS plugin ZIP package
#

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Plugin root directory
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
# Plugin name
PLUGIN_NAME="AutoStyle"
# Output directory
OUTPUT_DIR="$PLUGIN_DIR/dist"

# Read version from metadata.txt
VERSION=$(grep "^version=" "$PLUGIN_DIR/metadata.txt" | cut -d'=' -f2)

if [ -z "$VERSION" ]; then
    VERSION="1.0.0"
fi

# Output filename
OUTPUT_FILE="$OUTPUT_DIR/${PLUGIN_NAME}-${VERSION}.zip"

echo "========================================"
echo "AutoStyle Plugin Packaging Script"
echo "========================================"
echo "Plugin directory: $PLUGIN_DIR"
echo "Version: $VERSION"
echo "Output file: $OUTPUT_FILE"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Remove old package file
if [ -f "$OUTPUT_FILE" ]; then
    echo "Removing old package file..."
    rm "$OUTPUT_FILE"
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
TEMP_PLUGIN_DIR="$TEMP_DIR/$PLUGIN_NAME"

echo "Creating temporary directory: $TEMP_DIR"

# Copy plugin files to temporary directory
mkdir -p "$TEMP_PLUGIN_DIR"

# Copy core files
cp "$PLUGIN_DIR/__init__.py" "$TEMP_PLUGIN_DIR/"
cp "$PLUGIN_DIR/auto_style.py" "$TEMP_PLUGIN_DIR/"
cp "$PLUGIN_DIR/metadata.txt" "$TEMP_PLUGIN_DIR/"

# Copy icon (SVG only)
cp "$PLUGIN_DIR/icon.svg" "$TEMP_PLUGIN_DIR/"

# Copy core module
mkdir -p "$TEMP_PLUGIN_DIR/core"
cp "$PLUGIN_DIR/core/__init__.py" "$TEMP_PLUGIN_DIR/core/"
cp "$PLUGIN_DIR/core/style_manager.py" "$TEMP_PLUGIN_DIR/core/"
cp "$PLUGIN_DIR/core/layer_processor.py" "$TEMP_PLUGIN_DIR/core/"
cp "$PLUGIN_DIR/core/i18n.py" "$TEMP_PLUGIN_DIR/core/"
cp "$PLUGIN_DIR/core/update_checker.py" "$TEMP_PLUGIN_DIR/core/"

# Copy ui module
mkdir -p "$TEMP_PLUGIN_DIR/ui"
cp "$PLUGIN_DIR/ui/__init__.py" "$TEMP_PLUGIN_DIR/ui/"
cp "$PLUGIN_DIR/ui/panel_widget.py" "$TEMP_PLUGIN_DIR/ui/"
cp "$PLUGIN_DIR/ui/edit_dialog.py" "$TEMP_PLUGIN_DIR/ui/"

# Create empty styles directory
mkdir -p "$TEMP_PLUGIN_DIR/styles"
touch "$TEMP_PLUGIN_DIR/styles/.gitkeep"

echo "Packaging files..."

# Switch to temporary directory and create package
cd "$TEMP_DIR"
zip -r "$OUTPUT_FILE" "$PLUGIN_NAME" -x "*.pyc" -x "*__pycache__*" -x "*.git*"

# Clean up temporary directory
echo "Cleaning up temporary directory..."
rm -rf "$TEMP_DIR"

echo ""
echo "========================================"
echo "Packaging complete!"
echo "========================================"
echo "Output file: $OUTPUT_FILE"
echo ""
echo "Installation instructions:"
echo "1. Open QGIS"
echo "2. Menu: Plugins -> Manage and Install Plugins -> Install from ZIP"
echo "3. Select $OUTPUT_FILE"
echo "4. Click Install"
echo ""

# Display package contents
echo "Package contents:"
unzip -l "$OUTPUT_FILE"
