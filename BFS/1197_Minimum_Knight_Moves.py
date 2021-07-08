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


def min_knight_moves_v2(x, y):
    """ Based on the above idea of BFS, one optimization that we can apply is to perform bidirectional exploration
        instead of unidirectional exploration, which means we start BFS from both origin and target coordinates.
        To implement the bidirectional BFS algorithm, we will double the usage of the data structures in the
        unidirectional BFS. Additionally, we need to make the following adaptations
            Instead of using the set data structure to keep track of the visited places, we use the map data
            structure, which contains not only the information of visited cells but also the distance between each
            cell and the starting exploration point.
    Time complexity: Reducing the scope of exploration by half does speed up the algorithm. However, it does not change
    the time complexity of the algorithm which remains O((max(|x|, |y|)) ^ 2)
    """
    origin_queue = deque([(0, 0, 0)])
    target_queue = deque([(x, y, 0)])
    distance_from_origin = {(0, 0): 0}
    distance_from_target = {(x, y): 0}
    directions = [(-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, 2), (2, 1), (1, -2), (2, -1)]
    while True:
        origin_i, origin_j, origin_moves = origin_queue.popleft()
        if (origin_i, origin_j) in distance_from_target:  # Check if we reach the exploration circle of target
            return origin_moves + distance_from_target[(origin_i, origin_j)]
        target_i, target_j, target_moves = target_queue.popleft()
        if (target_i, target_j) in distance_from_origin:  # Check if we reach the exploration circle of origin
            return target_moves + distance_from_origin[(target_i, target_j)]
        for a, b in directions:
            # Expand the exploration circle of origin
            if (origin_i + a, origin_j + b) not in distance_from_origin:
                origin_queue.append((origin_i + a, origin_j + b, origin_moves + 1))
                distance_from_origin[(origin_i + a, origin_j + b)] = origin_moves + 1
            # Expand the exploration circle of target
            if (target_i + a, target_j + b) not in distance_from_target:
                target_queue.append((target_i + a, target_j + b, target_moves + 1))
                distance_from_target[(target_i + a, target_j + b)] = target_moves + 1


def min_knight_moves_v3(x, y):
    """ Before explaining the following BFS optimization, we should address the symmetry of the answers, which we
        haven't touched on so far.
            We claim that the target (x, y), its horizontally, vertically, and diagonally symmetric points
            (i.e. (x, -y), (-x, y), (-x, -y)) share the same answer as the target point.
        Based on the above insight, we can focus on the first quadrant of the coordinate plane where both x and y are
        positive. Any target that is outside of the first quadrant can be shifted to its symmetric point in the first
        quadrant by taking the absolute value of each coordinate, i.e. (|x|, |y|).
        However, code fails when (x, y) = (1, 1). To reach (1, 1) from (0, 0), the best way is to get (2, -1) or (-1, 2)
        first, then (1, 1) (two steps). If we eliminate all coordinates with negative values and consider only those in
        the first quadrant, we can't reach (1, 1) from (0, 0) in two steps.
        The coordinates in general to compute the knight moves are: (x - 2, y - 1), (x - 2, y + 1), (x - 1, y - 2) ...
        where for all x, y >= 2 the next "move" will always be >= 0 (i.e. in the first quadrant). Only for
        (x = 1, y = 1) the next move may fall in the negative quadrant, and hence x = -1, y = -1 boundary is considered.
    """
    x, y = abs(x), abs(y)
    queue, visited = deque([(0, 0, 0)]), set()
    directions = [(-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, 2), (2, 1), (1, -2), (2, -1)]
    while queue:
        i, j, distance = queue.popleft()
        if i == x and j == y:
            return distance
        for a, b in directions:
            new_i, new_j = i + a, j + b
            if (new_j, new_j) not in visited and new_i >= -1 and new_j >= -1:
                visited.add((new_i, new_j))
                queue.append((new_i, new_j, distance + 1))


