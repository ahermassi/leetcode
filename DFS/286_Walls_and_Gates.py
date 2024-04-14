""" You are given an m x n 2D grid initialized with these three possible values.
-1   - A wall or an obstacle.
0     - A gate.
INF  - Infinity means an empty room. We use the value 2^31 - 1 = 2147483647 to represent INF as you may assume that the
distance to a gate is less than 2147483647.
Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled
with INF. """

from collections import deque
import unittest2 as unittest


def walls_and_gates_v1(rooms):
    """ Brute force. DFS from every gate.

        The condition (rooms[x][y] > distance) solves 3 problems:

            1- Do not update walls & gates (-1s & 0s) because 'distance' will always be strictly greater than 0 except
                 for the first call to dfs() from an empty room where distance = 0

            2- Distinguish the visited and non-visited nodes (the visited can only have smaller distance)

            3- Stop early when we find that a previous gate has given a shorter distance than the current one

    Time complexity: O((N * M)^2)
    Space complexity: O(N * M)
    """

    def dfs(i, j, distance):
        # 'distance' is the distance from cell (i,j) to the nearest gate
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if 0 <= x < n and 0 <= y < m and rooms[x][y] > distance:
                rooms[x][y] = distance + 1
                dfs(x, y, distance + 1)

    n, m = len(rooms), len(rooms[0])
    for i in range(n):
        for j in range(m):
            if rooms[i][j] == 0:
                dfs(i, j, 0)


# Video explanation: https://www.youtube.com/watch?v=e69C6xhiSQE
def walls_and_gates_v2(rooms):
    """ Multi-source BFS.

        We initiate a BFS from all gates. Since BFS guarantees that we search all rooms of distance d before searching
        rooms of distance d+1, the distance to an empty room must be the shortest. So whenever an empty room is
        reached, it must be from the closest gate.

        We start BFS from each of the gates by enqueuing the coordinates into the queue. Since the queue is FIFO, the
        first gate is processed first. While doing a BFS from the first gate, we check the coordinates at distance 1
        from that gate, and only if we hit an empty room at coordinates (x, y) we increment the distance by 1 since it
        is the next level, i.e. rooms[x][y] = rooms[row][col] + 1.

        Then we enqueue the adjacent nodes of this cell, but since it is a queue, those coordinates are added to the
        back of the queue. So next to be processed is the 2nd gate which was added, and so on. Since we spread out from
        each gate in a BFS manner for a single step only each time and evaluate the distance, we have to get the
        shortest distance from each room to a gate.

        Each gate looks only at the areas within 1 hop (immediate neighbors) before we check the next gate. So each
        area within 1 hop of the gate is checked for rooms and these rooms are marked then added to the queue.
        Once all the gates are checked, each new space is checked, and so on. So, once a room is reached, it has to be
        from the closest gate.

        We can understand it by level-order BFS. First, we enqueue all 0s, and let's say these 0s are at level 1.
        Then from each 0 of the queue, we will go up, down, left and right, all these positions that are rooms are at
        level 1, and so on. So assume we only have Gate A and Gate B, and we have a room C and all the other
        positions 1 hop away are walls. Assume that distance A-C is 3 and distance B-C is 4. So for Gate A, room C is at
        its level 3, and for Gate B room C is at its level 4. Since we are doing level-order BFS, C will always first be
        reached from the gate that is closer to it which is A.

        Imagine that all the gates are "competing" against each other "at the same time". Once a gate reaches an empty
        room and marks it with the distance, that room must be closest to that gate (compared to the rest of the gates)
        because that gate is the 1st gate (think of it as a 1st prize winner) to reach that room.

        Consider this linear grid: [[GATE] [INF] [INF] [INF] [GATE]]
        queue: [ (gate_0,0), (gate_0,4) ]

        Iteration 1: (updating distances from (gate_0,0)) : [[GATE] [1] [INF] [INF] [GATE]]
        queue: [ (gate_0,4), (room_0,1) ]

        Iteration 2: (updating distances from (gate_0,4) not from (room_0,1)) : [[GATE] [1] [INF] [1] [GATE]]
        queue: [ (room_0,1), (room_0,3) ]

        Iteration 3: (updating distances from (room_0,1)) : [[GATE] [1] [2] [1] [GATE]]
        queue: [ (room_0,3), (room_0,2) ]

    Time complexity: O(N * M). Let us start with the case with only one gate. The breadth-first search takes at most
    N * M steps to reach all rooms, therefore the time complexity is O(N * M). But what if we are doing BFS from
    k gates? Once we set a room's distance, we are basically marking it as visited/done processing, which means each
    room is visited at most once. Therefore, the time complexity does not depend on the number of gates and is O(N * M).
    Space complexity: O(N * M), the space complexity depends on the queue's size. We insert at most N * M points into
    the queue
    """
    n, m = len(rooms), len(rooms[0])
    queue = deque((i, j) for i in range(n) for j in range(m) if rooms[i][j] == 0)  # Enqueue all gates
    while queue:
        i, j = queue.popleft()
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            # If a room was previously reached (rooms[x][y] != INF), it has to be from the closest gate, so there is
            # no need to visit it again.
            if 0 <= x < n and 0 <= y < m and rooms[x][y] > rooms[i][j] + 1:  # Or rooms[x][y]  == 2**31 - 1
                rooms[x][y] = rooms[i][j] + 1
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
