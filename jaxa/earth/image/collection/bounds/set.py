#--------------------------------------------------------------------------------
# Load module
#--------------------------------------------------------------------------------
import sys
import math

#--------------------------------------------------------------------------------
# set_bbox ： 
#--------------------------------------------------------------------------------
def set_bbox_geojson(bbox,geoj,proj_params):
  
    # Set min, max of lat,lon
    LAT_RANGE = proj_params.lat_range_max
    LON_RANGE = proj_params.lon_range_max
    MIN_RANGE = proj_params.lon_min_width
    UNIT      = proj_params.unit_str
    DECIMAL   = proj_params.r_dec_bbox

    # Initialize bbox if no input
    if (bbox is None) & (geoj is None):
        if "qgis.utils" in sys.modules:
            bbox_out = set_bbox_qgis(proj_params.epsg)
            bbox_out = fix_bbox(bbox_out,LAT_RANGE,LON_RANGE,MIN_RANGE,UNIT,DECIMAL)
            geoj_out = bbox2geojson(bbox_out)
        else:
            bbox_out = [LON_RANGE[0],LAT_RANGE[0],LON_RANGE[1],LAT_RANGE[1]]
            bbox_out = fix_bbox(bbox_out,LAT_RANGE,LON_RANGE,MIN_RANGE,UNIT,DECIMAL)
            geoj_out = bbox2geojson(bbox_out)

    # Input geojson from bbox
    elif geoj is None:
        bbox_out = fix_bbox(bbox,LAT_RANGE,LON_RANGE,MIN_RANGE,UNIT,DECIMAL)
        geoj_out = bbox2geojson(bbox_out)

    # Input bbox from geojson
    else:
        bbox_out = geoj2bbox(geoj,DECIMAL)
        bbox_out = fix_bbox(bbox_out,LAT_RANGE,LON_RANGE,MIN_RANGE,UNIT,DECIMAL)
        geoj["bbox"] = bbox_out
        geoj_out = geoj

    # Output
    return bbox_out, geoj_out

#--------------------------------------------------------------------------------
# geoj2bbox : Calculate bounding box of geojson
#--------------------------------------------------------------------------------
def geoj2bbox(geoj,DECIMAL):

    # Get lon, lat
    lonlat = list(flatten_list(geoj["geometry"]["coordinates"]))

    # Get lonall, latall
    lonall = lonlat[0::2]
    latall = lonlat[1::2]

    # Get bbox
    bbox = [math.floor(min(lonall)*10**DECIMAL)/(10**DECIMAL),\
            math.floor(min(latall)*10**DECIMAL)/(10**DECIMAL),\
            math.ceil( max(lonall)*10**DECIMAL)/(10**DECIMAL),\
            math.ceil( max(latall)*10**DECIMAL)/(10**DECIMAL)]

    # Output
    return bbox

#--------------------------------------------------------------------------------
# bbox2geojson
#--------------------------------------------------------------------------------
def bbox2geojson(bbox):

    # Get coordinates from bbox
    lonlat = [[bbox[0], bbox[1]],
              [bbox[0], bbox[3]],
              [bbox[2], bbox[3]],
              [bbox[2], bbox[1]]]

    # Set geojson dict
    geoj = {"bbox":bbox,
            "geometry":{"coordinates":[lonlat],"type":"Polygon"},
            "properties":{},
            "type":"Feature"}

    # Output
    return geoj

#--------------------------------------------------------------------------------
# flatten_list
#--------------------------------------------------------------------------------
def flatten_list(l):
    for el in l:
        if isinstance(el, list):
            yield from flatten_list(el)
        else:
            yield el

#--------------------------------------------------------------------------------
# fix_bbox
#--------------------------------------------------------------------------------
def fix_bbox(bbox,LAT_RANGE,LON_RANGE,MIN_RANGE,UNIT,DECIMAL):

    # Check bbox length
    if len(bbox) != 4:
        raise Exception("Error! bbox_out needs 4 arguments!")

    # Check bbox limit
    if (bbox[0] < LON_RANGE[0]): bbox[0] = LON_RANGE[0]
    if (bbox[0] > LON_RANGE[1]): bbox[0] = LON_RANGE[1]
    if (bbox[1] < LAT_RANGE[0]): bbox[1] = LAT_RANGE[0]
    if (bbox[1] > LAT_RANGE[1]): bbox[1] = LAT_RANGE[1]
    if (bbox[2] < LON_RANGE[0]): bbox[2] = LON_RANGE[0]
    if (bbox[2] > LON_RANGE[1]): bbox[2] = LON_RANGE[1]
    if (bbox[3] < LAT_RANGE[0]): bbox[3] = LAT_RANGE[0]
    if (bbox[3] > LAT_RANGE[1]): bbox[3] = LAT_RANGE[1]

    # Check bbox range (small enough from MIN_RANGE)
    eq1 = (not math.isclose(bbox[2]-bbox[0],MIN_RANGE)) and ((bbox[2]-bbox[0]) < MIN_RANGE)
    eq2 = (not math.isclose(bbox[3]-bbox[1],MIN_RANGE)) and ((bbox[3]-bbox[1]) < MIN_RANGE)
    if eq1 or eq2 :
         raise Exception(f"Error! At least {MIN_RANGE} {UNIT} difference is need, Input bbox_out : {bbox}")

    # Round bbox_out
    for i in range(len(bbox)):
        bbox[i] = round(bbox[i],DECIMAL)

    # Output
    return bbox

#--------------------------------------------------------------------------------
# set_bbox_qgis ： 
#--------------------------------------------------------------------------------
def set_bbox_qgis(epsg):

    # Load module
    from qgis.core import QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsProject
    import qgis.utils

    # Get displaying bounding box on QGIS crs
    extent = qgis.utils.iface.mapCanvas().extent()

    # Transform crs to EPSG4326
    source_crs = qgis.utils.iface.mapCanvas().mapSettings().destinationCrs()
    dest_crs   = QgsCoordinateReferenceSystem().fromEpsgId(epsg)
    rtrans     = QgsCoordinateTransform(source_crs,dest_crs,QgsProject.instance())
    extent_out = rtrans.transformBoundingBox(extent)

    # Extent to bbox
    bbox = [extent_out.xMinimum(),extent_out.yMinimum(),
            extent_out.xMaximum(),extent_out.yMaximum()]
  
    # Output
    return bbox