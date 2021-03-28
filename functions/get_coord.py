from eolearn.core import EOPatch
import numpy as np
import sys
sys.path.insert(1,'../functions')
from matplotlib import pyplot as plt
from sentinelhub import BBox, CRS, DataCollection, SHConfig


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
    if any([image_width,image_height,BBox]):
        raise TypeError("NoneType value in one of the arguments")
    if not isinstance(image_width,int):
        raise TypeError('Please provide a int for image height.')
 
    if not isinstance(image_height,int):
        raise TypeError('Please provide a int for image width.')
    
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
    if any([geo_matrix,index_pixel]):
        raise TypeError("NoneType value in one of the arguments")
    if not isinstance(geo_matrix,tuple):
        raise TypeError('Please provide a tuple for geo_matrix argument.')
 
    if not isinstance(index_pixel,tuple):
        raise TypeError('Please provide a tuple for index_pixel.')

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
    if any([geo_matrix,index_pixel]):
        raise TypeError("NoneType value in one of the arguments")

    if not isinstance(geo_matrix,tuple):
        raise TypeError('Please provide a tuple for geo_matrix argument.')
 
    if not isinstance(index_pixel,tuple):
        raise TypeError('Please provide a tuple for index_pixel.')

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
    if any([geo_matrix,index_pixel]):
        raise TypeError("NoneType value in one of the arguments")
#        raise TypeError

    if not isinstance(geo_matrix,tuple):
        raise TypeError('Please provide a tuple for geo_matrix argument.')
 
    if not isinstance(index_pixel,tuple):
        raise TypeError('Please provide a tuple for index_pixel.')
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
    if any([geo_matrix,blobs]):
        raise TypeError("NoneType value in one of the arguments")

    if not isinstance(geo_matrix,tuple):
        raise TypeError('Please provide a tuple for geo_matrix argument.')
 
    if not isinstance(blobs,tuple):
        raise TypeError('Please provide a tuple for blobs argument.')

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

    if not isinstance(data,np.ndarray):
        raise TypeError('Please provide a numpy array for data argument.')
 
    if not isinstance(blobs,tuple):
        raise TypeError('Please provide a tuple for blobs.')
    vfin = []
    for i in range(len(blobs)):
        y,x,_ = blobs[i]
        y,x = int(y),int(x)
        if dim_error and i==0:
            vfin.append(data[:,y-filter_shape-8:y+filter_shape,x-filter_shape:x+filter_shape,:])
        else:
            vfin.append(data[:,y-filter_shape:y+filter_shape,x-filter_shape:x+filter_shape,:])

    return vfin
    


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
# _munich = gpd.read_file('../geojson/munich.geojson')
# _interested_area = _munich.geometry.unary_union
# _bbox_interested_area = _interested_area.bounds
# _roi_bbox = BBox(bbox=_bbox_interested_area, crs=CRS.WGS84)
# vM,_ = get_coord_matrix(vImg.shape[2],vImg.shape[1],_roi_bbox)
# vROI = make_bbox(vM,vCoord)
# print(vROI)
 ## longitude is width, latitude is height
 #pdb.set_trace()


 
