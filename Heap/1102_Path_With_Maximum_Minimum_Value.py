""" Given a matrix of integers A with R rows and C columns, find the maximum score of a path starting at [0,0] and
ending at [R-1,C-1].
The score of a path is the minimum value in that path.  For example, the value of the path 8 →  4 →  5 →  9 is 4.
A path moves some number of times from one visited cell to any neighbouring unvisited cell in one of the 4 cardinal
directions (north, east, west, south). """

from heapq import heappush, heappop
import unittest2 as unittest


def maximum_minimum_path_v1(A):
    """ Use a max heap to choose the next step with the maximum value. Keep track of the minimum value along the path
        which is the score of that path.
    Time complexity: O(N * M log(N * M)), since for each element in matrix we have to do a heap push, which costs
    O(log # of element in the heap), the size of the heap can grow up to # of elements in the matrix
    Space complexity: O(N * M)
    """
    n, m, visited, heap = len(A), len(A[0]), set(), []
    max_score = A[0][0]
    heappush(heap, (-A[0][0], 0, 0))
    visited.add((0, 0))
    while heap:
        val, i, j = heappop(heap)
        max_score = min(max_score, -val)
        if i == n - 1 and j == m - 1:
            return max_score
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if 0 <= x < n and 0 <= y < m and (x, y) not in visited:
                heappush(heap, (-A[x][y], x, y))
                visited.add((x, y))


class Test(unittest.TestCase):
    data = [([[5, 4, 5], [1, 2, 6], [7, 4, 6]], 4), ([[2, 2, 1, 2, 2, 2], [1, 2, 2, 2, 1, 2]], 2)]

    def test_maximum_minimum_path(self):
        for test_a, result in self.data:
            self.assertEqual(result, maximum_minimum_path_v1(test_a))


if __name__ == '__main__':
    unittest.main()
