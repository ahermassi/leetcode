""" Given an integer matrix, find the length of the longest increasing path.
From each cell, you can either move to four directions: left, right, up or down. You may NOT move diagonally or move
outside of the boundary (i.e. wrap-around is not allowed). """

from collections import deque
import unittest2 as unittest


def longest_increasing_path_v1(matrix):
    """ DFS can find the longest increasing path starting from any cell. We can do this for all the cells.

        Each cell can be seen as a vertex in a graph G. If two adjacent cells have values a < b, i.e. increasing then
        we have a directed edge (a, b). The problem then becomes:

                            Search the longest path in the directed graph G

        Naively, we can use DFS or BFS to visit all the cells connected starting from a root. We update the maximum
        length of the path during search and find the answer when it finished.

        It is apparent that the naive brute force approach has:

            - Overlapping sub-problems: Once we calculate the optimal answer for a cell, we most probably have
              also recurred for its adjacent cells and calculated the optimal answers for them as well. There's no
              need to repeat the same calculations again.
            - Optimal substructure: The solutions of bigger problems can be calculated from optimal solutions of
              its sub-problems. So, if there's a longest path (optimal solution) for a given cell starting at that
              cell, all the cells in its path must also have optimal paths as well starting at those cells respectively.

        Therefore, we cache the results for the recursion so that any sub-problem will be calculated only once.

        Usually, in DFS or BFS, we can employ a set 'visited' to prevent the cells from duplicate visits. We don't need
        it here because the path is increasing, so we will never visit a node with smaller value. The key observation
        is that the sequence is strictly increasing, so it cannot have loops. So we have the following:

                        longest(i,j) = longest increasing path from (i,j) to (k,l) + longest(k,l)

        Where longest(i,j) is longest increasing path starting from (i,j).

    Time complexity: O(N * M), each vertex/cell will be calculated once and only once, and each edge will be visited
    once and only once, the total time complexity is then O(V + E). V is the total number of vertices and E is the
    total number of edges. In our problem, O(V) = O(N * M), O(E) = O(4V) = O(N * M)
    Space complexity: O(N * M), the cache dominates the space complexity
    """

    def dfs(i, j):
        if (i, j) not in memo:
            longest_path_from_neighbors = 0
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and matrix[x][y] > matrix[i][j]:
                    longest_path_from_neighbors = max(longest_path_from_neighbors, dfs(x, y))
            memo[(i, j)] = longest_path_from_neighbors + 1  # Count itself
        return memo[(i, j)]

    n, m, res = len(matrix), len(matrix[0]), 0
    memo = {}
    for i in range(n):
        for j in range(m):
            res = max(res, dfs(i, j))
    return res


def longest_increasing_path_v2(matrix):
    """ The result of each cell is related only to the result of its neighbors. Can we use Dynamic Programming?

        If we define the longest increasing path starting from cell (i, j) as a function f(i,j), then we have the
        following transition function:

                f(i,j) = 1 + max{f(x,y)∣(x,y) is a neighbor of (i,j) and matrix[x][y] > matrix[i][j]}

        This formula is the same as used in the previous approach. With such transition function, we may think that
        it is possible to use dynamic programming to deduce all the results without employing DFS!
        That is right with one thing missing: We don't have the dependency list.

        For dynamic programming to work, if problem B depends on the result of problem A, then we must make sure that
        problem A is calculated before problem B. Such order is natural and obvious for many problems. For example, the
        famous Fibonacci sequence:

                F(0) = 1, F(1) = 1, F(n) = F(n - 1) + F(n - 2)

        The sub-problem F(n) depends on its two predecessors. Therefore, the natural order from 0 to n is the correct
        order. The dependent is always behind the dependee.

        The terminology of such dependency order is Topological Order or Topological Sorting:

                Topological Sorting for Directed Acyclic Graph (DAG) is a linear ordering of vertices such
                that for every directed edge (u,v) vertex u comes before v in the ordering

        The idea is that in a DAG, we will have some vertices that don't depend on others which we call 'leaves'.
        We put these leaves in a list (their internal ordering does matter), and then we remove them from the DAG.
        After removal, there will be new leaves. We do the same repeatedly as if we are peeling an onion layer by
        layer. In the end, the list will have a valid topological ordering of our vertices.

        In our problem, we want the longest path in the DAG, which equals to the total number of layers of the 'onion'.
        Thus, we can count the number of layers during 'peeling' and return the count in the end.

        The logic is similar to 210- Course Schedule II.

    Time complexity: O(N * M), the topological sort is O(V + E) = O(N * M). V is the total number of vertices and
    E is the total number of edges. In our problem, O(V) = O(N * M), O(E) = O(4V) = O(N * M)
    Space complexity: O(N * M), we need to store the out degrees and each level of leaves in the queue
    """
    n, m = len(matrix), len(matrix[0])
    outdegree = [[0] * m for _ in range(n)]  # outdegree[i][j] is the number of adjacent cells greater than matrix[i][j]
    for i in range(n):
        for j in range(m):
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and matrix[x][y] > matrix[i][j]:
                    outdegree[i][j] += 1
    queue = deque([(i, j) for i in range(n) for j in range(m) if outdegree[i][j] == 0])
    length = 0
    while queue:
        size = len(queue)
        for _ in range(size):
            i, j = queue.popleft()
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):  # Immediate neighbors form the adjacency list
                # We're retrieving the nodes of the path backwards: from those with largest values to the smallest
                if 0 <= x < n and 0 <= y < m and matrix[x][y] < matrix[i][j]:
                    outdegree[x][y] -= 1
                    if outdegree[x][y] == 0:
                        queue.append((x, y))
        length += 1
    return length


def longest_increasing_path_v3(matrix):
    """ Topological Sort. Instead of counting the number of 'onion layers', for every node pushed into the queue we
        add the path length till that node. We keep track of the longest path seen so far in 'res' variable.
    """
    n, m = len(matrix), len(matrix[0])
    outdegree = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and matrix[x][y] > matrix[i][j]:
                    outdegree[i][j] += 1
    queue = deque([(i, j, 1) for i in range(n) for j in range(m) if outdegree[i][j] == 0])
    res = 0
    while queue:
        i, j, path_length = queue.popleft()
        res = max(res, path_length)
        for (x, y) in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if 0 <= x < n and 0 <= y < m and matrix[x][y] < matrix[i][j]:
                outdegree[x][y] -= 1
                if outdegree[x][y] == 0:
                    queue.append((x, y, path_length + 1))
    return res


class Test(unittest.TestCase):
    data = [([[9, 9, 4], [6, 6, 8], [2, 1, 1]], 4), ([[3, 4, 5], [3, 2, 6], [2, 2, 1]], 4)]

    def test_longest_increasing_path(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, longest_increasing_path_v1(test_matrix))
            self.assertEqual(result, longest_increasing_path_v2(test_matrix))


if __name__ == '__main__':
    unittest.main()
