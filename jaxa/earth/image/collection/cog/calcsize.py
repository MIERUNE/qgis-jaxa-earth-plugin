#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np

#----------------------------------------------------------------------------------------
# calcsize : Calculate cog image size, and throw error if too large size
#----------------------------------------------------------------------------------------
def calc_img_size(feat_cogs,feat_query,ifd_ppu,img_ppu,PIX_NUM_MAX,proj_params,loffsets):

    # Check ppu (request ppu vs cog ppu)
    if abs(ifd_ppu-img_ppu) < 1:
        selected_ppu = ifd_ppu
    else:
        selected_ppu = img_ppu
        pix_str  = f"{selected_ppu} pixels"
        unit_str = f"{proj_params.unit} {proj_params.unit_str} per"
        print(" - Resolution (changed) : "+unit_str+pix_str)

    # Set params
    unit     = proj_params.unit
    decimals = proj_params.r_dec_pix
    res      = unit/selected_ppu

    # Calclate all COG's bbox's lat, lon
    lat,lon,bbox_each = calc_all_latlon(feat_cogs,res,decimals,loffsets)

    # Calc query area's pixels position
    imgsize_all, pix_x, pix_y = calc_pix_pos(feat_query,lat,lon,bbox_each)

    # Check image size
    check_img_size(imgsize_all,PIX_NUM_MAX)

    # Output imagesize, pixel location
    return imgsize_all,pix_x,pix_y

#----------------------------------------------------------------------------------------
# calc_pix_pos : Calc query area's lat, lon pix positions
#----------------------------------------------------------------------------------------
def calc_pix_pos(feat_query,lat,lon,bbox_each):

    # Get geojson type,lat,lon
    gtype        = feat_query["geometry"]["type"]
    latlim_query = feat_query["bbox"][1::2]
    lonlim_query = feat_query["bbox"][0::2]    

    # Extract query area, calc image size
    lat         = lat[(latlim_query[0] < lat) & (lat < latlim_query[1])]
    lon         = lon[(lonlim_query[0] < lon) & (lon < lonlim_query[1])]
    imgsize_all = [len(lat),len(lon)]

    # Calc each cog file's pixel location
    pix_x = []
    pix_y = []
    for i in range(len(bbox_each)):
        latlim_tmp = bbox_each[i][1::2]
        lonlim_tmp = bbox_each[i][0::2]
        index_x    = np.where((latlim_tmp[0] < lat) & (lat < latlim_tmp[1]))
        index_y    = np.where((lonlim_tmp[0] < lon) & (lon < lonlim_tmp[1]))
        pix_x.append([min(index_x[0]),max(index_x[0])])
        pix_y.append([min(index_y[0]),max(index_y[0])])

    # Output
    return imgsize_all, pix_x, pix_y

#----------------------------------------------------------------------------------------
# calc_all_latlon : Calc all lat, lon of cogs
#----------------------------------------------------------------------------------------
def calc_all_latlon(feat_cogs,res,decimals,loffsets):

    bbox_each = []
    for i in range(len(feat_cogs)):
        for j in range(len(feat_cogs[i])):
            bbox_tmp = feat_cogs[i][j]["bbox"]
            bbox_tmp = [bbox_tmp[0]+loffsets[i][j],bbox_tmp[1],
                        bbox_tmp[2]+loffsets[i][j],bbox_tmp[3]]
            bbox_each.append(bbox_tmp)
    bbox_each = np.array(bbox_each)
    bbox_all  = [min(bbox_each[:,0]),min(bbox_each[:,1]),
                 max(bbox_each[:,2]),max(bbox_each[:,3])]

    # Calc lat,lon array
    latlim_all  = bbox_all[1::2]
    lonlim_all  = bbox_all[0::2]
    latsize_all = int((latlim_all[1]-latlim_all[0])/res)
    lonsize_all = int((lonlim_all[1]-lonlim_all[0])/res)
    lat         = np.round(np.linspace(latlim_all[1]-res/2,
                                       latlim_all[0]+res/2,latsize_all),decimals=decimals)
    lon         = np.round(np.linspace(lonlim_all[0]+res/2,
                                       lonlim_all[1]-res/2,lonsize_all),decimals=decimals)

    # Output
    return lat,lon,bbox_each

#----------------------------------------------------------------------------------------
# check_img_size_rough : Check image size roughly
#----------------------------------------------------------------------------------------
def check_img_size_rough(feat_query,ifd_ppu,PIX_NUM_MAX,proj_params):

    # Set params
    unit = proj_params.unit

    # Get lat,lon
    latlim_g = feat_query["bbox"][1::2]
    lonlim_g = feat_query["bbox"][0::2]

    # Scale factor to ppd
    resolution = unit/ifd_ppu

    # Calc rough img size
    img_size = [round((lonlim_g[1]-lonlim_g[0])/resolution),
                round((latlim_g[1]-latlim_g[0])/resolution)]

    # Error if over PIX_NUM_MAX
    check_img_size(img_size,PIX_NUM_MAX)

#----------------------------------------------------------------------------------------
# check_img_size : Throw error if image size is too large
#----------------------------------------------------------------------------------------
def check_img_size(img_size,PIX_NUM_MAX):
    
    pix_num = img_size[0]*img_size[1]
    if pix_num > PIX_NUM_MAX:
        message0 = f"maximum pix num : {PIX_NUM_MAX}\n"
        message1 = f"requested pix num : {pix_num}\n"
        raise Exception("Error! Requested ppd/LatLon is too large!\n"+message0+message1)