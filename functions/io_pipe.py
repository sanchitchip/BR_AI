import datetime
from typing import Type
from sentinelhub import BBox, CRS, DataCollection, SHConfig
from eolearn.core import SaveTask, FeatureType, LinearWorkflow, EOPatch,OverwritePermission
from eolearn.io import SentinelHubInputTask
import geopandas as gpd
import numpy as np
import pdb

def set_config(new_id=False, **kwargs):
    """
    A sentinelhub-py package configuration class.
    Args:
        instance_id: An instance ID for Sentinel Hub service used for OGC requests.
        sh_client_id: User’s OAuth client ID for Sentinel Hub service
        sh_client_secret: User’s OAuth client secret for Sentinel Hub service
    
    Return: a config Instance
    """
    config = SHConfig()
    if new_id == True:
        config.instance_id = kwargs['INSTANCE_ID']
        config.sh_client_id = kwargs['CLIENT_ID']
        config.sh_client_secret = kwargs['CLIENT_SECRET']
    if config.sh_client_id == '' or config.sh_client_secret == '' or config.instance_id == '':
        print(
            "Warning! To use Sentinel Hub services, please provide the credentials (client ID and client secret)."
        )
    return config

def get_landsat8(aoi=None,
                 time_interval=('2020-04-10', '2020-04-28'),
                 time_difference=None,    
                 maxcc=.1,
                 resolution=20,
                 config=None):
    """
    Download landsat8 images from sentinelhub.
    Args:
        param aoi: Area of Interest.
        type aoi: shapely.geometry.multipolygon.MultiPolygon.
        
        param time_interval: Time period want to get.
        type time_interval: two elements list. (Start, End).
        
        param maxcc: Maximum cloud coverage.
        type maxcc: float.
        
        param resolution: The resolution of images
        type resolution: int.
        
        param config: 
        type config: sentinelhub.config.SHConfig
        
    Returns:
        A eopatch datatable, which has the image data, mask data.
        image data: np.ndarray, shape(time,image_width,image_height, bands)
        mask data: np.ndarray, shape(time,image_width,image_height, 1)
    """

    if aoi is None:
        # if aoi not specificed use munich as default
        _munich = gpd.read_file('../geojson/munich.geojson')
        _interested_area = _munich.geometry.unary_union
        _bbox_interested_area = _interested_area.bounds
        _roi_bbox = BBox(bbox=_bbox_interested_area, crs=CRS.WGS84)
    else:
        if not isinstance(aoi, list) | isinstance(aoi, tuple):
            raise TypeError("Input should be List or Tuple.")
        if len(aoi) != 4:
            raise TypeError(
                "Input should be like (long_1,lati_1,long_2,lati_2).")
    if not config:
        config_dict = {
            'INSTANCE_ID': '31aacbb6-8ad8-43f5-b19d-84a8302c2a3e',
            'CLIENT_ID': '8c799cf6-53fa-4f98-a3ff-417cdc658b57',
            'CLIENT_SECRET': '13[,;5upS5%e3@oZk?J^1:)Fu?*.+0kF|,kD6re2'
        }
        config = set_config(config_dict)

    if time_difference is None:
        _time_difference = datetime.timedelta(hours=2)
    else:
        _time_difference = time_difference

            
    input_task = SentinelHubInputTask(
        data_collection=DataCollection.LANDSAT8,
        bands=[
            'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09',
            'B10', 'B11', 'BQA'
        ],
        bands_feature=(FeatureType.DATA, 'L1C_data'),
        additional_data=[(FeatureType.MASK, 'dataMask')],
#        size = (1000,1000),
        bands_dtype=np.int16,
        resolution=resolution,
#        additional_data=[(FeatureType.MASK, 'dataMask'),(FeatureType.META_INFO, 'META')],
        maxcc=maxcc,
        time_difference=_time_difference,
        config=config,
        max_threads=3)
    save = SaveTask('data_landsat', overwrite_permission=2, compress_level=1)
    workflow = LinearWorkflow(input_task)

    _result = workflow.execute({
        input_task: {
            'bbox': _roi_bbox,
            'time_interval': time_interval
        },
        # save: {'eopatch_folder': './landsat_eopatch'}
    })
    eopatch = _result.eopatch()

    return eopatch


