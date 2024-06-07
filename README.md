# JAXA Earth API Plugin

![icon](imgs/icon.png)

QGIS Plugin for JAXA Earth API  

[QGIS Python Plugins Repository](https://plugins.qgis.org/plugins/qgis-jaxa-earth-plugin-master)  

![04](imgs/04.jpg)

## Usage

1. Install the plugin via [QGIS Python Plugins Repository](https://plugins.qgis.org/plugins/qgis-jaxa-earth-plugin-master) or ZIP-file downloadable from releases.  

2. JAXA Earth Icon is added to QGIS toolbar. By clicking on this icon, Plugin dialog is shown.  
![01](imgs/01.jpg)

3. Set CRS to EPSG:4326 or EPSG:3857 and set the area of interest.  
- Area of interest can be set with:
    - Layer: target layer extent
    - Layout Map: target layout map extent
    - Bookmark: extent saved on bookmark
    - Map Canvas Extent: current map canvas extent
    - Draw on canvas: draw customize extent on map canvas
- Default is current map extent.

![02](imgs/02.jpg)

4. Select the dataset, a band, and the date range, then Load! (Earth API seems to be currently available in 2021 only.)  
![03](imgs/03.jpg)

> **Note**  
> This plugin is not related to [JAXA](https://www.jaxa.jp/). It is just using [JAXA Earth API for Python](https://data.earth.jaxa.jp/api/python/index.html) distributed by JAXA. JAXA Earth API for Python is Prototype, so this plugin is also Prototype.  

## License

Python modules are released under the GNU General Public License v2.0
