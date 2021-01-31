from .station import MonitoringStation
from .stationdata import  update_water_levels


def stations_level_over_threshold(stations, tol):
    """
    returns a list of tuples
    each tuple holds:
    (i) a station (object) at which the latest relative water level is over tol
    (ii) the relative water level at the station.
    The returned list should be sorted by the relative level in descending order.
    """
    # update water levels
    update_water_levels(stations)

    # create an empty list
    level_list = []

    # iterate over the stations
    for station in stations:
        level = station.relative_water_level()

        # append (station object, level) only when consistent and over tol
        if level != None and level > tol:
            level_list.append((station, level))

    # sort list
    level_list.sort(key=lambda level: level[1], reverse=True)

    return level_list


def stations_highest_rel_level(stations, N):
    """
    returns a list of stations
    The returned list shopuld be sorted by the relative level in descending order
    and of lenth N
    """
    # update water levels
    update_water_levels(stations)

    # create an empty list
    level_list = []

    # iterate over the stations
    for station in stations:
        level = station.relative_water_level()

        # append (station object, level)
        if level != None:
            level_list.append((station, level))

    # sort and keep the top N
    level_list.sort(key=lambda level: level[1], reverse=True)

    new_level_list = []

    for n in range(N):
        new_level_list.append(level_list[n][0])

    return new_level_list
