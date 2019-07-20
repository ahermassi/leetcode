""" You are given two arrays (without duplicates) nums1 and nums2 where nums1’s elements are subset of nums2. Find
all the next greater numbers for nums1's elements in the corresponding places of nums2.
Example:
Input: nums1 = [4,1,2], nums2 = [1,3,4,2].
Output: [-1,3,-1] """

import unittest2 as unittest


def next_greater_element(nums1, nums2):
    """ Brute force approach.
    Time complexity: O(N * M) where N is the length of nums1 and M is the length of nums2
    Space complexity: O(N)
    """
    res = []
    for i in nums1:
        next_greater = i
        for j in nums2[nums2.index(i):]:  # Look to the right of i
            if j > next_greater:
                next_greater = j
                break
        res.append(-1 if next_greater == i else next_greater)
    return res


class Test(unittest.TestCase):
    data = [([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]),
            ([2, 4], [1, 2, 3, 4], [3, -1])
            ]

    def test_move_zeroes(self):
        for nums1, nums2, result in self.data:
            self.assertEqual(result, next_greater_element(nums1, nums2))


if __name__ == '__main__':
    unittest.main()
