# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains utility functions.

"""


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
