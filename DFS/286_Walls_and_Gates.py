""" You are given a m x n 2D grid initialized with these three possible values.
-1 - A wall or an obstacle.
0 - A gate.
INF - Infinity means an empty room. We use the value 231 - 1 = 2147483647 to represent INF as you may assume that the
distance to a gate is less than 2147483647.
Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled
with INF. """

import unittest2 as unittest


def walls_and_gates_v1(rooms):
    """ DFS.
        The condition rooms[i][j] < d solves 3 problems:
            1- Do not update walls & gates (-1 & 0s)
            2- Distinguish the visited and not-visited nodes (the visited can only have smaller distance)
            3- Stop earlier when you find the previous gate has given shorter distance than the current one
    Time complexity: O((N * M) ** 2) in the worst case, for each point in the grid, the gate could be at most N * M
    steps away
    """

    def dfs(i, j, d):
        if not 0 <= i < n or not 0 <= j < m or rooms[i][j] < d:
            return
        rooms[i][j] = d
        for x, y in (-1, 0), (1, 0), (0, -1), (0, 1):
            dfs(i + x, j + y, d + 1)

    if not rooms:
        return
    n, m = len(rooms), len(rooms[0])
    for i in range(n):
        for j in range(m):
            if rooms[i][j] == 0:
                dfs(i, j, 0)


class Test(unittest.TestCase):
    data = [
        ([[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1], [2147483647, -1, 2147483647, -1],
          [0, -1, 2147483647, 2147483647]], [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]])]

    def test_walls_and_gates(self):
        for test_rooms, result in self.data:
            walls_and_gates_v1(test_rooms)
            self.assertEqual(result, test_rooms)


if __name__ == '__main__':
    unittest.main()
