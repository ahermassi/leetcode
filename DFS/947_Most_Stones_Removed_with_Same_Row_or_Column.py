""" On a 2D plane, we place stones at some integer coordinate points.  Each coordinate point may have at most one stone.
Now, a move consists of removing a stone that shares a column or row with another stone on the grid.
What is the largest possible number of moves we can make? """

from collections import defaultdict
import unittest2 as unittest


def remove_stones(stones):
    """ Connected stones, or island, can be reduced to 1 "representative" stone that can't be matched to any other
        neighbor. Hence, every island / connected component's "representative" is one of the stones that can't be
        removed, so the maximum number of stones that can be removed is:
            number of total stones - number of islands
        The whole problem is transformed to: What is the number of islands? You can show all your skills on a DFS
        implementation, and solve this problem as a normal one.
        The key point here is, we define an island as number of points that are connected by row or column. Every point
        does not have to be next to each other as in previous island problems.
    Time complexity: O(N^2), where N is the number of stones
    Space complexity: O(N)
    """

    def dfs(i, j):
        # With each (i, j) pair in hand, we discard it from points set and proceed to examine all the points that share
        # the same row or column with current pair. What dfs basically does is remove all points that share a row or
        # a column, thus forming an island, to finally sink the island and leave us with its single representative stone
        points.remove((i, j))
        for col in cols_share_this_row[i]:
            if (i, col) in points:
                dfs(i, col)
        for row in rows_share_this_col[j]:
            if (row, j) in points:
                dfs(row, j)

    points = {(i, j) for i, j in stones}  # points set is used instead of the good old visited set
    cols_share_this_row, rows_share_this_col = defaultdict(list), defaultdict(list)
    island = 0
    for i, j in stones:
        cols_share_this_row[i].append(j)  # column coordinates of points that share the same row with i
        rows_share_this_col[j].append(i)  # row coordinates of points that share the same column with j
    for i, j in stones:
        if (i, j) in points:
            dfs(i, j)
            island += 1
    return len(stones) - island


class Test(unittest.TestCase):
    data = [([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]], 5), ([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]], 3),
            ([[0, 0]], 0)]

    def test_remove_stones(self):
        for test_stones, result in self.data:
            self.assertEqual(result, remove_stones(test_stones))


if __name__ == '__main__':
    unittest.main()
