""" You are a professional robber planning to rob houses along a street. Each house has a certain amount of money
stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one.
Meanwhile, adjacent houses have security system connected and it will automatically contact the police if two adjacent
houses were broken into on the same night.
Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of
money you can rob tonight without alerting the police.
"""

import unittest2 as unittest


def rob_v1(nums):
    """ In the original question, 198- House Robber, whether to rob nums[0] is entirely our choice. But, it is now
        constrained by whether num[-1] is robbed. However, since we already have a nice solution to the simpler
        problem, we do not want to throw it away. Then, it becomes how can we reduce this problem to the simpler one.
        This problem can be simply decomposed into two House Robber problems.
        Suppose there are n houses. Since house 0 and n - 1 are now neighbors, we cannot rob them together, and thus
        the solution is now the maximum of:
            1- Rob houses 0 to n - 2
            2- Rob houses 1 to n - 1
        If we rob the first, then we cannot rob the last, so nums[:-1]
        If we do not rob the first, then we can rob the last, so nums[1:]
        You want the first, leave the last. You want the last, leave the first.
        Let us try to prove it. For nums[0..n-1], 0 and n-1 are neighboring each other. Basically, there are only three
        possible cases:
            1- Rob 0, but leave n-1 untouched
            2- Leave 0 untouched, rob n-1
            3- Leave both 0 and n-1 untouched. Obviously, this case can be covered by case 1 or case 2 in the simple
               House Robber problem.
        Hence, the above solution covers all the possible cases.

    """

    def helper(nums):
        if not nums:
            return 0
        n = len(nums)
        if n == 1:
            return nums[0]
        dp = [0] * n
        dp[0], dp[1] = nums[0], max(nums[0], nums[1])
        for i in range(2, n):
            dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])
        return dp[-1]

    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    return max(helper(nums[:-1]), helper(nums[1:]))


class Test(unittest.TestCase):
    data = [([2, 3, 2], 3), ([1, 2, 3, 1], 4)]

    def test_rob(self):
        for test_array, result in self.data:
            self.assertEqual(result, rob_v1(test_array))


if __name__ == '__main__':
    unittest.main()
