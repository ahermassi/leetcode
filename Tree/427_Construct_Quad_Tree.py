""" Read description on Leetcode """


# Definition for a QuadTree node.
class Node(object):
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


def construct(grid):
    """ Construct the tree recursively.
    Time complexity: O(N * 2 logN), where log is base 4
    Space complexity: O(logN), where log is base 4
    """
    n, m = len(grid), len(grid[0])
    if all(grid[i][j] == grid[0][0] for i in range(n) for j in range(m)):
        return Node(grid[0][0] == 1, True, None, None, None, None)
    root = Node(grid[0][0] == 1, False, None, None, None, None)
    root.topLeft = construct([row[:n // 2] for row in grid[:n // 2]])
    root.topRight = construct([row[n // 2:] for row in grid[:n // 2]])
    root.bottomLeft = construct([row[:n // 2] for row in grid[n // 2:]])
    root.bottomRight = construct([row[n // 2:] for row in grid[n // 2:]])
    return root

