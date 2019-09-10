""" A robot is located at the top-left corner of a m x n grid (marked 'Start' in the diagram below).
The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner
of the grid (marked 'Finish' in the diagram below).

How many possible unique paths are there? """

import unittest2 as unittest


def unique_paths_v1(m, n):
    """ Top down + memoization
        The idea is to notice that:
        - When we are in cells (n - 2, m - 1) or (n - 1, m - 2), there is exactly only one way to reach bottom right
          corner, which is to either move down or right, respectively
        - When we are at cell (n - 2, m - 2), there are exactly 2 ways to reach bottom right corner, which are to either
          right - down or down - right
        These are the base cases.
        So if we know the number of ways to get to these points, denoted as right and down , then the total ways to get
        to the bottom right corner is right + down
    Time complexity: O(n * m)
    Space complexity: O(n * m)
    """

    def count(i, j):
        if i >= n or j >= m:
            return 0
        if (i == n - 2 and j == m - 1) or (i == n - 1 and j == m - 2):
            return 1
        if i == n - 2 and j == m - 2:
            return 2
        if (i, j + 1) in memo:
            right = memo[i, j + 1]
        else:
            right = count(i, j + 1)
            memo[(i, j + 1)] = right
        if (i + 1, j) in memo:
            down = memo[i + 1, j]
        else:
            down = count(i + 1, j)
            memo[(i + 1, j)] = down
        return right + down

    memo = {}
    if n == m == 1:
        return 1
    return count(0, 0)


def unique_paths_v2(m, n):
    """ Bottom up + memoization.
        dp[i][j] equals to how many ways I can reach the current cell (i, j) moving only right and/or down, expect the
        first row and the first column, since there are only one way to get to those cells (straight right or straight
        down, respectively).
    Time complexity: O(n * m)
    Space complexity: O(n * m)
    """
    dp = [[1 for _ in range(m)] for _ in range(n)]
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i][j - 1] + dp[i - 1][j]  # This is our 'right' and 'down' from previous solution
    return dp[-1][-1]  # This is the bottom right corner where we want to stop


class Test(unittest.TestCase):
    data = [(3, 2, 3), (7, 3, 28)]

    def test_unique_paths(self):
        for test_m, test_n, result in self.data:
            self.assertEqual(result, unique_paths_v1(test_m, test_n))
            self.assertEqual(result, unique_paths_v2(test_m, test_n))


if __name__ == '__main__':
    unittest.main()

