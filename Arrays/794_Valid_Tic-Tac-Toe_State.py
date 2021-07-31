""" A Tic-Tac-Toe board is given as a string array board. Return True if and only if it is possible to reach this board
position during the course of a valid tic-tac-toe game.
The board is a 3 x 3 array, and consists of characters " ", "X", and "O".  The " " character represents an empty square.
"""

import unittest2 as unittest


def valid_tic_tac_toe(board):
    """ Let's try to think about the necessary conditions for a tic-tac-toe board to be valid.
        - Since players take turns, the number of 'X's must be equal to or one greater than the number of 'O's
        - If the first player wins, the number of 'X's is one more than the number of 'O's
        - If the second player wins, the number of 'X's is equal to the number of 'O's
        - The board can't simultaneously have three 'X's and three 'O's in a row: Once one player has won (on their
          move), there are no subsequent moves
        - If X wins, the game is over and 'O' cannot play again, so the number of 'O' MUST be less than 'X'. Since
          player X plays the first move, if player X wins, the player X's count would be 1 more than player O.
        - If 'O' wins, the game is over and 'X' cannot play again, so the number of 'X' CANNOT be greater than 'O'.
        We'll count the number of 'X's and 'O's as 'x_count' and 'o_count'. 'rows' stores the number of X or O in each
        row. 'cols' stores the number of X or O in each column. 'diagonal' stores the number of X or O in diagonal.
        'anti_diagonal' stores the number of X or O in anti-diagonal. When any of the values gets to 3, it means X wins.
        When any of the values gets to -3, it means O wins.
        After, we just have to check our conditions as stated above.
        Since X starts first, x_count >= o_count. So if o_count > x_count, we can return False.
        Since the players take turns, we could also return False if x_count > o_count + 1.
        X and O cannot win at the same time.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    x_count = o_count = 0
    rows, cols = [0] * 3, [0] * 3
    diagonal = anti_diagonal = 0
    for i in range(3):
        for j in range(3):
            c = board[i][j]
            if c == ' ':
                continue
            if c == 'X':
                x_count += 1
            else:
                o_count += 1
            add = [-1, 1][c == 'X']
            rows[i] += add
            cols[j] += add
            if i == j:
                diagonal += add
            if i + j == 2:
                anti_diagonal += add
    if o_count > x_count or x_count > o_count + 1:
        return False
    win_values = {rows[0], rows[1], rows[2], cols[0], cols[1], cols[2], diagonal, anti_diagonal}
    x_won = 3 in win_values
    o_won = -3 in win_values
    if x_won and o_won:
        return False
    if x_won and x_count != o_count + 1:
        return False
    if o_won and x_count != o_count:
        return False
    return True


class Test(unittest.TestCase):
    data = [(['O  ', '   ', '   '], False), (['XOX', ' X ', '   '], False), (['XXX', '   ', 'OOO'], False), 
            (['XOX', 'O O', 'XOX'], True)] 

    def test_valid_tic_tac_toe(self):
        for test_board, result in self.data:
            self.assertEqual(result, valid_tic_tac_toe(test_board))


if __name__ == '__main__':
    unittest.main()
