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



