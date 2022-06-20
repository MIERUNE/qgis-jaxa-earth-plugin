#--------------------------------------------------------------------------------
# Load module
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# select_features
#--------------------------------------------------------------------------------
def select_features(geoj_all,keywords):

    # Get all properties
    prop_all = []
    for i in range(len(geoj_all)):
        tmp_list = list(geoj_all[i]["properties"].values())
        tmp_str  = "_".join([str(tmp_list[i]) for i in range(len(tmp_list))])
        prop_all.append(tmp_str)

    # Extract geojson
    geoj,prop = [],[]
    for i in range(len(prop_all)):
        if all([x in prop_all[i] for x in keywords]):
            geoj.append(geoj_all[i])
            prop.append(prop_all[i])

    # Output
    return geoj


