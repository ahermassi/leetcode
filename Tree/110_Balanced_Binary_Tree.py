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


def is_balanced_v1(root):
    """ Top-down approach.
        Check whether the tree is balanced strictly according to the definition of balanced binary tree: the difference
        between the heights of the two sub trees is not greater than 1, and both the left sub tree and right sub tree
        are also balanced.
    Time complexity: O(N^2), for the current node root, calling height() for its left and right children actually has
    to access all of its children, thus the complexity is O(N). We do this for each node in the tree, so the overall
    complexity is O(N logN) because there are logN levels, but in the worst case of skewed tree the complexity is O(N^2)
    Space complexity: O(N) in the worst case
    """

    def height(root):
        if not root:
            return 0
        return 1 + max(height(root.left), height(root.right))

    if not root:
        return True
    left_height, right_height = height(root.left), height(root.right)
    if abs(left_height - right_height) > 1:
        return False
    return is_balanced_v1(root.left) and is_balanced_v1(root.right)


def is_balanced_v2(root):
    """ Bottom up approach using DFS. We return the height of the current node in DFS recursion. When the subtree of
        the current node (inclusive) is balanced, the function height() returns a non-negative value as the height.
        Otherwise -1 is returned. According to the left height and right height of the two children, the parent node
        could check if the subtree is balanced, and decides its return value.
        In other words:
        Check if the child subtrees are balanced. If they are, use their heights to determine if the current subtree is
        balanced as well as to calculate the current subtree's height.
    Time complexity: O(N) in the worst case of a skewed tree, each node in the tree only need to be accessed once
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


def is_balanced_v3(root):
    """ Exact same logic of second solution, but the code is more self-explanatory. """

    def helper(root):
        if not root:
            return True, 0  # First value of the return value indicates if tree is balanced, and if balanced the
            # second value of the return value is the height of tree
        left_height, left_balanced = helper(root.left)
        right_height, right_balanced = helper(root.right)
        height = 1 + max(left_height, right_height)
        balanced = abs(left_height - right_height) <= 1 and left_balanced and right_balanced
        return height, balanced

    return helper(root)[1]


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
        self.assertTrue(is_balanced_v1(self.root1))
        self.assertFalse(is_balanced_v2(self.root2))
        self.assertFalse(is_balanced_v3(self.root2))


if __name__ == '__main__':
    unittest.main()

