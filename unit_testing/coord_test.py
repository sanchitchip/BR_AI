import sys
sys.path.insert(1,"../functions/")
import pytest
import numpy as np
import get_coord

def test_coord_matrix_input_type():
    with pytest.raises(TypeError) as msg:
        get_coord.get_coord_matrix("s",int(34),[35,45])

def test_coord_matrix_input_type2():
    with pytest.raises(TypeError) as msg:
        get_coord.get_coord_matrix(int(30),'s',[35,45])

## checking if we get a None type error if we input a None value in the function.
def test_geoindex_Noneerror():
    with pytest.raises(TypeError) as msg:
        get_coord.get_geoindex(None,(24,56))
    print(str(msg.value))
    assert 'NoneType' in str(msg.value)

def test_geoindex_Noneerror2():
    val = ((1,2,3),(4,67,8))
    with pytest.raises(TypeError) as msg:
        get_coord.get_geoindex(val,None)
    print(str(msg.value))
    assert 'NoneType' in str(msg.value)


## checking if we get a None type error if we input a None value in the function.
def test_makebbox_Noneerror():
    with pytest.raises(TypeError) as msg:
        get_coord.make_bbox(None,(24,56))
    assert 'NoneType' in str(msg.value)

def test_makebbox_Noneerror():
    val = ((1,2,3),(4,67,8))
    with pytest.raises(TypeError) as msg:
        get_coord.make_bbox(val,None)
    assert 'NoneType' in str(msg.value)

def test_makebbox_input_type():
    with pytest.raises(TypeError) as msg:
        get_coord.make_bbox(25,(24,56))
    #assert 'Type' in str(msg.value)

## checking if we get a None type error when we input a None value in the function for get bbox function.
def test_getbbox_input_type():
    with pytest.raises(TypeError) as msg:
        get_coord.get_bbox(2324,(21,516))
    #assert 'Type' in str(msg.value)

def test_getbbox_Noneerror():
    val = ((1,2,3),(4,67,8))
    with pytest.raises(TypeError) as msg:
        get_coord.get_bbox(None,val)
    assert 'NoneType' in str(msg.value)

def test_getebbox_Noneerror():
    val = ((1,2,3),(4,67,8))
    with pytest.raises(TypeError) as msg:
        get_coord.get_bbox(val,None)
    assert 'NoneType' in str(msg.value)



#def test_testing():
#    with pytest.raises(TypeError):
        
#    print(e_info.value)
#    assert str(e_info.value) in 'division by zero'

