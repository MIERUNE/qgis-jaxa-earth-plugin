#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
import numpy as np
import zlib

#----------------------------------------------------------------------------------------
# bin2img: Convert binary to image
#----------------------------------------------------------------------------------------
def bin2img(bin,ifd,twidth,tlength):

    # Decompress if compressed binary
    if   ifd["Compression"][0] ==     8 or\
         ifd["Compression"][0] == 32946:
        bin = zlib.decompress(bin)

    elif ifd["Compression"][0] == 1:
        bin = bin
    else:
        raise Exception("Error! the API can't read the compression type!")

    # Change data type
    type = gettype(ifd)
    dtmp = bin2num2(bin,type)
    data = np.array(dtmp,dtype=type)

    # Reshape data shape
    img  = data.reshape(twidth,tlength,ifd["SamplesPerPixel"][0])

    # Process Predictor
    if "Predictor" in ifd:
        if ifd["Predictor"][0] == 2:
            img = np.cumsum(img,axis = 1)

    # Output
    return img

#----------------------------------------------------------------------------------------
# gettype : Detect data type from ifd
#----------------------------------------------------------------------------------------
def gettype(ifd):
    bits    = ifd["BitsPerSample"][0]
    formats = ifd["SampleFormat" ][0]
    if   formats == 1: type = "uint"   + str(bits)
    elif formats == 2: type = "int"    + str(bits)
    elif formats == 3: type = "single"
    elif formats == 4: type = "unknown"
    return type


#----------------------------------------------------------------------------------------
# bin2num2：convert type using memory view (fast)
#----------------------------------------------------------------------------------------
def bin2num2(bin,outtype):

    # Detect type
    if   outtype ==  "uint8":type = "B"
    elif outtype ==   "int8":type = "b"
    elif outtype == "uint16":type = "H"
    elif outtype ==  "int16":type = "h"
    elif outtype == "uint32":type = "L"
    elif outtype ==  "int32":type = "l"
    elif outtype == "single":type = "f"
    elif outtype == "double":type = "d"
    else:
        raise Exception("Error! No appropriate type request!")

    # Output
    return memoryview(bin).cast(type).tolist()

#----------------------------------------------------------------------------------------
# bin2num1: multiple data's converet (slow)
#----------------------------------------------------------------------------------------
def bin2num1(bin,outtype):

    # Separete
    if   outtype ==  "uint8":inc = 1
    elif outtype ==   "int8":inc = 1
    elif outtype == "uint16":inc = 2
    elif outtype ==  "int16":inc = 2
    elif outtype == "uint32":inc = 4
    elif outtype ==  "int32":inc = 4
    elif outtype == "single":inc = 4
    elif outtype == "double":inc = 8
    else:
        raise Exception("Error! No appropriate type request!")

    # Data processing
    num = []
    for i in range(int(len(bin)/inc)):
        num.append(bin2num0(bin[inc*i:inc*(i+1)],outtype))

    # Convert list to number if one value
    if len(num) == 1:
        num = num[0]
    return num

#----------------------------------------------------------------------------------------
# bin2num0: single data's converet (slow)
#----------------------------------------------------------------------------------------
def bin2num0(bin,outtype):
    if   outtype ==  "uint8":num = int.from_bytes(bin,byteorder='little',signed=False)
    elif outtype ==   "int8":num = int.from_bytes(bin,byteorder='little',signed=True )
    elif outtype == "uint16":num = int.from_bytes(bin,byteorder='little',signed=False)
    elif outtype ==  "int16":num = int.from_bytes(bin,byteorder='little',signed=True )
    elif outtype == "uint32":num = int.from_bytes(bin,byteorder='little',signed=False)
    elif outtype == "single":
        import struct
        num = struct.unpack('<f',bin)
        num = num[0]
    elif outtype == "double":
        import struct
        num = struct.unpack('<d',bin)
        num = num[0]
    else:
        raise Exception("Error! No appropriate type request!")
    return num
