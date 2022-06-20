#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
from PIL import Image

#----------------------------------------------------------------------------------------
# apply_palette
#----------------------------------------------------------------------------------------
def apply_palette(img_in,color_map):

    # Change dimension (3d to 2d)
    img_tmp = img_in.reshape(img_in.shape[0:2])

    # Grayscale to RGB numpy array
    img_tmp = Image.fromarray(img_tmp, mode="P")
    img_tmp.putpalette(color_map)
    img_out = np.array(img_tmp.convert("RGB"))

    # Output
    return img_out

#----------------------------------------------------------------------------------------
# conv_cmap
#----------------------------------------------------------------------------------------
def conv_cmap(cmap_in):
    
    cmap_out = list(np.array(cmap_in).reshape([3,-1]).T.flatten())
    return cmap_out