import datetime
from sentinelhub import BBox, CRS, DataCollection, SHConfig
from eolearn.core import SaveTask, FeatureType, LinearWorkflow
from eolearn.io import SentinelHubInputTask
import geopandas as gpd


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
                 time_interval=('2020-04-01', '2020-05-01'),
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
    if aoi == None:
        # if aoi not specificed use munich as default
        _munich = gpd.read_file('../geojson/munich.geojson')
        _interested_area = _munich.geometry.unary_union
        _bbox_interested_area = _interested_area.bounds
        _roi_bbox = BBox(bbox=_bbox_interested_area, crs=CRS.WGS84)
    else:
        _roi_bbox = aoi.bounds
    if not config:
        config_dict = {
            'INSTANCE_ID': '31aacbb6-8ad8-43f5-b19d-84a8302c2a3e',
            'CLIENT_ID': '8c799cf6-53fa-4f98-a3ff-417cdc658b57',
            'CLIENT_SECRET': '13[,;5upS5%e3@oZk?J^1:)Fu?*.+0kF|,kD6re2'
        }
        config = set_config(config_dict)

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
        # save: {'eopatch_folder': './eopatch'}
    })
    eopatch = _result.eopatch()

    return eopatch


if __name__ == '__main__':
    set_config()
    eo_test = get_landsat8()
