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


def missing_number_v2(nums):
    """ if we initialize an integer to n and XOR it with every index and value, we will be left with the missing number.
    Time complexity: O(N) assuming that XOR is a constant-time operation
    Space complexity: O(1)
    """
    missing = len(nums)
    for i, num in enumerate(nums):
        missing ^= i ^ num
    return missing


def missing_number_v3(nums):
    """ A brute force method would be to simply check for the presence of each number that we expect to be present. Use
         a set to get constant time containment queries and overall linear runtime.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    num_set = set(nums)
    for number in range(len(nums) + 1):
        if number not in num_set:
            return number


class Test(unittest.TestCase):
    data = [([3, 0, 1], 2), ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8)]

    def test_missing_number(self):
        for test_array, result in self.data:
            self.assertEqual(result, missing_number_v1(test_array))
            self.assertEqual(result, missing_number_v2(test_array))
            self.assertEqual(result, missing_number_v3(test_array))


if __name__ == '__main__':
    unittest.main()
