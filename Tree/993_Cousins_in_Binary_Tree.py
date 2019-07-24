""" Two nodes of a binary tree are cousins if they have the same depth, but have different parents.
We are given the root of a binary tree with unique values, and the values x and y of two different nodes in the tree.
Return true if and only if the nodes corresponding to the values x and y are cousins. """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_cousins(root, x, y):
    """ If a node's left/right child value is either x or y then store that value along with its depth and parent node
    in a hash table (nodes). Keep track of next nodes to visit and their respective depth in a LIFO stack.
    Time complexity: O(N)
    Space complexity: O(N) used by the stack. The hash table is O(1) space because the only values stored are root, x,
    and y no matter how big N is.
    """
    nodes, stack, depth = {root.val: (0, None)}, [(0, root)], 0
    while stack:
        depth, node = stack.pop()
        if node.left:
            if node.left.val in {x, y}:
                nodes[node.left.val] = (depth + 1, node)  # depth + 1 because the node.left is in the next level
            stack.append((1 + depth, node.left))
        if node.right:
            if node.right.val in {x, y}:
                nodes[node.right.val] = (depth + 1, node)
            stack.append((1 + depth, node.right))
        if x in nodes and y in nodes:
            return nodes[x][0] == nodes[y][0] and nodes[x][1] != nodes[y][1]


class Test(unittest.TestCase):
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.left.left = TreeNode(4)
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(3)
    root2.left.right = TreeNode(4)
    root2.right.right = TreeNode(5)

    def test_is_cousins(self):
        self.assertFalse(is_cousins(self.root1, 4, 3))
        self.assertTrue(is_cousins(self.root2, 5, 4))


if __name__ == '__main__':
    unittest.main()
