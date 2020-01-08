""" You are given coins of different denominations and a total amount of money amount. Write a function to compute the
fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any
combination of the coins, return -1. """

from collections import deque
import unittest2 as unittest


def coin_change_v1(coins, amount):
    """ This solution is inspired by the BFS solution for problem 279- Perfect Squares. Since it is to find the least
        number of coins (like a shortest path from amount to 0), using BFS gives results much faster than DP. We use a
        'visited' set to avoid exploring amounts that were previously investigated.
    Time complexity: O(S * N), where S is the amount and N is the number of coins
    Space complexity: O(S + N) for the queue and 'visited' set
    """
    visited = set()
    queue = deque([(amount, 0)])
    while queue:
        remaining, total_coins = queue.popleft()
        if not remaining:
            return total_coins  # Because we use BFS, we're sure this is the 'shortest path' from amount to 0
        for coin in coins:
            if remaining >= coin and remaining - coin not in visited:
                queue.append((remaining - coin, total_coins + 1))
                visited.add(remaining - coin)
    return -1


def coin_change_v2(coins, amount):
    """ The problem could be solved with polynomial time using Dynamic programming technique. First, let's define:
        F(S) - minimum number of coins needed to make change for amount S using coin denominations [c0.. cn−1].
        How to split the problem into sub problems? Let's assume that we know F(S) where some change val_1, val_2,...
        for S which is optimal and the last coin's denomination is C. Then the following equation should be true
        because of optimal substructure of the problem:
        F(S) = F(S−C) + 1
        But we don't know which is the denomination of the last coin C. We compute F(S - c_i) for each possible
        denomination c0, c1,...,c_n-1 and choose the minimum among them. The following recurrence relation holds:
        F(S) = min(F(S - c_i) for i 0..n-1) + 1 subject to  S − c_i ≥ 0
    Time complexity: O(S * N), on each step the algorithm finds the next F(i) in N iterations, where 1 ≤i ≤S. Therefore
    in total the iterations are S * N
    Space complexity: O(S)
    """
    dp = [0] + [float('inf')] * amount
    for i in range(1, len(dp)):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[-1] if dp[-1] != float('inf') else -1


class Test(unittest.TestCase):
    data = [([1, 2, 5], 11, 3), ([2], 3, -1)]

    def test_coin_change(self):
        for test_coins, test_amount, result in self.data:
            self.assertEqual(result, coin_change_v1(test_coins, test_amount))
            self.assertEqual(result, coin_change_v2(test_coins, test_amount))


if __name__ == '__main__':
    unittest.main()
