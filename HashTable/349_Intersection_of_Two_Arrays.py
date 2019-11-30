""" Given two arrays, write a function to compute their intersection. """

from collections import defaultdict
import unittest2 as unittest


def intersection_v1(nums1, nums2):
    """ Create a set out of one of the arrays, and then iterate over the other array and check if each element appears
        in the set. Append common elements to a set to avoid redundancy.
    Time complexity: O(N + M)
    Space complexity: O(N + M)
    """
    res, nums1 = set(), set(nums1)
    for num in nums2:
        if num in nums1:
            res.add(num)
    return list(res)


def intersection_v2(nums1, nums2):
    """ Same as previous solution, but instead of appending common elements to a set to avoid redundancy, append them
        to the final result list instead and remove that element from the nums set.
    Time complexity: O(N + M) where N is the length of nums1 and M is the length of nums2
    Space complexity: O(N + M)
    """
    res, nums1 = [], set(nums1)
    for num in nums2:
        if num in nums1:
            res.append(num)
            nums1.remove(num)
    return res


def intersection_v3(nums1, nums2):
    """ The idea is to convert both arrays into sets, and then iterate over the smallest set checking the presence of
    each element in the larger set.
    Time complexity: O(N + M)
    Space complexity: O(N + M)
    """

    def set_intersection(set1, set2):
        return [x for x in set1 if x in set2]

    set1 = set(nums1)
    set2 = set(nums2)
    if len(set1) < len(set2):
        return set_intersection(set1, set2)
    return set_intersection(set2, set1)


class Test(unittest.TestCase):
    data = [([1, 2, 2, 1], [2, 2], [2]),
            ([4, 9, 5], [9, 4, 9, 8, 4], [9, 4])
            ]

    def test_intersection(self):
        for nums1, nums2, result in self.data:
            self.assertEqual(result, intersection_v1(nums1, nums2))
            self.assertEqual(result, intersection_v2(nums1, nums2))
            self.assertEqual(result, intersection_v3(nums1, nums2))


if __name__ == '__main__':
    unittest.main()
