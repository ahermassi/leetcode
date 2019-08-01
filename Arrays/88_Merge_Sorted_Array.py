""" Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.
The number of elements initialized in nums1 and nums2 are m and n respectively.
Do not return anything, modify nums1 in-place instead.
"""

import unittest2 as unittest


def merge_v1(nums1, m, nums2, n):
    """ The straightforward implementation would be to set pointer p1 in the beginning of nums1, p2 in the beginning
        of nums2, and push the smallest value in the output array at each step.
        Since nums1 is an array used for output, keep first m elements of nums1 somewhere aside.
    Time complexity: O(n + m)
    Space complexity: O(m) for nums1_copy
    """
    nums1_copy = nums1[:m]
    nums1[:] = []
    i = j = 0
    while i < m and j < n:
        if nums1_copy[i] < nums2[j]:
            nums1.append(nums1_copy[i])
            i += 1
        else:
            nums1.append(nums2[j])
            j += 1
    # If there are still elements to add
    if i < m:
        nums1[i + j:] = nums1_copy[i:]
    if j < n:
        nums1[i + j:] = nums2[j:]


class Test(unittest.TestCase):
    data = [([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6])]

    def test_merge(self):
        for test_array1, m, test_array2, n, result in self.data:
            merge_v1(test_array1, m, test_array2, n)
            self.assertEqual(result, test_array1)


if __name__ == '__main__':
    unittest.main()
