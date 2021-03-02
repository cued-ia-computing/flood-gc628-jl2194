from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level
from floodsystem.station import MonitoringStation
import pytest


def test_stations_level_over_threshold():
    # Create a station
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = "some coordinate"
    trange = "some range"
    river = "River X"
    town = "some town"
    latest_level = "some level"

    s1 = MonitoringStation(s_id, m_id, label, coord, (0, 1), river, town)
    s1.latest_level = 0.5

    s2 = MonitoringStation(s_id, m_id, label, coord, (4, 8), river, town)
    s2.latest_level = 7

    s3 = MonitoringStation(s_id, m_id, label, coord, (3, 4), river, town)
    s3.latest_level = 4

    stations = []
    stations.append(s1)
    stations.append(s2)
    stations.append(s3)

    # check the correctness of returned list
    level_list = stations_level_over_threshold(stations, 0.7)
    assert len(level_list) == 2
    assert level_list[0][1] == 1
    assert level_list[1][1] == 0.75


def test_stations_highest_rel_level():
    # Create a station
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = "some coordinate"
    trange = "some range"
    river = "River X"
    town = "some town"
    latest_level = "some level"

    s1 = MonitoringStation(s_id, m_id, label, coord, (0, 1), river, town)
    s1.latest_level = 0.5

    s2 = MonitoringStation(s_id, m_id, label, coord, (4, 8), river, town)
    s2.latest_level = 7

    s3 = MonitoringStation(s_id, m_id, label, coord, (3, 4), river, town)
    s3.latest_level = 4

    stations = []
    stations.append(s1)
    stations.append(s2)
    stations.append(s3)

    # check the correctness of returned list
    level_list = stations_highest_rel_level(stations, 2)
    assert len(level_list) == 2
    assert level_list[0].relative_water_level() == 1
    assert level_list[1].relative_water_level() == 0.75
