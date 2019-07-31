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


def intersect_v2(nums1, nums2):
    """ Follow up questions: What if the given array is already sorted? How would you optimize your algorithm?
        If both arrays are sorted, use two pointers to iterate.
    Time complexity: O(N) where N is the length of the shortest array
    Space complexity: O(1)
    """
    nums1, nums2 = sorted(nums1), sorted(nums2)
    p1, p2, res = 0, 0, []
    while p1 < len(nums1) and p2 < len(nums2):
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
        Suppose lengths of two arrays are N and M, the time complexity of the solution is O(N+M) and the space
        complexity is O(N) considering the hash. So it's better to use the smaller array to construct the counter hash.
    """
    pass

def intersect_v4(nums1, nums2):
    """ Follow up question: What if elements of nums2 are stored on disk, and the memory is limited such that you
        cannot load all elements into the memory at once?
        If the two arrays have relatively the same length, we can use external sort to sort out the two arrays in the
        disk. Then load chunks of each array into the memory and compare, by using the method 1.
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
