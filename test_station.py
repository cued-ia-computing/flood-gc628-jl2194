# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Unit test for the station module"""

from floodsystem.station import MonitoringStation
from floodsystem.station import inconsistent_typical_range_stations


def test_create_monitoring_station():

    # Create a station
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    trange = (-2.3, 3.4445)
    river = "River X"
    town = "My Town"
    s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    assert s.station_id == s_id
    assert s.measure_id == m_id
    assert s.name == label
    assert s.coord == coord
    assert s.typical_range == trange
    assert s.river == river
    assert s.town == town

def test_typical_range_consistent():
    # Create a station
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    river = "River X"
    town = "My Town"

    # test for missing data
    s = MonitoringStation(s_id, m_id, label, coord, None, river, town)
    assert s.typical_range_consistent() == False

    # test for valid data
    s = MonitoringStation(s_id, m_id, label, coord, (0,1), river, town)
    assert s.typical_range_consistent() == True

    # test for equall values
    s = MonitoringStation(s_id, m_id, label, coord, (1,1), river, town)
    assert s.typical_range_consistent() == True

    # test for invalid data
     s = MonitoringStation(s_id, m_id, label, coord, (1,0), river, town)
    assert s.typical_range_consistent() == False


def test_inconsistent_typical_range_stations:
    # Create list of stations
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    river = "River X"
    town = "My Town"
    stations = [MonitoringStation(s_id, m_id, label, coord, (0,1), river, town)]

    # normal operation
    assert len(inconsistent_typical_range_stations(stations)) == 1

    stations.append(MonitoringStation(s_id, m_id, label, coord, None, river, town))
    stations.append(MonitoringStation(s_id, m_id, label, coord, (1,0), river, town))

    # invalid excluded
    assert len(inconsistent_typical_range_stations(stations)) == 1


