"""unit tests for plot submodule"""
from floodsystem.stationdata import build_station_list
from floodsystem.plot import plot_water_levels
from floodsystem.plot import cure_levels
from floodsystem.plot import plot_data
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.geo import stations_by_distance
import matplotlib.pyplot as plt
import datetime
import pytest

def test_cure_levels():
    #create normal test data
    levels = [0.1, 0.2]
    assert cure_levels(levels) == [0.1, 0.2]

    #create data to be cured
    levels = [0.1, [0.2, 0.3], (0.3, 0.4), 'a']
    assert cure_levels(levels) == [0.1, 0.2, 0.3, 0.0]

def test_plot_water_levels():
    """cannot assert if data is plotted correctly, so instead
    the program cretes 3 graphs for 3 cases and checks if it crashed
    """
    #get stations
    stations = build_station_list()

    dates = []
    levels = []

    for stat in stations[:4]:
        temp = fetch_measure_levels(stat.measure_id, dt=datetime.timedelta(days=2))
        dates.append(temp[0])
        levels.append(temp[1])

    #1 station
    plot_water_levels(stations[0],dates[0],levels[0])

    #prime number of stations
    plot_water_levels(stations[:3],dates[:3],levels[:3])

    #non prime + non 1 stations
    plot_water_levels(stations[:4],dates[:4],levels[:4])

def test_plot_data():
    """cannot assert if data is plotted correctly, so instead
    the program cretes a graphs and checks if it crashed
    """
     #get stations
    stations = build_station_list()

    dates = []
    levels = []

    for stat in stations[:4]:
        temp = fetch_measure_levels(stat.measure_id, dt=datetime.timedelta(days=2))
        dates.append(temp[0])
        levels.append(temp[1])

    #1 station
    plot_water_levels(stations[0],dates[0],levels[0])

    fig , axs = plt.subplots(2, 2, sharex = True, sharey = True)
    plot_data(axs[0, 0],stations[0], dates[0], levels[0])


    

if __name__ == "__main__":
    print("*** Task 2E: CUED Part IA Flood Warning System ***")
    test_plot_data()