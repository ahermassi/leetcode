""" Write a function to compute the next state (after one update) of the board given its current state. The next
state is created by applying the above rules simultaneously to every cell in the current state, where births and
deaths occur simultaneously. """

from collections import defaultdict


def game_of_life(board):
    """ The first approach could be as easy as having a copy of the board using a hash map. The copy is never mutated.
        So, we never lose the original value for a cell. Whenever a rule is applied to any of the cells, we look at its
        neighbors in the hash map and change the original board accordingly. Here we keep the copy unmodified since the
        problem asks us to make the changes to the original array in-place.
    Time complexity: O(N * M) where N is the number of rows and M is the number of columns of the board
    Space complexity: O(N * M), this is the space occupied by the copy board we created initially
    """
    live_neighbors, n, m = defaultdict(int), len(board), len(board[0])

    def get_neighbors(i, j):
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1),
                     (i - 1, j - 1), (i + 1, j + 1), (i - 1, j + 1), (i + 1, j - 1)]
        return [neighbor for neighbor in neighbors if 0 <= neighbor[0] < n and 0 <= neighbor[1] < m]

    for i in range(n):
        for j in range(m):
            for neighbor in get_neighbors(i, j):
                if board[neighbor[0]][neighbor[1]] == 1:
                    live_neighbors[(i, j)] += 1
    for i in range(n):
        for j in range(m):
            if board[i][j] == 1 and (live_neighbors[(i, j)] < 2 or live_neighbors[(i, j)] > 3):
                board[i][j] = 0
            if board[i][j] == 0 and live_neighbors[(i, j)] == 3:
                board[i][j] = 1

