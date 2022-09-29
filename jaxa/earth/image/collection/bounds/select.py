#--------------------------------------------------------------------------------
# Load module
#--------------------------------------------------------------------------------
import numpy as np
from .intersect import line as intersect_line
from ..stac.select import get_all_children

#--------------------------------------------------------------------------------
# select_multiple_dates_bounds_url ： 
#--------------------------------------------------------------------------------
def select_multiple_dates_bounds_url(input,bbox):
    
    # Detect bounds URL
    stac_bounds_url = []
    lon_offset      = []  
    for i in range(len(input.stac_ppu.url)):
        url_date_tmp1 = get_all_children(input._session, "child", input.stac_ppu.url[i][0], input.stac_ppu.json[i][0])
        url_date_tmp2,lon_off_tmp = select_bounds(input._session,url_date_tmp1, bbox, input.proj_params)
        if len(url_date_tmp2) != 0:
            stac_bounds_url.append(url_date_tmp2)
            lon_offset.append(lon_off_tmp)

    # Output
    return stac_bounds_url, lon_offset

#--------------------------------------------------------------------------------
# select_bounds ： 
#--------------------------------------------------------------------------------
def select_bounds(session,URL,bbox,proj_params):

    # Detect each COG's lon range
    lonall = [url2lon(URL[i],proj_params) for i in range(len(URL))]

    # If EPSG4326, set offset
    if proj_params.epsg == 4326:

        # Set lon offset
        LON_OFFSET = 360

        # Set each longitude and offset
        url_idxadd = []
        lon_add    = []
        lon_offadd = []
        for i in range(len(lonall)):
            if (0 <= lonall[i][0]) & (lonall[i][1] <= LON_OFFSET):
                url_idxadd.append(i)
                lon_offadd.append(-LON_OFFSET)
                lon_add.append([lonall[i][0]-LON_OFFSET,lonall[i][1]-LON_OFFSET])
            elif (-LON_OFFSET <= lonall[i][0]) & (lonall[i][1] <= 0):
                url_idxadd.append(i)
                lon_add.append([lonall[i][0]+LON_OFFSET,lonall[i][1]+LON_OFFSET])
                lon_offadd.append( LON_OFFSET)

        # Extend longitude from -360 to +360
        lon_offset = np.zeros(len(URL))
        lon_offset = np.append(lon_offset,lon_offadd)
        lon_ext = lonall
        lon_ext.extend(lon_add)
        url_idx = list(range(0,len(URL),1))
        url_idx.extend(url_idxadd)

    # Other projections (EPSG3995,3031)
    else:
        lon_offset = np.zeros(len(URL))
        lon_ext    = lonall
        url_idx    = list(range(0,len(URL),1))

    # Select child All
    decimals = proj_params.r_dec_pix
    idx = intersect_line(bbox[0::2],lon_ext,decimals)

    # Update URL and offset
    url_tmp0   = np.array(URL)[np.array(url_idx)[idx]]
    lon_offset = lon_offset[idx]

    # Check url_tmp0
    if len(url_tmp0) == 0:
        return []

    # Get URL lat list
    url_tmp2    = []
    lon_off_tmp = []
    for i in range(len(url_tmp0)):
        url_tmp1 = get_all_children(session,"item", url_tmp0[i], [])
        if len(url_tmp1) != 0:
            url_tmp2    = np.append(url_tmp2,url_tmp1,axis=0)
            lon_off_tmp = np.append(lon_off_tmp,np.full(len(url_tmp1),lon_offset[i]))

    # Detect each COG's lat range
    latall = [url2lat(url_tmp2[i],proj_params) for i in range(len(url_tmp2))]

    # Select child All
    idx = intersect_line(bbox[1::2],latall,decimals)

    # Detect json
    url_out     = np.array(url_tmp2)[idx].tolist()
    lon_off_out = lon_off_tmp[idx]

    # Output
    return url_out,lon_off_out

#--------------------------------------------------------------------------------
# url2lon ： 
#--------------------------------------------------------------------------------
def url2lon(URL,proj_params):

    # Set parameters depend on projection
    TYPE_LEN  = len("/catalog.json")
    STR_LEN   = TYPE_LEN+proj_params.lon_str_len*2+1
    LON_PLUS  = proj_params.lon_plus_str
    LON_MINUS = proj_params.lon_minus_str

    # Get lon value
    lon = str2values(URL,TYPE_LEN,STR_LEN,LON_PLUS,LON_MINUS)

    # Output
    return lon

#--------------------------------------------------------------------------------
# url2lat ： 
#--------------------------------------------------------------------------------
def url2lat(URL,proj_params):

    # Set parameters depend on projection
    TYPE_LEN  = len(".json") 
    STR_LEN   = TYPE_LEN+proj_params.lat_str_len*2+1
    LAT_PLUS  = proj_params.lat_plus_str
    LAT_MINUS = proj_params.lat_minus_str

    # Get lon value
    lat = str2values(URL,TYPE_LEN,STR_LEN,LAT_PLUS,LAT_MINUS)

    # Output
    return lat

#--------------------------------------------------------------------------------
# str2values ： 
#--------------------------------------------------------------------------------
def str2values(URL,TYPE_LEN,STR_LEN,PLUS_STR,MINUS_STR):

    # Split each value
    values_str = URL[-STR_LEN:-TYPE_LEN].split("-")

    # Detect lon
    values = []
    for i in range(len(values_str)):
        if   PLUS_STR  in values_str[i]:
            values.append( float(values_str[i][1:]))
        elif MINUS_STR in values_str[i]:
            values.append(-float(values_str[i][1:]))

    # Output
    return values