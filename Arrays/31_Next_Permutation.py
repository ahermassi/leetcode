""" Implement next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers.
If such arrangement is not possible, it must rearrange it as the lowest possible order (ie, sorted in ascending order).
The replacement must be in-place and use only constant extra memory.
"""

import unittest2 as unittest


def next_permutation(nums):
    """ Refer to this article for an explanation:
        https://www.nayuki.io/page/next-lexicographical-permutation-algorithm
    Time complexity: O(N)
    Space complexity: O(1)
    """
    i = j = len(nums) - 1
    while i > 0 and nums[i - 1] >= nums[i]:
        i -= 1
    if i == 0:
        nums.reverse()
        return nums
    k = i - 1
    while nums[j] <= nums[k]:
        j -= 1
    nums[j], nums[k] = nums[k], nums[j]
    l, r = k + 1, len(nums) - 1
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1
        r -= 1
    return nums


class Test(unittest.TestCase):
    data = [([1, 2, 3], [1, 3, 2]),
            ([3, 2, 1], [1, 2, 3]),
            ([1, 1, 5], [1, 5, 1])]

    def test_next_permutation(self):
        for test_array, result in self.data:
            self.assertEqual(result, next_permutation(test_array))


if __name__ == '__main__':
    unittest.main()
