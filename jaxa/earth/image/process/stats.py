#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
import warnings

#----------------------------------------------------------------------------------------
# composite : simple composite
#----------------------------------------------------------------------------------------
def composite(img_in,method):

    # Set warning ignore (RuntimeWarning: Mean of empty slice)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)

        # Execute composite
        if method   == "mean":
            img_out = np.nanmean(img_in,axis=0)
        elif method == "std":
            img_out = np.nanstd(img_in,axis=0)
        elif method == "min":
            img_out = np.nanmin(img_in,axis=0)
        elif method == "max":
            img_out = np.nanmax(img_in,axis=0)
        elif method == "median":
            img_out = np.nanmedian(img_in,axis=0)

    # Output
    return np.array([img_out])

#----------------------------------------------------------------------------------------
# timeseries
#----------------------------------------------------------------------------------------
def timeseries(img):

    # Reshape
    img_shape = np.array(img).shape
    img_1d    = np.array(img).reshape(img_shape[0],img_shape[1]*img_shape[2],img_shape[3])

    # Set warning ignore (RuntimeWarning: Mean of empty slice)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)

        # Execute composite
        data = {"mean"  : np.nanmean(  img_1d,axis=1),
                "std"   : np.nanstd(   img_1d,axis=1),
                "min"   : np.nanmin(   img_1d,axis=1),
                "max"   : np.nanmax(   img_1d,axis=1),
                "median": np.nanmedian(img_1d,axis=1)}

    # Output
    return data