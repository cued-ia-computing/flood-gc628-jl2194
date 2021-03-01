from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.analysis import eval_risk
from floodsystem.plot import plot_water_levels_with_fit
from floodsystem.datafetcher import fetch_measure_levels
import threading

import datetime

def run():
    """Requirements for Task 2F"""

    # Build list of stations
    stations = build_station_list()

    # update water levels
    update_water_levels(stations)

    #sorting the stations by their town
    towns = []
    town_stations = []

    for stat in stations:
        try:
            town_stations[towns.index(stat.town)].append(stat)
        except:
            towns.append(stat.town)
            town_stations.append([])
            town_stations[len(town_stations)-1].append(stat)
    

    count = 0
    
    for i in range(len(towns)):
        eval_risk(town_stations[i])
        count += len(town_stations[i])
        print("{} / {} towns done, {} / {} stations done".format(i, len(towns), count, len(stations)))
            
    


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()