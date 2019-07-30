""" Given two arrays, write a function to compute their intersection.
Each element in the result should appear as many times as it shows in both arrays."""

import unittest2 as unittest


def intersect_v1(nums1, nums2):
    """ Use a hash table to record all nums that appeared in the first list, and then check if there are nums in the
    second list have appeared in the hash table.
    Time complexity: O(N + M) where N is the length of nums1 and M is the length of nums2
    Space complexity: O(N + M)
    """
    counts, res = {}, []
    for i in nums1:
        counts[i] = counts.get(i, 0) + 1
    for i in nums2:
        if i in counts and counts[i] > 0:
            res.append(i)
            counts[i] -= 1
    return res


class Test(unittest.TestCase):
    data = [([1, 2, 2, 1], [2, 2], [2, 2]),
            ([4, 9, 5], [9, 4, 9, 8, 4], [9, 4])
            ]

    def test_intersect(self):
        for nums1, nums2, result in self.data:
            self.assertEqual(result, intersect_v1(nums1, nums2))


if __name__ == '__main__':
    unittest.main()
