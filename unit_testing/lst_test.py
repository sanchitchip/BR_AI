import sys
import pytest
sys.path.insert(1,"../functions/")
import nd_index
import numpy as np
import pdb
import lst

#### Randomly generating data instead of using mp load 
landsat_ndvi = np.random.uniform(low=-.99, high=.99, size=(1,1000,1000))
B10 = np.random.uniform(low= 280, high=300, size=(1,1000,1000))
B11 = np.random.uniform(low= 280, high=300, size=(1,1000,1000))
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
        

## add test cases for lst functions.
# check for none type error in calc_ndvi functions.        
def test_calc_island_detection_Noneerror():
    with pytest.raises(TypeError) as msg:
        lst.island_detection(np.zeros((3,4)),
                           None)
    with pytest.raises(TypeError) as msg2:
        lst.island_detection(None,'doh')

    print(msg.value)    
    assert 'NoneType' in str(msg.value)
    print(msg2.value)        
    assert 'NoneType' in str(msg2.value)

    
# check for input type error in calc_ndvi functions.

def test_calc_island_detection_input_method():
#    print('hi')
    with pytest.raises(TypeError) as msg:
        vblob = lst.island_detection(vLSE,
                             'alpha',False)
    print(msg)
    assert 'TypeError' in str(msg.value)
    
