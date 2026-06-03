# ----------------------------------------------------------------------------------------
# Load module
# ----------------------------------------------------------------------------------------
import json

import numpy as np
from osgeo import gdal, ogr, osr


# ----------------------------------------------------------------------------------------
# geoj2raster : Convert geojson to raster index
# ----------------------------------------------------------------------------------------
def geoj2raster(geoj, raster):
    # Get img size
    img_size_2d = raster.img.shape[1:3]
    height, width = img_size_2d

    # Showing progress
    print(" - ROI mask : ", end="")

    # Build OGR layer in memory holding the ROI geometry
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    ogr_drv = ogr.GetDriverByName("Memory")
    src_ds = ogr_drv.CreateDataSource("roi")

    geom = ogr.CreateGeometryFromJson(json.dumps(geoj["geometry"]))
    layer = src_ds.CreateLayer("roi", srs, geom.GetGeometryType())

    feat = ogr.Feature(layer.GetLayerDefn())
    feat.SetGeometry(geom)
    layer.CreateFeature(feat)
    feat = None

    # Build in-memory target raster matching the source raster's bbox
    lat_min, lat_max = raster.latlim[0]
    lon_min, lon_max = raster.lonlim[0]

    gdal_drv = gdal.GetDriverByName("MEM")
    target = gdal_drv.Create("", width, height, 1, gdal.GDT_Byte)
    target.SetGeoTransform(
        [
            lon_min,
            (lon_max - lon_min) / width,
            0,
            lat_max,
            0,
            -(lat_max - lat_min) / height,
        ]
    )
    target.SetProjection(srs.ExportToWkt())

    # Rasterize: GDAL handles Point/Line/Polygon and Multi* + polygon holes natively
    gdal.RasterizeLayer(target, [1], layer, burn_values=[1])

    mask = target.GetRasterBand(1).ReadAsArray()

    # Reshape to (1, H, W, 1) boolean
    index = (mask == 1).reshape(1, height, width, 1)

    # Showing progress
    print("masked")

    # Output
    return index
