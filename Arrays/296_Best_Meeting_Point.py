""" Given an m x n binary grid grid where each 1 marks the home of one friend, return the minimal total travel distance.

The total travel distance is the sum of the distances between the houses of the friends and the meeting point.

The distance is calculated using Manhattan Distance, where distance(p1, p2) = |p2.x - p1.x| + |p2.y - p1.y|. """

from collections import deque


def min_total_distance_v1(grid):
    """ Breadth-First Search. TLE

        A brute force approach is to evaluate all possible meeting points in the grid. We could apply breadth-first
        search originating from each of the points. While inserting a point into the queue, we need to record the
        distance of that point from the meeting point. Also, we need an extra visited hash set to record which point
        had already been visited to avoid being inserted into the queue again.

    Time complexity: O(N^2 * M^2), for each point in the N x M grid, the breadth-first search takes at most N x M
    steps to reach all points
    Space complexity: O(N * M), the visited set consists of N x M elements to map each point in the grid. We insert at
    most N x M points into the queue.
    """
    n, m = len(grid), len(grid[0])
    res = float('inf')
    for i in range(n):
        for j in range(m):
            # Start a BFS from this cell and try to reach all the houses. The best meeting point can be an empty cell
            # as well as a house, that's why we do a BFS from every cell on the grid.
            queue = deque([(i, j, 0)])
            visited = {(i, j)}
            total_distance = 0
            while queue:
                x, y, distance = queue.popleft()
                if grid[x][y] == 1:
                    total_distance += distance
                for a, b in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
                    if 0 <= a < n and 0 <= b < m and (a, b) not in visited:
                        visited.add((a, b))
                        queue.append((a, b, distance + 1))
            res = min(res, total_distance)
    return res if res != float('inf') else 1
