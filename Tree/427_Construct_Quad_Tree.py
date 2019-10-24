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


def construct_v1(grid):
    """ Construct the tree recursively.
    Time complexity: O(N * 2 logN), where log is base 4
    Space complexity: O(logN), where log is base 4
    """
    n, m = len(grid), len(grid[0])
    if all(grid[i][j] == grid[0][0] for i in range(n) for j in range(m)):
        return Node(grid[0][0] == 1, True, None, None, None, None)
    root = Node(grid[0][0] == 1, False, None, None, None, None)
    root.topLeft = construct_v1([row[:n // 2] for row in grid[:n // 2]])
    root.topRight = construct_v1([row[n // 2:] for row in grid[:n // 2]])
    root.bottomLeft = construct_v1([row[:n // 2] for row in grid[n // 2:]])
    root.bottomRight = construct_v1([row[n // 2:] for row in grid[n // 2:]])
    return root


def construct_v2(grid):
    """ Use the results of recursive calls to improve time complexity. Each cell is examined only once.
    Time complexity: O(N ** 2)
    Space complexity: O(log N), where log is base 4
    """

    def helper(x, y, length):
        if length == 1:
            return Node(grid[0][0] == 1, True, None, None, None, None)
        root = Node(grid[0][0] == 1, False, None, None, None, None)
        topLeft = helper(x, y, length // 2)
        topRight = helper(x, y + length // 2, length // 2)
        bottomLeft = helper(x + length // 2, y, length // 2)
        bottomRight = helper(x + length // 2, y + length // 2, length // 2)
        if topLeft.isLeaf and topRight.isLeaf and bottomLeft.isLeaf and bottomRight.isLeaf and topLeft.val == \
                topRight.val and topRight.val == bottomLeft.val and bottomLeft.val == bottomRight.val:
            root.isLeaf = True
            root.val = topLeft.val
        else:
            root.topLeft = topLeft
            root.topRight = topRight
            root.bottomLeft = bottomLeft
            root.bottomRight = bottomRight
        return root

    return helper(0, 0, len(grid))

