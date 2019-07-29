""" Given a sorted array and a target value, return the index if the target is found. If not, return the index where
it would be if it were inserted in order.
You may assume no duplicates in the array. """

import unittest2 as unittest


def search_insert(nums, target):
    """ Typical binary search.
    Time complexity: O(log N)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    return left


class Test(unittest.TestCase):
    data = [([1, 3, 5, 6], 5, 2),
            ([1, 3, 5, 6], 2, 1),
            ([1, 3, 5, 6], 7, 4),
            ([1, 3, 5, 6], 0, 0)
            ]

    def test_search_insert(self):
        for test_array, target, result in self.data:
            self.assertEqual(result, search_insert(test_array, target))


if __name__ == '__main__':
    unittest.main()
