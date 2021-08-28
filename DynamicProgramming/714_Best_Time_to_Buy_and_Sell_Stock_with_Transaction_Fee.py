""" You are given an array prices where prices[i] is the price of a given stock on the ith day, and an integer fee
representing a transaction fee.

Find the maximum profit you can achieve. You may complete as many transactions as you like, but you need to pay the
transaction fee for each transaction.

Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).
"""


def max_profit_v1(prices, fee):
    """ If I am holding a share after today, then either I am just continuing holding the share I had yesterday, or
        that I held no share yesterday, but bought in one share today.
        If I am not holding a share after today, then either I did not hold a share yesterday, or that I held a share
        yesterday but I decided to sell it out today. The service fee is only charged when stock is sold
        Given any day i, its max profit status boils down to one of the two status below:
            - Buy status: max_profit_hold_at_day[i] represents the max profit at day i in buy status, given that the
              last action we took is a buy action at day k, where k <= i. We have the right to either sell at day
              (i + 1) or to do nothing (hold).
            - Sell status: max_profit_sell_at_day[i] represents the max profit at day i in sell status, given that the
              last action we took is a sell action at day k, where k <= i. We have the right to either buy at day
            (i + 1) or do nothing.
        We can start from buy status, which means we buy stock at day 0: max_profit_hold_at_day[0] = -prices[0].
        Or we can start from sell status, which means we sell stock at day 0. Given that we don't have any stock at
        hand in day 0, we set sell status to be 0: max_profit_sell_at_day[0] = 0.
        At day i, we may buy stock (from previous sell status) or do nothing (from previous buy status):

            max_profit_hold_at_day[i] = max(max_profit_hold_at_day[i-1], max_profit_sell_at_day[i-1] - prices[i])

        Or, at day i, we may sell stock (from previous buy status) or do nothing (from previous sell status):

            max_profit_sell_at_day[i] = max(max_profit_sell_at_day[i-1], max_profit_hold_at_day[i-1] + prices[i])

        We finally return max_profit_sell_at_day[last_day] as our result, which represents the max profit at the last
        day, given that we took sell action at any day before the last day.
        This problem is an introduction to state machine logic. In order to solve it, we can consider the two possible
        distinct states of being: Having no stock and being ready to buy (Buying) and owning stock and being ready to
        sell (Selling). We just need to iterate through the prices and keep track of the best possible value for these
        two states of being for each day.
        If we consider the state of being buying stock at this iteration (Buying), it can be reached from buying
        yesterday and doing nothing, OR it can be reached by being ready to sell yesterday (with the additional fee).
        We just need to pick whichever one yields the best value.
        The same is true of the selling state. The new selling state is the better result between the previous selling
        state with no action and the previous buying state with a stock purchase today.

                       no action                          sell stock (+ prices[i] - fee)
            B[i-1] ---------------> B[i]           B[i-1] ------------------------------> S[i]




            S[i-1] ---------------> S[i]           S[i-1] ------------------------------> B[i]
                       no action                             buy stock (- prices[i])

        The B state is the one in which we don't own any stock and are looking to buy. The S state is the one in which
        we own stock and are looking to sell.
        S[i] represents the max profit on day i if we don't have a stock and don't buy or have a stock and sell it.
        B[i] represents the max profit on day i if we buy a stock or have a stock and keep it.

        max_profit_sell_at_day(i): The cash in hand if we are not holding the stock at the end of day i: We might be
        not holding the stock at the end of day (i - 1), and do nothing in day i, or we might be holding the stock at
        the end of day (i - 1) and sell it at the end of day i:

                max_profit_sell_at_day[i] = max(max_profit_sell_at_day[i-1], max_profit_hold_at_day[i-1] + prices[i])

        max_profit_hold_at_day(i): The cash in hand if we are holding the stock at the end of day i. We might be
        holding the stock at the end of day (i - 1) and do nothing in day i, or we might not be not holding the stock
        at the end of day (i - 1) and buy it at the end of day i:

            max_profit_hold_at_day[i] = max(max_profit_hold_at_day[i-1], max_profit_sell_at_day[i-1] - prices[i])

    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(prices)
    max_profit_sell_at_day = [0] * n
    max_profit_hold_at_day = [0] * n
    max_profit_sell_at_day[0] = 0
    max_profit_hold_at_day[0] = -prices[0]
    for i in range(1, n):
        # Keep the same as day i-1, or sell from buy status at day i-1
        max_profit_sell_at_day[i] = max(max_profit_sell_at_day[i - 1],
                                        max_profit_hold_at_day[i - 1] + prices[i] - fee)
        # Keep the same as day i-1, or buy from sell status at day i-1
        max_profit_hold_at_day[i] = max(max_profit_hold_at_day[i - 1],
                                        max_profit_sell_at_day[i - 1] - prices[i])
    return max_profit_sell_at_day[n - 1]
