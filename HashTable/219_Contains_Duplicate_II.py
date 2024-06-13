""" Given an integer array nums and an integer k, return true if there are two distinct indices i and j in the array
such that nums[i] == nums[j] and abs(i - j) <= k.
 """

from collections import defaultdict
import unittest2 as unittest


def contains_nearby_duplicate_v1(nums, k):
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


def contains_nearby_duplicate_v2(nums, k):
    """ Keep a sliding window of k elements using hash set. This is a space-optimized approach using a fixed-size set
         with a least-recently used (LRU) eviction policy.

        Loop through the array, and for each element:

            - Search the current element in hash set, and return true if found

            - Otherwise, put the current element in the hash set.

            - If the size of the hash set is larger than k, remove the oldest item.

    Time complexity: O(N), where N is the length of array
    Space complexity: O(min(N, k))
    """
    seen = set()
    for i, num in enumerate(nums):
        if num in seen:
            return True
        seen.add(num)
        if i >= k:
            #  When len(seen) > k, we need to slide the window to the right, and thus we need to remove the first
            #  element of the window.
            seen.remove(nums[i - k])
    return False


class Test(unittest.TestCase):
    data = [([1, 2, 3, 1], 3, True), ([1, 0, 1, 1], 1, True), ([1, 2, 3, 1, 2, 3], 2, False)]

    def test_contains_duplicate(self):
        for test_nums, k, result in self.data:
            self.assertEqual(result, contains_nearby_duplicate_v1(test_nums, k))
            self.assertEqual(result, contains_nearby_duplicate_v2(test_nums, k))


if __name__ == '__main__':
    unittest.main()
