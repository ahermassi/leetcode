""" A robot is located at the top-left corner of a m x n grid (marked 'Start' in the diagram below).
The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner
of the grid (marked 'Finish' in the diagram below).

How many possible unique paths are there? """

import unittest2 as unittest


def unique_paths_v1(m, n):
    """ Top down + memoization
        A key observation is that because paths must advance down or right, the number of ways to get to the
        bottom-right entry is the number of ways to get to the entry immediately above it, plus the number of ways to
        get to the entry immediately to its left.
        The idea is to notice that:
            When we are at cells (n - 2, m - 1) or (n - 1, m - 2), there is exactly only one way to reach bottom right
            corner, which is to either move down or right, respectively
        This is the base case.
        So if we know the number of ways to get to these points, then the total ways to get to the bottom right corner
        is the sum.
    Time complexity: O(n * m)
    Space complexity: O(n * m)
    """

    def helper(i, j):
        if not 0 <= i < n or not 0 <= j < m:
            return 0
        if (i, j) in {(n - 1, m - 2), (n - 2, m - 1), (n - 1, m - 1)}:
            return 1
        if (i, j) not in memo:
            res = helper(i + 1, j) + helper(i, j + 1)
            memo[(i, j)] = res
        return memo[(i, j)]

    memo = {}
    return helper(0, 0)


def unique_paths_v2(m, n):
    """ Bottom-up dynamic programming.
        Let dp[i][j] be the number of unique ways we can reach the current cell (i, j) moving only right and/or down
        and starting from top-left corner cell (0, 0). Therefore, dp[i][j] is the sum of unique ways we can reach
        the left cell (i, j-1) and top cell (i-1, j) (since starting from left and top, we can move right and down,
        respectively, to arrive at (i,j)).
            dp[i][j] = dp[i][j-1] + dp[i-1][j]
        The first column and first row must be 1's since there is only one path to get there (i.e. to get anywhere in
        the first row we must have just done all right moves, and similarly for the first column we must have just done
        all down moves).
    Time complexity: O(n * m)
    Space complexity: O(n * m)
    """
    dp = [[1 for _ in range(m)] for _ in range(n)]
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i][j - 1] + dp[i - 1][j]
    return dp[n-1][m-1]  # This is the bottom-right corner where we want to stop

# For more details about the 1D optimization: https://leetcode.com/problems/unique-paths/discuss/22954/C%2B%2B-DP


def unique_paths_v3(m, n):
    """ Bottom-up dynamic programming using 1D array.
        Notice that each time when we update dp[i][j], we only need dp[i-1][j] (at the previous row) and dp[i][j-1]
        (at the current row but previous column). We only need to store the previous row/column to perform the
        calculation for the current one. So a 1D array would suffice.
    Time complexity: O(n * m)
    Space complexity: O(m)
    """
    # pre, cur = [1] * m, [1] * m
    # for i in range(n):
    #     for j in range(m):
    #         cur[j] = pre[j] + cur[j-1]  pre[j] is above cell (in the previous row), cur[j-1] is previous/left column
    #     swap(pre, cur)
    # return pre[-1]
    # Further inspecting the above code, pre[j] is just the cur[j] before the update. So we can further reduce the
    # memory usage to one row.
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

