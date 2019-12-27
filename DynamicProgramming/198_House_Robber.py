""" You are a professional robber planning to rob houses along a street. Each house has a certain amount of money
stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system
connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of
money you can rob tonight without alerting the police. """

# Refer to this link for more detailed explanation:
# https://leetcode.com/problems/house-robber/discuss/156523/From-good-to-great.-How-to-approach-most-of-DP-problems.

import unittest2 as unittest


def rob_v1(nums):
    """ A robber has 2 options:
            1- rob current house i
            2- don't rob current house.
        If 1st option is selected, it means the robber can't rob previous (i-1) house but can safely proceed to the
        one before previous (i-2) and gets all cumulative loot that follows.
        If 2nd option is selected, the robber gets all the possible loot from robbery of (i-1) house and all the
        following buildings.
        So it boils down to calculating what is more profitable:
            1- Robbery of current house + loot from houses before the previous
            2- Loot from the previous house robbery and any loot captured after that
            rob(i) = max(rob(i-2) + currentHouseValue, rob(i-1))
    Time complexity: O(2^N)
    Space complexity: O(N)
    """
    # This solution TLEs.
    def helper(i):
        if i < 0:
            return 0
        return max(nums[i] + helper(i - 2), helper(i - 1))

    return helper(len(nums) - 1)


def rob_v2(nums):
    """ Recursion + memoization
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def helper(i):
        if i < 0:
            return 0
        if i in memo:
            return memo[i]
        res = max(nums[i] + helper(i - 2), helper(i - 1))
        memo[i] = res
        return res

    memo = {}
    return helper(len(nums) - 1)


# Bottom-up + 2 variables (constant space)


def rob_v3(nums):
    """
    Time complexity: O(N)
    Space complexity: O(1)
    """
    a = b = 0
    for i in range(len(nums)):
        a, b = b, max(nums[i] + a, b)
    return b

# To do: implement it recursively


class Test(unittest.TestCase):
    data = [([1, 2, 3, 1], 4),
            ([2, 7, 9, 3, 1], 12)]

    def test_rob(self):
        for test_array, result in self.data:
            self.assertEqual(result, rob_v1(test_array))
            self.assertEqual(result, rob_v2(test_array))


if __name__ == '__main__':
    unittest.main()
