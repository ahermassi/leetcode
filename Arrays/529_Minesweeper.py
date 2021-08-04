""" You are given an m x n char matrix board representing the game board where:

'M' represents an unrevealed mine,
'E' represents an unrevealed empty square,
'B' represents a revealed blank square that has no adjacent mines (i.e., above, below, left, right, and all 4 diagonals),
digit ('1' to '8') represents how many mines are adjacent to this revealed square, and
'X' represents a revealed mine.
You are also given an integer array click where click = [clickr, clickc] represents the next click position among all the unrevealed squares ('M' or 'E').

Return the board after revealing this position according to the following rules:

If a mine 'M' is revealed, then the game is over. You should change it to 'X'.
If an empty square 'E' with no adjacent mines is revealed, then change it to a revealed blank 'B' and all of its
adjacent unrevealed squares should be revealed recursively.
If an empty square 'E' with at least one adjacent mine is revealed, then change it to a digit ('1' to '8') representing
the number of adjacent mines.
Return the board when no more squares will be revealed. """


def update_board_v1(board, click):
    """ This is a typical search problem the can be solved using DFS. Search rules:
            - If we click on a mine ('M'), mark it as 'X', stop further search.
            - If we click on an empty cell ('E'), depending on how many surrounding mine it has:
                - If it has surrounding mine(s), mark it with the number of surrounding mine(s), stop further search.
                - If it has no surrounding mine, mark it as 'B', then continue searching its 8 neighbors.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def reveal(x, y):
        if not 0 <= x < n or not 0 <= y < m or board[x][y] != 'E':
            return
        mines_nearby = 0
        for a, b in directions:
            if 0 <= x + a < n and 0 <= y + b < m and board[x + a][y + b] == 'M':
                mines_nearby += 1
        if not mines_nearby:
            board[x][y] = 'B'
            for a, b in directions:
                reveal(x + a, y + b)
        else:
            board[x][y] = str(mines_nearby)

    n, m = len(board), len(board[0])
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)}
    x, y = click
    if board[x][y] == 'M':  # If a mine ('M') is revealed, then the game is over - change it to 'X' and return.
        board[x][y] = 'X'
    else:
        reveal(x, y)  # Run dfs to reveal the board
    return board
