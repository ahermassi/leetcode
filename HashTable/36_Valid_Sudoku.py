""" Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be validated according to the following
rules:
    Each row must contain the digits 1-9 without repetition.
    Each column must contain the digits 1-9 without repetition.
    Each of the 9 3x3 sub-boxes of the grid must contain the digits 1-9 without repetition. """

from collections import defaultdict
import unittest2 as unittest


def is_valid_sudoku_v1(board):
    """ Iterate three times over the board to ensure that:

            1- There is no row with duplicates
            2- There is no column with duplicates
            3- There is no sub-box with duplicates

        In order to check 9 rows, 9 columns, and 9 boxes, we need to distinguish each of these entities. It is
        comparatively intuitive to check for duplicates in each row and column, given the row index i and column
        index j.

    Time complexity: O(1), as the number of iterations is fixed (9 X 9 board)
    Space complexity: O(1)
    """

    def is_valid_rows():
        for row in board:
            if not is_valid_unit(row):
                return False
        return True

    def is_valid_cols():
        for j in range(9):
            col = [board[i][j] for i in range(9)]
            if not is_valid_unit(col):
                return False
        return True

    def is_valid_unit(unit):
        values = set()
        for cell in unit:
            if cell == '.':
                continue
            if cell in values:
                return False
            values.add(cell)
        return True

    def is_valid_squares():
        # square1(x=0..2, y=0..2)
        # square2(x=0..2, y=3..5)
        # square3(x=0..2, y=6..8)
        # -> x = 0..2 = i..i+3, y = j..j+3
        #
        # square4(x=3..5, y=0..2)
        # square5(x=3..5, y=3..5)
        # square6(x=3..5, y=6..8)
        # -> x =3..5 = i..i+3, y = j..j+3
        #
        # square7(x=6..8, y=0..2)
        # square8(x=6..8, y=3..5)
        # square9(x=6..8, y=6..8)
        # -> x = 6..8 = i..i+3, y = j..j+3
        for i in (0, 3, 6):
            for j in (0, 3, 6):
                square = []
                for x in range(i, i + 3):
                    for y in range(j, j + 3):
                        square.append(board[x][y])
                if not is_valid_unit(square):
                    return False
        return True

    return is_valid_rows() and is_valid_cols() and is_valid_squares()


# Video explanation: https://youtu.be/TjFXEUCMqI8
def is_valid_sudoku_v2(board):
    """ One-pass solution.

        We can create a hash set for each row. For board[i][j], we check if the cell value already exists in the hash
        set corresponding to ith row. If it does, this row contains a duplicate value, therefore the sudoku is not
        valid. Otherwise, we proceed to check the next position until we finish scanning the whole sudoku board.
        The same logic can be applied to each column.

        The tricky part is when we check the validity of each box. The question is, given row index i and column
        index j, how to assign the position to one of the 9 boxes correctly?

        The first observation is that, in each column, rows 0, 1, and 2 belong to the same box, as do rows 3, 4, and 5,
        and rows 6, 7, and 8.

        What do they have in common? Every group of three belonging to the same box has the same value when we perform
        integer division by 3. Therefore, we can use i/3 to ensure that the rows are grouped as expected and use j/3 to
        ensure that the columns are grouped correctly. Then, (i/3, j/3) can uniquely mark each box, and we can directly
        use the tuple as the hash key if we want to create a hash set for each box.

    Time complexity: O(1)
    Space complexity: O(1)
    """
    rows = defaultdict(set)
    cols = defaultdict(set)
    squares = defaultdict(set)
    for i in range(9):
        for j in range(9):
            cell = board[i][j]
            if cell == '.':
                continue
            if cell in rows[i] or cell in cols[j]:
                return False
            square_key = (i // 3, j // 3)
            if cell in squares[square_key]:
                return False
            rows[i].add(cell)
            cols[j].add(cell)
            squares[square_key].add(cell)
    return True


class Test(unittest.TestCase):
    data = [([
                 ["5", "3", ".", ".", "7", ".", ".", ".", "."],
                 ["6", ".", ".", "1", "9", "5", ".", ".", "."],
                 [".", "9", "8", ".", ".", ".", ".", "6", "."],
                 ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
                 ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
                 ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                 [".", "6", ".", ".", ".", ".", "2", "8", "."],
                 [".", ".", ".", "4", "1", "9", ".", ".", "5"],
                 [".", ".", ".", ".", "8", ".", ".", "7", "9"]
             ], True),
        ([
             ["8", "3", ".", ".", "7", ".", ".", ".", "."],
             ["6", ".", ".", "1", "9", "5", ".", ".", "."],
             [".", "9", "8", ".", ".", ".", ".", "6", "."],
             ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
             ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
             ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
             [".", "6", ".", ".", ".", ".", "2", "8", "."],
             [".", ".", ".", "4", "1", "9", ".", ".", "5"],
             [".", ".", ".", ".", "8", ".", ".", "7", "9"]
         ], False)]

    def test_is_valid_sudoku(self):
        for test_board, result in self.data:
            self.assertEqual(result, is_valid_sudoku_v1(test_board))
            self.assertEqual(result, is_valid_sudoku_v2(test_board))


if __name__ == '__main__':
    unittest.main()
