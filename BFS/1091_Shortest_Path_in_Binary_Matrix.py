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
    """ The grid is a graph, and we need to find the length of the shortest path from the top-left to the bottom-right
        cell. Finding the shortest path between two nodes in a graph is almost always done using BFS. BFS works by
        firstly identifying all of the nodes that can be reached in 1 step from the top-left cell, then those in 2
        steps, then 3 steps, etc., until it "finds" the target node (the bottom-right cell). We'll use a queue to
        keep track of cells that we have numbered but haven't yet numbered the *neighbors* of. We'd need a 'visited'
        set to avoid infinite looping around cycles.
        The simplest BFS variant is to put the distances on the queue, alongside the row and column (triplets instead
        of pairs).
        Exploring the cell's neighbors involves identifying all open cells adjacent to the current cell that still have
        a 0 in them. For each of these cells, we associate the (distance + 1) to them.
        We return -1 if the loop terminates without returning, as this means we ran out of cells to explore before
        reaching the bottom-right cell.
    Time complexity: O(N), where N is the number of cells in the grid. Each cell was guaranteed to be enqueued at most
    once. This is because a condition for a cell to be enqueued was that it had a zero in the grid, and when enqueuing,
    we also add the cell to the 'visited' set. The outer loop runs as long as there are still cells in the queue,
    dequeuing one each time. Therefore, it runs at most N times, giving a time complexity of O(N).
    Space complexity: O(N), given that BFS will have nodes of at most two unique distances on the queue at any one
    time, it would be reasonable to wonder if the worst-case space complexity is actually lower. But actually, it turns
    out that there are cases with massive grids where the number of cells at a single distance is proportional to N.
    So even with cells of a single distance on the queue, in the worst case, the space needed is O(N).
    """
    if grid[0][0] or grid[-1][-1]:
        return -1
    n = len(grid)
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)}
    queue = deque([(0, 0, 1)])
    visited = {(0, 0)}
    while queue:
        i, j, distance = queue.popleft()
        if i == j == n - 1:
            return distance
        for x, y in directions:
            a, b = i + x, j + y
            if 0 <= a < n and 0 <= b < n and not grid[a][b] and (a, b) not in visited:
                queue.append((a, b, distance + 1))
                visited.add((a, b))
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
