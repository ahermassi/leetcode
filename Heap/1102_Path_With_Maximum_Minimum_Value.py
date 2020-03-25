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


def maximum_minimum_path_v2(A):
    """ The intuition behind this solution is that the maximum of all scores of the different paths has to be less than
        or equal to the minimum of top-left cell and bottom-right cell. This is because the score of every path is the
        minimum value along that path, and every path starts from top-left and ends at bottom-right.
        We collect all the cells with value <= min(begin,end) and sort the list in ascending order.
        After that, we use binary search on that list and DFS to check whether there exists a path from begin to end
        such that this mid value is the the minimum among the values in that path (in other words, we check if the
        mid value in binary search is the score of a certain path in the grid).
        If yes, we keep on doing binary search to try to find a bigger value.
        Otherwise, we try to find a smaller value by moving the right pointer to the left.
        Why use DFS? We use DFS to check if there exists a path from begin to end.
        Why use Binary Search? We use binary search to find the upper boundary. So when we find a valid value, we move
        left pointer forward and try to find a larger value.
    Time complexity: Time complexity: O(N * M log(N * M))
    Space complexity: Time complexity: O(N * M)
    """

    def check(val):
        """ This function checks if there is a path from top-left to bottom-right such that 'val' is the score of
            that path (val <= every other value along the path)
        """

        def dfs(i, j):
            if i == n - 1 and j == m - 1:
                return True
            visited.add((i, j))
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < m and (x, y) not in visited and A[x][y] >= val and dfs(x, y):
                    return True
            return False

        visited = set()
        return dfs(0, 0)

    n, m = len(A), len(A[0])
    ceiling = min(A[0][0], A[-1][-1])
    candidates = set(A[i][j] for i in range(n) for j in range(m) if A[i][j] <= ceiling)
    candidates = sorted(list(candidates))
    left, right = 0, len(candidates) - 1
    while left <= right:
        mid = (left + right) // 2
        if check(candidates[mid]):
            left = mid + 1
        else:
            right = mid - 1
    return candidates[right]


class Test(unittest.TestCase):
    data = [([[5, 4, 5], [1, 2, 6], [7, 4, 6]], 4), ([[2, 2, 1, 2, 2, 2], [1, 2, 2, 2, 1, 2]], 2)]

    def test_maximum_minimum_path(self):
        for test_a, result in self.data:
            self.assertEqual(result, maximum_minimum_path_v1(test_a))
            self.assertEqual(result, maximum_minimum_path_v2(test_a))


if __name__ == '__main__':
    unittest.main()
