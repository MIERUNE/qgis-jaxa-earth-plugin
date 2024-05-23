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
import datetime
import webbrowser

# QGIS-API
from qgis.PyQt import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface

# Load module
from .jaxa.earth import je

with open(os.path.join(os.path.dirname(__file__), "catalog.json")) as f:
    CATALOG = json.load(f)


def parse_jaxa_dateid(date_id: str, year=None) -> (int, int, int):
    """
    JAXA Earth API for Pythonで存在しうるdate_idから年月日を取得する
    一部のパターンには年情報が含まれていないので、その場合はyear引数を参照する
    """
    if year is None:
        _year = 2017
    else:
        _year = year

    if len(date_id) == 8:
        # YYYYMMDD
        return int(date_id[:4]), int(date_id[4:6]), int(date_id[6:8])
    elif len(date_id) == 6:
        # YYYYMM
        return int(date_id[:4]), int(date_id[4:6]), 1
    elif len(date_id) == 4:
        if int(date_id[:2]) > 12:
            # YYYY
            return int(date_id), 1, 1
        else:
            # MMDD
            return _year, int(date_id[:2]), int(date_id[2:4])
    elif len(date_id) == 3:
        # 001-365
        dt = datetime.datetime(_year, 1, 1) + datetime.timedelta(days=int(date_id) - 1)
        return dt.year, dt.month, dt.day
    elif len(date_id) == 2:
        # MM
        return _year, int(date_id), 1

    return 1980, 1, 1  # fallback


def has_yearly_data(data_id: str) -> bool:
    """
    JAXA Earth API for Pythonで存在しうるdata_idから年が判別出来るかどうかを返す
    """
    if len(data_id) == 8 or len(data_id) == 6:
        return True

    if len(data_id) == 4 and int(data_id[:2]) > 12:
        return True

    return False


