#--------------------------------------------------------------------------------
# Load module
#--------------------------------------------------------------------------------
import datetime
import calendar
import numpy as np
from ..stac.select import get_all_children

#--------------------------------------------------------------------------------
# select
#--------------------------------------------------------------------------------
def select_multiple_dates_url(input,date):

    # Get STAC URL of date
    stac_date_url_all = get_all_children(input._session, "child", input.stac_collection.url[0][0], input.stac_collection.json[0][0])

    # Detect STAC Date format and depth
    date_format_raw = input.stac_collection.json[0][0]["summaries"]["je:stac_date_format"]
    
    # Detect date format type
    if   type(date_format_raw) == list:
        date_format = date_format_raw[0]
    elif type(date_format_raw) == str :
        date_format = date_format_raw

    # Detect Appropriate Date Catalog URL
    stac_date_url, stac_date_id = select_date(input._session, stac_date_url_all, date_format, date)

    # Output
    return stac_date_url, stac_date_id

#--------------------------------------------------------------------------------
# select
#--------------------------------------------------------------------------------
def select_date(session,stac_date_url_all,DATE_FORMAT,date_lim_str):

    # Judge Input date
    try:
        date_lim = [datetime.datetime.strptime(date_lim_str[i],'%Y-%m-%dT%H:%M:%S') for i in range(len(date_lim_str))] 
    except:
        raise Exception("Error! Requested date string is incorrect!")

    #----------------------------------------------------------------------------
    # YYYY-MM/DD : daily,half-monthly data screening
    #----------------------------------------------------------------------------
    if DATE_FORMAT == "YYYY-MM/DD":

        # Change Date range (start:day1 - end:day31)
        date_lim_tmp = [date_lim[0].replace(day=1),
                        date_lim[1].replace(day=calendar.monthrange(date_lim[1].year, date_lim[1].month)[1])]

        # Depth 0 screening
        URL0         = stac_date_url_all
        DATE_FORMAT0 = "YYYY-MM"
        STR_FORMAT0  = '%Y-%m/'
        stac_date_url_all, date_id = url2date(URL0,DATE_FORMAT0,STR_FORMAT0,date_lim_tmp)

        # Get final depth's stac catalog url list
        stac_date_url_tmp = []
        for i in range(len(stac_date_url_all)):
            url_tmp = get_all_children(session,"child",stac_date_url_all[i][0],[])
            stac_date_url_tmp.extend(url_tmp)
        
        # Depth 1 screening
        URL1         = stac_date_url_tmp
        DATE_FORMAT1 = "YYYY-MM/DD"
        STR_FORMAT1  = '%Y-%m/%d/'
        stac_date_url, date_id = url2date(URL1,DATE_FORMAT1,STR_FORMAT1,date_lim)
    
    #----------------------------------------------------------------------------
    # YYYY-MM : monthly data screening
    #----------------------------------------------------------------------------
    elif DATE_FORMAT == "YYYY-MM":

        # Change Date range (start:day1 - end:day31)
        date_lim_tmp = [date_lim[0].replace(day=1),
                        date_lim[1].replace(day=calendar.monthrange(date_lim[1].year, date_lim[1].month)[1])]

        # Screening
        URL        = stac_date_url_all
        STR_FORMAT = '%Y-%m/'
        stac_date_url, date_id = url2date(URL,DATE_FORMAT,STR_FORMAT,date_lim_tmp)

    #----------------------------------------------------------------------------
    # YYYY : Yearly data screening
    #----------------------------------------------------------------------------
    elif DATE_FORMAT == "YYYY":

        # Screening
        URL        = stac_date_url_all
        STR_FORMAT = '%Y/'
        stac_date_url, date_id = url2date(URL,DATE_FORMAT,STR_FORMAT,date_lim)

    #----------------------------------------------------------------------------
    # DDD : Normal data (daily) screening
    #----------------------------------------------------------------------------
    elif DATE_FORMAT == "DDD":
        
        # Set parameters
        URL = stac_date_url_all
        stac_date_url, date_id = url2doy(URL,DATE_FORMAT,date_lim)

    #----------------------------------------------------------------------------
    # MM-DD : Normal data (half-monthly) screening
    #----------------------------------------------------------------------------
    elif DATE_FORMAT == "MM-DD":

        # Set parameters
        URL = stac_date_url_all
        stac_date_url, date_id = url2hmonth(URL,DATE_FORMAT,date_lim)

    #----------------------------------------------------------------------------
    # MM : Normal data (monthly) screening
    #----------------------------------------------------------------------------
    elif DATE_FORMAT == "MM":
        
        # Set parameters
        URL = stac_date_url_all
        stac_date_url, date_id = url2month(URL,DATE_FORMAT,date_lim)

    #----------------------------------------------------------------------------
    # No date type
    #----------------------------------------------------------------------------
    else:
        raise Exception("Error! Requested date format type is not defined!")

    # Output
    return stac_date_url,date_id

