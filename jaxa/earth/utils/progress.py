#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import sys
import numpy as np

#----------------------------------------------------------------------------------------
# bar : Showing progress bar
#----------------------------------------------------------------------------------------
def bar(i,Num):

    # Display progress percentage
    if i==0:
        print("   ------10------20------30------40------50"+\
                 "------60------70------80------90-----100")
        print("   ",end="")
    
    # Display bar by 80th percentile
    progress = np.ceil(np.linspace(0,Num,81))
    progress = np.delete(progress,0)
    
    # Display bar (Qgis console)
    if "qgis.core" in sys.modules:
        barnum_q = sum((i < progress) & (progress <= i+1))
        if barnum_q > 0:
            print("|"*barnum_q, end="")
    
    # Display bar (Python console)
    else:
        barnum_p = sum(progress <= i+1)
        if barnum_p > 0:
            print("\r   "+"|"*barnum_p, end="")
    
    # Insert a new line
    if i == Num-1:
        print("")

    # Finish
    return 1