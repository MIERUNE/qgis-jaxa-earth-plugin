#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
from .latlon  import get_latlon_pos
from .tile    import calc_padding, get_tiles_pos, get_tiles, reshape_tiles
from .palette import apply_palette,conv_cmap
from .dn2p    import dn2physical
from .raster  import Raster

#----------------------------------------------------------------------------------------
# get_single_raster : Read single COG image
#----------------------------------------------------------------------------------------
def get_single_raster(session,fname,loff,geoj,ifd,roles,r_params,proj_params):

    # Get ifd parameters
    toffset = np.array( ifd[-1]["TileOffsets"   ])
    tcounts = np.array( ifd[-1]["TileByteCounts"])
    tsize   = np.array([ifd[-1]["TileWidth"  ][0],
                        ifd[-1]["TileLength" ][0]])
    imgsize = np.array([ifd[-1]["ImageLength"][0],
                        ifd[-1]["ImageWidth" ][0]])
    pint    = ifd[-1]["PhotometricInterpretation"][0]

    # Padding bytes aquition
    byte_pad = calc_padding(toffset,tcounts)

    # Calclate lat,lon,pixel roi range of image
    latlim,lonlim,latpix,lonpix,ppu = get_latlon_pos(ifd,geoj,imgsize,proj_params,loff)

    # Calclate parameters about tiles
    tpos_x,tpos_y,tidx,gidx = get_tiles_pos(latpix,lonpix,imgsize,tsize)

    # Data aquisition by horizontal tile group
    for i in range(max(gidx)+1):

        # Get horizontal tiles
        img_tmp1 = get_tiles(session,fname,ifd[-1],tidx,gidx,i,byte_pad)
        
        # Append horizontal tile group
        if i == 0:
            img = np.array(img_tmp1)
        else:
            img = np.append(img,img_tmp1,axis=0)

    # Reshape 3D stacked tiles to 2D image
    img = reshape_tiles(img,tpos_x,tpos_y)

    # Extract ROI area in image
    lat_pix_ROI = np.array(latpix-tsize[0]*(tpos_x[0]-1),dtype = int)
    lon_pix_ROI = np.array(lonpix-tsize[1]*(tpos_y[0]-1),dtype = int)
    img         = img[lat_pix_ROI[0]:lat_pix_ROI[1]+1,
                      lon_pix_ROI[0]:lon_pix_ROI[1]+1]

    # Apply colormap if PhotoInterp == 3
    if pint == 3:

        # Convert color map
        cmap_tmp = conv_cmap(ifd[-1]["ColorMap"])

        # Paletted RGB image (visual), no color map
        if roles != "data":
            img = apply_palette(img,cmap_tmp)

    # Convert digital number to physical values
    img = dn2physical(img,r_params,roles,pint)

    # Image showing for test
    #import matplotlib.pyplot as plt
    #plt.imshow(img)
    #plt.show()

    # Set raster class
    raster = Raster(img,latlim,lonlim,ppu,pint)

    # Output
    return raster