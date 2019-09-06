""" Given preorder and inorder traversal of a tree, construct the binary tree.

Note:
You may assume that duplicates do not exist in the tree.

For example, given

preorder = [3,9,20,15,7]
inorder = [9,3,15,20,7]
Return the following binary tree:

    3
   / \
  9  20
    /  \
   15   7 """
from collections import deque

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def build_tree_v1(preorder, inorder):
    """ Looking at preorder traversal, the first value (node 1) must be the root. Then, we find the index of root within
        in-order traversal, and split into two sub problems.
        Example: preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7]
                3 is root, [9] is the left subtree, [15, 20, 7] is the right subtree, and so on (recursively)
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def get_tree(preorder, inorder):
        if inorder:
            val = preorder.popleft()
            index = inorder.index(val)
            root = TreeNode(inorder[index])
            root.left = get_tree(preorder, inorder[:index])
            root.right = get_tree(preorder, inorder[index + 1:])
            return root

    preorder = deque(preorder)  # Speed up a bit by making preorder a queue (cheap left pops as opposed to list.pop(0))
    return get_tree(preorder, inorder)


class Test(unittest.TestCase):
    preorder = [3, 9, 20, 15, 7]
    inorder = [9, 3, 15, 20, 7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    def test_is_balanced(self):
        root = build_tree_v1(self.preorder, self.inorder)
        self.assertEqual(3, root.val)
        self.assertEqual(9, root.left.val)
        self.assertEqual(20, root.right.val)
        self.assertEqual(15, root.right.left.val)
        self.assertEqual(7, root.right.right.val)


if __name__ == '__main__':
    unittest.main()
