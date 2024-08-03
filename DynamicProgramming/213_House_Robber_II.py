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

         Therefore, the problem becomes to rob either [nums[0]...nums[n-2]] or [nums[1]...nums[n-1]], depending on which
         choice offers more money. Now the problem has degenerated to the original house robber.

         Assume we have nums = [7,4,1,9,3,8,6,5].
         Since the start house and last house are adjacent to each other, if the thief decides to rob the start house 7,
         they cannot rob the last house 5. Similarly, if they select last house 5, they have to start from a house with
         value 4. Therefore, the final solution that we are looking for is to take the maximum value the thief can rob
         between houses of list [7,4,1,9,3,8,6] and [4,1,9,3,8,6,5]. For each of the lists, all we need to do is to
         figure out the maximum value the thief can get using the approach in the original house robber problem.

        Suppose there are n houses. Since houses 0 and n-1 are now neighbors, we cannot rob them together, and thus
        the solution is now the maximum of:

            1- Rob houses 0 to n-2
            2- Rob houses 1 to n-1

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
    """ Space optimized version of the previous solution.

        Imagine two thieves, t1 and t2, coordinating a grand robbery. They are equipped with walkie-talkies to
        communicate the values of houses to each other.

        Before entering any of the houses, both t1 and t2 have values of zero.

        t1 enters the first house and records the value of the house.
        If that is the only house to rob, they can rob this house and be done with it.
        If there is more than one house, t1 will leave a note of maximum value reaped until this point (which is just
        the value of the first house) and move to the next house while t2 moves into the house t1 was in.

        Now, t1 and t2 are going to communicate over the walkie-talkie to ask who has the most value. At this point,
        t2 will read the note left by t1 when the values are compared. If they have only two houses to rob, they would
        rob the one with the most value and be done with it.

        If there are three houses, t1 will leave a note of the maximum value reaped until this point and move to the
        next house. Then t1 will compare the value of the sum of the current house and the house which t2 is in with the
        value of the house t1 was in. The maximum value between those two will be chosen and t2 will move into the house
        next to it.

        If there are four houses, t1 will leave a note of the maximum value reaped until this point and move to the next
        house. Then t1 will compare the value of the sum of the current house and the house which t2 is in with the
        value of the house t1 was in. The maximum value between those two will be chosen and t2 will move into the house
        next to it.

        This procedure is done over and over again as long as there are houses left. If t1 has reached the last house,
        t1 should have reaped the maximum amount obtainable from all the houses.

    Time complexity: O(N)
    Space complexity: O(1)
    """

    def rob_houses(left, right):
        rob_previous = rob_before_previous = 0
        for i in range(left, right+1):
            cur_max_loot = max(nums[i] + rob_before_previous, rob_previous)
            rob_before_previous, rob_previous = rob_previous, cur_max_loot
        return rob_previous

    n = len(nums)
    if n == 1:
        return nums[0]
    return max(rob_houses(0, n-2), rob_houses(1, n-1))  # Pass left and right boundaries as parameters


class Test(unittest.TestCase):
    data = [([2, 3, 2], 3), ([1, 2, 3, 1], 4)]

    def test_rob(self):
        for test_array, result in self.data:
            self.assertEqual(result, rob_v1(test_array))
            self.assertEqual(result, rob_v2(test_array))


if __name__ == '__main__':
    unittest.main()
