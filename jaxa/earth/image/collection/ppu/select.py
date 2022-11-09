#--------------------------------------------------------------------------------
# Load module
#--------------------------------------------------------------------------------
import sys
import numpy as np
from ..geometry.set import Projections
from ..stac.select import get_all_children

#--------------------------------------------------------------------------------
# select_multiple_dates_bounds_url
#--------------------------------------------------------------------------------
def select_multiple_dates_ppu_url(input,ppu):

    # Get proj param, ppu params
    summaries = input.stac_collection.json[0][0]["summaries"]
    proj_params,user_ppu,ppu_max = select_ppu_params(ppu,summaries)

    # Detect nearest PPU URL
    stac_ppu_url_tmp = []
    for i in range(len(input.stac_date.url)):
        url_date_tmp = get_all_children(input._session, "child", input.stac_date.url[i][0], input.stac_date.json[i][0])
        stac_ppu_url_tmp.append(select_ppu(url_date_tmp, user_ppu, ppu_max, proj_params))

    # Check all PPU and URL (unify to single ppu)
    stac_ppu_url_tmp, date_idx = check_selected_ppu(stac_ppu_url_tmp)

    # Output
    return stac_ppu_url_tmp,date_idx,user_ppu, proj_params

#--------------------------------------------------------------------------------
# select_ppu_params
#--------------------------------------------------------------------------------
def select_ppu_params(ppu,summaries):

    # Get projection number, parameter
    if "proj:epsg" in summaries:
        proj = summaries["proj:epsg"]
    elif "je:epsg" in summaries:
        proj = summaries["je:epsg"][0]
    else:
        proj = Projections().epsg
    proj_params = Projections(proj)

    # Initialize ppu if no input
    if ppu is None:
        if "qgis.utils" in sys.modules:
            user_ppu = select_ppu_qgis(proj_params)
        else:
            user_ppu = proj_params.ppu_default
    else:
        user_ppu = ppu

    # Set PPUMAX
    if "je:ppu_max" in summaries:
        ppu_max_raw = summaries["je:ppu_max"]
        
        # Detect date format type
        if   type(ppu_max_raw) == list:
            ppu_max = ppu_max_raw[0]
        elif (type(ppu_max_raw) == int) or (type(ppu_max_raw) == float) :
            ppu_max = ppu_max_raw

    else:
        ppu_max = proj_params.ppu_max_default

    # Output
    return proj_params,user_ppu,ppu_max

#--------------------------------------------------------------------------------
# select_ppu
#--------------------------------------------------------------------------------
def select_ppu(URL,ppu_user,ppu_max,proj_params):

    # COG level, PPU(Pixels Per Unit) list
    levels = np.array(proj_params.levels)

    # Delete number which Exceed PPUMAX
    if ppu_max is not None:
        idx_del = np.where(levels[1] > ppu_max)
        levels  = np.delete(levels,idx_del,axis=1)

    # Detect each files COG,IFD level
    cog_lev     = []
    cog_ifd_lev = []
    cog_ifd_ppu = []
    score       = []
    for i in range(len(URL)):

        # Calculate temporal value (COG,ifd)
        cog_lev_tmp = int(URL[i][-14:-13])
        cog_ppu_tmp = levels[1][levels[0] == cog_lev_tmp]
        ifd_lev_tmp = range(len(cog_ppu_tmp)-1,-1,-1)   

        # Check empty
        if len(cog_ppu_tmp) != 0:

            # Select best index
            IDX_best  = abs(cog_ppu_tmp-ppu_user).argmin()
            score_tmp = abs(cog_ppu_tmp-ppu_user).min()

            # Append best value
            cog_lev.append(cog_lev_tmp)
            cog_ifd_lev.append(ifd_lev_tmp[IDX_best])
            cog_ifd_ppu.append(cog_ppu_tmp[IDX_best])
            score.append(score_tmp)

    # Select best resolution's file
    idx_file_best = np.array(score).argmin()
    URL_PPD       = URL[              idx_file_best]
    cog_lev       = int(  cog_lev[    idx_file_best])
    cog_ifd_lev   = int(  cog_ifd_lev[idx_file_best])
    cog_ifd_ppu   = float(cog_ifd_ppu[idx_file_best])

    # Output
    return [URL_PPD, cog_lev, cog_ifd_lev, cog_ifd_ppu]

#--------------------------------------------------------------------------------
# check_selected_ppu
#--------------------------------------------------------------------------------
def check_selected_ppu(stac_url_list):

    # Convert to numpy array(url,cog level,ifd level, ifd ppu)
    stac_url_list = np.array(stac_url_list,dtype="object")

    # Detect maximum ppu (multiple)
    tmp = stac_url_list[:,3]
    idx_max = [i for i, x in enumerate(tmp) if x == max(tmp)]

    # Output
    return stac_url_list[idx_max,:].tolist(),idx_max

#--------------------------------------------------------------------------------
# select_ppu_qgis
#--------------------------------------------------------------------------------
def select_ppu_qgis(proj_params):

    # Load module
    from qgis.core import QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsProject
    import qgis.utils

    # Get extent on QGIS crs
    extent = qgis.utils.iface.mapCanvas().extent()    

    # Get display size pixel
    upp    = qgis.utils.iface.mapCanvas().mapUnitsPerPixel()
    pix_width  = extent.width()/upp
    pix_height = extent.height()/upp

    # Transform crs to EPSG4326
    source_crs = qgis.utils.iface.mapCanvas().mapSettings().destinationCrs()
    dest_crs   = QgsCoordinateReferenceSystem()
    dest_crs.createFromSrid(proj_params.epsg)
    rtrans     = QgsCoordinateTransform(source_crs,dest_crs,QgsProject.instance())
    extent_out = rtrans.transformBoundingBox(extent)

    # Get PPU
    ppu_w = proj_params.unit*pix_width/extent_out.width()
    ppu_h = proj_params.unit*pix_height/extent_out.height()
    ppu   = round((ppu_w+ppu_h)/2,1)

    # Output
    return ppu