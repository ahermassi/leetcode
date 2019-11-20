""" Given a matrix of m x n elements (m rows, n columns), return all elements of the matrix in spiral order. """

import unittest2 as unittest


def spiral_order_v1(matrix):
    """ Take the first row plus the spiral order of the rotated remaining matrix.
        Here's how the matrix changes by always extracting the first row and rotating the remaining matrix
        counter-clockwise:
        |1 2 3|      |6 9|      |8 7|      |4|  =>  |5|  =>  ||
        |4 5 6|  =>  |5 8|  =>  |5 4|  =>  |5|
        |7 8 9|      |4 7|
        Now look at the first rows we extracted:
        |1 2 3|      |6 9|      |8 7|      |4|      |5|
        Those concatenated are the desired result.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    res = []
    while matrix:
        res.extend(matrix.pop(0))
        matrix = list(zip(*matrix))[::-1]
    return res


def spiral_order_v2(matrix):
    """ Walk through an example to better understand this solution. Peel off layers.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    res = []
    while matrix:
        res.extend(matrix.pop(0))
        if matrix and matrix[0]:
            for row in matrix:
                res.append(row.pop())
        if matrix:
            res.extend(matrix.pop()[::-1])
        if matrix and matrix[0]:
            for row in matrix[::-1]:
                res.append(row.pop(0))
    return res


def spiral_order_v3(matrix):
    """ We simulate peeling off the layers as in the previous solution, but without modifying the input matrix.
        We traverse right and increment row_begin, then traverse down and decrement col_end, then we traverse left
        and decrement row_end, and finally we traverse up and increment col_begin.
        Note that row_begin, row_end, col_begin, col_end are the boundaries of rows and columns.
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    if not matrix:
        return None
    row_begin, row_end = 0, len(matrix) - 1
    col_begin, col_end = 0, len(matrix[0]) - 1
    res = []
    while row_begin <= row_end and col_begin <= col_end:
        # Traverse Right
        for i in range(col_begin, col_end + 1):
            res.append(matrix[row_begin][i])
        row_begin += 1
        # Traverse Down
        for i in range(row_begin, row_end + 1):
            res.append(matrix[i][col_end])
        col_end -= 1
        # Traverse Left
        if row_begin <= row_end:
            for i in reversed(range(col_begin, col_end + 1)):
                res.append(matrix[row_end][i])
        row_end -= 1
        # Traverse Up
        if col_begin <= col_end:
            for i in reversed(range(row_begin, row_end + 1)):
                res.append(matrix[i][col_begin])
        col_begin += 1
    return res


class Test(unittest.TestCase):
    data = [([[
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ],
        [1, 2, 3, 6, 9, 8, 7, 4, 5]]),
        ([
             [1, 2, 3, 4],
             [5, 6, 7, 8],
             [9, 10, 11, 12]
         ], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])]

    def test_spiral_order(self):
        for test_array, result in self.data:
            self.assertEqual(result, spiral_order_v1(test_array))
            self.assertEqual(result, spiral_order_v3(test_array))


if __name__ == '__main__':
    unittest.main()
