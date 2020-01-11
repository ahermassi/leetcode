""" Given a 2D board containing 'X' and 'O' (the letter O), capture all regions surrounded by 'X'.
A region is captured by flipping all 'O's into 'X's in that surrounded region. """

import unittest2 as unittest


def solve_v1(board):
    """ Surrounded regions shouldn't be on the border, which means that any 'O' on the border of the board is not
        flipped to 'X'.
        Any 'O' that is not on the border but is connected to an 'O' on the border will not be flipped to 'X'.
        Any 'O' that is not on the border and is not connected to an 'O' on the border will be flipped to 'X'.
        The idea is to first find all 'O's on the edge, and do DFS from these 'O's. Mark all 'O's encountered as '1'
        since these 'O's are found by doing DFS from the 'O's on the edge, which means they are connected to the edge
        'O's and hence they are the 'O's that will remain as 'O' in the result (not surrounded).
        At the end of DFS, there are some 'O's that could not be reached. These are the 'O's that need to be turned to
        'X' (surrounded).
            1- Check the four border of the matrix. If a cell is 'O', alter it and all its neighbor 'O's to '1'. Then
               after DFS:
            2- Alter all the 'O's to 'X'
            3- Alter all the '1's to 'O'
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < m or board[i][j] != 'O':
            return
        board[i][j] = '1'
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            dfs(x, y)

    if not board:
        return None
    n, m = len(board), len(board[0])
    for i in range(n):
        if board[i][0] == 'O':  # Left border
            dfs(i, 0)
        if board[i][m - 1] == 'O':  # Right border
            dfs(i, m - 1)
    for i in range(m):
        if board[0][i] == 'O':  # Top border
            dfs(0, i)
        if board[n - 1][i] == 'O':  # Bottom border
            dfs(n - 1, i)
    for i in range(n):
        for j in range(m):
            if board[i][j] == 'O':
                board[i][j] = 'X'
            elif board[i][j] == '1':
                board[i][j] = 'O'


class Test(unittest.TestCase):
    data = [([['X', 'X', 'X', 'X'], ['X', 'O', 'O', 'X'], ['X', 'X', 'O', 'X'], ['X', 'O', 'X', 'X']],
             [['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'O', 'X', 'X']])]

    def test_solve(self):
        for test_board, result in self.data:
            solve_v1(test_board)
            self.assertEqual(result, test_board)


if __name__ == '__main__':
    unittest.main()
