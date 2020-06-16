""" This question is about implementing a basic elimination algorithm for Candy Crush.
Given a 2D integer array board representing the grid of candy, different positive integers board[i][j] represent
different types of candies. A value of board[i][j] = 0 represents that the cell at position (i, j) is empty. The given
board represents the state of the game following the player's move. Now, you need to restore the board to a stable
state by crushing candies according to the following rules:
- If three or more candies of the same type are adjacent vertically or horizontally, "crush" them all at the same
time - these positions become empty.
- After crushing all candies simultaneously, if an empty space on the board has candies on top of itself, then these
candies will drop until they hit a candy or bottom at the same time. (No new candies will drop outside the top
boundary.)
- After the above steps, there may exist more candies that can be crushed. If so, you need to repeat the above steps.
- If there does not exist more candies that can be crushed (ie. the board is stable), then return the current board.
You need to perform the above rules until the board becomes stable, then return the current board. """

import unittest2 as unittest


def candy_crush_v1(board):
    """ We need to simply perform the algorithm as described. It consists of two major steps: a crush step, and a
        gravity step. We work through each step individually.
        When crushing, we should flag candy that should be crushed first. We could use an auxiliary 'cells_to_crush'
        set. As for how to scan the board, let's call a line any row or column of the board. For each line, we could
        look at each width-3 slice of the line: if they are all the same, then we should flag those 3. After, we can
        crush the candy by setting all flagged board cells to zero.
        For each column, we want all the candy to go to the bottom. We could use a sliding window approach, maintaining
        a read and write head. As the read head iterates through the column in reverse order, when the read head sees
        a candy, the write head will write it down and move one place. Then, the write head will write zeroes to the
        remainder of the column.
    Time complexity: O((N * M)^2), worst case is at every loop we flag 3 candies. If we only crush 3 candies each time,
    the function will be called (N * M)/3 times. Multiply those two terms together we get O((N * M)^2).
    Space complexity: O(N * M)
    """

    def collect_cells(i, j):
        if i + 2 < n and board[i][j] == board[i + 1][j] == board[i + 2][j]:
            cells_to_crush.add((i, j))
            cells_to_crush.add((i + 1, j))
            cells_to_crush.add((i + 2, j))
        if j + 2 < m and board[i][j] == board[i][j + 1] == board[i][j + 2]:
            cells_to_crush.add((i, j))
            cells_to_crush.add((i, j + 1))
            cells_to_crush.add((i, j + 2))

    def drop_cells():
        for j in range(m):
            read_index = write_index = n - 1
            while read_index >= 0:
                if board[read_index][j]:
                    board[write_index][j] = board[read_index][j]
                    write_index -= 1
                read_index -= 1
            while write_index >= 0:
                board[write_index][j] = 0
                write_index -= 1

    n, m = len(board), len(board[0])
    cells_to_crush = set()
    for i in range(n):
        for j in range(m):
            if board[i][j]:
                collect_cells(i, j)
    if not cells_to_crush:
        return board
    for i, j in cells_to_crush:
        board[i][j] = 0
    drop_cells()
    return candy_crush_v1(board)


class Test(unittest.TestCase):
    data = [([[110, 5, 112, 113, 114], [210, 211, 5, 213, 214], [310, 311, 3, 313, 314], [410, 411, 412, 5, 414],
              [5, 1, 512, 3, 3], [610, 4, 1, 613, 614], [710, 1, 2, 713, 714], [810, 1, 2, 1, 1], [1, 1, 2, 2, 2],
              [4, 1, 4, 4, 1014]],
             [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [110, 0, 0, 0, 114], [210, 0, 0, 0, 214],
              [310, 0, 0, 113, 314], [410, 0, 0, 213, 414], [610, 211, 112, 313, 614], [710, 311, 412, 613, 714],
              [810, 411, 512, 713, 1014]])]

    def test_candy_crush(self):
        for test_board, result in self.data:
            self.assertEqual(result, candy_crush_v1(test_board))


if __name__ == '__main__':
    unittest.main()
