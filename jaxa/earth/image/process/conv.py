#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
from PIL import Image, ImageDraw

#----------------------------------------------------------------------------------------
# geoj2raster : Convert geojson to raster index
#----------------------------------------------------------------------------------------
def geoj2raster(geoj,raster):

    # Get img size
    img_size_2d = raster.img.shape[1:3]

    # No processing if type is point
    type = geoj["geometry"]["type"]

    # Showing progress
    print(" - ROI mask : ",end="")

    # Get polygon
    polym = geoj["geometry"]["coordinates"]

    # Convert multiple to single polygon
    polys = multi2single(polym)

    # Initialize image
    img  = Image.new('L', img_size_2d[::-1], 0)
    draw = ImageDraw.Draw(img)

    # Aquire polygon data
    for i in range(len(polys)):

        # Convert coordinate's lat,lon to pixel value
        polypix = lonlat2pix(polys[i],img_size_2d,raster.latlim[0],raster.lonlim[0])

        # Draw point () and append
        if (type == "Point") | \
           (type == "MultiPoint"):
             draw.point(polypix, fill=1)

        # Draw line (Convert line's lat,lon to pixel value) and append
        elif (type == "LineString"     ) | \
             (type == "MultiLineString"):
              draw.line(polypix, fill=1, width = 1)

        # Draw polygon (Convert polygon's lat,lon to pixel value) and append
        elif (type == "Polygon"       ) | \
             (type == "MultiPolygon"  ):
              draw.polygon(polypix, outline=1, fill=1)              

    # Mask image
    mask = np.array(img)

    # Delete holes and change to boolean
    index = mask % 2 == 1

    # Showing image (for test)
    #import matplotlib.pyplot as plt
    #plt.imshow(index)
    #plt.show()

    # Reshape img size
    index = np.reshape(index,[1,img_size_2d[0],img_size_2d[1],1])

    # Showing progress
    print("masked")

    # Output
    return index

#----------------------------------------------------------------------------------------
# multi2single : Flatten polygon list
#----------------------------------------------------------------------------------------
def multi2single(poly_in):

    # Get max depth
    ld = depth(poly_in)

    # Change list shape to 3 depend on depth
    if   ld == 4: 
        poly_out =  [poly_in[i][0] for i in range(len(poly_in))]
    elif ld == 3:
        poly_out =   poly_in        
    elif ld == 2: 
        poly_out =  [poly_in]
    elif ld == 1: 
        poly_out = [[poly_in]]

    # Output
    return poly_out

#----------------------------------------------------------------------------------------
# lonlat2pix : Convert lat,lon to pixels
#----------------------------------------------------------------------------------------
def lonlat2pix(poly,imgsize,latlim,lonlim):
    
    # Get polygon's lat,lon
    lon = np.array(poly)[:,0]
    lat = np.array(poly)[:,1]

    # Degree per pixel
    dpp = np.array([lonlim[1]-lonlim[0],latlim[1]-latlim[0]])/imgsize[::-1]

    # Calc pixel position (lat : x, lon : y)
    pix_x = np.array(((latlim[1]-dpp[1]/2)-lat)/dpp[1],dtype="int")
    pix_y = np.array((lon-(lonlim[0]+dpp[0]/2))/dpp[0],dtype="int")

    # Check Difference (to remove same pixel position's data)
    diff_xy = np.append(1,abs(pix_x[1:]-pix_x[:-1])+\
                          abs(pix_y[1:]-pix_y[:-1]))
    idx_ok  = diff_xy != 0

    # Update pix
    pix_x = pix_x[idx_ok]
    pix_y = pix_y[idx_ok]

    # If only one point
    if len(pix_x) == 1:
        pix_x = np.append(pix_x,pix_x)
        pix_y = np.append(pix_y,pix_y)

    # Convert to tuple
    pix = []
    for i in range(len(pix_x)):
        pix.append((pix_y[i],pix_x[i]))

    # Output
    return pix

#----------------------------------------------------------------------------------------
# depth : Calc list's depth
#----------------------------------------------------------------------------------------
def depth(mylist):
    if not mylist:
        return 0
    else:
        if isinstance(mylist,list):
            return 1 + max(depth(i) for i in mylist)
        else:
            return 0

