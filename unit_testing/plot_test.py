import geopandas as gpd
import sys
sys.path.insert(1,"../functions/")
import pytest
import io_pipe
import nd_index
from eolearn.core import EOPatch
import numpy as np
import pdb
import lst
import plot_utils

def test_plot_lst_true():
    with pytest.raises(TypeError) as msg:
        plot_utils.plot_LST_true(np.zeros((3,4),5),None)
        
def test_plot_lst_true():
    with pytest.raises(TypeError) as msg:
        plot_utils.plot_LST_true(5,np.zeros((3,4)),None)

# check for none type error in lst_true plot functions.        
def test_plot_lst_true_Noneerror():
    with pytest.raises(TypeError) as msg:
        plot_utils.plot_LST_true(None,np.zeros((4,5)),None)
    with pytest.raises(TypeError) as msg2:
        plot_utils.plot_LST_true(np.zeros((4,5)),None,None)
    assert 'NoneType' in str(msg.value)
    assert 'NoneType' in str(msg2.value)

# check for input type error in all_lst plot functions.        
def test_plot_lst_true():
    with pytest.raises(TypeError) as msg:
        plot_utils.plot_all_LST(np.zeros((3,4),5),None)
    with pytest.raises(TypeError) as msg2:
        plot_utils.plot_all_LST(5, np.zeros((3,4),None))
# check for none type error in all_lst plot functions.        
def test_plot_all_LST_Noneerror():
    with pytest.raises(TypeError) as msg:
        plot_utils.plot_all_LST(None,np.zeros((4,5)),None)
    with pytest.raises(TypeError) as msg2:
        plot_utils.plot_all_LST(np.zeros((4,5)),None,None)
    assert 'NoneType' in str(msg.value)
    assert 'NoneType' in str(msg2.value)



# check for none type error in all_lst plot functions.        
def test_plot_islands_Noneerror():
    with pytest.raises(TypeError) as msg:
        plot_utils.plot_islands(None,np.zeros((4,5)),([3,4],[6,7]))
    with pytest.raises(TypeError) as msg2:
        plot_utils.plot_islands(np.zeros((4,5)),None,([3,4],[6,7]))
    with pytest.raises(TypeError) as msg3:
        plot_utils.plot_islands(np.zeros((4,5)),None,([3,4],[6,7]))
        #        plot_utils.plot_all_LST(np.zeros((4,5)),None,None)
    assert 'NoneType' in str(msg.value)
    assert 'NoneType' in str(msg2.value)
    assert 'NoneType' in str(msg3.value)


#def test_makebbox_input_type():
#    with pytest.raises(TypeError) as msg:
#        get_coord.make_bbox(25,(24,56))
    #assert 'Type' in str(msg.value)
