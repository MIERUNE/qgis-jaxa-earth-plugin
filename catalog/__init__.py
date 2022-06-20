"""
    disabled: can't get image
    "Copernicus.C3S_PROBA-V_LCCS_global_yearlly": {
        "title": "Land Cover Class (Yearly)",
        "bands": ["LCCS"],
        "keywords": ["Landcover", "VGT-P", "PROBA-V", "ESA"],
    },
"""
CATALOG = {
    "JAXA.EORC_ALOS.PRISM_AW3D30.v2012_global": {
        "title": "Digital Surface Model",
        "bands": ["DSM", "MSK"],
        "keywords": ["Elevation", "ALOS", "JAXA"],
    },
    "JAXA.EORC_GSMaP_standard.Gauge.00Z-23Z.v6_daily": {
        "title": "Precipitation Rate (Daily Averaged)",
        "bands": ["RainRate"],
        "keywords": ["Precipitation", "DPR", "GPM", "NASA", "JAXA"],
    },
    "JAXA.EORC_GSMaP_standard.Gauge.00Z-23Z.v6_half-monthly": {
        "title": "Precipitation Rate (Half-monthly Averaged)",
        "bands": ["RainRate"],
        "keywords": ["Precipitation", "DPR", "GPM", "NASA", "JAXA"],
    },
    "JAXA.EORC_GSMaP_standard.Gauge.00Z-23Z.v6_half-monthly-normal": {
        "title": "Precipitation Rate (Half-monthly-normal)",
        "bands": ["RainRate_2012_2021"],
        "keywords": ["Precipitation", "DPR", "GPM", "NASA", "JAXA"],
    },
    "JAXA.EORC_GSMaP_standard.Gauge.00Z-23Z.v6_monthly": {
        "title": "Precipitation Rate (Monthly Averaged)",
        "bands": ["RainRate"],
        "keywords": ["Precipitation", "DPR", "GPM", "NASA", "JAXA"],
    },
    "JAXA.EORC_GSMaP_standard.Gauge.00Z-23Z.v6_monthly-normal": {
        "title": "Precipitation Rate (Monthly-normal)",
        "bands": ["RainRate_2012_2021"],
        "keywords": ["Precipitation", "DPR", "GPM", "NASA", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-AROT.daytime.v3_global_daily": {
        "title": "Aerosol optical thickness over land and ocean at 500 nm (Daytime/Daily)",
        "bands": ["AROT"],
        "keywords": ["AROT", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-AROT.daytime.v3_global_half-monthly": {
        "title": "Aerosol optical thickness over land and ocean at 500 nm (Daytime/Half-monthly)",
        "bands": ["AROT"],
        "keywords": ["AROT", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-AROT.daytime.v3_global_monthly": {
        "title": "Aerosol optical thickness over land and ocean at 500 nm (Daytime/Monthly)",
        "bands": ["AROT"],
        "keywords": ["AROT", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-LST.daytime.v3_global_daily": {
        "title": "Land surface temperature (Daytime/Daily)",
        "bands": ["LST"],
        "keywords": ["LST", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-LST.daytime.v3_global_half-monthly": {
        "title": "Land surface temperature (Daytime/Half-monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-LST.daytime.v3_global_monthly": {
        "title": "Land surface temperature (Daytime/Monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-LST.nighttime.v3_global_daily": {
        "title": "Land surface temperature (Nighttime/Daily)",
        "bands": ["LST"],
        "keywords": ["LST", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-LST.nighttime.v3_global_half-monthly": {
        "title": "Land surface temperature (Nighttime/Half-monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-LST.nighttime.v3_global_monthly": {
        "title": "Land surface temperature (Nighttime/Monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-NDVI.daytime.v3_global_daily": {
        "title": "Normalized Difference Vegetation Index (Daytime/Daily)",
        "bands": ["NDVI"],
        "keywords": ["NDVI", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-NDVI.daytime.v3_global_half-monthly": {
        "title": "Normalized Difference Vegetation Index (Daytime/Half-monthly)",
        "bands": ["NDVI"],
        "keywords": ["NDVI", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-NDVI.daytime.v3_global_monthly": {
        "title": "Normalized Difference Vegetation Index (Daytime/Monthly)",
        "bands": ["NDVI"],
        "keywords": ["NDVI", "SGLI", "GCOM-C", "GCOM", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-C.SGLI_standard.L3-RGB.daytime.v3_global_monthly": {
        "title": "Surface Reflectance RGB (Daytime/Monthly)",
        "bands": ["RGB1", "RGB4"],
        "keywords": ["Reflectance", "SGLI", "GCOM-C", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.daytime.v3_global_daily": {
        "title": "Soil Moisture Content (Daytime/Daily)",
        "bands": ["SMC"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.daytime.v3_global_half-monthly": {
        "title": "Soil Moisture Content (Daytime/Half-monthly)",
        "bands": ["SMC"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.daytime.v3_global_half-monthly-normal": {
        "title": "Soil Moisture Content (Daytime/Half-monthly-normal)",
        "bands": ["SMC_2012_2021"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.daytime.v3_global_monthly": {
        "title": "Soil Moisture Content (Daytime/Monthly)",
        "bands": ["SMC"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.daytime.v3_global_monthly-normal": {
        "title": "Soil Moisture Content (Daytime/Monthly-normal)",
        "bands": ["SMC_2012_2021"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.nighttime.v3_global_daily": {
        "title": "Soil Moisture Content (Nighttime/Daily)",
        "bands": ["SMC"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.nighttime.v3_global_half-monthly": {
        "title": "Soil Moisture Content (Nighttime/Haf-monthly)",
        "bands": ["SMC"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.nighttime.v3_global_half-monthly-normal": {
        "title": "Soil Moisture Content (Nighttime/Haf-monthly-normal)",
        "bands": ["SMC_2012_2021"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.nighttime.v3_global_monthly": {
        "title": "Soil Moisture Content (Nighttime/Monthly)",
        "bands": ["SMC"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.nighttime.v3_global_monthly-normal": {
        "title": "Soil Moisture Content (Nighttime/Monthly-normal)",
        "bands": ["SMC_2012_2021"],
        "keywords": ["SMC", "AMSR2", "GCOM-W", "JAXA"],
    },
    "JAXA.JASMES_Aqua.MODIS_swr.v811_global_daily": {
        "title": "Shortwave Radiation (Aqua MODIS/Daily)",
        "bands": ["swr"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Aqua.MODIS_swr.v811_global_half-monthly": {
        "title": "Shortwave Radiation (Aqua MODIS/Half-monthly)",
        "bands": ["swr"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Aqua.MODIS_swr.v811_global_half-monthly-normal": {
        "title": "Shortwave Radiation (Aqua MODIS/Half-monthly-normal)",
        "bands": ["swr_2012_2021"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Aqua.MODIS_swr.v811_global_monthly": {
        "title": "Shortwave Radiation (Aqua MODIS/Monthly)",
        "bands": ["swr"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Aqua.MODIS_swr.v811_global_monthly-normal": {
        "title": "Shortwave Radiation (Aqua MODIS/Monthly-normal)",
        "bands": ["swr_2012_2021"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_ndvi.v811_global_half-monthly": {
        "title": "Normalized Difference Vegetation Index (Half-monthly)",
        "bands": ["ndvi"],
        "keywords": ["NDVI", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_ndvi.v811_global_half-monthly-normal": {
        "title": "Normalized Difference Vegetation Index (Half-monthly-normal)",
        "bands": ["ndvi_2012_2021"],
        "keywords": ["NDVI", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_ndvi.v811_global_monthly": {
        "title": "Normalized Difference Vegetation Index (Monthly)",
        "bands": ["ndvi"],
        "keywords": ["NDVI", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_ndvi.v811_global_monthly-normal": {
        "title": "Normalized Difference Vegetation Index (Monthly-normal)",
        "bands": ["ndvi_2012_2021"],
        "keywords": ["NDVI", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_taua.v811_global_daily": {
        "title": "Aerosol Optical Depth at 500 nm (Terra & Aqua MODIS average/Daily)",
        "bands": ["taua"],
        "keywords": ["AOD", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_taua.v811_global_half-monthly": {
        "title": "Aerosol Optical Depth at 500 nm (Terra & Aqua MODIS average/Half-monthly)",
        "bands": ["taua"],
        "keywords": ["AOD", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_taua.v811_global_half-monthly-normal": {
        "title": "Aerosol Optical Depth at 500 nm (Terra & Aqua MODIS average/Half-monthly-normal)",
        "bands": ["taua_2012_2021"],
        "keywords": ["AOD", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_taua.v811_global_monthly": {
        "title": "Aerosol Optical Depth at 500 nm (Terra & Aqua MODIS average/Monthly)",
        "bands": ["taua"],
        "keywords": ["AOD", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS-Aqua.MODIS_taua.v811_global_monthly-normal": {
        "title": "Aerosol Optical Depth at 500 nm (Terra & Aqua MODIS average/Monthly-normal)",
        "bands": ["taua_2012_2021"],
        "keywords": ["AOD", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS_swr.v811_global_daily": {
        "title": "Shortwave Radiation (Terra MODIS/Daily)",
        "bands": ["swr"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS_swr.v811_global_half-monthly": {
        "title": "Shortwave Radiation (Terra MODIS/Half-monthly)",
        "bands": ["swr"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS_swr.v811_global_half-monthly-normal": {
        "title": "Shortwave Radiation (Terra MODIS/Half-monthly-normal)",
        "bands": ["swr_2012_2021"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS_swr.v811_global_monthly": {
        "title": "Shortwave Radiation (Terra MODIS/Monthly)",
        "bands": ["swr"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_Terra.MODIS_swr.v811_global_monthly-normal": {
        "title": "Shortwave Radiation (Terra MODIS/Monthly-normal)",
        "bands": ["swr_2012_2021"],
        "keywords": ["SWR", "MODIS", "JASMES", "JAXA"],
    },
    "JAXA.JASMES_ic0.v201_north_daily": {
        "title": "Sea Ice Concentration (5-day Averaged/Daily)",
        "bands": ["IC0"],
        "keywords": ["IC0", "AMSR2", "WindSat ", "AMSR-E ", "SSM/I", "SMMR"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.daytime.v061_global_daily": {
        "title": "Land Surface Temperature (Aqua MODIS/Daytime/Daily)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.daytime.v061_global_half-monthly": {
        "title": "Land Surface Temperature (Aqua MODIS/Daytime/Haf-monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.daytime.v061_global_half-monthly-normal": {
        "title": "Land Surface Temperature (Aqua MODIS/Daytime/Haf-monthly-normal)",
        "bands": ["LST_2012_2021"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.daytime.v061_global_monthly-normal": {
        "title": "Land Surface Temperature (Aqua MODIS/Daytime/Monthly-normal)",
        "bands": ["LST_2012_2021"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.nighttime.v061_global_daily": {
        "title": "Land Surface Temperature (Aqua MODIS/Nighttime/Daily)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.nighttime.v061_global_half-monthly": {
        "title": "Land Surface Temperature (Aqua MODIS/Nighttime/Haf-monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.nighttime.v061_global_half-monthly-normal": {
        "title": "Land Surface Temperature (Aqua MODIS/Nighttime/Haf-monthly-normal)",
        "bands": ["LST_2012_2021"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.nighttime.v061_global_monthly-normal": {
        "title": "Land Surface Temperature (Aqua MODIS/Nighttime/Monthly-normal)",
        "bands": ["LST_2012_2021"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C2-LST.daytime.v061_global_8-day": {
        "title": "Land Surface Temperature (Aqua MODIS/Daytime/8-day)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C2-LST.nighttime.v061_global_8-day": {
        "title": "Land Surface Temperature (Aqua MODIS/Nighttime/8-day)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C3-LST.daytime.v061_global_monthly": {
        "title": "Land Surface Temperature (Aqua MODIS/Daytime/Monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Aqua.MODIS_MYD11C3-LST.nighttime.v061_global_monthly": {
        "title": "Land Surface Temperature (Aqua MODIS/Nighttime/Monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.daytime.v061_global_daily": {
        "title": "Land Surface Temperature (Terra MODIS/Daytime/Daily)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.daytime.v061_global_half-monthly": {
        "title": "Land Surface Temperature (Terra MODIS/Daytime/Haf-monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.daytime.v061_global_half-monthly-normal": {
        "title": "Land Surface Temperature (Terra MODIS/Daytime/Haf-monthly-normal)",
        "bands": ["LST_2012_2021"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.daytime.v061_global_monthly-normal": {
        "title": "Land Surface Temperature (Terra MODIS/Daytime/Monthly-normal)",
        "bands": ["LST_2012_2021"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.nighttime.v061_global_daily": {
        "title": "Land Surface Temperature (Terra MODIS/Nighttime/Daily)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.nighttime.v061_global_half-monthly": {
        "title": "Land Surface Temperature (Terra MODIS/Nighttime/Haf-monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.nighttime.v061_global_half-monthly-normal": {
        "title": "Land Surface Temperature (Terra MODIS/Nighttime/Haf-monthly-normal)",
        "bands": ["LST_2012_2021"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.nighttime.v061_global_monthly-normal": {
        "title": "Land Surface Temperature (Terra MODIS/Nighttime/Monthly-normal)",
        "bands": ["LST_2012_2021"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C2-LST.daytime.v061_global_8-day": {
        "title": "Land Surface Temperature (Terra MODIS/Daytime/8-day)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C2-LST.nighttime.v061_global_8-day": {
        "title": "Land Surface Temperature (Terra MODIS/Nighttime/8-day)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C3-LST.daytime.v061_global_monthly": {
        "title": "Land Surface Temperature (Terra MODIS/Daytime/Monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
    "NASA.EOSDIS_Terra.MODIS_MOD11C3-LST.nighttime.v061_global_monthly": {
        "title": "Land Surface Temperature (Terra MODIS/Nighttime/Monthly)",
        "bands": ["LST"],
        "keywords": ["LST", "MODIS", "NASA"],
    },
}
