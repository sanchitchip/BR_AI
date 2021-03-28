from eolearn.core import EOPatch
import numpy as np
import sys
import pdb
sys.path.insert(1,'../functions')
import io_pipe
import nd_index
import lst
import plot_utils
from matplotlib import pyplot as plt
import geopandas as gpd
from sentinelhub import BBox, CRS, DataCollection, SHConfig
import pdb


## -- for testing 
# 1.) check type of image_height,width
# 2.) check type of bbox
# 3.) if any input value is None return value error.

def get_coord_matrix(image_width,image_height,bbox):
    """ This functions returns tuples of list where each list tells latitude or longitude values of a particular pixel
    Args:
        param image_width: width of image
        type image_width: int.

        param image_height: height of image
        type image_height: int.
        
        bbox: BBox using which the satellite image was generated. or the diagonal geo-coordinates of the 
                image
        type bbox: sentinelhub bbox object.
        
    Returns: 
         returns the  geo coodinates of a coordinates of a given pixel in an image
    """

    #!!!!! be careful what does the width and height individually correspond to? long or lati?
    if all([image_width,image_height,BBox]):
        raise TypeError

    bounds = tuple(bbox)
    long_shape = image_width 
    lati_shape = image_height 
    long = bounds[::2]
    lati = bounds[1::2]
    space_long,diff_long = np.linspace(*long,long_shape,retstep=True)
    space_lati,diff_lati = np.linspace(*lati,lati_shape,retstep=True)
    distance = [diff_long, diff_lati]
    return (space_long,space_lati), distance




## -- for testing 
# 1.) check type of geo_matrix
# 2.) check type of index_pixel and check if value is None or not in case of none return value error
def get_geoindex(geo_matrix, index_pixel):
    """ This functions returns geo-coordinates of pixels of image coordinate.
    Args:
        param geo_matrix: this is a tuple which tells us which image coordinate corresponds
                          to which geo-coordinates.
        type geo_matrix: tuple of 2 list.
        
        param index_pixel: coordinates of our reqired point in image.
        type index_pixel: tuple.
        
    Returns: 
         returns the  geo coodinates of a coordinates of a given pixel in an image
    """
    if all([geo_matrix,index_pixel]):
        raise TypeError
    vX_geo = geo_matrix[0][index_pixel[0]]
    vL = len(geo_matrix[1])
    # instead of using this modify the y as difference value.
    vY_geo = geo_matrix[1][index_pixel[1]]
    #vY_geo = geo_matrix[1][vL - index_pixel[1]]
    
    return (vX_geo,vY_geo)
 #   return list(geo1,geo2,...)

    
def get_patch(geo_matrix,index_pixel,filter_size=20):
    """ This functions returns pixel coordinates of diagonal patch which is used to compute bbox
    for possible heat islands

    Args:
        param geo_matrix: this is a tuple which tells us which image coordinate corresponds
                          to which geo-coordinates.
        type geo_matrix: tuple of 2 list.
        
        param index_pixel: coordinates of our reqired point in image.
        type index_pixel: tuple.
        
        param filter_size: filter size of AOI.
        type filter_size: int.
      
    Returns:
        returns tuple of pixel coordinates of diagonal patch
    """
    
    # geo = (long: image_width,lati: image_height)
    if all([geo_matrix,index_pixel]):
        raise TypeError
    image_width,image_height = [len(i) for i in geo_matrix]
    x,y = index_pixel
    vX_max = index_pixel[0]+20
    vX_min = index_pixel[0]-20
    vY_max = index_pixel[1]+20
    vY_min = index_pixel[1]-20    
    if y+20>image_height:
        vY_max = image_height-1
        vY_min = vY_max-2*filter_size
    if y-20<0:
        vY_min = 0
        vdiff = filter_size - y
        vY_max = vY_min +2*filter_size
    ## doing the same for x    
    if x+20>image_width:
        vX_max = image_width -1
#        vdiff = filte_size + image_width-x
        vX_min = vX_max-2*filter_size
    if x-20<0:
        vY_min = 0        
#        vdiff = filter_size - x
        vY_max = vY_min+2*filter_size
    return (vX_max,vY_max,vX_min,vY_min)

