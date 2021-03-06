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
from qgis.PyQt import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *

# Load module
from .jaxa.earth import je
from .catalog import CATALOG

# uiファイルの定義と同じクラスを継承する
class JaxaEarthApiDockWidget(QDockWidget):
    closingPlugin = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(
            os.path.join(os.path.dirname(__file__), "jaxaEarthApiDockWidget.ui"), self
        )

        self.init_gui()

    def init_gui(self):
        self.datasetCombobox.addItem(self.tr("Select Dataset", None))
        self.bandCombobox.addItem(self.tr("Select Band", None))

        for dataset_name, dataset_info in CATALOG.items():
            self.datasetCombobox.addItem(
                dataset_info["title"], {**dataset_info, "key": dataset_name}
            )

        self.datasetCombobox.currentIndexChanged.connect(
            lambda: self.reload_band_combobox()
        )

        self.loadButton.clicked.connect(lambda: self.load_dataset())

        self.datasetCombobox.currentIndexChanged.connect(
            lambda: self.loadButton.setEnabled(self.is_executable())
        )
        self.bandCombobox.currentIndexChanged.connect(
            lambda: self.loadButton.setEnabled(self.is_executable())
        )

    def is_executable(self):
        return (
            self.datasetCombobox.currentData() is not None
            and self.bandCombobox.currentData() is not None
        )

    def reload_band_combobox(self):
        self.bandCombobox.clear()
        if self.datasetCombobox.currentData() is None:
            return

        dataset_info = self.datasetCombobox.currentData()
        for band in dataset_info.get("bands", []):
            self.bandCombobox.addItem(band, band)

    def load_dataset(self):
        dataset_name = self.datasetCombobox.currentData()["key"]
        band = self.bandCombobox.currentData()
        start_datetime = self.startDateEdit.date().toString("yyyy-MM-dd") + "T00:00:00"
        end_datetime = self.endDateEdit.date().toString("yyyy-MM-dd") + "T23:59:59"
        # Get an image
        try:
            data = (
                je.ImageCollection(
                    collection=dataset_name,
                    ssl_verify=True,
                )
                .filter_date([start_datetime, end_datetime])
                .filter_resolution()
                .filter_bounds(bbox=None)  # implicitly use MapCanvas Extent
                .select(band)
                .get_images()
            )
        except Exception as e:
            QMessageBox.information(
                self,
                self.tr("Error"),
                str(e),
            )
            print(e)
            return
        # print(data.stac_bounds.band_url)

        # Process and show an image
        qgs_layers = je.ImageProcess(data).get_qgis_layers()

        root = QgsProject().instance().layerTreeRoot()
        group_node = root.insertGroup(0, dataset_name)
        group_node.setExpanded(False)

        for layer in qgs_layers:
            QgsProject.instance().addMapLayer(layer, False)
            layer_node = group_node.addLayer(layer)
            layer_node.setExpanded(False)
