# --------------------------------------------------------------------------------
# Load module
# --------------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
import warnings
from ....params import ColorMap

# --------------------------------------------------------------------------------
# ColorInfo class
# --------------------------------------------------------------------------------
class ColorInfo:

    # ----------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------
    def __init__(self,pint,roles,vinfo,nodata):

        # Set cmin, cmax
        
        # (0) Visual RGB data
        if roles == "visual":
            ctype = None

        # (1) Land cover data
        elif (pint == 3) and (roles == "data"):
            ctype = "exact"

        # (2) Mask or quality data
        elif (pint == 1) and (roles == "data-mask"):
            ctype = "linear"

        # (3) Other physical data
        else:
            ctype = "linear"

        # Output
        self.unit    = vinfo["unit"]
        self._nodata = nodata
        self._ctype  = ctype                
        self._pint   = pint
        self._roles  = roles
        self._vinfo  = vinfo

    # ----------------------------------------------------------------------------
    # set_clim : Set colormap params
    # ----------------------------------------------------------------------------
    def set_clim(self,img):

        # Set cmin, cmax
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
        
            # (0) Visual RGB data
            if self._roles == "visual":
                cmin  = None
                cmax  = None

            # (1) Land cover data
            elif (self._pint == 3) and (self._roles == "data"):
                cmin  = None
                cmax  = None

            # (2) Mask or quality data
            elif (self._pint == 1) and (self._roles == "data-mask"):
                cmin  = np.nanmin(img)
                cmax  = np.nanmax(img)
            
            # (3) Other physical data
            else:
                cmin = np.nanmean(img)-2*np.nanstd(img)
                if cmin < np.nanmin(img):
                   cmin = np.nanmin(img)
                cmax = np.nanmean(img)+2*np.nanstd(img)
                if cmax > np.nanmax(img):
                   cmax = np.nanmax(img) 
    
        # Output
        self.clim = [cmin,cmax]

        # Return
        return self

    # ----------------------------------------------------------------------------
    # set_cmap_params : Set colormap params
    # ----------------------------------------------------------------------------
    def set_cmap_params(self, cmap_name = ColorMap.default):

        # Set land cover labels (not selectable)
        if self._ctype == "exact":
            cmap_params = {"name":"default in tif",
                           "type":self._ctype,
                           "labels":self._vinfo["labels"],
                           "lnames":self._vinfo["lnames"],
                           "nodata":self._nodata}

        # Set values colors
        elif self._ctype == "linear":
            colors = getattr(ColorMap,cmap_name)
            cmap_params = {"name":cmap_name,
                           "type":self._ctype,
                           "colors":colors}

        # Set None (RGB, etc. Not selectable)
        else:
            cmap_params = {"name":None,
                           "type":None,
                           "colors":None,
                           "nodata":self._nodata}

        # Set self
        self.cmap_params = cmap_params

        # Return
        return self

    # ----------------------------------------------------------------------------
    # get_lin_seg_cmap : get linear segmented colormap
    # ----------------------------------------------------------------------------
    def get_lin_seg_cmap(self):

        # Initialization
        cmap = None
        norm = None

        # (1) Make Land cover color value,palette (exact)
        if self.cmap_params["type"] == 'exact':

            # Set palette code and value
            tmp    = self.cmap_params["labels"]
            pcode  = []
            pvalue = []
            for i in range(len(tmp)):
                pcode.append( tmp[i][self._vinfo["lnames"]["color"]])
                pvalue.append(tmp[i][self._vinfo["lnames"]["value"]])

            # Generate colormap
            cmap = mpl.colors.ListedColormap(pcode)
            norm = mpl.colors.BoundaryNorm(pvalue, cmap.N,extend="max")

        # (2) Make physical value color value,palette (linear)
        elif self.cmap_params["type"] == 'linear':

            # Set palette code and value
            pname = self.cmap_params["name"]
            pcode = self.cmap_params["colors"]

            # Generate colormap
            cmap = mpl.colors.LinearSegmentedColormap.from_list(pname,pcode)

        # Output
        return cmap,norm
