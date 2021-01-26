"""unit tests for geo module"""
from floodsystem.geo import stations_by_distance
from floodsystem.geo import stations_within_radius
from floodsystem.geo import rivers_with_station
from floodsystem.geo import stations_by_river
from floodsystem.geo import rivers_by_station_number
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
    stations.append(
        MonitoringStation(s_id, m_id, label, (0.0, -1.5), trange, river, "0,-1.5")
    )
    stations.append(
        MonitoringStation(s_id, m_id, label, (1.0, 1.0), trange, river, "1,1")
    )

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
    stations.append(
        MonitoringStation(s_id, m_id, label, (10.0, 10.0), trange, river, "10,10")
    )
    stations.append(
        MonitoringStation(s_id, m_id, label, (1.0, 0.0), trange, river, "1,")
    )
    assert len(stations_within_radius(stations, (0.0, 0.0), 115)) == 2

    # check you duplicate distances being included
    stations.append(
        MonitoringStation(s_id, m_id, label, (0.0, 1.0), trange, river, "1,")
    )
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


def test_rivers_with_station():
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = "some coordinate"
    trange = "some range"
    river = "River X"
    town = "some town"

    # self define river
    stations = [MonitoringStation(s_id, m_id, label, coord, trange, "River X", town)]
    stations.append(
        MonitoringStation(s_id, m_id, label, coord, trange, "River Y", town)
    )
    stations.append(
        MonitoringStation(s_id, m_id, label, coord, trange, "River X", town)
    )

    rivers = rivers_with_station(stations)

    # check no repetition
    assert len(rivers) == 2

    # check river included
    assert "River X" in rivers
    assert "River Y" in rivers


def test_stations_by_river():
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = "some coordinate"
    trange = "some range"
    river = "River X"
    town = "some town"

    # self define stations and rivers
    stations = [
        MonitoringStation(s_id, m_id, "Station A", coord, trange, "River X", town)
    ]
    stations.append(
        MonitoringStation(s_id, m_id, "Station B", coord, trange, "River Y", town)
    )
    stations.append(
        MonitoringStation(s_id, m_id, "Station C", coord, trange, "River X", town)
    )

    river_dict = stations_by_river(stations)

    # check type is dict
    assert type(river_dict) == dict

    # check the keys are rivers
    assert "River X" in river_dict.keys()
    assert "River Y" in river_dict.keys()

    # check the values are lists of correct stations
    assert type(river_dict["River X"]) == list
    assert type(river_dict["River Y"]) == list
    assert "Station A" in river_dict["River X"]
    assert "Station B" in river_dict["River Y"]
    assert "Station C" in river_dict["River X"]


def test_rivers_by_station_number():
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = "some coordinate"
    trange = "some range"
    river = "River X"
    town = "some town"

    # self define stations and rivers
    stations = [
        MonitoringStation(s_id, m_id, "Station A", coord, trange, "River X", town)
    ]
    stations.append(
        MonitoringStation(s_id, m_id, "Station B", coord, trange, "River Y", town)
    )
    stations.append(
        MonitoringStation(s_id, m_id, "Station C", coord, trange, "River X", town)
    )
    stations.append(
        MonitoringStation(s_id, m_id, "Station D", coord, trange, "River Y", town)
    )
    stations.append(
        MonitoringStation(s_id, m_id, "Station E", coord, trange, "River Z", town)
    )
    stations.append(
        MonitoringStation(s_id, m_id, "Station F", coord, trange, "River X", town)
    )

    num = rivers_by_station_number(stations, 2)

    # Check error raised when N exceeds range
    with pytest.raises(ValueError) as e:
        rivers_by_station_number(stations, "a")
    assert "valid" in str(e)

    with pytest.raises(ValueError) as e:
        rivers_by_station_number(stations, 10)
    assert "valid" in str(e)

    # Check correct river names returned and sorted
    assert num[0][0] == "River X"
    assert num[1][0] == "River Y"

    # Check correct numbers returned
    assert num[0][1] == 3
    assert num[1][1] == 2

    # length is equal to or more than N
    assert len(num) == 2