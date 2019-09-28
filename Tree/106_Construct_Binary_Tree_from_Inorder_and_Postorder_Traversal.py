""" Given inorder and postorder traversal of a tree, construct the binary tree. """

import unittest2 as unittest


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def build_tree(inorder, postorder):
    """ Looking at postorder traversal, the last value must be the root. Then, we find the index of root within
            in-order traversal, and split into two sub problems.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    def helper(inorder_left, inorder_right):
        if inorder_left > inorder_right:  # If there are no elements to construct subtrees
            return None
        root = TreeNode(postorder.pop())
        index = indexes[root.val]
        root.right = helper(index + 1, inorder_right)
        root.left = helper(inorder_left, index - 1)
        return root

    indexes = {v: i for i, v in enumerate(inorder)}  # Build a map of indices of the values as they appear in inorder
    return helper(0, len(inorder) - 1)


class Test(unittest.TestCase):
    postorder = [9, 15, 7, 20, 3]
    inorder = [9, 3, 15, 20, 7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    def test_is_balanced(self):
        root = build_tree(self.inorder, self.postorder)
        self.assertEqual(3, root.val)
        self.assertEqual(9, root.left.val)
        self.assertEqual(20, root.right.val)
        self.assertEqual(15, root.right.left.val)
        self.assertEqual(7, root.right.right.val)


if __name__ == '__main__':
    unittest.main()
