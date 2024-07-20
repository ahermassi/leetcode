""" Given an integer array nums where every element appears three times except for one, which appears exactly once.
Find the single element and return it.

You must implement a solution with a linear runtime complexity and use only constant extra space.
"""
from collections import defaultdict
import unittest2 as unittest


def single_number(nums):
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
