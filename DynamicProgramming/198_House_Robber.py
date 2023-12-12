""" You are a professional robber planning to rob houses along a street. Each house has a certain amount of money
stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system
connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of
money you can rob tonight without alerting the police. """

# Refer to this link for more detailed explanation:
# https://leetcode.com/problems/house-robber/discuss/156523/From-good-to-great.-How-to-approach-most-of-DP-problems.

import unittest2 as unittest


def rob_v1(nums):
    """ A series of choices essentially gives us a subset of houses from the original list. We need to make these
         choices in such a way that the overall profit is maximized.

         There is no greedy way of deciding if the robber should rob a house or not. The best greedy strategy may be to
         check the neighboring houses and only rob a house if it gives them more money than the neighbors combined.
         That might be a sound greedy strategy. However, by doing so, the robber may miss out on making the maximum
         profit.

         What we need is to try all the possibilities and see which one gives the robber the optimal loot. We do this
         because there is no plausible greedy strategy that we can use to decide if the robber should rob a particular
         house or not.

         The basic choice that we make is whether to rob the current house or not. If the robber decides to rob the
         current house, they have to skip the previous house. Otherwise, they can evaluate the same choice on the next
         house i.e. to rob or not to rob.

         To approach a problem recursively, we need to make sure that it can be broken down into sub-problems.
         Additionally, we need to ensure that the optimal solution to these sub-problems can be used to form the
         solution to the main problem. Let's see how we can divide this problem into smaller recursive problems.

         Let's say that we have a function called rob_houses which we will use to solve this problem. The only input
         this function takes is an index, position. This position essentially represents a PREFIX in the array which the
         robber has scanned so far. Essentially, the position indicates that the robber has scanned houses
         [0...position-1].

        Naturally, the answer to our problem would be the function call rob_houses(N), where N represents the total
        number of houses, which means scan all the houses and return the maximum profit.

        Now let's think about rob_houses(i) for a moment. This simply represents a sub-array or a prefix from the main
        array. We can think about this as a smaller max-profit problem in itself, can't we?

        A prefix of the initial set of houses simply means a smaller set of houses that the robber has to consider. We
        will be working with the assumption that in the function call rob_houses(i), the robber has to maximize their
        profit from 0...i-1 houses.

        At each step, the robber has two options:

            1- Rob current house i: If this option is selected, it means the robber can't rob previous (i-1) house but
                 can safely proceed to the one before previous (i-2) and get all cumulative loot that follows.
            2- Don't rob current house i: If this option is selected, the robber gets all the possible loot from robbery
            of house (i-1) and all the following houses.

        So it boils down to calculating what is more profitable:

            1- Robbery of current house + loot from houses before the previous
            2- Loot from the previous house robbery and any loot captured after that

        Let's put this mathematically:

                    rob_houses(i) = max(rob_houses(i-2) + currentHouseValue, rob_houses(i-1))

    Time complexity: O(2^N)
    Space complexity: O(N)
    """
    # This solution TLEs.
    def rob_houses(i):
        if i < 0:
            return 0
        return max(nums[i] + rob_houses(i - 2), rob_houses(i - 1))

    return rob_houses(len(nums) - 1)


def rob_v2(nums):
    """ Top-Down Dynamic Programming

        If we visualize the recursion tree from the previous solution, we can see that we have repeating sub-problems,
        in which case we can use memoization or caching to reduce the overall solution complexity. We cache the already
        computed results so that we don't need to re-calculate the maximum profit for previously seen sub-problems.

    Time complexity: O(N), since we process at most N recursive calls thanks to caching, and during each of these calls,
    we make an O(1) computation which is simply making two other recursive calls, finding their maximum, and populating
     the cache based on that.
    Space complexity: O(N), which is occupied by the cache and also by the recursion stack
    """

    def rob_houses(i):
        if i < 0:
            return 0
        if i not in memo:
            memo[i] = max(nums[i] + rob_houses(i - 2), rob_houses(i - 1))
        return memo[i]

    memo = {}
    return rob_houses(len(nums) - 1)


def rob_v3(nums):
    """ Bottom-up Dynamic Programming.

        The idea here is the same as before except that instead of following a recursive approach, we will be sticking
        with a tabular approach. The recursive approach may run into trouble when the recursion stack grows too large.

        The cache we had before will still exist in this approach but instead of calling it a cache, we will refer to
        it as our dynamic programming table. Every DP solution has a table that we populate starting with the base case
        or the simplest of cases for which we already know the answer. E.g. for our problem, we know that in the absence
        of houses, the robber will make 0 profit. Similarly, if there is just one house left to rob, the robber will rob
        that house, and that will be the maximum profit.

        We start by populating the dynamic programming table with these initial values and then build the table in a
        bottom-up fashion which is the essence of this solution.

        Let dp[i] be the maximum profit that can be made from robbing houses up to index (i-1). Therefore:

                    dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])

        At every index:

            - We can keep same loot as we had at previous index: dp[i-1]. Or,
            - We can rob the current house and add it to the loot we have at (i-2)th index: nnums[i] + dp[i-2]

        Note that this is the same as the recursive formulation in the previous solution. The only difference is that we
        have already calculated the solutions to the sub-problems, and we simply reuse the solutions in O(1) time when
        calculating the solution to the main problem.

    Time complexity: O(N)
    Space complexity: O(N), which is used by the table. So what is the real advantage of this solution over the previous
    solution? In this case, we don't have a recursion stack. When the number of houses is large, a recursion stack can
    become a serious limitation, because the recursion stack size will be huge and the compiler will eventually run into
    stackoverflow problems.
    """
    n = len(nums)
    if n == 1:
        return nums[0]
    dp = [0] * n
    dp[0], dp[1] = nums[0], max(nums[0], nums[1])
    for i in range(2, n):
        dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])
    return dp[-1]


# Video explanation: https://youtu.be/73r3KWiEvyk
def rob_v4(nums):
    """ This is the exact same solution as the previous one with the exception that we will be optimizing the space
         complexity here.

         We notice that in the previous solution, in order to calculate the value at a current index in the dynamic
         programming table, we simply need to know the previous two values. So instead of keeping an entire table for
         storing these cached values, we can get by with simply keeping track of the "previous" two values.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    rob_previous = rob_before_previous = 0
    for i in range(n):
        cur_max_loot = max(nums[i] + rob_before_previous, rob_previous)
        rob_before_previous, rob_previous = rob_previous, cur_max_loot
    return rob_previous


class Test(unittest.TestCase):
    data = [([1, 2, 3, 1], 4),
            ([2, 7, 9, 3, 1], 12)]

    def test_rob(self):
        for test_array, result in self.data:
            self.assertEqual(result, rob_v1(test_array))
            self.assertEqual(result, rob_v2(test_array))
            self.assertEqual(result, rob_v3(test_array))
            self.assertEqual(result, rob_v4(test_array))


if __name__ == '__main__':
    unittest.main()
