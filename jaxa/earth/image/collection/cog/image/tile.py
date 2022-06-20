#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
from ..bin      import bin2img
from .....utils import get

#----------------------------------------------------------------------------------------
# calc_padding : Calculate padding bytes
#----------------------------------------------------------------------------------------
def calc_padding(toffset,tcounts):

    # Calc byte padding (0 or 8)
    if len(toffset) == 1:
        byte_pad = int(0)
    else:
        offset0  = toffset[0:-1:]
        offset1  = toffset[1:   ]
        tcount0  = tcounts[0:-1:]
        byte_pad = int((offset1-offset0-tcount0).mean())

    # Output
    return byte_pad

#----------------------------------------------------------------------------------------
# get_tiles_pos : Caluculate parameters about tiles
#----------------------------------------------------------------------------------------
def get_tiles_pos(latpix,lonpix,imgsize,Tsize):

    # Calculate number of tiles, positition
    tnum   = np.ceil(imgsize/Tsize)
    tpos_x = np.floor(latpix/Tsize[0])+1
    tpos_y = np.floor(lonpix/Tsize[1])+1
    y,x    = np.meshgrid(list(range(int(tpos_y[0]),int(tpos_y[1])+1)),\
                         list(range(int(tpos_x[0]),int(tpos_x[1])+1)))
    x      = np.ravel(x)
    y      = np.ravel(y)
    tidx   = np.ravel(tnum[1]*(x-1)+y)-1

    # Index's initirazation
    #x0  = x-min(x)
    #x0  = y-min(y)

    # Append horizontal bytes range to reduce query
    gidx  = []
    dtnum = np.append(1,tidx[1:]-tidx[0:-1])
    for i in range(len(tidx)):
        if i == 0:
            gidx.append(0)
        else:
            if dtnum[i] > 1:
                gidx.append(gidx[i-1]+1)
            else:
                gidx.append(gidx[i-1])
    gidx = np.array(gidx)

    # Change datatype to uint
    tidx = tidx.astype(np.uint32)
    gidx = gidx.astype(np.uint32)
 
    # Output
    return tpos_x,tpos_y,tidx,gidx

#----------------------------------------------------------------------------------------
# get_tiles : get horizotal tiles data
#----------------------------------------------------------------------------------------
def get_tiles(session,fname,ifd,tidx,gidx,i,byte_pad):

    # Set Parameters
    twidth  = ifd["TileWidth" ][0]
    tlength = ifd["TileLength"][0]    
    toffset = np.array(ifd["TileOffsets"   ])
    tcounts = np.array(ifd["TileByteCounts"])    

    # Each horizontal tile group's index
    j1 = min(np.where(gidx == i)[0])
    j2 = max(np.where(gidx == i)[0])

    # Padding bytes addition due to padding
    byte_add_tmp = byte_pad*(j2-j1+1)

    # Extract bytes range
    bytes0 = toffset[tidx[j1]]
    bytes1 = bytes0 + sum(tcounts[tidx[j1:j2+1]])-1 + byte_add_tmp

    # Get horizontal tile group binary
    bin = get.range(session,fname,bytes0,bytes1) 

    # Devide and Decompress, Append each tiles
    for j in range(j1,j2+1) :

        # Set start, end position of binary
        bstart = toffset[tidx[j]]-bytes0
        bend   = bstart+tcounts[tidx[j]]

        # Convert binary to image
        img_tmp0 = bin2img(bin[bstart:bend+1],ifd,twidth,tlength)

        # Append image
        if j == j1:
            img_tmp1 = [img_tmp0]
        else:
            img_tmp1 = np.append(img_tmp1,[img_tmp0],axis=0)

    # Output
    return img_tmp1

#----------------------------------------------------------------------------------------
# reshape_tiles : Reshape stacked tile to 2d image
#----------------------------------------------------------------------------------------
def reshape_tiles(img_in,tpos_x,tpos_y):

    # Get tile x,y number
    tile_num = np.array([tpos_x[1]-tpos_x[0]+1,
                         tpos_y[1]-tpos_y[0]+1],dtype=int)

    # Stack tiles to 2d image
    for i in range(tile_num[0]):
        img_tmp = np.concatenate(img_in[tile_num[1]*i:tile_num[1]*(i+1)],axis=1)
        if i==0:
            img_out = img_tmp
        else:
            img_out = np.concatenate([img_out,img_tmp],axis=0)

    # Output
    return img_out
