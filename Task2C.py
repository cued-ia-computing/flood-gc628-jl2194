from floodsystem.stationdata import build_station_list
from floodsystem.flood import stations_highest_rel_level


def run():

    # Build list of stations
    stations = build_station_list()

    # update water levels
    update_water_levels(stations)

    # return a list of top 10 water level stations
    result = stations_highest_rel_level(stations, 10)

    # Print station and water level
    for n in range(len(result)):
        print(str(result[n].name) + " " + str(result[n].relative_water_level()))


if __name__ == "__main__":
    print("*** Task 2C: CUED Part IA Flood Warning System ***")
    run()
