"""This module provides functionality for performing data analysis
"""
import numpy as np
import matplotlib
import datetime
from datetime import datetime, timedelta
from .datafetcher import fetch_measure_levels
from matplotlib.dates import date2num as date2num
from matplotlib.dates import num2date as num2date


def cure_levels(levels):
    """this fixes any issues with level data
    levels should be a list generated by the fetch_measure_levels submodule
    this is here to fix circular dependancies
    """
    for i in range(len(levels)):
        if type(levels[i]) == list or type(levels[i]) == tuple:
            levels[i] = levels[i][0]
        elif type(levels[i]) != float:
            # checking if it is an number or something else
            try:
                levels[i] = float(levels[i])
            except Exception:
                levels[i] = 0.0
    return levels


def polyfit(dates, levels, p):
    """returns a least-squares fit of order p
    dates = a list of dates
    levels = a list of floats
    p = an int
    """
    # ensure data is of correct type
    if type(p) != int or type(dates) != list or type(levels) != list or len(dates) == 0:
        raise TypeError(
            "variable of wrong type, p={}, dates={}, levels={}".format(
                type(p), type(dates), type(levels)
            )
        )

    if type(dates[0]) != datetime:
        raise TypeError("dates were of wrong type dates={}".format(type(dates)))
    levels = cure_levels(levels)

    if len(levels) != len(dates):
        # truncate length of longer list so that polyfit can be done
        if len(dates) > len(levels):
            dates = dates[: len(levels)]
        else:
            levels = levels[: len(dates)]
        # raise ValueError('mismatched list lengths levels={}, dates={}'.format(len(levels),len(dates)))
    if p < 0:
        raise ValueError("invalid p, p was {}".format(p))

    # return polyfit
    try:
        return np.poly1d(np.polyfit(matplotlib.dates.date2num(dates), levels, p))
    except Exception as e:
        raise e


def eval_risk(stations, n=3):
    """evaluates the highest expected water levels in the next 2 days of a list of stations
    stations = list of station datas
    thresholds = list of values used to sort stations into risk factors
    """

    PastDt = 5
    FutureDt = 2

    for stat in stations:

        # checking for invalid stations
        if stat.typical_range == None:
            print("station had no typical range, name = {}".format(stat.name))
            continue

        # gets data for time period
        temp = fetch_measure_levels(stat.measure_id, dt=timedelta(days=PastDt))

        # if no data exsists
        # this is needed because the code to get water levels
        # uses the last level which might not be in the dt timeframe
        if len(temp[0]) == 0:
            print("{} station had no data, checking next".format(stat.name))
            continue

        # storing data
        dates = temp[0]
        levels = temp[1]

        # computes the polyfit and its derivitive
        waterLevel = polyfit(
            num2date(date2num(dates) - date2num(datetime.today())), levels, n
        )

        waterChange = np.polynomial.polynomial.polyder(waterLevel)

        # this gets rid of complex roots
        roots = np.polynomial.polynomial.polyroots(waterChange)
        curedRoots = []

        for root in roots:
            if type(root) != np.complex128 or root.imag == 0.0:
                if type(root) == np.complex128:
                    root = root.real

                # make sure root is in range
                if root > 0 and root < FutureDt:
                    curedRoots.append(root)

        # default value is the current one or the last one
        highestLevel = waterLevel(0)
        highestLevel = max(highestLevel, waterLevel(FutureDt))

        for root in curedRoots:
            highestLevel = max(highestLevel, waterLevel(root))

        # convert highest level into ratio
        stat.set_highest_ratio(
            (highestLevel - stat.typical_range[0])
            / (stat.typical_range[1] - stat.typical_range[0])
        )
    return


def risk_calculation(towns, town_stations):
    """
    this function returns a list with tuples [(town, risk)]
    towns is a list of all the towns
    town_stations is a list which includes lists of stations in different towns.
    The index for these two lists are matched.
    """

    town_risk = []

    # check for valid

    # Add town and values to list
    for n in range(len(towns)):
        # the risk value takes the average of sum of exponential for each station in a town
        risk_value = 0
        for m in town_stations[n]:
            # check for valid stations
            if m.highest_ratio == None:
                continue
            risk_value += np.exp(float(m.highest_ratio))
        risk_value /= len(town_stations[n])

        town_risk.append((towns[n], risk_value))

    return town_risk