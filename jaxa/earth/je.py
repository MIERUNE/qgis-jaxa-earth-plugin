
# --------------------------------------------------------------------------------
# je module description
# --------------------------------------------------------------------------------
"""
    This API package for Python was developed for the utilization of various earth 
    observation data held by `JAXA`_. By using this API, you can easily acquire and 
    process data without worrying about the specifications, sensors, resolution, 
    etc. of each satellite data.
    
    Warning:
        Attention! The API and the database are prototypes. Therefore, please be 
        aware that major destructive specification changes may be made in the future. 
        We are not responsible for any event or accident caused by the use of 
        this API or modules or databases.

    je module contains four classes : ``FeatureCollection``, ``ImageCollectionList``,
    ``ImageCollection``, ``ImageProcess``.

    .. _JAXA:
        https://www.jaxa.jp/

    .. code-block:: python

        # Usage example        
    
        # Import module
        from jaxa.earth import je
        
        # Read geojson
        geoj_path = "gadm36_JPN_0.geojson"
        geoj = je.FeatureCollection().read(geoj_path).select([])
        
        # Get images
        data_out = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v2012_global")\\
                     .filter_date(["2021-01-01T00:00:00","2022-01-01T00:00:00"])\\
                     .filter_resolution(20)\\
                     .filter_bounds(geoj[0])\\
                     .select("DSM")\\
                     .get_images()
        
        # Process and show images
        img = je.ImageProcess(data_out)\\
                .show_images()\\
                .calc_spatial_stats()\\
                .show_spatial_stats()
"""

# --------------------------------------------------------------------------------
# Load modules
# --------------------------------------------------------------------------------

# Common
import sys
import requests
from .utils  import read
from .params import Settings

# For FeatureCollection class, Feature
from .feature.collection.check  import CheckFeatureCollection
from .feature.collection.select import select_features

# Common parameters for ImageCollectionList/ImageCollection/ImageProcess
from .image.collection.check import CheckImageCollection

# For ImageCollectionList
from .image.collection.stac.select import Stac, get_all_children, extract_id, select_by_keywords

# For ImageCollection class
from .image.collection.date.select   import select_multiple_dates_url
from .image.collection.ppu.select    import select_multiple_dates_ppu_url
from .image.collection.bounds.set    import set_bbox_geojson
from .image.collection.bounds.select import select_multiple_dates_bounds_url
from .image.collection.cog.get       import get_multiple_dates_raster

# For ImageProcess class
from .image.process.conv  import geoj2raster
from .image.process.stats import composite, timeseries
from .image.process.match import match_images
from .image.process.mask  import mask_images
from .image.process.diff  import diff_images
from .image.process.show  import show_image, show_image_qgis, show_timeseries, get_qgis_layer

# --------------------------------------------------------------------------------
# FeatureCollection class
# --------------------------------------------------------------------------------
class FeatureCollection:
    """
    The ``FeatureCollection`` class is used to read a feature collection and select 
    features of geojson data from your computer.

    Returns:
        A ``FeatureCollection`` class object which has a propery of ``feature_collection``.
        the object's all properties is set to None as default.

    Attributes:
        feature_collection (dict): The property is updated after the method ``read`` 
            is executed. Default value is None.

    .. code-block:: python

        # Usage example: Aquire feature collection data
        geoj_path = "C:\\MyData\\gadm36_JPN_1.geojson"
        geoj = je.FeatureCollection().read(geoj_path).select(["Tokyo"])
    """

    # ----------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------
    def __init__(self):

        # Initilization
        self.feature_collection = None

    # ----------------------------------------------------------------------------
    # read: Read features collection
    # ----------------------------------------------------------------------------
    def read(self,path:str):
        """
        The method ``read`` read the inputed path's geojson data as feature collection.
        
        Args:
            path (str): User's geojson data location's absolute path

        Returns:
            A ``FeatureCollection`` class object that stores updated ``feature_collection`` property

        .. code-block:: python
    
            # Usage example: Read geojson data as feature collection
            data_path = "C:\\MyData\\MyArea.geojson"
            data_fc   = je.FeatureCollection.read(data_path)
        """

        # Check input/display status
        CheckFeatureCollection.File.read_input(path)
        
        # Set self
        self.feature_collection = read.json_raw(path)

        # Check output/display status
        CheckFeatureCollection.File.read_output(self.feature_collection)

        # Output
        return self

    # ----------------------------------------------------------------------------
    # select: Select feature collection's features by keywords
    # ----------------------------------------------------------------------------
    def select(self, keywords:list=[]):
        """
        The method ``select`` filter the inputed feature collection's data in 
        properties by keywords. The Default is blank list, so all features of 
        feature collection is selected.

        Args:
            keywords (list): keywords list of your prefered word

        Returns:
            geojson features selected by keywords

        .. code-block:: python
    
            # Usage example: Select feature from geojson's feature collection
            geojson = data_fc.select(["Japan","Tokyo"])
        """

        # Check input/display status
        CheckFeatureCollection.File.select_input(keywords)

        # All features in collection
        geoj_all = self.feature_collection["features"]

        # Select features which match all keywords
        geoj = select_features(geoj_all,keywords)

        # Check output/display status
        CheckFeatureCollection.File.select_output(geoj)        

        # Output
        return geoj

