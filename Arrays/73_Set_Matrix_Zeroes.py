""" Given a m x n matrix, if an element is 0, set its entire row and column to 0. Do it in-place. """

import unittest2 as unittest


def set_zeroes_v1(matrix):
    """ If any cell of the matrix has a zero, we can record its row and column number. All the cells of this recorded
         row and column can be marked zero in the next pass.

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
    """ The additional use of space can be avoided by manipulating the original matrix instead.

         We iterate over the original array, and if we find an entry, say matrix[i][j], to be 0, then we iterate over
         row i and column j separately and set all the NON-ZERO elements to some dummy value (say 'a'). Note, choosing
         the right dummy value is dependent on the constraints of the problem. Any value outside the range of
         permissible values in the matrix will work as a dummy value.

         Finally, we iterate over the original matrix, and if we find an entry to be equal to the dummy value then we
         set the value in the cell to 0.

         Note that the dummy value is only assigned to non-zero elements because zero elements could entail further
         updates to the matrix later on, and by assigning a dummy value to them we're keeping these updates from
         occurring.

    Time complexity: O((N * M) * (N + M)), where N and M are the number of rows and columns respectively. Even though
    this solution avoids using space, it is very inefficient since in worst case for every cell we might have to zero
    out its corresponding row and column. Thus, for all (N * M) cells zeroing out (N + M) cells.
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


# Video explanation: https://www.youtube.com/watch?v=T41rL0L3Pnw

def set_zeroes_v3(matrix):
    """ The inefficiency in the previous approach is that we might be repeatedly setting a row or column even if it was
         set to zero already. We can avoid this by postponing the step of setting a row or a column to zeroes.

         We can rather use the first cell of every row and column as a flag. This flag would determine whether a row or
         column has been set to zero. This means for every cell instead of going to (N + M) cells and setting it to
         zero, we just set the flag in two cells.

        These flags are used later to update the matrix. If the first cell of a row is set to zero this means the row
        should be marked zero. If the first cell of a column is set to zero this means the column should be marked zero.

        We iterate over the matrix, and if matrix[i][j] == 0 we mark the first cell of the row i (matrix[i][0]) and
        the first cell of a column j (matrix[0][j]) as zeroes.

        The first cell of the first row and first column, i.e. matrix[0][0], is the same . Hence, we use an additional
        variable 'first_col_zero' to tell us if the first column had been marked or not and matrix[0][0] would be
        used to tell the same for the first row.

        After we're done marking, we iterate over the original matrix starting from second row and second column i.e.
        matrix[1][1] onwards. For every cell, we check if the row i or column j had been marked earlier by checking the
        respective first row cell (matrix[i][0]) or first column cell (matrix[0][j]). If any of them was marked, we set
        the value in the current cell to 0.

        We then check if matrix[0][0] == 0, if this is the case, we mark the first row as zero.

        Finally, we check if the first column was marked, and if it's the case we make all entries in it as zeros.

        Note how the first row and first column serve as the 'rows' and 'cols' sets that we used in the first approach.
        It means matrix[i][0] = 0 has the same meaning as 'i in rows' and matrix[0][j] = 0 has the same meaning
        as 'j in cols'.

        By placing the marker zeros in the first row and first column, there are two benefits. First, there is no
        confusion whether a zero is real or marker in the main chunk of the matrix. Second, confusion of marker zero and
        real zero in the first row and column can be resolved by additional markers with constant space.

        If we don't handle the first row separately, then if there is a zero in the row, we would mark matrix[0][0] as
        zero (based on our core logic), which means the first column would be set all to 0s later on when in fact it may
        not be required.

        Vice versa, if we don't treat the first column separately, if there is a zero in the column, we would also mark
        matrix[0][0] as zero, which means the first row would be set all to 0s later on when in fact it may not be
        required.

        In this solution, matrix[0][0] is whether row 0 should be zeroed out, first_col_zero is whether column 0 should
        be zeroed out, m[i][0] for i > 0 is whether row i should be zeroed out, and m[0][j] for j > 0 is whether column j
        should be zeroed out.

    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m = len(matrix), len(matrix[0])
    first_row_zero = False if matrix[0][0] else True
    first_col_zero = False
    for i in range(n):
        if matrix[i][0] == 0:  # The first cell of this row is zero, so the first column needs to be set to zero as well
            first_col_zero = True
        for j in range(1, m):
            if matrix[i][j] == 0:
                # If a cell is zero, we set the first element of the corresponding row and column to 0
                matrix[i][0] = matrix[0][j] = 0
    # Iterate over the matrix once again and using the first row and first column update the cells
    for i in range(1, n):
        for j in range(1, m):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if first_row_zero:  # See if the first row needs to be set to zero as well
        for j in range(m):
            matrix[0][j] = 0
    if first_col_zero:  # See if the first column needs to be set to zero as well
        for i in range(n):
            matrix[i][0] = 0


class Test(unittest.TestCase):
    data = [([[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
            ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])]

    def test_set_zeroes(self):
        for test_matrix, result in self.data:
            set_zeroes_v3(test_matrix)
            self.assertEqual(result, test_matrix)


if __name__ == '__main__':
    unittest.main()
