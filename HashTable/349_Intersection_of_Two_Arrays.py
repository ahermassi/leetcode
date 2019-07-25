""" Given two arrays, write a function to compute their intersection. """
from collections import defaultdict

import unittest2 as unittest


def intersection_v1(nums1, nums2):
    """ Use a hash table to record all nums that appeared in the first list, and then check if there are nums in the
    second list have appeared in the hash table.
    Time complexity: O(N + M) where N is the length of nums1 and M is the length of nums2
    Space complexity: O(N + M)
    """
    count, result = defaultdict(int), []
    for i in nums1:
        if i not in count:  # Avoid duplicate numbers
            count[i] = 1
    for i in nums2:
        if count[i] == 1 and i not in result:  # If number exists in hash table and not in the result list
            result.append(i)
    return result


class Test(unittest.TestCase):
    data = [([1, 2, 2, 1], [2, 2], [2]),
            ([4, 9, 5], [9, 4, 9, 8, 4], [9, 4])
            ]

    def test_intersection(self):
        for nums1, nums2, result in self.data:
            self.assertEqual(result, intersection_v1(nums1, nums2))


if __name__ == '__main__':
    unittest.main()