# --------------------------------------------------------------------------------
# ImageCollectionList class
# --------------------------------------------------------------------------------
class ImageCollectionList:

    """
    The class, ``ImageCollectionList`` get and filter colletion's catalog json 
    depend on user input keywords.

    Args:
        ssl_verify (bool): Users can set valid ssl certification process to ``True``
            or ``False``. The default is ``True``.

            Note:
                Setting the value to ``False`` can be a serucity risk.

    Returns:
        An ``ImageCollectionList`` class object which has properties of ``stac_collections``.

    .. code-block:: python
    
        # Usage example: Get collection's name and band
        keywords = ["LST","_half-month"]
        collections,bands = je.ImageCollectionList(ssl_verify=False)\\
                              .filter_name(keywords=keywords)
    """      

    # ----------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------
    def __init__(self,ssl_verify:bool=None):

        # Display status
        print(" - Geting image collection information : ", end="")        

        # JAXA Earth public datasets (COG) STAC URL
        settings     = Settings
        STAC_COG_URL = settings.stac_cog_url

        if (ssl_verify is not None) & ((ssl_verify == True) or (ssl_verify == False)):
            settings.ssl_verify = ssl_verify

        # Initialize session connection, verification
        session = requests.Session()
        session.verify = settings.ssl_verify

        # Get STAC URL list of image collection
        stac_ic_url = get_all_children(session,"child",STAC_COG_URL,[])

        # Extract collection's name
        stac_ic_id = extract_id(stac_ic_url)

        # Set self
        self._session  = session
        self._settings = settings
        self.stac_collections = Stac(session).set_url(stac_ic_url)\
                                             .set_id(stac_ic_id)

        # Display status
        print("completed")                                             
        
    # ----------------------------------------------------------------------------
    # filter_name: Filter image collection's name by keywords
    # ----------------------------------------------------------------------------
    def filter_name(self, keywords:list=[]):
        """
        The method, ``filter_name`` filter colletion's catalog json from 
        collection's id depend on user input keywords. 
        
        Args:
            keywords (list): keywords of request.

        Returns:
            filtered collections and filtered bands

        .. code-block:: python
    
            # Usage example: Get collection's name and band
            key = ["LST","_half-month"]
            collections,bands = je.ImageCollectionList()\\
                                  .filter_name(keywords=key)
        """      

        # Check input/display status
        CheckImageCollection.List.input(keywords)

        # Detect collections
        stac_ic_id, stac_band = select_by_keywords(self, keywords)

        # Check input/display status
        CheckImageCollection.List.output(stac_ic_id)        

        # Output
        return stac_ic_id, stac_band

