""" Read description on Leetcode """

from collections import deque
import unittest2 as unittest


def snakes_and_ladders_v1(board):
    """ As we are looking for a shortest path, a breadth-first search is ideal. The main difficulty is to handle
        enumerating all possible moves from each square.
        Suppose we are on a square with number s. We would like to know all final destinations with number s2 after
        making one move. This requires knowing the coordinates get(s2) of square s2. This is a small puzzle in itself.
        We know that the row changes every N squares, and so is only based on quot = (s2-1) / N; also the column is
        only based on rem = (s2-1) % N and what row we are on (forwards or backwards)
        From there, we perform a breadth first search, where the nodes are the square numbers s.
    Time complexity: O(N ** 2)
    Space complexity: O(N)
    """

    def get_coordinates(num):
        quot, rem = divmod(num - 1, n)
        row = n - quot - 1
        col = rem if quot % 2 == 0 else n - 1 - rem
        return row, col

    n = len(board)
    distance, queue = {1: 0}, deque([1])  # distance[a] = b means we arrived at cell #a with b moves
    while queue:
        num = queue.popleft()
        if num == n * n:
            return distance[n * n]
        for i in range(num + 1, num + 7):  # Try all the 6 possible moves
            if i > n * n:  # We landed outside the board
                break
            row, col = get_coordinates(i)
            if board[row][col] != -1:  # There is a snake or ladder in this square
                i = board[row][col]  # So this move takes us straight to cell #board[row][col]
            if i not in distance:
                distance[i] = distance[num] + 1  # This means we've arrived to cell #i with 1 move from cell #num
                queue.append(i)  # Continue exploring from there
    return -1


class Test(unittest.TestCase):
    data = [([
                 [-1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1],
                 [-1, 35, -1, -1, 13, -1],
                 [-1, -1, -1, -1, -1, -1],
                 [-1, 15, -1, -1, -1, -1]], 4)]

    def test_snakes_and_ladders(self):
        for test_board, result in self.data:
            self.assertEqual(result, snakes_and_ladders_v1(test_board))


if __name__ == '__main__':
    unittest.main()
