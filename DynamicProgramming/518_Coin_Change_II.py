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


def change_v2(amount, coins):
    """ Bottom-Up Dynamic Programming.

         Let dp[i][j] be the number of ways to make up the j amount using the coins[:i+1], i.e. coins up to and
         including index i.

         We initialize dp[i][0] = 1 for all values of i from 0 to n-1 since we can always make up the amount 0 by not
         selecting any coins. While moving from bottom to top, this serves as the base case for the solution.

         When converting a top-down solution to a bottom-up one, we need to iterate starting from the base cases. As
         such, we will iterate i from 1 until n in the outer loop. It controls the index of the current coin under
         consideration. For the inner loop, we iterate j from 1 until amount to control the remaining amount to be made.

         Each iteration inside the nested loop represents a state (i, j). As such, we can apply the exact same logic to
         calculate dp[i][j].

         If coins[i] > j, we cannot use the current coin, so we set:

                    dp[i][j] = dp[i - 1][j].

         Otherwise, if we can use the current coin, we add the number of ways to make up the amount j by both selecting
         it and ignoring it:

                    dp[i][j] = dp[i - 1][j] + dp[i][j - coins[i]]

        After computing all the dp states in the nested loops, dp[n][amount] state stores the answer.

        For any combination making up to amount=j, it can be uniquely classified into either one of the following cases:

            - Case 1:  coins[i] is not used at all
            - Case 2:  coins[i] is used somewhere

        In case 1, there's dp[i-1][j] ways by definition.
        In case 2, we need to make sure at least one coins[i] is used. This is equivalent to adding one coins[i] for
        every way to make up amount = j - coins[i].

        !!! IMPORTANT !!!
        An alternate way of defining dp[i][j] is the number of ways to make up the j amount using the first i coins,
        i.e. coins[:i]. This definition doesn't change the base cases but does change the transition function to:

                    dp[i][j] = dp[i - 1][j] + (dp[i][j - coins[i-1]] if j >= coins[i-1])

        Notice the i-1 instead of i.

    Time complexity: O(amount * coins)
    Space complexity: O(amount * coins)
    """
    n = len(coins)
    dp = [[0] * (amount + 1) for _ in range(n)]
    for i in range(n):
        dp[i][0] = 1
    for i in range(n):
        for j in range(1, amount + 1):
            dp[i][j] = dp[i - 1][j]  # Skip the ith coin
            if j >= coins[i]:
                dp[i][j] += dp[i][j - coins[i]]  # Use the ith coin
    return dp[n - 1][amount]