def get_landsat8_range(aoi=None,config=None,year_range=None,
                       month = None,date_range=(1,30),maxcc=.1):
    '''
    Download uncorrupted landsat8 image for a given time range,cloud coverage.
    This function makes sure that you don't get any image which requires Mask data or have certain pixels
    with missing data.
    '''
    vtime_interval = []
    for idx,val in enumerate(year_range):
        vstrt = str(val)+'-0'+str(month[0])+'-0'+str(date_range[0])
        vend = str(val)+'-0'+str(month[1])+'-'+str(date_range[1])
        vtime_interval.append((vstrt,vend))    
    vdata = []
    vtimestamp = []
    vMask = []
    vcloud_coverage=maxcc
    for i in range(len(vtime_interval)):
        try:
            vband = get_landsat8(time_interval=vtime_interval[i],
                                              maxcc=vcloud_coverage,
                                              config=config)
            vM = vband.mask['dataMask']
            ## images which have data mask and we want to remove if the list is not empty
            vNot = list(set(np.where(vM==False)[0]))
            ## if the vNot lise is empty it implies that all the images fethced in this case 
            ## don't have any masking and so we can just add the timestamp data and bands data to our list
            if not vNot:
                vdata.append(vband.data['L1C_data'])
                for i in vband.timestamp:
                    vtimestamp.append(i)
            else:
                ## in case vNot list is not empty we should find all images which might 
                ## not have masking and add only them.
                vInd= [i for i in range(vM.shape[0]) if i not in vNot]
                if vInd:
    #                print("Some of the images in this interval are corrupted {}".format(vtime_interval[i]))
                    vdata.append(vband.data['L1C_data'][vInd,:,:,:])
    #                print("Indices which are corrupted are {}".format(vNot))
    #                print("Indices which are good are {}".format(vInd))
                    for i in vInd:
                        vtimestamp.append(vband.timestamp[i])

                else:
                    print("All the fetched image have corrupted data hence not added time_interval {}"
                          .format(vtime_interval[i],vcloud_coverage))
                    continue;


        except:
            print("No image exists for the parameters: time interval {},cloud coverage: {},".format(vtime_interval[i],
                                                                                                    vcloud_coverage))
    eopatch_data = np.concatenate(vdata,axis=0)
    return eopatch_data,vtimestamp


def get_sentinel2(aoi=None,
                  time_interval=('2020-04-01', '2020-05-05'),
                  maxcc=.8,
                  resolution=20,
                  config=None):
    """
    Download sentinel2 images from sentinelhub.
    Args:
        param aoi: Area of Interest.
        type aoi: shapely.geometry.multipolygon.MultiPolygon.
        
        param time_interval: Time period want to get.
        type time_interval: two elements list. (Start, End).
        
        param maxcc: Maximum cloud coverage.
        type maxcc: float.
        
        param resolution: The resolution of images
        type resolution: int.
        
        param config: 
        type config: sentinelhub.config.SHConfig
        
    Returns:
        A eopatch datatable, which has the image data, mask data.
        image data: np.ndarray, shape(time,image_width,image_height, bands)
        mask data: np.ndarray, shape(time,image_width,image_height, 1)
    """

    if aoi is None:
        # if aoi not specificed use munich as default
        _munich = gpd.read_file('../geojson/munich.geojson')
        _interested_area = _munich.geometry.unary_union
        _bbox_interested_area = _interested_area.bounds
        _roi_bbox = BBox(bbox=_bbox_interested_area, crs=CRS.WGS84)
    else:
        if not isinstance(aoi, list) | isinstance(aoi, tuple):
            raise TypeError("Input should be List or Tuple.")
        if len(aoi) != 4:
            raise TypeError(
                "Input should be like (long_1,lati_1,long_2,lati_2).")
        _roi_bbox = BBox(bbox=aoi, crs=CRS.WGS84)
    if not config:
        config_dict = {
            'INSTANCE_ID': '31aacbb6-8ad8-43f5-b19d-84a8302c2a3e',
            'CLIENT_ID': '8c799cf6-53fa-4f98-a3ff-417cdc658b57',
            'CLIENT_SECRET': '13[,;5upS5%e3@oZk?J^1:)Fu?*.+0kF|,kD6re2'
        }
        config = set_config(config_dict)

    _time_difference = datetime.timedelta(hours=2)

    input_task = SentinelHubInputTask(
        data_collection=DataCollection.SENTINEL2_L1C,
        bands=['B01', 'B02', 'B03', 'B04', 'B05', 'B06',
               'B07', 'B08', 'B8A', 'B09', 'B10', 'B11', 'B12'],
        bands_feature=(FeatureType.DATA, 'L1C_data'),
        additional_data=[(FeatureType.MASK, 'dataMask')],
        resolution=resolution,
        maxcc=maxcc,
        time_difference=_time_difference,
        config=config,
        max_threads=3)
    save = SaveTask('data_sentinel', overwrite_permission=2, compress_level=1)
    workflow = LinearWorkflow(input_task)

    _result = workflow.execute({
        input_task: {
            'bbox': _roi_bbox,
            'time_interval': time_interval
        },
        # save: {'eopatch_folder': './sentinel_eopatch'}
    })
    eopatch = _result.eopatch()

    return eopatch


