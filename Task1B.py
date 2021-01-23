from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_by_distance
from haversine import haversine, Unit

def run():
    """Requirements for Task 1A"""

    # Build list of stations
    stations = build_station_list()

    #sort stations
    sorted_stations = stations_by_distance(stations,(52.2053, 0.1218))

    #print data from closest 10
    print("Closest 10")
    print([(stat[0].name,stat[0].town,stat[1]) for stat in sorted_stations[:10]])

    #print data from furthest 10
    print("Furthest 10")
    print([(stat[0].name,stat[0].town,stat[1]) for stat in sorted_stations[len(stations)-10:]])



if __name__ == "__main__":
    print("*** Task 1A: CUED Part IA Flood Warning System ***")
    run()
