from floodsystem.geo import stations_by_river, rivers_by_station_number
from floodsystem.stationdata import build_station_list


def run():
    # build list of stations
    stations = build_station_list()

    # prints the list of (river, number stations) tuples when N = 9
    print(rivers_by_station_number(stations, 9))


if __name__ == "__main__":
    print("*** Task 1E: CUED Part IA Flood Warning System ***")
    run()
