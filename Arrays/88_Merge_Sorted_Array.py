""" Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.
The number of elements initialized in nums1 and nums2 are m and n respectively.
Do not return anything, modify nums1 in-place instead.
"""

import unittest2 as unittest


def merge_v1(nums1, m, nums2, n):
    """ The simplest implementation would be to make a copy of the values in nums1, called nums1_copy, and then use two
         read pointers and one write pointer to read values from nums1_copy and nums2 and write them into nums1.

    Time complexity: O(n + m)
    Space complexity: O(m), for nums1_copy
    """
    nums1_copy = nums1[:m]
    i = j = write_index = 0
    while i < m and j < n:
        if nums1_copy[i] < nums2[j]:
            nums1[write_index] = nums1_copy[i]
            i += 1
        else:
            nums1[write_index] = nums2[j]
            j += 1
        write_index += 1
    nums1[write_index:] = nums1_copy[i:] if i < m else nums2[j:]


def merge_v2(nums1, m, nums2, n):
    """ We do have spare space at the end of the first array. We take advantage of this by filling the first array
        from its end. The last element in the result will be written to index (m + n - 1).
        For example, if A = [5, 13, 17, , , , , ], B = [3, 7, 11, 19], then A is updated in the following manner:
                                    ^        ^                     ^
                                    i       w_i                    j

        A = [5, 13, 17, , , , 19, ], B = [3, 7, 11, 19]
                    ^      ^                    ^
                    i      w_i                  j

        A = [5, 13, 17, , , 17, 19, ], B = [3, 7, 11, 19]
                ^        ^                        ^
                i       w_i                       j

        A = [5, 13, 17, , 13, 17, 19, ], B = [3, 7, 11, 19]
             ^         ^                            ^
             i        w_i                           j

        A = [5, 13, 17, 11, 13, 17, 19, ], B = [3, 7, 11, 19]
             ^      ^                              ^
             i     w_i                             j

        A = [5, 13, 7, 11, 13, 17, 19, ], B = [3, 7, 11, 19]
             ^  ^                              ^
             i w_i                             j

        A =    [5, 5, 7, 11, 13, 17, 19, ], B = [3, 7, 11, 19]
            ^   ^                                ^
           i<0 w_i                               j

        A = [3, 5, 7, 1, 13, 17, 19, ]
        Note that we will never overwrite an entry in the first array that has not already been processed. The reason
        is that even if every entry of the second array is larger than each element of the first array, all elements
        of the second array will fill up indices m to (m + n - 1) inclusive, which does not conflict with entries
        stored in the first array.
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
            merge_v1(test_array1, m, test_array2, n)
            self.assertEqual(result, test_array1)


if __name__ == '__main__':
    unittest.main()
