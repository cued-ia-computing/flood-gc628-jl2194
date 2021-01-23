"""Unit test for the utils module"""

import floodsystem.utils
import pytest

def test_sort():
    """Test sort container by specific index"""

    a = (10, 3, 3)
    b = (5, 1, -1)
    c = (1, -3, 4)
    list0 = (a, b, c)

    # Test sort on 1st entry
    list1 = floodsystem.utils.sorted_by_key(list0, 0)
    assert list1[0] == c
    assert list1[1] == b
    assert list1[2] == a

    # Test sort on 2nd entry
    list1 = floodsystem.utils.sorted_by_key(list0, 1)
    assert list1[0] == c
    assert list1[1] == b
    assert list1[2] == a

    # Test sort on 3rd entry
    list1 = floodsystem.utils.sorted_by_key(list0, 2)
    assert list1[0] == b
    assert list1[1] == a
    assert list1[2] == c


def test_reverse_sort():
    """Test sort container by specific index (reverse)"""

    a = (10, 3, 3)
    b = (5, 1, -1)
    c = (1, -3, 4)
    list0 = (a, b, c)

    # Test sort on 1st entry
    list1 = floodsystem.utils.sorted_by_key(list0, 0, reverse=True)
    assert list1[0] == a
    assert list1[1] == b
    assert list1[2] == c

    # Test sort on 2nd entry
    list1 = floodsystem.utils.sorted_by_key(list0, 1, reverse=True)
    assert list1[0] == a
    assert list1[1] == b
    assert list1[2] == c

    # Test sort on 3rd entry
    list1 = floodsystem.utils.sorted_by_key(list0, 2, reverse=True)
    assert list1[0] == c
    assert list1[1] == a
    assert list1[2] == b

def test_binary_search_highest_lesser():
    """Test binary search in specific dimension"""

    a = (1, 1, 3)
    b = (3, 5, 3)
    c = (5, 2, 3)
    list0 = (a, b, c)

    # Test search on 1st entry , normal list
    assert floodsystem.utils.binary_search_highest_lesser(list0,0,4,0,len(list0)) == 1

    # Test search on 2nd entry , invalid list
    with pytest.raises(ValueError) as e:
        floodsystem.utils.binary_search_highest_lesser(list0,1,4,0,len(list0))
    assert "list was not searchable" in str(e)

    # Test search on 3rd entry , duplicated answer
    assert floodsystem.utils.binary_search_highest_lesser(list0,2,3,0,len(list0)) == 2

