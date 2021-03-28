import sys
import pytest
sys.path.insert(1,"../functions/")
import io_pipe
import nd_index
from eolearn.core import EOPatch
import numpy as np
import pdb
import lst

landsat8_eopatch = EOPatch.load('../data/ld8_example')

landsat8_data = landsat8_eopatch.data['L1C_data']
#landsat8_data = io_pipe.get_raw(landsat8_eopatch)

#pdb.set_trace()
#### loading the necessary files so that don't have to fetch them.
landsat_ndvi = nd_index.calc_ndvi(landsat8_data)
#lst.BrightnessTemp()
B10 = landsat8_data[:,:,:,9]-273
B11 = landsat8_data[:,:,:,10]-273
vLSE = lst.LSE(landsat_ndvi)


## test cases for input type and shape for LSE functions.
def test_LSE_input_shape():    
    assert len(landsat_ndvi.shape)==3


def test_LSE_input_type():
    with pytest.raises(TypeError):
        lst.LSE(5)

## test cases for output type and shape for LSE functions.
def test_LSE_output_type():
    vLSE = lst.LSE(landsat_ndvi)
    assert type(vLSE)==np.ndarray

def test_LSE_output_shape():
    assert lst.LSE(landsat_ndvi).shape==landsat_ndvi.shape

## test cases for input type and shape for mono_lst functions.
def test_LST_input_shape():    
    assert B10.shape == vLSE.shape

def test_LST_input_length():    
    assert len(B10.shape) == 3
    assert len(vLSE.shape) == 3

def test_LST_input_type():
    with pytest.raises(TypeError):
        lst.mono_LST(5,4)

def test_LST_output_type():
    vLST = lst.mono_LST(landsat_ndvi,vLSE)
    assert type(vLST)==np.ndarray

def test_LSE_output_shape():
    assert lst.mono_LST(landsat_ndvi,vLSE).shape==landsat_ndvi.shape

## test cases for input type and shape for temperature_threshold functions.
def test_threshold_input_type():
    with pytest.raises(TypeError):
        lst.temperature_threshold(np.zeros((5,5)),5)
        
    
def test_threshold_input_type():
    with pytest.raises(TypeError):
        lst.temperature_threshold(5,[1,35,67,3])
        

