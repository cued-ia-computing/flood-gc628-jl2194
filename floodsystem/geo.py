# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
from .utils import binary_search_highest_lesser
from .utils import haversine


def stations_by_distance(stations, p):
    """Returns the stations list sorted by their great-circle distance
    from a given latitude and longitude (p)
    p should be a 2d tuple
    stations should be a list of MonitoringStation
    objects
    """

    # make sure that p is valid
    # checing p type and length, and values type and range
    if (
        type(p) != tuple
        or len(p) != 2
        or type(p[0]) != float
        or type(p[1]) != float
        or abs(p[0]) > 180
        or abs(p[1]) > 180
    ):
        raise TypeError("invalid point, point was {}".format(p))

    for stat in stations:
        try:
            stat.is_station()
        except Exception:
            raise TypeError("invalid station, station was {}".format(type(stat)))

    # create list of tuples sorted by their haversine distance
    distances = sorted_by_key(
        [(stat, haversine(p, stat.coord)) for stat in stations], 1
    )

    # returns the list
    return distances


def stations_within_radius(stations, centre, r):
    """Returns the stations that are within rkm from the coordinate centre
    stations should be a list of MonitoringStation objects
    centre should be a 2d tuple
    r should be a posotive float"""

    # getting sorted stations and carrying forward exceptions
    try:
        sorted_stations = stations_by_distance(stations, centre)
    except Exception as e:
        raise e

    # validation for r
    if type(r) != float and type(r) != int:
        raise TypeError("invalid radius, radius was type {}".format(type(r)))

    if r < 0:
        raise ValueError("invalid raidus, radius was negative")

    index = (
        binary_search_highest_lesser(sorted_stations, 1, r, 0, len(sorted_stations)) + 1
    )

    return [stat[0] for stat in sorted_stations[:index]]


# for 1D
def rivers_with_station(stations):

    """
    given a list of station objects
    returns a list/tuple/set with the names of the rivers with a monitoring station.
    """

    temp = []
    for n in stations:
        temp.append(n.river)
    rivers = set(temp)
    return rivers


def stations_by_river(stations):

    """
    returns a Python dict that maps river names (the ‘key’) to a list of station objects on a given river.
    """

    river_stations = {}
    for n in stations:
        if n.river in river_stations:
            river_stations[n.river].append(n.name)
        else:
            # can river be empty??
            river_stations[n.river] = [n.name]
    return river_stations


# for 1E
def rivers_by_station_number(stations, N):
    """
    determines the N rivers with the greatest number of monitoring stations.
    return a list of (river name, number of stations) tuples, sorted by the number of stations.
    In the case that there are more rivers with the same number of stations as the N th entry, include these rivers in the list.
    """
    # use dict created for 1D
    riverstation_dict = stations_by_river(stations)
    riverstation_number = []

    # iterate over keys (rivers), unordered list created
    for n in riverstation_dict:
        riverstation_number.append((n, len(riverstation_dict[n])))

    # sort list
    riverstation_number.sort(key=lambda river: river[1], reverse=True)

    # get the Nth value of number of stations
    n_value = riverstation_number[N][1]

    # include all >= Nth value tuples in the list
    result = []
    for n in riverstation_number:
        if n[1] >= n_value:
            result.append(n)
        else:
            break
    return result