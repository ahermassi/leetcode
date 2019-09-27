""" Given an array with n objects colored red, white or blue, sort them in-place so that objects of the same color
are adjacent, with the colors in the order red, white and blue.
Here, we will use the integers 0, 1, and 2 to represent the color red, white, and blue respectively. """

from collections import defaultdict

import unittest2 as unittest


def sort_colors_v1(nums):
    """ A rather straight forward solution is a two-pass algorithm using counting sort.
        First, iterate the array counting number of 0's, 1's, and 2's, then overwrite array with total number of 0's,
        then 1's and followed by 2's.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    d = defaultdict(int)
    for num in nums:
        d[num] += 1
    nums[:] = [0] * d[0] + [1] * d[1] + [2] * d[2]


def sort_colors_v2(nums):
    """ Let's use here three pointers to track the rightmost boundary of zeros, the leftmost boundary of twos and the
        current element under the consideration.
        The idea of solution is to move curr pointer along the array, if nums[curr] = 0 - swap it with nums[p0], if
        nums[curr] = 2 - swap it with nums[p2].
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, curr, right = 0, 0, len(nums) - 1
    # For all idx < left : nums[idx] == 0
    # For all idx > right : nums[idx] == 2
    # curr is an index of element under consideration
    while curr <= right:
        num = nums[curr]
        if num == 0:
            nums[left], nums[curr] = nums[curr], nums[left]
            left += 1  # Move both pointers to the right
            curr += 1
        elif num == 1:
            curr += 1
        else:
            nums[right], nums[curr] = nums[curr], nums[right]
            right -= 1


class Test(unittest.TestCase):
    data = [([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2])]

    def test_sort_colors(self):
        for test_array, result in self.data:
            sort_colors_v1(test_array)
            self.assertEqual(result, test_array)


if __name__ == '__main__':
    unittest.main()
