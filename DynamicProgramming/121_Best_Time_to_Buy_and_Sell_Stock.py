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


class Test(unittest.TestCase):
    data = [([7, 1, 5, 3, 6, 4], 5), ([7, 6, 4, 3, 1], 0)]

    def test_max_stock_profit(self):
        for test_array, result in self.data:
            self.assertEqual(result, max_stock_profit_v1(test_array))


if __name__ == '__main__':
    unittest.main()
