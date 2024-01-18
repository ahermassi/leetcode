""" Write a function to compute the next state (after one update) of the board given its current state. The next
state is created by applying the above rules simultaneously to every cell in the current state, where births and
deaths occur simultaneously. """

from collections import defaultdict


def game_of_life_v1(board):
    """ The problem might look very easy at first, however, the most important catch in this problem is to realize
         that if we update the original array with the given rules, we won't be able to perform simultaneous updates as
         is required in the question. We might end up using the updated values for some cells to update the values of
         other cells. But the problem requires applying the given rules simultaneously to every cell.

         Thus, we cannot update some cells first and then use their updated values to update other cells. An update to
         a cell can impact the other neighboring cells. If we use the updated value of a cell while updating its
         neighbors, then we are not applying rules to all cells simultaneously.

         Here, "simultaneously" isn't about parallelism but using the original values of the neighbors instead of the
         updated values while applying rules to any cell. Hence, the first approach could be as easy as having a copy
         of the board. The copy is never mutated, so we never lose the original value for a cell.

         Whenever a rule is applied to any of the cells, we look at its neighbors and change the original board
         accordingly. We keep the copy unmodified since the problem asks us to make the changes to the original
         board in-place.

                1- Make a copy of the original board which will remain unchanged throughout the process.

                2- Iterate over the cells of the board one by one.

                3- While computing the results of the rules, use the copy board and apply the result in the original
                     board.

    Time complexity: O(N * M), where N is the number of rows and M is the number of columns of the board
    Space complexity: O(N * M), this is the space occupied by the board copy
    """
    n, m = len(board), len(board[0])
    copy = [[board[row][col] for col in range(m)] for row in range(n)]
    for i in range(n):
        for j in range(m):
            live_neighbors = 0
            for x, y in (i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1):
                if 0 <= x < n and 0 <= y < m and copy[x][y]:
                    live_neighbors += 1
            if copy[i][j] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                board[i][j] = 0
            elif live_neighbors == 3:
                board[i][j] = 1


def game_of_life_v2(board):
    """ O(N * M) space complexity could be too expensive when the board is very large. We only have two states live (1)
        or dead (0) for a cell. We can use some dummy cell value to signify previous state of the cell along with the
        new changed value.
        For example, if the value of the cell was 1 originally but it has now become 0 after applying the rule, then we
        can change the value to 2. Also, if the value of the cell was 0 originally but it has now become 1 after
        applying the rule, then we can change the value to 3. Hence:
            0, 3 are 'dead' and 'dead->live'
            1, 2 are 'live' and 'live->dead'
        We iterate over the board again and change the value of a cell to a 0 if its value currently is 2 and change
        the value to a 1 if its current value is 3.
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m = len(board), len(board[0])
    for i in range(n):
        for j in range(m):
            live_neighbors = 0
            for x, y in (i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1):
                if 0 <= x < n and 0 <= y < m and board[x][y] in {1, 2}:  # 1 means now alive, 2 means was alive
                    live_neighbors += 1
            if board[i][j] and (live_neighbors < 2 or live_neighbors > 3):
                board[i][j] = 2
            elif board[i][j] == 0 and live_neighbors == 3:
                board[i][j] = 3
    for i in range(n):
        for j in range(m):
            if board[i][j] == 2:  # 2 means was previously alive
                board[i][j] = 0
            elif board[i][j] == 3:  # 3 means was previously dead
                board[i][j] = 1


# Follow up: In this question, we represent the board using a 2D array. In principle, the board is infinite, which would
# cause problems when the active area encroaches the border of the array. How would you address these problems?

def game_of_life_v3(board):
    """ If we have an extremely sparse matrix, it would make much more sense to actually save the location of only
        the live cells and then apply the 4 rules accordingly using only these live cells.
        We have the coordinates of all living cells in a set. Then we count the living neighbors of all cells by going
        through the living cells and increasing the counter of their neighbors (thus cells without living neighbor will
        not be in the counter). Afterwards, we just collect the new set of living cells by picking those with the right
        amount of neighbors.
    """
    n, m = len(board), len(board[0])
    live = {(i, j) for i in range(n) for j in range(m) if board[i][j]}
    all_live, new_live = defaultdict(int), set()
    for i, j in live:
        for neighbor in (i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1):
            if 0 <= neighbor[0] < n and 0 <= neighbor[1] < m:
                all_live[neighbor] += 1
    for cell in all_live:
        if (cell in live and all_live[cell] in {2, 3}) or (cell not in live and all_live[cell] == 3):  # If the cell
            # is initially alive and has 2 or 3 live neighbors, or the cell is initially dead and has 3 live neighbors
            new_live.add(cell)
    for i in range(n):
        for j in range(m):
            board[i][j] = int((i, j) in new_live)

# The only problem with this solution would be when the entire board cannot fit into memory. If that is indeed the case,
# then we would have to approach this problem in a different way.
# For that scenario, we assume that the contents of the matrix are stored in a file, one row at a time. In order for us
# to update a particular cell, we only have to look at its 8 neighbors which essentially lie in the row above and below
# it. So, for updating the cells of a row, we just need the row above and the row below. Thus, we read one row at a
# time from the file and at max we will have 3 rows in memory. We will keep discarding rows that are processed and then
# we will keep reading new rows from the file, one at a time.
