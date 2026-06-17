# ----------------------------------------------------------------------------------------
# TIFF tag code -> name mapping (replaces PIL.TiffTags.lookup).
# Covers baseline TIFF 6.0, GeoTIFF, and GDAL extension tags encountered in COG files.
# Unknown codes fall back to "Tag<code>" so unrecognized tags still produce a stable key.
# ----------------------------------------------------------------------------------------
_TAG_NAMES = {
    254: "NewSubfileType",
    255: "SubfileType",
    256: "ImageWidth",
    257: "ImageLength",
    258: "BitsPerSample",
    259: "Compression",
    262: "PhotometricInterpretation",
    263: "Threshholding",
    264: "CellWidth",
    265: "CellLength",
    266: "FillOrder",
    269: "DocumentName",
    270: "ImageDescription",
    271: "Make",
    272: "Model",
    273: "StripOffsets",
    274: "Orientation",
    277: "SamplesPerPixel",
    278: "RowsPerStrip",
    279: "StripByteCounts",
    280: "MinSampleValue",
    281: "MaxSampleValue",
    282: "XResolution",
    283: "YResolution",
    284: "PlanarConfiguration",
    285: "PageName",
    286: "XPosition",
    287: "YPosition",
    288: "FreeOffsets",
    289: "FreeByteCounts",
    290: "GrayResponseUnit",
    291: "GrayResponseCurve",
    292: "T4Options",
    293: "T6Options",
    296: "ResolutionUnit",
    297: "PageNumber",
    301: "TransferFunction",
    305: "Software",
    306: "DateTime",
    315: "Artist",
    316: "HostComputer",
    317: "Predictor",
    318: "WhitePoint",
    319: "PrimaryChromaticities",
    320: "ColorMap",
    321: "HalftoneHints",
    322: "TileWidth",
    323: "TileLength",
    324: "TileOffsets",
    325: "TileByteCounts",
    330: "SubIFDs",
    332: "InkSet",
    333: "InkNames",
    334: "NumberOfInks",
    336: "DotRange",
    337: "TargetPrinter",
    338: "ExtraSamples",
    339: "SampleFormat",
    340: "SMinSampleValue",
    341: "SMaxSampleValue",
    342: "TransferRange",
    343: "ClipPath",
    344: "XClipPathUnits",
    345: "YClipPathUnits",
    346: "Indexed",
    347: "JPEGTables",
    351: "OPIProxy",
    512: "JPEGProc",
    513: "JPEGInterchangeFormat",
    514: "JPEGInterchangeFormatLength",
    515: "JPEGRestartInterval",
    517: "JPEGLosslessPredictors",
    518: "JPEGPointTransforms",
    519: "JPEGQTables",
    520: "JPEGDCTables",
    521: "JPEGACTables",
    529: "YCbCrCoefficients",
    530: "YCbCrSubSampling",
    531: "YCbCrPositioning",
    532: "ReferenceBlackWhite",
    700: "XMP",
    33432: "Copyright",
    33550: "ModelPixelScaleTag",
    33922: "ModelTiepointTag",
    34264: "ModelTransformationTag",
    34377: "ImageResources",
    34665: "ExifIFD",
    34675: "InterColorProfile",
    34735: "GeoKeyDirectoryTag",
    34736: "GeoDoubleParamsTag",
    34737: "GeoAsciiParamsTag",
    42112: "GDAL_METADATA",
    42113: "GDAL_NODATA",
}


# ----------------------------------------------------------------------------------------
# dec2name : extract tag name from number
# ----------------------------------------------------------------------------------------
def dec2name(dec):
    return _TAG_NAMES.get(dec, f"Tag{dec}")


# ----------------------------------------------------------------------------------------
# num2type : extract tag type from number
# ----------------------------------------------------------------------------------------
def num2type(num):
    Data = [
        {"key": 1, "type": "uint8", "length": 1},
        {"key": 2, "type": "char", "length": 1},
        {"key": 3, "type": "uint16", "length": 2},
        {"key": 4, "type": "uint32", "length": 4},
        {"key": 5, "type": "uint64", "length": 8},
        {"key": 6, "type": "int8", "length": 1},
        {"key": 7, "type": "uint8", "length": 1},
        {"key": 8, "type": "int16", "length": 2},
        {"key": 9, "type": "int32", "length": 4},
        {"key": 10, "type": "int64", "length": 8},
        {"key": 11, "type": "single", "length": 4},
        {"key": 12, "type": "double", "length": 8},
    ]
    type = getvalues(Data, "key", "type", num)
    leng = getvalues(Data, "key", "length", num)
    return type, leng


# ----------------------------------------------------------------------------------------
# getvalues: extract key value from dict list
# ----------------------------------------------------------------------------------------
def getvalues(Data, Keyname, Valuename, UserKey):
    keys = []
    values = []
    for i in range(len(Data)):
        keys.append(Data[i][Keyname])
        values.append(Data[i][Valuename])
    value = values[keys.index(UserKey)]
    return value
