""" Given a binary tree, return the inorder traversal of its nodes' values. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def inorder_traversal_v1(root):
    """ Recursive approach. Most straightforward.
    Time complexity: O(N) as we visit each node once
    Space complexity: O(N)
    """

    def process(root):
        if not root:
            return
        process(root.left)
        values.append(root.val)
        process(root.right)

    values = []
    process(root)
    return values


class Test(unittest.TestCase):
    root = TreeNode(7)
    root.left = TreeNode(3)
    root.right = TreeNode(15)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(20)
    result = [3, 7, 9, 15, 20]

    def test_has_cycle(self):
        self.assertEqual(self.result, inorder_traversal_v1(self.root))


if __name__ == '__main__':
    unittest.main()