""" In a given grid, each cell can have one of three values:
the value 0 representing an empty cell;
the value 1 representing a fresh orange;
the value 2 representing a rotten orange.
Every minute, any fresh orange that is adjacent (4-directionally) to a rotten orange becomes rotten.
Return the minimum number of minutes that must elapse until no cell has a fresh orange.  If this is impossible,
return -1 instead. """

from collections import deque
import unittest2 as unittest


def oranges_rotting_v1(grid):
    """ Simple BFS solution using all rotten oranges as start position.
        Moreover, we use 'fresh' to count the number of 1s. If there is not fresh oranges initially, we immediately
        return 0. Otherwise, we return (res - 1) because the final iteration of the while loop runs for orange/oranges
        that are already rotten and don't have any fresh neighbours (so no time consumed).
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m, fresh, res = len(grid), len(grid[0]), 0, 0
    queue = deque()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                fresh += 1
            if grid[i][j] == 2:
                queue.append((i, j))
    if not fresh:
        return 0
    while queue:
        l = len(queue)
        for _ in range(l):
            i, j = queue.popleft()
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and grid[x][y] == 1:
                    grid[x][y] = 2
                    queue.append((x, y))
        res += 1
    return -1 if any(1 in row for row in grid) else res - 1


class Test(unittest.TestCase):
    data = [([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4), ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1), ([[0, 2]], 0)]

    def test_oranges_rotting(self):
        for test_grid, result in self.data:
            self.assertEqual(result, oranges_rotting_v1(test_grid))


if __name__ == '__main__':
    unittest.main()
