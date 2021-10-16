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


def min_total_distance_v2(grid):
    """ Finding the best meeting point in a 2D grid seems difficult. Let us take a step back and solve the 1D case
        which is much simpler. Notice that the Manhattan distance is the sum of two independent variables. Therefore,
        once we solve the 1D case, we can solve the 2D case as two independent 1D problems.

        Suppose we have N people living on a straight street and they want to find somewhere to meet. The total
        distance is:
            Σ |x_i - m|
            i
        where x_i is the location of each house and m is the meeting point. To minimize this problem, take the
        derivative of this equation. Each term will give:
            1,  if x_i > m
            -1, if x_i < m

        To reach the minimum, the derivative must be 0. To make the derivative 0, the number of 1s and -1s must be
        equal.
        If n is even, then m must be located between the middle two locations (any location between them will give
        the minimum, not necessarily the median).
        If n is odd, then m must be located on the middle one house. That's the median.

        Then we can discuss the 2D case. Let's write down the equation directly:
            Σ |x_i - m| + |y_i - n|
            i
        So this time, we have two variables, m and n. To find the minimum, we need to take the partial derivatives
        for the equation, and each partial derivative (or we can say, each dimension) will give the same result as the
        1D case.

        We simply find the list of x and y coordinates where we have a house. Then we individually sort them to find
        the median element in each list. This is the best meeting point (x_median, y_median).
        To find the total walking distance, simply add abs(x_median - x) and abs(y_median - y) to the final result,
        where (x, y) are the coordinates of each of the houses.

    Time complexity: O(N * M * log(N * M)), in the worst-case where all elements in the grid are 1s, then both 'rows'
    and 'cols' would be arrays of size N * M; sorting the arrays takes O(N * M * log(N * M))
    Space complexity: O(N * M)
    """
    n, m = len(grid), len(grid[0])
    rows, cols = [], []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                rows.append(i)
                cols.append(j)
    x_median = rows[len(rows) // 2]  # We do not need to sort the rows indices as we collected them in sorted order
    y_median = sorted(cols)[len(cols) // 2]
    distance = 0
    for x in rows:
        distance += abs(x - x_median)
    for y in cols:
        distance += abs(y - y_median)
    return distance

