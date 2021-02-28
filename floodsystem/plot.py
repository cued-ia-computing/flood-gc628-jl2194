import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
from floodsystem.analysis import polyfit
from floodsystem.analysis import cure_levels
from matplotlib.dates import date2num as date2num
from matplotlib.dates import num2date as num2date
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

def plot_water_levels(stations, dates, levels, fit = False, p = 0):
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

        #if fits are needed generate all fits
        if fit:
            polys = []
            for i in range(len(stations)):
                try:
                    polys.append(polyfit(num2date(date2num(dates[i]) - date2num(datetime.today())),levels[i],p))
                except Exception as e:
                    raise e

        #for all stations
        for x in range(height):
            for y in range(length):
                # special case for prime numbers
                if length == 1:
                    axs[x]=plot_data(axs[x],stations[x],dates[x],levels[x])
                    if fit:
                        axs[x].plot(dates[x],polys[x](date2num(dates[x]) - date2num(datetime.today())),color = 'k')
                else:
                    # non prime and non 1 numbers
                    axs[x, y] = plot_data(axs[x, y], stations[(length * x) + y], dates[(length * x) + y], levels[(length * x) + y])
                    if fit:
                        axs[x, y].plot(dates[(length * x) + y],polys[(length * x) + y](date2num(dates[(length * x) + y]) - date2num(datetime.today())),color = 'k')
        
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

            #adding fit if needed
            if fit:
                try:
                    poly = polyfit(num2date(date2num(dates) - date2num(datetime.today())),levels,p)
                    print(poly)
                except Exception as e:
                    raise e
                plt.plot(dates,poly(date2num(dates) - date2num(datetime.today())),color = 'k')


            # adding title and displaying
            plt.title("{} water levels over time".format(stations.name))
            plt.xlabel('date')
            plt.ylabel('water level (m)')
            plt.xticks(rotation=45)
            plt.show() 
            return plt

    raise TypeError('station was not a station, station was a {}'.format(type(stations)))

def plot_water_levels_with_fit(stations, dates, levels, p):
    import matplotlib.pyplot as plt
    """plots the water level of 1 station over time, along side a line of best fit
    station should be a station
    date should be a list of dates
    level should be a list of floats
    p should be an int
    """
    try:
        axs = plot_water_levels(stations, dates, levels, True, p)
    except Exception as e:
        raise e

