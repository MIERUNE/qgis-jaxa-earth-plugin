#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
from PIL import Image

#----------------------------------------------------------------------------------------
# apply_palette
#----------------------------------------------------------------------------------------
def apply_palette(img_in,color_map_in):

    # Change dimension (3d to 2d)
    img_tmp = img_in.reshape(img_in.shape[0:2])

    # If colormap is 16bit, reduce it to 8 bit
    if max(color_map_in) > 255:
        color_map = [i >> 8 for i in color_map_in]
    else:
        color_map = color_map_in

    # Grayscale to RGB numpy array
    img_tmp = Image.fromarray(img_tmp, mode="P")
    img_tmp.putpalette(color_map)
    img_out3 = np.array(img_tmp.convert("RGB"))

    # Add alpha channel
    img_tmp = np.zeros(img_out3.shape[0:2], dtype=np.uint8)
    img_tmp[np.sum(img_out3,axis=2) > 0] = 255
    img_out = np.dstack([img_out3,img_tmp])

    # Showing image (for test)
    #import matplotlib.pyplot as plt
    #plt.imshow(img_out)
    #plt.show()

    # Output
    return img_out

#----------------------------------------------------------------------------------------
# conv_cmap
#----------------------------------------------------------------------------------------
def conv_cmap(cmap_in):
    
    cmap_out = list(np.array(cmap_in).reshape([3,-1]).T.flatten())
    return cmap_out