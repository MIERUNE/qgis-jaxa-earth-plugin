# --------------------------------------------------------------------------------
# Setting parameters class
# --------------------------------------------------------------------------------
class Settings:

    # Default SSL Verify settings
    ssl_verify = True

    # STAC URL (COG)
    stac_cog_url = "https://data.earth.jaxa.jp/stac/cog/v1/catalog.json"

    # Parameters about collection
    col_default  = "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global"

    # Parameters about date
    dlim_default = ["2021-01-01T00:00:00",
                    "2021-12-31T23:59:59"]
    date_num_max = 100 # Maximum date number 

    # Default ppu, bounds is determined depend on projection

    # Parameters about band
    band_default = "DSM"

    # Image processing, showing parameters
    pixels_max     = 3000**2
    first_get_byte = 65535

# --------------------------------------------------------------------------------
# ColorMap class
# --------------------------------------------------------------------------------
class ColorMap:

    # Default color map
    default  = "turbo"

    # Color map list
    turbo    = ["#31133D","#4663D8","#35ABF8","#1AE4B6","#72FE5E",
                "#C8EF34","#FABA39","#F66C19","#CB2B04","#7B0403"]
    ndvi     = ["#9C7810","#E8C34D","#E9EF57","#C4FF46","#8FFF2A",
                "#5AE90F","#31C500","#199800","#0F6800","#2E2E2E"]
    spectral = ["#2b83ba","#abdda4","#ffffbf","#fdae61","#d7191c"]
