""" A robot is located at the top-left corner of a m x n grid.
The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner
of the grid.
Now consider if some obstacles are added to the grids. How many unique paths would there be? """

import unittest2 as unittest


# Video explanation: https://youtu.be/d3UOz7zdE4I
def unique_paths_with_obstacles_v1(obstacle_grid):
    """ Top-Down Dynamic Programming.

         A key observation is that since paths must advance down or right, the number of ways to get to the
         bottom-right corner is the number of ways to get to the cell immediately above it, plus the number of ways to
         get to the cell immediately to its left.

         The idea is to notice that:

                When we are at cell (n - 2, m - 1) or at cell (n - 1, m - 2), there is exactly only one way to reach the
                bottom -right corner, which is to either move down or right, respectively

         This is the base case.
         So if we know the number of ways to get to these cells, the total ways to get to the bottom-right corner
         is their sum.

         This is identical to 62- Unique Paths solution, except that a second base case is needed. If at any time we
         reach a cell with value 1, then it is an obstacle cell, and we can't move any further. So, we just stop
         exploring further paths from this cell.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def dfs(i, j):
        # dfs(i, j) returns the number of unique paths from cell (i, j) to the bottom-right corner
        if obstacle_grid[i][j] == 1:
            return 0
        if (i, j) == (m - 1, n - 1):
            return 1
        if (i, j) in {(n - 1, m - 2), (n - 2, m - 1)}:
            return 1
        if (i, j) in memo:
            return memo[(i, j)]
        right_paths = down_paths = 0
        if j < n - 1:
            right_paths = dfs(i, j + 1)
        if i < m - 1:
            down_paths = dfs(i + 1, j)
        memo[(i, j)] = right_paths + down_paths
        return memo[(i, j)]

    m, n = len(obstacle_grid), len(obstacle_grid[0])
    if obstacle_grid[m - 1][n - 1] == 1:
        return 0
    memo = {}
    return dfs(0, 0)


def unique_paths_with_obstacles_v2(obstacle_grid):
    """ Bottom-Up Dynamic Programming.

         Similar to 62- Unique Paths. The introduction of obstacles only changes the boundary conditions and makes some
         cells unreachable.

         A cell (i,j) can be reached either from (i−1,j) or (i,j−1), and thus the number of unique paths to (i,j) is the
         sum of the number of unique paths to these two cells.

         For any other cell in the grid, we can reach it either from the cell to left of it or the cell above it. If any
         cell has an obstacle, we won't let that cell contribute to any path.

         We iterate the grid from left-to-right and top-to-bottom. Thus, before reaching any cell we would have the
         number of ways of reaching the predecessor cells.

         The robot can only move either down or right. Hence, any cell in the first row can only be reached from the
         cell to its left to. Similarly, any cell in the first column can only be reached from the cell above it. If any
         cell has an obstacle, we won't let that cell contribute to any path.

         Let dp[i][j] be the number of unique paths to reach cell (i, j) moving only right and/or down and starting
         from top-left corner cell (0, 0). Therefore, dp[i][j] is the sum of unique paths to reach the left cell (i, j-1)
         and the top cell (i-1, j). However, this is only true if the cell (i, j) does not have an obstacle. If it does,
         then the number of ways to reach this cell is 0 because it's inaccessible.

                dp[i][j] = dp[i - 1][j] + dp[i][j - 1] if obstacle_grid[i][j] != 1; 0 otherwise

         Now let's finish the boundaries' initialization. In 62- Unique Paths, we set dp[0][j] = 1, dp[i][0] = 1
         for all valid i, j. However, due to obstacles, some boundary points are no longer reachable and need to be
         initialized to 0. For example, if obstacle_grid is [0, 0, 1, 0, 0], then the last three points are not
         reachable and need to be initialized to be 0. The result is [1, 1, 0, 0, 0].

         If the first cell obstacle_grid[0][0] contains 1, this means there is an obstacle in the first cell. Hence, the
         robot won't be able to make any move, and we would return the number of paths as 0.

         Iterate over the first row. If a cell originally contains a 1, this means the current cell has an obstacle and
         shouldn't contribute to any path. Hence, set the value of that cell to 0. Otherwise, set it to the value of
         previous cell i.e. dp[0][j] = dp[0][j-1].

         Iterate over the first column. If a cell originally contains a 1, this means the current cell has an obstacle
         and shouldn't contribute to any path. Hence, set the value of that cell to 0. Otherwise, set it to the value of
         previous cell i.e. dp[i][0] = dp[i-1][0].

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    if obstacle_grid[0][0] == 1:
        # If the starting cell has an obstacle, then simply return as there would be no paths to the destination.
        return 0
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for i in range(1, m):
        if obstacle_grid[i][0] != 1:
            dp[i][0] = dp[i - 1][0]
    for j in range(1, n):
        if obstacle_grid[0][j] != 1:
            dp[0][j] = dp[0][j - 1]
    for i in range(1, m):
        for j in range(1, n):
            if obstacle_grid[i][j] != 1:
                dp[i][j] = dp[i][j - 1] + dp[i - 1][j]
    return dp[m - 1][n - 1]  # This is the bottom-right corner where we want to stop