# --------------------------------------------------------------------------------
# ImageCollection class
# --------------------------------------------------------------------------------
class ImageCollection:
    """
    The class, ``ImageCollection`` gets selected collection's catalog json data from
    JAXA Earth database. If you use the class's method, users can aquire collection's
    raster images depend on query such as date limit, resolution, bounds, band. 

    Args:
        collection (str): Selected collection's name. If no input, 
            "JAXA.EORC_ALOS.PRISM_AW3D30.v2012_global" will be used.
        ssl_verify (bool): Users can set valid ssl certification process to ``True``
            or ``False``. The default is ``True``.

            Note:
                Setting the value to ``False`` can be a serucity risk.

    Returns:
        An ``ImageCollection`` class object which has properties of ``stac_date``,
        ``stac_ppu`` , ``stac_bounds`` , ``stac_band`` and ``raster``. The object's 
        all properties is set to None as default.

    Attributes:
        stac_date (An ``Stac`` class object): Default value is None. The updated property 
            will be set after the method, ``filter_date``. The updated property has four 
            properties such as ``query`` , ``url`` , ``id`` and ``json``. The object is 
            used as input to the method ``filter_resolution``. 
        stac_ppu (An ``Stac`` class object): Default value is None. The updated property 
            will be set after the method, ``filter_resolution``. The updated property has 
            three properties such as ``query`` , ``url`` and ``json``. The object is 
            used as input to the method ``filter_bounds``. 
        stac_bounds (An ``Stac`` class object): Default value is None. The updated property 
            will be set after the method, ``filter_bounds``. The updated property has three 
            properties such as ``query`` , ``url`` and ``json``. The object 
            is used as input to the method ``select``. 
        stac_band (An ``Stac`` class object): Default value is None. The updated property 
            will be set after the method, ``select``. The updated property has two properties such 
            as ``query`` and ``url``. The object is used as input to the method ``get_images``. 
        raster (An ``Raster`` class object): Default value is None. The updated property 
            will be set after the method, ``get_images``. The updated ``Raster`` class 
            object property has properties of ``img`` , ``latlim`` and ``lonlim``. 

    .. code-block:: python
    
        # Usage example: Get image
        data_out = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v2012_global")\\
                     .filter_date(["2021-01-01T00:00:00","2023-01-31T00:00:00"])\\
                     .filter_resolution(20)\\
                     .filter_bounds([-180,-90,180,90])\\
                     .select("DSM")\\
                     .get_images()
    """    

    # ----------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------
    def __init__(self, collection:str=None, ssl_verify:bool=None):

        # Display status
        print(" - Collection : ", end="")

        # If no input, set default collection
        settings = Settings
        if collection is None:
            collection = settings.col_default

        # If ssl_verify is inputed, set verify
        if (ssl_verify is not None) & ((ssl_verify == True) or (ssl_verify == False)):
            settings.ssl_verify = ssl_verify

        # Initialize session connection, verification
        session = requests.Session()
        session.verify = settings.ssl_verify

        # Set stac cog url
        STAC_COG_URL = settings.stac_cog_url        

        # Get STAC URL of image collection (COG catalog's child)
        stac_cog_child_url = Stac(session).set_url([[STAC_COG_URL]]).set_json()\
                                          .set_child("child","collection",collection)\
                                          .child

        # Set collection's url, get json and child url
        self.stac_collection = Stac(session).set_query(collection)\
                                            .set_url(stac_cog_child_url)\
                                            .set_json()

        # Initialize Session
        self._session  = session
        self._settings = settings

        # All parameter initilization
        self.stac_date   = None # (0) filterDate's Output
        self.stac_ppu    = None # (1) filterResolution's Output
        self.cog_lev     = None # 
        self.cog_ifd_lev = None # 
        self.cog_ifd_ppu = None # 
        self.stac_bounds = None # (2) filterBounds's Output
        self.stac_band   = None # (3) select's Output
        self.raster      = None # (4) image,images

        # Display status
        print(collection)

    # ----------------------------------------------------------------------------
    # filter_date: Filter catalong by inputed date
    # ----------------------------------------------------------------------------
    def filter_date(self, dlim:list=[]):
        """
        The method, ``filter_date`` filters collection's catalog json by user query of
        date limit. If no inputs, defaulut date lim parameter is set as 
        ["2021-01-01T00:00:00","2021-12-31T23:59:59"]. Property of ``stac_date`` will 
        be updated after the method.

        Args:
            date_lim (list): date limits of minimum date, maximum date.

        Returns:
            An ``ImageCollection`` class object that stores updated ``stac_date`` property

        .. code-block:: python
    
            # Usage example: Filter ImageCollection by date limit
            date_lim = ["2021-01-01T00:00:00","2022-01-01T00:00:00"]
            data_ic1 = data_ic0.filter_date(date_lim)
        """

        # If no input, set default dlim
        if dlim == []:
            dlim = self._settings.dlim_default   

        # Check input/display status
        CheckImageCollection.Date.input(dlim)

        # Detect multi-dates URL
        stac_date_url, stac_date_id = select_multiple_dates_url(self,dlim)

        # Check output/display status
        CheckImageCollection.Date.output(stac_date_id)

        # Set and get catalog information
        self.stac_date = Stac(self._session).set_query(dlim)\
                                            .set_url(stac_date_url)\
                                            .set_id(stac_date_id)\
                                            .set_json()

        # Return
        return self

    # ----------------------------------------------------------------------------
    # filter_resolution: Filter catalog by inputed ppu(resolution)
    # ----------------------------------------------------------------------------
    def filter_resolution(self, ppu:float=None):
        """
        The method, ``filter_resolution`` filters collection's catalog json 
        by user query of resolution of ppu (Pixels Per Unit). Unit means one 
        degree in epsg 4326, 32786m in epsg 3995. If no input, minimum value or
        appropriate value (only in QGIS) is set. Property of ``stac_ppu`` will 
        be updated after the method.

        Args:
            ppu (float): ppu input.

        Returns:
            An ``ImageCollection`` class object that stores updated ``stac_ppu`` property

        Note:
            Attention! you have to use method ``filter_date`` before the method.

        .. code-block:: python
    
            # Usage example: Filter ImageCollection by ppu
            ppu = 20
            data_ic2 = data_ic1.filter_resolution(ppu)
        """

        # Check input/display status
        CheckImageCollection.Ppu.input(self.stac_date,ppu)        

        # Detect multi-dates ppu URL
        stac_ppu_url_tmp, date_idx, user_ppu, proj_params = select_multiple_dates_ppu_url(self,ppu)

        # Detect stac url
        stac_ppu_url = [[x[0]] for x in stac_ppu_url_tmp]

        # Check ppu URL list
        if stac_ppu_url == []:
            raise Exception("Error! No PPU list found!")

        # Update date information
        self.stac_date.url = [x[1] for x in enumerate(self.stac_date.url) if x[0] in date_idx]
        self.stac_date.id  = [x[1] for x in enumerate(self.stac_date.id ) if x[0] in date_idx]

        # Set catalog information
        self.proj_params = proj_params
        self.cog_lev     = stac_ppu_url_tmp[0][1]
        self.cog_ifd_lev = stac_ppu_url_tmp[0][2]
        self.cog_ifd_ppu = stac_ppu_url_tmp[0][3]

        # Display status
        CheckImageCollection.Ppu.output(proj_params,stac_ppu_url_tmp[0][3])   

        # Set and get catalog information
        self.stac_ppu = Stac(self._session).set_query(user_ppu)\
                                           .set_url(stac_ppu_url)\
                                           .set_json()        

        # Return
        return self

    # ----------------------------------------------------------------------------
    # filter_bounds: Filter catalog by inputed bbox or geojson
    # ----------------------------------------------------------------------------
    def filter_bounds(self, bbox:list=None, geoj:dict=None):
        """
        The method, ``filter_bounds`` filters collection's catalog json 
        by user query of bounds or geojson. If you input both of bbox and geoj,
        geoj is used to detect bounding box. If you don't input neither of them,
        maximum bounding box will be selected. 
        In QGIS environment, appropriate area will be selected with no input. 
        Property of ``stac_bounds`` will be updated after the method.

        Args:
            bbox (list): bounding box input.
            geoj (dict): geojson input

        Returns:
            An ``ImageCollection`` class object that stores updated ``stac_bounds`` property

        Note:
            Attention! you have to use method ``filter_resolution`` before the method.

        .. code-block:: python
    
            # Usage example: Filter ImageCollection by bbox of geojson
            bbox = [120,20,150,50]
            data_ic3 = data_ic2.filter_bounds(bbox)
        """

        # Check input/display status
        CheckImageCollection.Bounds.input(self.stac_ppu,bbox,geoj)   

        # Set bbox, geojson
        bbox,geoj = set_bbox_geojson(bbox, geoj, self.proj_params)

        # Detect multi-dates bounds cog's URL
        stac_bounds_url = select_multiple_dates_bounds_url(self,bbox)

        # Check output/display status
        CheckImageCollection.Bounds.output(stac_bounds_url,bbox)          

        # Set and get catalog information
        self.stac_bounds = Stac(self._session).set_query(geoj)\
                                              .set_url(stac_bounds_url)\
                                              .set_json()   

        # Return
        return self

    # ----------------------------------------------------------------------------
    # select: Select catalog by inputed band
    # ----------------------------------------------------------------------------
    def select(self, band:str=None):
        """
        The method, ``select`` selects collection's catalog json 
        by user query of band. If you don't input band, the first
        band will be selected. Property of ``stac_band`` will 
        be updated after the method.

        Args:
            band (str): band of asset

        Returns:
            An ``ImageCollection`` class object that stores updated ``stac_band`` property

        Note:
            Attention! you have to use method ``filter_bounds`` before the method.

        .. code-block:: python
    
            # Usage example: Filter ImageCollection by band
            band = "DSM"
            data_ic4 = data_ic3.filter_band(band)
        """
        # If no input, set default band
        if band is None:
            band = self._settings.band_default 
        
        # Check input/display status
        CheckImageCollection.Band.input(self.stac_bounds,band)

        # Set and get catalog information
        band_url = self.stac_bounds.set_band_url(band).band_url

        # Check output/display status
        CheckImageCollection.Band.output(band) 

        # Set and get catalog information
        self.stac_band = Stac(self._session).set_query(band)\
                                            .set_url(band_url)

        # Return
        return self

    # ----------------------------------------------------------------------------
    # get_images: Get images
    # ----------------------------------------------------------------------------
    def get_images(self):
        """
        The method, ``get_images`` gets collection's images depend on the user 
        querys of date limit, resolution, bounds, band. Property of ``raster`` will 
        be updated after the method. In addition to this, regeon of interest area of
        ``raster`` images will be returned.

        Returns:
            An ``ImageCollection`` class object that stores updated ``raster`` property

        Note:
            Attention! you have to use method ``filter_band`` before the method.

        .. code-block:: python
    
            # Usage example: Get Image depend on user's query.
            data_out0 = data_ic4.get_images()
        """

        # Check Input variable
        if not self.stac_band:
            raise Exception("Error! Please use method select before get_image")

        # Get multiple dates COG
        raster, cinfo = get_multiple_dates_raster(self)

        # Generate area mask and apply
        geoj = self.stac_bounds.query
        roi  = geoj2raster(geoj,raster)

        # Mask image
        raster.img = mask_images(raster.img,roi,"values_equal",[1])

        # Set self
        self.raster = raster
        self.cinfo  = cinfo

        # Return
        return self

