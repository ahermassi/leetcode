""" There are a row of n houses, each house can be painted with one of the three colors: red, blue or green. The cost
of painting each house with a certain color is different. You have to paint all the houses such that no two adjacent
houses have the same color.
The cost of painting each house with a certain color is represented by a n x 3 cost matrix. For example, costs[0][0]
is the cost of painting house 0 with color red; costs[1][2] is the cost of painting house 1 with color green, and so
on... Find the minimum cost to paint all houses.  """

import unittest2 as unittest


def min_cost_v1(costs):
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


class Test(unittest.TestCase):
    data = [([[17, 2, 17], [16, 16, 5], [14, 3, 19]], 10)]

    def test_min_cost(self):
        for test_costs, result in self.data:
            self.assertEqual(result, min_cost_v1(test_costs))


if __name__ == '__main__':
    unittest.main()
