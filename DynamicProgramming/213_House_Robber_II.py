""" You are a professional robber planning to rob houses along a street. Each house has a certain amount of money
stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one.
Meanwhile, adjacent houses have security system connected and it will automatically contact the police if two adjacent
houses were broken into on the same night.
Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of
money you can rob tonight without alerting the police.
"""

import unittest2 as unittest


# Video explanation: https://youtu.be/rWAJCfYYOvM
def rob_v1(nums):
    """ This problem is a minor extension to the original 198- House Robber Problem. The only difference is that the
         first and the last houses are adjacent to each other and therefore, if the thief has robbed the first house,
         they cannot steal the last house and vice versa.

         Therefore, the problem becomes to rob either nums[0]...nums[n-2] or nums[1]...nums[n-1], depending on which
         choice offers more money. Now the problem has degenerated to the original house robber.

         Assume we have nums = [7,4,1,9,3,8,6,5].
         Since the start house and last house are adjacent to each other, if the thief decides to rob the start house 7,
         they cannot rob the last house 5. Similarly, if they select last house 5, they have to start from a house with
         value 4. Therefore, the final solution that we are looking for is to take the maximum value the thief can rob
         between houses of list [7,4,1,9,3,8,6] and [4,1,9,3,8,6,5]. For each of the lists, all we need to do is to
         figure out the maximum value the thief can get using the approach in the original house robber problem.

        Suppose there are n houses. Since house 0 and n - 1 are now neighbors, we cannot rob them together, and thus
        the solution is now the maximum of:

            1- Rob houses 0 to n - 2
            2- Rob houses 1 to n - 1

        You want the first, leave the last. You want the last, leave the first.

        Let us try to prove it. For nums[0...n-1], 0 and n-1 are neighboring each other. Basically, there are only three
        possible cases:

            1- Rob 0, but leave n-1 untouched
            2- Leave 0 untouched, rob n-1
            3- Leave both 0 and n-1 untouched. Obviously, this case can be covered by case 1 or case 2 in the original
               House Robber problem.

        Hence, this solution covers all the possible cases.

    Time complexity: O(N)
    Space complexity: O(N)
    """

    def rob_houses(houses):
        if not houses:
            return 0
        n = len(houses)
        if n == 1:
            return houses[0]
        dp = [0] * n
        dp[0], dp[1] = houses[0], max(houses[0], houses[1])
        for i in range(2, n):
            dp[i] = max(houses[i] + dp[i - 2], dp[i - 1])
        return dp[-1]

    if len(nums) == 1:
        return nums[0]
    return max(rob_houses(nums[1:]), rob_houses(nums[:-1]))


def rob_v2(nums):
    """ Space optimised version of the previous solution.
    Time complexity: O(N)
    Space complexity: O(1)
    """

    def helper(left, right):
        a = b = 0
        for i in range(left, right + 1):
            a, b = b, max(nums[i] + a, b)
        return b

    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    n = len(nums)
    return max(helper(0, n - 2), helper(1, n - 1))  # Pass left and right boundaries as parameters


class Test(unittest.TestCase):
    data = [([2, 3, 2], 3), ([1, 2, 3, 1], 4)]

    def test_rob(self):
        for test_array, result in self.data:
            self.assertEqual(result, rob_v1(test_array))
            self.assertEqual(result, rob_v2(test_array))


if __name__ == '__main__':
    unittest.main()
