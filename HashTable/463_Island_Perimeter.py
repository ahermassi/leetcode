""" You are given a map in form of a two-dimensional integer grid where 1 represents land and 0 represents water.
Grid cells are connected horizontally/vertically (not diagonally). The grid is completely surrounded by water, and
there is exactly one island (i.e., one or more connected land cells).
Determine the perimeter of the island.
 """

import unittest2 as unittest


def island_perimeter(grid):
    """ For each cell with land on it, add the number of cells around it that have water. All cells that are not on
        the grid are also considered to have water.
    Time complexity: O(N * M), where N is the length of grid and M is the length of grid[0]
    Space complexity: O(1)
    """
    width, height = len(grid[0]), len(grid)

    def sum_adjacent(i, j):
        adjacent = [(i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)]  # These correspond to top, bottom, left, right
        res = 0
        for x, y in adjacent:
            if x < 0 or y < 0 or x == height or y == width or grid[x][y] == 0:
                res += 1
        return res

    count = 0
    for i in range(height):
        for j in range(width):
            if grid[i][j] == 1:
                count += sum_adjacent(i, j)
    return count


class Test(unittest.TestCase):
    data = [([[0, 1, 0, 0],
              [1, 1, 1, 0],
              [0, 1, 0, 0],
              [1, 1, 0, 0]],
             16)]

    def test_island_perimeter(self):
        for test_grid, result in self.data:
            self.assertEqual(result, island_perimeter(test_grid))


if __name__ == '__main__':
    unittest.main()
