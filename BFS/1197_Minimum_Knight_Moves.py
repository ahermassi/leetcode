""" In an infinite chess board with coordinates from -infinity to +infinity, you have a knight at square [0, 0].
A knight has 8 possible moves it can make, as illustrated below. Each move is two squares in a cardinal direction,
then one square in an orthogonal direction.
Return the minimum number of steps needed to move the knight to the square [x, y].  It is guaranteed the answer exists.
"""

from collections import deque
import unittest2 as unittest


def min_knight_moves(x, y):
    """ The moves are symmetric. Hence, we can just assume the problem to be in the first quadrant and push only
        positive coordinates to the queue. Consequently, a simple BFS would give us the required result.
        However, code fails when (x, y) = (1, 1). To reach (1, 1) from (0, 0), the best way is to get (2, -1) or (-1, 2)
        first, then (1,1) (two steps). If we eliminate all coordinates with negative values and consider only those in
        the first quadrant, we can't reach (1, 1) from (0, 0) in two steps.
        Since adjusted target is in the first quadrant, we'd like to explore towards that direction rather than the
        opposite. So whenever there's a step that lies < (-1, -1), we'd like to stop exploring that direction.
    """
    x, y = abs(x), abs(y)
    queue, visited = deque([(0, 0, 0)]), set()
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
    while queue:
        i, j, distance = queue.popleft()
        if i == x and j == y:
            return distance
        for move in moves:
            a, b = i + move[0], j + move[1]
            if (a, b) not in visited and a >= -1 and b >= -1:
                visited.add((a, b))
                queue.append((a, b, distance + 1))


class Test(unittest.TestCase):
    data = [(2, 1, 1), (5, 5, 4)]

    def test_min_knight_moves(self):
        for test_x, test_y, result in self.data:
            self.assertEqual(result, min_knight_moves(test_x, test_y))


if __name__ == '__main__':
    unittest.main()
