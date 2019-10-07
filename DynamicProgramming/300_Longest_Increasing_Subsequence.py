""" Given an unsorted array of integers, find the length of longest increasing subsequence. """

import unittest as unittest


def length_of_LIS_v1(nums):
    """ We use dp array to store our sub problems, default answer is 1. A single item is neither increasing or
        decreasing. Each index i holds the answer to "what is the longest increasing sub sequence ending at index i of
        the original nums array ?". Test every possible end index of a longest increasing sub sequence
    Time complexity: O(N ** 2)
    Space complexity: O(N)
    """
    if not nums:
        return 0
    dp = [1] * len(nums)
    max_len = 1
    for i in range(1, len(nums)):
        # We aim to see if we can append the item at nums[i] to extend the Longest Increasing Subsequence achieved
        # from index 0...j. We want to solve for dp[i] if the value at i is greater than the value at j
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)  # The value of dp[j] is the length of the LIS from 0...j, we conceptually
                # "append" this item to that LIS by adding 1 to that sub problem answer, yielding a otentially new
                # answer for LIS[0..i]
        max_len = max(max_len, dp[i])
    return max_len


def length_of_LIS_v2(nums):
    """ For an explanation:
        https://leetcode.com/problems/longest-increasing-subsequence/discuss/74824/JavaPython-Binary-search-O(nlogn)-time-with-explanation
    Time complexity: O(N logN), binary search takes logN time and it is called N times
    Space complexity: O(N)
    """
    increasing_subsequence = [0] * len(nums)
    size = 0
    for x in nums:
        left, right = 0, size
        while left != right:
            mid = (left + right) // 2
            if increasing_subsequence[mid] < x:
                left = mid + 1
            else:
                right = mid
        increasing_subsequence[left] = x
        size = max(left + 1, size)
    return size


class Test(unittest.TestCase):
    data = [([10, 9, 2, 5, 3, 7, 101, 18], 4)]

    def test_length_of_LIS(self):
        for test_array, result in self.data:
            self.assertEqual(result, length_of_LIS_v1(test_array))
            self.assertEqual(result, length_of_LIS_v2(test_array))


if __name__ == '__main__':
    unittest.main()
