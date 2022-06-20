#----------------------------------------------------------------------------------------
# Load module
#----------------------------------------------------------------------------------------
from PIL import TiffTags

#----------------------------------------------------------------------------------------
# dec2name:extract tag name from number
#----------------------------------------------------------------------------------------
def dec2name(dec):
    return TiffTags.lookup(dec).name
    #return getvalues(tags,"dec","name",dec)

#----------------------------------------------------------------------------------------
# num2type：extract tag type from number
#----------------------------------------------------------------------------------------
def num2type(num):
    Data = [{"key": 1,"type":"uint8" ,"length":1},\
            {"key": 2,"type":"char"  ,"length":1},\
            {"key": 3,"type":"uint16","length":2},\
            {"key": 4,"type":"uint32","length":4},\
            {"key": 5,"type":"uint64","length":8},\
            {"key": 6,"type":"int8"  ,"length":1},\
            {"key": 7,"type":"uint8" ,"length":1},\
            {"key": 8,"type":"int16" ,"length":2},\
            {"key": 9,"type":"int32" ,"length":4},\
            {"key":10,"type":"int64" ,"length":8},\
            {"key":11,"type":"single","length":4},\
            {"key":12,"type":"double","length":8}]
    type = getvalues(Data,"key","type"  ,num)
    leng = getvalues(Data,"key","length",num)
    return type, leng
    
#----------------------------------------------------------------------------------------
# getvalues: extract key value from dict list
#----------------------------------------------------------------------------------------
def getvalues(Data,Keyname,Valuename,UserKey):
    keys   = []
    values = []
    for i in range(len(Data)):
        keys.append(  Data[i][Keyname  ])
        values.append(Data[i][Valuename])
    value = values[keys.index(UserKey)]
    return value
