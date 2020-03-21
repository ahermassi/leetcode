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
    """ Instead of searching from an empty room to the gates, how about searching the other way round ? In other words,
        we initiate a BFS from all gates. Since BFS guarantees that we search all rooms of distance d before searching
        rooms of distance d + 1, the distance to an empty room must be the shortest. So whenever an empty room is
        reached, it must be from the closest gate.
        Each gate only looks at the areas within 1 space (immediate neighbors) before we check the next gate. So each
        area within 1 space of the gates are checked for rooms and these rooms are marked, then added to the queue.
        Once all gates are checked, each new space is checked, and so forth. So, once a room gets hit, it has to be
        from the closest gate.
        We can understand it by level-order BFS. First, we enqueue all 0s, let's say these these 0s are in level 1.
        Then from each 0 of the queue, we will go up, down, left and right, all these positions that are rooms are at
        level 1, and so forth. So assume we only have Gate A and Gate B, and we have a room C and all the other
        positions are walls. Assume that distance AC is 3 and distance BC is 4. So for Gate A, room C is at its level 3,
        and for Gate B room C is at its level 4. Since we are doing level order BFS, C will always first be accessed by
        the gate that is closer to it which is A.
    Time complexity: O(N * M). Let us start with the case with only one gate. The breadth-first search takes at most
    N * M steps to reach all rooms, therefore the time complexity is O(N * M). But what if we are doing BFS from
    k gates? Once we set a room's distance, we are basically marking it as visited, which means each room is visited at
    most once. Therefore, the time complexity does not depend on the number of gates and is O(N * M)
    Space complexity: O(N * M), the space complexity depends on the queue's size. We insert at most N * M points into
    the queue
    """
    if not rooms:
        return
    n, m = len(rooms), len(rooms[0])
    queue = deque([(i, j) for i in range(n) for j in range(m) if rooms[i][j] == 0])  # Enqueue all gates
    while queue:
        i, j = queue.popleft()
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if 0 <= x < n and 0 <= y < m and rooms[x][y] == 2 ** 31 - 1:  # If a room was hit (rooms[x][y] != INF), it
                # has to be from the closest gate, so there is no need to explore it again
                rooms[x][y] = 1 + rooms[i][j]
                queue.append((x, y))


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