def change_v3(amount, coins):
    """ Bottom-Up Dynamic Programming.

         Let dp[i][j] be the number of ways to make up the j amount using the coins beginning from index i. Note that
         here, dp[i][j] is equivalent to dfs(i, j) from the top-down approach.

         We initialize dp[i][0] = 1 for all values of i from 0 to n since we can always make up the amount 0 by not
         selecting any coins. While moving from bottom to top, this serves as the base case for the solution.

         When converting a top-down solution to a bottom-up one, we need to iterate starting from the base cases. As
         such, we will iterate i from n-1 until 0 in the outer loop. It controls the index of the current coin under
         consideration. For the inner loop, we iterate j from 1 until amount to control the remaining amount to be made.

         Each iteration inside the nested loop represents a state (i, j). As such, we can apply the exact same logic to
         calculate dp[i][j].

         If coins[i] > j, we cannot use the current coin, so we set:

                    dp[i][j] = dp[i + 1][j].

         Otherwise, if we can use the current coin, we add the number of ways to make up the amount j by both selecting
         it and ignoring it:

                    dp[i][j] = dp[i + 1][j] + dp[i][j - coins[i]]

        After computing all the dp states in the nested loops, dp[0][amount] state stores the answer, just like
        dfs(0, amount) was the answer in the top-down approach.

    Time complexity: O(amount * coins)
    Space complexity: O(amount * coins)
    """
    n = len(coins)
    dp = [[0] * (amount + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1
    for i in reversed(range(n)):
        for j in range(1, amount + 1):
            dp[i][j] = dp[i + 1][j]  # Skip the ith coin
            if j >= coins[i]:
                dp[i][j] += dp[i][j - coins[i]]  # Use the ith coin
    return dp[0][amount]


def change_v4(amount, coins):
    """ Space-optimized Bottom-Up Dynamic Programming.

         The value in column j only depends on the value in column j-1 and the column j itself. Thus, we can store the
         previous column when calculating the result for current column.

         Notice we can not do this by each row since the result of row i also depends on the result in row i-coin[j] for
         a different j. Thus, we need information on multiple rows to calculate the current row.

    Time complexity: O(amount * coins)
    Space complexity: O(amount)
    """
    n = len(coins)
    cur = [0] * (amount + 1)
    cur[0] = 1
    for i in range(n):
        nxt = [0] * (amount + 1)
        nxt[0] = 1
        for j in range(1, amount + 1):
            nxt[j] = cur[j]
            if j >= coins[i]:
                nxt[j] += nxt[j - coins[i]]
        cur = nxt
    return cur[amount]


def change_v5(amount, coins):
    """ Space-optimized Bottom-Up Dynamic Programming.

         The state transition, as we discussed in previous approaches, is:

                    dp[i][j] = dp[i - 1][j] + dp[i][j - coins[i]]

        Looking closely at this transition, we can see that to fill dp[i][j] for a specific i and all values of j we
        only need the values from dp[i] and dp[i - 1]. Values from older rows like i-2, i-3, etc. are no longer
        relevant.

        We can optimize the previous solution by using just one 1D array dp of size amount+1.

        We would have an outer loop that selects the current coin under consideration from i=0 to n-1 similar to a
        previous approach. After the ith iteration of the outer loop, dp[j] would represent dp[i][j] from a previous
        implementation.

        We initialize dp[0] = 1 since we can always make up the amount 0 by not selecting any coins. It acts as a base
        case. This is similar to setting dp[i][0] = 1 in a previous approach.

        Now, consider that we have all the values of row i-1 in dp and that we now need to compute the values of row i.
        We can begin an inner loop that iterates from j = coins[i] to amount. The reason we don't need to consider
        values from j=1 to coins[i] - 1 is because we cannot select the ith coin for those values of j.

        In such cases, as we saw in a previous approach, dp[i][j] = dp[i - 1][j]. As a result, we don't need to
        modify these values that were computed in the previous iteration.

        We start an inner loop from j = coins[i] to amount. Now, we have two cases.

            - We ignore the current coin. The number of ways to make up the j amount ignoring the current coin is
               already present in dp[j]. It is computed in the previous iteration (for row i-1) and is identical to the
               state dp[i - 1][j] of a previous approach.

            - When we choose the current coin, we add dp[j - coins[i]]. This is equivalent to adding dp[i][j - coins[i]]
               from a previous approach.

        So, we do dp[j] += dp[j - coins[i]] to add both the cases (analogous to dp[i - 1][j] and dp[i][j - coins[i]]).

        After all iterations, dp[amount] stores the answer.

        Let's consider an example: amount = 11, coins = [2, 5, 10] . Note, that coins are unlimited.

        If the total amount of money is zero, there is only one combination: to take zero coins.

        Let's consider the situation where there is only one kind of coins available: 2.
        It's obvious that all amounts less than 2 are not impacted by the presence of coin 2. Starting from amount=2,
        we could use 2 in the combinations. Since the amounts are considered gradually from 2 to 11, at each given
        moment we could be sure to add not more than one coin to the previously created combinations.

        So let's pick 2 and use it to make up amount=2. The number of combinations is the number combinations for
        amount=2-2=0, i.e. 1.

        Now let's pick 2 and use it to make up amount=3. The number of combinations is the number combinations for
        amount=3-2=1, i.e. 0.

        That leads to DP formula for the number of combinations to make up the amount x:

                    dp[x] = dp[x - coin]

        where coin is the value of the coin under consideration.

        Now let's add coin 5. The formula is the same, but do not forget to add dp[x], number of combinations
        with coin 2. The same applies to coin 10.

        Therefore, the number of combinations to make up amount = x is:

                    dp[x] += dp[x - coin_i]

        !!! IMPORTANT !!!
        It is important to note that changing the order of the nested loops would produce an incorrect answer. We must
        iterate over the coins in the outer loop, not the amount.
        If we change the ordering of the two loops, the outer loop would run from i=1 to amount and the inner loop would
        execute from j=0 to n-1. We would perform the same operation dp[i] += dp[i - coins[j]] inside the loops. After
        the ith iteration, dp[i] would store all the ways to make up the amount i using all the coins.

        Let's take an example where coins = [1, 2] and amount = 3. The correct answer for this case is 2 (1 + 1 + 1 and
        1 + 2).

        However, if we look at the last iteration of the outer loop when i=3, we will execute dp[3] = dp[3] + dp[3-1]
        when the first coin is selected using the inner loop. dp[2] would be equal to 2 as there is two ways to make
        up amount 2 (1+1 and 2). This way we selected two cases: 1+1+1 and 1+2.

        We also execute dp[3] = dp[3] + dp[3-2] when the second coin is selected. dp[1] would be equal to 1 as there is
        just one way to make up amount 1. This way we counted the 1+2 case. We counted the 1+2 case TWICE.

        Overall, the returned answer would be 3 which is incorrect. Switching the ordering of the loops returns all the
        PERMUTATIONS (1 + 1 + 1, 1 + 2, 2 + 1) as the answer instead of the COMBINATIONS where 1 + 2 and 2 + 1 are not
        considered as separate cases.

        If the outer loop is the amount, then the same combination will be counted multiple times because they can come
        in different orders. By letting the coins be the outer loop, we're sure that for any valid combination, the
        order of each coin will always be the same as their order in coins, so there can be no duplicates.

        Let's take another example: amount=3, coins = [1, 2]

        If we make amount the outer loop, we will get amount=3 using: [1+1+1 , 1+2, 2+1] . We can see that we are
        counting [1+2] and [2+1], although both are same arrangement. The reason behind it is we count
        dp[3] = dp[3-1] + dp[3-2] = dp[2] + dp[1]

        --> arrangements of amount = 2 with coin 1 at the end AND arrangements of amount = 1 with coin 2 at the end
        --> {1+1 +1; 2 +1} AND {1 +2}

        If the outer loop is the amount, we are considering every coin at every stage.
        If amount=2, it can be made using 2 and 1+1, so 2 combinations. If amount=3,  we would consider every coin
        again, which would mean that we're trying dp[amount-1] and dp[amount-2], which is 2 (as there are 2 combinations
        for amount=2) and 1 (1 combination for amount=1). So in this case, we have 3 combinations for amount=3:

            1 + 2 - taken from dp[amount-2]
            2 + 1, 1 + 1 + 1 - taken from dp[amount-1]

        We can see there is one duplicate: 1+2 and 2+1

        If the outer loop is coins, we are NOT considering every coin at every stage.
        Let's assume we've already calculated all dps for coin with value 1. So for every amount there is just one
        combination, dp array looks like that: [1, 1, 1, 1, 1...]
        Now we are doing all calculations with value 2. We are at amount=2, so, again, amount=2 has 2 combinations:
        1+1 and 2. Makes sense, no duplicates.
        For amount=3, we are NOT considering every coin again - we are just considering ending every combination with 2,
        so ONLY dp[amount-2]. That would make only two combinations for amount=3:

            1 + 1 + 1 - taken as previous value of dp[3], calculated for coin value 1
            1 + 2 - taken from dp[amount-2]

        Hopefully, this shows why we don't have duplicates - all combinations are started with the lowest value coins,
        and there is no way to have the lowest value coin at the end. Think of it as having all SORTED combinations.

        If amount=4, the question is: how many ways to make up 4 using coins 1, 2 ?
        We already know how many ways to get 4 using only coin denomination 1 (1+1+1+1), but we also know how many ways
        to get amount =2 (4 - 2) using coins 1, 2: 1+1 and 2. What if we add a coin of denomination 2 to these two
        combinations: 1+1 +2, 2 +2. Then in total, we'll have 3 combinations: 1+1+1+1, 1+1+2, 2+2.

    Time complexity: O(amount * coins)
    Space complexity: O(amount)
    """
    n = len(coins)
    dp = [0] * (amount + 1)
    dp[0] = 1
    for i in range(n):
        for j in range(coins[i], amount + 1):
            dp[j] += dp[j - coins[i]]
    return dp[amount]


class Test(unittest.TestCase):
    data = [(5, [1, 2, 5], 4), (3, [2], 0)]

    def test_change(self):
        for test_amount, test_coins, result in self.data:
            self.assertEqual(result, change_v1(test_amount, test_coins))
            self.assertEqual(result, change_v2(test_amount, test_coins))
            self.assertEqual(result, change_v3(test_amount, test_coins))
            self.assertEqual(result, change_v4(test_amount, test_coins))
            self.assertEqual(result, change_v5(test_amount, test_coins))


if __name__ == '__main__':
    unittest.main()
