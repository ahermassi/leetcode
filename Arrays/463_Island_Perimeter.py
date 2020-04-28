""" You are given a map in form of a two-dimensional integer grid where 1 represents land and 0 represents water.
Grid cells are connected horizontally/vertically (not diagonally). The grid is completely surrounded by water, and
there is exactly one island (i.e., one or more connected land cells).
Determine the perimeter of the island.
 """

import unittest2 as unittest


def island_perimeter_v1(grid):
    """ For each cell with land on it, add the number of cells around it that have water. All cells that are not on
        the grid are also considered to have water.
    Time complexity: O(N * M), where N is the length of grid and M is the width grid
    Space complexity: O(1)
    """
    n, m, res = len(grid[0]), len(grid), 0
    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    if not 0 <= x < n or not 0 <= y < m or not grid[x][y]:
                        res += 1
    return res


def island_perimeter_v2(grid):
    """ Loop over the matrix and count the number of land cells. If the current cell is a land, count if it has any
        neighbors. The result is land * 4 - neighbors, since a neighbor subtracts a side from the perimeter.
        +--+     +--+              +--+--+
        |  |  +  |  |     ->       |     |
        +--+     +--+              +--+--+
         4     +   4      - 2    =    6
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m = len(grid), len(grid[0])
    land = neighbors = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                land += 1
                for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    if 0 <= x < n and 0 <= y < m and grid[x][y]:
                        neighbors += 1
    return land * 4 - neighbors


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
