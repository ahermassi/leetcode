""" In a given grid, each cell can have one of three values:
the value 0 representing an empty cell;
the value 1 representing a fresh orange;
the value 2 representing a rotten orange.
Every minute, any fresh orange that is adjacent (4-directionally) to a rotten orange becomes rotten.
Return the minimum number of minutes that must elapse until no cell has a fresh orange.  If this is impossible,
return -1 instead. """

from collections import deque
import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=y704fEOx0s0
def oranges_rotting_v1(grid):
    """ It would be more intuitive to visualize the rotting process with a graph data structure, where each node
         represents a cell and the edge between two nodes indicates that the given two cells are adjacent to each other.

         The process of rotting could be explained perfectly with the BFS procedure, i.e. the rotten oranges will
         contaminate their neighbors first, before the contamination propagates to other fresh oranges that are farther
         away. The number of minutes that are elapsed would be equivalent to the number of levels in the graph that we
         traverse during the propagation.

         We use all rotten oranges as start position of the BFS. Moreover, we keep track of 'fresh_oranges' to count
         the number of 1s. If there is no fresh oranges initially, we immediately return 0.

         Usually in BFS algorithms, we keep a visited set which keeps track of the visited cells. The visited set helps
         avoid repetitive visits. But as we can notice, rather than using the visited set, we reuse the input grid to
         mark the visited cells, i.e. we are altering the status of the input grid in-place.

    Time complexity: O(N * M), first we scan the grid to find the initial values for the queue, then we run BFS on the
    queue, which in the worst case would enumerate all the cells in the grid once and only once.
    Space complexity: O(N * M), in the worst case, the grid is filled with rotten oranges. As a result, the queue would
    be initialized with all the cells in the grid.
    Normally for BFS, the main space complexity lies in the process rather than the initialization. For instance, for a
    BFS traversal of a tree, at any given moment, the queue would hold no more than 2 levels of tree nodes. Therefore,
    the space complexity of BFS traversal in a tree would depend on the width of the input tree.
    """

    n, m = len(grid), len(grid[0])
    queue = deque()
    fresh_oranges = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 2:
                queue.append((i, j))
            elif grid[i][j] == 1:
                fresh_oranges += 1
    if not fresh_oranges:
        return 0
    time = 0
    # If there are rotten oranges in the queue and there are still fresh oranges in the grid, keep looping
    while queue and fresh_oranges > 0:
        size = len(queue)
        # Process the rotten oranges of the current level
        for _ in range(size):
            i, j = queue.popleft()
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and grid[x][y] == 1:
                    grid[x][y] = 2  # Contaminate the fresh orange
                    fresh_oranges -= 1
                    queue.append((x, y))  # This orange would then contaminate other oranges
        # Update the number of minutes passed. It is safe to update the minutes by 1, since we visit oranges level by
        # level in BFS traversal.
        time += 1
    # Return -1 if there are fresh oranges left in the grid (there were no adjacent rotten oranges to contaminate them)
    return time if not fresh_oranges else -1


def oranges_rotting_v2(grid):
    """ BFS without altering the input grid. We use a hash set to keep track of the fresh oranges.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(grid), len(grid[0])
    queue = deque()
    fresh_oranges = set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 2:
                queue.append((i, j))
            elif grid[i][j] == 1:
                fresh_oranges.add((i, j))
    if not fresh_oranges:
        return 0
    time = 0
    while queue and fresh_oranges:
        size = len(queue)
        for _ in range(size):
            i, j = queue.popleft()
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and (x, y) in fresh_oranges:
                    fresh_oranges.remove((x, y))
                    queue.append((x, y))
        time += 1
    # Return -1 if there are fresh oranges left in the grid (there were no adjacent rotten oranges to contaminate them)
    return time if not fresh_oranges else -1


class Test(unittest.TestCase):
    data = [([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4), ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1), ([[0, 2]], 0)]

    def test_oranges_rotting(self):
        for test_grid, result in self.data:
            self.assertEqual(result, oranges_rotting_v1(test_grid))


if __name__ == '__main__':
    unittest.main()
