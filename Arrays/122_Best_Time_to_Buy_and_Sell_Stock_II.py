""" Say you have an array for which the ith element is the price of a given stock on day i.
Design an algorithm to find the maximum profit. You may complete as many transactions as you like (i.e., buy one and
sell one share of the stock multiple times).
Note: You may not engage in multiple transactions at the same time (i.e., you must sell the stock before you buy
again). """

import unittest2 as unittest


def max_profit_v1(prices):
    """ The profit is the sum of sub-profits. Each sub-profit is the difference between selling at day j, and buying at
        day i (with j > i). The range [i, j] should be chosen so that the sub-profit is maximum:
            sub-profit = prices[j] - prices[i]
        We should choose j that prices[j] is as big as possible, and choose i that prices[i] is as small as possible
        (of course in their local range).
        From this observation, from day X, the buying day will be the last continuous day that the price is smallest.
        Then, the selling day will be the last continuous day that the price is biggest.
        In other words:
        Consider a contiguous subsequence of increasing prices. The profit-maximizing strategy within this subsequence
        is to buy on the first day and sell on the last day because this is the only strategy that realizes all of the
        day-to-day gains within the subsequence.
        Therefore profit can be maximized by identifying each maximally-sized contiguous subsequence of increasing
        prices, and buying at the beginning of it and selling at the end of it.
        Since we are only asked to return the total profit and not the actual transaction log, it suffices to sum
        together the day-to-day gains across the entire sequence.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_profit, i, n = 0, 0, len(prices)
    while i < n - 1:
        # Finding local minima
        while i < n - 1 and prices[i + 1] <= prices[i]:  # While we can find a smaller price ahead, we keep moving
            i += 1
        buy = prices[i]  # Buy with this locally smallest price
        # Finding local maxima
        while i < n - 1 and prices[i + 1] >= prices[i]:  # While we can find a bigger price ahead, we keep moving
            i += 1
        sell = prices[i]  # Sell at this locally biggest price
        max_profit += sell - buy
    return max_profit


class Test(unittest.TestCase):
    data = [([7, 1, 5, 3, 6, 4], 7), ([1, 2, 3, 4, 5], 4), ([7, 6, 4, 3, 1], 0)]

    def test_max_profit(self):
        for test_prices, result in self.data:
            self.assertEqual(result, max_profit_v1(test_prices))


if __name__ == '__main__':
    unittest.main()
