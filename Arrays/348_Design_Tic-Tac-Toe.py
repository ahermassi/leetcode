""" Design a Tic-tac-toe game that is played between two players on a n x n grid.
You may assume the following rules:
    A move is guaranteed to be valid and is placed on an empty block.
    Once a winning condition is reached, no more moves is allowed.
    A player who succeeds in placing n of their marks in a horizontal, vertical, or diagonal row wins the game. """

import unittest2 as unittest


class TicTacToe(object):
    """ Pretty simple logic. Since we know that each move will be legal, we don't need to keep track of the actual grid.
        If we assign the value of 1 for player 1 and -1 for player 2, we just keep track of the changes to individual
        rows and columns (and the two diagonals). On every move, we must determine whether a player has marked all of
        the cells in a row or column. In other words, we could say that, if there are n rows and n columns on a board,
        the player must have marked a certain row or column n times. Also, there are always n cells on the diagonal or
        anti-diagonal. Thus, to win by either of these, a player must have marked the cells on the diagonal or
        anti-diagonal n times.
        With this, we can say that, if the value of rows[i] is equal to n, player 1 has marked ith row n times.
        Similarly, if the value of rows[i] is equal to -n, then player 2 has marked the ith row n times. Similar logic
        applies to the columns and diagonals. We must finally determine whether the current player has won the game.
        If any row, column, diagonal, or anti-diagonal is equal to n (for player 1) or -n (for player 2) then the
        current player has won the game. And since the player can only either draw or win during a move, player is
        returned if a win condition is reached.
        The important abstraction in this approach is rows/cols arrays. rows[i] represents ith row in the actual game
        grid. Since we're only interested in the entire content of a row (sum of values in this case), this abstraction
        makes a lot of sense.
    Time complexity: O(1)
    Space complexity: O(n)
    """

    def __init__(self, n):
        self.rows = [0] * n
        self.cols = [0] * n
        self.size = n
        self.diagonal = 0
        self.anti_diagonal = 0

    def move(self, row, col, player):
        add = 1 if player == 1 else -1
        self.rows[row] += add
        self.cols[col] += add
        if col == row:
            self.diagonal += add
        if col + row == self.size - 1:
            self.anti_diagonal += add
        if add * self.size in {self.rows[row], self.cols[col], self.diagonal, self.anti_diagonal}:
            # Account for n and -n
            return player
        return 0


class Test(unittest.TestCase):
    toe = TicTacToe(3)
    move1 = toe.move(0, 0, 1)
    move2 = toe.move(0, 2, 2)
    move3 = toe.move(2, 2, 1)
    move4 = toe.move(1, 1, 2)
    move5 = toe.move(2, 0, 1)
    move6 = toe.move(1, 0, 2)
    move7 = toe.move(2, 1, 1)

    def test_tic_tac_toe(self):
        self.assertEqual(0, self.move1)
        self.assertEqual(0, self.move2)
        self.assertEqual(0, self.move3)
        self.assertEqual(0, self.move4)
        self.assertEqual(0, self.move5)
        self.assertEqual(0, self.move6)
        self.assertEqual(1, self.move7)


if __name__ == '__main__':
    unittest.main()

