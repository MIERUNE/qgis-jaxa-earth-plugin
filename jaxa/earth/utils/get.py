#----------------------------------------------------------------------------------------
# Load module (common)
#----------------------------------------------------------------------------------------
import urllib3
#from ..params import Settings

#----------------------------------------------------------------------------------------
# Disable SSL certificate varification,  warning
#----------------------------------------------------------------------------------------
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
#ssl_verify = Settings.ssl_verify

#----------------------------------------------------------------------------------------
# range : Get binary by HTTP Range request
#----------------------------------------------------------------------------------------
def range(session,URL,r1,r2):
    header = {"content-type":"application/octet-stream","Range":f"bytes={r1}-{r2}"}
    res = session.get(URL,headers=header)#,verify=ssl_verify)
    check_error(res,URL)
    return res.content

#----------------------------------------------------------------------------------------
# json : Get json
#----------------------------------------------------------------------------------------
def json(session,URL):
    res = session.get(URL)#,verify=ssl_verify)
    check_error(res,URL)
    return res.json()

#----------------------------------------------------------------------------------------
# jsongz : Get json.gz and decompress
#----------------------------------------------------------------------------------------
def jsongz(session,URL):
    import gzip
    import json
    res   = session.get(URL)#,verify=ssl_verify)
    check_error(res,URL)
    bytes = gzip.decompress(res.content)
    return json.loads(bytes)
    
#----------------------------------------------------------------------------------------
# check_error : check error
#----------------------------------------------------------------------------------------
def check_error(res,URL):
    if res.status_code >= 400:
        print(" - Requested URL : " + URL)
        raise Exception(f"Error! Status code = {res.status_code},  {res.reason}")
