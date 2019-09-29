""" Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be validated according to the following
rules:
    Each row must contain the digits 1-9 without repetition.
    Each column must contain the digits 1-9 without repetition.
    Each of the 9 3x3 sub-boxes of the grid must contain the digits 1-9 without repetition. """

import unittest2 as unittest


def is_valid_sudoku_v1(board):
    """ Iterate three times over the board to ensure that :
            There is no rows with duplicates.
            There is no columns with duplicates.
            There is no sub-boxes with duplicates.
    Time complexity: O(1) as the number of iterations is known in advance (9 X 9 board)
    Space complexity: O(1)
    """

    def valid_rows(board):
        for row in board:
            if not is_valid(row):
                return False
        return True

    def valid_cols(board):
        for col in zip(*board):
            if not is_valid(col):
                return False
        return True

    def valid_squares(board):
        for i in (0, 3, 6):
            for j in (0, 3, 6):
                square = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if not is_valid(square):
                    return False
        return True

    def is_valid(row):
        d = {}
        for cell in row:
            if cell != '.' and cell in d:
                return False
            d[cell] = 1
        return True

    return valid_rows(board) and valid_cols(board) and valid_squares(board)


def is_valid_sudoku_v2(board):
    """ Actually, all this could be done in just one iteration.
        We could use box_index = (row / 3) * 3 + col / 3 where / is an integer division, row is a row number, and col
        is a column number.
        Move along the board. Check for each cell value if it was seen already in the current row / column / box
    Time complexity: O(1)
    Space complexity: O(1)
    """
    rows = [{} for _ in range(9)]
    cols = [{} for _ in range(9)]
    boxes = [{} for _ in range(9)]

    for i in range(9):
        for j in range(9):
            cell = board[i][j]
            if cell != '.':
                if cell in rows[i]:
                    return False
                rows[i][cell] = 1
                if cell in cols[j]:
                    return False
                cols[j][cell] = 1
                box_index = (i // 3) * 3 + j // 3
                if cell in boxes[box_index]:
                    return False
                boxes[box_index][cell] = 1
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

    def test_find_duplicate(self):
        for test_board, result in self.data:
            self.assertEqual(result, is_valid_sudoku_v1(test_board))
            self.assertEqual(result, is_valid_sudoku_v2(test_board))


if __name__ == '__main__':
    unittest.main()
