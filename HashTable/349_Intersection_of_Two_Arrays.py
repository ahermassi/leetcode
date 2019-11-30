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
