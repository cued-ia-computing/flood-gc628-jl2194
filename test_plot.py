"""unit tests for plot submodule"""
from floodsystem.stationdata import build_station_list
from floodsystem.plot import plot_water_levels
from floodsystem.plot import plot_water_levels_with_fit
from floodsystem.plot import plot_data
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.geo import stations_by_distance
import matplotlib.pyplot as plt
import datetime
import pytest

def test_plot_water_levels_with_fit():
    """cannot assert if data is plotter correctly, so instead
    the program creates a graph and checks if it crashes
    """
    #get stations
    stations = build_station_list()

    dates = []
    levels = []

    for stat in stations[:1]:
        temp = fetch_measure_levels(stat.measure_id, dt=datetime.timedelta(days=2))
        dates.append(temp[0])
        levels.append(temp[1])

    #1 station
    plot_water_levels_with_fit(stations[0],dates[0],levels[0],4)

def test_plot_water_levels():
    """cannot assert if data is plotted correctly, so instead
    the program creates 3 graphs for 3 cases and checks if it crashed
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
    print("*** Task 2F: CUED Part IA Flood Warning System ***")
    test_plot_water_levels_with_fit()