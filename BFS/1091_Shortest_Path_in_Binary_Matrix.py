""" In an N by N square grid, each cell is either empty (0) or blocked (1).
A clear path from top-left to bottom-right has length k if and only if it is composed of cells C_1, C_2, ..., C_k such
that:
Adjacent cells C_i and C_{i+1} are connected 8-directionally (ie., they are different and share an edge or corner)
C_1 is at location (0, 0) (ie. has value grid[0][0])
C_k is at location (N-1, N-1) (ie. has value grid[N-1][N-1])
If C_i is located at (r, c), then grid[r][c] is empty (ie. grid[r][c] == 0).
Return the length of the shortest such clear path from top-left to bottom-right.  If such a path does not exist,
return -1. """

from collections import deque
import unittest2 as unittest


def shortest_path_binary_matrix_v1(grid):
    """ Do a breadth first search to find the shortest path.
        Using DFS can help us determine if there is a path from source to destination. However, the time complexity is
        terrible. We may not get the shortest path if we use DFS, we might end up with just some path. Also, using DFS
        in this particular problem will lead to TLE. DFS does not guarantee that if node 1 is visited before another
        node 2 starting from a source vertex, then node 1 is closer to the source than node 2. Hence, BFS is our best
        shot since it goes from level to level from source to destination.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if grid[0][0] or grid[-1][-1]:
        return -1
    n, m = len(grid), len(grid[0])
    queue = deque([(0, 0, 1)])
    visited = {(0, 0)}
    while queue:
        i, j, distance = queue.popleft()
        if i == n - 1 and j == m - 1:
            return distance
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), \
                    (i + 1, j + 1):
            if not 0 <= x < n or not 0 <= y < m or grid[x][y] or (x, y) in visited:
                continue
            queue.append((x, y, distance + 1))
            visited.add((x, y))
    return -1


def shortest_path_binary_matrix_v2(grid):
    """ If we're allowed to modify the grid, we can securely set the visited cells as non-empty to avoid revisiting
        without using a 'visited' set.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if grid[0][0] or grid[-1][-1]:
        return -1
    n, m = len(grid), len(grid[0])
    queue = deque([(0, 0, 1)])
    while queue:
        i, j, distance = queue.popleft()
        if i == n - 1 and j == m - 1:
            return distance
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), \
                    (i + 1, j + 1):
            if not 0 <= x < n or not 0 <= y < m or grid[x][y]:
                continue
            queue.append((x, y, distance + 1))
            grid[x][y] = 1  # Mark the cell visited
    return -1


class Test(unittest.TestCase):
    data = [([[0, 1], [1, 0]], 2), ([[0, 0, 0], [1, 1, 0], [1, 1, 0]], 4)]

    def test_shortest_path_binary_matrix(self):
        for test_grid, result in self.data:
            self.assertEqual(result, shortest_path_binary_matrix_v1(test_grid))
            self.assertEqual(result, shortest_path_binary_matrix_v2(test_grid))


if __name__ == '__main__':
    unittest.main()
