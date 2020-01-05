""" Given a m x n matrix, if an element is 0, set its entire row and column to 0. Do it in-place. """

import unittest2 as unittest


def set_zeroes_v1(matrix):
    """ If any cell of the matrix has a zero we can record its row and column number. All the cells of this recorded
        row and column can be marked zero in the next iteration.
        We make a pass over our original array and look for zero entries.
        If we find that an entry at [i, j] is 0, then we need to record somewhere the row i and column j.
        Finally, we iterate over the original matrix. For every cell we check if the row r or column c had been marked
        earlier. If any of them was marked, we set the value in the cell to 0.
    Time complexity: O(N * M), where N and M are the number of rows and columns respectively
    Space complexity: O(N + M), since we're only recording the indices of rows and columns in the two hash sets
    """
    n, m = len(matrix), len(matrix[0])
    rows, cols = set(), set()
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 0:
                rows.add(i)
                cols.add(j)
    for i in range(n):
        for j in range(m):
            if i in rows or j in cols:
                matrix[i][j] = 0


def set_zeroes_v2(matrix):
    """ The additional use of space can be avoided by manipulating the original array instead.
        We iterate over the original array, and if we find an entry, say cell[i][j], to be 0, then we iterate over
        row i and column j separately and set all the NON ZERO elements to some dummy value (say 'a'). Note, choosing
        the right dummy value for our solution is dependent on the constraints of the problem. Any value outside the
        range of permissible values in the matrix will work as a dummy value.
        Finally, we iterate over the original matrix, and if we find an entry to be equal to the dummy value then we
        set the value in the cell to 0.
        Note that the dummy value is only assigned to non zero elements because zero elements could entail further
        updates to the matrix later on, and by assigning a dummy value of them we're keeping these updates from
        occurring.
    Time complexity: O((N * M) * (N + M)), where N and M are the number of rows and columns respectively. Even though
    this solution avoids using space, it is very inefficient since in worst case for every cell we might have to zero
    out its corresponding row and column. Thus for all (N * M) cells zeroing out (N + M) cells.
    Space complexity: O(1)
    """
    n, m = len(matrix), len(matrix[0])
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 0:
                for k in range(n):
                    matrix[k][j] = 'a' if matrix[k][j] != 0 else 0
                for k in range(m):
                    matrix[i][k] = 'a' if matrix[i][k] != 0 else 0
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 'a':
                matrix[i][j] = 0


class Test(unittest.TestCase):
    data = [([[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
            ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])]

    def test_set_zeroes(self):
        for test_matrix, result in self.data:
            set_zeroes_v1(test_matrix)
            self.assertEqual(result, test_matrix)


if __name__ == '__main__':
    unittest.main()
