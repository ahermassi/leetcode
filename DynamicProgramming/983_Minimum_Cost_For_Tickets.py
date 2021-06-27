""" You have planned some train traveling one year in advance. The days of the year in which you will travel are given
as an integer array days. Each day is an integer from 1 to 365.

Train tickets are sold in three different ways:

a 1-day pass is sold for costs[0] dollars,
a 7-day pass is sold for costs[1] dollars, and
a 30-day pass is sold for costs[2] dollars.
The passes allow that many days of consecutive travel.

For example, if we get a 7-day pass on day 2, then we can travel for 7 days: 2, 3, 4, 5, 6, 7, and 8.
Return the minimum number of dollars you need to travel every day in the given list of days. """

from collections import deque
import unittest2 as unittest


def min_cost_tickets_v1(days, costs):
    """ For each travel day, we can buy a one-day ticket, or use 7-day or 30-day pass as if we would have purchased it
        7 or 30 days ago. We need to track rolling costs for at least 30 days back, and use them to pick the cheapest
        option for the next travel day.
        We track the minimum cost for all calendar days in dp array.
        Let dp[i] be minimum cost for i days of travel. Hence, dp[max(days)] is what we're looking for.
        For non-travel days, the cost stays the same as for the previous day.
        For travel days, it's a minimum of yesterday's cost plus one single-day ticket, or cost for 7 days ago plus
        one 7-day pass, or cost  of 30 days ago plus one 30-day pass:
            dp[i] = min(dp[i-1] + costs[0], dp[i-7] + costs[1], dp[i-30] + costs[2])
    Time complexity: O(W), where W = 365 is the maximum numbered day in the travel plan
    Space complexity: O(W)
    """
    dp = [0] * (days[-1] + 1)  # Instead of creating a 365 days table, we create until the last day on the days list
    durations, days, n = [1, 7, 30], set(days), len(dp)  # Faster lookup of days using a hash set
    for i in range(1, n):
        if i in days:
            for duration, cost in zip(durations, costs):
                dp[i] = min(dp[i], dp[i - duration if i - duration >= 0 else 0] + cost)  # Note how we deal with edge
                # cases (i < 7) and (i < 30)
        else:  # If the current day is a non-travel day, we're not spending any extra money
            dp[i] = dp[i - 1]
    return dp[-1]


def min_cost_tickets_v2(days, costs):
    """ In the previous solution, we store cost for all calendar days. However, we can track the minimum cost only
        for each travel day. We process only travel days and store (day, cost) for 7-and 30-day passes in the last7
        and last30 queues. After a pass 'expires', we remove it from the queue. This way, our queues only contains
        travel days for the last 7 and 30 days, and the cheapest pass prices are in the front of the queues.
    Time complexity: O(days)
    Space complexity: O(38). Stricter, it's a sum of duration for all pass types, (1 + 7 + 30) in our case
    """
    last7 = deque()  # Using queue so that the oldest ticket is at the top
    last30 = deque()
    min_cost = 0
    for today in days:
        # Discard expired 7-day pass(es). For example, if we travel on days 1, 2, 3, and 9, on day 9 we remove 1 and 2
        # and use the 7-day pass price we would have bought on day 3. Elements in last7 show the price for the
        # previous day plus a 7-day pass.
        while last7 and last7[0][0] + 7 <= today:
            last7.popleft()
        while last30 and last30[0][0] + 30 <= today:  # Discard expired 30-day pass(es)
            last30.popleft()
        last7.append((today, min_cost + costs[1]))
        last30.append((today, min_cost + costs[2]))
        # Take the min of daily pass and current valid 7-day or 30-day pass
        min_cost = min(min_cost + costs[0], last7[0][1], last30[0][1])
    return min_cost


class Test(unittest.TestCase):
    data = [([1, 4, 6, 7, 8, 20], [2, 7, 15], 11), ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15], 17)]

    def test_min_cost_tickets(self):
        for test_days, test_costs, result in self.data:
            self.assertEqual(result, min_cost_tickets_v1(test_days, test_costs))
            self.assertEqual(result, min_cost_tickets_v2(test_days, test_costs))


if __name__ == '__main__':
    unittest.main()
