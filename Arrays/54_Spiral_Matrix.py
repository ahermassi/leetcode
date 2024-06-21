""" Given a matrix of m x n elements (m rows, n columns), return all elements of the matrix in spiral order. """

import unittest2 as unittest


# def spiral_order_v1(matrix):
#     """ Take the first row plus the spiral order of the rotated remaining matrix.
#
#         Here's how the matrix changes by always extracting the first row and rotating the remaining matrix
#         counter-clockwise:
#
#         |1 2 3|         |6 9|         |8 7|         |4|  =>  |5|  =>  ||
#         |4 5 6|  =>  |5 8|  =>  |5 4|  =>  |5|
#         |7 8 9|         |4 7|
#
#         Now look at the first rows we extracted:
#
#         |1 2 3|      |6 9|      |8 7|      |4|      |5|
#
#         Those concatenated are the desired result.
#     Time complexity: O(N * M)
#     Space complexity: O(N * M)
#     """
#     res = []
#     while matrix:
#         res.extend(matrix.pop(0))
#         matrix = list(zip(*matrix))[::-1]
#     return res


def spiral_order_v2(matrix):
    """ Peel off layers. Process the array in ‘shells' from the outside moving to the center.

        We go boundary by boundary and move inwards. That is the essential operation. First row, last column, last row
        in reverse order, first column in reverse order, and then we move inwards by 1 and then repeat.
        That is all the simulation we need.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    res = []
    while matrix:
        res.extend(matrix.pop(0)) # First row
        if matrix and matrix[0]:
            for row in matrix:
                res.append(row.pop()) # Last column == last element of each row
        if matrix:
            res.extend(matrix.pop()[::-1]) # Last row in reverse order
        if matrix and matrix[0]:
            # First column in reverse order. First column == first element of each row
            for row in matrix[::-1]:
                res.append(row.pop(0))
    return res


# Video explanation: https://www.youtube.com/watch?v=BJnMZNwUk1M
def spiral_order_v3(matrix):
    """ We simulate peeling off the layers as in the previous solution, but without modifying the input matrix.

        We process entries in the sequence (Ro,Co), (R0,C1), …  (R0,Cn-1), i.e., we are moving to the right.
        Then we process entries (Ro,Cn-1), (R1,Cn-1), …, (Rn-1,Cn-.1)., i.e., we are moving down.
        Then we process entries (Rn-1,Cn-2), (Rn-1,Cn-3), …  (Rn-1,C0), i.e., we are moving to the left.
        Then we process entries (Rn-2,C0), (Rn-3,C0), …, (R1,C0), i.e., we are moving up.
        This method is applied until all elements are processed. Conceptually, we are processing the array in ‘shells'
        from the outside moving to the center.

        We can achieve moving in different directions by modifying row and column indices. Given that we are at
        (row, col), where row is the row index, and col is the column index, we have:

                move right: (row, col + 1)
                move downwards: (row + 1, col)
                move left: (row, col - 1)
                move upwards: (row - 1, col)

        When shall we change our direction? We need to turn when we either reach the matrix boundaries, or we reach the
        cells in the array that we have visited before. Matrix boundaries are fixed and provided already, but how could
        we know if we have visited a particular cell or not?

        We can move the boundaries towards the center of the matrix after we have traversed a row or a column.
        Then, when we meet a boundary, we know it's time to change the direction and update the boundary.

        Let's define row_begin, row_end, col_begin, col_end as the boundaries of rows and columns.

        We traverse right and increment row_begin, then traverse down and decrement col_end, then we traverse left
        and decrement row_end, and finally we traverse up and increment col_begin.

        Before we traverse from right to left, we need to make sure that we are not on a row that has already been
        traversed. If we are not, then we can traverse from right to left.
        Similarly, before we traverse upwards, we need to make sure that we are not on a column that has already been
        traversed. Then we can traverse from down to up.

        These checks avoid repeating the right-to-left or down-to-up scan if there is only 1 row or column in the
        matrix.
        First, (row_begin <= row_end) will return false if there is only 1 row, so no need to scan right-to-left.
        Then, (col_begin <= col_end) will return false if there is only 1 column, so no need to scan down-to-up.

    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    row_begin, row_end = 0, len(matrix) - 1
    col_begin, col_end = 0, len(matrix[0]) - 1
    res = []
    while row_begin <= row_end and col_begin <= col_end:
        # Traverse from left to right
        for j in range(col_begin, col_end + 1):
            res.append(matrix[row_begin][j])
        row_begin += 1
        # Traverse downwards
        for i in range(row_begin, row_end + 1):
            res.append(matrix[i][col_end])
        col_end -= 1
        # Traverse from right to left
        if row_begin <= row_end:
            for j in reversed(range(col_begin, col_end + 1)):
                res.append(matrix[row_end][j])
        row_end -= 1
        # Traverse upwards
        if col_begin <= col_end:
            for i in reversed(range(row_begin, row_end + 1)):
                res.append(matrix[i][col_begin])
        col_begin += 1
    return res


def spiral_order_v4(matrix):
    """ We can avoid the boundary checks of the previous simulation if we use a direction variable.

    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    row_begin, row_end = 0, len(matrix) - 1
    col_begin, col_end = 0, len(matrix[0]) - 1
    direction = 0
    res = []
    while row_begin <= row_end and col_begin <= col_end:
        if direction == 0:
            for j in range(col_begin, col_end + 1):
                res.append(matrix[row_begin][j])
            row_begin += 1
        elif direction == 1:
            for i in range(row_begin, row_end + 1):
                res.append(matrix[i][col_end])
            col_end -= 1
        elif direction == 2:
            for j in reversed(range(col_begin, col_end + 1)):
                res.append(matrix[row_end][j])
            row_end -= 1
        else:
            for i in reversed(range(row_begin, row_end + 1)):
                res.append(matrix[i][col_begin])
            col_begin += 1
        direction = (direction + 1) % 4
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
            self.assertEqual(result, spiral_order_v3([test_array]))


if __name__ == '__main__':
    unittest.main()
