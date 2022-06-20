#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
from ..collection.bounds.intersect import bbox as intersect_bbox

#----------------------------------------------------------------------------------------
# match : match images
#----------------------------------------------------------------------------------------
def match_images(data,mask,decimals):

    # Set input
    imgs         = data.img
    imgs_latlim  = data.latlim[0]
    imgs_lonlim  = data.lonlim[0]
    masks        = mask.img
    masks_latlim = mask.latlim[0]
    masks_lonlim = mask.lonlim[0]

    # Check samples per pixel
    if masks.shape[3] != 1:
        message0 = f"mask_shape : {masks.shape}"
        raise Exception("Error! masks samples per pixel must to be one!\n"+message0)

    # Check intersect
    imgs_bbox  = [  imgs_lonlim[0], imgs_latlim[0], imgs_lonlim[1], imgs_latlim[1]]
    masks_bbox = [[masks_lonlim[0],masks_latlim[0],masks_lonlim[1],masks_latlim[1]]]
    id = intersect_bbox(imgs_bbox,masks_bbox)

    # Error if not intersect
    if id[0] == False:
        raise Exception("Error! images and masks dont have overlap area!")

    # Overlapped area's lat,lon
    latlim = np.sort(np.ravel([masks_latlim,imgs_latlim]))[1:3]
    lonlim = np.sort(np.ravel([masks_lonlim,imgs_lonlim]))[1:3]

    # Detect image's lat,lon pixcel area, shape
    imgs_ovr_shape , imgs_ovr_lat_pix, imgs_ovr_lon_pix = extract(imgs , imgs_latlim, imgs_lonlim,latlim,lonlim,decimals)
    masks_ovr_shape,masks_ovr_lat_pix,masks_ovr_lon_pix = extract(masks,masks_latlim,masks_lonlim,latlim,lonlim,decimals)

    # Mask area's lon,lat

    # (1) No reshape
    if imgs_ovr_shape == masks_ovr_shape:

        # New mask initialize
        if masks[0].dtype == "float32":
            fillvalue = np.nan
        else:
            fillvalue = 0
        masks_new_shape = tuple([np.array(masks).shape[0]])+np.array(imgs).shape[1:3]+tuple([1])
        masks_new = np.full(masks_new_shape,fillvalue,masks[0].dtype)

        # Allocation
        masks = np.array(masks)
        for i in range(len(masks)):
            masks_tmp = masks[i,masks_ovr_lat_pix[0]:masks_ovr_lat_pix[1]+1,
                                masks_ovr_lon_pix[0]:masks_ovr_lon_pix[1]+1]
            masks_new[i,imgs_ovr_lat_pix[0]:imgs_ovr_lat_pix[1]+1,
                        imgs_ovr_lon_pix[0]:imgs_ovr_lon_pix[1]+1] = masks_tmp

    # (2) Need reshape
    else:
        raise Exception("Error! image and mask resolution must be same!")

    # Output
    return masks_new

#----------------------------------------------------------------------------------------
# extract : extract lat,lon pixels information
#----------------------------------------------------------------------------------------
def extract(imgs,imgs_latlim,imgs_lonlim,latlim,lonlim,decimals):

    # Detect image's lat,lon pixcel area, shape
    imgs_shape  = np.array(imgs).shape
    imgs_ddeg   = np.array([imgs_latlim[1]-imgs_latlim[0],
                            imgs_lonlim[1]-imgs_lonlim[0]])/imgs_shape[1:3]
    imgs_lat    = np.round(np.linspace(imgs_latlim[1]-imgs_ddeg[0]/2,
                                       imgs_latlim[0]+imgs_ddeg[0]/2,imgs_shape[1]),decimals=decimals)
    imgs_lon    = np.round(np.linspace(imgs_lonlim[0]+imgs_ddeg[1]/2,
                                       imgs_lonlim[1]-imgs_ddeg[1]/2,imgs_shape[2]),decimals=decimals)
    pix_lat_tmp = (latlim[0] < imgs_lat ) & (imgs_lat < latlim[1])
    pix_lat     = [np.min(np.where(pix_lat_tmp == True)),
                   np.max(np.where(pix_lat_tmp == True))]
    pix_lon_tmp = (lonlim[0] < imgs_lon ) & (imgs_lon < lonlim[1])
    pix_lon     = [np.min(np.where(pix_lon_tmp == True)),
                   np.max(np.where(pix_lon_tmp == True))]
    ovr_shape   = (pix_lat[1]-pix_lat[0]+1,pix_lon[1]-pix_lon[0]+1)

    # Output
    return ovr_shape,pix_lat,pix_lon