""" You are a professional robber planning to rob houses along a street. Each house has a certain amount of money
stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system
connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of
money you can rob tonight without alerting the police. """

# Refer to this link for more detailed explanation:
# https://leetcode.com/problems/house-robber/discuss/156523/From-good-to-great.-How-to-approach-most-of-DP-problems.

import unittest2 as unittest


def rob_v1(nums):
    """ A robber has 2 options: a) rob current house i; b) don't rob current house.
    If an option "a" is selected it means she can't rob previous i-1 house but can safely proceed to the one before
    previous i-2 and gets all cumulative loot that follows.
    If an option "b" is selected the robber gets all the possible loot from robbery of i-1 and all the following
    buildings.
    So it boils down to calculating what is more profitable:
        * robbery of current house + loot from houses before the previous
        * loot from the previous house robbery and any loot captured before that
    rob(i) = Math.max( rob(i - 2) + currentHouseValue, rob(i - 1) )
    Time complexity: O(N)
    Space complexity: O(N)
    """
    # Bottom-up + memoization
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    dp = [None] * len(nums)
    dp[0], dp[1] = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])
    return dp[-1]


class Test(unittest.TestCase):
    data = [([1, 2, 3, 1], 4),
            ([2, 7, 9, 3, 1], 12)]

    def test_rob(self):
        for test_array, result in self.data:
            self.assertEqual(result, rob_v1(test_array))


if __name__ == '__main__':
    unittest.main()
