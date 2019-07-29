""" Given an array of integers that is already sorted in ascending order, find two numbers such that they add up to a
specific target number.
Your returned answers (both index1 and index2) are not zero-based.
"""

import unittest2 as unittest


def two_sum_v1(numbers, target):
    """ While we iterate and insert elements into the hash table, we also look back to check if current element's
    complement already exists in the hash table. If it exists, we have found a solution and return immediately.
    Time complexity: O(N) for array pass
    Space complexity: O(N)
    """
    vals = {}
    for i, v in enumerate(numbers, 1):  # enumerate(numbers, 1) to account for 1-based indexing
        try:  # EAFP fashion
            return [vals[target - v], i]
        except KeyError:
            vals[v] = i


class Test(unittest.TestCase):
    data = ([2, 7, 11, 15], 9)

    def test_two_sum(self):
        self.assertEqual([1, 2], two_sum_v1(self.data[0], self.data[1]))
        # self.assertEqual([0, 1], two_sum_v2(self.data[0], self.data[1]))
        # self.assertEqual([0, 1], two_sum_v3(self.data[0], self.data[1]))


if __name__ == '__main__':
    unittest.main()