# --------------------------------------------------------------------------------
# Image Process class
# --------------------------------------------------------------------------------
class ImageProcess:
    """
    The class, ``ImageProcess`` execute various process by using inputed ``ImageCollecion``
    class objects. If you use ``ImageProcess`` class method, users can process and get
    images such as masking images, differencial images, calculated temporal/spatial 
    statistics. In addition to the processing, It's possible to show images or 
    timeseries graph. 

    Args:
        data (object): ``ImageCollection`` class object which contains 
            updated ``raster`` property

            Note:
                Attention! ``ImageCollection`` class object must have correct ``raster`` property.            

    Returns:
        An ``ImageProcess`` class object with updated property

    Attributes:
        raster (An ``Raster`` class object): Default value is same as inputed 
            ``ImageCollection`` class object's  ``raster`` property. The property
            will be updated after  ``ImageProcess`` class object's method execution 
            such as ``mask_images`` , ``diff_images`` and ``calc_temporal_stats``.
        timeseries (dict): Default value is None. The property will be updated after  
            ``ImageProcess`` class object's method execution such as ``calc_spatial_stats``.
            Updated property has five keys and values such as "mean", "std", "min", "max", 
            "median".

    .. code-block:: python
    
        # Usage example: Process and show images
        img = je.ImageProcess(data_out0)\\
                .show_images()\\
                .calc_spatial_stats()\\
                .show_spatial_stats()
    """

    # ----------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------
    def __init__(self, data):

        # Set self
        self._settings   = data._settings
        self.collection  = data.stac_collection.query
        self.band        = data.stac_band.query
        self.date_id     = data.stac_date.id
        self.raster      = data.raster
        self.cinfo       = data.cinfo
        self.proj_params = data.proj_params
        self.timeseries  = None

    # ----------------------------------------------------------------------------
    # mask_images: Mask images
    # ----------------------------------------------------------------------------
    def mask_images(self, mask, method_query:str="values_equal", values:float=[0,1]):
        """
        The method, ``mask_images`` masks by using mask, type_query, values.

        Args:
            mask (class): ``ImageCollection`` class object that has updated ``raster`` 
                property which is used as masking data.

                Note: 
                    Attention! mask's shape (including resolution) must be 
                    same as data.

            method_query (dict): "range" or "values_equal" or "bits_equal". 
                Default method is "values_equal".
                
                "range" is used if users would like to extract specific range of 
                values and masks out of range values. Data type of float is acceptable 
                as "range" mask.

                "values_equal" is used if users would like to extract specific values 
                pixels only and other values pixels are masked. Data type of float is 
                acceptable. Typically, land cover products will be used as "values_equal" 
                mask.

                "bits_equal" is used if users would like to extract specific bit values 
                pixels only and other bit values pixels are masked. Data type of float is 
                not acceptable as mask. Typically, quality assuarance products will be 
                used as "bits_equal" mask.

            values(list): user query of values list. if you set type_query as "range",
                please set values as two values list as minimum and maximum. If "values_equal",
                you can set multiple values list as you like. If "bits_equal", you can set
                bit values 0 or 1 as bit values which begins from zero bit.
                Default values is [0,1].

        Returns:
            An ``ImageProcess`` class object that stores updated ``raster`` property

        .. code-block:: python
    
            # Usage example: Mask data_out0 by data_out1
            data_masked = data_ip0.mask_images(data_out1,"range",[0,100])
        """

        # Display status
        print(" - Mask : ", end="")

        # Match mask to image
        masks = match_images(self.raster,mask.raster,self.proj_params.r_dec_pix)

        # Execute mask images
        self.raster.img = mask_images(self.raster.img, masks, method_query, values)

        # Display status
        print(f"{method_query} , {values}")

        # output
        return self

    # ----------------------------------------------------------------------------
    # diff_images: Diff images
    # ----------------------------------------------------------------------------
    def diff_images(self, ref):
        """
        The method, ``diff_images`` take difference by user inputed query of ref.

        Args:
            ref (object): ``ImageCollection`` class object that has updated ``raster`` 
                property which is used as ref data.

                Note: 
                    Attention! ref's shape (including resolution) must be 
                    same as data.            

        Returns:
            An ``ImageProcess`` class object that stores updated ``raster`` property

        .. code-block:: python
    
            # Usage example: Differential data(data_out0-data_out1)
            data_diff = data_ip0.diff_images(data_out1)
        """

        # Display status
        print(" - Diff : ", end="")

        # Match ref to image
        refs = match_images(self.raster,ref.raster,self.proj_params.r_dec_pix)

        # Execute difference images
        self.raster.img = diff_images(self.raster.img, refs)

        # Display status
        print("difference tooked")

        # output
        return self

    # ----------------------------------------------------------------------------
    # calc_temporal_stats: Calculate temporal statistics
    # ----------------------------------------------------------------------------
    def calc_temporal_stats(self, method_query:str="mean"):
        """
        The method, ``calc_temporal_stats`` calculate temporal statistics by user 
        inputed query of method_query.

        Args:
            method_query (dict): "mean" or "max" or "min" or "std" or "median".
                Default is "mean".

        Returns:
            An ``ImageProcess`` class object that stores updated ``raster`` property

        .. code-block:: python
    
            # Usage example: Calculate temporal stats of data_ip0
            data_t_stats = data_ip0.calc_temporal_stats("mean")
        """

        # Display status
        print(" - Temporal stats : ", end="")

        # Method list
        method_all = ["mean", "std", "min", "max", "median"]

        # Detect method
        method = [s for s in method_all if method_query in s]

        # Check method
        if not method:
            raise Exception("Error! requested method is not inpremented !")

        # Calculate statistics, display status
        if len(self.raster.img) > 1:
            num = str(len(self.raster.img))
            self.raster.img = composite(self.raster.img, method[0])
            print(f"{num} images composited, method : {method[0]}")
        else:
            print("Warning! no need to composite")

        # output
        return self

    # ----------------------------------------------------------------------------
    # calc_spatial_stats: Calculate spatial Statistics
    # ----------------------------------------------------------------------------
    def calc_spatial_stats(self):
        """
        The method, ``calc_spatial_stats`` calculate spatial statistics.

        Returns:
            An ``ImageProcess`` class object that stores updated ``timeseries`` property.
            Updated property has five keys and values such as "mean", "std", "min", "max", 
            "median".

        .. code-block:: python
                
            # Usage example: Calculate spatial stats of data_ip0
            data_s_stats = data_ip0.calc_spatial_stats()
        """

        # Display status
        print(" - Spatial stats : ", end="")

        # Calculate statistics, display status
        self.timeseries = timeseries(self.raster.img)

        # Display status
        print(f"{len(self.raster.img)} images processed, method : mean, std, min, max, median")

        # output
        return self

    # ----------------------------------------------------------------------------
    # show_images: Show images
    # ----------------------------------------------------------------------------
    def show_images(self,cmap:str=None,clim:list=[]):
        """
        The method, ``show_images`` shows images of ``raster`` property. If multiple
        date's image is set, the method shows all of images.

        Args:
            cmap (str): query of colormap name. User can choose "ndvi","turbo", 
                "spectral". Default is "turbo".

            clim (list): query of color range (optional).

        Returns:
            An ``ImageProcess`` class object

        .. code-block:: python
    
            # Usage example: Show images of data_ip0
            data_ip0.show_images()
        """

        # Get values
        imgs   = self.raster.img
        latlim = self.raster.latlim[0]
        lonlim = self.raster.lonlim[0]
        title0 = f"{self.collection}, {self.band}"
        cinfo  = self.cinfo
        proj_params = self.proj_params

        # Display status
        print(" - Show images : ", end="")

        # Check imgs
        if imgs is None:
            raise Exception("Error! please use get_images before use show_images")

        else:

            # Show each day's image
            for i in range(len(imgs)):

                # Set cmap if required
                if not (not cmap):
                    cinfo[i].set_cmap_params(cmap_name = cmap)

                # Set clim if required
                if not clim:
                    cinfo[i].set_clim(imgs[i])
                else:
                    cinfo[i].clim = clim

                # Show single image
                title = f"{title0}, {self.date_id[i]}"
                show_image(imgs[i], latlim, lonlim, title, cinfo[i], proj_params)

        # Display status
        print("showed")

        #import matplotlib.pyplot as plt
        #plt.imshow(self.image[0])
        #plt.show()

        # Output
        return self

    # ----------------------------------------------------------------------------
    # show_images_qgis: Show images qgis
    # ----------------------------------------------------------------------------
    def show_images_qgis(self,cmap:str=None,clim:list=[]):
        """
        The method, ``show_images_qgis`` shows images in qgis.

        Args:
            cmap (str): query of colormap name. User can choose "ndvi","turbo", 
                "spectral". Default is "turbo".
            clim (list): query of color range (optional).

        Returns:
            An ``ImageProcess`` class object

        Note:
            Attention! This method is only valid in QGIS environment.

        .. code-block:: python
    
            # Usage example: Show images of data_ip0 in qgis
            data_ip0.show_images_qgis()
        """

        # Check QGIS module
        if "qgis.core" not in sys.modules:
            raise Exception("Error! qgis.core module was not found!")

        # Get values
        imgs   = self.raster.img
        latlim = self.raster.latlim[0]
        lonlim = self.raster.lonlim[0]
        cinfo  = self.cinfo
        proj   = self.proj_params.epsg

        # Display status
        print(" - Show images in QGIS : ", end="")

        # Check imgs
        if imgs is None:
            raise Exception("Error! please use get_images before use show_images")
        else:

            # Show each day's image
            for i in range(len(imgs)):

                # Set cmap if required
                if not (not cmap):
                    cinfo[i].set_cmap_params(cmap_name = cmap)
                
                # Set clim default or required
                if not clim:
                    cinfo[i].set_clim(imgs[i])
                else:
                    cinfo[i].clim = clim

                # Detect date id
                date_id = self.date_id[i].replace("/","").replace("-","")

                # Show single image
                show_image_qgis(i, date_id, imgs[i], latlim, lonlim, cinfo[i], proj)

        # Display status
        print("showed")

        # Output
        return self

    def get_qgis_layers(self,cmap:str=None,clim:list=[]):
        """
        The method, ``show_images_qgis`` shows images in qgis.

        Args:
            cmap (str): query of colormap name. User can choose "ndvi","turbo", 
                "spectral". Default is "turbo".
            clim (list): query of color range (optional).

        Returns:
            An ``ImageProcess`` class object

        Note:
            Attention! This method is only valid in QGIS environment.

        .. code-block:: python
    
            # Usage example: Show images of data_ip0 in qgis
            data_ip0.show_images_qgis()
        """

        # Check QGIS module
        if "qgis.core" not in sys.modules:
            raise Exception("Error! qgis.core module was not found!")

        # Get values
        imgs   = self.raster.img
        latlim = self.raster.latlim[0]
        lonlim = self.raster.lonlim[0]
        cinfo  = self.cinfo
        proj   = self.proj_params.epsg

        qgs_layers = []

        # Check imgs
        if imgs is None:
            raise Exception("Error! please use get_images before use show_images")
        else:

            # Show each day's image
            for i in range(len(imgs)):

                # Set cmap if required
                if not (not cmap):
                    cinfo[i].set_cmap_params(cmap_name = cmap)
                
                # Set clim default or required
                if not clim:
                    cinfo[i].set_clim(imgs[i])
                else:
                    cinfo[i].clim = clim

                # Detect date id
                date_id = self.date_id[i].replace("/","").replace("-","")

                # Show single image
                qgs_layer = get_qgis_layer(i, date_id, imgs[i], latlim, lonlim, cinfo[i], proj)
                qgs_layers.append(qgs_layer)

        # Output
        return qgs_layers

    # ----------------------------------------------------------------------------
    # show_spatial_stats: Show spatial statistics
    # ----------------------------------------------------------------------------
    def show_spatial_stats(self,ylim:list=[]):
        """
        The method, ``show_spatial_stats`` shows graph of calclation result of 
        the method ``calc_spatial_stats``.

        Args:
            ylim (list): query of color range (optional)

        Returns:
            An ``ImageProcess`` class object

        Note:
            Attention! you should use the method ``calc_spatial_stats`` before the method.

        .. code-block:: python
    
            # Usage example: Show graph of calclation result of the method calc_spatial_stats
            data_s_stats.show_spatial_stats()
        """
        
        # Get values
        title      = self.collection
        timeseries = self.timeseries
        x_label    = self.date_id
        y_label    = f"{self.band} [{self.cinfo[0].unit}]".replace("None","-")

        # Display status
        print(" - Show spatial stats : ", end="")

        # Check imgs
        if not timeseries:
            raise Exception("Error! please use calc_spatial_stats before use show_spatial_stats")
        else:
            # Show single image
            show_timeseries(timeseries,title,x_label,y_label,ylim)

        # Display status
        print("showed")

        # Output
        return self
