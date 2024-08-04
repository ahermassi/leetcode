""" A robot is located at the top-left corner of a m x n grid (marked 'Start' in the diagram below).
The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner
of the grid (marked 'Finish' in the diagram below).

How many possible unique paths are there? """

import unittest2 as unittest


def unique_paths_v1(m, n):
    """ Top- Down + Dynamic Programming

         A key observation is that since paths must advance down or right, the number of ways to get to the
         bottom-right corner is the number of ways to get to the cell immediately above it, plus the number of ways to
         get to the cell immediately to its left.

         The idea is to notice that:

                When we are at cell (n - 2, m - 1) or at cell (n - 1, m - 2), there is exactly only one way to reach the
                bottom -right corner, which is to either move down or right, respectively

         This is the base case.
         So if we know the number of ways to get to these cells, the total ways to get to the bottom-right corner
         is their sum.

    Time complexity: O(n * m)
    Space complexity: O(n * m)
    """

    def dfs(i, j):
        # dfs(i, j) returns the number of unique paths from cell (i, j) to the bottom-right corner
            if (i, j) == (m - 1, n - 1):
                return 1
            if (i, j) in {(n - 1, m - 2), (n - 2, m - 1)}:
                return 1
            if (i, j) in memo:
                return memo[(i, j)]
            right_paths = down_paths = 0
            if j < n - 1:
                right_paths = dfs(i, j+1)
            if i < m - 1:
                down_paths = dfs(i+1, j)
            memo[(i, j)] = right_paths + down_paths
            return memo[(i, j)]

    if n == 1 and m == 1:
        return 1
    memo = {}
    return dfs(0, 0)


# Video explanation: https://youtu.be/IlEsdxuD4lY
def unique_paths_v2(m, n):
    """ Bottom-Up Dynamic Programming.

         A cell (i,j) can be reached either from (i−1,j) or (i,j−1), and thus the number of unique paths to (i,j) is the
         sum of the number of unique paths to these two cells.

         Let dp[i][j] be the number of unique paths to reach cell (i, j) moving only right and/or down and starting
         from top-left corner cell (0, 0). Therefore, dp[i][j] is the sum of unique paths to reach the left cell
         (i, j-1) and the top cell (i-1, j):

                    dp[i][j] = dp[i][j-1] + dp[i-1][j]

        The first column and first row must be initialized to 1. The robot can move either down or right, so there is
        only one path to reach the cells in the first row: right->right->...->right. The same is valid for the first
        column, though the path here is down->down->...->down.

        Note that for simplicity, we could also initialize the entire DP array with 1's since dp[i][j]  depends only on
        the previously calculated cells.

    Time complexity: O(n * m)
    Space complexity: O(n * m)
    """
    dp = [[1] * n for _ in range(m)]
    # Alternatively:
    # dp = [[0] * n for _ in range(m)]
    # for i in range(m):
    #     dp[i][0] = 1
    # for j in range(n):
    #     dp[0][j] = 1
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i][j - 1] + dp[i - 1][j]
    return dp[m-1][n-1]  # This is the bottom-right corner where we want to stop


# For more details about the 1D optimization: https://leetcode.com/problems/unique-paths/discuss/22954/C%2B%2B-DP
def unique_paths_v3(m, n):
    """ Space-optimized Bottom-Up Dynamic Programming.

         Notice that each time when we update dp[i][j], we only need dp[i-1][j] (in the previous row) and dp[i][j-1]
         (in the current row but previous column). We only need to store the previous row/column to perform the
         calculation for the current one. So a 1D array would suffice.

    Time complexity: O(n * m)
    Space complexity: O(m)
    """
    pre, cur = [1] * n, [1] * n
    for i in range(m):
        for j in range(n):
            # pre[j] is above cell (in the previous row), cur[j-1] is previous/left column
            cur[j] = cur[j-1] + pre[j]
        pre, cur = cur, [1] * n
    # return pre[-1]
    # Notice that pre[j] is just cur[j] before the update, so we can further reduce the memory usage to one row.
    dp = [1] * m
    for i in range(1, n):
        for j in range(1, m):
            dp[j] = dp[j] + dp[j - 1]
    return dp[-1]


class Test(unittest.TestCase):
    data = [(3, 2, 3), (7, 3, 28)]

    def test_unique_paths(self):
        for test_m, test_n, result in self.data:
            self.assertEqual(result, unique_paths_v1(test_m, test_n))
            self.assertEqual(result, unique_paths_v2(test_m, test_n))
            self.assertEqual(result, unique_paths_v3(test_m, test_n))


if __name__ == '__main__':
    unittest.main()

