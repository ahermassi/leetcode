""" Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊
n/2 ⌋ times.
You may assume that the array is non-empty and the majority element always exist in the array. """

from collections import defaultdict

import unittest2 as unittest


def majority_element_v1(nums):
    """ Basic hash map solution with one pass.
    Time complexity: O(N / 2) in the best case where all instances of the majority element appear at the beginning of
    nums. O(N) in the worst case
    Space complexity: O(N) in the worst case, O(1) in the best case.
    """
    n, count = len(nums), defaultdict(int)
    for num in nums:
        count[num] += 1
        if count[num] > n // 2:
            return num


class Test(unittest.TestCase):
    data = [([3, 2, 3], 3), ([2, 2, 1, 1, 1, 2, 2], 2)]

    def test_majority_element(self):
        for test_array, result in self.data:
            self.assertEqual(result, majority_element_v1(test_array))


if __name__ == '__main__':
    unittest.main()
