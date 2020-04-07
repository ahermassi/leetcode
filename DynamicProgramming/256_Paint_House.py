""" There are a row of n houses, each house can be painted with one of the three colors: red, blue or green. The cost
of painting each house with a certain color is different. You have to paint all the houses such that no two adjacent
houses have the same color.
The cost of painting each house with a certain color is represented by a n x 3 cost matrix. For example, costs[0][0]
is the cost of painting house 0 with color red; costs[1][2] is the cost of painting house 1 with color green, and so
on... Find the minimum cost to paint all houses.  """

import unittest2 as unittest


def min_cost_v1(costs):
    """ Let dp[i][j] be the minimum cost of painting houses from [0, i] if we paint ith house with color j. Because j
        can only be 3 colors - 0, 1, 2, if j = 0:
            dp[i][0] = min(the min cost of painting (i-1)th house with either blue or green) + costs[i][0]
                     = min(dp[i-1][1], dp[i-1][2]) + costs[i][0]
        The basic idea is when we have painted the first (i - 1) houses, and want to paint the ith house, we have 3
        choices: paint it either red, green, or blue.
        If we choose to paint it red, we have the follow the deduction:
            paint_current_red = min(paint_previous_green, paint_previous_blue) + costs[i][0]
        Which translates to:
            dp[i][0] = min(dp[i-1][1], dp[i-1][2]) + costs[i][0]
        Same for the green and the blue.
    Time complexity: O(N)
    Space complexity: O(N * 3) = O(N)
    """
    if not costs:
        return 0
    n = len(costs)
    dp = [[float('inf')] * 3 for _ in range(n)]
    dp[0] = costs[0]
    for i in range(1, n):
        dp[i][0] = min(dp[i-1][1], dp[i-1][2]) + costs[i][0]
        dp[i][1] = min(dp[i-1][0], dp[i-1][2]) + costs[i][1]
        dp[i][2] = min(dp[i-1][0], dp[i-1][1]) + costs[i][2]
        # Equivalent to:
        # for j in range(3):
        #     dp[i][j] = costs[i][j] + min(dp[i - 1][k] for k in range(3) if k != j)
    return min(dp[-1])


def min_cost_v2(costs):
    """ We don't know whether the current choice is optimal for next stage or not (the difference with greedy
    problem)? Thus, we delay the decision to make choice for current step at the next step. The trick in this
    problem is that we could not make the stage 1's choice based on current information, since it would affect our
    available choices at stage 2. At current stage, we should only prepare the right information for next stage to
    directly use, and let the next stage to make choice for the current stage.
    Assume at stage i:
    min_red[i] : the minimum cost to paint houses if we had only i houses and if house i was painted with red color.
    min_blue[i] : the minimum cost to paint houses if we had only i houses and if house i was painted with blue color.
    min_green[i] : the minimum cost to paint houses if we had only i houses and if house i was painted with green color.
    Transitional function.
    min_red[i] = Math.min(min_blue[i-1], min_green[i-1]) + red_cost[i]
    We actually made the decision for the previous stage at here. (if i house was painted as red).

    Time complexity: O(N) where N is the length of costs array
    Space complexity: O(1)
    """

    if not costs:
        return 0
    min_red, min_blue, min_green = costs[0][0], costs[0][1], costs[0][2]
    for i in range(1, len(costs)):
        cost = costs[i]
        temp_red, temp_blue, temp_green = min_red, min_blue, min_green
        min_red = min(temp_blue, temp_green) + cost[0]
        min_blue = min(temp_red, temp_green) + cost[1]
        min_green = min(temp_red, temp_blue) + cost[2]
    return min(min_red, min_blue, min_green)


def min_cost_v2(costs):
    """ Same idea as above but slightly different implementation that alters the input array.
    Time complexity: O(N) where N is the length of costs array
    Space complexity: O(1)
    """
    if not costs:
        return 0
    for i in range(1, len(costs)):
        cost, prev = costs[i], costs[i - 1]
        cost[0] += min(prev[1], prev[2])
        cost[1] += min(prev[0], prev[2])
        cost[2] += min(prev[0], prev[1])
    return min(costs[-1])


class Test(unittest.TestCase):
    data = [([[17, 2, 17], [16, 16, 5], [14, 3, 19]], 10)]

    def test_min_cost(self):
        for test_costs, result in self.data:
            self.assertEqual(result, min_cost_v1(test_costs))


if __name__ == '__main__':
    unittest.main()
