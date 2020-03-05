""" Given a 2D board containing 'X' and 'O' (the letter O), capture all regions surrounded by 'X'.
A region is captured by flipping all 'O's into 'X's in that surrounded region. """
from collections import deque

import unittest2 as unittest


def solve_v1(board):
    """ It is easier to focus on the inverse problem, namely identifying 'O's that can reach the boundary. The reason
        that the inverse is simpler is that if an 'O' is adjacent to an 'O that can reach the boundary, then the first
        'O' can reach it too.
        Surrounded regions shouldn't be on the border, which means that any 'O' on the border of the board is not
        flipped to 'X'.
        Any 'O' that is not on the border but is connected to an 'O' on the border will not be flipped to 'X'.
        Any 'O' that is not on the border and is not connected to an 'O' on the border will be flipped to 'X'.
        The idea is to first find all 'O's on the edge, and do DFS from these 'O's. Mark all 'O's encountered as '1'
        since these 'O's are found by doing DFS from the 'O's on the edge, which means they are connected to the edge
        'O's and hence they are the 'O's that will remain as 'O' in the result (not surrounded).
        At the end of DFS, there are some 'O's that could not be reached. These are the 'O's that need to be turned to
        'X' (surrounded).
            1- Check the four borders of the matrix. If a cell is 'O', alter it and all its neighbor 'O's to '1'. Then
               after DFS:
            2- Alter all the 'O's to 'X'
            3- Alter all the '1's to 'O'
        Rather than using a 'visited' set to keep track of the visited cells, we simply mark visited cells in place.
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
        dfs(i, 0)  # Left border
        dfs(i, m - 1)  # Right border
    for i in range(m):
        dfs(0, i)  # Top border
        dfs(n - 1, i)  # Bottom border
    for i in range(n):
        for j in range(m):
            if board[i][j] == 'O':
                board[i][j] = 'X'
            elif board[i][j] == '1':
                board[i][j] = 'O'


def solve_v2(board):
    """ BFS version of previous solution.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    if not board:
        return None
    n, m = len(board), len(board[0])
    queue = deque()
    for i in range(n):
        queue.extend([(i, 0), (i, m-1)])
    for j in range(m):
        queue.extend([(0, j), (n-1, j)])
    # More pythonically
    # queue = deque([(i, j) for i in range(n) for (i, j) in {(i, 0), (i, m-1)}] + [(i, j) for j in range(m) for (i, j)
    #                                                                              in {(0, j), (n-1, j)}])
    while queue:
        i, j = queue.popleft()
        if 0 <= i < n and 0 <= j < m and board[i][j] == 'O':
            board[i][j] = '1'
            queue.extend([(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)])
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
