#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
import warnings
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1

#----------------------------------------------------------------------------------------
# show : Visualize image
#----------------------------------------------------------------------------------------
def show_image(img,latlim,lonlim,title,cinfo,proj_params):

    # Set color map information
    cmap,norm  = cinfo.get_lin_seg_cmap()

    # Set labels
    x_label  = proj_params.lon_label_str
    y_label  = proj_params.lat_label_str
    decimals = 5

    # Set lat_tick,lon tick
    tick_itv = 5
    lat_d    = (latlim[1]-latlim[0])/img.shape[0]
    lat_pix  = np.linspace(        0,img.shape[0]-1,tick_itv)
    lat_tick = np.linspace(latlim[-1]-lat_d/2,
                           latlim[ 0]+lat_d/2,tick_itv).round(decimals)
    lon_d    = (lonlim[1]-lonlim[0])/img.shape[1]
    lon_pix  = np.linspace(        0,img.shape[1]-1,tick_itv)
    lon_tick = np.linspace(lonlim[ 0]+lon_d/2,
                           lonlim[ 1]-lon_d/2,tick_itv).round(decimals)

    # Set figure size
    aspect_ratio = img.shape[1]/img.shape[0]

    # Set figure,title,tick interval
    fig = plt.figure(figsize=(5*aspect_ratio+2,5))
    ax  = fig.add_subplot(111)
    ax.set_title( title ,fontsize=10)
    
    # Set latitude(y) label
    ax.set_ylabel(y_label,fontsize=10)
    ax.set_yticks(     lat_pix )
    ax.set_yticklabels(lat_tick)

    # Set longitude(x) label
    ax.set_xlabel(x_label,fontsize=10)
    ax.set_xticks(     lon_pix )
    ax.set_xticklabels(lon_tick)
    
    # Set grid line
    ax.grid(color='gray',linestyle='--',linewidth=0.5)

    # Set image
    if   cinfo.cmap_params["type"] == "exact":
        im = ax.imshow(img.squeeze(), cmap=cmap, norm=norm, interpolation="nearest")
    elif cinfo.cmap_params["type"] == "linear":
        im = ax.imshow(img.squeeze(), cmap=cmap, vmin = cinfo.clim[0], vmax = cinfo.clim[1])
    else:
        im = ax.imshow(img.squeeze())

    # Set colorbar (visual(RGB) dont need colorbar)
    if cinfo.cmap_params["type"] is not None:
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
        cax     = divider.append_axes('right',0.2, pad = '3%')
        cbar    = fig.colorbar(im,cax=cax)
        cbar.set_label(cinfo.unit,fontsize = 10)

    # Keep showing until press close button
    plt.show()
    plt.pause(1)

    # Save image (if required)
    #plt.savefig("test.png")    

    # Close image
    #plt.clf()
    #plt.close()

    # Finish
    return 1

#----------------------------------------------------------------------------------------
# show_image_qgis : Visualize image in qgis
#----------------------------------------------------------------------------------------
def show_image_qgis(id,date_id,img,latlim,lonlim,cinfo,proj):

    # Load module
    import os
    import datetime
    import numpy as np
    from qgis.core import QgsRasterLayer, QgsProject, QgsProcessingUtils
    from osgeo import gdal,osr
    from .set import gdal_type as set_gdal_type
    from .set import cmap_qgis as set_cmap_qgis

    # Temp directory path which is used to save tif file
    folder_tmp = QgsProcessingUtils.tempFolder()

    # Set fname, data path
    fn_t  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{fn_t}_{id:03.0f}_{date_id}"
    data_path = os.path.join(folder_tmp,fname+".tif")

    # Set Image
    img_size = img.shape
    image    = np.transpose(img,(2,0,1))

    # Set resolution
    lon_res =  (lonlim[1]-lonlim[0])/img_size[1]
    lat_res = -(latlim[1]-latlim[0])/img_size[0]

    # Set data type
    d_type = set_gdal_type(img)

    # Set tiff driver
    driver = gdal.GetDriverByName('GTiff')
    raster = driver.Create(data_path, img_size[1], img_size[0], img_size[2], d_type)
    
    # Check type and throw error if None type
    if raster is None:
        print("path : " + data_path)
        raise Exception("Error! please check the inputed file path and permission to write/read!")

    # Set Transform
    raster.SetGeoTransform((lonlim[0], lon_res,    0    ,
                            latlim[1],    0   , lat_res))

    # Set projection
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(proj)
    raster.SetProjection(srs.ExportToWkt())

    # Write data to tif file in temp folder
    for i in range(len(image)):
        raster.GetRasterBand(i+1).WriteArray(image[i])
    raster.FlushCache()
    raster = None

    # Load as QGIS layer 
    layer = QgsRasterLayer(data_path,fname)
    QgsProject.instance().addMapLayer(layer)

    # Apply colormap
    set_cmap_qgis(img,cinfo,layer)

    # Finish
    return 1