def save_eopatch(eopatch, path: str):
    """
    Save eopatch to local directory.
    Args:
        param eopatch: eopatch data, generated by get_satellite function
        type eopatch: eolearn.core.eodata.EOPatch.
        
        param path: local directory path.
        type path: str.
        
    Returns:
        None
    """
    eopatch.save(path,overwrite_permission=OverwritePermission.OVERWRITE_FEATURES)

def read_eopatch(path:str):
    """
    Load eopatch from local directory.
    Args:
        param path: local directory path.
        type path: str.
    Returns:
        None
    """
    return EOPatch.load(path)


def get_raw(eopatch,mask=False,bands=None,satellite="landsat"):
    """
    Get the raw data of eopatch
    Args:
        param eopatch: eopatch data, generated by get_satellite function
        type eopatch: eolearn.core.eodata.EOPatch.
        
        param mask: Whether to save mask data.
        type mask:bool.
    Returns:
        image data: np.ndarray, shape(time,image_width,image_height, bands)
        mask data: bool np.ndarray, shape(time,image_width,image_height, 1)
    """
    if bands is not None:
        if satellite=="landsat":
            assert all(band_num <= 12 for band_num in bands)
        if satellite=="sentinel":
            assert all(band_num <= 12 for band_num in bands)
            
    _raw_data = eopatch.data['L1C_data']
    _mask = eopatch.mask
    if mask:
        data = {
            "L1C_data":_raw_data,
            "Mask":_mask
        }
    else:
        data = _raw_data
    return data


def validate_timestamp(aoi=None,
                 time_interval=('2020-04-10', '2020-04-28'),
                 time_difference=None,    
                 maxcc=.2,
                 config=None):
    if aoi is None:
        # if aoi not specificed use munich as default
        _munich = gpd.read_file('../geojson/munich.geojson')
        _interested_area = _munich.geometry.unary_union
        _bbox_interested_area = _interested_area.bounds
        _roi_bbox = BBox(bbox=_bbox_interested_area, crs=CRS.WGS84)
    else:
        if not isinstance(aoi, list) | isinstance(aoi, tuple):
            raise TypeError("Input should be List or Tuple.")
        if len(aoi) != 4:
            raise TypeError(
                "Input should be like (long_1,lati_1,long_2,lati_2).")
    if not config:
        config_dict = {
            'INSTANCE_ID': '31aacbb6-8ad8-43f5-b19d-84a8302c2a3e',
            'CLIENT_ID': '8c799cf6-53fa-4f98-a3ff-417cdc658b57',
            'CLIENT_SECRET': '13[,;5upS5%e3@oZk?J^1:)Fu?*.+0kF|,kD6re2'
        }
        config = set_config(config_dict)

    if time_difference is None:
        _time_difference = datetime.timedelta(hours=2)
    else:
        _time_difference = time_difference

            
    input_task = get_available_timestamps(bbox = _roi_bbox,
                                          data_collection=DataCollection.LANDSAT8,
                                          time_interval=time_interval,
                                          maxcc=maxcc,
                                          time_difference=_time_difference,
                                          config=config)
    return input_task



if __name__ == '__main__':
    set_config()
    eo_test = get_landsat8()
    # save_eopatch(eo_test,'../example_data/generate_by_io_pipe')
