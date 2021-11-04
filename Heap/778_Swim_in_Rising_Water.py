""" You are given an n x n integer matrix grid where each value grid[i][j] represents the elevation at that point
(i, j).

The rain starts to fall. At time t, the depth of the water everywhere is t. You can swim from a square to another
4-directionally adjacent square if and only if the elevation of both squares individually are at most t. You can swim
infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.

Return the least time until you can reach the bottom right square (n - 1, n - 1) if you start at the top left
square (0, 0). """

from heapq import heappush, heappop


def swim_in_water_v1(grid):
    """ Let's first start with an explanation.
        At time t, all elements in the matrix that are less than or equal to t get a new value of t; all elements
        greater than t remain unchanged. So if the input is grid = [[0,1],[2,3]] at t=0, then at time t=1 the elements
        are [[1,1],[2,3]], and at t=2 the elements are [[2,2],[2,3]] and finally at t=3 [[3,3],[3,3]].

        What is the earliest time t coordinates (0,0) and (n-1,n-1) are connected?
        Two adjacent coordinates are connected if and only if their values are both less than or equal to t.
        We are looking for the smallest possible t.
        We can treat the initial values in grid as the land elevation "h". We can get through the land only when the
        water level "t" is higher than the land elevation. At time t, cells with elevation no more than t will be
        flooded, and the surface of water has height t, thus we can reach those cells by swimming.
        maximum value.

        From top-left to bottom-right, there are many paths. For each path, we have one maximum value. Let's find the
        minimum of such maximum values, i.e. the minimum maximum value in each path. This is the opposite of
        1102- Path with Maximum Minimum Value.

        When a problem asks us to find the best path when there is something quantifiable making certain paths worse
        than others, one natural option would be Dijkstra's algorithm or a variation of it. Dijkstra's algorithm uses
        a breadth-first search approach to a graph traversal, but it takes into account the weight/distance/difficulty
        of the different edges. In our case, the weight will be the time required to move to a particular cell.

        We'll need to use a min priority queue to store the possible moves at any point. These moves will be
        prioritized by how early they can be achieved (represented by the value in grid[i][j]).
        Starting at (0,0), we can iterate through the surrounding squares and enter them into our priority queue.
        After we've entered possible cell moves into the queue, we should mark them as seen so that we don't enter the
        same cell more than once.

        After we store the new possible moves, we then move to the next cell indicated by the priority queue,
        remembering to keep track of the largest cell value (priority) seen so far. We should repeat this process
        until we reach the end cell, and then we can return the result.

        Since the result is bounded by the largest value in the path, the strategy would be always picking the
        neighboring cell with the smallest value for the next step. So we can use a priority queue to take all
        neighboring cells as candidates for the next step, and each time we pop out the smallest one to move forward
        and update the maximum so far as well (it's actually the minimum maximum).
        Once we detect the destination as one of the neighboring cells, we finish the path and return the result.

    Time complexity: O(N^2 log(N^2) = O(N^2 * 2logN) ~= O(N^2 logN), we may expand O(N^2) nodes, and each one requires
    O(logN) time to perform the heap operations.
    Space complexity: O(N^2), the maximum size of the heap
    """
    n, m, visited, heap = len(grid), len(grid[0]), set(), []
    min_max_time = 0
    heappush(heap, (grid[0][0], 0, 0))
    visited.add((0, 0))
    while heap:
        val, i, j = heappop(heap)
        min_max_time = max(min_max_time, val)
        if i == n - 1 and j == m - 1:
            return min_max_time
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if 0 <= x < n and 0 <= y < m and (x, y) not in visited:
                heappush(heap, (grid[x][y], x, y))
                visited.add((x, y))
