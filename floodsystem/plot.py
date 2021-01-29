import matplotlib.pyplot as plt
from datetime import datetime, timedelta
"""This module contains a collection of functions related to
plotting data.

"""

def plot_water_levels(stations, dates, levels):
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
                # prime numbers
                if length == 1:
                    # try catch needed as someimtes levels contains tuples instead of floats
                    # seems to be bad data from the source that gets through
                    #plot data
                    try:
                        axs[x].scatter(dates[x], levels[x])
                    except Exception:
                        print('The dates and levels are mismatched, incorrect data fetched. dates = {} levels = {}'.format(dates[x], levels[x]))
                    
                    axs[x].set_title(stations[x].name)
                    #plot typical values
                    axs[x].hlines(stations[x].typical_range,dates[x][0], dates[x][len(dates[x])-1],['g','r'])
                else:
                    #plot data
                    try :
                        axs[x, y].scatter(dates[(length * x) + y], levels[(length * x) + y])
                    except Exception:
                        print('The dates and levels are mismatched, incorrect data fetched. dates = {} levels = {}'.format(dates[(length * x) + y], levels[(length * x) + y]))
                    
                    #plot typical values
                    axs[x, y].set_title(stations[(length * x) + y].name)
                    axs[x, y].hlines(stations[(length * x) + y].typical_range,dates[(length * x) + y][0], dates[(length * x) + y][len(dates[(length * x) + y])-1],['g','r'])
        
        # changing lables
        for ax in axs.flat:
            ax.set(xlabel='date', ylabel='water level (m)')
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
            ax.label_outer()

        plt.show()

        return
    else:
        if type(stations) == list:
            # correcting list input into single values
            stations = stations[0]
            dates = dates[0]
            levels = levels[0]

        if stations.is_station():
            #plotting the actuall data
            try:
                plt.scatter(dates,levels)
            except Exception:
                print('The dates and levels are mismatched, incorrect data fetched. dates = {} levels = {}'.format(dates, levels))
            
            plt.hlines(stations.typical_range, dates[0], dates[len(dates)-1], ['g','r'])
            # adding title and displaying
            plt.title("{} water levels over time".format(stations.name))
            plt.xlabel('date')
            plt.ylabel('water level (m)')
            plt.xticks(rotation=45) 
            plt.show()
            return

    raise TypeError('station was not a station, station was a {}'.format(type(stations)))

    