from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.analysis import eval_risk
from floodsystem.plot import plot_water_levels_with_fit
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
import datetime

def run():
    """Requirements for Task 2F"""

    # Build list of stations
    stations = build_station_list()

    # update water levels
    update_water_levels(stations)

    #sorting stations so that only the highest risk ones are considered
    sorted_stations = stations_highest_rel_level(stations, 100)


    #sorting the stations by their town
    towns = []
    town_stations = []
    NoOfStations = len(stations)

    #starting the town-station lists and remocing duplicate stations
    for stat in sorted_stations:
        stations.remove(stat)
        try:
            town_stations[towns.index(stat.town)].append(stat)
        except:
            towns.append(stat.town)
            town_stations.append([])
            town_stations[len(town_stations)-1].append(stat)
    

    count = 0

    """
     this uses a more complex algorithm to look closely at the 100 highest ratio stations
     only 100 are looked at due to the time taken to request data from the API
     if the program did not have to finish in 5 minuets all stations would go through this taking 
     approx 10-15 minuets. It must compleate in 5 mins due to GitHub limitations
    """

    for i in range(len(towns)):
        eval_risk(town_stations[i])
        count += len(town_stations[i])
        # progress indicator
        if count % 10 == 0: print("{} / {} stations done".format(count, NoOfStations))


    #this adds all stations to the town-station lists, and sets their highest ratio naively
    for i in range(len(stations)):
        stations[i].set_highest_ratio(stations[i].relative_water_level())
        try:
            town_stations[towns.index(stations[i].town)].append(stations[i])
        except:
            towns.append(stations[i].town)
            town_stations.append([])
            town_stations[len(town_stations)-1].append(stations[i])

        count += 1
        #progress indicator
        if count % 1000 == 0: print("{} / {} stations done".format(count, NoOfStations))


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()