import datetime
from typing import Type
from sentinelhub import BBox, CRS, DataCollection, SHConfig
from eolearn.core import SaveTask, FeatureType, LinearWorkflow, EOPatch,OverwritePermission
from eolearn.io import SentinelHubInputTask
import geopandas as gpd

def set_config(new_id=True, **kwargs):
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
                 time_interval=('2020-04-01', '2020-05-05'),
                 maxcc=.8,
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
            'INSTANCE_ID': '9445bbf5-1f51-4a12-9a1c-909625defaa6',
            'CLIENT_ID': '278cd057-ed6f-4cd2-b7df-abf1698cdb9c',
            'CLIENT_SECRET': 'r3NKPHdw6pOFsv&gOW}3Ljk&<ZL-zJu6]p5z-ln:'
        }
        config = set_config(**config_dict)

    _time_difference = datetime.timedelta(hours=2)

    input_task = SentinelHubInputTask(
        data_collection=DataCollection.LANDSAT8,
        bands=[
            'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09',
            'B10', 'B11', 'BQA'
        ],
        bands_feature=(FeatureType.DATA, 'L1C_data'),
        additional_data=[(FeatureType.MASK, 'dataMask')],
        resolution=resolution,
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
            'INSTANCE_ID': '9445bbf5-1f51-4a12-9a1c-909625defaa6',
            'CLIENT_ID': '278cd057-ed6f-4cd2-b7df-abf1698cdb9c',
            'CLIENT_SECRET': 'r3NKPHdw6pOFsv&gOW}3Ljk&<ZL-zJu6]p5z-ln:'
        }
        config = set_config(**config_dict)
        
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


if __name__ == '__main__':
    set_config()
    eo_test = get_landsat8()
    
    # save_eopatch(eo_test,'../example_data/generate_by_io_pipe')
    


