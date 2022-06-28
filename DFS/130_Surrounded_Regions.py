""" Given a 2D board containing 'X' and 'O' (the letter O), capture all regions surrounded by 'X'.
A region is captured by flipping all 'O's into 'X's in that surrounded region. """
from collections import deque

import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=9z2BunfoZ5Y


def solve_v1(board):
    """ If we are asked to summarize the algorithm in one sentence, it would be that we enumerate all those candidate
         cells (i.e. the ones filled with O), and check one by one if they are captured or not, i.e. we start with a
         candidate cell (O), and then apply either DFS or BFS strategy to explore its surrounding cells.

        It is easier to focus on the inverse problem, namely identifying 'O's that can reach the border. The reason
        that the inverse is simpler is that if an 'O' is adjacent to an 'O that can reach the border, then the first
        'O' can reach it too.

        Surrounded regions shouldn't be on the border, which means that any 'O' on the border of the board is not
        flipped to 'X'.

        Any 'O' that is not on the border but is connected to an 'O' on the border will not be flipped to 'X'.
        Any 'O' that is not on the border and is not connected to an 'O' on the border will be flipped to 'X'.

        The algorithm consists of three steps:

            1- We select all the cells that are located on the borders of the board.

            2- Start from each of the above selected cell, we then perform the DFS traversal.
                 If a cell on the border happens to be O, then we know that this cell is alive, together with the other
                 O cells that are connected to this border cell. Two cells are connected, if there exists a path
                 consisting of only O letter that bridges between the two cells.
                Based on the above conclusion, the goal of our DFS traversal would be to mark out all those connected O
                cells that is originated from the border, with any distinguished letter such as T

            3- Once we iterate through all border cells, we would then obtain three types of cells:
                    - The one with the X letter: The cell that we could consider as the wall.
                    - The one with the O letter: The cells that are spared in our DFS traversal, i.e. these cells have
                       no connection to the border, therefore they are captured. We then should replace
                       these cells with X letter.
                    - The one with the T letter: These are the cells that are marked during our DFS traversal, i.e.
                       these are the cells that have at least one connection to the borders, therefore they are not
                       captured. As a result, we would revert the cell to its original letter O.

        Rather than using a 'visited' set to keep track of the visited cells, we simply mark visited cells in place.

    Time complexity: O(N * M), in the worst case where it contains only the O cells on the board, we would traverse each
    cell twice: once during the DFS traversal and the other time during the cell reversion in the last step.
    Space complexity: O(N * M), during the recursive calls of DFS() function we would consume some space in the function
    call stack, i.e. the call stack will pile up along with the depth of recursive calls. The maximum depth of recursive
    calls would be N*M as in the worst scenario mentioned in the time complexity.
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < m or board[i][j] != 'O':
            return
        board[i][j] = 'T'
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            dfs(x, y)

    n, m = len(board), len(board[0])
    for i in range(n):
        dfs(i, 0)  # Left border
        dfs(i, m - 1)  # Right border
    for j in range(m):
        dfs(0, j)  # Top border
        dfs(n - 1, j)  # Bottom border
    for i in range(n):
        for j in range(m):
            if board[i][j] == 'O':
                board[i][j] = 'X'
            elif board[i][j] == 'T':
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
