#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np

#----------------------------------------------------------------------------------------
# mask : simple mask
#----------------------------------------------------------------------------------------
def diff_images(img,ref):

    # Check input
    img_shape = img.shape
    ref_shape = ref.shape
    if img_shape[1:] != ref_shape[1:]:
        raise Exception("Error! image shape and referenece shape is not match!")
    if (ref_shape[0] != 1) and (img_shape[0] != ref_shape[0]):
        raise Exception("Error! reference shape time size must be 1 or same as image shape!")

    # Duplicate date number to img
    if ref_shape[0] == 1:
        ref = np.repeat(ref,img_shape[0],axis=0)

    # Take difference
    img_out = img - ref

    # Output
    return img_out
