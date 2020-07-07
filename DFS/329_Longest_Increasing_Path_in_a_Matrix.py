""" Given an integer matrix, find the length of the longest increasing path.
From each cell, you can either move to four directions: left, right, up or down. You may NOT move diagonally or move
outside of the boundary (i.e. wrap-around is not allowed). """

import unittest2 as unittest


def longest_increasing_path_v1(matrix):
    """ DFS can find the longest increasing path starting from any cell. We can do this for all the cells.
        Each cell can be seen as a vertex in a graph G. If two adjacent cells have values a < b, i.e. increasing then
        we have a directed edge (a, b). The problem then becomes:
            Search the longest path in the directed graph G
        Naively, we can use DFS or BFS to visit all the cells connected starting from a root. We update the maximum
        length of the path during search and find the answer when it finished.
        Cache the results for the recursion so that any sub-problem will be calculated only once.

        Usually, in DFS or BFS, we can employ a set 'visited' to prevent the cells from duplicate visits. We don't need
        it here because the path is increasing, so we will never visit a node with smaller value.
        The key observation is that the sequence is strictly increasing, so it can not have loops. So we have the
        following:
            longest(i,j) = longest increasing path from (i,j) to (k,l) + longest(k,l)
        Where longest(i,j) is longest increasing path starting from (i,j).
    Time complexity: O(N * M), each vertex/cell will be calculated once and only once, and each edge will be visited
    once and only once, the total time complexity is then O(V + E). V is the total number of vertices and E is the
    total number of edges. In our problem, O(V) = O(N * M), O(E) = O(4V) = O(N * M)
    Space complexity: O(N * M), the cache dominates the space complexity
    """

    def dfs(i, j):
        if (i, j) not in memo:
            res = 0
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and matrix[x][y] > matrix[i][j]:
                    res = max(res, dfs(x, y))
            memo[(i, j)] = res + 1  # Count oneself
        return memo[(i, j)]

    if not matrix:
        return 0
    n, m, res = len(matrix), len(matrix[0]), 0
    memo = {}
    for i in range(n):
        for j in range(m):
            res = max(res, dfs(i, j))
    return res


class Test(unittest.TestCase):
    data = [([[9, 9, 4], [6, 6, 8], [2, 1, 1]], 4), ([[3, 4, 5], [3, 2, 6], [2, 2, 1]], 4)]

    def test_longest_increasing_path(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, longest_increasing_path_v1(test_matrix))


if __name__ == '__main__':
    unittest.main()
