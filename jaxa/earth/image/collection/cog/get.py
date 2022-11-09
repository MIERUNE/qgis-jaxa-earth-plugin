#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
from ....utils  import progress,get
from .calcsize  import check_img_size_rough,calc_img_size
from .image.get import get_single_raster
from .integ     import integ_img
from .color     import ColorInfo
from .ifd.read  import read_all_ifd

#----------------------------------------------------------------------------------------
# get_multiple_dates_raster
#----------------------------------------------------------------------------------------
def get_multiple_dates_raster(input):

    # Get data parameters
    session     = input._session
    feat_query  = input.stac_bounds.query
    fname       = input.stac_band.url
    lon_offsets = input.stac_bounds.lon_offsets
    date_id     = input.stac_date.id
    ifd_ppu     = input.cog_ifd_ppu
    pixels_max  = input._settings.pixels_max
    proj_params = input.proj_params

    # Get and check image size and each file's pixel location    
    check_img_size_rough(feat_query,ifd_ppu,pixels_max,proj_params)    

    # Read multiple date cog
    for i_date in range(len(fname)):

        # Showing progress
        print(f" - Loading images No.{i_date} : {date_id[i_date]}")

        # Get valid cog names, offsets
        fn_date   = np.ravel(fname[i_date])
        loff_date = np.ravel(lon_offsets[i_date])

        # Read multiple bounds cog
        raster_tmp,cinfo_tmp = get_multiple_bounds_raster(session,input,fn_date,loff_date)        

        # Append raster, cinfo
        if i_date == 0:
            raster = raster_tmp
            cinfo  = np.array([cinfo_tmp])
        else:
            raster = raster.append(raster_tmp)
            cinfo  = np.append(cinfo,[cinfo_tmp],axis=0)
    
    # Calc lat,lon range and img list to numpy array
    raster.calc_latlon_range().to_numpy()

    # Showing image (for test)
    #import matplotlib.pyplot as plt
    #plt.imshow(raster.img[0])
    #plt.show()

    # Output image
    return raster,cinfo

#----------------------------------------------------------------------------------------
# get_multiple_bounds_raster : Read multiple COG image
#----------------------------------------------------------------------------------------
def get_multiple_bounds_raster(session,input,fn_date,loff_date):

    # Set parameters
    pixels_max  = input._settings.pixels_max
    bin_len     = input._settings.first_get_byte
    feat_query  = input.stac_bounds.query
    lon_offsets = input.stac_bounds.lon_offsets
    feat_cogs   = input.stac_bounds.json
    band        = input.stac_band.query
    ifd_lev     = input.cog_ifd_lev
    ifd_ppu     = input.cog_ifd_ppu
    proj_params = input.proj_params
    
    # Get data roles, raster parameters, values
    roles      = feat_cogs[0][0]["assets"][band]["roles"][0]
    r_params   = feat_cogs[0][0]["assets"][band]["je:rasters"]
    value_info = r_params["value"]
    nodata     = feat_cogs[0][0]["assets"][band]["je:rasters"]["dn"]["nodata"]

    # Overwrite labels classification if exists
    if "classification:classes" in feat_cogs[0][0]["assets"][band]:
        value_info["labels"] = feat_cogs[0][0]["assets"][band]["classification:classes"]
        value_info["lnames"] = {
            "name":"description",
            "value":"value",
            "color":"color-hint"
        }
    else:
        value_info["lnames"] = {
            "name":"name",
            "value":"value",
            "color":"color"
        }

    # Get multiple cog files
    for i_bounds in range(len(fn_date)):

        # Skip if file name is not valid
        if fn_date[i_bounds].count(".tif") == 0:
            progress.bar(i_bounds,len(fn_date))
            continue

        # Get raw binary (until first specific bytes)
        first_bin = get.range(session,fn_date[i_bounds],0,bin_len)

        # Read binary and convert it to IFD meta data
        ifd = read_all_ifd(first_bin,ifd_lev)
        
        # Get single raster files
        raster_tmp = get_single_raster(session,fn_date[i_bounds],loff_date[i_bounds],feat_query,ifd,roles,r_params,proj_params)

        # Append raster
        if i_bounds == 0:
            raster = raster_tmp
        else:
            raster.append(raster_tmp)

        # Showing progress
        progress.bar(i_bounds,len(fn_date))

    # Calc image size
    img_size,pix_x,pix_y = calc_img_size(feat_cogs,feat_query,ifd_ppu,raster.ppu,pixels_max,proj_params,lon_offsets)
    
    # Convert from list(3d) to image (2d), Fill in the missing places
    raster.img = integ_img(raster.img,img_size,pix_x,pix_y,roles)

    # Get color information
    cinfo = ColorInfo(raster.pint,roles,value_info,nodata).set_cmap_params()

    # Get all raster's boundary's range of lat, lon
    raster.calc_latlon_range()

    # Showing image (for test)
    #import matplotlib.pyplot as plt
    #plt.imshow(raster.img[0])
    #plt.show()

    # Output
    return raster,cinfo