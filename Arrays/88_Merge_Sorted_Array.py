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
    i = j = write_index = 0
    while i < m and j < n:
        if nums1_copy[i] <= nums2[j]:
            nums1[write_index] = nums1_copy[i]
            i += 1
        else:
            nums1[write_index] = nums2[j]
            j += 1
        write_index += 1
    if i < m:
        nums1[write_index:] = nums1_copy[i:]
    elif j < n:
        nums1[write_index:] = nums2[j:]


def merge_v2(nums1, m, nums2, n):
    """ If we start to overwrite nums1 from the end, where there is no information yet, then no additional space
        is needed.
    Time complexity: O(n + m)
    Space complexity: O(1)
    """
    write_index = m + n - 1  # This is the first slot where a new element can be moved
    i, j = m - 1, n - 1
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:  # If the last non-zero in nums1 is > last non-zero in nums2
            nums1[write_index] = nums1[i]  # Move that last non-zero of nums1 to the write_index
            i -= 1
        else:
            nums1[write_index] = nums2[j]
            j -= 1
        write_index -= 1
    if j >= 0:  # There are more elements in nums2 to copy. Take the edge case of all nums2 elements are smaller than
        # nums1 elements
        nums1[:j + 1] = nums2[:j + 1]


class Test(unittest.TestCase):
    data = [([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6])]

    def test_merge(self):
        for test_array1, m, test_array2, n, result in self.data:
            merge_v2(test_array1, m, test_array2, n)
            self.assertEqual(result, test_array1)


if __name__ == '__main__':
    unittest.main()
