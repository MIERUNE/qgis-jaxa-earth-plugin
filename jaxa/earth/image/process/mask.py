#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import math
import numpy as np

#----------------------------------------------------------------------------------------
# mask : simple mask
#----------------------------------------------------------------------------------------
def mask_images(img,mask,type_query,values):

    # Check input
    # 1. Image
    img_shape  = img.shape
    mask_shape = mask.shape
    if img_shape[1:3] != mask_shape[1:3]:
        message0 = f"img_shape : {  img_shape}\n"
        message1 = f"mask_shape : {mask_shape}"
        raise Exception("Error! image shape and mask shape is not match!\n"+message0+message1)
    if (mask_shape[0] != 1) and (img_shape[0] != mask_shape[0]):
        message0 = f"img_shape : {  img_shape}\n"
        message1 = f"mask_shape : {mask_shape}"
        raise Exception("Error! Mask shape time size must be 1 or same as image shape!\n"+message0+message1)
    if mask_shape[3] != 1:
        message0 = f"img_shape : {  img_shape}\n"
        message1 = f"mask_shape : {mask_shape}"
        raise Exception("Error! Mask shape depth must be 1!\n"+message0+message1)      

    # 2. Type
    type_all  = ["range","values_equal","bits_equal"]
    mask_type = [s for s in type_all if type_query in s]
    if len(mask_type) == 0:
        message0 = f"requested type : {type_query}"
        raise Exception("Error! requested type is not inpremented !\n"+message0)
    
    # 3. Value
    if type(values) != list:
        message0 = f"Inputed values type : {type(values)}"
        raise Exception("Error! only list object will be allowed to input !\n"+message0)
    elif type_query == "range":
        if len(values) !=2:
            message0 = f"Inputed values length : {len(values)}"
            raise Exception("Error! range type require only two values !")

    # Time series processing
    img_out = []
    for i_date in range(len(img)):

        # Detect mask's depth
        if len(mask) == 1:
            i_mask = 0
        else:
            i_mask = i_date

        # Execute mask
        if   mask_type[0] == "range":
            img_out.append(mask_range(img[i_date],mask[i_mask],values))        
        elif mask_type[0] == "values_equal":
            img_out.append(mask_value(img[i_date],mask[i_mask],values))
        elif mask_type[0] == "bits_equal":
            img_out.append(mask_bit(  img[i_date],mask[i_mask],values))

    # Output
    return img

#----------------------------------------------------------------------------------------
# mask_range : simple value mask
#----------------------------------------------------------------------------------------
def mask_range(img,mask,values):

    # Extract requested range values
    img_ok = np.full(mask.shape,False)
    img_ok = (values[0] <= mask) & (mask <= values[1])

    # Apply mask
    img_out = mask_apply(img,img_ok)
        
    # Output
    return img_out

#----------------------------------------------------------------------------------------
# mask_value : simple value mask
#----------------------------------------------------------------------------------------
def mask_value(img,mask,values):

    # Extract requested values (OR)
    img_ok = np.full(mask.shape,False)
    for i in range(len(values)):
        img_ok_tmp = mask == values[i]
        img_ok = img_ok | img_ok_tmp

    # Apply mask
    img_out = mask_apply(img,img_ok)

    # Output
    return img_out

#----------------------------------------------------------------------------------------
# mask_bit : simple bit mask
#----------------------------------------------------------------------------------------
def mask_bit(img,mask,values):

    # Check values
    bitmax = math.log2(np.iinfo(mask.dtype).max -\
                       np.iinfo(mask.dtype).min + 1)
    bitlen = len(values)
    if bitlen > bitmax:
        raise Exception("Error! inputed bit depth is beyond mask data!")
    if mask.dtype == "float32":
        raise Exception("Error! can not execute float data as bit mask!")

    # Calc bit caluclation
    #   1  : 1 data is OK
    #   0  : 0 data is OK
    # None : Not masked
    img_ok = np.full(mask.shape,True)
    for i in range(bitlen):
        if values[i] != None:

            # Check single value
            if (values[i] != 1) and (values[i] != 0):
                raise Exception("Error! only 0 or 1 is allowed to input!")

            # Get i value 2^n
            bitvalue = 2**i

            # Bit caluculation (AND)
            bitmat     = np.full(mask.shape,bitvalue)
            img_ok_tmp = mask & bitmat
            img_ok_tmp = img_ok_tmp.astype(dtype=bool)

            # Flip true/false in case of 0
            if values[i] == 0:
                img_ok_tmp = np.logical_not(img_ok_tmp)

            # Apply mask (AND)
            img_ok = img_ok & img_ok_tmp

    # Apply mask
    img_out = mask_apply(img,img_ok)    

    # output
    return img_out

#----------------------------------------------------------------------------------------
# mask_apply : apply mask
#----------------------------------------------------------------------------------------
def mask_apply(img_in,img_ok):

    # Duplicate mask depth(1) to img depth(N=1,3)
    depth  = img_in.shape[2]
    img_ok = np.repeat(img_ok,depth,axis=2)

    # Apply value mask (false to NaN or zero)
    img_out = img_in
    if img_in.dtype == "float32":
        img_out[~img_ok] = np.nan
    else:
        img_out[~img_ok] = 0

    #import matplotlib.pyplot as plt
    #plt.imshow(self.image[0])
    #plt.show()

    # Output
    return img_out