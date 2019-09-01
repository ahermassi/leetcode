""" Write a function to compute the next state (after one update) of the board given its current state. The next
state is created by applying the above rules simultaneously to every cell in the current state, where births and
deaths occur simultaneously. """

from collections import defaultdict


def game_of_life_v1(board):
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


def game_of_life_v2(board):
    """ O(N * M) space complexity could be too expensive when the board is very large. We only have two states live(1)
        or dead(0) for a cell. We can use some dummy cell value to signify previous state of the cell along with the
        new changed value.
        For e.g. If the value of the cell was 1 originally but it has now become 0 after applying the rule, then we can
        change the value to 2. Also, if the value of the cell was 0 originally but it has now become 1 after applying
        the rule, then we can change the value to 3. Hence:
        0, 3 are "dead", and "dead->live"
        1, 2 are "live", and "live->dead"
        We iterate the board again and change the value of a cell to a 0 if its value currently is 2 and change the
        value to a 1 if its current value is 3.
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m = len(board), len(board[0])

    def get_neighbors(i, j):
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1),
                     (i - 1, j - 1), (i + 1, j + 1), (i - 1, j + 1), (i + 1, j - 1)]
        return [neighbor for neighbor in neighbors
                if 0 <= neighbor[0] < n and 0 <= neighbor[1] < m]

    for i in range(n):
        for j in range(m):
            live_neighbors = 0
            for neighbor in get_neighbors(i, j):
                if board[neighbor[0]][neighbor[1]] in (1, 2):  # 1 means now alive, 2 means was previously alive
                    live_neighbors += 1
            if board[i][j] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                board[i][j] = 2
            elif board[i][j] == 0 and live_neighbors == 3:
                board[i][j] = 3
    for i in range(n):
        for j in range(m):
            if board[i][j] == 2:  # 2 means was previously alive
                board[i][j] = 0
            elif board[i][j] == 3:  # 3 means was previously dead
                board[i][j] = 1

