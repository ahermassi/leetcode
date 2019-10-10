""" You are given coins of different denominations and a total amount of money amount. Write a function to compute the
fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any
combination of the coins, return -1. """

import unittest2 as unittest


def coin_change_v1(coins, amount):
    """ This solution is inspired by the BFS solution for problem 279- Perfect Squares. Since it is to find the least
        coin solution (like a shortest path from 0 to amount), using BFS gives results much faster than DP. We use a
        'visited' set to avoid exploring amounts that were previously investigated (memoization)
    Time complexity: S * N, where S is the amount and N is the number of coins
    Space complexity: O(S + N) for 'remaining' and 'visited' sets
    """
    if amount == 0:
        return 0
    visited = set()
    remaining, count = {amount}, -1
    while remaining:
        count += 1
        temp = set()
        for x in remaining:
            if x not in visited:
                for y in coins:
                    if x == y:
                        return count + 1
                    if x > y:
                        temp.add(x - y)
                visited.add(x)
        remaining = temp
    return -1


class Test(unittest.TestCase):
    data = [([1, 2, 5], 11, 3), ([2], 3, -1)]

    def test_coin_change(self):
        for test_coins, test_amount, result in self.data:
            self.assertEqual(result, coin_change_v1(test_coins, test_amount))


if __name__ == '__main__':
    unittest.main()
