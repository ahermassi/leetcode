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


class Test(unittest.TestCase):
    matrix = NumMatrixV1([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
    data = [(2, 1, 4, 3, 8), (1, 1, 2, 2, 11), (1, 2, 2, 4, 12)]

    def test_sum_region(self):
        for test_row1, test_col1, test_row2, test_col2, result in self.data:
            self.assertEqual(result, self.matrix.sumRegion(test_row1, test_col1, test_row2, test_col2))


if __name__ == '__main__':
    unittest.main()
