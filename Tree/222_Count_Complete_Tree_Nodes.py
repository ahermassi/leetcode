""" Given a complete binary tree, count the number of nodes.

Note:
Definition of a complete binary tree from Wikipedia:
In a complete binary tree every level, except possibly the last, is completely filled, and all nodes in the last level
are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h. """

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def count_nodes_v1(root):
    """ Iterative solution. Perform a BFS on the tree and record each level. When the number of nodes in the current
        level is less than 2 ** depth, we know that we are in the last level (definition of complete binary tree).
        We eventually end up with an empty level which means the BFS traversal is done (perfect binary tree).
    Time complexity: O(N)
    Space complexity: O(2 ** h) = O(2 ** log N), since the maximum number of nodes at each level is 2 ** height of
    that level, and height == log N
    """
    if not root:
        return 0
    level, depth, count = [root], 0, 1
    while True:
        next_level = []
        for node in level:
            next_level.extend([kid for kid in (node.left, node.right) if kid])
        depth += 1
        if len(next_level) < pow(2, depth):
            return count + len(next_level)
        count += len(next_level)
        level = next_level


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    result = 6

    def test_count_nodes(self):
        self.assertEqual(self.result, count_nodes_v1(self.root))


if __name__ == '__main__':
    unittest.main()