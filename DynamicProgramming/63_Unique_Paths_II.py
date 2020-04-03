""" A robot is located at the top-left corner of a m x n grid.
The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner
of the grid.
Now consider if some obstacles are added to the grids. How many unique paths would there be? """

import unittest2 as unittest


def unique_paths_with_obstacles_v1(obstacle_grid):
    """ This problem is similar to 62- Unique Paths. The introduction of obstacles only changes the boundary conditions
        and makes some points unreachable (simply set to 0).
        The robot can only move either down or right. Hence any cell in the first row can only be reached from the cell
        left to it. Similarly, any cell in the first column can only be reached from the cell above it. If any cell has
        an obstacle, we won't let that cell contribute to any path.
        Let dp[i][j] be the number of paths to arrive at point (i, j). The state equation is:
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1] if obstacle_grid[i][j] != 1 and 0 otherwise
        Now let's finish the boundary conditions. In the Unique Paths problem, we initialize dp[0][j] = 1, dp[i][0] = 1
        for all valid i, j. Now, due to obstacles, some boundary points are no longer reachable and need to be
        initialized to 0. For example, if obstacle_grid is [0, 0, 1, 0, 0], then the last three points are not
        reachable and need to be initialized to be 0. The result is [1, 1, 0, 0, 0].
        If the first cell i.e. obstacle_grid[0][0] contains 1, this means there is an obstacle in the first cell.
        Hence, the robot won't be able to make any move and we would return the number of ways as 0.
        Iterate the first row. If a cell originally contains a 1, this means the current cell has an obstacle and
        shouldn't contribute to any path. Hence, set the value of that cell to 0. Otherwise, set it to the value of
        previous cell i.e. dp[0][j] = dp[0][j-1]
        Iterate the first column. If a cell originally contains a 1, this means the current cell has an obstacle and
        shouldn't contribute to any path. Hence, set the value of that cell to 0. Otherwise, set it to the value of
        previous cell i.e. dp[i][0] = dp[i-1][0]
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    if obstacle_grid[0][0]:  # If the starting cell has an obstacle, then simply return as there would be no paths to
        # the destination.
        return 0
    n, m = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[1] * m for _ in range(n)]
    for j in range(1, m):
        dp[0][j] = dp[0][j - 1] * (1 - obstacle_grid[0][j])
    for i in range(1, n):
        dp[i][0] = dp[i - 1][0] * (1 - obstacle_grid[i][0])
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1] if not obstacle_grid[i][j] else 0
    return dp[-1][-1]


def unique_paths_with_obstacles_v2(obstacle_grid):
    """ Same as previous solution, but with a cool trick to handle all edge cases in a more elegant way.
        We use a DP array with one extra row and one extra column such as dp[i][j] relates to obstacle_grid[i-1][j-1]
        and dp[1][1] is the starting point. We set dp[0][1] = 1 to make dp[1][1] (starting point) equal to 1 if
        obstacle[0][0] is not 1 and make it 0 otherwise. This is also equivalent to setting dp[1][0] = 1 because we
        can only arrive at dp[1][1] from dp[0][1] or dp[1][0].
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][1] = 1  # Or dp[1][0] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1] if not obstacle_grid[i - 1][j - 1] else 0
    return dp[-1][-1]


def unique_paths_with_obstacles_v3(obstacle_grid):
    """ We can use the obstacle_grid array as the DP array thus not utilizing any additional space.
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m = len(obstacle_grid), len(obstacle_grid[0])
    obstacle_grid[0][0] = 1 - obstacle_grid[0][0]
    for j in range(1, m):
        obstacle_grid[0][j] = obstacle_grid[0][j - 1] * (1 - obstacle_grid[0][j])
    for i in range(1, n):
        obstacle_grid[i][0] = obstacle_grid[i - 1][0] * (1 - obstacle_grid[i][0])
    for i in range(1, n):
        for j in range(1, m):
            obstacle_grid[i][j] = obstacle_grid[i - 1][j] + obstacle_grid[i][j - 1] if not obstacle_grid[i][j] else 0
    return obstacle_grid[-1][-1]


class Test(unittest.TestCase):
    data = [([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2)]

    def test_unique_paths_with_obstacles(self):
        for test_obstacle_grid, result in self.data:
            self.assertEqual(result, unique_paths_with_obstacles_v1(test_obstacle_grid))
            self.assertEqual(result, unique_paths_with_obstacles_v3(test_obstacle_grid))


if __name__ == '__main__':
    unittest.main()
