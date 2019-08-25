""" Given a non-empty 2D array grid of 0's and 1's, an island is a group of 1's (representing land) connected
4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.
Find the maximum area of an island in the given 2D array. (If there is no island, the maximum area is 0.) """

import unittest2 as unittest


def max_area_of_island_v1(grid):
    """ We want to know the area of each connected shape in the grid, then take the maximum of these.
        If we are on a land square and explore every square connected to it 4-directionally (and recursively squares
        connected to those squares, and so on), then the total number of squares explored will be the area of that
        connected shape.
        To ensure we don't count squares in a shape more than once, let's use seen to keep track of squares we haven't
        visited before. It will also prevent us from counting the same shape more than once.
    Time complexity: O(N * M) where N is the number of rows in the given grid and M is the number of columns. We visit
    every square once.
    Space complexity: O(N * M) for both visited set and recursion call stack
    """

    def area(x, y):
        if 0 <= x < rows and 0 <= y < cols and grid[x][y] and (x, y) not in visited:
            visited.add((x, y))
            return 1 + area(x - 1, y) + area(x + 1, y) + area(x, y - 1) + area(x, y + 1)
        return 0

    rows, cols, max_area, visited = len(grid), len(grid[0]), 0, set()
    for i in range(rows):
        for j in range(cols):
            if grid[i][j]:
                max_area = max(max_area, area(i, j))
    return max_area


class Test(unittest.TestCase):
    data = [([[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], 6)]

    def test_max_area_of_island(self):
        for test_grid, result in self.data:
            self.assertEqual(result, max_area_of_island_v1(test_grid))


if __name__ == '__main__':
    unittest.main()
