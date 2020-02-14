""" Given two arrays, write a function to compute their intersection. """

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
    """ Sort the two arrays, and then exploit this fact.
        Simultaneously advance through the two input arrays in increasing order. At each iteration, if the array
        elements differ, the smaller one can be eliminated. If they are equal, we add that value to the intersection
        and advance both. We handle duplicates by comparing the current element with the next one.
    Time complexity: O(N logN), where N is the length of the longest array
    Space complexity: O(N + M) for Timsort. If the sorting algorithm was in-place, the space complexity would be O(1).
    """
    n, m = len(nums1), len(nums2)
    nums1.sort()
    nums2.sort()
    i, j, res = 0, 0, []
    while i < n and j < m:
        if nums1[i] == nums2[j]:
            res.append(nums1[i])
            while i < n - 1 and nums1[i] == nums1[i + 1]:
                i += 1
            while j < m - 1 and nums2[j] == nums2[j + 1]:
                j += 1
            i += 1
            j += 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1
    return res


def intersection_v4(nums1, nums2):
    """ Slightly modified version of the previous algorithm. The difference is how duplicates are handled.
         For example, if the arrays are A = [2, 3, 3, 5, 7, 11] and B = [3, 3, 7, 15, 31], then we know by inspecting
         the first element of each that 2 cannot belong to the intersection, so we advance to the second element of A.
         Now we have a common element, 3, which we add to the result, and then we advance in both arrays. Now we are at
         3 in both arrays, but we know 3 has already been added to the result since the previous element in A is also 3.
         We advance in both again without adding to the intersection. Comparing 5 to7, we can eliminate 5 and advance
        to the fourth element in A, which is 7, and equal to the element that B's iterator holds, so it is added to the
        result. We then eliminate 11, and since no elements remain in A, we return [3, 7].
    Time complexity: O(N logN), where N is the length of the longest array
    Space complexity: O(N + M) for Timsort
    """
    nums1.sort()
    nums2.sort()
    n, m, res = len(nums1), len(nums2), []
    i = j = 0
    while i < n and j < m:
        if nums1[i] == nums2[j]:
            if i == 0 or nums1[i] != nums1[i - 1]:
                res.append(nums1[i])
            i += 1
            j += 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1
    return res


class Test(unittest.TestCase):
    data = [([1, 2, 2, 1], [2, 2], [2]),
            ([4, 9, 5], [9, 4, 9, 8, 4], [9, 4])
            ]

    def test_intersection(self):
        for nums1, nums2, result in self.data:
            self.assertEqual(result, intersection_v1(nums1, nums2))
            self.assertEqual(result, intersection_v2(nums1, nums2))


if __name__ == '__main__':
    unittest.main()
