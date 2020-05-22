""" You are given coins of different denominations and a total amount of money. Write a function to compute the number
of combinations that make up that amount. You may assume that you have infinite number of each kind of coin. """

import unittest2 as unittest


def change(amount, coins):
    """ This is a classical dynamic programming problem.
        Let's pick an example: amount = 11, available coins: 2 cent, 5 cent and 10 cent. Note, that coins are unlimited.
        If the total amount of money is zero, there is only one combination: to take zero coins.
        Let's do one step further and consider the situation with one kind of available coins: 2 cent. It's quite
        obvious that all amounts less than 2 are not impacted by the presence of 2 cent coins. Starting from amount = 2,
        we could use 2 cent coins in the combinations. Since the amounts are considered gradually from 2 to 11, at each
        given moment we could be sure to add not more than one coin to the previously known combinations.
        So let's pick up 2 cent coin, and use it to make amount = 2. The number of combinations with this 2 cent coin
        is the number combinations for amount = 0, i.e. 1.
        Now let's pick up 2 cent coin, and use it to make up amount = 3. The number of combinations with this 2 cent
        coin is the number combinations for amount = 1, i.e. 0.
        That leads to DP formula for number of combinations to make up the amount x:
            dp[x] = dp[x] + dp[x - coin]
        where coin = 2 cents is the value of coin we're currently adding.
        Now let's add 5 cent coins. The formula is the same, but do not forget to add dp[x], number of combinations
        with 2 cent coins. The story is the same for 10 cent coins.
        Therefore, the number of combinations to make up amount = x is:
            dp[x] += dp[x - coin]
        for each of the coins.
        Why is the outer loop is the coins, not the amount?
        The reason behind that is that the problem is to find the total number of combinations, not the permutations.
        If the outer loop is the amount, then the same combination will be counted multiple times because they can come
        in in different orders. By letting the coins be the outer loop, we're sure that for any valid combination, the
        order of each coin will always be the same as their order in coins, so there can be no duplicates. If we switch
        the loops order, we will count same arrangement multiple times.
        Let's take an example: amount = 3, coins = [1, 2]
        If we make amount the outer loop, we will get amount = 3 like this: [1+1+1 , 1+2, 2+1] . We can see that we are
        counting [1+2] and [2+1], although both are same arrangement. The reason behind it is we will count
        dp[3] = dp[3-1] + dp[3-2] = dp[2] + dp[1]
        ---> arrangements of amount = 2 with coin 1 at the end AND arrangements of amount = 1 with coin 2 at the end
        ---> {1+1 +1; 2 +1} AND {1 +2}
        If outer loop is amount, we are considering every coin at every stage.
        If amount = 2, it can be made from 2 and 1 + 1, so 2 combinations. If amount = 3,  we would consider every coin
        again, which would mean that we're trying dp[amount - 1] and dp[amount - 2], which is: 2 (as there are 2
        combinations for amount 2) and 1 (1 combination for amount 1). So in this case we have 3 combinations for
        amount = 3:
            1 + 2 - taken from dp[amount - 2]
            2 + 1, 1 + 1 + 1 - taken from dp[amount - 1]
        We can see there is one duplicate: 1 + 2 and 2 + 1
        If outer loop is coins, we are NOT considering every coin at every stage.
        Let's assume we've already calculated all dps for coin with value 1. So for every amount there is just one
        combination, dp array looks like that: [1, 1, 1, 1, 1...]
        Now we are doing all calculations with value 2. We are at amount = 2, so again, amount 2 has 2 combinations:
        1 + 1 and 2. Makes sense, no duplicates.
        For amount = 3, we are NOT considering every coin again - we are just considering ending every combination
        with 2, so ONLY dp[amount - 2]. That would make only two combinations for amount 3:
            1 + 1 + 1 - taken as previous value of dp[3], calculated for coin value 1
            1 + 2 - taken from dp[amount - 2]
        Hopefully it shows why we don't have duplicates - all combinations are started with lowest coins, there is no
        way to have lowest coin at the end. We can think that We have all SORTED combinations.
        If amount = 4, the question is: How many ways to make up 4 using coins 1, 2 ?
        We already know how many ways to get 4 using only coin denomination 1 (1+1+1+1), but we also know how many ways
        to get an amount of 2 (4 - 2) using coins 1, 2: 1+1 and 2. What if we add a coin of denomination 2 to these
        two combinations: 1+1 +2, 2 +2. Then in total we'll have 3 combinations: 1+1+1+1, 1+1+2, 2+2.
    Time complexity: O(amount * coins)
    Space complexity: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for i in range(1, amount + 1):
            if i >= coin:
                dp[i] += dp[i - coin]
    return dp[amount]


class Test(unittest.TestCase):
    data = [(5, [1, 2, 5], 4), (3, [2], 0)]

    def test_change(self):
        for test_amount, test_coins, result in self.data:
            self.assertEqual(result, change(test_amount, test_coins))


if __name__ == '__main__':
    unittest.main()
