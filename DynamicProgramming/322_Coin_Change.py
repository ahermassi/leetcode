""" You are given coins of different denominations and a total amount of money amount. Write a function to compute the
fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any
combination of the coins, return -1. """

from collections import deque
import unittest2 as unittest


def coin_change_v1(coins, amount):
    """ BFS. Similar to  279- Perfect Squares

        Since we want to find the least number of coins (like the shortest path from amount to 0), using BFS gives
        results that are much faster than DP.

        We use a 'visited' set to avoid exploring amounts that were previously processed.

    Time complexity: O(S * N), where S is the amount and N is the number of coins
    Space complexity: O(S + N), for the queue and 'visited' set
    """
    visited, queue = set(), deque([(amount, 0)])
    while queue:
        remaining, total_coins = queue.popleft()
        if not remaining:
            # Because we use BFS, we're sure this is the shortest path from amount to 0
            return total_coins
        for coin in coins:
            if remaining >= coin and remaining - coin not in visited:
                queue.append((remaining - coin, total_coins + 1))
                visited.add(remaining - coin)
    return -1


def coin_change_v2(coins, amount):
    """ Top-down recursion + memoization.
        Let's define:
            F(S): minimum number of coins needed to make change for amount S
        We compute F(S - c_i) for each possible denomination c_0, c_1, c_2, c_n-1 and choose the minimum among them:
            F(S) = min(F(S - c_i) for i 0..n-1) + 1, subject to  S − c_i ≥ 0
​        For example, if S = 11 and coins = [1, 2, 5], then:
        F(11) = min(F(11-1), F(11-2), F(11-5)) + 1. Let's suppose min(F(11-1), F(11-2), F(11-5)) = F(11-5) = F(6).
        F(6) is the number of coins needed to make change for amount 6. When we add the coin 5 to the result, this
        represents the number of coins needed to make change for amount 11, hence the 1 added to the result.
        The answer to the sub-problem for amount 11 is the same thing as the MINIMUM of the answers to the sub problems
        with each currency deduced from the original sub problem (11) PLUS ONE since we are acting as if each coin we
        subtract from 11 is the last coin used to make change.
    Time complexity: O(S * N), where S is the amount and N is the number of coins. For each amount we will
    approximately be doing N work in trying to deduct each denomination from the current sub problem. Our recursive
    tree will at maximum have a depth of S (worst case if each call deducts 1 at each call).
    Space complexity: O(S), we answer and store a total of S sub-problems in our dynamic programming table to get to
    our globally optimum answer.
    """

    def dfs(remaining):
        if not remaining:
            return 0
        if remaining < 0:  # Minimum coins to make change for a negative amount is -1. This is just a base case we
            # arbitrarily define.
            return -1
        if remaining not in memo:
            min_coins = float('inf')
            for coin in coins:  # Remove each coin from the remaining amount and see how many more coins are needed
                res = dfs(remaining - coin)
                if 0 <= res < min_coins:
                    min_coins = res + 1  # +1 == add back the coin removed recursively
            memo[remaining] = min_coins if min_coins != float('inf') else -1  # If no answer is found
            # (min_coins == float('inf')) then the sub problem answer is just arbitrarily made to be -1, otherwise the
            # sub problem's answer is min_coins
        return memo[remaining]

    memo = {}  # We cache the minimum number of coins needed to make various smaller amounts of change
    return dfs(amount)


# Watch: https://www.youtube.com/watch?v=jgiZlGzXMBw

def coin_change_v3(coins, amount):
    """ The problem could be solved in polynomial time using Dynamic programming. First, let's define:
            dp(S): minimum number of coins needed to make change for amount S using coin denominations [c0.. cn−1]
        How to split the problem into sub problems? Let's assume that we know dp(S) where some change val_1, val_2,...
        for S which is optimal and the last coin's denomination is C. Then the following equation should be true
        because of optimal substructure of the problem:
            dp(S) = dp(S−C) + 1
        But we don't know which is the denomination of the last coin C. We compute dp(S - c_i) for each possible
        denomination c0, c1,...,c_n-1 and choose the minimum among them. The following recurrence relation holds:
            dp(S) = min(dp(S - c_i) for i 0..n-1) + 1 subject to  S − c_i ≥ 0
    Time complexity: O(S * N), for each amount we will potentially try each of the denominations
    Space complexity: O(S), we answer and store a total of S sub-problems in our dynamic programming table to get to
    our globally optimum answer
    """
    dp = [float('inf')] * (amount+1)
    dp[0] = 0  # The answer to making change with minimum coins for 0 will always be 0 coins no matter what the coins
    # we are given
    for i in range(1, amount+1):  # Solve every sub-problem from 1 to 'amount'
        for coin in coins:  # For each coin we are given ..
            if coin <= i:  # if it is less than or equal to the sub problem amount ..
                dp[i] = min(dp[i], dp[i - coin] + 1)  # try it, see if it gives us a more optimal solution
    return dp[amount] if dp[amount] != float('inf') else -1


class Test(unittest.TestCase):
    data = [([1, 2, 5], 11, 3), ([2], 3, -1)]

    def test_coin_change(self):
        for test_coins, test_amount, result in self.data:
            self.assertEqual(result, coin_change_v1(test_coins, test_amount))
            self.assertEqual(result, coin_change_v2(test_coins, test_amount))
            self.assertEqual(result, coin_change_v3(test_coins, test_amount))


if __name__ == '__main__':
    unittest.main()
