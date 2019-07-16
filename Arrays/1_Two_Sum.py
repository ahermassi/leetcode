""" Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice. """

import unittest2 as unittest


def two_sum(nums, target):
    """ Brute force approach. Not the best performance.
    Time complexity: O(N ** 2)
    Space complexity: O(1)
    """
    for i in range(len(nums)):
        s = nums[i]
        for j in range(i + 1, len(nums)):
            if s + nums[j] == target:
                return [i, j]


class Test(unittest.TestCase):
    data = ([2, 7, 11, 15], 9)

    def test_two_sum(self):
        self.assertEqual([0, 1], two_sum(self.data[0], self.data[1]))


if __name__ == '__main__':
    unittest.main()