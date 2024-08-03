""" Say you have an array for which the ith element is the price of a given stock on day i.
Design an algorithm to find the maximum profit. You may complete as many transactions as you like (i.e., buy one and
sell one share of the stock multiple times).
Note: You may not engage in multiple transactions at the same time (i.e., you must sell the stock before you buy
again). """

import unittest2 as unittest


# For more details: https://leetcode.com/articles/best-time-to-buy-and-sell-stock-ii/

def max_profit_v1(prices):
    """ The profit is the sum of sub-profits. Each sub-profit is the difference between selling at day j, and buying at
         day i (with j > i). The range [i, j] should be chosen so that the sub-profit is maximum:

                    sub-profit = prices[j] - prices[i]

         We should choose j that prices[j] is as big as possible, and choose i that prices[i] is as small as possible
         (of course within their local range).

         From this observation, from day X, the buying day will be the last continuous day that the price is smallest.
         Then, the selling day will be the last continuous day that the price is biggest.

         In other words:

         Consider a contiguous sub-sequence of increasing prices. The profit-maximizing strategy within this
         sub-sequence is to buy on the first day and sell on the last day because this is the only strategy that
         realizes all the day-to-day gains within the sub-sequence.

         Therefore, profit can be maximized by identifying each maximally-sized contiguous sub-sequence of increasing
         prices, and buying at the beginning of it and selling at the end of it.

         Since we are only asked to return the total profit and not the actual transaction log, it suffices to sum
         together the day-to-day gains across the entire sequence.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_profit, i, n = 0, 0, len(prices)
    while i < n - 1:
        # Finding local minima
        while i < n - 1 and prices[i + 1] <= prices[i]:
            # While we can find a lower price ahead, we keep moving
            i += 1
        buy = prices[i]  # Buy at this locally lowest price
        # Finding local maxima
        while i < n - 1 and prices[i + 1] >= prices[i]:
            # While we can find a higher price ahead, we keep moving
            i += 1
        sell = prices[i]  # Sell at this locally highest price
        max_profit += sell - buy
    return max_profit


# Video explanation: https://youtu.be/3SJ3pUkPQMc
def max_profit_v2(prices):
    """ Instead of looking for every peak following a valley, we can simply go on crawling over the slope and keep on
         adding the profit obtained from every consecutive transaction.

         We can directly keep on adding the difference between the consecutive prices if the current price is higher
         than the previous one, and the total sum we obtain will be the maximum profit.

         !!! IMPORTANT !!!
         Notice that this is equivalent to considering EVERY day a buying day and realizing a profit only when an
         opportunity arises THE FOLLOWING DAY. The previous day's price is the LAST buying price. This step simulates
         selling the stock bought at start price, capturing the profit, and then considering the current price as a new
          buying price for potential future transactions.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            max_profit += prices[i] - prices[i - 1]
    # The following is equivalent and more explicit:
    # max_profit = 0
    # buying_price = prices[0]
    # for i in range(1, len(prices)):
    #     if prices[i] > buying_price:
    #         max_profit += prices[i] - buying_price
    #     buying_price = prices[i]
    return max_profit


class Test(unittest.TestCase):
    data = [([7, 1, 5, 3, 6, 4], 7), ([1, 2, 3, 4, 5], 4), ([7, 6, 4, 3, 1], 0)]

    def test_max_profit(self):
        for test_prices, result in self.data:
            self.assertEqual(result, max_profit_v1(test_prices))
            self.assertEqual(result, max_profit_v2(test_prices))


if __name__ == '__main__':
    unittest.main()
