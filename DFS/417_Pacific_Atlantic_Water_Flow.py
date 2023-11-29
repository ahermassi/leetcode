""" Given an m x n matrix of non-negative integers representing the height of each unit cell in a continent, the
"Pacific ocean" touches the left and top edges of the matrix and the "Atlantic ocean" touches the right and bottom
edges.
Water can only flow in four directions (up, down, left, or right) from a cell to another one with height equal or lower.
Find the list of grid coordinates where water can flow to both the Pacific and Atlantic ocean. """

from collections import deque
import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=s-VkcjHqkGI
def pacific_atlantic_v1(heights):
    """ Matrices such as this one are a type of graph representation. Standard graph traversal algorithms such as BFS
         and DFS can be used to solve this problem.

         The naive approach would be to check every cell - that is, iterate through every cell, and at each one, start a
         traversal that follows the problem's conditions. That is, find every cell that manages to reach both oceans.

         This approach, however, is extremely slow, as it repeats a ton of computation. Instead of looking for every
         path from cell to ocean, let's start at the oceans and try to work our way to the cells. This will be much
         faster because when we start a traversal at a cell, whatever result we end up with can be applied to only that
         cell. However, when we start from the ocean and work backwards, we already know that every cell we visit MUST
         be connected to the ocean.

         The logic is similar to 130- Surrounded Regions.

         If we start traversing from the ocean and flip the condition (check for higher height instead of lower height),
         then we know that every cell we visit during the traversal can flow into that ocean.

         The pattern here is that instead of starting from a certain point and then extending outwards to see if any of
         those paths actually reaches the goal, we instead start at the goal and then figure out if it's possible to
         reach a starting point.

        Let's start a DFS traversal from every cell that is immediately beside the Pacific Ocean, and figure out what
        cells can flow into the Pacific. Then, let's do the exact same thing with the Atlantic Ocean. At the end, the
        cells that end up connected to both oceans will be our answer.

        We maintain two hash sets for the two oceans, 'can_flow_to_pacific' and 'can_flow_to_atlantic', where if (i,j)
        is in can_flow_to_ocean means that the cell (i, j) can reach the ocean, which we also use to keep track of the
        cells we already visited to avoid infinite loops.

        Note that the DFS method will be called only for REACHABLE cells.

        Summary:

        If we start from the cells connected to the Atlantic Ocean and visit all cells having height greater than
        current cell (water can only flow from a cell to another one with height equal or lower), we are able to reach
        some subset of cells (let's call them A).
        Next, we start from the cells connected to the Pacific Ocean and repeat the same process, we find another subset
        (let's call this one B).
        The final answer we need will be the intersection of sets A and B

    Time complexity: O(N * M), in the worst case such as a matrix where every value is equal, we would visit every cell
    twice. This is because we perform 2 traversals, and during each traversal, we visit each cell exactly once.
    There are N * M cells total, which gives us a time complexity of O(2 * N * M) = O(N * M)
    Space complexity: O(N * M)
    """

    def dfs(i, j, can_flow_to_ocean):
        can_flow_to_ocean.add((i,j))  # This cell is reachable, so mark it.
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            # Check that the new cell is within bounds, hasn't already been visited, and has a higher or equal
            # height, so that water can flow from the new cell to the old cell
            if 0 <= x < n and 0 <= y < m and (x,y) not in can_flow_to_ocean and heights[x][y] >= heights[i][j]:
                # If we've gotten this far, that means the new cell is reachable
                dfs(x, y, can_flow_to_ocean)

    n, m, res = len(heights), len(heights[0]), []
    can_flow_to_pacific, can_flow_to_atlantic = set(), set()
    for i in range(n):
        dfs(i, 0, can_flow_to_pacific)  # Left border
        dfs(i, m-1, can_flow_to_atlantic)  # Right border
    for j in range(m):
        dfs(0, j, can_flow_to_pacific)  # Top border
        dfs(n-1, j, can_flow_to_atlantic)  # Bottom border
    for i in range(n):
        for j in range(m):
            # Find all cells that can reach both oceans
            if (i,j) in can_flow_to_pacific and (i,j) in can_flow_to_atlantic:
                res.append([i, j])
    return res


