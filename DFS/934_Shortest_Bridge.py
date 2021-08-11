""" In a given 2D binary array A, there are two islands.  (An island is a 4-directionally connected group of 1s not
connected to any other 1s.)
Now, we may change 0s to 1s so as to connect the two islands together to form 1 island.
Return the smallest number of 0s that must be flipped. (It is guaranteed that the answer is at least 1) """

from collections import deque
import unittest2 as unittest


def shortest_bridge_v1(grid):
    """ Conceptually, our method is very straightforward: Find the first island, then keep "growing" it by 1 until we
        touch the second island. We can use a depth-first search to find the island and collect its cells in a queue at
        the same time, and then start a breadth-first search to "grow" the island and find number of bridges (levels)
        until we reach the second island.
    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < n or not grid[i][j] or (i, j) in visited:
            return
        visited.add((i, j))
        queue.append((i, j, 0))  # Add all cells of first island into queue as first level as they all can be the
        # starting points of a later BFS
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            dfs(x, y)

    n, queue, visited = len(grid), deque(), set()
    first_island_found = False
    for i in range(n):
        if first_island_found:
            break
        for j in range(n):
            if grid[i][j]:
                dfs(i, j)
                first_island_found = True
                break
    while queue:
        x, y, distance = queue.popleft()
        for a, b in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
            if 0 <= a < n and 0 <= b < n and (a, b) not in visited:
                if grid[a][b]:  # grid[a][b] == 1 and not previously visited: This is the second island!
                    return distance
                # (a, b) not in visited and grid[a][b] != 1 means grid[a][b] == 0
                visited.add((a, b))
                queue.append((a, b, distance + 1))
    return 1


def shortest_bridge_v2(grid):
    """ Same approach but we count the number of levels before finding the second island. The BFS goes level by level.
    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < n or not grid[i][j] or (i, j) in visited:
            return
        visited.add((i, j))
        queue.append((i, j))  # Add all cells of first island into queue without any level
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            dfs(x, y)

    n, queue, visited = len(grid), deque(), set()
    first_island_found = False
    for i in range(n):
        if first_island_found:
            break
        for j in range(n):
            if grid[i][j]:
                dfs(i, j)
                first_island_found = True
                break
    level = 0
    while queue:
        size = len(queue)
        for _ in range(size):
            x, y = queue.popleft()
            for a, b in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
                if 0 <= a < n and 0 <= b < n and (a, b) not in visited:
                    if grid[a][b]:
                        return level
                    visited.add((a, b))
                    queue.append((a, b))
        level += 1
    return 1


def shortest_bridge_v3(grid):
    """ We first paint one of the islands using DFS with color 2, so we can easily identify island #1 and island #2.
        Then we start expanding the island painted with color 2 until we "bump" into the other island.
        This approach is only different in the use of a different color to mark visited cells instead of 'visited' set.
    Time complexity:
    Space complexity:
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < n or grid[i][j] != 1:
            return
        grid[i][j] = 2
        queue.append((i, j, 0))
        for x, y in (-1, 0), (1, 0), (0, -1), (0, 1):
            dfs(i + x, j + y)

    n = len(grid)
    queue = deque()
    first_island_found = False
    for i in range(n):
        if first_island_found:
            break
        for j in range(n):
            if grid[i][j]:
                dfs(i, j)
                first_island_found = True
                break
    while queue:
        x, y, distance = queue.popleft()
        for a, b in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
            if 0 <= a < n and 0 <= b < n and grid[a][b] != 2:
                if grid[a][b]:
                    return distance
                # grid[a][b] != 2 and grid[a][b] != 1 means grid[a][b] == 0
                grid[a][b] = 2  # Mark visited
                queue.append((a, b, distance + 1))
    return 1


class Test(unittest.TestCase):
    data = [([[0, 1], [1, 0]], 1), ([[0, 1, 0], [0, 0, 0], [0, 0, 1]], 2),
            ([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]], 1)]

    def test_shortest_bridge(self):
        for test_a, result in self.data:
            self.assertEqual(result, shortest_bridge_v1(test_a))
            self.assertEqual(result, shortest_bridge_v2(test_a))
            self.assertEqual(result, shortest_bridge_v3(test_a))


if __name__ == '__main__':
    unittest.main()
