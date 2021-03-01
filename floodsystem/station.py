# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides a model for a monitoring station, and tools
for manipulating/modifying station data

"""


def inconsistent_typical_range_stations(stations):
    """this takes a list of MonitoringStations and returns
    a sub list of those stations with invalid typical ranges"""
    return [stat for stat in stations if stat.typical_range_consistent() == False]


class MonitoringStation:
    """This class represents a river level monitoring station"""

    def __init__(
        self, station_id, measure_id, label, coord, typical_range, river, town
    ):

        self.station_id = station_id
        self.measure_id = measure_id

        # Handle case of erroneous data where data system returns
        # '[label, label]' rather than 'label'
        self.name = label
        if isinstance(label, list):
            self.name = label[0]

        self.coord = coord
        self.typical_range = typical_range
        self.river = river
        self.town = town
        self.highest_ratio = 0

    def __repr__(self):
        d = "Station name:     {}\n".format(self.name)
        d += "   id:            {}\n".format(self.station_id)
        d += "   measure id:    {}\n".format(self.measure_id)
        d += "   coordinate:    {}\n".format(self.coord)
        d += "   town:          {}\n".format(self.town)
        d += "   river:         {}\n".format(self.river)
        d += "   typical range: {}".format(self.typical_range)
        return d

    def is_station(self):
        """ this is used to check if an object is a MoniteringStation"""
        return True

    def __lt__(self, other):
        """ this makes the class sortable"""
        if self.name < other.name:
            print(self.name, other.name)
            return self
        print(other.name, self.name)
        return other

    def typical_range_consistent(self):
        """this returns true if the objects typical range is valid"""
        if self.typical_range == None or self.typical_range[0] > self.typical_range[1]:
            return False
        return True

    def set_highest_ratio(self, ratio):
        """setter for highest ratio"""
        self.highest_ratio = ratio

    # for 2B
    def relative_water_level(self):
        """
        returns the latest water level as a fraction of the typical range
        i.e. a ratio of 1.0 corresponds to a level at the typical high and a ratio of 0.0 corresponds to a level at the typical low.
        If the necessary data is not available or is inconsistent, the function should return None.
        """
        # return None if data invalid
        if self.typical_range_consistent() == False or self.latest_level == None:
            return None

        # (lastest level - low)/(high - low)
        relative_wl = (self.latest_level - self.typical_range[0]) / (
            self.typical_range[1] - self.typical_range[0]
        )

        return relative_wl