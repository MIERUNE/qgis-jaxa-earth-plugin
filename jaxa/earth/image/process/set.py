#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
#----------------------------------------------------------------------------------------
# gdal_type : Generate datatype on gdal
#----------------------------------------------------------------------------------------
def gdal_type(img):

    # Load module
    from osgeo import gdal

    # Set datatype
    if img.dtype == "uint8":
        d_type = gdal.GDT_Byte
    if img.dtype == "uint16":
        d_type = gdal.GDT_UInt16    
    elif img.dtype == "float32":
        d_type = gdal.GDT_Float32

    # Output
    return d_type

#----------------------------------------------------------------------------------------
# cmap_qgis
#----------------------------------------------------------------------------------------
def cmap_qgis(img,cinfo,layer):

    # (1) Land cover data
    if cinfo.cmap_params["type"] == "exact":
        cmap_qgis_category(cinfo,layer)
        return 1

    # (2) Other physical data (Set cmin,cmax with +-2 sigma)
    elif cinfo.cmap_params["type"] == "linear":
        cmap_qgis_data(cinfo,layer)
        return 1

    # (3) Visual data (3 layer)
    else:
        return 1

#----------------------------------------------------------------------------------------
# cmap_qgis_data
#----------------------------------------------------------------------------------------
def cmap_qgis_data(cinfo,layer):

    # Load module
    from qgis.core import QgsColorRampShader, QgsRasterShader, QgsSingleBandPseudoColorRenderer
    from qgis.PyQt.QtGui import QColor        

    # Set Shader
    fcn = QgsColorRampShader()
    fcn.setColorRampType(QgsColorRampShader.Interpolated)

    # Generate color map list
    cmin = cinfo.clim[0]
    cmax = cinfo.clim[1]
    cmap = cinfo.cmap_params["colors"]
    lst  = []
    for i in range(len(cmap)):
        value_tmp = (cmax-cmin)*(i/(len(cmap)-1))+cmin
        lst.append(QgsColorRampShader.ColorRampItem(value_tmp,QColor(cmap[i]),str(round(value_tmp,2))))

    # Set shader
    fcn.setColorRampItemList(lst)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)

    # Apply render
    renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader)
    layer.setRenderer(renderer)
    layer.triggerRepaint()

    # Finish
    return 1

#----------------------------------------------------------------------------------------
# cmap_qgis_category
#----------------------------------------------------------------------------------------
def cmap_qgis_category(cinfo,layer):

    # Load module
    from qgis.core import QgsPalettedRasterRenderer
    from qgis.PyQt.QtGui import QColor    

    # Set labels
    labels = cinfo.cmap_params["labels"]
    lnames = cinfo.cmap_params["lnames"]
    nodata = cinfo.cmap_params["nodata"]

    # Generate value, color, label list
    lst  = []
    for i in range(len(labels)):

        # Set parameters
        value = labels[i][lnames["value"]]
        color = QColor(labels[i][lnames["color"]])
        label = str(labels[i][lnames["value"]])+" : "+labels[i][lnames["name"]]        

        # Set color label list (ignore nodata)
        if value != nodata:
            lst.append(QgsPalettedRasterRenderer.Class(value,color,label))

    # Set renderer
    renderer = QgsPalettedRasterRenderer(
        layer.dataProvider(), # QgsRasterInterface
        1,                    # bandNumber
        lst)                  # classes:Iterable
    layer.setRenderer(renderer)

    # Finish
    return 1