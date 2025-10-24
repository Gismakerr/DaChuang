import h5py
import numpy as np
import pandas as pd
import xarray as xr
from Utils import *
from  Download import *
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
auth = earthaccess.login()

SWOT_Data_Dictionary = {
    "SWOT_L1B_HR_SLC_017_350_037R_20240701T125608_20240701T125616_PIC0_01.nc": None,
    "SWOT_L2_HR_PIXC_010_106_086R_20240128T183540_20240128T183551_PIC0_01.nc": None,
    "SWOT_L2_HR_PIXCVec_010_106_086R_20240128T183540_20240128T183551_PIC0_01.nc": None,
    "SWOT_L2_HR_RiverSP_Node_001_313_GR_20230801T095053_20230801T095102_PGC0_01.zip": "*Node*_GR_*",
    "SWOT_L2_HR_RiverSP_Reach_016_089_GR_20240601T090328_20240601T090336_PIC0_01.zip": "*Reach*_GR_*",
    "SWOT_L2_HR_LakeSP_Prior_013_145_GR_20240401T184641_20240401T185132_PIC0_01.zip": "*Prior*_GR_*",
    "SWOT_L2_HR_Raster_250m_UTM23V_N_x_x_x_017_406_021F_20240703T125800_20240703T125808_PIC0_01.nc": "*100m**563_138F*"
}

start_date = "2023-10-04"
end_date = "2023-10-06"
extent_path = r"E:\Haoyu_space\05_Presentation\End_of_Septemple\extent\冰川范围.shp"
short_name = "SWOT_L2_HR_PIXC_2.0"
granule_name = "*Node*_GR_*"
download_dir = r"E:\Haoyu_space\07_Presentation\End_of_Septemple\Watson_PIXCVec"
results = search_swot_data("2023-10-04", "2023-10-06", extent_path, short_name = short_name, granule_pattern = granule_name)
download_swot_granules(results, download_dir)