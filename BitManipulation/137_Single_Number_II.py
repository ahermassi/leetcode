""" Given an integer array nums where every element appears three times except for one, which appears exactly once.
Find the single element and return it.

You must implement a solution with a linear runtime complexity and use only constant extra space.
"""
from collections import defaultdict
import unittest2 as unittest


def single_number_v1(nums):
    """ The naive approach is to count the frequency of every integer in nums. Then we can iterate over the counter to
         find the key which has a value of 1.

    Time complexity: O(N)
    Space complexity: O(N), there will be approximately N/3 keys, so the space complexity is O(N/3) which is O(N)
    """
    counter = defaultdict(int)
    for num in nums:
        counter[num] += 1
    for num, count in counter.items():
        if count == 1:
            return num


def single_number_v2(nums):
    """ Given an array, its set counterpart num_set will have all the integers of the array, but without duplicates.

         Let there be k integers that have three occurrences in the array. These integers can be enumerated as
         x1, x2,..., xk. Let y be the loner.

         The sum of the num_set will be S_set = x1 + x2 + ... + xk + y --> S_set - y = x1 + x2 + ... + xk
         The sum of nums will be S_nums = 3*x1 + 3*x2 + ... + 3*xk + y = 3 * (S_set - y) + y = 3*S_set - 2*y
         --> S_sums = 3*S_set - 2*y
         --> 2*y = 3*S_set - S_nums
         Therefore, the loner y will be: (3*S_set - S_nums) / 2

    Time complexity: O(N)
    Space complexity: O(N), there will be approximately N/3 integers in the hash set, so the space complexity is O(N/3)
    which is O(N)
    """
    return (3 * sum(set(nums)) - sum(nums)) // 2
