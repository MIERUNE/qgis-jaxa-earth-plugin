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
import json

# QGIS-API
from qgis.PyQt import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *

# Load module
from .jaxa.earth import je

with open(os.path.join(os.path.dirname(__file__), "catalog.json")) as f:
    CATALOG = json.load(f)


# uiファイルの定義と同じクラスを継承する
class JaxaEarthApiDockWidget(QDockWidget):
    closingPlugin = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(
            os.path.join(os.path.dirname(__file__),
                         "jaxaEarthApiDockWidget.ui"), self
        )

        self.init_gui()

    def classify_datasets(self):
        classes = {
            "globe": [],
            "local": [],
            "unknown": []
        }

        for dataset_name, dataset_info in CATALOG.items():
            bbox = dataset_info["bbox"][0]
            logitude_W = int(bbox[0])
            logitude_E = int(bbox[2])
            logitude = [logitude_W, logitude_E]

            _dataset_info = {
                **dataset_info,
                "key": dataset_name
            }

            if logitude == [-180, 180]:
                classes["globe"].append(_dataset_info)
            elif -180 < logitude_W < 180:
                classes["local"].append(_dataset_info)
            else:
                classes["unknown"].append(_dataset_info)

        return classes

    def init_gui(self):
        self.bandCombobox.addItem(self.tr("Select Band", None))

        classes = self.classify_datasets()

        # global
        self.datasetCombobox.addItem(
            self.tr("-------- Global ------------", None))
        for dataset in classes["globe"]:
            self.datasetCombobox.addItem(
                dataset["title"], dataset
            )
        # local
        self.datasetCombobox.addItem(
            self.tr("--------- Local(Japan) ---------", None))
        for dataset in classes["local"]:
            self.datasetCombobox.addItem(
                dataset["title"], dataset
            )
        # unknown
        self.datasetCombobox.addItem(
            self.tr("----------- Unknown -----------", None))
        for dataset in classes["unknown"]:
            self.datasetCombobox.addItem(
                dataset["title"], dataset
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

        # dataset_infoの中身を見てみたい。
        # dataset_infoには何が入っているのか？
        # dataset_info["temporal"] = [["1980-1-31T12:34:56Z", "1980-12-31T12:34:56Z"]]->correct?
        print("dataset_info : ", dataset_info)
        print("temporal     : ", dataset_info["temporal"])

        import datetime
        # current time
        current_time = datetime.datetime.now()
        ct_list = [
            current_time.year,  # all elemnts are int
            current_time.month,
            current_time.day,
            current_time.hour,
            current_time.minute,
            current_time.second
        ]

        # dataset_info["temporal"] = [["1980-1-31T12:34:56Z", "1980-12-31T12:34:56Z"]]->correct?
        # interval start_time, end_time
        # str　→ error が出てくる。dataset_info.get("temporal", [])なのか？
        interval_start_time = dataset_info["temporal"][0][0]
        interval_end_time = dataset_info["temporal"][0][1]  # str

        # change interval times info from iso8601 into int within integer
        # make interval_start_time
        interval_start_time_obj = datetime.datetime.strptime(
            interval_start_time, '%Y-%m-%dT%H:%M:%SZ')
        st_list = [
            interval_start_time_obj.year,
            interval_start_time_obj.month,
            interval_start_time_obj.day,
            interval_start_time_obj.hour,
            interval_start_time_obj.minute,
            interval_start_time_obj.second
        ]

        ##
        self.startDateEdit.setMinimumDateTime(
            QDateTime(st_list[0], st_list[1], st_list[2], st_list[3], st_list[4], st_list[5]))

        self.endDateEdit.setMinimumDateTime(
            QDateTime(st_list[0], st_list[1], st_list[2], st_list[3], st_list[4], st_list[5]))

        if interval_end_time is None:
            # 　When end time inside temporal is None
            # ->use current time
            self.startDateEdit.setMaximumDateTime(
                QDateTime(ct_list[0], ct_list[1], ct_list[2], ct_list[3], ct_list[4], ct_list[5]))

            self.endDateEdit.setMaximumDateTime(
                QDateTime(ct_list[0], ct_list[1], ct_list[2], ct_list[3], ct_list[4], ct_list[5]))

        else:
            # 　When end time inside temporal is available
            # ->use interval_end_time
            #  make interval_end_time
            interval_end_time_obj = datetime.datetime.strptime(
                interval_end_time, '%Y-%m-%dT%H:%M:%SZ')
            et_list = [
                interval_end_time_obj.year,
                interval_end_time_obj.month,
                interval_end_time_obj.day,
                interval_end_time_obj.hour,
                interval_end_time_obj.minute,
                interval_end_time_obj.second
            ]

            self.startDateEdit.setMaximumDateTime(
                QDateTime(et_list[0], et_list[1], et_list[2], et_list[3], et_list[4], et_list[5]))

            self.endDateEdit.setMaximumDateTime(
                QDateTime(et_list[0], et_list[1], et_list[2], et_list[3], et_list[4], et_list[5]))

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

        # Process and show an image
        qgs_layers = je.ImageProcess(data).get_qgis_layers()

        for idx, layer in enumerate(qgs_layers):
            layer.temporalProperties().setIsActive(True)

            #  range is temporary.
            # Need to fix QgsDateTimeRange into proper time range.
            range = QgsDateTimeRange(QDateTime(1980 + idx, 1, 1, 0, 0, 0),
                                     QDateTime(1980 + idx, 12, 31, 23, 59, 59))
            layer.temporalProperties().setFixedTemporalRange(range)

        root = QgsProject().instance().layerTreeRoot()
        group_node = root.insertGroup(0, dataset_name)
        group_node.setExpanded(False)

        for layer in qgs_layers:
            QgsProject.instance().addMapLayer(layer, False)
            layer_node = group_node.addLayer(layer)
            layer_node.setExpanded(False)
