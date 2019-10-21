""" There is a ball in a maze with empty spaces and walls. The ball can go through empty spaces by rolling up, down,
left or right, but it won't stop rolling until hitting a wall. When the ball stops, it could choose the next direction.
Given the ball's start position, the destination and the maze, determine whether the ball could stop at the destination.
"""

import unittest2 as unittest


def has_path_v1(maze, start, destination):
    """ Good ol' DFS.
        We choose one path at a time and try to go as deep as possible into the levels of the tree before going for the
        next path. From every start position, we can move CONTINUOUSLY in either left, right, upward or downward
        direction till we reach the boundary or a wall. Thus, from the start position, we determine all the end points
        which can be reached by choosing the four directions. For each of the cases, the new endpoint will now act as
        the new start point for the traversals. Thus, now we call the same function four times for the four directions,
        each time with a new start point obtained previously. If any of the function call returns a True value, it
        means we can reach the destination.
    Time complexity: O(N * M), complete traversal of maze will be done in the worst case
    Space complexity: O(N * M), 'visited' set of size N * M is used
    """

    def dfs(i, j):
        if (i, j) in visited:
            return False
        if [i, j] == destination:
            return True
        visited.add((i, j))
        for x, y in (-1, 0), (1, 0), (0, -1), (0, 1):  # The 4 possible directions: up, down, left, right respectively
            new_i, new_j = i, j  # Start from current position and move
            while 0 <= new_i + x < n and 0 <= new_j + y < m and maze[new_i + x][new_j + y] == 0:  # Moving CONTINUOUSLY
                new_i += x
                new_j += y
            if dfs(new_i, new_j):  # When we can't move anymore, we see where we can go from the new position
                return True
        return False

    n, m = len(maze), len(maze[0])
    x, y = start
    visited = set()
    return dfs(x, y)


class Test(unittest.TestCase):
    data = [
        ([[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]], [0, 4], [4, 4], True)]

    def test_has_path(self):
        for test_maze, test_start, test_destination, result in self.data:
            self.assertEqual(result, has_path_v1(test_maze, test_start, test_destination))


if __name__ == '__main__':
    unittest.main()
