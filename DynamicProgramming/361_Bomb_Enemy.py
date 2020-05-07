""" Given a 2D grid, each cell is either a wall 'W', an enemy 'E' or empty '0' (the number zero), return the maximum
enemies you can kill using one bomb.
The bomb kills all the enemies in the same row and column from the planted point until it hits the wall since the wall
is too strong to be destroyed.
Note: You can only put the bomb at an empty cell. """

import unittest2 as unittest


def max_killed_enemies_v1(grid):
    """ The brute force solution is very intuitive. Just count 'E's in rows and cols for each 0 in the matrix and
        return the maximum.
    Time complexity: O(N * M * (M + N)), as we have to traverse up, down, left, and right for every (i, j)
    Space complexity: O(1)
    """

    def bomb(i, j):
        killed = 0
        x, y = i - 1, j
        while 0 <= x < n and 0 <= y < m and grid[x][y] != 'W':
            killed += grid[x][y] == 'E'
            x -= 1
        x, y = i + 1, j
        while 0 <= x < n and 0 <= y < m and grid[x][y] != 'W':
            killed += grid[x][y] == 'E'
            x += 1
        x, y = i, j - 1
        while 0 <= x < n and 0 <= y < m and grid[x][y] != 'W':
            killed += grid[x][y] == 'E'
            y -= 1
        x, y = i, j + 1
        while 0 <= x < n and 0 <= y < m and grid[x][y] != 'W':
            killed += grid[x][y] == 'E'
            y += 1
        return killed

    if not grid:
        return 0
    n, m, res = len(grid), len(grid[0]), 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '0':
                res = max(res, bomb(i, j))
    return res


def max_killed_enemies_v2(grid):
    """ Walk through the matrix. At the START of each non-wall-streak (row-wise or column-wise), count the number of
        hits in that streak and remember it. As we are traversing along the row, the enemies killed between any walls,
        denoted by 'row_hits', is same, but that's not the case with columns because as we traverse a particular row
        our columns keep on changing. This is the reason we need to track the number of enemies killed in each column
        using an array 'col_hits'. Even for columns, the enemies killed between walls is same, so we need to
        recalculate only if the previous column was a wall. So for each row, we visit each column once. Once we visit
        second row (and other rows too), we don't want to recompute for columns unless the above column is a wall.
        It is a DP-like solution, where 'col_hits' is storing column enemies count and is only updated once for
        consecutive enemies column and reused for later calculation.
    Time complexity: O(N * M)
    Space complexity: O(M)
    """
    if not grid:
        return 0
    n, m, res = len(grid), len(grid[0]), 0
    row_hits, col_hits = 0, [0] * m
    for i in range(n):
        for j in range(m):
            if j == 0 or grid[i][j - 1] == 'W':
                row_hits = 0
                k = j
                while k < m and grid[i][k] != 'W':
                    row_hits += grid[i][k] == 'E'
                    k += 1
            if i == 0 or grid[i - 1][j] == 'W':
                col_hits[j] = 0
                k = i
                while k < n and grid[k][j] != 'W':
                    col_hits[j] += grid[k][j] == 'E'
                    k += 1
            if grid[i][j] == '0':
                res = max(res, row_hits + col_hits[j])
    return res


class Test(unittest.TestCase):
    data = [([['0', 'E', '0', '0'], ['E', '0', 'W', 'E'], ['0', 'E', '0', '0']], 3)]

    def test_max_killed_enemies(self):
        for test_grid, result in self.data:
            self.assertEqual(result, max_killed_enemies_v1(test_grid))
            self.assertEqual(result, max_killed_enemies_v2(test_grid))


if __name__ == '__main__':
    unittest.main()
