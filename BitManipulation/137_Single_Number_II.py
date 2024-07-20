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


def single_number_v3(nums):
    """ What if all the numbers were clustered together? Then we can compare the first occurrence of each number with
         the element present at the next index. If they are the same, we can conclude that this element is not the
         loner. We don't need to traverse till the very end of the array.

         The integers can be clustered together by sorting the array.

         After sorting, we can check every integer with its next integer starting from the zeroth index. If they are the
         same, we can conclude that the integer is not the loner. We will jump three indices ahead. This is because we
         are given that if an integer is not the loner, it appears exactly three times. So, we can skip the next two
         indices. Otherwise, we can conclude that the integer is the loner and return it.

         The last index doesn't have any next index. Thus, if until the last index we don't find any loner, we can
         conclude that the last integer is the loner because nums has exactly one loner.

    Time complexity: O(N + N logN) = O(N logN
    Space complexity: O(N), for sorting
    """
    nums.sort()
    n = len(nums)
    i = 0
    while i < n - 1:
        if nums[i] == nums[i + 1]:
            i += 3
        else:
            return nums[i]
    return nums[-1]
