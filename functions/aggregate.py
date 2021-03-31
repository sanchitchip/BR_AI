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
    """This function will create a data frame for index plot. 
    The row of data frame represents the index of blobs(heat island area), and
    the column of the data frame represents the timestamp.
    
    Args:
        param island_aggregate_data: each element of list is a 4 dim-[time,weight,height,bands]np.array.
        type data: list.
        
        param timestamp: each element of the timstamp is the the timestamp of the data, can get from the EOpatch.
        type timestamp: list.
        
        param bbox: filter size of AOI.
        type bbox: list.

        param index_name: the index want to calculate]. Defaults to 'ndvi'.
        type index_name: list.
        
        param YEARS:the years you want to include. Will be the column name 
        type YEARS: list
    Returns:
       pd.DataFrame: each element of The row of data frame represents the index of blobs(heat island area), and
    the column of the data frame represents the timestamp.
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
    """[get the coord for each blobs, used for prepare plot.]

    Args:
        param island_aggregate_data: each element of list is a 4 dim-[time,weight,height,bands]np.array.
        type data: list.
        
        param timestamp: each element of the timstamp is the the timestamp of the data, can get from the EOpatch.
        type timestamp: list.
        
        param bbox: filter size of AOI.
        type bbox: list.

        param filter_shape: default = 20
        type filter_shape: int. 
        
    Returns:
       list: each element of the list is the coordinate for the xarray.
    """    
    
    _bbox = [list(i) for i in bbox]
    # save all the plot data.frame as a list.
    coord_data = []
    
    # for each data, we create a data.frame to save all the coordinate index.
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
        # append each data.frame to list.
        coord_data.append(coord_sub_dict)
    
    return coord_data
    
    
def get_line_data(df,type='mean'):
    """get the data for line chart, each element is only one single value,
    representing the index value of corresponding blob index in the corresponding year.

    Args:
    param df: each element of The row of data frame represents the index of blobs(heat island area), and
    the column of the data frame represents the timestamp].
    type df: pd.DataFrame

    param type: the type of calculate the index of the area.
                'mean' represents use the mean value as the whole area to plot the line chart.
    type type: string
    
    Returns:
       pd.DataFrame: each element of The row of data frame represents the index value of blobs(heat island area), and
    the column of the data frame represents the timestamp.
    """
    # assert index
    assert type in ['mean','max','min'], "Please enter 'mean','max' or 'min'"
    # copy data
    return_df = df.copy(deep=True)
    # get the number of row and column
    row,column = df.shape
    # three different types to aggregate the matrix into one single value
    # because line chart only need one single value for each plot.
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