import geopandas as gpd
import sys
import pytest
sys.path.insert(1,"../functions/")
import io_pipe


munich = gpd.read_file('../geojson/munich.geojson')


def test_input_should_be_list_tuple_sentinel():
    with pytest.raises(TypeError) as inf:
        io_pipe.get_sentinel2(aoi = munich)
    assert str(inf.value) == "Input should be List or Tuple."
    
def test_input_length():
    with pytest.raises(TypeError) as inf:
        io_pipe.get_sentinel2(aoi = (1,1,1))
    assert str(inf.value) == "Input should be like (long_1,lati_1,long_2,lati_2)."


def test_set_config():

        config_dict = {
            'INSTANCE_ID': '9445bbf5-1f51-4a12-9a1c-909625defaa6',
            'CLIENT_ID': '278cd057-ed6f-4cd2-b7df-abf1698cdb9c',
            'CLIENT_SECRET': 'r3NKPHdw6pOFsv&gOW}3Ljk&<ZL-zJu6]p5z-ln:'
        }
        config = io_pipe.set_config(**config_dict)
        assert all(
            [config.instance_id=='9445bbf5-1f51-4a12-9a1c-909625defaa6',
             config.sh_client_id=='278cd057-ed6f-4cd2-b7df-abf1698cdb9c',
             config.sh_client_secret=='r3NKPHdw6pOFsv&gOW}3Ljk&<ZL-zJu6]p5z-ln:']
        )