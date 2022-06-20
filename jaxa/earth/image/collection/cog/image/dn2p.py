# ----------------------------------------------------------------------------------------
# Load module
# ----------------------------------------------------------------------------------------
import numpy as np

# ----------------------------------------------------------------------------------------
# dn2physical : Convert digital number image to physical value image
# ----------------------------------------------------------------------------------------
def dn2physical(img_in, r_params, roles, photo_interp):

    # roles : data (float)
    if (roles == "data") and (photo_interp == 1):

        # Get parameters
        slope, offset, dn_min, dn_max, dn_nodata, dn_err = get_params(r_params)

        # Apply parameters
        img_out = apply_params(img_in, slope, offset,
                               dn_min, dn_max, dn_nodata, dn_err)

    # roles : visual, data_mask, and so on
    else:
        img_out = img_in

    # Output
    return img_out

# ----------------------------------------------------------------------------------------
# apply_params
# ----------------------------------------------------------------------------------------
def apply_params(img_in, slope, offset, dn_min, dn_max, dn_nodata, dn_err):

    # Datatype conversion
    img_out = img_in.astype(dtype="float32")

    # Apply slope, offset
    img_out = img_out*slope + offset

    # In case of beyond min,max
    if (dn_min != None) & (dn_max != None):
        img_out[(img_in < dn_min) | (dn_max < img_in)] = np.nan

    # In case of nodata value
    if dn_nodata != None:
        img_out[img_in == dn_nodata] = np.nan

    # In case of error value (multiple)

    # Output
    return img_out

# ----------------------------------------------------------------------------------------
# get_params
# ----------------------------------------------------------------------------------------
def get_params(params):

    # (1) slope
    if "slope" in params["dn2value"]:
        slope = params["dn2value"]["slope"]
    else:
        slope = 1

    # (2) offset
    if "offset" in params["dn2value"]:
        offset = params["dn2value"]["offset"]
    else:
        offset = 0

    # (3) dn_min
    if "min" in params["dn"]:
        dn_min = params["dn"]["min"]
    else:
        dn_min = None

    # (4) dn_max
    if "max" in params["dn"]:
        dn_max = params["dn"]["max"]
    else:
        dn_max = None

    # (4) dn_err
    if "nodata" in params["dn"]:
        dn_nodata = params["dn"]["nodata"]
    else:
        dn_nodata = None

    # (5) dn_err
    if "error" in params["dn"]:
        dn_err = params["dn"]["error"]
    else:
        dn_err = None

    # Output
    return slope, offset, dn_min, dn_max, dn_nodata, dn_err