## -- for testing 
# 1.) check type of geo_matrix
# 2.) check type of index_pixel and check if value is None or not in case of none return value error:Done
def make_bbox(geo_matrix,index_pixel,filter_size=20):
    """ This functions makes bbox for a particular x,y coordinates from images by first fetching their geo-coordinates 
    and converting them to BBox object.

    Args:
        param geo_matrix: this is a tuple which tells us which image coordinate corresponds
                          to which geo-coordinates.
        type geo_matrix: tuple of 2 list.
        
        param index_pixel: coordinates of our reqired point in image.
        type index_pixel: tuple.
        
        param filter_size: filter size of AOI.
        type filter_size: int.
      
    Returns:
        returns bbox of the given geo coordinates
    """
    if all([geo_matrix,index_pixel]):
        raise TypeError
    vX_max,vY_max,vX_min,vY_min = get_patch(geo_matrix,index_pixel,filter_size)
    vX_geo_max = geo_matrix[0][vX_max]
    vX_geo_min = geo_matrix[0][vX_min]
    # instead of using this modify the y as difference value.
    vL = len(geo_matrix[1])
    #vY_geo = geo_matrix[1][vL - index_pixel[1]]
    vY_geo_max = geo_matrix[1][vL - vY_max]
    vY_geo_min = geo_matrix[1][vL - vY_min]
    interested_area = (vX_geo_min,vY_geo_min,vX_geo_max,vY_geo_max)
    
    roi_bbox = BBox(bbox=interested_area, crs=CRS.WGS84)
    return roi_bbox


## -- for testing 
# 1.) check type of geo_matrix
# 2.) check type of blobs and check if value is None or not in case of none return value error
def get_bbox(geo_matrix,blobs,filter_size=20):
    """ This function returns list of bbox for the geo-coordinates of detected heat islands.

    Args:
        param geo_matrix: this is a tuple which tells us which image coordinate corresponds
                          to which geo-coordinates.
        type geo_matrix: tuple of 2 list.
        
        param blobs: list of islands candidate detected using hessian algorithm
        type blobs: list of tuple.
        
        param filter_size: filter size of AOI.
        type filter_size: int.
        
    Returns:
        returns bbox of the given geo coordinates
    """
    if all([geo_matrix,blobs]):
        raise TypeError
    vfinal=[]
    for i in range(len(blobs)):
        y,x,_ = blobs[i]
        vfinal.append(make_bbox(geo_matrix,(int(x),int(y)),filter_size))
    return vfinal

## there is a chance that this might give bad results for first image. I know the reason why and will try to fix it eventually 
## but this should work for the other functions.
## --test for testing 
# 1.) check if number of bands correct
# 2.) check if input shape is correct.
# 3.) check if blobs is of list type and not empty
def get_island_submatrix(data,blobs,filter_shape=20,dim_error=False):
    """ This function is used for Demo UI for alex

    Args:
        param data: Array of eopatch data of shape (timestamp,image_height,image_width,bands).
        type data: numpy array.
        
        param blobs: list of islands candidate detected using hessian algorithm
        type blobs: list of tuple.
        
        param filter_size: filter size of AOI.
        type filter_size: int.

        param dim_error: hack for 1st image being corrupted need a long term solution.
        type filter_size: boolean.
        
      
    Returns:
        returns numpy array of dim (Number of island,Number of Images,image_height,image_width,bands)
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




if __name__ == '__main__':

 eopatch = EOPatch.load('../data/ld8_example')
 eopatch_data = eopatch.data['L1C_data']

 vR = eopatch_data[:,:,:,3]
 vG = eopatch_data[:,:,:,2]
 vB = eopatch_data[:,:,:,1]
 vImg = np.stack([vR,vG,vB],axis =3)
 vImg = (vImg *(255/  np.max(vImg))).astype(np.uint8)
 vImg = (vImg*(3.5/255))
 f, ax = plt.subplots(1,1)
 im = ax.imshow(vImg[0],
                cmap=plt.cm.jet)

 #f.colorbar(im,orientation="horizontal",fraction=0.07)
 ## matplotlib
 ## allianz arena reference:
 # in x,y way:
 vCoord=(955,170)
 r = 2
 c = plt.Circle((vCoord[0], vCoord[1]), r*10, color='green', linewidth=2, fill=False)

 ax.add_patch(c)
 plt.show()
 _munich = gpd.read_file('../geojson/munich.geojson')
 _interested_area = _munich.geometry.unary_union
 _bbox_interested_area = _interested_area.bounds
 _roi_bbox = BBox(bbox=_bbox_interested_area, crs=CRS.WGS84)
 vM,_ = get_coord_matrix(vImg.shape[2],vImg.shape[1],_roi_bbox)
 vROI = make_bbox(vM,vCoord)
 print(vROI)
 ## longitude is width, latitude is height
 #pdb.set_trace()


 
