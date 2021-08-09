""" Given a 2d grid map of '1's (land) and '0's (water), count the number of islands. An island is surrounded by
water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the
grid are all surrounded by water. """

from collections import deque
import unittest2 as unittest


def num_islands_v1(grid):
    """ Treat the 2d grid map as an undirected graph and there is an edge between two horizontally or vertically
        adjacent nodes of value '1'.
        Iterate through each of the cells, and if it is an island do DFS to mark all adjacent islands, then increase
        the counter by 1. This solution uses a 'visited' set in order to avoid an infinite recursion.
        Count the number of root nodes that trigger DFS, this number would be the number of islands since each DFS
        starting at some root identifies an island.
    Time complexity: O(N * M), where N is the number of rows in the given grid and M is the number of columns. We visit
    every square once.
    Space complexity: O(N * M), for both 'visited' set and recursion call stack
    """
    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < m or (i, j) in visited or grid[i][j] == '0':
            return
        visited.add((i, j))
        for x, y in directions:
            dfs(i+x, j+y)

    n, m, res, visited = len(grid), len(grid[0]), 0, set()
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1' and (i, j) not in visited:
                dfs(i, j)
                res += 1
    return res


def num_islands_v2(grid):
    """ Same solution as above but without using a 'visited' set. Instead, mark every visited cell as '0'. This is
        also known as 'sinking' the islands.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < m or grid[i][j] == '0':
            return
        grid[i][j] = '0'
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            dfs(x, y)

    if not grid:
        return 0
    n, m, res = len(grid), len(grid[0]), 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1':
                dfs(i, j)
                res += 1
    return res


def num_islands_v3(grid):
    """ BFS version.
        Linearly scan the 2D grid. If a node contains a '1', then it is a root node that triggers a Breadth First
        Search. Put it into a queue and and mark it as visited node. Iteratively search the neighbors of enqueued nodes
        until the queue becomes empty.
    Time complexity: O(N * M)
    Space complexity: not clear
    """
    if not grid:
        return 0
    n, m, res, visited = len(grid), len(grid[0]), 0, set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1' and (i, j) not in visited:
                queue = deque([(i, j)])
                while queue:
                    x, y = queue.popleft()
                    if not 0 <= x < n or not 0 <= y < m or (x, y) in visited or grid[x][y] == '0':
                        continue
                    visited.add((x, y))
                    queue.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])
                res += 1
    return res


class Test(unittest.TestCase):
    data = [([['1', '1', '1', '1', '0'], ['1', '1', '0', '1', '0'], ['1', '1', '0', '0', '0'],
              ['0', '0', '0', '0', '0']], 1)]

    def test_num_islands(self):
        for test_island, result in self.data:
            self.assertEqual(result, num_islands_v1(test_island))
            self.assertEqual(result, num_islands_v2(test_island))


if __name__ == '__main__':
    unittest.main()
