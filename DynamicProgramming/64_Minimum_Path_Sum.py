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


def min_path_sum_v2(grid):
    """ instead of using a 2D matrix for dp, we can do the same work using a dp array of the row size, since for making
        the current entry all we need is the dp entry for the top and the left element. Thus, we start by initializing
        only the first element of dp as the first element of the given matrix. Then, we start moving towards the right
        and update the entry dp(j) as:
            dp(j) = grid(i,j) + min(dp(j), dp(j+1))
    Time complexity: O(N * M)
    Space complexity: O(M)
    """
    n, m = len(grid), len(grid[0])
    dp = [0 for _ in range(m)]
    for i in range(n):
        for j in range(m):
            if i == j == 0:
                dp[j] = grid[i][j]
            elif not i:
                dp[j] = grid[i][j] + dp[j - 1]
            elif not j:
                dp[j] = grid[i][j] + dp[j]
            else:
                dp[j] = grid[i][j] + min(dp[j - 1], dp[j])
    return dp[m - 1]


def min_path_sum_v3(grid):
    """ Instead of using another dp matrix, we can store the minimum sums in the original matrix itself, since we need
        not retain the original matrix here. Thus, the governing equation now becomes:
            grid(i,j) = grid(i,j) + min(grid(i+1,j), grid(i,j+1))
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if i == j == 0:
                continue
            elif not i:
                grid[i][j] += grid[i][j - 1]
            elif not j:
                grid[i][j] += grid[i - 1][j]
            else:
                grid[i][j] += min(grid[i][j - 1], grid[i - 1][j])
    return grid[n - 1][m - 1]


class Test(unittest.TestCase):
    data = [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7)]

    def test_min_path_sum(self):
        for test_grid, result in self.data:
            self.assertEqual(result, min_path_sum_v1(test_grid))
            self.assertEqual(result, min_path_sum_v2(test_grid))


if __name__ == '__main__':
    unittest.main()
