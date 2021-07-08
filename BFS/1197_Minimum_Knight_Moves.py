""" In an infinite chess board with coordinates from -infinity to +infinity, you have a knight at square [0, 0].
A knight has 8 possible moves it can make, as illustrated below. Each move is two squares in a cardinal direction,
then one square in an orthogonal direction.
Return the minimum number of steps needed to move the knight to the square [x, y].  It is guaranteed the answer exists.
"""

from collections import deque
import unittest2 as unittest


def min_knight_moves_v1(x, y):
    """ The key to solving this problem is based on the BFS strategy. The idea is that starting from the origin, we
        explore the neighborhood following the order that is determined by the distance to the origin, i.e. we first
        explore all the points within a single step from the origin, then we explore all the points that can be reached
        with two steps, so on and so forth. During the exploration process, as soon as we reach the target point, we
        then can call the current path the shortest path, since our exploration follows the order of distance.
        We can imagine the whole process as if we send a sound wave to determine the distance to an unknown object.
        The sound wave propagates in all directions with the same speed, while its scope grows as a circle. Once the
        circle reaches the target object, the radius is the shortest distance between the origin and the target object.
    Time complexity: Due to the nature of BFS, before reaching the target, we will have covered all the neighborhoods
    that are closer to the start point. The aggregate of these neighborhoods forms a circle, and the area can be
    approximated by the area of a square with an edge length of max(2|x|, 2|y|). The number of cells within this square
    would be (max(2|x|, 2|y|)) ^ 2. Hence, the overall time complexity of the algorithm is O((max(|x|, |y|)) ^ 2).
    """
    queue = deque([(0, 0, 0)])
    visited = set()
    directions = [(-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, 2), (2, 1), (1, -2), (2, -1)]
    while queue:
        i, j, distance = queue.popleft()
        if (i, j) == (x, y):
            return distance
        for a, b in directions:
            new_i, new_j = i + a, j + b
            if (new_i, new_i) not in visited:
                visited.add((new_i, new_j))
                queue.append((new_i, new_j, distance + 1))


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
