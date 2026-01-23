# -*- coding: utf-8 -*-
"""
AutoStyle - QGIS 样式表管理与应用插件

该插件提供样式配置表的管理功能，支持通过正则表达式匹配图层名称，
自动为匹配的图层应用对应的 QML 样式文件。
"""


def classFactory(iface):
    """
    QGIS 插件入口函数

    :param iface: QgisInterface 实例，提供与 QGIS 交互的接口
    :return: AutoStyle 插件实例
    """
    from .auto_style import AutoStyle
    return AutoStyle(iface)
