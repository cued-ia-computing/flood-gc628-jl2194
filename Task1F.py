from floodsystem.stationdata import build_station_list
from floodsystem.station import inconsistent_typical_range_stations

def run():
    """ Requirements for Task 1F"""

    # build list of stations
    stations = build_station_list()
    stations = inconsistent_typical_range_stations(stations)

    station_names = [station.name for station in stations]
    print(sorted(station_names))


if __name__ == "__main__":
    print("*** Task 1F: CUED Part IA Flood Warning System ***")
    run()