#--------------------------------------------------------------------------------
# url2date
#--------------------------------------------------------------------------------
def url2date(URL,DATE_FORMAT,STR_FORMAT,date_lim):

    # Set parameters
    str_len1 = len(DATE_FORMAT)
    str_len2 = len("catalog.json")

    # Extract stac catalog's datetime, detection
    stac_date_url = []
    date_id       = []
    for i in range(len(URL)):
        date_id_tmp   = URL[i][-(str_len1+str_len2+1):-str_len2]
        stac_date_tmp = datetime.datetime.strptime(date_id_tmp,STR_FORMAT)
        time_delta1   = (stac_date_tmp-date_lim[0]).total_seconds()
        time_delta2   = (date_lim[1]-stac_date_tmp).total_seconds()
        if (time_delta1 >= 0) and (time_delta2 >= 0):
            stac_date_url.append([URL[i]])
            date_id.append(date_id_tmp) 

    # Output
    return stac_date_url, date_id

#--------------------------------------------------------------------------------
# url2month
#--------------------------------------------------------------------------------
def url2month(URL,DATE_FORMAT,date_lim):

    # Set start,end time in monthly date
    year_lim = [date_lim[0].year ,date_lim[1].year ]
    m_lim    = [1,12]
    m_lim_in = [date_lim[0].month,date_lim[1].month]
    m_all    = np.linspace(1,12,12)

    # Detect url, id
    stac_date_url, date_id = detect_url_id(URL,DATE_FORMAT,year_lim,
                                           m_lim,m_lim_in,m_all)

    # Output
    return stac_date_url, date_id

#--------------------------------------------------------------------------------
# url2hmonth
#--------------------------------------------------------------------------------
def url2hmonth(URL,DATE_FORMAT,date_lim):

    # Set start,end time in half-monthly date
    year_lim  = [date_lim[0].year ,date_lim[1].year ]
    hm_lim    = [101,1216]
    hm_lim_in = [date_lim[0].month*100+15*(date_lim[0].day//16)+1,
                 date_lim[1].month*100+15*(date_lim[1].day//16)+1]
    
    # Set half month's number list
    hm_all = np.array([[1],[ 1]])*np.linspace(1,12,12)*100+\
             np.array([[1],[16]])*np.ones([2,12])
    hm_all = np.sort(hm_all.flatten().astype("uint16"))

    # Detect url, id
    stac_date_url, date_id = detect_url_id(URL,DATE_FORMAT,year_lim,hm_lim,hm_lim_in,hm_all)

    # Return
    return stac_date_url, date_id

#--------------------------------------------------------------------------------
# url2doy
#--------------------------------------------------------------------------------
def url2doy(URL,DATE_FORMAT,date_lim):

    # Set start,end time in monthly date
    year_lim   = [date_lim[0].year ,date_lim[1].year ]
    doy_lim    = [1,366]
    doy_lim_in = [date_lim[0].timetuple().tm_yday,
                  date_lim[1].timetuple().tm_yday]
    doy_all    = np.linspace(1,366,366)

    # Detect url, id
    stac_date_url, date_id = detect_url_id(URL,DATE_FORMAT,year_lim,
                                           doy_lim,doy_lim_in,doy_all)

    # Output
    return stac_date_url, date_id

#--------------------------------------------------------------------------------
# detect_url_id
#--------------------------------------------------------------------------------
def detect_url_id(URL,DATE_FORMAT,year_lim,date_lim,date_lim_in,date_all):

    # Set parameters
    str_len1 = len(DATE_FORMAT)
    str_len2 = len("catalog.json")    

    # Detect each years day number
    years = np.linspace(year_lim[0],year_lim[1],year_lim[1]-year_lim[0]+1)
    
    # Make date list
    dates = []
    for i in range(len(years)):

        # Update date0 if type is DDD (day of year)
        if DATE_FORMAT == "DDD":
            date_lim[1] = (datetime.datetime(int(years[i]),12,31)-\
                           datetime.datetime(int(years[i]), 1, 1)).days+1

        # Set start date
        if i == 0:
            date0 = date_lim_in[0]
        else:
            date0 = date_lim[0]
        
        # Set end date
        if i == len(years)-1:
            date1 = date_lim_in[1]
        else:
            date1 = date_lim[1]
        
        # Make dates, append
        idx   = (date0 <= date_all) & (date_all <= date1)
        dates = np.append(dates,date_all[idx])

    # Extract all date id
    date_id_tmp = []
    date_id_num = []
    for i in range(len(URL)):
        date_id_tmp_tmp = URL[i][-(str_len1+str_len2+1):-str_len2]
        date_id_num_tmp = int(date_id_tmp_tmp[:-1].replace("-",""))
        date_id_tmp.append(date_id_tmp_tmp) 
        date_id_num.append(date_id_num_tmp)

    # Allocate every date_id and URL to date's data
    stac_date_url = []
    date_id       = []
    for i in range(len(dates)):
        if dates[i] in date_id_num:
            idx = date_id_num.index(dates[i])
            stac_date_url.append([URL[idx]])
            date_id.append(date_id_tmp[idx])

    # Output
    return stac_date_url, date_id