def unique_paths_with_obstacles_v3(obstacle_grid):
    """ Same as previous solution, but with a cool trick to handle all edge cases in a more elegant way.

         We use a DP array with one extra row and one extra column such as dp[i][j] relates to obstacle_grid[i-1][j-1]
         and dp[1][1] is the starting point. We set dp[0][1] = 1 to make dp[1][1] (starting point) equal to 1 if
         obstacle_grid[0][0] is not an obstacle and make it 0 otherwise. This is also equivalent to setting dp[1][0] = 1
         because we can only reach dp[1][1] from dp[0][1] or dp[1][0].

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][1] = 1  # Or dp[1][0] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if obstacle_grid[i][j] != 1:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[-1][-1]


def unique_paths_with_obstacles_v4(obstacle_grid):
    """ Space-optimized Bottom-Up Dynamic Programming.

         Notice that each time when we update dp[i][j], we only need dp[i-1][j] (in the previous row) and dp[i][j-1]
         (in the current row but previous column). We only need to store the previous row/column to perform the
         calculation for the current one. So a 1D array would suffice.

         pre is analogous to dp[i-1] and cur is analogous to dp[i].

    Time complexity: O(N * M)
    Space complexity: O(M)
    """
    if obstacle_grid[0][0] == 1:
        return 0
    n, m = len(obstacle_grid), len(obstacle_grid[0])
    pre, cur = [0] * m, [0] * m
    pre[0] = 1
    for j in range(1, m):
        # Populating the first row
        if obstacle_grid[0][j] != 1:
            pre[j] = pre[j - 1]
    for i in range(1, n):
        if obstacle_grid[i][0] != 1:
            # Edge case j=0, the result depends only on the above cell pre[0]
            cur[0] = pre[0]
        for j in range(1, m):
            if obstacle_grid[i][j] != 1:
                cur[j] = cur[j - 1] + pre[j]
        pre, cur = cur, [0] * m
    return pre[-1]


def unique_paths_with_obstacles_v5(obstacle_grid):
    """ We can use the obstacle_grid array as the DP array thus not utilizing any additional space.

    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    if obstacle_grid[0][0] == 1:
        return 0
    n, m = len(obstacle_grid), len(obstacle_grid[0])
    obstacle_grid[0][0] = 1
    for i in range(1, n):
        obstacle_grid[i][0] = obstacle_grid[i - 1][0] if obstacle_grid[i][0] != 1 else 0
    for j in range(1, m):
        obstacle_grid[0][j] = obstacle_grid[0][j - 1] if obstacle_grid[0][j] != 1 else 0
    for i in range(1, n):
        for j in range(1, m):
            obstacle_grid[i][j] = obstacle_grid[i - 1][j] + obstacle_grid[i][j - 1] if obstacle_grid[i][j] != 1 else 0
    return obstacle_grid[-1][-1]


class Test(unittest.TestCase):
    data = [([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2)]

    def test_unique_paths_with_obstacles(self):
        for test_obstacle_grid, result in self.data:
            self.assertEqual(result, unique_paths_with_obstacles_v1(test_obstacle_grid))
            self.assertEqual(result, unique_paths_with_obstacles_v2(test_obstacle_grid))
            self.assertEqual(result, unique_paths_with_obstacles_v3(test_obstacle_grid))
            self.assertEqual(result, unique_paths_with_obstacles_v4(test_obstacle_grid))


if __name__ == '__main__':
    unittest.main()
