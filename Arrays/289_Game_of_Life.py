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


# Video explanation: https://www.youtube.com/watch?v=fei4bJQdBUQ
def game_of_life_v2(board):
    """  O(N * M) space complexity could be too expensive when the board is very large. Whenever we are asked to do
         something in-place, we are mostly given the luxury of modifying the input data structure itself. Even though a
         cell can only be in one of two states (dead or alive), we are given an integer matrix, where a bool matrix
         would obviously have been sufficient. But we can exploit that.

         We introduce two new states for a cell: 2: newly dead / originally alive, and 3: newly alive / originally dead.
         For example, if the cell value was 1 originally, but it has now become 0 after applying the rule, then we can
         change the value to 2. Also, if the cell value was 0 originally, but it has now become 1 after applying the
         rule, then we can change the value to 3. Hence:

                {0, 3} --> {'dead',  'dead->live'}
                {1, 2} --> {'live',  'live->dead'}

        For our intents and purposes (i.e. checking the neighbors of a cell), the newly died cell is still alive, since
        the changes made by us have not been enforced right now, hence the check (board[x][y] == 1) becomes
         (board[x][y] in {1, 2}).

                1- Iterate over the cells of the board

                2- The rules are computed and applied on the original board. The updated values signify both previous
                     and updated states.

                3- The updated rules can be seen as this:

                     * Rule 1: Any live cell with fewer than two live neighbors dies, as if caused by under-population.
                        Hence, change the value of cell to 2. This means the cell was live before but now is dead.

                     * Rule 2: Any live cell with two or three live neighbors lives on to the next generation. Hence, no
                        change in the value.

                     * Rule 3: Any live cell with more than three live neighbors dies, as if by over-population. Hence,
                        change the value of cell to 2. This means the cell was live before but now dead. Note that we
                        don't need to differentiate between rules 1 and 3. The start and end values are the same. Hence,
                        we use the same dummy state value.

                     * Rule 4: Any dead cell with exactly three live neighbors becomes a live cell, as if by
                        reproduction. Hence, change the value of cell to 3. This means the cell was dead before but now
                        live.

                4- Apply the new rules to the board.

                5- Iterate over the board again and change the value of a cell to a 0 if its current value is 2 and
                     change the value to a 1 if its current value is 3.

    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m = len(board), len(board[0])
    for i in range(n):
        for j in range(m):
            live_neighbors = 0
            for x, y in (i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1):
                # 1 means now alive, 2 means was alive
                if 0 <= x < n and 0 <= y < m and board[x][y] in {1, 2}:
                    live_neighbors += 1
            if board[i][j] and (live_neighbors < 2 or live_neighbors > 3):
                board[i][j] = 2 # The cell is now dead but was originally alive
            elif board[i][j] == 0 and live_neighbors == 3:
                board[i][j] = 3 # The cell is now live but was originally dead
    for i in range(n):
        for j in range(m):
            if board[i][j] == 2:  # 2 means was previously alive
                board[i][j] = 0
            elif board[i][j] == 3:  # 3 means was previously dead
                board[i][j] = 1


# Follow up: In this question, we represent the board using a 2D array. In principle, the board is infinite, which would
# cause problems when the active area encroaches the border of the array. How would you address these problems?

def game_of_life_v3(board):
    """ If the board becomes infinitely large, there are multiple problems the current solution would run into:

            1- It would be computationally impossible to iterate a matrix that large.
            2- It would not be possible to store that big a matrix entirely in memory. We have huge memory capacities
               these days i.e. of the order of hundreds of GBs. However, it still wouldn't be enough to store such a
               large matrix in memory.
            3- We would be wasting a lot of space if such a huge board only has a few alive cells and the rest of them
                 are all dead. In such a case, we have an extremely sparse matrix, and it wouldn't make sense to save
                 the board as a "matrix".

         If we have an extremely sparse matrix, it would make much more sense to actually save the location of only
         the alive cells and then apply the 4 rules accordingly using only these alive cells.

         We have the coordinates of all alive cells in a set. Then we count the alive neighbors of all cells by going
         through the alive cells and incrementing the counter of their neighbors (thus cells without alive neighbors
         will not be in the counter). Afterwards, we just collect the new set of alive cells by picking those with the
         right amount of neighbors.
    """
    n, m = len(board), len(board[0])
    alive = {(i, j) for i in range(n) for j in range(m) if board[i][j]}
    alive_neighbors_counter = defaultdict(int)
    for i, j in alive:
        for cell in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1):
            if 0 <= cell[0] < n and 0 <= cell[1] < m:
                alive_neighbors_counter[cell] += 1
    for i in range(n):
        for j in range(m):
            if (i, j) not in alive and alive_neighbors_counter[(i, j)] == 3:
                board[i][j] = 1
            elif (i, j) in alive and alive_neighbors_counter[(i, j)] not in {2, 3}:
                board[i][j] = 0

# The only problem with this solution would be when the entire board cannot fit into memory. If that is indeed the case,
# then we would have to approach this problem in a different way.
# For that scenario, we assume that the contents of the matrix are stored in a file, one row at a time. In order for us
# to update a particular cell, we only have to look at its 8 neighbors which essentially lie in the row above and below
# it. So, for updating the cells of a row, we just need the row above and the row below. Thus, we read one row at a
# time from the file and at max we will have 3 rows in memory. We will keep discarding rows that are processed and then
# we will keep reading new rows from the file, one at a time.
