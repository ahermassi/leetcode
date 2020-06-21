""" Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be validated according to the following
rules:
    Each row must contain the digits 1-9 without repetition.
    Each column must contain the digits 1-9 without repetition.
    Each of the 9 3x3 sub-boxes of the grid must contain the digits 1-9 without repetition. """

import unittest2 as unittest


def is_valid_sudoku_v1(board):
    """ Iterate three times over the board to ensure that:
            1- There is no rows with duplicates
            2- There is no columns with duplicates
            3- There is no sub-boxes with duplicates
    Time complexity: O(1), as the number of iterations is known in advance (9 X 9 board)
    Space complexity: O(1)
    """

    def is_valid(lst):
        for l in lst:
            if not is_valid_unit(l):
                return False
        return True

    def is_valid_unit(unit):
        values = set()
        for cell in unit:
            if cell != '.' and cell in values:
                return False
            values.add(cell)
        return True

    def is_valid_squares():
        # Row 0: i = 0; j takes values 0,3,6 to create: box0(x=0..2, y=0..2), box1(x=0..2, y=3..5), box2(x=0..2, y=6..8)
        # -> x = 0..2 = i..i+3, y = j..j+3
        # Row 1: i = 3; j takes values 0,3,6 to create: box0(x=3..5, y=0..2), box1(x=3..5, y=3..5), box2(x=3..5, y=6..8)
        # -> x = 3..5 = i..i+3, y = j..j+3
        # Row 2: i = 6; j takes values 0,3,6 to create: box0(x=6..8, y=0..2), box1(x=6..8, y=3..5), box2(x=6..8, y=6..8)
        # -> x = 6..8 = i..i+3, y = j..j+3
        for i in (0, 3, 6):
            for j in (0, 3, 6):
                square = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if not is_valid_unit(square):
                    return False
        return True

    rows = [row for row in board]
    cols = [col for col in zip(*board)]
    return is_valid(rows) and is_valid(cols) and is_valid_squares()


def is_valid_sudoku_v2(board):
    """ Actually, all this could be done in just one iteration.
        We could use box_index = (row / 3) * 3 + col / 3 where / is an integer division, 'row' is a row number, and
        'col' is a column number.
        Move along the board. Check for each cell value if it was seen in the current row / column / box.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for i in range(9):
        for j in range(9):
            cell = board[i][j]
            if cell == '.':
                continue
            if cell in rows[i] or cell in cols[j]:
                return False
            rows[i].add(cell)
            cols[j].add(cell)
            box_index = (i // 3) * 3 + j // 3
            if cell in boxes[box_index]:
                return False
            boxes[box_index].add(cell)
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
