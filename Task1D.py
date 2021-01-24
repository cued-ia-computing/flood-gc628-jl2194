# from floodsystem.geo import rivers_with_station, stations_by_river
from floodsystem.stationdata import build_station_list


# geo.py start


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


# geo.py end


def run():
    """ Requirements for Task 1D"""

    # (1/2)
    # build list of stations (?)
    stations = build_station_list()

    # build list of rivers
    rivers = rivers_with_station(stations)

    # print how many rivers have at least one monitoring station.
    num_river = len(rivers)
    print("{} rivers have at least one monitoring station".format(num_river))

    # print the first 10 of these rivers in alphabetical order.
    sorted_river = sorted(rivers)
    ten_rivers = sorted_river[:10]
    print(ten_rivers)

    # (2/2)
    # create dict of {river: stations}
    river_stations = stations_by_river(stations)

    # print the names of the stations located on the following rivers in alphabetical order
    # ‘River Aire’
    print("River Aire")
    stations_RiverAire = sorted(river_stations["River Aire"])
    print(stations_RiverAire)

    # ‘River Cam’
    print("River Cam")
    stations_Cam = sorted(river_stations["River Cam"])
    print(stations_Cam)

    # ‘River Thames’
    print("River Thames")
    stations_RiverThames = sorted(river_stations["River Thames"])
    print(stations_RiverThames)


if __name__ == "__main__":
    print("*** Task 1D: CUED Part IA Flood Warning System ***")
    run()
