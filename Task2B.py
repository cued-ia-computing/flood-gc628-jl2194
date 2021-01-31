from floodsystem.stationdata import build_station_list
from floodsystem.flood import stations_level_over_threshold


def run():

    # Build list of stations
    stations = build_station_list()

    # return a list of stations with water level over 0.8
    result = stations_level_over_threshold(stations, 0.8)

    # Print station and water level
    for n in range(len(result)):
        print(str(result[n][0].name) + " " + str(result[n][1]))


if __name__ == "__main__":
    print("*** Task 2B: CUED Part IA Flood Warning System ***")
    run()
