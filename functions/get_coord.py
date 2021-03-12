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

def get_coord_matrix(image_width,image_height,bbox):
    
    #!!!!! be careful what does the width and height individually correspond to? long or lati?
    """[summary]

    Args:
        image_width ([type]): [description]
        image_height ([type]): [description]
        bbox ([type]): [description]

    Returns:
        [type]: [description]
    """
    bounds = tuple(bbox)
    # please double check this
    long_shape = image_width 
    lati_shape = image_height 
    long = bounds[::2]
    lati = bounds[1::2]
    space_long,diff_long = np.linspace(*long,long_shape,retstep=True)
    space_lati,diff_lati = np.linspace(*lati,lati_shape,retstep=True)
    #pdb.set_trace()
    #geo_matrix = None
    distance = [diff_long, diff_lati]
    return (space_long,space_lati), distance





def get_geoindex(geo_matrix, index_pixel):
    """[summary]
    Args:
        param geo_matrix: this is a tuple which tells us which image coordinate corresponds
                          to which geo-coordinates.
        type geo_matrix: tuple of 2 list.
        
        param index_pixel: coordinates of our reqired point in image.
        type index_pixel: tuple.
        
    Returns: 
         returns the  geo coodinates of a coordinates of a given pixel in an image
    """
    vX_geo = geo_matrix[0][index_pixel[0]]
    vL = len(geo_matrix[1])
    # instead of using this modify the y as difference value.
    vY_geo = geo_matrix[1][index_pixel[1]]
    #vY_geo = geo_matrix[1][vL - index_pixel[1]]
    
    return (vX_geo,vY_geo)
 #   return list(geo1,geo2,...)


def make_bbox(geo_matrix,index_pixel,filter_size=20):
    """[summary]

    Args:
        param geo_matrix: this is a tuple which tells us which image coordinate corresponds
                          to which geo-coordinates.
        type geo_matrix: tuple of 2 list.
        
        param index_pixel: coordinates of our reqired point in image.
        type index_pixel: tuple.
        
        param filter_size: filter size of AOI.
        type filter_size: int.
        

        geo_matrix ([tuple]): 
      
    Returns:
        returns bbox of the given geo coordinates
    """
    vX_max = index_pixel[0]+20
    vX_min = index_pixel[0]-20
    vY_max = index_pixel[1]+20
    vY_min = index_pixel[1]-20
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

def get_bbox(geo_matrix,blobs,filter_size=20):
    vfinal=[]
    for i in range(len(blobs)):
        y,x,_ = blobs[i]
        pdb.set_trace()
        vfinal.append(make_bbox(geo_matrix,(int(x),int(y)),filter_size))
    return vfinal

#    return list(geo_bbox1,geo_bbox2)
# Read eopatch as eodata


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


 
