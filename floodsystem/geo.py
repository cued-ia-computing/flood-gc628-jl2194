# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
from haversine import haversine, Unit

def stations_by_distance(stations, p):
    """Returns the stations list sorted by their great-circle distance
    from a given latitude and longitude (p)
    p should be a 2d tuple 
    stations should be a list of MonitoringStation
    objects
    """

    #make sure that p is valid
    #checing p type and length, and values type and range
    if type(p) != tuple or len(p)!=2 or type(p[0]) != float or type(p[1]) != float or abs(p[0]) > 180 or abs(p[1]) > 180 :
        raise TypeError('invalid point, point was {}'.format(p))

    for stat in stations:
        try:
            stat.is_station()
        except Exception:
            raise TypeError('invalid station, station was {}'.format(type(stat)))

    #create list of tuples sorted by their haversine distance
    distances = sorted_by_key([(stat,haversine(p,stat.coord)) for stat in stations],1)
    
    #returns the list
    return distances
