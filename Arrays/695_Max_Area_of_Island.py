""" Given a non-empty 2D array grid of 0's and 1's, an island is a group of 1's (representing land) connected
4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.
Find the maximum area of an island in the given 2D array. (If there is no island, the maximum area is 0.) """

import unittest2 as unittest


def max_area_of_island_v1(grid):
    """ We want to know the area of each connected shape in the grid, then take the maximum of these.
        If we are on a land square and explore every square connected to it 4-directionally (and recursively squares
        connected to those squares, and so on), then the total number of squares explored will be the area of that
        connected shape.
        To ensure we don't count squares in a shape more than once, let's use 'visited' set to keep track of squares
        we have visited before. It will also prevent us from counting the same shape more than once.
    Time complexity: O(N * M) where N is the number of rows in the given grid and M is the number of columns. We visit
    every square once.
    Space complexity: O(N * M) for both visited set and recursion call stack
    """

    def helper(i, j):
        if not 0 <= i < n or not 0 <= j < m or (i, j) in visited or grid[i][j] == 0:
            return 0
        visited.add((i, j))
        area = 1
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            area += helper(x, y)
        return area

    n, m = len(grid), len(grid[0])
    visited, res = set(), 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1 and (i, j) not in visited:
                area = helper(i, j)
                res = max(res, area)
    return res


def max_area_of_island_v2(grid):
    """ We can try the same approach using a stack-based, (or iterative) DFS.
        Here, 'visited' set will represent squares that have either been visited or are added to our list of squares
        to visit (stack). For every starting land square that hasn't been visited, we will explore 4-directionally
        around it, adding land squares that haven't been added to 'visited' to our stack.
        On the side, we'll keep a count 'area' of the total number of squares seen during the exploration of this shape.
        We'll want the running max of these counts.
    Time complexity: O(N * M)
    Space complexity: O(N * M), the space used by 'visited' to keep track of visited squares and the space used by stack
    """
    n, m = len(grid), len(grid[0])
    visited, res = set(), 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1 and (i, j) not in visited:
                area = 0
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    if not 0 <= x < n or not 0 <= y < m or (x, y) in visited or grid[x][y] == 0:
                        continue
                    area += 1
                    visited.add((x, y))
                    stack.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])
                res = max(res, area)
    return res


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
            self.assertEqual(result, max_area_of_island_v2(test_grid))


if __name__ == '__main__':
    unittest.main()
