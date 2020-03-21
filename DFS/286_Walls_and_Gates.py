""" You are given a m x n 2D grid initialized with these three possible values.
-1 - A wall or an obstacle.
0 - A gate.
INF - Infinity means an empty room. We use the value 231 - 1 = 2147483647 to represent INF as you may assume that the
distance to a gate is less than 2147483647.
Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled
with INF. """

from collections import deque
import unittest2 as unittest


def walls_and_gates_v1(rooms):
    """ DFS.
        The condition rooms[i][j] < d solves 3 problems:
            1- Do not update walls & gates (-1s & 0s) because d will be always strictly greater than 0 except for the
               first call to dfs() from an empty room where d = 0
            2- Distinguish the visited and not visited nodes (the visited can only have smaller distance)
            3- Stop early when we find a previous gate has given shorter distance than the current one
    Time complexity: O((N * M)^2) in the worst case, for each point in the grid, the gate could be at most N * M
    steps away
    Space complexity: O(N * M)
    """

    def dfs(i, j, d):  # d is the distance of cell (i,j) to the nearest gate
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


def walls_and_gates_v2(rooms):
    """ Instead of searching from an empty room to the gates, how about searching the other way round? In other words,
        we initiate a BFS from all gates. Since BFS guarantees that we search all rooms of distance d before searching
        rooms of distance d + 1, the distance to an empty room must be the shortest. So whenever an empty room is
        reached, it must be from the closest gate.
    Time complexity: O(N * M). Let us start with the case with only one gate. The breadth-first search takes at most
    N* M steps to reach all rooms, therefore the time complexity is O(N * M). But what if you are doing BFS from
    k gates? Once we set a room's distance, we are basically marking it as visited, which means each room is visited at
    most once. Therefore, the time complexity does not depend on the number of gates and is O(N * M)
    Space complexity: O(N * M), the space complexity depends on the queue's size. We insert at most N* M points into
    the queue
    """
    if not rooms:
        return
    n, m, queue = len(rooms), len(rooms[0]), deque()
    for i in range(n):
        for j in range(m):
            if rooms[i][j] == 0:
                queue.append((i, j))
    while queue:
        i, j = queue.popleft()
        for x, y in (-1, 0), (1, 0), (0, -1), (0, 1):
            new_i, new_j = i + x, j + y
            if 0 <= new_i < n and 0 <= new_j < m and rooms[new_i][new_j] == 2147483647:
                rooms[new_i][new_j] = rooms[i][j] + 1
                queue.append((new_i, new_j))


class Test(unittest.TestCase):
    data = [
        ([[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1], [2147483647, -1, 2147483647, -1],
          [0, -1, 2147483647, 2147483647]], [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]])]

    def test_walls_and_gates(self):
        for test_rooms, result in self.data:
            walls_and_gates_v2(test_rooms)
            self.assertEqual(result, test_rooms)


if __name__ == '__main__':
    unittest.main()
