import matplotlib.pyplot as plt
from datetime import datetime, timedelta
"""This module contains a collection of functions related to
plotting data.

"""

def cure_levels(levels):
    """this fixes any issues with level data
    levels should be a list generated by the fetch_measure_levels submodule
    """
    for i in range(len(levels)):
        if type(levels[i]) == list or type(levels[i]) == tuple:
            levels[i] = levels[i][0]
        elif type(levels[i]) != float:
            #checking if it is an number or something else
            try:
                levels[i] = float(levels[i])
            except Exception:
                levels[i]=0.0
    return levels

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

        return
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

    