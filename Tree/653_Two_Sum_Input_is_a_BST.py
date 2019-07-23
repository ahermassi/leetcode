""" Given a Binary Search Tree and a target number, return true if there exist two elements in the BST such that
their sum is equal to the given target. """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def find_target(root, k):
    """ Check out problem 1. Two Sum. Same logic.
    While we traverse the tree and insert nodes' values into the set, we also look back to check if current node's
    complement already exists in the set. If it exists, we have found a solution and return immediately.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    vals, nodes = set(), []
    if root:
        nodes.append(root)
    while nodes:
        node = nodes.pop()
        if node:
            if k - node.val in vals:
                return True
            vals.add(node.val)
            nodes.append(node.left)
            nodes.append(node.right)
    return False


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.right.right = TreeNode(7)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)

    def test_find_target(self):
        self.assertTrue(find_target(self.root, 9))
        self.assertFalse(find_target(self.root, 28))


if __name__ == '__main__':
    unittest.main()
