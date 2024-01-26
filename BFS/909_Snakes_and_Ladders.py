""" Read description on Leetcode """

from collections import deque
import unittest2 as unittest


# Video explanation: https://youtu.be/6lH4nO3JfLk
def snakes_and_ladders(board):
    """ We can model the grid as a graph. Each square is a node. There are edges between squares within 6 of each other,
         and the snakes and ladders add new edges.

         The problem is asking us for the minimum number of moves, which suggests this is a shortest-path problem:

                Given an unweighted directed graph, the shortest path problem is the problem of finding a path from one
                vertex to another, such that the number of edges is the minimum possible.

        We can consider the input as an unweighted directed graph. The edges are moves corresponding to the results of
        a 6-sided die roll.

        Breadth-first search is an algorithm for finding the shortest path in unweighted graphs (directed or
        undirected). It maintains a queue of vertices (nodes). It starts with only the starting vertex (cell 1 in this
        problem). Then it processes the vertices one by one in the queue. Let's say we are processing some vertex.
        There are (possibly zero) outgoing edges from this vertex. If these edges lead to unvisited vertices, push these
        vertices to the queue. The algorithm terminates when it has visited all vertices.

            - Maintain a queue of cells and distances to all cells from the first one. By distance to the cell, we mean
               the least number of moves required to reach it. The distance from the first cell to itself is 0. Push the
               first cell to the queue.

            - While the queue is not empty:
                    * Pop a cell from the queue. Let's say its label is cur. For each square next_square with a label in
                       the range (cur+1) to min(curr+6,n^2), if next_square has a snake or a ladder, set next_square to
                       the destination of that snake or ladder.
                    * If next_square has not been visited yet, increment the number of moves and push it along
                       next_square on to the queue.

            - Return the distance to cell n^2 if it is reachable, otherwise return −1.

    Time complexity: O(N^2), we run BFS on a graph whose vertices are the board cells, and the edges are moves between
    them. There are N^2 vertices and no more than 6 * N^2=O(N^2) edges. The time complexity of BFS is O(∣V∣+∣E∣).
    We have ∣V∣= N^2 and ∣E∣ <6 * N^2, thus the total time complexity for BFS is O(7 * N^2)=O(N^2).
    Space complexity: O(N)
    """

    def get_coordinates(num):
        quot, rem = divmod(num - 1, n)
        row = n - quot - 1
        col = rem if quot % 2 == 0 else n - 1 - rem
        return row, col

    n, m = len(board), len(board[0])
    queue = deque([(1, 0)])
    visited = set()
    while queue:
        square, steps = queue.popleft()
        for next_square in range(square + 1, min(square + 6, n * n) + 1):
            x, y = get_coordinates(next_square)
            if board[x][y] != -1:
                next_square = board[x][y]
            if next_square == n * n:
                return steps + 1
            if next_square not in visited:
                queue.append((next_square, steps + 1))
                visited.add(next_square)
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
            self.assertEqual(result, snakes_and_ladders(test_board))


if __name__ == '__main__':
    unittest.main()