# uiファイルの定義と同じクラスを継承する
class JaxaEarthApiDialog(QDialog):
    closingPlugin = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(
            os.path.join(os.path.dirname(__file__), "jaxaEarthApiDialog.ui"), self
        )

        self.init_gui()

    def classify_datasets(self):
        classes = {"globe": [], "local": [], "unknown": []}

        for dataset_name, dataset_info in CATALOG.items():
            bbox = dataset_info["bbox"][0]
            longitude_W = int(bbox[0])
            longitude_E = int(bbox[2])
            longitude = [longitude_W, longitude_E]

            _dataset_info = {**dataset_info, "key": dataset_name}

            if longitude == [-180, 180]:
                classes["globe"].append(_dataset_info)
            elif -180 < longitude_W < 180:
                classes["local"].append(_dataset_info)
            else:
                classes["unknown"].append(_dataset_info)

        return classes

    def init_gui(self):
        self.bandCombobox.addItem(self.tr("Select Band", None))

        classes = self.classify_datasets()

        # global
        self.datasetCombobox.addItem(self.tr("-------- Global ------------", None))
        for dataset in classes["globe"]:
            self.datasetCombobox.addItem(dataset["title"], dataset)
        # local
        self.datasetCombobox.addItem(self.tr("--------- Local(Japan) ---------", None))
        for dataset in classes["local"]:
            self.datasetCombobox.addItem(dataset["title"], dataset)
        # unknown
        self.datasetCombobox.addItem(self.tr("----------- Unknown -----------", None))
        for dataset in classes["unknown"]:
            self.datasetCombobox.addItem(dataset["title"], dataset)

        self.datasetCombobox.currentIndexChanged.connect(
            lambda: self.reload_band_combobox()
        )

        self.loadButton.clicked.connect(lambda: self.load_dataset())
        self.detailsButton.clicked.connect(lambda: self.show_details())

        self.datasetCombobox.currentIndexChanged.connect(self.on_dataset_changed)
        self.bandCombobox.currentIndexChanged.connect(self.on_dataset_changed)

        # QgsExtentGroupBox
        self.ui.mExtentGroupBox.setMapCanvas(iface.mapCanvas())
        self.ui.mExtentGroupBox.setOutputCrs(QgsProject.instance().crs())
        self.ui.mExtentGroupBox.setOutputExtentFromCurrent()
        QgsProject.instance().crsChanged.connect(
            lambda: [
                self.ui.mExtentGroupBox.setOutputCrs(QgsProject.instance().crs()),
                self.ui.mExtentGroupBox.setOutputExtentFromCurrent(),
            ]
        )

    def on_dataset_changed(self):
        self.loadButton.setEnabled(self.is_executable())
        self.detailsButton.setEnabled(self.is_executable())

        self.adjustSize()

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

        current_time = datetime.datetime.now()
        ct_list = [
            current_time.year,
            current_time.month,
            current_time.day,
            current_time.hour,
            current_time.minute,
            current_time.second,
        ]

        interval_start_time = dataset_info["temporal"][0][0]
        interval_end_time = dataset_info["temporal"][0][1]  # str

        interval_start_time_obj = datetime.datetime.strptime(
            interval_start_time, "%Y-%m-%dT%H:%M:%SZ"
        )
        st_list = [
            interval_start_time_obj.year,
            interval_start_time_obj.month,
            interval_start_time_obj.day,
            interval_start_time_obj.hour,
            interval_start_time_obj.minute,
            interval_start_time_obj.second,
        ]

        self.startDateEdit.setMinimumDateTime(
            QDateTime(
                st_list[0], st_list[1], st_list[2], st_list[3], st_list[4], st_list[5]
            )
        )

        self.endDateEdit.setMinimumDateTime(
            QDateTime(
                st_list[0], st_list[1], st_list[2], st_list[3], st_list[4], st_list[5]
            )
        )

        if interval_end_time is None:
            self.startDateEdit.setMaximumDateTime(
                QDateTime(
                    ct_list[0],
                    ct_list[1],
                    ct_list[2],
                    ct_list[3],
                    ct_list[4],
                    ct_list[5],
                )
            )

            self.endDateEdit.setMaximumDateTime(
                QDateTime(
                    ct_list[0],
                    ct_list[1],
                    ct_list[2],
                    ct_list[3],
                    ct_list[4],
                    ct_list[5],
                )
            )

        else:
            interval_end_time_obj = datetime.datetime.strptime(
                interval_end_time, "%Y-%m-%dT%H:%M:%SZ"
            )
            et_list = [
                interval_end_time_obj.year,
                interval_end_time_obj.month,
                interval_end_time_obj.day,
                interval_end_time_obj.hour,
                interval_end_time_obj.minute,
                interval_end_time_obj.second,
            ]

            self.startDateEdit.setMaximumDateTime(
                QDateTime(
                    et_list[0],
                    et_list[1],
                    et_list[2],
                    et_list[3],
                    et_list[4],
                    et_list[5],
                )
            )

            self.endDateEdit.setMaximumDateTime(
                QDateTime(
                    et_list[0],
                    et_list[1],
                    et_list[2],
                    et_list[3],
                    et_list[4],
                    et_list[5],
                )
            )

    def load_dataset(self):
        # 1年以上の期間があれば、もう一方のQDateTimeEditの入力値を制限する
        if (
            self.startDateEdit.dateTime().secsTo(self.endDateEdit.dateTime())
            > 365 * 24 * 60 * 60
        ):
            QMessageBox.information(
                self, "Error", self.tr("1年を超える期間を指定することは出来ません。", None)
            )
            return

        dataset_name = self.datasetCombobox.currentData()["key"]
        band = self.bandCombobox.currentData()
        start_datetime = self.startDateEdit.date().toString("yyyy-MM-dd") + "T00:00:00"
        end_datetime = self.endDateEdit.date().toString("yyyy-MM-dd") + "T23:59:59"

        extent = [
            self.ui.mExtentGroupBox.outputExtent().xMinimum(),
            self.ui.mExtentGroupBox.outputExtent().yMinimum(),
            self.ui.mExtentGroupBox.outputExtent().xMaximum(),
            self.ui.mExtentGroupBox.outputExtent().yMaximum(),
        ]

        # Get an image
        try:
            data = (
                je.ImageCollection(
                    collection=dataset_name,
                    ssl_verify=True,
                )
                .filter_date([start_datetime, end_datetime])
                .filter_resolution()
                .filter_bounds(bbox=extent)
                .select(band)
            )
        except Exception as e:
            QMessageBox.information(
                self,
                self.tr("Error"),
                str(e),
            )
            print(e)
            return

        # check amount of data
        data_count = len(data.stac_band.url)

        if data_count == 0:
            QMessageBox.information(self, "Error", "No feature found.")
            return

        if data_count > 0:
            if QMessageBox.No == QMessageBox.question(
                None,
                "Check",
                f"{data_count} features found.\nLoad it?",
                QMessageBox.Yes,
                QMessageBox.No,
            ):
                return

        try:
            data = je.ImageCollection.get_images(data)
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

        prev_month = 0
        year_increment = 0
        for layer in qgs_layers:
            layer.temporalProperties().setIsActive(True)

            date_id = layer.name().split("_")[-1]
            year = None
            if not has_yearly_data(date_id):
                year = self.startDateEdit.date().year()

            y, m, d = parse_jaxa_dateid(date_id, year)

            if prev_month > m:
                # 年跨ぎ
                year_increment += 1

            y += year_increment

            #  range is temporary.
            # Need to fix QgsDateTimeRange into proper time range.
            range = QgsDateTimeRange(
                QDateTime(y, m, d, 0, 0, 0),
                QDateTime(y, m, d, 23, 59, 59),
            )
            layer.temporalProperties().setFixedTemporalRange(range)

            prev_month = m

        root = QgsProject().instance().layerTreeRoot()
        group_node = root.insertGroup(0, dataset_name)
        group_node.setExpanded(False)

        for layer in qgs_layers:
            QgsProject.instance().addMapLayer(layer, False)
            layer_node = group_node.addLayer(layer)
            layer_node.setExpanded(False)

    def show_details(self):
        dataset_name = self.datasetCombobox.currentData()["key"]
        webbrowser.open(f"https://data.earth.jaxa.jp/en/datasets/#/id/{dataset_name}")
        return
