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
    """ The process of rotting could be explained perfectly with the BFS procedure, i.e. the rotten oranges will
         contaminate their neighbors first, before the contamination propagates to other fresh oranges that are farther
         away. The number of minutes that are elapsed would be equivalent to the number of levels in the graph that we
         traverse during the propagation.

         We use all rotten oranges as start position of the BFS. Moreover, we keep track of a 'fresh_oranges' to count
         the number of 1s. If there is no fresh oranges initially, we immediately return 0.

         Usually in BFS algorithms, we keep a visited set which records the visited candidates. The visited set helps
         us avoid repetitive visits. But as we can notice, rather than using the visited set, we reuse the input grid to
         keep track of our visits, i.e. we were altering the status of the input grid in-place.

    Time complexity: O(N * M), first we scan the grid to find the initial values for the queue, then we run BFS on the
    queue, which in the worst case would enumerate all the cells in the grid once and only once.
    Space complexity: O(N * M), in the worst case, the grid is filled with rotten oranges. As a result, the queue would
    be initialized with all the cells in the grid.
    By the way, normally for BFS, the main space complexity lies in the process rather than the initialization. For
    instance, for a BFS traversal in a tree, at any given moment, the queue would hold no more than 2 levels of tree
    nodes. Therefore, the space complexity of BFS traversal in a tree would depend on the width of the input tree.
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
        # Process rotten oranges on the current level
        for _ in range(size):
            i, j = queue.popleft()
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and grid[x][y] == 1:
                    grid[x][y] = 2  # This orange would be rotten
                    fresh_oranges -= 1
                    queue.append((x, y))  # This orange would then contaminate other oranges
        # Update the number of minutes passed. It is safe to update the minutes by 1, since we visit oranges level by
        # level in BFS traversal.
        time += 1
    # Return -1 if there are fresh oranges left in the grid (there were no adjacent rotten oranges to make them rotten)
    return time if not fresh_oranges else -1


def oranges_rotting_v2(grid):
    """ Same BFS using depth.
        Every turn, the rotting spreads from each rotting orange to other adjacent oranges. Initially, the rotten
        oranges have 'depth' 0 [as in the spanning tree of a graph], and every time they rot a neighbor, the neighbors
        have 1 more depth. We want to know the largest possible depth.
        Because we always explore nodes (oranges) with the smallest depth first, we're guaranteed that each orange that
        becomes rotten does so with the lowest possible depth number.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m, fresh, depth = len(grid), len(grid[0]), 0, 0
    queue = deque()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                fresh += 1
            if grid[i][j] == 2:
                queue.append((i, j, 0))
    if not fresh:
        return 0
    while queue:
        i, j, depth = queue.popleft()
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if 0 <= x < n and 0 <= y < m and grid[x][y] == 1:
                grid[x][y] = 2
                queue.append((x, y, depth + 1))
    return -1 if any(1 in row for row in grid) else depth


class Test(unittest.TestCase):
    data = [([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4), ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1), ([[0, 2]], 0)]

    def test_oranges_rotting(self):
        for test_grid, result in self.data:
            self.assertEqual(result, oranges_rotting_v1(test_grid))


if __name__ == '__main__':
    unittest.main()
