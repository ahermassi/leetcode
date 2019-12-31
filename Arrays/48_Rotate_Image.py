""" You are given an n x n 2D matrix representing an image.
Rotate the image by 90 degrees (clockwise).
Note:
You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate
another 2D matrix and do the rotation.
"""

import unittest2 as unittest


def rotate(matrix):
    """ The obvious idea would be to transpose the matrix first and then reverse each row. Transposing a matrix
        exchanges the row and column of the same index: 1st row becomes 1st column, 2nd row becomes 2nd column etc.
        Rotating the matrix by 90 degrees (clockwise) puts the 1st row to the last column, 2nd row to the 2nd-to-last
        column, etc.
        Clockwise rotate:
            First swap the symmetry, then reverse rows:
            1 2 3     1 4 7     7 4 1
            4 5 6  => 2 5 8  => 8 5 2
            7 8 9     3 6 9     9 6 3
        Anti-clockwise rotate:
            First swap the symmetry, then reverse the matrix:
            1 2 3     1 4 7     3 6 9
            4 5 6  => 2 5 8  => 2 5 8
            7 8 9     3 6 9     1 4 7

    Time complexity : O(N^2)
    Space complexity : O(1) since we do a rotation in place
    """
    n = len(matrix)
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()


class Test(unittest.TestCase):
    data = [([
                 [1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]
             ], [
                 [7, 4, 1],
                 [8, 5, 2],
                 [9, 6, 3]
             ]),
        ([
             [5, 1, 9, 11],
             [2, 4, 8, 10],
             [13, 3, 6, 7],
             [15, 14, 12, 16]
         ],
         [
             [15, 13, 2, 5],
             [14, 3, 4, 1],
             [12, 6, 8, 9],
             [16, 7, 10, 11]
         ]
        )]

    def test_rotate(self):
        for test_matrix, result in self.data:
            rotate(test_matrix)
            self.assertEqual(result, test_matrix)


if __name__ == '__main__':
    unittest.main()
