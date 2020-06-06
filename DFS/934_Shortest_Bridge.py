""" In a given 2D binary array A, there are two islands.  (An island is a 4-directionally connected group of 1s not
connected to any other 1s.)
Now, we may change 0s to 1s so as to connect the two islands together to form 1 island.
Return the smallest number of 0s that must be flipped. (It is guaranteed that the answer is at least 1) """

from collections import deque
import unittest2 as unittest


def shortest_bridge(A):
    """ Conceptually, our method is very straightforward: find the first island, then keep "growing" it by 1 until we
        touch the second island. We can use a depth-first search to find the island and collect its cells in a queue at
        the same time, and then start a breadth-first search to "grow" the island and find number of bridges (levels)
        until we reach the second island.
    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < n or not A[i][j] or (i, j) in visited:
            return
        visited.add((i, j))
        queue.append((i, j))
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            dfs(x, y)

    n, queue, visited = len(A), deque(), set()
    first_island_found = False
    for i in range(n):
        for j in range(n):
            if A[i][j]:
                dfs(i, j)
                first_island_found = True
                break
        if first_island_found:
            break
    levels = 0
    while queue:  # Count number of levels before finding the second island
        size = len(queue)
        for _ in range(size):
            i, j = queue.popleft()
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < n and (x, y) not in visited:
                    if A[x][y]:  # A[x][y] == 1 and not previously visited: This is the second island!
                        return levels
                    visited.add((x, y))
                    queue.append((x, y))
        levels += 1
    return 1


class Test(unittest.TestCase):
    data = [([[0, 1], [1, 0]], 1), ([[0, 1, 0], [0, 0, 0], [0, 0, 1]], 2),
            ([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]], 1)]

    def test_shortest_bridge(self):
        for test_a, result in self.data:
            self.assertEqual(result, shortest_bridge(test_a))


if __name__ == '__main__':
    unittest.main()
