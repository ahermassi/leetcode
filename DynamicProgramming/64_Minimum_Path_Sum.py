""" Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right which minimizes the
sum of all numbers along its path.
Note: You can only move either down or right at any point in time. """

import unittest2 as unittest


def min_path_sum_v1(grid):
    """ Brute force. TLE

         The brute force approach involves recursion. For each element, we consider two paths, rightwards and downwards,
         and find the minimum sum out of those two. It specifies whether we need to take a right step or downward step
         to minimize the sum:

                    cost(i,j) = grid[i][j] + min(cost(i+1,j), cost(i,j+1))

    Time complexity: O(2^(N + M)), for every move we have at most 2 options
    Space complexity: O(N + M), for recursion stack
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < m:
            # Exclude the cell from consideration
            return float('inf')
        if (i, j) == (n - 1, m - 1):
            return grid[i][j]
        return grid[i][j] + min(dfs(i, j + 1), dfs(i + 1, j))

    n, m = len(grid), len(grid[0])
    return dfs(0, 0)


def min_path_sum_v2(grid):
    """ Bottom-Up Dynamic Programming. Similar to 62- Unique paths.

         Let dp[i][j] be the minimum sum of the path from the top-left cell to cell (i,j).

         We start by initializing the top left element of dp as the first element of the given matrix. Some boundary
         conditions need to be handled as well. These relate the topmost row and the leftmost column.
         Suppose the topmost row is like [1, 1, 1, 1], then the minimum sum to arrive at each point is simply the
         cumulative sum of the previous elements: [1, 2, 3, 4].

         Then for each element starting from the top left (excluding the first row and the first column), we traverse
         backwards the matrix and fill the required minimum sums. Now, we need to note that at every element, we
         could've arrived to that cell moving either rightwards or downwards. Therefore, the minimum sum at the current
         cell can be derived from the minimum path sum to reach the left cell (i, j-1) and the top cell (i-1, j):

                    dp[i][j]= grid[i][j] + min(dp[i-1][j], d[(i][j-1])

    Time complexity: O(N * M), we traverse the entire matrix once
    Space complexity: O(N * M)
    """
    n, m = len(grid), len(grid[0])
    dp = [[0] * m for _ in range(n)]
    dp[0][0] = grid[0][0]
    for i in range(1, n):
        dp[i][0] = grid[i][0] + dp[i - 1][0]
    for j in range(1, m):
        dp[0][j] = grid[0][j] + dp[0][j - 1]
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    return dp[n-1][m-1]


# Video explanation: https://youtu.be/pGMsrvt0fpk
def min_path_sum_v3(grid):
    """ Space-optimized Bottom-Up Dynamic Programming.

         Notice that each time we update dp[i][j], we only need dp[i-1][j] (at the previous row) and dp[i][j-1]
         (at the left column of same row). So we don't need to maintain the full dp matrix. Keeping two rows at each
         iteration is enough.

    Time complexity: O(N * M)
    Space complexity: O(M)
    """
    n, m = len(grid), len(grid[0])
    pre, cur = [0] * m, [0] * m
    pre[0] = grid[0][0]
    for j in range(1, m):  # Populating the first row as it is a special case because it has no previous row
        pre[j] = grid[0][j] + pre[j - 1]
    for i in range(1, n):
        cur[0] = grid[i][0] + pre[0]  # cur[j] has no left predecessor when j = 0
        for j in range(1, m):
            cur[j] = grid[i][j] + min(pre[j], cur[j - 1])
        pre, cur = cur, [0] * m
    return pre[-1]


def min_path_sum_v4(grid):
    """ Further inspecting the above code, it can be seen that maintaining 'pre' is for recovering pre[j], which is
        simply cur[j] before its update. So it is enough to use only one row. Now the space is further optimized.
    Time complexity: O(N * M)
    Space complexity: O(M)
    """
    n, m = len(grid), len(grid[0])
    cur = [0] * m
    cur[0] = grid[0][0]
    for j in range(1, m):
        cur[j] = grid[0][j] + cur[j - 1]
    for i in range(1, n):
        cur[0] += grid[i][0]
        for j in range(1, m):
            cur[j] = grid[i][j] + min(cur[j], cur[j - 1])
    return cur[-1]


def min_path_sum_v5(grid):
    """ Instead of using another dp matrix, we can store the minimum sums in the original matrix itself, since we don't
        need to retain the original matrix. Thus, the governing equation now becomes:
            grid(i,j) = grid(i,j) + min(grid(i-1,j), grid(i,j-1))
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m = len(grid), len(grid[0])
    for i in range(1, n):
        grid[i][0] += grid[i-1][0]
    for j in range(1, m):
        grid[0][j] += grid[0][j-1]
    for i in range(1, n):
        for j in range(1, m):
            grid[i][j] += min(grid[i-1][j], grid[i][j-1])
    return grid[-1][-1]


class Test(unittest.TestCase):
    data = [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7)]

    def test_min_path_sum(self):
        for test_grid, result in self.data:
            self.assertEqual(result, min_path_sum_v1(test_grid))
            self.assertEqual(result, min_path_sum_v2(test_grid))
            self.assertEqual(result, min_path_sum_v3(test_grid))
            self.assertEqual(result, min_path_sum_v4(test_grid))
            self.assertEqual(result, min_path_sum_v5(test_grid))


if __name__ == '__main__':
    unittest.main()
