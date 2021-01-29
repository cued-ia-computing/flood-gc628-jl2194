"""unit tests for analysis submodule"""
from floodsystem.analysis import polyfit
from floodsystem.analysis import cure_levels
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import date
import pytest

def test_polyfit():
    """test to make sure polyfit returns the expected values
    """
    x = np.linspace(0, 10, 10)
    y = [1 + (2 * i) + (3 * (i ** 2)) for i in x]

    poly = polyfit(matplotlib.dates.num2date(x),y,2)
    assert round(poly[2],5) == round(3,5)
    assert round(poly[1],5) == round(2,5)
    assert round(poly[0],5) == round(1,5)

    # test validation for type
    with pytest.raises(TypeError) as e:
        polyfit(matplotlib.dates.num2date(x),y,"this is not the correct type")
    assert "variable of wrong type" in str(e)

    # test validation for list length
    with pytest.raises(ValueError) as e:
        polyfit(matplotlib.dates.num2date(x),y[1:],2)
    assert "mismatched list lengths" in str(e)

    # test validation for p sign
    with pytest.raises(ValueError) as e:
        polyfit(matplotlib.dates.num2date(x),y,-2)
    assert "invalid p" in str(e)

     # test validation for p sign
    with pytest.raises(TypeError) as e:
        polyfit(y,y,2)
    assert "dates were of" in str(e)

def test_cure_levels():
    #create normal test data
    levels = [0.1, 0.2]
    assert cure_levels(levels) == [0.1, 0.2]

    #create data to be cured
    levels = [0.1, [0.2, 0.3], (0.3, 0.4), 'a']
    assert cure_levels(levels) == [0.1, 0.2, 0.3, 0.0]
  