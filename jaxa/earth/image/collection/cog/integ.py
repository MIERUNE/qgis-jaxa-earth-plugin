#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np

#----------------------------------------------------------------------------------------
# integ_img : Convert 3d list to 2d image
#----------------------------------------------------------------------------------------
def integ_img(img_tmp,img_size,pix_x,pix_y,roles):

    # Detect data type
    dtype = img_tmp[0].dtype

    # Detect fill values depend on roles
    if roles == "data":
        fillvalue = np.nan
    else:
        fillvalue = 0

    # Detect img_tmp's depth (z axis)
    depth = len(img_tmp[0][0][0])

    # Initiarize image
    img_size3 = [img_size[0],img_size[1],depth]
    img_out   = np.full(img_size3,fillvalue,dtype=dtype)

    # Allocate images to each position
    for i in range(len(img_tmp)):
        img_out[pix_x[i][0]:pix_x[i][1]+1,
                pix_y[i][0]:pix_y[i][1]+1] = img_tmp[i]
    
    # Output
    return [img_out]