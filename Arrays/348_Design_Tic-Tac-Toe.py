""" Design a Tic-tac-toe game that is played between two players on a n x n grid.
You may assume the following rules:
    A move is guaranteed to be valid and is placed on an empty block.
    Once a winning condition is reached, no more moves is allowed.
    A player who succeeds in placing n of their marks in a horizontal, vertical, or diagonal row wins the game. """

import unittest2 as unittest


class TicTacToe(object):
    """ Pretty simple logic. Since we know that each move will be legal, we don't need to keep track of the actual grid.
        If we assign the value of 1 for player 1 and -1 for player 2, we just keep track of the changes to individual
        rows and columns (and the two diagonals). If the value reaches either n or -n, we know that one of the players
        won. And since the player can only either draw or win during a move, player is returned if a win condition is
        reached.
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
        self.diag = 0
        self.anti_diagonal = 0

    def move(self, row, col, player):
        coef = 1 if player == 1 else -1
        self.rows[row] += coef
        self.cols[col] += coef
        if col == row:
            self.diag += coef
        if col + row == self.size - 1:
            self.anti_diagonal += coef
        if coef * self.size in {self.rows[row], self.cols[col], self.diag, self.anti_diagonal}:  # Account for n and -n
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

