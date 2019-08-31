""" Given an array containing n distinct numbers taken from 0, 1, 2, ..., n, find the one that is missing from the
array. """

import unittest2 as unittest


def missing_number_v1(nums):
    """ We can compute the sum of nums in linear time, and by Gauss' formula, we can compute the sum of the first n
        natural numbers in constant time. Therefore, the number that is missing is simply the result of Gauss' formula
        minus the sum of nums.
    Time complexity: O(N), although Gauss' formula can be computed in O(1) time, summing nums costs O(n) time, so the
    algorithm is overall linear.
    Space complexity: O(1)
    """
    n = len(nums)
    return n * (n + 1) / 2 - sum(nums)


class Test(unittest.TestCase):
    data = [([3, 0, 1], 2), ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8)]

    def test_missing_number(self):
        for test_array, result in self.data:
            self.assertEqual(result, missing_number_v1(test_array))


if __name__ == '__main__':
    unittest.main()
