from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_within_radius


def run():
    """ Requirements for Task 1B"""

    # build list of stations
    stations = build_station_list()
    stations = stations_within_radius(stations, (52.2053, 0.1218), 10)

    station_names = [station.name for station in stations]
    print(sorted(station_names))

if __name__ == "__main__":
    print("*** Task 1C: CUED Part IA Flood Warning System ***")
    run()
