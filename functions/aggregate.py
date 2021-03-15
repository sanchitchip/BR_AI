import sys
sys.path.insert(1, "../functions/")
import io_pipe
import nd_index
import filter
import plot_utils
import numpy as np
import pandas as pd
from shapely import geometry
import geopandas as gpd
from datetime import datetime as dt
from functools import reduce, partial
import xarray as xr


def get_index_plot_data(island_aggregate_data:list,timestamp:list,bbox:list,index_name='ndvi',YEARS = [2014, 2015, 2016, 2017, 2018]):
    """[Creating Data.Frame for index plot]

    Args:
        island_aggregate_data (list): [description]
        timestamp (list): [description]
        bbox (list): [description]
        index_name (str, optional): [description]. Defaults to 'ndvi'.
        YEARS (list, optional): [description]. Defaults to [2014, 2015, 2016, 2017, 2018].

    Returns:
        [type]: [description]
    """
    # get the timestamp for the data
    years_timestamp = [dt.date(i) for i in timestamp]

    # get the coord_data for xarray
    coord_data = get_plot_coord(bbox=bbox,island_aggregate_data=island_aggregate_data)
    # run for each years (as column of df)

    # 
    plot_df = pd.DataFrame()
    for year in YEARS:
        index_one_year = [year == sub_year.year for sub_year in years_timestamp]
        index_data_all_land_one_year = []
        for index,data_one_land in enumerate(island_aggregate_data):
            # data_one_land_one_year has shape [time,weidth,height,bands]
            data_one_land_one_year = data_one_land[index_one_year]
            if index_name=='ndvi':
                index_data_one_land_one_year = nd_index.calc_ndvi(data_one_land_one_year)
            if index_name=='ndwi':
                index_data_one_land_one_year = nd_index.calc_ndwi(data_one_land_one_year)
            if index_name=='temp':
                index_data_one_land_one_year = nd_index.calc_lst(data_one_land_one_year) 

            # create xarray
            # xr_time = [sub_year for sub_year in years_timestamp if sub_year.year==year]
            # space_lati = coord_data[index]['space_lati']
            # space_long = coord_data[index]['space_long']
            # xr_array = xr.DataArray(index_data_one_land_one_year,coords=[xr_time,space_lati,space_long],dims=['time','lati','long'])
            # # create all land xarray as column our data.frame
            index_data_all_land_one_year.append(index_data_one_land_one_year)

        plot_df[str(year)] = index_data_all_land_one_year

    return plot_df




def get_plot_coord(bbox:list,island_aggregate_data:list,filter_shape=20)->list:
    """[get the coord for xarray]

    Args:
        bbox (list): [description]
        heat_data (list): [description]

    Returns:
        list: [return a list,whose element is all the  information of coord of one area]
    """
    _bbox = [list(i) for i in bbox]
    coord_data = []
    for index,sub_data in enumerate(island_aggregate_data):
        sub_size_long = 2*filter_shape
        sub_size_lati = 2*filter_shape
        long = _bbox[index][::2]
        lati = _bbox[index][1::2]
        space_long, diff_long = np.linspace(*long, sub_size_long, retstep=True)
        space_lati, diff_lati = np.linspace(*lati, sub_size_lati, retstep=True)
        
        coord_sub_dict = {'space_long':space_long,
                          'space_lati':space_lati, 
                          'diff_long':diff_long,
                          'diff_lati':diff_lati}
        coord_data.append(coord_sub_dict)
    
    return coord_data

    
def get_line_data(df,type='mean'):
    """[summary]

    Args:
        df ([type]): [description]
        type (str, optional): [description]. Defaults to 'mean'.

    Returns:
        [type]: [description]
    """
    # copy data
    return_df = df.copy(deep=True)
    row,column = df.shape
    if type == 'max':
        fun = np.max
    if type == 'mean':
        fun = np.mean
    if type == 'min':
        fun = np.min
    for r in range(row):
        for c in range(column):
            return_df.iloc[r,c] = fun(df.iloc[r,c])
    
    return return_df