def pacific_atlantic_v2(heights):
    """ We can also use BFS, and it doesn't really make much of a difference.

         BFS is very similar to DFS. Instead of using recursion, we'll use a queue and work iteratively for every
         reachable cell. We start by collecting the cells that border the Pacific and Atlantic oceans into a queue.
         Then, we iteratively figure out what cells can flow into one of or both oceans.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m, res = len(heights), len(heights[0]), []
    can_flow_to_pacific = [[False] * m for _ in range(n)]
    can_flow_to_atlantic = [[False] * m for _ in range(n)]
    queue = deque()
    for i in range(n):
        queue.append((i, 0, heights[i][0], can_flow_to_pacific))
        queue.append((i, m - 1, heights[i][m - 1], can_flow_to_atlantic))
    for j in range(m):
        queue.append((0, j, heights[0][j], can_flow_to_pacific))
        queue.append((n - 1, j, heights[n - 1][j], can_flow_to_atlantic))
    while queue:
        i, j, prev_height, can_flow_to_ocean = queue.popleft()
        if not 0 <= i < n or not 0 <= j < m or heights[i][j] < prev_height or can_flow_to_ocean[i][j]:
            continue
        can_flow_to_ocean[i][j] = True
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            queue.append((x, y, heights[i][j], can_flow_to_ocean))
    for i in range(n):
        for j in range(m):
            if can_flow_to_pacific[i][j] and can_flow_to_atlantic[i][j]:
                res.append([i, j])
    return res


def pacific_atlantic_v3(heights):
    """ BFS using a separate queue for each ocean.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def bfs(queue, can_flow_to_ocean):
        while queue:
            i, j, prev_height = queue.popleft()
            if not 0 <= i < n or not 0 <= j < m or heights[i][j] < prev_height or can_flow_to_ocean[i][j]:
                continue
            can_flow_to_ocean[i][j] = True
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                queue.append((x, y, heights[i][j]))

    n, m, res = len(heights), len(heights[0]), []
    can_flow_to_pacific = [[False] * m for _ in range(n)]
    can_flow_to_atlantic = [[False] * m for _ in range(n)]
    pacific_queue = deque()
    atlantic_queue = deque()
    for i in range(n):
        pacific_queue.append((i, 0, heights[i][0]))
        atlantic_queue.append((i, m - 1, heights[i][m - 1]))
    for j in range(m):
        pacific_queue.append((0, j, heights[0][j]))
        atlantic_queue.append((n - 1, j, heights[n - 1][j]))
    bfs(pacific_queue, can_flow_to_pacific)
    bfs(atlantic_queue, can_flow_to_atlantic)
    for i in range(n):
        for j in range(m):
            if can_flow_to_pacific[i][j] and can_flow_to_atlantic[i][j]:
                res.append([i, j])
    return res


def pacific_atlantic_v4(heights):
    """ We can replace the two boolean matrices with two hash sets where we collect the coordinates of the cells that
         can flow into each of the oceans . The answer is the intersection of the sets.

         Note that this is applicable to both DFS and BFS algorithms.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(heights), len(heights[0])
    can_flow_to_pacific = set()
    can_flow_to_atlantic = set()
    queue = deque()
    for i in range(n):
        queue.append((i, 0, heights[i][0], can_flow_to_pacific))
        queue.append((i, m - 1, heights[i][m - 1], can_flow_to_atlantic))
    for j in range(m):
        queue.append((0, j, heights[0][j], can_flow_to_pacific))
        queue.append((n - 1, j, heights[n - 1][j], can_flow_to_atlantic))
    while queue:
        i, j, prev_height, can_flow_to_ocean = queue.popleft()
        if not 0 <= i < n or not 0 <= j < m or heights[i][j] < prev_height or (i, j) in can_flow_to_ocean:
            continue
        can_flow_to_ocean.add((i, j))
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            queue.append((x, y, heights[i][j], can_flow_to_ocean))
    return list(can_flow_to_pacific & can_flow_to_atlantic)


class Test(unittest.TestCase):
    data = [([[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]],
             [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]])]

    def test_pacific_atlantic(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, pacific_atlantic_v1(test_matrix))
            self.assertEqual(result, pacific_atlantic_v2(test_matrix))
            self.assertEqual(result, pacific_atlantic_v3(test_matrix))
            self.assertEqual(result, pacific_atlantic_v4(test_matrix))


if __name__ == '__main__':
    unittest.main()
