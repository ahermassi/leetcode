""" Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice. """

import unittest2 as unittest


def two_sum_v1(nums, target):
    """ Brute force approach. Not the best performance.
    Time complexity: O(N ** 2)
    Space complexity: O(1)
    """
    for i in range(len(nums)):
        s = nums[i]
        for j in range(i + 1, len(nums)):
            if s + nums[j] == target:
                return [i, j]


def two_sum_v2(nums, target):
    """ Using a hash table and one array pass. Trading space for time complexity.
    Time complexity: O(N) for array pass
    Space complexity: O(N)
    """
    d = {v: i for i, v in enumerate(nums)}
    for i in range(len(nums)):
        s = nums[i]
        if d.get(target - s) and d.get(target - s) != i:  # The complement (target - s) found in O(1) lookup
            return [i, d.get(target - s)]


class Test(unittest.TestCase):
    data = ([2, 7, 11, 15], 9)

    def test_two_sum(self):
        self.assertEqual([0, 1], two_sum_v2(self.data[0], self.data[1]))


if __name__ == '__main__':
    unittest.main()