""" Say you have an array for which the ith element is the price of a given stock on day i.
If you were only permitted to complete at most one transaction (i.e., buy one and sell one share of the stock), design
an algorithm to find the maximum profit.
Note that you cannot sell a stock before you buy one. """

import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=1pkOgXD63yU


def max_stock_profit_v1(prices):
    """ If we plot the stock prices on a graph, we can clearly see that the points of interest are the peaks and
        valleys in the given graph. For every stock, we need to calculate the difference between that stock price and
        the minimum of all the values before that element, and update the maximum profit so far.

        We can maintain two variables - lowest_buying_price and max_profit, corresponding to the smallest valley and
        maximum profit (maximum difference between selling price and min buying price) obtained so far, respectively.

        While iterating over the array, we consider selling on day i and calculate what would be the best profit against
        the current minimum buying price.

        Example:
        prices = [5, 6, 2, 4, 8, 9, 5, 1, 5]

        Note: In the following code run, 'Sell' has an undefined value every time a buy operation is carried out
        (a lower buying price is found) since we can't buy and sell on the same day, but in reality the 'profit'
        is calculated in all cases as implemented in the algorithm, and profit is equal to 0 when we sell and buy
        on the same day.

        Now we will traverse the array from left to right. So in the given array 5 is the stock we bought.
            Min Buying Price:5     Sell:-               Profit:-             max profit=-

        So next element is 6. If we sell the stock at that price we will earn profit of $1.
            Min Buying Price:5     Sell:6               Profit:$1             max profit=$1

        Now the next element is 2 which is lower price than the stock we bought previously which was 5. So if we buy
        this stock at price $2 and sell it in the future, we will surely earn more profit than the stock we bought at
        price 5. So we buy stock at $2.
            Min Buying Price:2     Sell:-              Profit:-                  max profit=$1

        Next element is 4 which has higher price than the stock we bought. So we sell the stock at this price.
            Min Buying Price:2     Sell:4              Profit:$2               max profit=$2

        Moving further, now the next stock price is $8. We still have $2 stock we bought previously. If instead of
        selling it at price $4, if we sell it for $8 then the profit would be $6.
            Min Buying Price:2     Sell:8              Profit:$6                max profit=$6

        Now next stock is of $9 which is also higher than the price we bought at ($2).
            Min Buying Price:2     Sell:9              Profit:$7                max profit=$7

        Now the next stock is $5. If we sell at this price then we will earn profit of $3, but we already have a max
        profit of $7 because of our previous transaction.
            Min Buying Price:2     Sell:5              Profit:$3                max profit=$7

        Now next stock price is $1 which is less than the stock we bought of $2. If we buy this stock and sell it in
        the future then obviously we will gain more profit.
            Min Buying Price:1     Sell:-              Profit:-                   max profit=$7

        Now next stock is of $5. So this price is higher than the stock we bought.
            Min Buying Price:1     Sell:5              Profit:$4                max profit=$7

        Our maximum profit is $7.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_profit, lowest_buying_price = 0, float('inf')
    for cur_price in prices:
        lowest_buying_price = min(cur_price, lowest_buying_price)  # This is the min buying price so far
        # This is the best possible profit if stock is sold now at this current selling price
        profit = cur_price - lowest_buying_price
        max_profit = max(profit, max_profit)
    return max_profit


# Below are two variations of the solution.

def max_stock_profit_v2(prices):
    """ Here the logic is to calculate the difference (max_cur += prices[i] - prices[i-1]) of the original array, and
        find a contiguous sub-array giving maximum profit. If the difference falls below 0, reset it to zero. By
        resetting max_cur to 0, it essentially means that we have found a point i where prices[i] is lower than the
        time we bought at and that we should then try to buy at point i to see if we can achieve a bigger gain.
        We are basically applying Kadane's algorithm to the difference array of prices to find the maximum sub-array
        sum.
        Example:
        prices = [7, 1, 5, 3, 6, 4] --> prices_difference = [0, -6, 4, -2, 3, -2]
        At each step i, we update cur_max: cur_max = max(0, cur_max + prices_difference[i]), such as:
        prices_difference[i] = prices[i] - prices[i-1]
    Time complexity: O(N)
    Space complexity: O(1)
    """
    cur_max = max_profit = 0
    for i in range(1, len(prices)):
        cur_max = max(0, cur_max + prices[i] - prices[i-1])  # At any point, we either buy stock and have a current
        # maximum profit of 0 (buying and selling at the same day is not possible, so we're basically starting over),
        # or sell stock and update our new current max profit
        max_profit = max(cur_max, max_profit)  # Keep track of the maximum profit found so far
    return max_profit


def max_stock_profit_v3(prices):
    """ Let dp[i] denote the max profit on ith day. dp[i] = 0 means that it's not possible to make any (positive)
        profit selling the stock at hand. Resetting it to 0 is like saying start over and buy stock at time i. Positive
        dp[i] indicates how much profit can be made selling stock at time i.
        At any given day, we can either be in a trade, or not. If we're in a trade, our profit at the end of that day
        is:
            dp[i] = prices[i] - prices[i-1] + dp[i-1]
        The price movement today, plus the profit from yesterday. If we're not in a trade, our profit is 0. Since we're
        looking for profitable trades, we can take the max of that:
            dp[i] = max(0, prices[i] - prices[i-1] + dp[i-1])
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not prices:
        return 0
    dp = [0] * len(prices)
    for i in range(1, len(prices)):
        dp[i] = max(0, dp[i-1] + prices[i] - prices[i-1])
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
