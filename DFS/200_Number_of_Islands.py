""" Given a 2d grid map of '1's (land) and '0's (water), count the number of islands. An island is surrounded by
water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the
grid are all surrounded by water. """

import unittest2 as unittest


def num_islands_v1(grid):
    """ Iterate through each of the cell and if it is an island, do dfs to mark all adjacent islands, then increase
        the counter by 1.
        This solution uses a 'visited' set in order to avoid an infinite recursion.
        This is DFS because the recursive call happens before finishing the current execution.
    Time complexity: O(N * M) where N is the number of rows in the given grid and M is the number of columns. We visit
    every square once.
    Space complexity: O(N * M) for both 'visited' set and recursion call stack
    """
    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < m or (i, j) in visited or grid[i][j] == '0':
            return
        visited.add((i, j))
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            dfs(x, y)

    if not grid:
        return 0
    n, m, res = len(grid), len(grid[0]), 0
    visited = set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1' and (i, j) not in visited:
                dfs(i, j)
                res += 1
    return res


def num_islands_v2(grid):
    """ Same solution as above, but without using a 'seen' set. Instead, mark every visited cell as '0'.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    def dfs(i, j):
        if i < 0 or i >= row or j < 0 or j >= col or grid[i][j] == '0':
            return
        grid[i][j] = '0'
        dfs(i - 1, j)
        dfs(i + 1, j)
        dfs(i, j - 1)
        dfs(i, j + 1)

    if not grid:
        return 0
    count, seen = 0, set()
    row, col = len(grid), len(grid[0])
    for i in range(row):
        for j in range(col):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    return count


class Test(unittest.TestCase):
    data = [([['1', '1', '1', '1', '0'], ['1', '1', '0', '1', '0'], ['1', '1', '0', '0', '0'],
              ['0', '0', '0', '0', '0']], 1)]

    def test_num_islands(self):
        for test_island, result in self.data:
            self.assertEqual(result, num_islands_v1(test_island))
            self.assertEqual(result, num_islands_v2(test_island))


if __name__ == '__main__':
    unittest.main()
