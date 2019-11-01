""" Given a 2D matrix matrix, find the sum of the elements inside the rectangle defined by its upper left corner
(row1, col1) and lower right corner (row2, col2). """

import unittest2 as unittest


class NumMatrixV1(object):
    """ Brute force. TLE
        Each time sumRegion is called, we use a double for loop to sum all elements from(row1,col1) → (row2,col2).
    Time complexity: O(N * M) per query, where N and M represent the number of rows and columns respectively
    Space complexity: O(1)
    """

    def __init__(self, matrix):
        self.matrix = matrix

    def sumRegion(self, row1, col1, row2, col2):
        res = 0
        for i in range(row1, row2 + 1):
            for j in range(col1, col2 + 1):
                res += self.matrix[i][j]
        return res


class NumMatrixV2(object):
    """ Caching rows.
        Try to see the 2D matrix as mm rows of 1D arrays. To find the region sum, we just accumulate the sum in the
        region row by row.
    Time complexity: O(N) per query, O(N * M) for pre-calculation, where N and M represent the number of rows and
    columns respectively
    Space complexity: O(N * M) to store the cumulative sum of all rows
    """

    def __init__(self, matrix):
        if not matrix:
            return
        n, m = len(matrix), len(matrix[0])
        self.dp = [[0 for _ in range(m+1)] for _ in range(n)]
        for i in range(1, n):
            for j in range(1, m):
                self.dp[i][j+1] = self.dp[i][j] + matrix[i][j]

    def sumRegion(self, row1, col1, row2, col2):
        dp, res = self.dp, 0
        for i in range(row1, row2+1):
            res += dp[i][col2+1] - dp[i][col1]
        return res


class Test(unittest.TestCase):
    matrix = NumMatrixV1([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
    data = [(2, 1, 4, 3, 8), (1, 1, 2, 2, 11), (1, 2, 2, 4, 12)]

    def test_sum_region(self):
        for test_row1, test_col1, test_row2, test_col2, result in self.data:
            self.assertEqual(result, self.matrix.sumRegion(test_row1, test_col1, test_row2, test_col2))


if __name__ == '__main__':
    unittest.main()