def get_qgis_layer(id,date_id,img,latlim,lonlim,cinfo,proj):

    # Load module
    import os
    import datetime
    import numpy as np
    from qgis.core import QgsRasterLayer, QgsProject, QgsProcessingUtils
    from osgeo import gdal,osr
    from .set import gdal_type as set_gdal_type
    from .set import cmap_qgis as set_cmap_qgis

    # Temp directory path which is used to save tif file
    folder_tmp = QgsProcessingUtils.tempFolder()

    # Set fname, data path
    fn_t  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{fn_t}_{id:03.0f}_{date_id}"
    data_path = os.path.join(folder_tmp,fname+".tif")

    # Set Image
    img_size = img.shape
    image    = np.transpose(img,(2,0,1))

    # Set resolution
    lon_res =  (lonlim[1]-lonlim[0])/img_size[1]
    lat_res = -(latlim[1]-latlim[0])/img_size[0]

    # Set data type
    d_type = set_gdal_type(img)

    # Set tiff driver
    driver = gdal.GetDriverByName('GTiff')
    raster = driver.Create(data_path, img_size[1], img_size[0], img_size[2], d_type)
    
    # Check type and throw error if None type
    if raster is None:
        print("path : "+data_path)
        raise Exception("Error! please check the inputed file path and permission to write/read!")

    # Set Transform
    raster.SetGeoTransform((lonlim[0], lon_res,    0    ,
                            latlim[1],    0   , lat_res))

    # Set projection
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(proj)
    raster.SetProjection(srs.ExportToWkt())

    # Write data to tif file in temp folder
    for i in range(len(image)):
        raster.GetRasterBand(i+1).WriteArray(image[i])
    raster.FlushCache()
    raster = None

    # Load as QGIS layer 
    layer = QgsRasterLayer(data_path,fname)

    # Apply colormap
    set_cmap_qgis(img,cinfo,layer)

    # Finish
    return layer


#----------------------------------------------------------------------------------------
# show_timeseries_multi : Visualize multiple band timeseries
#----------------------------------------------------------------------------------------
def show_timeseries(timeseries,title,xlabel,ylabel,ylim):

    # Check dimension
    ts_dim = timeseries["mean"].shape

    # Loop for multi
    for i in range(ts_dim[1]):
        ts_in = {"mean":timeseries["mean"][:,i],
                 "std" :timeseries["std" ][:,i],
                 "min" :timeseries["min" ][:,i],
                 "max" :timeseries["max" ][:,i]}
        show_timeseries_single(ts_in,title,xlabel,ylabel,ylim)

    # Finish
    return 1

#----------------------------------------------------------------------------------------
# show_timeseries_single : Visualize single band timeseries
#----------------------------------------------------------------------------------------
def show_timeseries_single(timeseries,title,xlabel,ylabel,ylim):

    # Set figure,title,tick interval
    fig = plt.figure()
    ax  = fig.add_axes((0.1,0.2,0.8,0.7))
    ax.set_title( title ,fontsize=10)
    
    # Set latitude(y) label
    ax.set_ylabel(ylabel,fontsize=10)

    # Set longitude(x) label
    ax.set_xticks(np.linspace(0,len(xlabel)-1,len(xlabel)))
    ax.set_xticklabels(xlabel,rotation=90,ha="right")

    # Set grid line
    ax.grid(color='gray',linestyle='--',linewidth=0.5)

    # Set timeseries plot (mean, std)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        ax.errorbar(xlabel,timeseries["mean"],
                    yerr = timeseries["std" ],
                    fmt="ob-",linewidth=3,capsize=5,elinewidth=1,label="mean +/- std")
    
    # Set timeseries plot (min, max)
    ax.plot(xlabel,timeseries["max"],linestyle="--",color="r",label="max")                
    ax.plot(xlabel,timeseries["min"],linestyle="--",color="r",label="min")
    ax.legend()
    
    # Set ylim
    if not (not ylim):
        ax.set_ylim(ylim)

    # Keep showing until press close button
    plt.show()
    plt.pause(1)

    # Save image (if required)
    #plt.savefig("test.png")

    # Close figure
    #plt.clf()
    #plt.close()

    # Finish
    return 1
