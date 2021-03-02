"""unit tests for analysis submodule"""
from floodsystem.analysis import polyfit
from floodsystem.analysis import cure_levels
from floodsystem.analysis import eval_risk
from floodsystem.analysis import risk_calculation
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import date
import pytest
from floodsystem.station import MonitoringStation


def test_polyfit():
    """test to make sure polyfit returns the expected values"""
    x = np.linspace(0, 10, 10)
    y = [1 + (2 * i) + (3 * (i ** 2)) for i in x]

    poly = polyfit(matplotlib.dates.num2date(x), y, 2)
    assert round(poly[2], 5) == round(3, 5)
    assert round(poly[1], 5) == round(2, 5)
    assert round(poly[0], 5) == round(1, 5)

    # test validation for type
    with pytest.raises(TypeError) as e:
        polyfit(matplotlib.dates.num2date(x), y, "this is not the correct type")
    assert "variable of wrong type" in str(e)

    # test validation for p sign
    with pytest.raises(ValueError) as e:
        polyfit(matplotlib.dates.num2date(x), y, -2)
    assert "invalid p" in str(e)

    # test validation for p sign
    with pytest.raises(TypeError) as e:
        polyfit(y, y, 2)
    assert "dates were of" in str(e)


def test_cure_levels():
    # create normal test data
    levels = [0.1, 0.2]
    assert cure_levels(levels) == [0.1, 0.2]

    # create data to be cured
    levels = [0.1, [0.2, 0.3], (0.3, 0.4), "a"]
    assert cure_levels(levels) == [0.1, 0.2, 0.3, 0.0]


def test_risk_calculation():

    # Create a station
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = "some coordinate"
    trange = "some range"
    river = "River X"
    town = "some town"
    latest_level = "some level"

    s1 = MonitoringStation(s_id, m_id, label, coord, trange, river, "A")
    s1.highest_ratio = 1

    s2 = MonitoringStation(s_id, m_id, label, coord, trange, river, "B")
    s2.highest_ratio = 0

    s3 = MonitoringStation(s_id, m_id, label, coord, trange, river, "B")
    s3.highest_ratio = 1

    # create towns and town_stations
    town_stations = [[], []]
    town_stations[0].append(s1)
    town_stations[1].append(s2)
    town_stations[1].append(s3)

    towns = ["A", "B"]

    assert len(risk_calculation(towns, town_stations)) == 2
    assert risk_calculation(towns, town_stations)[0][0] == "A"
    assert risk_calculation(towns, town_stations)[0][1] == np.e
    assert risk_calculation(towns, town_stations)[1][0] == "B"
    assert risk_calculation(towns, town_stations)[1][1] == (np.e + 1) / 2
