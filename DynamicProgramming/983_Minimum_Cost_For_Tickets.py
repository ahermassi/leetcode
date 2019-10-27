""" Read description on Leetcode """

import unittest2 as unittest


def min_cost_tickets_v1(days, costs):
    """ For each travel day, we can buy a one-day ticket, or use 7-day or 30-day pass as if we would have purchased it
        7 or 30 days ago. We need to track rolling costs for at least 30 days back, and use them to pick the cheapest
        option for the next travel day.
        We track the minimum cost for all calendar days in dp.
        Let dp[i] == minimum cost for i days of travel. Hence, dp[max(days)] is what we're looking for.
        For non-travel days, the cost stays the same as for the previous day. For travel days, it's a minimum of
        yesterday's cost plus one single-day ticket, or cost for 7 days ago plus one 7-day pass, or cost  of 30 days
        ago plus  one 30-day pass:
        dp[i] = min(dp[i-1] + costs[0], dp[i-7] + costs[1], dp[i-30] + costs[2])
    Time complexity: O(W), where W = 365 is the maximum numbered day in the travel plan
    Space complexity: O(W)
    """
    dp = [0 for _ in range(days[-1] + 1)]
    days = set(days)  # Faster lookup of days
    for i in range(1, len(dp)):
        if i in days:
            dp[i] = min(dp[i - 1] + costs[0], dp[max(0, i - 7)] + costs[1], dp[max(0, i - 30)] + costs[2])  # Note how
            # max() is used to deal with edge cases of (i < 7) and (i < 30)
        else:  # If the current day is a non-travel day, we're not spending any extra money
            dp[i] = dp[i - 1]
    return dp[-1]


class Test(unittest.TestCase):
    data = [([1, 4, 6, 7, 8, 20], [2, 7, 15], 11), ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15], 17)]

    def test_min_cost_tickets(self):
        for test_days, test_costs, result in self.data:
            self.assertEqual(result, min_cost_tickets_v1(test_days, test_costs))


if __name__ == '__main__':
    unittest.main()
