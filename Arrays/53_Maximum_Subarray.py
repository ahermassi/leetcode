""" Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest
sum and return its sum. """

import unittest2 as unittest


def maximum_subarray_v1(nums):
    """ This is called Kadane's algorithm. Assume first element is the maximum (local and global) sum. Iterate over the
        array, and at each step ask yourself: which is greater, the current element x or (last sum + x) ? Update the
        local sum and global sum accordingly.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_so_far = max_ending_here = nums[0]
    for i in range(1, len(nums)):
        max_ending_here = max(nums[i], max_ending_here + nums[i])  # What's the maximum sub array ending here ? Either
        # [current element] or [previous sub array, current]
        max_so_far = max(max_so_far, max_ending_here)  # Update global max
    return max_so_far


def maximum_subarray_v2(nums):
    """ This is an optimization problem, which can be usually solved using DP. So when it comes to DP, the first thing
        for us to figure out is the format of the sub problem (or the state of each sub problem).
        The format of the sub problem is something like: maxSubArray(int A[], int i), which means the maxSubArray for
        A[0:i] which must has A[i] as the end element. Now the connection between the sub problem and the original one
        becomes clear. Let dp[i] be the maximum sum of a contiguous sub array ending at index i:
            dp[i] = max(nums[i], dp[i - 1] + nums[i])
        If the maximum sum of a contiguous sub array up to index (i-1) is positive, it is possible to make the maximum
        sum value bigger, so we add the current element to the sum.
        If the maximum sum is negative, we start over with the current element.
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
