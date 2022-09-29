#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np

#----------------------------------------------------------------------------------------
# get_latlon_pos : Calculate lat,lon range, pixel location range
#----------------------------------------------------------------------------------------
def get_latlon_pos(ifd,geoj,imgsize,proj_params,loffset):

    # lat,lon range (ifd level 0)
    latlimp = [ifd[0]["ModelTiepointTag"  ][4]-\
               ifd[0]["ModelPixelScaleTag"][1]*ifd[0]["ImageLength"][0],\
               ifd[0]["ModelTiepointTag"  ][4]]
    lonlimp = [ifd[0]["ModelTiepointTag"  ][3],\
               ifd[0]["ModelTiepointTag"  ][3]+\
               ifd[0]["ModelPixelScaleTag"][0]*ifd[0]["ImageWidth" ][0]]

    # Add lon offset
    lonlimp = [lonlimp[0]+loffset,lonlimp[1]+loffset]

    # Set Pixel's Unit
    unit = proj_params.unit

    # Calculate lat,lon vector
    decimals = proj_params.r_dec_pix

    # Lat,lon query limit and geojson type
    lon0,lat0,lon1,lat1 = geoj["bbox"]
    
    # Detect lat,lon query pixel location and range
    lat_lim_q, lat_lim_pix_q = calc_pix_lim(latlimp,imgsize[0],decimals,[lat0,lat1])
    lon_lim_q, lon_lim_pix_q = calc_pix_lim(lonlimp,imgsize[1],decimals,[lon0,lon1])

    # Convert pix number in lattitude direction
    lat_lim_pix_q = imgsize[0]-1-lat_lim_pix_q[::-1]

    # Calc ppu and rounding
    dec_ppu = 2
    ppu     = round(unit*(lat_lim_pix_q[1]-lat_lim_pix_q[0]+1)/(lat_lim_q[1]-lat_lim_q[0]),dec_ppu)

    # Output
    return lat_lim_q,lon_lim_q,lat_lim_pix_q,lon_lim_pix_q,ppu

#----------------------------------------------------------------------------------------
# calc_pix_lim : Detect lat,lon query pixel limit location
#----------------------------------------------------------------------------------------
def calc_pix_lim(data_lim,data_len,decimals,query_lim):
    
    # Calculate data vector
    delta = (data_lim[1]-data_lim[0])/data_len
    data  = np.round(np.linspace(data_lim[0]+delta/2,
                                 data_lim[1]-delta/2,data_len),decimals=decimals)

    # Detect pixel limit location
    data_tmp  = np.where((query_lim[0] < data) & (data < query_lim[1]))
    pix_lim_q = np.array([min(data_tmp[0]),max(data_tmp[0])])

    # Data offset (delta/2)
    data_lim_q = data[pix_lim_q] + np.array([-1,1])*round(delta/2,decimals)

    # Output
    return data_lim_q, pix_lim_q

