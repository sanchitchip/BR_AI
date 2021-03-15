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
    