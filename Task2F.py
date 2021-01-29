from floodsystem.stationdata import build_station_list
from floodsystem.plot import plot_water_levels_with_fit
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.geo import stations_by_distance
import datetime


def run():
    """Requirements for Task 2F"""

    # Build list of stations
    stations = build_station_list()

    # Print number of stations

    # using distance to my town untill risk is implimented
    sorted_stations = stations_by_distance(stations, (52.095211, -1.946930))

    dt = 2
    station_no = 5
    dates = []
    levels = []
    
    for stat in sorted_stations[:station_no]:
        temp = fetch_measure_levels(stat[0].measure_id, dt=datetime.timedelta(days=dt))
        dates.append(temp[0])
        levels.append(temp[1])

    # for all 5 stations
    for i in range(0,5):
        plot_water_levels_with_fit(sorted_stations[i][0],dates[i],levels[i],4)
    

if __name__ == "__main__":
    print("*** Task 2F: CUED Part IA Flood Warning System ***")
    run()