def min_knight_moves_v4(x, y):
    """ Top-down Dynamic Programming.
        We also use the symmetry property defined in the previous solution for this algorithm. We focus on the first
        quadrant of the coordinate plane where both x and y are positive.
        Rather than starting from the origin, we start from the target and walk backwards to reach the origin.
        For a target that is situated in the first quadrant, though technically we could move in 8 different directions,
        there are only two directions (i.e. left-down and down-left) that will move us closer to the origin.
        Indeed, before we reach the immediate neighborhood of the origin, we only need to explore the two left-down
        directions (with offsets of (-1, -2) and (-2, -1)), since the rest of the directions will deviate further away
        from the origin.
        The immediate neighborhood of the origin refers to the points of where the sum of coordinates is less than or
        equal to 2, i.e. x + y <= 2. As it turns out, any immediate neighbors with (x + y == 2) takes exactly 2 steps
        to reach when starting from the origin.
        With the above insights in mind, we can begin to work on our DFS algorithm.
        Assume that the function dfs(i, j) returns the minimum steps required to reach the target point (i, j). The
        idea of DFS can be expressed in the following formula:
            dfs(x, y) = min(dfs(∣x| − 2,∣y| − 1), dfs(∣x| − 1,∣y| − 2)) + 1
        The formula can be interpreted as such: At each step of the backward exploration process, by only exploring
        the left-down directions we can obtain the shortest path.
        As we might notice, the above function is a recursive function, and it is critical to define the base cases to
        make the definition sound. There are in general two base cases:
            - Case 1): i = 0, j = 0, when we reach the origin, no further steps are required to reach our goal, i.e.
              dfs(i, j) = 0.
            - Case 2): i + j = 2, when we are at a immediate neighbor as we discussed before, it takes two more steps
              to reach our goal, i.e. dfs(i, j) = 2. The moment we reach (0, 2), (2, 0), or (1, 1) the knight cannot
              move further to (0, 0) without going into negative coordinates quadrant. Or the best way is if we are on
              (0, 2) move the knight to (2, 1) then from there it could move to (0, 0), and this takes 2 moves . Same
              applies for (1, 1) and (2, 0).
        Additionally, it is important to apply the memoization technique to prevent duplicate calculations from
        occurring during the recursive process.
    Time complexity: O(|x| * |y|), we restrict the exploration to the first quadrant of the board. Therefore, in the
    worst case, we will explore all of the cells between the origin and the target in the first quadrant. In total,
    there are ∣x⋅y∣ cells in a rectangle that spans from the origin to the target.
    Space complexity: O(|x| * |y|), first of all, due to the presence of recursion in the algorithm, it will incur
    additional memory consumption in the function call stack. The consumption is proportional to the level of the
    execution tree, i.e. max(∣x∣,∣y∣). Secondly, due to the application of memoization technique, we will keep all the
    intermediate results in the memory for reuse. As we have seen in the above time complexity analysis, the maximum
    number of intermediate results will be O(|x| * |y|). To sum up, the overall space complexity of the algorithm is
    O(|x| * |y|), which is dominated by the memoization part.
    """

    def dfs(i, j):
        if i == j == 0:
            return 0
        if i + j == 2:
            return 2
        if (i, j) in cache:
            return cache[(i, j)]
        res = min(dfs(abs(i - 1), abs(j - 2)), dfs(abs(i - 2), abs(j - 1))) + 1
        cache[(i, j)] = res
        return res

    x, y = abs(x), abs(y)
    cache = {}
    return dfs(x, y)


class Test(unittest.TestCase):
    data = [(2, 1, 1), (5, 5, 4)]

    def test_min_knight_moves(self):
        for test_x, test_y, result in self.data:
            self.assertEqual(result, min_knight_moves_v1(test_x, test_y))
            self.assertEqual(result, min_knight_moves_v2(test_x, test_y))
            self.assertEqual(result, min_knight_moves_v3(test_x, test_y))
            self.assertEqual(result, min_knight_moves_v4(test_x, test_y))


if __name__ == '__main__':
    unittest.main()
