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

# Note: Why adding the cells to 'visited' set after being enqueued gives TLE ?
# Before or right after we make a new pair to queue, you should add (x, y) to 'visited' right away. Otherwise, on
# next round we might encounter several traversals to a same node.
#
# 0 : unvisited
# 1 : blocks
# 2 : current node in queue
#
# 021
# 200
# 022
# In this case, we might access grid[1][1] from 4 different nodes, so we should set it as visited once put into the
# queue.


def shortest_path_binary_matrix_v2(grid):
    """ BFS works by examining cells in order of distance from the starting point. In other words, all cells at a
        distance of x are visited before any cells at a distance of (x + 1). Additionally, cells at a distance of x
        can only enqueue other cells that are at a distance of (x + 1). Therefore, there are at most two unique
        distances in the queue at any one time.
        This implementation uses the same BFS property as the above one, but in a different way. At the start, there is
        exactly 1 cell at a distance of 1. Once we have dequeued and processed that cell, we know all cells currently
        in the queue must be of distance 2. We can check at this point how many of them there are and then dequeue and
        process that number of cells. Now we know all of the cells in the queue are of distance 3. This argument
        extends to the entire grid.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if grid[0][0] or grid[-1][-1]:
        return -1
    n = len(grid)
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)}
    queue, visited = deque([(0, 0)]), {(0, 0)}
    distance = 1
    while queue:
        size = len(queue)
        for _ in range(size):  # Process all nodes at distance 'distance' from the top-left cell
            i, j = queue.popleft()
            if i == j == n - 1:
                return distance
            for x, y in directions:
                a, b = i + x, j + y
                if 0 <= a < n and 0 <= b < n and not grid[a][b] and (a, b) not in visited:
                    queue.append((a, b))
                    visited.add((a, b))
        distance += 1  # We'll now be processing all nodes at (distance + 1)
    return -1


def shortest_path_binary_matrix_v3(grid):
    """ If we're allowed to modify the grid, we can securely set the visited cells as non-empty to avoid revisiting
        without using a 'visited' set. While usually for BFS, we'd need a 'visited' set to avoid infinite looping
        around cycles, we won't need one for this approach because we're going to overwrite the input, and so only
        unvisited cells will have a 0 in them. Exploring the cell's neighbors involves identifying all open cells
        adjacent to the current cell that still have a 0 in them. For each of these cells, we write 1 into them.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if grid[0][0] or grid[-1][-1]:
        return -1
    n = len(grid)
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)}
    queue = deque([(0, 0, 1)])
    while queue:
        i, j, distance = queue.popleft()
        if i == j == n - 1:
            return distance
        for x, y in directions:
            a, b = i + x, j + y
            if 0 <= a < n and 0 <= b < n and not grid[a][b] and not grid[a][b]:
                queue.append((a, b, distance + 1))
                grid[a][b] = 1  # Mark visited
    return -1


class Test(unittest.TestCase):
    data = [([[0, 1], [1, 0]], 2), ([[0, 0, 0], [1, 1, 0], [1, 1, 0]], 4)]

    def test_shortest_path_binary_matrix(self):
        for test_grid, result in self.data:
            self.assertEqual(result, shortest_path_binary_matrix_v1(test_grid))
            self.assertEqual(result, shortest_path_binary_matrix_v2(test_grid))
            self.assertEqual(result, shortest_path_binary_matrix_v3(test_grid))


if __name__ == '__main__':
    unittest.main()
