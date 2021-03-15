import io_pipe
import nd_index
from datetime import datetime as dt
from functools import reduce, partial
import numpy as np
import xarray as xr


def get_island_submatrix(data,blobs,filter_shape=20,dim_error=False):
    """This function return the sub_matrix of data.

    Args:
        data ([ndarray]): [description]
        blobs ([type]): [description]
        filter_shape (int, optional): [description]. Defaults to 20.
        dim_error (bool, optional): [description]. Defaults to False.

    Returns:
        [ndarray]: all the raw data of image,has shape (21,9,20,20,12), where 21 means 21 blobs.
    """
    vfin = []
    for i in range(len(blobs)):
        y,x,_ = blobs[i]
        y,x = int(y),int(x)
        if dim_error and i==0:
            vfin.append(data[:,y-filter_shape-8:y+filter_shape,x-filter_shape:x+filter_shape,:])
        else:
            vfin.append(data[:,y-filter_shape:y+filter_shape,x-filter_shape:x+filter_shape,:])

    return vfin






# def get_plot_df(heat_data: list, years: list, index='ndvi', satellite='landsat8', c=1e-8):
#     """[summary]

#     Args:
#         heat_data (list): [description]
#         years (list): [description]
#         index (str, optional): [description]. Defaults to 'ndvi'.
#         satellite (str, optional): [description]. Defaults to 'landsat8'.
#         c ([type], optional): [description]. Defaults to 1e-8.

#     Returns:
#         [pandas.DataFrame]: each row is the plot_data for one pixel in different years
#     """
#     plot_df = pd.DataFrame()

#     for year in years:
#         year_date_mask = get_years_date_mask(heat_data, year)
#         all_raw_data = get_masked_raw_data(heat_data, year_date_mask)
#         year_plot_data = get_year_plot_data(
#             all_raw_data, index=index, satellite=satellite)
#         plot_df[str(year)] = year_plot_data

#     return plot_df


# def get_overlap_date_mask(heat_data: list) -> list:
#     """[summary]

#     Args:
#         heat_data (list): list of eopatch

#     Returns:
#         list: each element is a mask list that whether the date of the corresponding
#         data is in the overlap_date.
#     """
#     # get all date of each area, combine as a list
#     all_date = [sub.timestamp for sub in heat_data]
#     for index, sub_date in enumerate(all_date):
#         sub_date = [dt.date(single_date) for single_date in sub_date]
#         all_date[index] = sub_date

#     # get the overlap_date
#     overlap_date = list(reduce(set.intersection, map(set, all_date)))

#     # create a mask date list for every data.
#     date_mask = []
#     for date in all_date:
#         date_sub_mask = [one_date in overlap_date for one_date in date]
#         date_mask.append(date_sub_mask)

#     return date_mask

# def get_years_date_mask(heat_data: list, year: int) -> list:
#     """[summary]

#     Args:
#         heat_data (list): [description]
#         year (int): [description]

#     Returns:
#         list: each element is a mask list that whether the date of the corresponding
#         data is in the overlap_date.
#     """
#     # get all date of each area, combine as a list
#     all_date = [sub.timestamp for sub in heat_data]
#     for index, sub_date in enumerate(all_date):
#         sub_date = [dt.date(single_date) for single_date in sub_date]
#         all_date[index] = sub_date

#     # get the overlap_date
#     overlap_date = list(reduce(set.intersection, map(set, all_date)))
    
#     # from the overlap_date, we select the date in coresponding year.
#     year_date_mask = []
#     for date in all_date:
#         year_date_sub_mask = [
#             one_date in overlap_date and one_date.year == year for one_date in date]
#         year_date_mask.append(year_date_sub_mask)

#     return year_date_mask


# def get_masked_raw_data(heat_data: list, date_mask: list) -> list:
#     """[summary]

#     Args:
#         heat_data (list): list of eopatch
#         date_mask (list): [description]

#     Returns:
#         list: [description]
#     """
#     # get raw data of each
#     raw_data = [io_pipe.get_raw(sub) for sub in heat_data]
#     # using mask to get the masked data, combine as a list.
#     masked_raw_data = []
#     for index, sub_raw_data in enumerate(raw_data):
#         masked_raw_data.append(sub_raw_data[date_mask[index], :])

#     return masked_raw_data


# def get_year_plot_data(masked_raw_data: list, index='ndvi', satellite='landsat8', c=1e-8,daily_mean=False):
#     """[summary]

#     Args:
#         masked_raw_data (list): [description]
#         index (str, optional): [description]. Defaults to 'ndvi'.
#         satellite (str, optional): [description]. Defaults to 'landsat8'.
#         c ([type], optional): [description]. Defaults to 1e-8.

#     Returns:
#         [type]: [description]
#     """
#     # create a dict to return function
#     index_dict = {"ndvi": partial(nd_index.calc_ndvi, satellite=satellite, c=c),
#                   "ndwi": partial(nd_index.calc_ndwi, satellite=satellite, c=c)}

#     # get the index function we will use
#     calc_fun = index_dict[index]

#     # calculate the plot data
#     if daily_mean:
#         index_data = [np.mean(calc_fun(sub_data)) for sub_data in masked_raw_data] 
    
#     if not daily_mean:
#         index_data = [calc_fun(sub_data) for sub_data in masked_raw_data]
    
    
#     return index_data




# def get_plot_coord(bbox:list,heat_data:list)->list:
#     """[summary]

#     Args:
#         bbox (list): [description]
#         heat_data (list): [description]

#     Returns:
#         list: [description]
#     """
#     coord_data = []
#     for index,sub_data in enumerate(heat_data):
#         sub_size_long = sub_data.meta_info['size_x']
#         sub_size_lati = sub_data.meta_info['size_y']
#         long = bbox[index][::2]
#         lati = bbox[index][1::2]
#         space_long, diff_long = np.linspace(*long, sub_size_long, retstep=True)
#         space_lati, diff_lati = np.linspace(*lati, sub_size_lati, retstep=True)
        
#         coord_sub_dict = {'space_long':space_long,
#                           'space_lati':space_lati, 
#                           'diff_long':diff_long,
#                           'diff_lati':diff_lati}
#         coord_data.append(coord_sub_dict)
    
#     return coord_data



# def get_masked_time(heat_data: list, date_mask: list) -> list:
    
#     masked_time = []
#     for index,sub in enumerate(heat_data):
#         sub_date_mask = date_mask[index]
#         sub_date =  sub.timestamp[sub_date_mask]
#         masked_time.append(sub_date)
        
#     return masked_time
    
    


# def get_plot_xarray(df,coord_data,masked_time,pixel_index:int,year:int):
#     """[summary]

#     Args:
#         df ([type]): [description]
#         coord_data ([type]): [description]
#         masked_time ([type]): [description]
#         pixel_index (int): [description]
#         year (int): [description]

#     Returns:
#         [type]: [description]
#     """
#     plot_data = df.loc[pixel_index,str(year)]
#     xr_time = masked_time[pixel_index]
#     space_lati = coord_data[pixel_index]['space_lati']
#     space_long = coord_data[pixel_index]['space_long']
#     xr_array = xr.DataArray(plot_data,coords=[xr_time,space_lati,space_long],dims=['time','lati','long'])
    
#     return xr_array



