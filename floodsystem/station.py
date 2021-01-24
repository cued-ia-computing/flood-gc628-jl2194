# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides a model for a monitoring station, and tools
for manipulating/modifying station data

"""
def inconsistent_typical_range_stations(stations):
    """ this takes a list of MonitoringStations and returns
    a sub list of those stations with invalid typical ranges"""
    return [stat for stat in stations if stat.typical_range_consistent() == False]


class MonitoringStation:
    """This class represents a river level monitoring station"""

    def __init__(self, station_id, measure_id, label, coord, typical_range,
                 river, town):

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

        self.latest_level = None

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

    def __lt__(self,other):
        """ this makes the class sortable"""
        if self.name < other.name:
            print(self.name, other.name)
            return  self
        print(other.name, self.name)
        return other

    def typical_range_consistent(self):
        """this returns true if the objects typical range is valid"""
        if self.typical_range == None or self.typical_range[0] > self.typical_range[1]:
            return False
        return True
