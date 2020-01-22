""" Given a non-empty 2D array grid of 0's and 1's, an island is a group of 1's (representing land) connected
4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.
Count the number of distinct islands. An island is considered to be the same as another if and only if one island can
be translated (and not rotated or reflected) to equal the other. """

import unittest2 as unittest


def num_distinct_islands_v1(grid):
    """ At the beginning, we need to find every island, which we can do using a straightforward depth-first search.
        The hard part is deciding whether two islands are the same.
        Since two islands are the same if one can be translated to match another, the path taken by our depth-first
        search will be the same if and only if the shape is the same. We can exploit this by recording the path we
        take as our shape - keeping in mind to record both when we enter and when we exit the function.
        DO NOT FORGET to add exit state, otherwise a different shape can have the same path:
        Example:              1 1 1   and    1 1 0
                              0 1 0          0 1 1
        With exit state:      rdbr           rdr
        Without exit state:   rdr            rdr
        We need to record when we 'hit a wall' and return.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def dfs(i, j, path, dir):
        if not 0 <= i < n or not 0 <= j < m or (i, j) in visited or not grid[i][j]:
            return
        visited.add((i, j))
        path.append(dir)
        dfs(i - 1, j, path, 'u')
        dfs(i + 1, j, path, 'd')
        dfs(i, j - 1, path, 'l')
        dfs(i, j + 1, path, 'r')
        path.append('b')  # Record the exit

    n, m, res, visited = len(grid), len(grid[0]), set(), set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] and (i, j) not in visited:
                path = []
                dfs(i, j, path, 'o')  # Record the origin
                res.add(tuple(path))
    return len(res)


def num_distinct_islands_v2(grid):
    """ The shape of the island can be represented by taking the relative position of the connected cells from the
        leftmost cell on the top row of the island (the first cell of each island we will visit). For each island we
        visit, we are guaranteed to visit the top row's leftmost cell first if we iterate the matrix row by row, left
        to right direction. We will get the same order of cells for islands of the same shape if we perform the search
        in a consistent manner.
        Example:
        11000
        10000
        00110
        00100
        The first island:
            11
            1
            [(0,0), (0,1), (1,0)] - (0,0) = [(0,0), (0,1), (1,0)]
        islands = set( '[(0,0), (0,1), (1,0)] ' )
        The second island:(the same one)
            [(2,2), (2,3), (3,2)] - (2,2) = [(0,0), (0,1), (1,0)]
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def dfs(i, j, origin_i, origin_j, path):
        if not 0 <= i < n or not 0 <= j < m or (i, j) in visited or not grid[i][j]:
            return
        visited.add((i, j))
        path.append((i - origin_i, j - origin_j))
        dfs(i - 1, j, origin_i, origin_j, path)
        dfs(i + 1, j, origin_i, origin_j, path)
        dfs(i, j - 1, origin_i, origin_j, path)
        dfs(i, j + 1, origin_i, origin_j, path)

    n, m, res, visited = len(grid), len(grid[0]), set(), set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] and (i, j) not in visited:
                path = []
                dfs(i, j, i, j, path)
                res.add(tuple(path))
    return len(res)


class Test(unittest.TestCase):
    data = [([[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]], 1)]

    def test_num_distinct_islands(self):
        for test_grid, result in self.data:
            self.assertEqual(result, num_distinct_islands_v1(test_grid))
            self.assertEqual(result, num_distinct_islands_v2(test_grid))


if __name__ == '__main__':
    unittest.main()
