""" Given a binary tree, determine if it is height-balanced.
For this problem, a height-balanced binary tree is defined as:
    a binary tree in which the depth of the two subtrees of every node never differ by more than 1.
"""

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_balanced(root):
    """ Bottom up approach using DFS. We return the height of the current node in DFS recursion. When the subtree of
        the current node (inclusive) is balanced, the function height() returns a non-negative value as the height.
        Otherwise -1 is returned. According to the left height and right height of the two children, the parent node
        could check if the subtree is balanced, and decides its return value.
    Time complexity: O(N) in the worst case of a skewed tree
    Space complexity: O(N) in the worst case
    """
    def height(root):
        if not root:
            return 0
        left_height = height(root.left)
        right_height = height(root.right)
        if abs(left_height - right_height) > 1 or left_height == -1 or right_height == -1:
            return -1
        return 1 + max(left_height, right_height)

    return height(root) != -1


class Test(unittest.TestCase):
    root1 = TreeNode(3)
    root1.left = TreeNode(9)
    root1.right = TreeNode(20)
    root1.right.left = TreeNode(15)
    root1.right.right = TreeNode(7)
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(2)
    root2.left.left = TreeNode(3)
    root2.left.right = TreeNode(3)
    root2.left.left.left = TreeNode(4)
    root2.left.left.right = TreeNode(4)

    def test_is_balanced(self):
        self.assertTrue(is_balanced(self.root1))
        self.assertFalse(is_balanced(self.root2))


if __name__ == '__main__':
    unittest.main()

