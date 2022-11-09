# --------------------------------------------------------------------------------
# Load module
# --------------------------------------------------------------------------------
from ....utils import get
from urllib.parse import urljoin

# --------------------------------------------------------------------------------
# Stac ： stac information class
# --------------------------------------------------------------------------------
class Stac:

    # Initilization
    def __init__(self,session):
        self._session = session

    # Set user query
    def set_query(self,query):
        self.query = query
        return self

    # Set URL
    def set_url(self,url):
        self.url = url
        return self

    # Set lon offsets
    def set_lon_offsets(self,offsets):
        self.lon_offsets = offsets
        return self

    # Set ID
    def set_id(self,id):
        self.id = id
        return self
    
    # Set json
    def set_json(self):

        # Get all json 
        json_tmp1 = []
        for i in range(len(self.url)):
            json_tmp0 = []
            for j in range(len(self.url[i])):
                json_tmp0.append(get.json(self._session, self.url[i][j]))
            json_tmp1.append(json_tmp0)
        self.json = json_tmp1

        # Output
        return self
    
    # Set child (dimension += 0)
    def set_child(self,rel_type,json_type,name):

        # Get all json 
        child_tmp1 = []
        for i in range(len(self.url)):
            child_tmp0 = []
            for j in range(len(self.url[i])):
                child_tmp0.append(select_child(self._session,rel_type, self.url[i][j],self.json[i][j],name,json_type))
            child_tmp1.append(child_tmp0)
        self.child = child_tmp1

        # Output
        return self

    # Set band url to tif
    def set_band_url(self,band):
        
        # Get COG URL of BAND
        cog_tmp1 = []
        for i in range(len(self.json)):
            cog_tmp0 = []
            for j in range(len(self.json[i])):
                try:
                    # Get url
                    tmp = self.json[i][j]["assets"][band]["href"]

                    # if relative, set https:// 
                    if not ("https://" in tmp):
                        tmp = urljoin(self.url[i][j],tmp)

                except:
                    raise Exception(f"Error! {band} was not exist in assets !")
                cog_tmp0.append(tmp)
            cog_tmp1.append(cog_tmp0)
        self.band_url = cog_tmp1

        # Output
        return self        

# --------------------------------------------------------------------------------
# select_child ： Select a child
# --------------------------------------------------------------------------------
def select_child(session, rel_type, URL, json, name, json_type):

    # Select child All
    URL = get_all_children(session, rel_type, URL, json)

    # Select childs One
    nametmp = f"/{name}/{json_type}.json"
    href    = [s for s in URL if nametmp in s]

    # Check output
    if len(href) == 0:
        message0 = f"requested : {name}"
        raise Exception(f"Error! Requested {json_type} name was not found !\n"+message0)

    # Output
    return href[0]

# --------------------------------------------------------------------------------
# get_all_children : Get all children (It's not appropriate to combine to Stac)
# --------------------------------------------------------------------------------
def get_all_children(session, rel_type, URL, json):

    # Read if json is empty
    if len(json) == 0:
        jsonall = get.json(session, URL)
    else:
        jsonall = json

    # Initialization
    href = []

    # Select childs
    for i in range(len(jsonall["links"])):
        if (jsonall["links"][i]["rel"] == rel_type):

            # Detect child path
            href_tmp = jsonall["links"][i]["href"]

            # Change ralative path to full path if no https://
            if not ("https://" in href_tmp):
                typetmp  = jsonall["type"].lower()+".json"
                URLtmp   = URL.replace(typetmp, "")
                href_tmp = URLtmp + href_tmp.replace("./","")

            # Append
            href.append(href_tmp)

    # Output
    return href

# --------------------------------------------------------------------------------
# extract_id : Extract nearest id from url list
# --------------------------------------------------------------------------------
def extract_id(URL):

    # Extract id
    stac_id = [URL[i].split('/')[-2] for i in range(len(URL))]

    # Output
    return stac_id

# --------------------------------------------------------------------------------
# select_by_keywords : Select collection's id,bands by keywords
# --------------------------------------------------------------------------------
def select_by_keywords(input, keyword):

    # Set Session, URL, ID
    session = input._session 
    URL     = input.stac_collections.url
    ID      = input.stac_collections.id

    # Initialization
    stac_url = []
    stac_id  = []

    # Extract id
    for i in range(len(ID)):
        if all([x in ID[i] for x in keyword]):
            stac_url.append(URL[i])
            stac_id.append(ID[i])

    # Detect each collection's band
    stac_band = []
    for i in range(len(stac_url)):
        stac_ic_json_tmp = get.json(session, stac_url[i])
        stac_band.append(list(stac_ic_json_tmp["assets"].keys()))            

    # Output
    return stac_id, stac_band
