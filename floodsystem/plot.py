import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
from floodsystem.analysis import polyfit
from floodsystem.analysis import cure_levels
"""This module contains a collection of functions related to
plotting data.

"""

def plot_data(axes, stations, dates, levels):
    """plots a graph using the given data, used to reduce code complexity
    axes should be a MatplotLib Axes
    station should be 1 station
    dates should be a list of dates
    levels should be a list created by fetch_measure_levels
    """
    #create graph of raw data
    axes.scatter(dates, cure_levels(levels))
    #title graph correectly
    axes.set_title(stations.name)
    #add typical value lines
    axes.hlines(stations.typical_range,dates[0], dates[len(dates)-1],['g','r'])

    return axes



def plot_water_levels(stations, dates, levels):
    import matplotlib.pyplot as plt
    """ plots a water levels against dates for an arbitary amount of stations
    stations is a list of stations
    dates is a list of list of datetimes
    levels is a list of list of floats
    """

    # if there are multiple stations
    if type(stations) == list and len(stations) > 1:
        # make sure that the lists are of the same length
        if len(stations) != len(dates) or len(dates) != len(levels):
            raise ValueError('Mismached list lengths stations={} dates={} levels={}'.format(len(stations),len(dates),len(levels)))

        #find best organisation
        height = len(stations) ** 0.5
        height -= height % 1
        while len(stations) % height != 0:
            height -= 1
        length = len(stations) / height

        height , length = int(max(height,length)) , int(min(height,length))
        
        # set up subplots
        fig , axs = plt.subplots(height, length, sharex = True, sharey = True)


        #for all stations
        for x in range(0,height):
            for y in range(0,length):
                # special case for prime numbers
                if length == 1:
                    axs[x]=plot_data(axs[x],stations[x],dates[x],levels[x])
                else:
                    # non prime and non 1 numbers
                    axs[x, y] = plot_data(axs[x, y], stations[(length * x) + y], dates[(length * x) + y], levels[(length * x) + y])
        
        # changing lables
        for ax in axs.flat:
            ax.set(xlabel='date', ylabel='water level (m)')
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
            ax.label_outer()

        plt.show()

        return axs
    else:
        #1 is a special case as it leads to non indexiable subplots if handled normally
        if type(stations) == list:
            # correcting list input into single values
            stations = stations[0]
            dates = dates[0]
            levels = levels[0]

        if stations.is_station():
            #plotting the actuall data
            plt.scatter(dates,cure_levels(levels))
            
            plt.hlines(stations.typical_range, dates[0], dates[len(dates)-1], ['g','r'])
            # adding title and displaying
            plt.title("{} water levels over time".format(stations.name))
            plt.xlabel('date')
            plt.ylabel('water level (m)')
            plt.xticks(rotation=45) 
            plt.show()
            return

    raise TypeError('station was not a station, station was a {}'.format(type(stations)))

def plot_water_levels_with_fit(station, dates, levels, p):
    import matplotlib.pyplot as plt
    """plots the water level of 1 station over time, along side a line of best fit
    station should be a station
    date should be a list of dates
    level should be a list of floats
    p should be an int
    """
    #this validates all of the values and gets the best fit
    try:
        poly = polyfit(dates,levels,p)
    except Exception as e:
        raise e
    if station.is_station() == False:
        raise TypeError('station was not a station, it was a'.format(type(station)))

    #plotting the actuall data
    plt.scatter(dates,cure_levels(levels))
    plt.plot(dates,poly(matplotlib.dates.date2num(dates)))
    plt.hlines(station.typical_range, dates[0], dates[len(dates)-1], ['g','r'])
    # adding title and displaying
    plt.title("{} water levels over time".format(station.name))
    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45) 
    plt.show()

    return



    