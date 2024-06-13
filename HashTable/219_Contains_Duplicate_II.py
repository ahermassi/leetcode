""" Given an integer array nums and an integer k, return true if there are two distinct indices i and j in the array
such that nums[i] == nums[j] and abs(i - j) <= k.
 """

from collections import defaultdict
import unittest2 as unittest


def contains_nearby_duplicate(nums, k):
    """ Loop through the elements of nums and check if the current element is present in the hashmap. If not present,
         then add (element, index) as key-val pair. If the current element is present in the dict, it is a duplicate.
         Return true if the difference between the current and stored indices is less than k.

    Time complexity: O(N), where N is the length of array
    Space complexity: O(N)
    """
    indices = dict()
    for i, num in enumerate(nums):
        if num in indices and i - indices[num] <= k:
            return True
        indices[num] = i
    return False


class Test(unittest.TestCase):
    data = [([1, 2, 3, 1], 3, True), ([1, 0, 1, 1], 1, True), ([1, 2, 3, 1, 2, 3], 2, False)]

    def test_contains_duplicate(self):
        for test_nums, k, result in self.data:
            self.assertEqual(result, contains_nearby_duplicate(test_nums, k))


if __name__ == '__main__':
    unittest.main()
