""" On a 2D plane, we place stones at some integer coordinate points.  Each coordinate point may have at most one stone.
Now, a move consists of removing a stone that shares a column or row with another stone on the grid.
What is the largest possible number of moves we can make? """

from collections import defaultdict
import unittest2 as unittest


def remove_stones(stones):
    """ Connected stones can be reduced to 1 stone, and hence the maximum number of stones that can be removed is:
        stones number - islands number.
        So just count the number of 'islands'.
        The whole problem is transformed to: What is the number of islands? You can show all your skills on a DFS
        implementation, and solve this problem as a normal one.
        The key point here is, we define an island as number of points that are connected by row or column. Every point
        does not have to be next to each other as in previous island problems.
    Time complexity: O(N^2), where N is the number of stones
    Space complexity: O(N)
    """

    def dfs(i, j):
        # With each (i, j) pair in hand, we start by verifying if the pair still exists (hasn't been removed by another
        # call to dfs). If it exists, we discard it from points set and proceed to examine all the points that share
        # the same row or column with current pair. What dfs basically does is remove all points that share a row or
        # a column and thus forming an island, to finally sink the island.
        if (i, j) in points:
            points.discard((i, j))
            for x in cols_that_share_this_row[i]:
                if (i, x) in points:
                    dfs(i, x)
            for y in rows_that_share_this_col[j]:
                if (y, j) in points:
                    dfs(y, j)

    points = {(i, j) for i, j in stones}  # points set is used instead of the good old visited set
    cols_that_share_this_row, rows_that_share_this_col = defaultdict(list), defaultdict(list)
    island = 0
    for i, j in stones:
        cols_that_share_this_row[i].append(j)  # column coordinates of points that share the same row with i
        rows_that_share_this_col[j].append(i)  # row coordinates of points that share the same column with j
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
