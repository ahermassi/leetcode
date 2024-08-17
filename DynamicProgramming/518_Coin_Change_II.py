""" You are given coins of different denominations and a total amount of money. Write a function to compute the number
of combinations that make up that amount. You may assume that you have infinite number of each kind of coin. """

import unittest2 as unittest


# Video explanation: https://youtu.be/Mjy4hd2xgrs
# Video explanation: https://www.youtube.com/watch?v=DJ4a7cmjZY0
def change_v1(amount, coins):
    """ Top-Down Dynamic Programming.

         Intuitively, we could think of iterating over the coins. For a specific coin, we have two options: either we
         take this coin and decrease the remaining amount we still need, or we ignore the coin and move to the next one
         without changing the remaining amount. We add the number of ways to make up the required amount from both
         choices.

         If we choose to take a coin with value, we are now searching for a combination of coins that sum up to
         amount-value. If we choose to skip the coin, we are still looking for a combination of coins that sum up to
         amount, but with fewer coins.

         Let dfs(index, remaining) be the recursive method that we use to solve the problem. It would require two
         parameters: the index of the current coin under consideration and the remaining amount needed. It would return
         the number of ways to make up the amount by only considering the coins beginning from that index.

            - If index equals n (where n is the number of coins), we return 1 if the remaining amount equals 0. We can
               choose one way by not selecting any coin to make up an amount of 0.

            - Otherwise, return 0 as we don't have any more coins and hence can't possibly make up the amount.

        These two form the base cases of the recursive implementation.

        If the current coin is worth more than the remaining amount we need, we must skip the current coin. Otherwise,
        we consider both options: skip the current coin or use the current coin (check the .img file).

        !!! IMPORTANT !!!
        One key thing to understand here is the fact that we are not looking for the number of permutations, rather, we
        are looking for the number of combinations. That is, [1, 2, 2] and [2, 1, 2] are equivalent. This is the reason
        we either choose the coin at index or skip it and move to the coin at index+1, in the latter case we will never
        revisit coins[index] again.

    Time complexity: O(amount * coins)
    Space complexity: O(amount)
    """

    def dfs(index, remaining):
        if index == n:
            return 1 if not remaining else 0
        if (index, remaining) in memo:
            return memo[(index, remaining)]
        combinations = 0
        use_coin = 0
        if remaining >= coins[index]:
            use_coin = dfs(index, remaining - coins[index])
        do_not_use_coin = dfs(index + 1, remaining)
        combinations += use_coin + do_not_use_coin
        memo[(index, remaining)] = combinations
        return combinations

    n = len(coins)
    memo = {}
    return dfs(0, amount)


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
            dp[x] = dp[x - coin]
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
        way to have the lowest coin at the end. We can think that we have all SORTED combinations.
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
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    return dp[amount]


class Test(unittest.TestCase):
    data = [(5, [1, 2, 5], 4), (3, [2], 0)]

    def test_change(self):
        for test_amount, test_coins, result in self.data:
            self.assertEqual(result, change(test_amount, test_coins))


if __name__ == '__main__':
    unittest.main()
