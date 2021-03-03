import io_pipe
from functools import reduce,partial
import nd_index


def get_overlap_date_mask(heat_data:list) ->list:
    """[summary]

    Args:
        heat_data (list): list of eopatch

    Returns:
        list: [description]
    """
    # get all date of each area, combine as a list
    all_date = [sub.timestamp for sub in heat_data]
    for index,sub_date in enumerate(all_date):
        sub_date = [dt.date(single_date) for single_date in sub_date]
        all_date[index] = sub_date
    
    # get the overlap_date
    overlap_date = list(reduce(set.intersection,map(set,all_date)))
    
    # create a mask date list for every data.
    date_mask = []
    for date in all_date:
        date_sub_mask = [one_date in overlap_date for one_date in date]
        date_mask.append(date_sub_mask)
        
    return date_mask



def get_masked_raw_data(heat_data:list, date_mask:list)->list:
    """[summary]

    Args:
        heat_data (list): list of eopatch
        date_mask (list): [description]

    Returns:
        list: [description]
    """
    # get raw data of each 
    raw_data = [io_pipe.get_raw(sub) for sub in heat_data]
    # using mask to get the masked data, combine as a list.
    masked_raw_data = []
    for index,sub_raw_data in enumerate(raw_data):
        masked_raw_data.append(sub_raw_data[date_mask[index],:])
    
    return masked_raw_data



def get_years_date_mask(heat_data:list,year:int)->list:
    """[summary]

    Args:
        heat_data (list): [description]
        year (int): [description]

    Returns:
        list: [description]
    """
    # get all date of each area, combine as a list
    all_date = [sub.timestamp for sub in heat_data]
    for index,sub_date in enumerate(all_date):
        sub_date = [dt.date(single_date) for single_date in sub_date]
        all_date[index] = sub_date
    
    # get the overlap_date
    overlap_date = list(reduce(set.intersection,map(set,all_date)))
    
    
    year_date_mask = []
    for date in all_date:
        year_date_sub_mask = [one_date in overlap_date and one_date.year==year for one_date in date]
        year_date_mask.append(year_date_sub_mask)
        
    return year_date_mask


    
def get_year_plot_data(masked_raw_data:list,index='ndvi',satellite='landsat8',c=1e-8):
    """[summary]

    Args:
        masked_raw_data (list): [description]
        index (str, optional): [description]. Defaults to 'ndvi'.
        satellite (str, optional): [description]. Defaults to 'landsat8'.
        c ([type], optional): [description]. Defaults to 1e-8.

    Returns:
        [type]: [description]
    """
    # create a dict to return function
    index_dict = {"ndvi":partial(nd_index.calc_ndvi,satellite=satellite,c=c),
                  "ndwi":partial(nd_index.calc_ndwi,satellite=satellite,c=c)}
    
    # get the index function we will use
    calc_fun = index_dict[index]
    
    # calculate the plot data
    index_data = [calc_fun(sub_data) for sub_data in masked_raw_data]
    
    return index_data


def get_plot_df(heat_data:list,years:list,index='ndvi',satellite='landsat8',c=1e-8):
    """[summary]

    Args:
        heat_data (list): [description]
        years (list): [description]
        index (str, optional): [description]. Defaults to 'ndvi'.
        satellite (str, optional): [description]. Defaults to 'landsat8'.
        c ([type], optional): [description]. Defaults to 1e-8.

    Returns:
        [type]: [description]
    """
    plot_df = pd.DataFrame()

    for year in years:
        year_date_mask = get_years_date_mask(heat_data,year)
        all_raw_data = get_masked_raw_data(heat_data, year_date_mask)
        year_plot_data = get_year_plot_data(all_raw_data,index=index,satellite=satellite)
        plot_df[str(year)] = year_plot_data
        
    return plot_df

        
        
        
        
        
        
        
