import numpy as np
import sys
import pytest
sys.path.insert(1,"../functions/")
import nd_index



def test_ndfun_changec():
    band_a = np.array([1,1])
    band_b = np.array([3,3])
    c = 1
    func_answer = nd_index.normalized_difference_index(band_a,band_b,c=c)
    real_answer = np.array([-0.2, -0.2])
    assert np.all(func_answer==real_answer)


# check for input type error in calc_lst  functions.        
def test_calc_lst_input():
    with pytest.raises(TypeError) as msg:
        nd_index.calc_lst(np.zeros((3,4)),
                          5)
    with pytest.raises(TypeError) as msg2:
        nd_index.calc_lst(5,'landsat8')
    
# check for none type error in calc_lst functions.        
def test_calc_lst_Noneerror():
    with pytest.raises(TypeError) as msg:
        nd_index.calc_lst(np.zeros((3,4)),
                                   None)
    with pytest.raises(TypeError) as msg2:
        nd_index.calc_lst(None,'landsat8')

    assert 'NoneType' in str(msg.value)
    assert 'NoneType' in str(msg2.value)




# check for input type error in calc_ndwi functions.        
def test_calc_ndwi_input():
    with pytest.raises(TypeError) as msg:
        nd_index.calc_ndwi(np.zeros((3,4)),
                          5)
    with pytest.raises(TypeError) as msg2:
        nd_index.calc_ndwi(5,'landsat8')


# check for none type error in calc_ndwi functions.        
def test_calc_ndwi_Noneerror():
    with pytest.raises(TypeError) as msg:
        nd_index.calc_ndwi(np.zeros((3,4)),
                           None)
    with pytest.raises(TypeError) as msg2:
        nd_index.calc_ndwi(None,'landsat8')
    assert 'NoneType' in str(msg.value)
    assert 'NoneType' in str(msg2.value)


#~~~~~~~

# check for none type error in calc_ndvi functions.        
def test_calc_ndvi_Noneerror():
    with pytest.raises(TypeError) as msg:
        nd_index.calc_ndvi(np.zeros((3,4)),
                           None)
    with pytest.raises(TypeError) as msg2:
        nd_index.calc_ndvi(None,'landsat8')
        
    assert 'NoneType' in str(msg.value)
    assert 'NoneType' in str(msg2.value)

    
# check for input type error in calc_ndvi functions.        
def test_calc_ndvi_input():
    with pytest.raises(TypeError) as msg:
        nd_index.calc_ndvi(np.zeros((3,4)),
                          5)
    with pytest.raises(TypeError) as msg2:
        nd_index.calc_ndvi(5,'landsat8')



