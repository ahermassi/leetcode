""" Given an array of integers nums, write a method that returns the "pivot" index of this array.
We define the pivot index as the index where the sum of the numbers to the left of the index is equal to the sum of the
numbers to the right of the index.
If no such index exists, we should return -1. If there are multiple pivot indexes, you should return the left-most
pivot index. """

import unittest2 as unittest


def pivot_index(nums):
    """ Prefix sum.
        We need to quickly compute the sum of values to the left and the right of every index.
        Let's say we knew S as the sum of the numbers, and we are at index i. If we knew the sum of numbers left_sum
        that are to the left of index i, then the other sum to the right of the index would just be
        S - nums[i] - left_sum.
        As such, we only need to know about left_sum to check whether an index is a pivot index in constant time.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left_sum, s = 0, sum(nums)
    for index, num in enumerate(nums):
        right_sum = s - left_sum - num
        if left_sum == right_sum:
            return index
        left_sum += num
    return -1


class Test(unittest.TestCase):
    data = [([1, 7, 3, 6, 5, 6], 3),
            ([1, 2, 3], -1),
            ]

    def test_pivot_index(self):
        for test_array, result in self.data:
            self.assertEqual(result, pivot_index(test_array))


if __name__ == '__main__':
    unittest.main()