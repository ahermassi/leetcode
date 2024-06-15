""" You are given a map in form of a two-dimensional integer grid where 1 represents land and 0 represents water.
Grid cells are connected horizontally/vertically (not diagonally). The grid is completely surrounded by water, and
there is exactly one island (i.e., one or more connected land cells).
Determine the perimeter of the island.
 """

import unittest2 as unittest


def island_perimeter_v1(grid):
    """ For each land cell, add the number of cells around it that have water. All cells that are not on
         the grid are also considered to have water.

    Time complexity: O(N * M), where N is the length of grid and M is the grid width
    Space complexity: O(1)
    """
    n, m, res = len(grid), len(grid[0]), 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                sides = 0
                for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    if not 0 <= x < n or not 0 <= y < m or grid[x][y] == 0:
                        sides += 1
                res += sides
    return res


def island_perimeter_v2(grid):
    """ Loop over the matrix and locate the land cells. A land cell without any surrounding land cells will have a
        perimeter of 4.

         For each land, count the number of its land neighbors and subtract 1 for each surrounding land cell because the
         common side between current cell and its neighbor doesn't count in perimeter.

    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m, res = len(grid), len(grid[0]), 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                cell_perimeter = 4
                for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    if 0 <= x < n and 0 <= y < m and grid[x][y] == 1:
                        cell_perimeter -= 1
                res += cell_perimeter
    return res


class Test(unittest.TestCase):
    data = [([[0, 1, 0, 0],
              [1, 1, 1, 0],
              [0, 1, 0, 0],
              [1, 1, 0, 0]],
             16)]

    def test_island_perimeter(self):
        for test_grid, result in self.data:
            self.assertEqual(result, island_perimeter_v1(test_grid))
            self.assertEqual(result, island_perimeter_v2(test_grid))


if __name__ == '__main__':
    unittest.main()
