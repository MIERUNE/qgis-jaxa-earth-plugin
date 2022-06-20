"""
/***************************************************************************
 Sample
                                 A QGIS plugin
 QGIS Sample Plugin
                              -------------------
        begin                : 2021-06-30
        git sha              : $Format:%H$
        copyright            : (C) 2021 by MIERUNE Inc.
        email                : info@mierune.co.jp
        license              : GNU General Public License v2.0
 ***************************************************************************/
"""

import os

# QGIS-API
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *

from .jaxaEarthApiDockWidget import JaxaEarthApiDockWidget

PLUGIN_NAME = "JAXA Earth Api"


class JaxaEarthApiPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.win = self.iface.mainWindow()
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = PLUGIN_NAME
        self.toolbar = self.iface.addToolBar(PLUGIN_NAME)
        self.toolbar.setObjectName(PLUGIN_NAME)
        self.dockwidget = None
        self.action = None

    def initGui(self):
        # メニュー設定
        self.dockwidget = JaxaEarthApiDockWidget()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)

    def unload(self):
        self.iface.removePluginMenu(PLUGIN_NAME, self.action)
        self.action = None

        self.iface.removeDockWidget(self.dockwidget)
        self.dockwidget = None
