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
    if type(p) != tuple or len(p)!= 2 or type(p[0]) != float or type(p[1]) != float or abs(p[0]) > 180 or abs(p[1]) > 180:
        raise TypeError('invalid point, point was {}'.format(p))

    for stat in stations:
        try:
            stat.is_station()
        except Exception:
            raise TypeError('invalid station, station was {}'.format(type(stat)))

    # create list of tuples sorted by their haversine distance
    distances = sorted_by_key([(stat, haversine(p, stat.coord)) for stat in stations], 1)

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
        raise TypeError('invalid radius, radius was type {}'.format(type(r)))

    if r < 0:
        raise ValueError('invalid raidus, radius was negative')

    index = binary_search_highest_lesser(sorted_stations, 1, r, 0, len(sorted_stations)) + 1

    return [stat[0] for stat in sorted_stations[:index]]
