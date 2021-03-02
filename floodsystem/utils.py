# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains utility functions.

"""

import numpy

def sorted_by_key(x, i, reverse=False):
    """For a list of lists/tuples, return list sorted by the ith
    component of the list/tuple, E.g.

    Sort on first entry of tuple:

      > sorted_by_key([(1, 2), (5, 1]), 0)
      >>> [(1, 2), (5, 1)]

    Sort on second entry of tuple:

      > sorted_by_key([(1, 2), (5, 1]), 1)
      >>> [(5, 1), (1, 2)]

    """

    # Sort by distance
    def key(element):
      try:
        return element[i]
      except Exception:
        print(element)
      return None

    return sorted(x, key=key, reverse=reverse)

def binary_search_highest_lesser(items,dimension,value,start,end):
  """finds the index of the last value to be less than the search value
  dimension is used to search 2D arrays
  list - any list where list[i][dimension] is sortable
  dimension - posotive int
  value - search value, same type as list[i][dimension]
  start- int start index
  end - int end index
  """

  # returning found value
  if start + 1 == end:
    if end < len(items) - 1 and items[end][dimension] > items[end + 1][dimension]:
      raise ValueError('list was not searchable')

    # dealing with 1 off errors
    if end < len(items) and items[end][dimension] < value:
      return end
    return start

  # errors in bounds
  if start > end:
    raise ValueError('start index was higher than end index')

  # choose new pivot point
  mid = (start + end) // 2

  # this ensures that duplicates are dealt with correctly
  if value == items[mid][dimension]:
    while mid < len(items) - 1 and items[mid + 1][dimension] == value:
      mid += 1
    return mid
  
  # call the next itteration
  if value < items[mid][dimension]:
    return binary_search_highest_lesser(items, dimension, value, start, mid)
  return binary_search_highest_lesser(items, dimension, value, mid, end)

def haversine(start,end):
  """this impliments the haversine formula, which calculates the great circle distance
  between 2 points
  start and end should be (float,float)
  """
  # r2 = twice the radius of the earth
  r2 = 2 * 6371.0088

  # checking for tuples
  if type(start) != tuple or type(end) != tuple:
    raise TypeError('One of the points is the wrong type start = {} , end = {}'.format(start,end))

  # making sure types are consitant
  if type(start[0]) != type(start[1]) or type(end[0]) != type(end[1]) or type(start[0]) != type(start[1]):
    raise TypeError('One of the points is the wrong type start = {} , end = {}'.format(start,end))

  # making sure that types are valid
  if type(start[0]) != float:
    raise TypeError('One of the points is the wrong type start = {} , end = {}'.format(start,end))

  # converting lat , long into radians
  start = [val * numpy.pi / 180 for val in start]
  end = [val * numpy.pi / 180 for val in end]

  # haversine formula found at 
  # https://en.wikipedia.org/wiki/Haversine_formula#:~:text=The%20haversine%20formula%20determines%20the,and%20angles%20of%20spherical%20triangles.
  value = numpy.sin((end[0] - start[0]) / 2) ** 2
  value += numpy.cos(start[0]) * numpy.cos(end[0]) * (numpy.sin((end[1] - start[1]) / 2) ** 2) 
  return  r2 *numpy.arcsin(numpy.sqrt(value))
