""" Given a binary tree, find its maximum depth.
The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
    3
   / \
  9  20
    /  \
   15   7
return its depth = 3.
"""

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def max_depth(root):
    """ Do it recursively.
    Time complexity: O(N)
    Space complexity: in the worst case, the tree is completely unbalanced, e.g. each node has only left child node,
    the recursion call would occur N times (the height of the tree), therefore the storage to keep the call stack
    would be O(N). But in the best case (the tree is completely balanced), the height of the tree would be log(N).
    Therefore, the space complexity in this case would be O(log(N)).
    """
    if not root:
        return 0
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    return max(left_depth, right_depth) + 1  # Add 1 to account for the root level


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    def test_max_depth(self):
        self.assertEqual(3, max_depth(self.root))


if __name__ == '__main__':
    unittest.main()

