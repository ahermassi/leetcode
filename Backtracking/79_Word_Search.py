""" Given a 2D board and a word, find if the word exists in the grid.
The word can be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally
or vertically neighboring. The same letter cell may not be used more than once. """

import unittest2 as unittest


def exist_v1(board, word):
    """ The accurate term to summarize the solution is backtracking, which is a methodology where we mark the current
         path of exploration, and if the path does not lead to a solution we revert the change (i.e. backtrack) and try
         another path.

         As the general idea for the solution, we would walk around the 2D grid, and at each step we mark our choice
         before jumping into the next step. At the end of each step, we would also revert the marking, so that we could
         have a clean slate to try another direction. In addition, the exploration is done via the DFS strategy, where
         we go as further/deep as possible before we try the next direction.

         The skeleton of the algorithm is a loop that iterates over each cell in the grid. For each cell, we invoke the
         backtracking function to check if we could obtain a solution starting from this very cell.

         For the backtracking function search(row, col, index), as a DFS algorithm, it is often implemented as a
         recursive function. The function can be broken down into the following 4 steps:

            1- At the beginning, we first check if we reached the bottom case of the recursion, where the word to be
                 matched is empty, i.e. we have already found the match for each prefix of the word.

            2- We then check if the current state is invalid, either the position of the cell is out of the boundaries
                 of the board or the letter in the current cell does not match the current letter of the word.

            3- If the current step is valid, we then start the exploration. First, we mark the current cell as visited,
                 e.g. any non-alphabetic letter will do. Then we iterate through the 4 possible directions, namely up,
                 right, down and left.

            4- At the end of the exploration, we revert the cell back to its original state. Finally, we return the
                 result of the exploration.

    Time complexity: O(N * M * (3^L)), where N and M are the dimensions of the board and L is the length of the word.
    We iterate through the board for backtracking, i.e. there could be N*M invocations of the backtracking function in
    the worst case. For the backtracking function, initially we could have at most 4 directions to explore, but further
    the choices are reduced to 3 (since we won't go back to where we came from). As a result, the execution trace after
    the first step could be visualized as a 3-ary tree, where each of the branches represents a potential exploration in
    the corresponding direction. Therefore, in the worst case, the total number of invocations would be the number of
    nodes in a full 3-ary tree, which is about 3^L.
    https://cs.stackexchange.com/questions/96626/whats-the-big-o-runtime-of-a-dfs-word-search-through-a-matrix
    Space complexity: O(L), the main consumption of the memory lies in the recursion call stack of the backtracking
    function. The maximum length of the call stack would be the length of the word.
    """

    def search(i, j, index):
        if index == length:
            # No characters left to search
            return True
        if not 0 <= i < n or not 0 <= j < m or board[i][j] != word[index]:
            return False
        temp = board[i][j]
        board[i][j] = '#'  # Mark the choice before exploring further
        for x, y in directions:
            if search(i + x, j + y, index + 1):
                return True
                # Sudden-death return, no cleanup. This would, however, leave with a "side-effect," i.e. the matched
                # letters in the original board would be altered to #
                # Instead of returning True directly once we find a match, we could've broken out of the loop to do the
                # cleanup before returning:
                # found = True
                # break
        # None of the 4 potential paths got matched up to the end, meaning the current cell is not a good candidate,
        # so return it back to the non-visited pool by changing it back to its original value.
        board[i][j] = temp  # Backtrack: Revert the change, a clean slate and no side effect
        return False

    n, m, length = len(board), len(board[0]), len(word)
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    for i in range(n):
        for j in range(m):
            if search(i, j, 0):
                return True
    return False


# Video explanation: https://youtu.be/pfiQ_PS1g8E
def exist_v2(board, word):
    """ Backtracking without altering the input board.

         We use a 'visited' set to store the visited cells. When we exhaust all search possibilities, we backtrack and
         remove the cell from 'visited' set.

        This (and the technique used in the following solution) resemble what we usually do in the backtracking
        problems where we have to try/enumerate all the possible paths. At every recursive call, we'd either:
            - Call f(path + new_val), or
            - path.append(new_val); f(path); path.pop()

    Time complexity: O(N * M * (3^L))
    Space complexity: O(L)
    """

    def search(i, j, index):
        if index == length:
            return True
        if not 0 <= i < n or not 0 <= j < m or board[i][j] != word[index] or (i, j) in visited:
            return False
        visited.add((i, j))
        # Mark the cell as visited. At each step, we mark our choice before jumping into the next step.
        # At the end of each step, we would also revert our marking, so that we could have a clean slate to try
        # another direction.
        for x, y in directions:
            if search(i + x, j + y, index + 1):
                return True
        visited.remove((i, j))  # Backtrack and remove the mark
        return False

    n, m, length = len(board), len(board[0]), len(word)
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    visited = set()
    for i in range(n):
        for j in range(m):
            if search(i, j, 0):
                return True
    return False


def exist_v3(board, word):
    """ Good ol' backtracking where we pass an augmented path to each recursive call.

    Time complexity: O(N * M * (3^L))
    Space complexity: O(L)
    """

    def search(i, j, index, visited):
        if index == len(word):
            return True
        if not 0 <= i < n or not 0 <= j < m or (i, j) in visited or board[i][j] != word[index]:
            return False
        for x, y in directions:
            # visited | {(i, j)} is equivalent to (path + new_val)
            if search(i + x, j + y, index + 1, visited | {(i, j)}):
                return True
        return False

    n, m = len(board), len(board[0])
    directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    visited = set()
    for i in range(n):
        for j in range(m):
            if search(0, i, j, visited):
                return True
    return False


class Test(unittest.TestCase):
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    data = [('ABCCED', True), ('SEE', True), ('ABCB', False)]

    def test_exist(self):
        for test_word, result in self.data:
            self.assertEqual(result, exist_v1(self.board, test_word))
            self.assertEqual(result, exist_v2(self.board, test_word))
            self.assertEqual(result, exist_v3(self.board, test_word))


if __name__ == '__main__':
    unittest.main()
