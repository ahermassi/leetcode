""" There is a ball in a maze with empty spaces and walls. The ball can go through empty spaces by rolling up, down,
left or right, but it won't stop rolling until hitting a wall. When the ball stops, it could choose the next direction.
Given the ball's start position, the destination and the maze, find the shortest distance for the ball to stop at the
destination. The distance is defined by the number of empty spaces traveled by the ball from the start position
(excluded) to the destination (included). If the ball cannot stop at the destination, return -1. """

from collections import deque
import unittest2 as unittest


def shortest_distance_v1(maze, start, destination):
    """" BFS. DFS version is below but it TLEs.
         Same logic as with 490- The Maze, but we also use a 'distance' array initialized with float('inf').
         distance[i][j] again represents the minimum number of steps required to reach the position (i,j) from the
         start position, such that distance[start[0]][start[1]] = 0
         When we reach any position next to a boundary or a wall during the traversal in a particular direction, as
         discussed earlier, we keep a track of the number of steps taken in the last direction in 'd' variable. Suppose
         we reach the position (k,l) starting from the last position (i,j). Now, for this position, we need to
         determine the minimum number of steps taken to reach this position starting from the start position. For this,
         we check if the current path takes lesser steps to reach (k, l) than any other previous path taken to reach
         the same position i.e. we check if distance[i][j] + d is less than distance[k][l].
         If distance[i][j] + d is less than distance[k][l], we can reach the position (k, l) from the current route in
         less number of steps. Thus, we need to update the value of distance[k][l as distance[i][j] + d. Further, now
         we need to try to reach the destination from the end position (k,l), since this could lead to a shorter path
         to destination.
         After this, we add the new position obtained, (k, l) to the back of the queue, so that the various paths
         possible from this new position will be explored later on when all the directions possible from the current
         position (i, j) have been explored.
         At the end, the entry in distance array corresponding to the destination's coordinates gives the required
         minimum distance to reach the destination. If the destination can't be reached, the corresponding entry will
         contain float('inf').
    Time complexity: O(N * M * max(N, M)), complete traversal of maze will be done in the worst case. Here, N and M
    refer to the number of rows and columns of the maze. Further, for every current node chosen, we can travel up to a
    maximum depth of max(N, M) in any direction.
    Space complexity: O(N * M),  queue size can grow up to N * M in the worst case
    """
    n, m = len(maze), len(maze[0])
    distance = [[float('inf') for _ in range(m)] for _ in range(n)]
    distance[start[0]][start[1]] = 0
    queue = deque([(start[0], start[1])])
    while queue:
        i, j = queue.popleft()
        for x, y in (-1, 0), (1, 0), (0, -1), (0, 1):  # The 4 possible directions: up, down, left, right respectively
            new_i, new_j, d = i + x, j + y, 0  # Start from current position and move
            while 0 <= new_i < n and 0 <= new_j < m and maze[new_i][new_j] == 0:  # Moving CONTINUOUSLY until wall hit
                d += 1
                new_i += x
                new_j += y
            if distance[i][j] + d < distance[new_i - x][new_j - y]:  # If we've just reached this position in fewer
                # steps
                distance[new_i - x][new_j - y] = distance[i][j] + d  # Update the shortest distance to this position
                queue.append((new_i - x, new_j - y))  # Explore the remaining paths from there
    res = distance[destination[0]][destination[1]]
    return res if res != float('inf') else -1


def shortest_distance_v2(maze, start, destination):
    """ DFS. TLE
        In the average case, BFS would be a much better result because more paths will be pruned since the first few
        moves.
    """
    def dfs(i, j):
        for x, y in (-1, 0), (1, 0), (0, -1), (0, 1):
            new_i, new_j, d = i + x, j + y, 0
            while 0 <= new_i < n and 0 <= new_j < m and maze[new_i][new_j] == 0:
                d += 1
                new_i += x
                new_j += y
            if distance[i][j] + d < distance[new_i - x][new_j - y]:
                distance[new_i - x][new_j - y] = distance[i][j] + d
                dfs(new_i - x, new_j - y)

    n, m = len(maze), len(maze[0])
    distance = [[float('inf') for _ in range(m)] for _ in range(n)]
    distance[start[0]][start[1]] = 0
    dfs(start[0], start[1])
    res = distance[destination[0]][destination[1]]  # distance[i][j] again represents the minimum number of steps
    # required to reach the position (i,j) from the start position
    return res if res != float('inf') else -1


class Test(unittest.TestCase):
    data = [
        ([[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]], [0, 4], [4, 4], 12)]

    def test_shortest_distance(self):
        for test_maze, test_start, test_destination, result in self.data:
            self.assertEqual(result, shortest_distance_v1(test_maze, test_start, test_destination))
            self.assertEqual(result, shortest_distance_v2(test_maze, test_start, test_destination))


if __name__ == '__main__':
    unittest.main()