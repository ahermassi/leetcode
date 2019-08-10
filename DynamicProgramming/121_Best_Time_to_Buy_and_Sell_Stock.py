""" Say you have an array for which the ith element is the price of a given stock on day i.
If you were only permitted to complete at most one transaction (i.e., buy one and sell one share of the stock), design
an algorithm to find the maximum profit.
Note that you cannot sell a stock before you buy one. """

import unittest2 as unittest


def max_stock_profit_v1(prices):
    """ We can maintain two variables - min_price and max_profit. When iterating the array we consider to sell on day
    i what would be the best profit against its current minimum buying price while updating minimum buying price.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_profit, min_price = 0, float('inf')
    for price in prices:
        min_price = min(price, min_price)  # This is the min price so far
        profit = price - min_price  # This is the best possible profit if stock is sold now at this current price
        max_profit = max(profit, max_profit)
    return max_profit


# Below are two variations of the solution.

def max_stock_profit_v2(prices):
    """
    Here, the logic is to calculate the difference (max_cur += prices[i] - prices[i-1]) of the original array, and find
    a contiguous sub-array giving maximum profit. If the difference falls below 0, reset it to zero. By resetting
    max_cur to 0, essentially it means that we have found a point i where the price[i] is lower than the time we bought,
    and that we should then try to buy at point i to see if we can achieve a bigger gain.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    cur_max = max_profit = 0
    for i in range(1, len(prices)):
        cur_max = max(0, cur_max + prices[i] - prices[i - 1])
        max_profit = max(cur_max, max_profit)
    return max_profit


def max_stock_profit_v3(prices):
    """
    dp[i] == 0 means that it's not possible to make any (positive) profit selling the stock at hand. Resetting it to 0
    is like saying start over and buy stock at time i. Positive dp[i] indicates how much profit can be made selling
    stock at time i.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not prices:
        return 0
    dp = [0] * len(prices)
    for i in range(1, len(prices)):
        dp[i] = max(0, dp[i - 1] + prices[i] - prices[i - 1])
    return max(dp)


class Test(unittest.TestCase):
    data = [([7, 1, 5, 3, 6, 4], 5), ([7, 6, 4, 3, 1], 0)]

    def test_max_stock_profit(self):
        for test_array, result in self.data:
            self.assertEqual(result, max_stock_profit_v1(test_array))
            self.assertEqual(result, max_stock_profit_v2(test_array))
            self.assertEqual(result, max_stock_profit_v3(test_array))


if __name__ == '__main__':
    unittest.main()
