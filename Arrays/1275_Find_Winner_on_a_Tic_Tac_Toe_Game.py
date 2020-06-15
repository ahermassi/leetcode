""" Given an array moves where each element is another array of size 2 corresponding to the row and column of the grid
where they mark their respective character in the order in which A and B play.
Return the winner of the game if it exists (A or B), in case the game ends in a draw return "Draw", if there are still
movements to play return "Pending".
You can assume that moves is valid (It follows the rules of Tic-Tac-Toe), the grid is initially empty and A will play
first. """

import unittest2 as unittest


def tic_tac_toe(moves):
    """ Just treat 'X' as 1 and 'O' as -1, and we see that we can just sum each column, row, or diagonal to see if a
        player won it (i.e. the sum is 3 or -3). This means we only have to check each row, column, or diagonal once.
        For a further speedup, we don't need to keep track of the grid at all. Just update the row, column, and diagonal
        sums while parsing the moves. This is similar to 348- Design Tic-Tac-Toe.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    rows, cols = [0] * 3, [0] * 3
    diagonal = anti_diagonal = 0
    player = 1
    for i, j in moves:
        rows[i] += player
        cols[j] += player
        if i == j:
            diagonal += player
        if i + j == 2:
            anti_diagonal += player
        if 3 * player in {rows[i], cols[j], diagonal, anti_diagonal}:
            return 'AB'[player == -1]
        player *= -1
    return 'Draw' if len(moves) == 9 else 'Pending'


class Test(unittest.TestCase):
    data = [([[0, 0], [2, 0], [1, 1], [2, 1], [2, 2]], 'A'), ([[0, 0], [1, 1], [0, 1], [0, 2], [1, 0], [2, 0]], 'B'),
            ([[0, 0], [1, 1], [2, 0], [1, 0], [1, 2], [2, 1], [0, 1], [0, 2], [2, 2]], 'Draw'),
            ([[0, 0], [1, 1]], 'Pending')]

    def test_tic_tac_toe(self):
        for test_moves, result in self.data:
            self.assertEqual(result, tic_tac_toe(test_moves))


if __name__ == '__main__':
    unittest.main()
