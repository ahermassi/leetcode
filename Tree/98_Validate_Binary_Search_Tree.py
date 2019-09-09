""" Given a binary tree, determine if it is a valid binary search tree (BST). """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_valid_bst_v1(root):
    """ Iterative inorder traversal.
        Do we need to keep the whole inorder traversal list? Actually, no. The last added inorder element is enough to
        ensure at each step that the tree is BST (or not). In fact, 'inorder' variable is what should've been inserted
        into an inorder list at this point of iteration if 'inorder' was a list.
    Time complexity: O(N) in the worst case when the tree is BST or the "bad" element is a rightmost leaf.
    Space complexity: O(N) to keep stack
    """
    stack = []
    inorder = float('-inf')
    while stack or root:
        while root:
            stack.append(root)
            root = root.left
        node = stack.pop()
        if node.val <= inorder:
            return False
        inorder = node.val
        root = node.right
    return True


def is_valid_bst_v2(root):
    """ Use recursion. Pass down two parameters: lower (which means that all nodes in the the current subtree must
        be greater than this value) and upper (all must be less than it). Compare root of the current subtree
        with these two values. Then, recursively check the left and right subtree of the current one. Take care of the
        values passed down.
    Time complexity: O(N) since we visit each node exactly once
    Space complexity: O(N) since we keep up to the entire tree
    """
    def check(root, lower, upper):
        if not root:
            return True
        if not lower < root.val < upper:
            return False
        return check(root.left, lower, root.val) and check(root.right, root.val, upper)

    return check(root, float('-inf'), float('inf'))


class Test(unittest.TestCase):
    root1 = TreeNode(2)
    root1.left = TreeNode(1)
    root1.right = TreeNode(3)
    root2 = TreeNode(5)
    root2.left = TreeNode(1)
    root2.right = TreeNode(4)
    root2.right.left = TreeNode(3)
    root2.right.right = TreeNode(6)

    def test_inorder_traversal(self):
        self.assertTrue(is_valid_bst_v1(self.root1))
        self.assertFalse(is_valid_bst_v1(self.root2))
        self.assertTrue(is_valid_bst_v2(self.root1))
        self.assertFalse(is_valid_bst_v2(self.root2))


if __name__ == '__main__':
    unittest.main()

