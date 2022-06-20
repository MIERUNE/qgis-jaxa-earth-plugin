#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
from ..bin     import bin2num1
from .tifftags import dec2name,num2type

#----------------------------------------------------------------------------------------
# read_all_ifd : Get multiple ifd level information in a file
#----------------------------------------------------------------------------------------
def read_all_ifd(btmp,ifd_level):

    # Detect first ifd location
    ifd     = []
    ifd_pos = bin2num1(btmp[4:8],"uint32")
    ifd_num = 0

    # Get ifd until requested ifd level
    while ifd_pos > 0:

        # (1) Get ifd and next ifd location
        ifd_tmp,ifd_pos = read_single_ifd(btmp,ifd_pos)
        ifd.append(ifd_tmp)

        # (2) Return if get ifd requested level
        if ifd_num == ifd_level:
            break

        # (3) Get next ifd location
        ifd_pos = bin2num1(btmp[ifd_pos:ifd_pos+4],"uint32")

        # (4) Level increment
        ifd_num = ifd_num + 1

    return ifd

#----------------------------------------------------------------------------------------
# read_single_ifd : Get single ifd level information in a file
#----------------------------------------------------------------------------------------
def read_single_ifd(btmp,ifd_pos):

    # Get the numbers of Tag elements
    tag_num_all = bin2num1(btmp[ifd_pos:ifd_pos+2],'uint16')
    
    # Get information of all Tag elements
    tag_pos = 0
    ifd    = {}
    for i in range(tag_num_all):

        # Get tag information (1:name, 2-3:dtype, 4:value num)
        tag_tmp0 = bin2num1(btmp[ifd_pos+tag_pos+2:ifd_pos+tag_pos+10],'uint16')

        # (1) 1-2 bytes : Name
        tag_name = dec2name(tag_tmp0[0])

        # (2)(3) 3-4 bytes : Data type, number of bytes
        tag_type,tag_size = num2type(tag_tmp0[1])

        # (4) 5-8 bytes : Number of the value
        value_num = tag_tmp0[2]+tag_tmp0[3]*2**16

        # (5) 9-12 bytes : value
        value_pos = ifd_pos+tag_pos+10
        tag_value = gettagvalue(value_pos,tag_type,tag_size,value_num,btmp)

        # Update(Append) ifd information
        ifd.update({tag_name:tag_value})

        # Update Tag location
        tag_pos = tag_pos + 12

    # Get next ifd location
    ifd_pos = ifd_pos+2+tag_num_all*12

    # Output ifd, next ifd location
    return ifd,ifd_pos

#----------------------------------------------------------------------------------------
# gettagvalue : Get geotiff tag's value
#----------------------------------------------------------------------------------------
def gettagvalue(value_pos,tag_type,tag_size,value_num,btmp):

    # In case of within 4 bytes
    if tag_size*value_num <=4 :

        # (1) one value
        if value_num == 1:
            value = [bin2num1(btmp[value_pos:value_pos+4],'uint32')]

        # (2) beyond two values
        else:
            if tag_type == "char":
                value = btmp[value_pos:value_pos+tag_size]
            else:
                value = []
                for i in range(value_num):
                    bpos0 = value_pos+tag_size*(i  )
                    bpos1 = value_pos+tag_size*(i+1)
                    value.append(bin2num1(btmp[bpos0:bpos1],tag_type))

    # In case of without 4 bytes
    else:

        # (1) Get offset location
        offset = bin2num1(btmp[value_pos:value_pos+4],"uint32")

        # (2) Get value
        if tag_type == "char":
            value = btmp[offset:offset+value_num].decode()
        else:
            value = []
            for i in range(value_num):
                bpos0 = offset+tag_size*(i  )
                bpos1 = offset+tag_size*(i+1)
                value.append(bin2num1(btmp[bpos0:bpos1],tag_type))

    # Output
    return value
