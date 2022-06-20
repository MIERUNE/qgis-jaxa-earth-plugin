#--------------------------------------------------------------------------------
# Load module
#--------------------------------------------------------------------------------
import numpy as np

#--------------------------------------------------------------------------------
# bbox
#--------------------------------------------------------------------------------
def bbox(bbox,boundsall):

    # Convert to numpy array
    boundsall = np.array(boundsall)

    # User ROI center position and width (lon, lat)
    Ucenter = np.append(np.mean(bbox[0:4:2]),np.mean(bbox[1:4:2]))
    Uwidth  = np.append(np.diff(bbox[0:4:2]),np.diff(bbox[1:4:2]))

    # COG's center position and width (lon, lat)
    Ccenter = np.append([np.mean(boundsall[:,0:4:2],axis=1)],\
                        [np.mean(boundsall[:,1:4:2],axis=1)],axis=0).T
    Cwidth  = np.append( np.diff(boundsall[:,0:4:2],axis=1) ,\
                         np.diff(boundsall[:,1:4:2],axis=1) ,axis=1)
    
    # Center distance and width
    DistXY  = abs(Ccenter-Ucenter)
    WidthXY = Cwidth/2+Uwidth/2

    # Judge hit or not hit
    IDX_X = (DistXY[:,0] - WidthXY[:,0]) < 0
    IDX_Y = (DistXY[:,1] - WidthXY[:,1]) < 0
    IDX   = IDX_X & IDX_Y

    # Output
    return IDX


#--------------------------------------------------------------------------------
# line
#--------------------------------------------------------------------------------
def line(line,linesall,decimals):

    # Convert to numpy array
    linesall = np.array(linesall)

    # User ROI center position and width (lon, lat)
    Ucenter = (line[1]+line[0])/2
    Uwidth  = line[1]-line[0]

    # COG's center position and width (lon, lat)
    Ccenter = np.mean(linesall,axis=1)
    Cwidth  = linesall[:,1]-linesall[:,0]
    
    # Center distance and width
    Dist  = abs(Ccenter-Ucenter)
    Width = Cwidth/2+Uwidth/2

    # Judge hit or not hit
    IDX = np.round(Dist-Width,decimals) < 0

    # Output
    return IDX