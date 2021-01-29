"""This module provides functionality for performing data analysis
"""
import numpy as np
import matplotlib
import datetime

def cure_levels(levels):
    """this fixes any issues with level data
    levels should be a list generated by the fetch_measure_levels submodule
    this is here to fix circular dependancies
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

def polyfit(dates, levels, p):
    """returns a least-squares fit of order p
    dates = a list of dates
    levels = a list of floats
    p = an int
    """
    #ensure data is of correct type
    if type(p) != int or type(dates) != list or type(levels) != list:
        raise TypeError('variable of wrong type, p={}, dates={}, levels={}'.format(type(p),type(dates),type(levels)))
    if type(dates[0]) != datetime.datetime:
        raise TypeError('dates were of wrong type dates={}'.format(type(dates)))
    levels = cure_levels(levels)

    if len(levels) != len(dates):
        raise ValueError('mismatched list lengths levels={}, dates={}'.format(len(levels),len(dates)))
    if p<0:
        raise ValueError('invalid p, p was {}'.format(p))
    
    #return polyfit
    try:
        return np.poly1d(np.polyfit(matplotlib.dates.date2num(dates),levels,p))
    except Exception as e:
        raise e