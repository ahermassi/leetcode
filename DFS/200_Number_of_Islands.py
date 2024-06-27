""" Given a 2d grid map of '1's (land) and '0's (water), count the number of islands. An island is surrounded by
water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the
grid are all surrounded by water. """

from collections import deque
import unittest2 as unittest


def num_islands_v1(grid):
    """ Treat the 2D grid map as an undirected graph and there is an edge between two horizontally or vertically
         adjacent nodes of value '1'.

         Linearly scan the cells, and if a cell contains '1' then it is a root node that triggers a DFS to mark all
         adjacent nodes, then increase the islands counter by 1. The algorithm uses a 'visited' set in order to avoid
         an infinite recursion.

        Count the number of root nodes that trigger DFS. This number would be the number of islands since each DFS
        starting at some root identifies an island.

    Time complexity: O(N * M), where N is the number of rows in the given grid and M is the number of columns. Because
    we mark cells as visited, we won't visit the same cell multiple times.
    Space complexity: O(N * M), for both 'visited' set and recursion call stack
    """
    def dfs(i, j):
        visited.add((i, j))
        for x, y in directions:
            if 0 <= i+x < n and 0 <= j+y < m and grid[i+x][j+y] == '1' and (i+x, j+y) not in visited:
                dfs(i+x, j+y)

    n, m = len(grid), len(grid[0])
    islands, visited = 0, set()
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1' and (i, j) not in visited:
                dfs(i, j)
                islands += 1
    return islands


def num_islands_v2(grid):
    """ Same solution as above but without using a 'visited' set. Instead, mark every visited cell as '0'. This is
        also known as 'sinking' the islands.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    def dfs(i, j):
        grid[i][j] = '0'
        for x, y in directions:
            if 0 <= i + x < n and 0 <= j + y < m and grid[i + x][j + y] == '1':
                dfs(i+x, j+y)

    n, m, islands = len(grid), len(grid[0]), 0
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1':
                dfs(i, j)
                islands += 1
    return islands


# Video explanation: https://youtu.be/pV2kpPD66nE
def num_islands_v3(grid):
    """ Same algorithm but using BFS.

        Linearly scan the 2D grid. If a node contains a '1', then it is a root node that triggers a Breadth-First
        Search. Put it into a queue and mark it as visited node. Iteratively search the neighbors of enqueued nodes
        until the queue becomes empty.

    Time complexity: O(N * M)
    Space complexity: O(min(N, M)). Considering BFS always starts from the upper left corner, grid[0][0], and BFS is
    scanning by the order of the same depth/level (FIFO), so there is no way an element can be added into the queue
    after we have already scanned it at that same position. This leads to the maximum size of queue should be the
    maximum diagonal length of the grid, same as, min(N, M) (Find visualization in notes).
    Think about an example where diff(N, M) is big like 3x1000 grid. The worst case is when we start from the middle of
    the grid. Imagine how the processed points form a shape in the grid. It will be like a diamond and at some point it
    will reach the longer edge of the grid. The possible shape at time t would be:
        ......QXXXQ.........
        ....QXXXXXQ........
        ......QXXXQ.........
    So in this specific example (Q: points in the queue, .: not processed, X: processed) the number of the items in the
    queue is proportional to 3 because the smallest side limits the expanding. So the actual value will be min(N, M).
    Example: Let's consider the below 3x4 grid. X denotes cells in the queue. The max space occupied by the queue in the
    below example is 3 which min(N, M).

        1 1 1 1
        1 1 1 1
        1 1 1 1

        Step 1
        0 X 1 1
        X 1 1 1
        1 1 1 1

        Step 2
        0 X 1 1
        0 X 1 1
        X 1 1 1

        Step 3
        0 0 X 1
        0 X 1 1
        X 1 1 1

        Step 4
        0 0 X 1
        0 X 1 1
        0 X 1 1


        Step 5
        0 0 0 X
        0 0 X 1
        0 X 1 1

        Step 6
        0 0 0 X
        0 0 X 1
        0 0 X 1

        Step 7
        0 0 0 X
        0 0 0 X
        0 0 X 1

        Step 8
        0 0 0 0
        0 0 0 X
        0 0 X 1

        Step 9
        0 0 0 0
        0 0 0 X
        0 0 0 X

        Step 10
        0 0 0 0
        0 0 0 0
        0 0 0 X

        Step 11
        0 0 0 0
        0 0 0 0
        0 0 0 0

        Can also think about what happens if grid is 1xN or Mx1 (1 row or 1 col). Only max of 1 item will be in the
        queue at a time
    """
    n, m,  = len(grid), len(grid[0])
    islands, visited = 0, set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1' and (i, j) not in visited:
                queue = deque([(i, j)])
                while queue:
                    x, y = queue.popleft()
                    for a, b in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
                        if 0 <= a < n and 0 <= b < m and grid[a][b] == '1' and (a, b) not in visited:
                            queue.append((a, b))
                            visited.add((a, b))
                islands += 1
    return islands


class Test(unittest.TestCase):
    data = [([['1', '1', '1', '1', '0'], ['1', '1', '0', '1', '0'], ['1', '1', '0', '0', '0'],
              ['0', '0', '0', '0', '0']], 1)]

    def test_num_islands(self):
        for test_island, result in self.data:
            self.assertEqual(result, num_islands_v1(test_island))
            # self.assertEqual(result, num_islands_v2(test_island))
            self.assertEqual(result, num_islands_v3(test_island))


if __name__ == '__main__':
    unittest.main()
