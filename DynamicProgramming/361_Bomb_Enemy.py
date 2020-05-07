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


class Test(unittest.TestCase):
    data = [([['0', 'E', '0', '0'], ['E', '0', 'W', 'E'], ['0', 'E', '0', '0']], 3)]

    def test_increasing_triplet(self):
        for test_grid, result in self.data:
            self.assertEqual(result, max_killed_enemies_v1(test_grid))


if __name__ == '__main__':
    unittest.main()
