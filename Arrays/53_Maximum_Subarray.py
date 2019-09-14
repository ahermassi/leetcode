""" Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest
sum and return its sum. """

import unittest2 as unittest


def maximum_subarray_v1(nums):
    """
    This algorithm is called Kadane's algorithm. Assume first element is the maximum (local and global) sum. Iterate
    over the array, and at each step ask yourself: which is greater, the current element x or (last sum + x) ? Update
    the local sum and global sum accordingly.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    curr_sum = max_sum = nums[0]
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])  # What's the maximum subarray ending here ? Either [current
        # element] or [previous subarray, current]
        max_sum = max(max_sum, curr_sum)  # Update global max
    return max_sum


def maximum_subarray_v2(nums):
    """ Let's do it the DP way. dp[i] represents the maximum sum of a contiguous subarray ending/starting at index i.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    dp = [0] * len(nums)
    dp[0] = nums[0]
    for i in range(1, len(nums)):
        dp[i] = max(nums[i], dp[i - 1] + nums[i])
    return max(dp)


class Test(unittest.TestCase):
    data = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([0, -1, 5], 5)
    ]

    def test_two_sum(self):
        for test_array, result in self.data:
            self.assertEqual(result, maximum_subarray_v1(test_array))
            self.assertEqual(result, maximum_subarray_v2(test_array))


if __name__ == '__main__':
    unittest.main()
