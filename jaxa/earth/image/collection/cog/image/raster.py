# --------------------------------------------------------------------------------
# Load module
# --------------------------------------------------------------------------------
import numpy as np

# --------------------------------------------------------------------------------
# Raster class
# --------------------------------------------------------------------------------
class Raster:

    # ----------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------
    def __init__(self,img,latlim,lonlim,ppu,pint):

        # Set data
        self.img    = [img]
        self.latlim = np.array([latlim])
        self.lonlim = np.array([lonlim])
        self.ppu    = ppu
        self.pint   = pint

    # ----------------------------------------------------------------------------
    # append (img is "list" because the type can append different size array)
    # ----------------------------------------------------------------------------
    def append(self,raster):

        # Append img, latlim, lonlim
        self.img.extend(raster.img)
        self.latlim = np.append(self.latlim, raster.latlim, axis=0)
        self.lonlim = np.append(self.lonlim, raster.lonlim, axis=0)

        # Return
        return self

    # ----------------------------------------------------------------------------
    # to_numpy
    # ----------------------------------------------------------------------------
    def to_numpy(self):

        # Append img, latlim, lonlim
        self.img = np.array(self.img)

        # Return
        return self

    # ----------------------------------------------------------------------------
    # calc_latlon_range
    # ----------------------------------------------------------------------------
    def calc_latlon_range(self):

        # Calc min, max
        self.latlim = np.array([[min(self.latlim[:,0]),max(self.latlim[:,1])]])
        self.lonlim = np.array([[min(self.lonlim[:,0]),max(self.lonlim[:,1])]])

        # Return
        return self

