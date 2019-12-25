""" Given two arrays, write a function to compute their intersection.
Each element in the result should appear as many times as it shows in both arrays."""

from collections import Counter
import unittest2 as unittest


def intersect_v1(nums1, nums2):
    """ We collect numbers and their counts from one of the arrays into a hash map. Then, we iterate along the second
        array, and check if the number exists in the hash map and its count is positive. If so, add the number to the
        result and decrease its count in the hash map.
        It's a good idea to check array sizes and use a hash map for the smaller array. It will reduce memory usage
        when one of the arrays is very large.
        Note: why decrease the count ?
        Example: nums1 = [1, 2, 2, 1], nums2 = [2, 2, 2], counter = {1: 2, 2: 2}
        While looping over nums2, we decrease the count by 1 whenever an intersection happens and stop considering it
        for intersection if the count reaches 0. If that is not done, then in the above case result would be [2, 2, 2]
        instead of [2, 2].
    Time complexity: O(N + M), where N is the length of nums1 and M is the length of nums2
    Space complexity: O(min(N, M))), we use hash map to store numbers (and their counts) from the smaller array
    """
    if len(nums2) < len(nums1):  # If nums1 is larger than nums2, swap the arrays
        return intersect_v1(nums2, nums1)
    counter, res = Counter(nums1), []
    for num in nums2:
        if num in counter and counter[num] > 0:
            res.append(num)
            counter[num] -= 1
    return res


def intersect_v2(nums1, nums2):
    """ Follow up questions: What if the given array is already sorted? How would you optimize your algorithm?
        If both arrays are sorted, we use two pointers to find common numbers in a single scan.
        Initialize i and j with zero. Move indices i along nums1, and j through nums2.
        Increment i if nums1[i] is smaller. Increment j if nums2[j] is smaller. If numbers are the same, copy the
        number into res and increment i and j.
    Time complexity: O(N) where N is the length of the shortest array
    Space complexity: O(1)
    """
    nums1, nums2 = sorted(nums1), sorted(nums2)
    n, m = len(nums1), len(nums2)
    p1, p2, res = 0, 0, []
    while p1 < n and p2 < m:
        if nums1[p1] == nums2[p2]:
            res.append(nums1[p1])
            p1 += 1
            p2 += 1
        elif nums1[p1] < nums2[p2]:
            p1 += 1
        else:
            p2 += 1
    return res


def intersect_v3(nums1, nums2):
    """ Follow up question:  What if nums1's size is small compared to nums2's size? Which algorithm is better?
        Solution 1 is a good choice here as we use a hash map for the smaller array.
    """
    pass


def intersect_v4(nums1, nums2):
    """ Follow up question: What if elements of nums2 are stored on disk, and the memory is limited such that you
        cannot load all elements into the memory at once?
        If nums1 fits into the memory, we can use solution 1 to collect counts for nums1 into a hash map. Then, we can
        sequentially load and process nums2.
        If neither of the arrays fits into the memory, sort them using external sort, read (let's say) 2G of each into
        memory, and then use the 2 pointer technique, then read 2G more from the array that has been exhausted. Repeat
        this until there is no more data to read from disk.
        External sorting is a class of sorting algorithms that can handle massive amounts of data. External sorting is
        required when the data being sorted does not fit into the main memory of a computing device and instead it must
        reside in the slower external memory, usually a hard disk drive.
    """


class Test(unittest.TestCase):
    data = [([1, 2, 2, 1], [2, 2], [2, 2]),
            ([4, 9, 5], [9, 4, 9, 8, 4], [9, 4])
            ]

    def test_intersect(self):
        for nums1, nums2, result in self.data:
            self.assertEqual(result, intersect_v1(nums1, nums2))


if __name__ == '__main__':
    unittest.main()
