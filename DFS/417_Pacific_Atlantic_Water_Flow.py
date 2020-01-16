""" Given an m x n matrix of non-negative integers representing the height of each unit cell in a continent, the
"Pacific ocean" touches the left and top edges of the matrix and the "Atlantic ocean" touches the right and bottom
edges.
Water can only flow in four directions (up, down, left, or right) from a cell to another one with height equal or lower.
Find the list of grid coordinates where water can flow to both the Pacific and Atlantic ocean. """

from collections import deque
import unittest2 as unittest


def pacific_atlantic_v1(matrix):
    """ The water on the continent (in the matrix) wants to flow out in the ocean. Water can advance only to positions
        with values the same or lower as the current position value.
        We do not need to scan the entire matrix to find the starting point of DFS. We essentially can find all points
        from where water can get to the ocean by starting DFS at the border. Cells on the border (first/last row, and
        first/last column) are guaranteed to get into the ocean. We start off with the border cells and go from there
        to explore the inner land. The logic is similar to 130- Surrounded Regions.
        Since water can only flow from higher/equal cell to lower cell, we dfs the neighbor cells with height higher
        than or equal to current cell and mark as visited.
        Maintain two boolean matrices for the two oceans, where ocean[i][j] indicates whether the cell matrix[i][j] can
        reach the ocean. Finally go through all cells again and see if each cell can reach both oceans.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def dfs(i, j, ocean):
        ocean[i][j] = True  # matrix[i][j] can reach this ocean
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if not 0 <= x < n or not 0 <= y < m or matrix[x][y] < matrix[i][j] or ocean[x][y]:
                continue
            dfs(x, y, ocean)

    if not matrix:
        return None
    n, m, res = len(matrix), len(matrix[0]), []
    pacific = [[False] * m for _ in range(n)]
    atlantic = [[False] * m for _ in range(n)]
    for i in range(n):
        dfs(i, 0, pacific)  # Left border
        dfs(i, m - 1, atlantic)  # Right border
    for j in range(m):
        dfs(0, j, pacific)  # Top border
        dfs(n - 1, j, atlantic)  # Bottom border
    for i in range(n):
        for j in range(m):
            if pacific[i][j] and atlantic[i][j]:
                res.append([i, j])
    return res


def pacific_atlantic_v2(matrix):
    """ BFS version of the previous algorithm. We add the border cells to a single queue and start a BFS from those
        cells.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    if not matrix:
        return None
    n, m, res = len(matrix), len(matrix[0]), []
    pacific = [[False] * m for _ in range(n)]
    atlantic = [[False] * m for _ in range(n)]
    queue = deque()
    for i in range(n):
        queue.extend([(i, 0, pacific), (i, m - 1, atlantic)])
    for j in range(m):
        queue.extend([(0, j, pacific), (n - 1, j, atlantic)])
    while queue:
        i, j, ocean = queue.popleft()
        ocean[i][j] = True
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if not 0 <= x < n or not 0 <= y < m or matrix[x][y] < matrix[i][j] or ocean[x][y]:
                continue
            queue.append((x, y, ocean))
    for i in range(n):
        for j in range(m):
            if pacific[i][j] and atlantic[i][j]:
                res.append([i, j])
    return res


def pacific_atlantic_v3(matrix):
    """ BFS using a separate queue for each ocean.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def bfs(queue, ocean):
        while queue:
            i, j = queue.popleft()
            ocean[i][j] = True
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if not 0 <= x < n or not 0 <= y < m or matrix[x][y] < matrix[i][j] or ocean[x][y]:
                    continue
                queue.append((x, y))

    if not matrix:
        return None
    n, m, res = len(matrix), len(matrix[0]), []
    pacific = [[False] * m for _ in range(n)]
    atlantic = [[False] * m for _ in range(n)]
    pacific_queue = deque()
    atlantic_queue = deque()
    for i in range(n):
        pacific_queue.append((i, 0))
        atlantic_queue.append((i, m - 1))
    for j in range(m):
        pacific_queue.append((0, j))
        atlantic_queue.append((n - 1, j))
    bfs(pacific_queue, pacific)
    bfs(atlantic_queue, atlantic)
    for i in range(n):
        for j in range(m):
            if pacific[i][j] and atlantic[i][j]:
                res.append([i, j])
    return res


class Test(unittest.TestCase):
    data = [([[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]],
             [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]])]

    def test_pacific_atlantic(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, pacific_atlantic_v1(test_matrix))
            self.assertEqual(result, pacific_atlantic_v2(test_matrix))
            self.assertEqual(result, pacific_atlantic_v3(test_matrix))


if __name__ == '__main__':
    unittest.main()
