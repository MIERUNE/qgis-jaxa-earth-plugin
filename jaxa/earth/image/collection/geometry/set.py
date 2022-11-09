# --------------------------------------------------------------------------------
# Projection parameters class
# --------------------------------------------------------------------------------
class Projections:

    # ----------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------
    def __init__(self,epsg=4326):

        # ------------------------------------------------------------------------
        # Polar steleo projection : South (EPSG:3031)
        # ------------------------------------------------------------------------        
        if epsg == 3031:

            # EPSG
            self.epsg = 3031

            # COG levels, PPU list (pixels per 32768 = 2**15 m)
            self.levels = [[0,0,0,1, 1, 1, 2,  2,  2],\
                           [1,2,4,8,16,32,64,128,256]]
            
            # ppu,unit
            self.ppu_default     = 1
            self.ppu_max_default = 128
            self.unit            = 32768
            self.unit_str        = "m"

            # Rounding decimals
            self.r_dec_bbox = 0
            self.r_dec_pix  = 0

            # latitude
            self.lat_range_max = [-2**23,2**23]
            self.lat_str_len   = 8
            self.lat_plus_str  = "P"
            self.lat_minus_str = "M"
            self.lat_min_width = 256
            self.lat_label_str = "Y-axis [m]"

            # longitude
            self.lon_range_max = [-2**23,2**23]
            self.lon_str_len   = 8
            self.lon_plus_str  = "P"
            self.lon_minus_str = "M"            
            self.lon_min_width = 256
            self.lon_label_str = "X-axis [m]"

        # ------------------------------------------------------------------------
        # Polar steleo projection : North (EPSG:3995)
        # ------------------------------------------------------------------------        
        if epsg == 3995:

            # EPSG
            self.epsg = 3995

            # COG levels, PPU list (pixels per 32768 = 2**15 m)
            self.levels = [[0,0,0,1, 1, 1, 2,  2,  2],\
                           [1,2,4,8,16,32,64,128,256]]
            
            # ppu,unit
            self.ppu_default     = 1
            self.ppu_max_default = 128
            self.unit            = 32768
            self.unit_str        = "m"

            # Rounding decimals
            self.r_dec_bbox = 0
            self.r_dec_pix  = 0

            # latitude
            self.lat_range_max = [-2**23,2**23]
            self.lat_str_len   = 8
            self.lat_plus_str  = "P"
            self.lat_minus_str = "M"
            self.lat_min_width = 256
            self.lat_label_str = "Y-axis [m]"

            # longitude
            self.lon_range_max = [-2**23,2**23]
            self.lon_str_len   = 8
            self.lon_plus_str  = "P"
            self.lon_minus_str = "M"            
            self.lon_min_width = 256
            self.lon_label_str = "X-axis [m]"

        # ------------------------------------------------------------------------
        # EQR projection (EPSG:4326, default)
        # ------------------------------------------------------------------------
        elif epsg == 4326:

            # EPSG
            self.epsg = 4326

            # COG levels, PPU list (pixels per degree)
            self.levels = [[   0,  0, 0, 1, 1, 1, 2,  2,  2,  3,   3,   3],\
                           [1.25,2.5, 5,10,20,40,90,180,360,900,1800,3600]] 

            # ppu, unit
            self.ppu_default     = 1.25
            self.ppu_max_default = 3600
            self.unit            = 1
            self.unit_str        = "degree"

            # Rounding decimals
            self.r_dec_bbox = 2
            self.r_dec_pix  = 7

            # latitude
            self.lat_range_max = [ -90, 90]
            self.lat_str_len   = 6
            self.lat_plus_str  = "N"
            self.lat_minus_str = "S"
            self.lat_min_width = 0.01
            self.lat_label_str = "Latitude [deg]"

            # longitude
            self.lon_range_max = [-360,360]
            self.lon_str_len   = 7
            self.lon_plus_str  = "E"
            self.lon_minus_str = "W"
            self.lon_min_width = 0.01
            self.lon_label_str = "Longitude [deg]"
        
