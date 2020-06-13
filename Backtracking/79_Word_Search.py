""" Given a 2D board and a word, find if the word exists in the grid.
The word can be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally
or vertically neighboring. The same letter cell may not be used more than once. """

import unittest2 as unittest


def exist_v1(board, word):
    """ DFS that alters the original board. We mark a visited cell as '#' to avoid using the same cell more than once.
        When we exhaust all search possibilities, we backtrack and remove the mark of the visited cell.
    Time complexity: O(N * M * (4^S)), where N and M are the dimensions of the board and S is the length of the word.
    First, we have to find the first letter to start which gives time O(N * M). Then, for each search step it has 2~4
    neighbours to go, and it has S steps, where S is the length of the word to be searched.
    https://cs.stackexchange.com/questions/96626/whats-the-big-o-runtime-of-a-dfs-word-search-through-a-matrix
    Space complexity: O(S), for the recursion call stack
    """

    def search(i, j, index):
        if index == length:  # Nothing left to complete
            return True
        if not 0 <= i < n or not 0 <= j < m or board[i][j] != word[index]:
            return False
        temp = board[i][j]
        board[i][j] = '#'  # Mark the cell as visited
        found = search(i-1, j, index+1) or search(i+1, j, index+1) or search(i, j-1, index+1) or search(i, j+1, index+1)
        board[i][j] = temp  # Backtrack and remove the mark
        return found

    n, m, length = len(board), len(board[0]), len(word)
    for i in range(n):
        for j in range(m):
            if search(i, j, 0):
                return True
    return False


def exist_v2(board, word):
    """ DFS without altering the input board. Use a 'visited' set to store the visited cells. When we exhaust all
        search possibilities, we backtrack and remove the cell from 'visited' set.
        This (and the technique used in the following solution) resemble what we usually do in the backtracking
        problems where we have to try/enumerate all the possible paths. At every recursive call, we'd either:
            - Call f(path + new_val), or
            - path.append(new_val); f(path); path.pop()
    Time complexity: O(N * M * (4^S))
    Space complexity: O(S)
    """

    def search(i, j, index):
        if index == length:
            return True
        if not 0 <= i < n or not 0 <= j < m or board[i][j] != word[index] or (i, j) in visited:
            return False
        visited.add((i, j))  # Mark the cell as visited. At each step, we mark our choice before jumping into the next
        # step. At the end of each step, we would also revert our marking, so that we could have a clean slate to try
        # another direction.
        found = search(i-1, j, index+1) or search(i+1, j, index+1) or search(i, j-1, index+1) or search(i, j+1, index+1)
        visited.remove((i, j))  # Backtrack and remove the mark
        return found

    n, m, length = len(board), len(board[0]), len(word)
    visited = set()
    for i in range(n):
        for j in range(m):
            if search(i, j, 0):
                return True
    return False


def exist_v3(board, word):
    """ Good ol' backtracking where we pass an augmented path to each recursive call.
    Time complexity: O(N * M * (4^S))
    Space complexity: O(S)
    """

    def search(i, j, index, visited):
        if index == len(word):
            return True
        if not 0 <= i < n or not 0 <= j < m or (i, j) in visited or board[i][j] != word[index]:
            return False
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if search(x, y, index + 1, visited | {(i, j)}):  # visited | {(i, j)} is equivalent to (path + new_val)
                return True
        return False

    n, m = len(board), len(board[0])
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
