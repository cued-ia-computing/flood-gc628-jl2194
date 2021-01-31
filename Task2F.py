from floodsystem.stationdata import build_station_list
from floodsystem.plot import plot_water_levels_with_fit
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
import datetime


def run():
    """Requirements for Task 2F"""

    # Build list of stations
    stations = build_station_list()

    dt = 2
    station_no = 5
    dates = []
    levels = []

    #getting level data and sorting
    sorted_stations = stations_highest_rel_level(stations,2 * station_no)

    valid = 0
    offset = 0
    stations = []

    #ensures that all stations have data in time period
    while(valid < station_no):
        #if not enough stations can be found, implies issue somewhere else
        if valid + offset == len(sorted_stations):
            print("could not find enough valid stations in {} stations".format(2 * station_no))
            raise ValueError('too many invalid stations')
        temp = fetch_measure_levels(sorted_stations[valid+offset].measure_id, dt=datetime.timedelta(days=dt))

        #if no data exsists
        #this is needed because the code to get water levels
        #uses the last level which might not be in the dt timeframe
        if len(temp[0]) == 0:
            print("{} station had no data, using next highest".format(sorted_stations[valid+offset].name))
            offset += 1
        else:
            dates.append(temp[0])
            levels.append(temp[1])
            stations.append(sorted_stations[valid+offset])
            valid += 1


    for i in range(station_no):
        plot_water_levels_with_fit(stations[i],dates[i],levels[i],4)    

if __name__ == "__main__":
    print("*** Task 2F: CUED Part IA Flood Warning System ***")
    run()