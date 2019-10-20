""" Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right which minimizes the
sum of all numbers along its path.
Note: You can only move either down or right at any point in time. """

import unittest2 as unittest


def min_path_sum_v1(grid):
    """ Similar to 62- Unique paths.
        dp(i,j) represents the minimum sum of the path from top left to the index (i, j). We start by initializing the
        top left element of dp as the first element of the given matrix. Then for each element starting from the top
        left, we traverse onwards and fill in the matrix with the required minimum sums. Now, we need to note that at
        every element, we can move either rightwards or downwards. Therefore, for filling in the minimum sum, we use
        the equation:
            dp(i,j)= grid(i,j) + min(dp(i+1,j), dp(i,j+1))
        taking care of the boundary conditions.
    Time complexity: O(N * M), we traverse the entire matrix once
    Space complexity: O(N * M)
    """
    n, m = len(grid), len(grid[0])
    dp = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if i == j == 0:
                dp[i][j] = grid[i][j]
            elif not i:
                dp[i][j] = grid[i][j] + dp[i][j - 1]
            elif not j:
                dp[i][j] = grid[i][j] + dp[i - 1][j]
            else:
                dp[i][j] = grid[i][j] + min(dp[i][j - 1], dp[i - 1][j])
    return dp[n - 1][m - 1]


class Test(unittest.TestCase):
    data = [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7)]

    def test_min_path_sum(self):
        for test_grid, result in self.data:
            self.assertEqual(result, min_path_sum_v1(test_grid))


if __name__ == '__main__':
    unittest.main()
