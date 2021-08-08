""" Given an m x n matrix board where each cell is a battleship 'X' or empty '.', return the number of the battleships
on board.

Battleships can only be placed horizontally or vertically on board. In other words, they can only be made of the shape
1 x k (1 row, k columns) or k x 1 (k rows, 1 column), where k can be of any size. At least one horizontal or vertical
cell separates between two battleships (i.e., there are no adjacent battleships). """


def count_battleships_v1(board):
    """ Good ol' DFS. When we find a battleship cell, move only right or down, as a battleship's head can only begin at
        the leftmost cell of a row or the topmost cell of a column. It's similar to counting the number of "vertical"
        and "horizontal" islands.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < m or board[i][j] == '.' or (i, j) in visited:
            return
        visited.add((i, j))
        dfs(i, j + 1)
        dfs(i + 1, j)

    n, m = len(board), len(board[0])
    visited, res = set(), 0
    for i in range(n):
        for j in range(m):
            if board[i][j] == 'X' and (i, j) not in visited:
                dfs(i, j)
                res += 1
    return res
