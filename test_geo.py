"""unit tests for geo module"""
from floodsystem.geo import stations_by_distance
from floodsystem.geo import stations_within_radius
from floodsystem.station import MonitoringStation
import pytest


def test_stations_by_distance():
    # testing for correct order and value, checked by hand
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    trange = (-1, 1)
    river = "River X"

    stations = [MonitoringStation(s_id, m_id, label, (1.0, 0.0), trange, river, "1,0")]
    stations.append(MonitoringStation(s_id, m_id, label, (0.0, -1.5), trange, river, "0,-1.5"))
    stations.append(MonitoringStation(s_id, m_id, label, (1.0, 1.0), trange, river, "1,1"))

    sorted_stations = stations_by_distance(stations, (0.0, 0.0))

    # assert correct order
    assert sorted_stations[0][0].town == "1,0"
    assert sorted_stations[1][0].town == "1,1"
    assert sorted_stations[2][0].town == "0,-1.5"

    # assert correct value
    assert round(sorted_stations[0][1], 3) == 111.195
    assert round(sorted_stations[1][1], 3) == 157.250
    assert round(sorted_stations[2][1], 3) == 166.793

    # test validation for point
    with pytest.raises(TypeError) as e:
        stations_by_distance(stations, ("This is an invlaid point"))
    assert "point" in str(e)

    # test validation for station
    with pytest.raises(TypeError) as e:
        stations_by_distance("This is an invlaid station", (0.0, 0.0))
    assert "station" in str(e)


def test_stations_within_radius():
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    trange = (-1, 1)
    river = "River X"

    # make sure that places on boundary are included
    stations = [MonitoringStation(s_id, m_id, label, (0.0, 0.0), trange, river, "0,0")]
    assert len(stations_within_radius(stations, (0.0, 0.0), 0)) == 1

    # make sure that un ordered input lists work as intended
    stations.append(MonitoringStation(s_id, m_id, label, (10.0, 10.0), trange, river, "10,10"))
    stations.append(MonitoringStation(s_id, m_id, label, (1.0, 0.0), trange, river, "1,"))
    assert len(stations_within_radius(stations, (0.0, 0.0), 115)) == 2

    # check you duplicate distances being included
    stations.append(MonitoringStation(s_id, m_id, label, (0.0, 1.0), trange, river, "1,"))
    assert len(stations_within_radius(stations, (0.0, 0.0), 115)) == 3

    # test validation for point
    with pytest.raises(TypeError) as e:
        stations_within_radius(stations, ("This is an invlaid point"), 100)
    assert "point" in str(e)

    # test validation for radius
    with pytest.raises(TypeError) as e:
        stations_within_radius(stations, (0.0, 0.0), "This is an invalid radius")
    assert "type" in str(e)

    with pytest.raises(ValueError) as e:
        stations_within_radius(stations, (0.0, 0.0), -100)
    assert "radius was negative" in str(e)

    # test validation for station
    stations.append("This is an invalid station")
    with pytest.raises(TypeError) as e:
        stations_within_radius(stations, (0.0, 0.0), 100)
    assert "station" in str(e)
